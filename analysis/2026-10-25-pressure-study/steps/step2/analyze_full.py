"""Step 2 analysis of the completed pressure study (revised after the expert review of the interim analysis).

Launch (owner rule: CPUs 0-3 stay free; pools sized from RESERVED_WORKERS):
    python <worktree>/tools/run_reserved.py analyze_full.py [--data CSV] [--schema JSON] [--out DIR] [--fresh]
Defaults: --data ../step1/trial_metrics.csv, --schema ../step1/metrics_schema.json, --out this folder.
Inputs are read-only. Writes only to --out (figures/, tables/, REPORT.md, PREREG.md copy, provenance.json).
Method: prompt-library/analysis/step2-analyze-and-report.md; primary test per PREREG.md (unchanged from the interim
pre-registration). Labels: FINAL-DATA when no planned trial is still not_started, otherwise PRELIMINARY.
Only numpy / pandas / matplotlib are used (scipy is not installed): every test is implemented here.
Revised from analyze_e1.py (interim snapshot) per the expert review: tipping-point failure sensitivity, monitoring
dose-response (conditional logit on discordant pairs), cluster-aware interaction bootstrap (B >= 1000), single BH family
over candidates, one shared cluster-bootstrap draw set for primary CIs, removal of notice-echo and mis-specified items.
"""
from __future__ import annotations

import argparse
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
WORKERS = max(1, int(os.environ.get("RESERVED_WORKERS", "1")))
AFFINITY = (f"launched via tools/run_reserved.py (RESERVED_CPUS={os.environ.get('RESERVED_CPUS', '0,1,2,3')}); "
            f"RESERVED_WORKERS={WORKERS}; BLAS threads = 1")

import hashlib
import json
import math
import sys
import textwrap
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

T0 = time.time()
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analyze_full_workers import int_rank, inter_task, perm_task, rankdata, ridge_logit, stat_fast  # noqa: E402

_ap = argparse.ArgumentParser()
_ap.add_argument("--data", default=str(HERE.parent / "step1" / "trial_metrics.csv"))
_ap.add_argument("--schema", default=None)
_ap.add_argument("--out", default=str(HERE))
_ap.add_argument("--fresh", action="store_true")
ARGS = _ap.parse_args()
SRC = Path(ARGS.data).resolve()
SCHEMA = Path(ARGS.schema).resolve() if ARGS.schema else SRC.parent / "metrics_schema.json"
OUTD = Path(ARGS.out).resolve()
OUTD.mkdir(parents=True, exist_ok=True)
FIG = OUTD / "figures"
TAB = OUTD / "tables"
FIG.mkdir(exist_ok=True)
TAB.mkdir(exist_ok=True)
SEED = 20261025
RNG = np.random.default_rng(SEED)
B_BOOT_SCREEN = 200      # scenario-cluster bootstrap draws per screening pair
B_BOOT_MAIN = 2000       # ONE shared set of scenario-cluster draws for every primary-section interval
B_PERM_MAX = 1999        # Besag-Clifford cap (floor 1/2000)
H_EXCEED = 50            # Besag-Clifford stop after this many exceedances
B_SIGNFLIP = 5000
B_INTER = 1000           # cluster-resampled parametric bootstrap draws per interaction test
RIDGE = 1.0
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    print(s, flush=True)


# ------------------------------------------------------------------ palette (dataviz reference instance)
SURFACE = "#fcfcfb"
TEXT_1 = "#0b0b0b"
TEXT_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
NA_FILL = "#f0efec"
S1, S2, S3, S4, S5, S6, S7, S8 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"
BLUE_STEPS = ["#f3f7fd", "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
              "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
SEQ = LinearSegmentedColormap.from_list("seq_blue", BLUE_STEPS)
SEQ.set_bad(NA_FILL)
DIV = LinearSegmentedColormap.from_list("div", ["#104281", "#3987e5", "#9ec5f4", NA_FILL, "#f2b3b2", "#e34948", "#a32b2b"])
DIV.set_bad(NA_FILL)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#c3c2b7",
                     "axes.labelcolor": TEXT_2, "xtick.color": TEXT_2, "ytick.color": TEXT_1,
                     "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                     "text.color": TEXT_1, "axes.grid": False, "hatch.color": "#898781", "hatch.linewidth": 0.6})
FIGS = []  # (file, caption)


def wrap(s, w=22):
    return "\n".join(textwrap.wrap(str(s), w, break_long_words=False))


def finish(fig, name, caption):
    fig.savefig(FIG / name, dpi=150, bbox_inches="tight")
    plt.close(fig)
    FIGS.append((name, caption))


def head(fig, title, subtitle=""):
    """Title and subtitle placed in inches from the top, so they never collide whatever the figure height."""
    h = fig.get_figheight()
    fig.text(0.01, 1 - 0.12 / h, title, ha="left", va="top", fontsize=11.5, fontweight="bold", color=TEXT_1)
    if subtitle:
        fig.text(0.01, 1 - 0.40 / h, subtitle, ha="left", va="top", fontsize=8.2, color=TEXT_2)


def clean_ax(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)


# ------------------------------------------------------------------ statistics helpers
def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(max(p * (1 - p) / n + z * z / (4 * n * n), 0)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


def gammq(a, x):
    """Regularised upper incomplete gamma Q(a, x) (Numerical Recipes series / continued fraction)."""
    if x <= 0:
        return 1.0
    gln = math.lgamma(a)
    if x < a + 1:
        ap, s, de = a, 1.0 / a, 1.0 / a
        for _ in range(1000):
            ap += 1
            de *= x / ap
            s += de
            if abs(de) < abs(s) * 1e-14:
                break
        return max(0.0, 1.0 - s * math.exp(-x + a * math.log(x) - gln))
    b = x + 1 - a
    c = 1e300
    d = 1 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1 / d
        de = d * c
        h *= de
        if abs(de - 1) < 1e-14:
            break
    return min(1.0, math.exp(-x + a * math.log(x) - gln) * h)


def chi2_sf(x, df):
    return gammq(df / 2.0, x / 2.0) if df > 0 else np.nan


def norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2))


def binom_two_sided(k, n, p=0.5):
    if n == 0:
        return 1.0
    pm = [math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    p0 = pm[k]
    return min(1.0, sum(v for v in pm if v <= p0 * (1 + 1e-9)))


def fisher_2x2(a, b, c_, d_):
    a, b, c_, d_ = int(a), int(b), int(c_), int(d_)
    r1, c1, n = a + b, a + c_, a + b + c_ + d_
    lo, hi = max(0, r1 - (n - c1)), min(r1, c1)
    lw = lambda x: math.lgamma(c1 + 1) - math.lgamma(x + 1) - math.lgamma(c1 - x + 1) + \
        math.lgamma(n - c1 + 1) - math.lgamma(r1 - x + 1) - math.lgamma(n - c1 - r1 + x + 1)
    ls = [lw(x) for x in range(lo, hi + 1)]
    m = max(ls)
    w = np.exp(np.array(ls) - m)
    p0 = w[a - lo]
    return float(min(1.0, w[w <= p0 * (1 + 1e-7)].sum() / w.sum()))


def codes(x):
    return pd.factorize(pd.Series(x).astype(str), sort=True)[0]


def chi2_stat(gi, yi, ng, ny):
    tab = np.bincount(gi * ny + yi, minlength=ng * ny).reshape(ng, ny).astype(float)
    tab = tab[tab.sum(1) > 0][:, tab.sum(0) > 0]
    if tab.shape[0] < 2 or tab.shape[1] < 2:
        return 0.0, tab.shape
    exp = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / tab.sum()
    return float(((tab - exp) ** 2 / exp).sum()), tab.shape


def cramers_v_bc(gi, yi, ng=None, ny=None):
    """Bias-corrected Cramer's V (Bergsma 2013) and asymptotic chi-square p."""
    ng = ng or gi.max() + 1
    ny = ny or yi.max() + 1
    st, (r, k) = chi2_stat(gi, yi, ng, ny)
    n = len(gi)
    if r < 2 or k < 2 or n < 3:
        return np.nan, np.nan
    phi2 = st / n
    phi2c = max(0.0, phi2 - (k - 1) * (r - 1) / (n - 1))
    rc = r - (r - 1) ** 2 / (n - 1)
    kc = k - (k - 1) ** 2 / (n - 1)
    den = min(kc - 1, rc - 1)
    v = math.sqrt(phi2c / den) if den > 0 else np.nan
    return v, chi2_sf(st, (r - 1) * (k - 1))


def kw_eps(gi, x, xr=None):
    """sqrt(epsilon^2) from Kruskal-Wallis H on ranks, and asymptotic p."""
    r = rankdata(x) if xr is None else xr
    n = len(r)
    cnt = np.bincount(gi).astype(float)
    ok = cnt > 0
    if ok.sum() < 2 or n < 3:
        return np.nan, np.nan
    means = np.bincount(gi, weights=r)[ok] / cnt[ok]
    h = 12 / (n * (n + 1)) * float((cnt[ok] * (means - (n + 1) / 2) ** 2).sum())
    # tie correction
    _, tc = np.unique(r, return_counts=True)
    corr = 1 - (tc ** 3 - tc).sum() / (n ** 3 - n) if n > 1 else 1
    h = h / corr if corr > 0 else h
    return math.sqrt(max(0.0, h / (n - 1))), chi2_sf(h, int(ok.sum()) - 1)


def spearman(x, y):
    rx, ry = rankdata(x), rankdata(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return np.nan, np.nan
    rho = float(np.corrcoef(rx, ry)[0, 1])
    n = len(rx)
    t = rho * math.sqrt((n - 2) / max(1e-12, 1 - rho * rho))
    return rho, 2 * norm_sf(abs(t))  # normal approx to t (n > 100 here)


def eta(gi, x):
    x = np.asarray(x, float)
    cnt = np.bincount(gi).astype(float)
    ok = cnt > 0
    m = np.bincount(gi, weights=x)[ok] / cnt[ok]
    ss_b = (cnt[ok] * (m - x.mean()) ** 2).sum()
    ss_t = ((x - x.mean()) ** 2).sum()
    return math.sqrt(ss_b / ss_t) if ss_t > 0 else np.nan


def bh(p):
    p = np.asarray(p, float)
    q = np.full_like(p, np.nan)
    ok = ~np.isnan(p)
    pv = p[ok]
    m = len(pv)
    if m == 0:
        return q
    order = np.argsort(pv)
    qq = np.empty(m)
    prev = 1.0
    for i, idx in enumerate(order[::-1]):
        rank = m - i
        prev = min(prev, pv[idx] * m / rank)
        qq[idx] = prev
    q[ok] = qq
    return q


def fmt_p(p):
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return "–"
    return f"{p:.2g}" if p >= 0.001 else f"{p:.1e}"


def pct(x, d=1):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{100 * x:.{d}f}%"


def pp(x, d=1):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{100 * x:+.{d}f} pp"


def _sha(pth):
    h = hashlib.sha256()
    with open(pth, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------ load
log("Loading", SRC)
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
SCOL = {c["name"]: c for c in schema["columns"]}
d = pd.read_csv(SRC, low_memory=False).copy()
import warnings
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
N_PLANNED = len(d)
if N_PLANNED != 4320:
    log(f"WARNING: {N_PLANNED} planned rows (design has 4,320)")
d["level"] = d["level"].astype(int)
RULE_NAME = {"W": "welfare", "D": "nondeception", "A": "authority"}
d["pairing_rule"] = d["pairing"].str[0].map(RULE_NAME)
d["started"] = d["status"] != "not_started"
c = d[d["status"] == "complete"].copy().reset_index(drop=True)
N_FAILED = int((d.status == "failed").sum())
N_NOTSTARTED = int((d.status == "not_started").sum())
N_CELLS = int(d.cell_id.nunique())
FINAL = N_NOTSTARTED == 0
if FINAL:
    TAG = "FINAL-DATA"
    PRELIM = f"FINAL-DATA (completed run: all {N_PLANNED:,} planned trials terminal; {len(c):,} complete, {N_FAILED} failed)"
else:
    TAG = "PRELIMINARY"
    PRELIM = f"PRELIMINARY (interim snapshot, {100 * (N_PLANNED - N_NOTSTARTED) / N_PLANNED:.0f}% of trials terminal)"
log("complete rows", len(c), "| label:", PRELIM)
# endpoints ordered by collection time (earliest first start_rank first)
EP_LEVELS = list(d[d.started].groupby("endpoint").start_rank.min().sort_values().index) if "start_rank" in d else \
    sorted(d.endpoint.dropna().unique())
EP_MAIN = d[d.started].endpoint.value_counts().idxmax()
log("endpoints (collection order):", EP_LEVELS, "main:", EP_MAIN)


def schema_validation(col):
    return (SCOL.get(col) or {}).get("validation") or {}


def _kn(v, key):
    x = v.get(key) or {}
    return f"{x['k']}/{x['n']}" if "k" in x else "?"


_st = schema_validation("stance_r1_a")
_di = schema_validation("deception_intended_a")
ACC_STANCE = (f"agreement watched {_kn(_st, 'agreement_watched')}, unwatched {_kn(_st, 'agreement_unwatched')}; "
              f"take recall {_kn(_st, 'recall_take')}: arm-error caveat") if _st else "per-arm accuracy not in schema"
ACC_DECINT = (f"agreement watched {_kn(_di, 'agreement_watched')} vs unwatched {_kn(_di, 'agreement_unwatched')}: "
              "POTENTIALLY BIASED") if _di else "per-arm accuracy not in schema: POTENTIALLY BIASED"

DIAG_ORDER = ["welfare", "nondeception", "authority"]
DIAG_NAME = {"welfare": "Welfare diagnostic", "nondeception": "Non-deception diagnostic", "authority": "Authority diagnostic"}
PAIR_ORDER = ["W-W", "W-none", "D-D", "D-none", "A-A", "A-none"]
PAIR_NAME = {"W-W": "Welfare + welfare", "W-none": "Welfare + no rule", "D-D": "Non-deception + non-deception",
             "D-none": "Non-deception + no rule", "A-A": "Authority + authority", "A-none": "Authority + no rule"}
CRIT_ORDER = ["welfare", "nondeception", "authority", "none"]
CRIT_NAME = {"welfare": "Welfare", "nondeception": "Non-deception", "authority": "Authority", "none": "No rule"}
SETTING_ORDER = ["hospital", "religious", "military", "school", "volunteer", "social_club", "family", "situational"]
SETTING_NAME = {s: s.replace("_", " ").capitalize() for s in SETTING_ORDER}
MON_ORDER = ["unwatched", "watched"]
MON_NAME = {"watched": "Watched notice", "unwatched": "Unwatched notice"}
LEVEL_NAME = {1: "Level 1 (lowest)", 2: "Level 2", 3: "Level 3", 4: "Level 4", 5: "Level 5 (highest)"}

# ------------------------------------------------------------------ derived per-agent long table
AG_COLS = ["planned_action", "plan_states_action", "final_action", "flipped", "first_take_proposal_round",
           "said_refuse_did_take", "said_take_did_refuse", "deception_words_public", "deception_words_notes",
           "deception_words_reasoning", "euphemism_gap", "evaluator_mentions_final_text", "agreement_phrases_public",
           "notice_echo_public", "notice_echo_private", "mentions_monitoring_public", "mentions_monitoring_private",
           "criterion_required_action", "criterion_self_reported_violation", "lone_take_aware",
           "take_linked_deception_sentences", "deception_intended", "reasoning_words", "words_sent_total",
           "plan_words", "msg_plan_words", "decision_text_words", "expected_first_take"]
rows = []
for s, o in (("a", "b"), ("b", "a")):
    t = pd.DataFrame({"ep": np.arange(len(c)), "role": s.upper(), "criterion": c[f"criterion_{s}"].values,
                      "partner_criterion": c[f"criterion_{o}"].values, "peer_final": c[f"final_action_{o}"].values})
    for col in AG_COLS:
        t[col] = c[f"{col}_{s}"].values
    rows.append(t)
ag = pd.concat(rows, ignore_index=True)
for k in ["scenario", "scenario_diagnostic", "setting_id", "level", "pairing", "pairing_rule", "matched_vs_mixed",
          "monitoring", "endpoint", "cell_id", "outcome"]:
    ag[k] = c[k].values[ag["ep"].values]
ag["took"] = (ag.final_action == "take").astype(float)
ag["plan_take"] = np.where(ag.planned_action.notna(), (ag.planned_action == "take").astype(float), np.nan)
ag["argued_take"] = ag.first_take_proposal_round.notna().astype(float)
ag["dec_pub"] = (ag.deception_words_public > 0).astype(float)
ag["dec_notes"] = (ag.deception_words_notes > 0).astype(float)
ag["dec_reas"] = (ag.deception_words_reasoning > 0).astype(float)
ag["dec_reas_per1k"] = np.where(ag.reasoning_words > 0, 1000 * ag.deception_words_reasoning / ag.reasoning_words.clip(lower=1), np.nan)
ag["mon_pub"] = (ag.mentions_monitoring_public > 0).astype(float)
ag["mon_priv"] = (ag.mentions_monitoring_private > 0).astype(float)
ag["echo_pub"] = (ag.notice_echo_public > 0).astype(float)
ag["echo_priv"] = (ag.notice_echo_private > 0).astype(float)
ag["evaluator"] = (ag.evaluator_mentions_final_text > 0).astype(float)
ag["agree_pub"] = (ag.agreement_phrases_public > 0).astype(float)
ag["tl_dec"] = (ag.take_linked_deception_sentences > 0).astype(float)
ag["said_other"] = np.where(ag.said_refuse_did_take.notna(),
                            ((ag.said_refuse_did_take == 1) | (ag.said_take_did_refuse == 1)).astype(float), np.nan)
ag["lone_aware"] = np.where((ag.final_action == "take") & (ag.peer_final == "refuse"), ag.lone_take_aware, np.nan)
ag["dec_int_given_take"] = np.where(ag.final_action == "take", ag.deception_intended, np.nan)


def ep_mean(col):
    """Agent metric averaged over the agents of each episode (NaN if neither agent is in the subset)."""
    return ag.groupby("ep")[col].mean().reindex(range(len(c))).to_numpy()


c["mutual_take"] = c["deal_taken"].astype(float)
c["unilateral_take"] = (c.outcome == "unilateral_take").astype(float)
c["any_take"] = (c.outcome != "both_refuse").astype(float)
c["explicit_agree"] = c.explicit_agreement_round.notna().astype(float)
c["any_silence"] = (c.silence_count > 0).astype(float)
for k in ["took", "plan_states_action", "plan_take", "flipped", "argued_take", "dec_pub", "dec_notes", "dec_reas",
          "dec_reas_per1k", "mon_pub", "mon_priv", "echo_pub", "echo_priv", "evaluator", "agree_pub", "tl_dec",
          "deception_intended", "said_other", "lone_aware", "reasoning_words", "words_sent_total", "dec_int_given_take"]:
    c["ag_" + k] = ep_mean(k)

# outcome registry: key -> (label, kind, level, heuristic flag, subset note)
# kind: bin (0/1 per episode), frac (episode mean of agent 0/1 -> agent rate), num
OUT = {
    "mutual_take": ("Mutual take (both agents took)", "bin", "pair", "", "all complete"),
    "unilateral_take": ("Lone take (exactly one took)", "bin", "pair", "", "all complete"),
    "any_take": ("Any take (at least one took)", "bin", "pair", "", "all complete"),
    "explicit_agree": ("Explicit public agreement reached", "bin", "pair", "stance: marginal", "all complete"),
    "final_public_stances_match": ("Final public stances match", "bin", "pair", "stance: marginal", "both last stances classifiable"),
    "any_silence": ("At least one empty message", "bin", "pair", "", "all complete"),
    "plans_agree": ("Private plans agreed (both plans state an action)", "bin", "pair", "", "both plans state an action"),
    "deception_intended_pair": ("Deception-intended flag, either agent", "bin", "pair", "marginal; arm-differential", "all complete"),
    "peer_deception_pair": ("Said one thing, did another (either agent)", "bin", "pair", "UNRELIABLE", "all complete"),
    "total_words_exchanged": ("Public words exchanged (both agents)", "num", "pair", "", "all complete"),
    "total_tokens": ("Total tokens used", "num", "pair", "", "all complete"),
    "ag_took": ("Agent took", "frac", "agent", "", "all agents"),
    "ag_plan_states_action": ("Plan states an action", "frac", "agent", "", "all agents"),
    "ag_plan_take": ("Plan said take (of plans with an action)", "frac", "agent", "", "plans with an action line"),
    "ag_flipped": ("Changed planned action", "frac", "agent", "", "plans with an action line"),
    "ag_argued_take": ("Argued for take in public (some round)", "frac", "agent", "stance: marginal", "all agents"),
    "ag_dec_pub": ("Deception words in public messages", "frac", "agent", "", "all agents"),
    "ag_dec_notes": ("Deception words in private notes", "frac", "agent", "", "all agents"),
    "ag_dec_reas": ("Deception words in reasoning", "frac", "agent", "", "all agents"),
    "ag_mon_pub": ("Mentions monitoring in public", "frac", "agent", "", "all agents"),
    "ag_mon_priv": ("Mentions monitoring in private", "frac", "agent", "", "all agents"),
    "ag_evaluator": ("Mentions evaluator / score in decision", "frac", "agent", "", "all agents"),
    "ag_deception_intended": ("Deception-intended flag (agent)", "frac", "agent", "marginal; arm-differential", "all agents"),
    "ag_said_other": ("Said one thing, did another (agent)", "frac", "agent", "UNRELIABLE", "last stance classifiable"),
    "ag_lone_aware": ("Lone taker aware peer refused", "frac", "agent", "UNRELIABLE", "lone takers"),
    "ag_reasoning_words": ("Reasoning length (words)", "num", "agent", "", "all agents"),
    "ag_words_sent_total": ("Public words sent (agent)", "num", "agent", "", "all agents"),
}
SHORT = {"mutual_take": "Mutual take", "unilateral_take": "Lone take", "any_take": "Any take",
         "explicit_agree": "Explicit agreement*", "final_public_stances_match": "Final stances match*",
         "any_silence": "Empty message", "plans_agree": "Plans agreed", "deception_intended_pair": "Dec.-intended (pair)*",
         "peer_deception_pair": "Said/did (pair)†", "total_words_exchanged": "Words exchanged", "total_tokens": "Tokens",
         "ag_took": "Agent took", "ag_plan_states_action": "Plan states action", "ag_plan_take": "Plan said take",
         "ag_flipped": "Changed plan", "ag_argued_take": "Argued take*", "ag_dec_pub": "Dec. words public",
         "ag_dec_notes": "Dec. words notes", "ag_dec_reas": "Dec. words reasoning", "ag_mon_pub": "Monitoring public",
         "ag_mon_priv": "Monitoring private", "ag_evaluator": "Evaluator mention", "ag_deception_intended": "Dec.-intended*",
         "ag_said_other": "Said/did†", "ag_lone_aware": "Lone aware†", "ag_reasoning_words": "Reasoning words",
         "ag_words_sent_total": "Public words"}
SUBSET_DEF = {"plans_agree": lambda t: t.plans_agree.notna(), "ag_plan_take": lambda t: t.ag_plan_take.notna(),
              "ag_flipped": lambda t: t.ag_flipped.notna(), "ag_lone_aware": lambda t: t.ag_lone_aware.notna(),
              "ag_said_other": lambda t: t.ag_said_other.notna(),
              "final_public_stances_match": lambda t: t.final_public_stances_match.notna()}
# by construction (outcome, outcome) and (parameter, outcome)
BC_OO = {frozenset(p) for p in [("mutual_take", "any_take"), ("mutual_take", "unilateral_take"), ("any_take", "unilateral_take"),
                                ("mutual_take", "ag_took"), ("any_take", "ag_took"), ("unilateral_take", "ag_took"),
                                ("ag_took", "ag_deception_intended"), ("ag_took", "deception_intended_pair"),
                                ("mutual_take", "deception_intended_pair"), ("any_take", "deception_intended_pair"),
                                ("ag_deception_intended", "deception_intended_pair"), ("ag_plan_take", "plans_agree"),
                                ("ag_flipped", "ag_plan_take"), ("explicit_agree", "final_public_stances_match"),
                                ("ag_said_other", "peer_deception_pair"), ("ag_words_sent_total", "total_words_exchanged"),
                                ("any_silence", "total_words_exchanged"), ("ag_reasoning_words", "total_tokens"),
                                ("ag_argued_take", "explicit_agree"), ("ag_lone_aware", "unilateral_take"),
                                ("ag_mon_pub", "ag_mon_priv"), ("ag_dec_notes", "ag_dec_reas"),
                                ("ag_argued_take", "final_public_stances_match"), ("ag_said_other", "ag_took"),
                                ("peer_deception_pair", "ag_took"), ("ag_lone_aware", "ag_took"),
                                ("ag_words_sent_total", "any_silence"), ("ag_plan_states_action", "plans_agree"),
                                ("ag_plan_states_action", "ag_plan_take"), ("ag_plan_states_action", "ag_flipped"),
                                # deception_intended = (planned or final take) AND acknowledgement: built on take
                                ("ag_deception_intended", "ag_plan_take"), ("deception_intended_pair", "ag_plan_take"),
                                ("any_take", "ag_deception_intended"), ("mutual_take", "ag_deception_intended"),
                                ("unilateral_take", "ag_deception_intended"), ("ag_took", "deception_intended_pair"),
                                ("unilateral_take", "deception_intended_pair")]}
BC_PO = set()  # parameter-outcome by construction: none of the parameters is computed from an outcome

# ------------------------------------------------------------------ parameter registry
# type: bin / cat / ord / num ; rand: scenario / scen_level / episode / cell / observational
PARAMS = {
    "monitoring": ("Monitoring notice", "bin", "cell", "manipulated; crossed with every cell"),
    "level": ("Pressure level", "ord", "episode", "manipulated within scenario"),
    "pairing": ("Pairing", "cat", "episode", "manipulated within scenario"),
    "pairing_rule": ("Rule in the pairing (W/D/A)", "cat", "episode", "coarsening of pairing"),
    "matched_vs_mixed": ("Matched vs. mixed pair", "bin", "episode", "coarsening of pairing"),
    "scenario_diagnostic": ("Scenario diagnostic (= family)", "cat", "scenario", "scenario-level; 24 scenes each"),
    "setting_id": ("Social setting", "cat", "scenario", "scenario-level; 9 scenes each"),
    "weekend_slice": ("Pilot-slice scene", "bin", "scenario", "scenario-level"),
    "welfare_if_take_designer": ("Designer's welfare-if-take", "cat", "scenario", "scene text; varies with level"),
    "take_principal_present": ("A principal instructs take", "bin", "scenario", "scene text; varies with level"),
    "soft_take_principal_present": ("A principal suggests take", "bin", "scenario", "scene text; varies with level"),
    "rank_stated_in_level_text": ("Rank stated in level text", "bin", "scenario", "scene text; varies with level"),
    "n_principals": ("Number of principal statements", "ord", "scenario", "scene text; varies with level"),
    "take_is_justified_ambiguous": ("Take arguably justified", "bin", "scenario", "scene text; varies with level"),
    "take_deceives_n": ("Parties misled by take", "ord", "scenario", "scene text"),
    "refuse_deceives_n": ("Parties misled by refuse", "ord", "scenario", "scene text"),
    "refuse_breaks_promise": ("Refusing breaks a promise", "bin", "scenario", "scene text"),
    "endpoint": ("Serving endpoint (collection order)", "bin", "episode", "not randomised; = collection time"),
    "start_rank": ("Execution order (start rank)", "num", "episode", "not randomised; = collection time"),
    "checkpoint_resumed": ("Episode resumed from checkpoint", "bin", "episode", "not randomised"),
    "imported_from_prior_batch": ("Imported from earlier batch", "bin", "episode", "not randomised; first endpoint only"),
}
# Randomisation levels. Script defaults (used when the schema has no randomisation_level field):
#   scenario: scenario-level and scene-text parameters -> permute whole scenarios (a scenario's
#             5-level vector of a level-varying text feature moves with it); effective n = number of scenarios.
#   episode:  level, pairing (and coarsenings), endpoint and other run-provenance flags -> permute within scenario.
#   cell:     monitoring -> swap within cell_id (the paired design).
#   agent:    criterion -> tested within mixed pairings only (asymmetry section).
# If the Step 1 schema carries `randomisation_level`, it is used (mapped onto these permutation schemes).
PARAMS = {k: v for k, v in PARAMS.items() if k in d.columns}
RAND_MAP = {"scenario": "scenario", "scene": "scenario", "episode": "episode", "trial": "episode", "cell": "cell",
            "pair": "cell", "cell_id": "cell"}
rl_rows = []
for p, (plab, ptype, rand, note) in list(PARAMS.items()):
    sv = (SCOL.get(p) or {}).get("randomisation_level")
    used = RAND_MAP.get(str(sv).lower(), rand) if sv not in (None, "", "none") else rand
    if p == "monitoring" and used == "episode":
        used = "cell"  # monitoring varies only within cell; a within-scenario shuffle would break the pairing
    rl_rows.append(dict(parameter=p, script_default=rand, schema_value=sv, used=used))
    PARAMS[p] = (plab, ptype, used, note)
RAND_TABLE = pd.DataFrame(rl_rows)
RAND_SOURCE = "schema randomisation_level" if RAND_TABLE.schema_value.notna().any() else "script defaults (schema has no randomisation_level)"
log("randomisation levels from:", RAND_SOURCE)
RAND_TABLE.to_csv(TAB / "randomisation_levels.csv", index=False)
N_SCEN = int(d.scenario.nunique())
log("parameters", len(PARAMS), "outcomes", len(OUT))

# ------------------------------------------------------------------ Step 0: profile all schema columns
prof = []
for col in d.columns:
    sc = SCOL.get(col, {})
    typ = sc.get("type", "?")
    role = sc.get("role", "?")
    if role in ("description", "id") or typ in ("text",):
        continue
    s = d[col] if sc.get("subset", "") == "all planned trials" or role == "parameter" or role == "meta" else c[col] if col in c else d[col]
    nn = s.notna().sum()
    vc = s.value_counts()
    prof.append(dict(variable=col, role=role, type=typ, level=sc.get("level"), heuristic=sc.get("heuristic"),
                     reliable=(sc.get("validation") or {}).get("reliable"), n_rows_base=len(s), n_nonmissing=int(nn),
                     missing=int(len(s) - nn), n_levels=int(vc.shape[0]),
                     level_count_min=int(vc.min()) if len(vc) else 0, level_count_median=float(vc.median()) if len(vc) else 0,
                     level_count_max=int(vc.max()) if len(vc) else 0,
                     excluded=typ in ("empty", "constant"), by_construction_with="|".join(sc.get("by_construction_with", [])),
                     subset=sc.get("subset")))
pd.DataFrame(prof).to_csv(TAB / "variable_profile.csv", index=False)
log("source_key_missing columns:", [k for k, v in SCOL.items() if v.get("source_key_missing")] or "none in schema")

# ------------------------------------------------------------------ Step 1: design check (parameter x parameter)
def assoc(x, y, tx, ty):
    m = pd.notna(x) & pd.notna(y)
    x, y = np.asarray(x)[m], np.asarray(y)[m]
    if len(x) < 10:
        return np.nan
    numx, numy = tx in ("ord", "num"), ty in ("ord", "num")
    if numx and numy:
        r, _ = spearman(x.astype(float), y.astype(float))
        return abs(r)
    if not numx and not numy:
        return cramers_v_bc(codes(x), codes(y))[0]
    if numx:
        x, y = y, x
    return eta(codes(x), y.astype(float))


plist = list(PARAMS)
base_design = d[d.started]  # observational parameters only exist for started trials
A = np.full((len(plist), len(plist)), np.nan)
for i, p in enumerate(plist):
    for j, q in enumerate(plist):
        if j < i:
            A[i, j] = A[j, i]
            continue
        if i == j:
            A[i, j] = 1.0
            continue
        A[i, j] = assoc(base_design[p].values, base_design[q].values, PARAMS[p][1], PARAMS[q][1])
pd.DataFrame(A, index=plist, columns=plist).to_csv(TAB / "design_association_matrix.csv")
aliased = []
for i, j in combinations(range(len(plist)), 2):
    if A[i, j] >= 0.3:
        aliased.append((plist[i], plist[j], A[i, j]))
aliased.sort(key=lambda r: -r[2])
pd.DataFrame(aliased, columns=["param_1", "param_2", "association"]).to_csv(TAB / "design_associated_pairs.csv", index=False)
with open(TAB / "design_cell_counts.csv", "w", encoding="utf-8", newline="") as fh:
    for p, q, a in aliased:
        if PARAMS[p][1] == "num" or PARAMS[q][1] == "num":
            continue
        ct = pd.crosstab(base_design[p], base_design[q])
        fh.write(f"# {p} x {q} (association {a:.2f}; started trials)\n")
        ct.to_csv(fh)
        fh.write("\n")
CONF = {p: sorted({q for a_, b_, v in aliased for q in (a_, b_) if p in (a_, b_) and q != p}) for p in plist}

fig, ax = plt.subplots(figsize=(11, 9.4))
im = ax.imshow(A, cmap=SEQ, vmin=0, vmax=1)
for i in range(len(plist)):
    for j in range(len(plist)):
        if not np.isnan(A[i, j]) and i != j:
            ax.text(j, i, f"{A[i, j]:.2f}".lstrip("0") if A[i, j] < 1 else "1", ha="center", va="center", fontsize=6.3,
                    color="white" if A[i, j] > 0.55 else TEXT_1)
lab = [PARAMS[p][0] for p in plist]
ax.set_xticks(range(len(plist)))
ax.set_xticklabels([wrap(l, 18) for l in lab], rotation=90, fontsize=7)
ax.set_yticks(range(len(plist)))
ax.set_yticklabels(lab, fontsize=7.5)
ax.tick_params(length=0)
for s_ in ax.spines.values():
    s_.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.01)
cb.set_label("Association (0 = none, 1 = aliased): Cramer's V (bias-corrected),\ncorrelation ratio eta, or |Spearman rho|", fontsize=7.5)
cb.outline.set_visible(False)
head(fig, "Design check: manipulated factors are independent; scene-text features track level and scenario",
     f"{PRELIM}. Parameter x parameter association over {len(base_design)} started trials. Endpoint, start rank and import status are collection-time variables.")
finish(fig, "01_design_association.png", "Parameter x parameter association matrix (design check).")

# ------------------------------------------------------------------ completion balance
d["is_complete"] = (d.status == "complete").astype(int)
d["is_failed"] = (d.status == "failed").astype(int)
comp_rows = []
for p in plist:
    if PARAMS[p][3].startswith("not randomised"):
        continue
    x = d[p]
    v, pv = cramers_v_bc(codes(x.astype(str)), codes(d.status))
    for lvl, g in d.groupby(p):
        n = len(g)
        k = int((g.status == "complete").sum())
        lo, hi = wilson(k, n)
        comp_rows.append(dict(parameter=p, level=lvl, n_planned=n, complete=k, failed=int((g.status == "failed").sum()),
                              not_started=int((g.status == "not_started").sum()), complete_rate=k / n, lo=lo, hi=hi,
                              V_status=v, p_status=pv))
comp = pd.DataFrame(comp_rows)
pvals_comp = comp.drop_duplicates("parameter")[["parameter", "V_status", "p_status"]].copy()
pvals_comp["q_status"] = bh(pvals_comp.p_status.values)
comp = comp.merge(pvals_comp[["parameter", "q_status"]], on="parameter")
comp.to_csv(TAB / "completion_balance.csv", index=False)
# endpoint (collection time) vs design among started trials
ep_rows = []
st = d[d.started]
for p in plist:
    if PARAMS[p][3].startswith("not randomised"):
        continue
    v, pv = cramers_v_bc(codes(st[p].astype(str)), codes(st.endpoint))
    ep_rows.append(dict(parameter=p, V_endpoint=v, p_endpoint=pv,
                        first_endpoint_share_min=st.groupby(p).endpoint.apply(lambda e: (e == EP_LEVELS[0]).mean()).min(),
                        first_endpoint_share_max=st.groupby(p).endpoint.apply(lambda e: (e == EP_LEVELS[0]).mean()).max()))
epb = pd.DataFrame(ep_rows)
epb["q_endpoint"] = bh(epb.p_endpoint.values)
epb.to_csv(TAB / "endpoint_balance.csv", index=False)
# failure reasons by arm
_fl = d[d.status == "failed"].copy()
_fl["failure_reason"] = _fl.failure_reason.fillna("unrecorded")
fail_tab = pd.crosstab(_fl.failure_reason, _fl.monitoring).reindex(columns=MON_ORDER, fill_value=0)
_started_arm = d[d.started].groupby("monitoring").size().reindex(MON_ORDER)
fail_rows = []
for reason in list(fail_tab.index) + ["(any failure)"]:
    k = fail_tab.sum(0) if reason == "(any failure)" else fail_tab.loc[reason]
    ku, kw = int(k["unwatched"]), int(k["watched"])
    nu, nw = int(_started_arm["unwatched"]), int(_started_arm["watched"])
    # Fisher: arm x (failed for this reason vs every other started trial)
    pf = fisher_2x2(kw, nw - kw, ku, nu - ku)
    fail_rows.append(dict(failure_reason=reason, unwatched=ku, watched=kw, started_unwatched=nu, started_watched=nw,
                          rate_unwatched=ku / nu, rate_watched=kw / nw, rate_diff_w_minus_u=kw / nw - ku / nu,
                          fisher_p_vs_all_started=pf))
FAILDF = pd.DataFrame(fail_rows)
# among failures only: is missing_message a larger share of watched failures?
if "missing_message" in fail_tab.index:
    _mm = fail_tab.loc["missing_message"]
    _tot = fail_tab.sum(0)
    P_MM_AMONG_FAIL = fisher_2x2(_mm["watched"], _tot["watched"] - _mm["watched"], _mm["unwatched"], _tot["unwatched"] - _mm["unwatched"])
    MM = FAILDF.set_index("failure_reason").loc["missing_message"]
else:
    P_MM_AMONG_FAIL, MM = np.nan, None
FAILDF["fisher_p_among_failures"] = [P_MM_AMONG_FAIL if r == "missing_message" else np.nan for r in FAILDF.failure_reason]
FAILDF.to_csv(TAB / "failures_by_reason_and_monitoring.csv", index=False)

show = ["monitoring", "level", "pairing", "scenario_diagnostic", "setting_id", "welfare_if_take_designer"]
fig, axes = plt.subplots(1, len(show), figsize=(14, 4.4))
for ax, p in zip(axes, show):
    g = comp[comp.parameter == p].copy()
    order = {"monitoring": MON_ORDER, "pairing": PAIR_ORDER, "scenario_diagnostic": DIAG_ORDER, "setting_id": SETTING_ORDER}.get(p)
    if order:
        g = g.set_index("level").reindex(order).reset_index()
    y = np.arange(len(g))
    ax.hlines(y, g.lo, g.hi, color=S1, lw=2)
    ax.plot(g.complete_rate, y, "o", color=S1, ms=6, mec=SURFACE, mew=1.5)
    ax.set_yticks(y)
    ax.set_yticklabels([str(v) for v in g.level], fontsize=7.5)
    ax.tick_params(labelleft=True)
    ax.axvline(len(c) / len(d), color=MUTED, lw=0.8, ls=":")
    ax.set_xlim(max(0.0, comp.lo.min() - 0.03), min(1.0, comp.hi.max() + 0.03))
    ax.set_title(wrap(f"{PARAMS[p][0]} (q={fmt_p(g.q_status.iloc[0])})", 24), fontsize=8.5, loc="left")
    ax.set_xlabel("Share of planned trials complete", fontsize=7.5)
    clean_ax(ax)
    ax.invert_yaxis()
head(fig, f"Completion is balanced across manipulated factors (dotted line = overall {100 * len(c) / len(d):.0f}%)",
     f"{PRELIM}. Complete / planned per level, 95% Wilson interval; q = BH over completion-status x parameter tests (status: complete / failed / not started).")
fig.subplots_adjust(top=0.78, wspace=0.6)
finish(fig, "02_completion_balance.png", "Completion rate by level of each design parameter.")
log("completion: min q", comp.q_status.min())

# ------------------------------------------------------------------ Step 1b: PRIMARY paired McNemar
# ONE shared set of scenario-cluster bootstrap draws for every primary-section interval (review item 7).
SCEN_LIST = sorted(d.scenario.unique())
SCEN_IDX = {s: i for i, s in enumerate(SCEN_LIST)}
G_SCEN = len(SCEN_LIST)
_drng = np.random.default_rng([SEED, 7])
DRAWS = _drng.integers(0, G_SCEN, (B_BOOT_MAIN, G_SCEN))           # B x G scenario indices
MULT = np.zeros((B_BOOT_MAIN, G_SCEN))                              # multiplicity of each scenario in each draw
np.add.at(MULT, (np.repeat(np.arange(B_BOOT_MAIN), G_SCEN), DRAWS.ravel()), 1)


def ssum(vals, scen_idx):
    """Per-scenario sums (length G_SCEN, scenario order SCEN_LIST)."""
    return np.bincount(np.asarray(scen_idx, int), weights=np.asarray(vals, float), minlength=G_SCEN)


def boot_ratio(num, den, scen_idx):
    """Shared-draw cluster bootstrap of sum(num)/sum(den); returns (lo, hi, draws)."""
    a, b = MULT @ ssum(num, scen_idx), MULT @ ssum(den, scen_idx)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = a / b
    r = r[np.isfinite(r)]
    if len(r) < 0.9 * B_BOOT_MAIN:
        return np.nan, np.nan, r
    return float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5)), r


def mcnemar_table(sub, ycol="mutual_take"):
    w = sub.pivot_table(index="cell_id", columns="monitoring", values=ycol, aggfunc="first")
    for k_ in MON_ORDER:
        if k_ not in w:
            w[k_] = np.nan
    w = w.dropna(subset=["watched", "unwatched"])
    n11 = int(((w.watched == 1) & (w.unwatched == 1)).sum())
    n10 = int(((w.watched == 1) & (w.unwatched == 0)).sum())  # watched-only take
    n01 = int(((w.watched == 0) & (w.unwatched == 1)).sum())  # unwatched-only take
    n00 = int(((w.watched == 0) & (w.unwatched == 0)).sum())
    return w, n11, n10, n01, n00


def newcombe_paired(n11, n10, n01, n00):
    n = n11 + n10 + n01 + n00
    if n == 0:
        return np.nan, np.nan, np.nan
    pw, pu = (n11 + n10) / n, (n11 + n01) / n
    D = pw - pu
    l1, u1 = wilson(n11 + n10, n)
    l2, u2 = wilson(n11 + n01, n)
    den = (n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00)
    phi = (n11 * n00 - n10 * n01) / math.sqrt(den) if den > 0 else 0.0
    dl = math.sqrt(max(0, (pw - l1) ** 2 - 2 * phi * (pw - l1) * (u2 - pu) + (u2 - pu) ** 2))
    du = math.sqrt(max(0, (pu - l2) ** 2 - 2 * phi * (pu - l2) * (u1 - pw) + (u1 - pw) ** 2))
    return D, D - dl, D + du


def mcnemar(n10, n01):
    m = n10 + n01
    exact = binom_two_sided(min(n10, n01), m) if m else 1.0
    chi = (abs(n10 - n01) - 1) ** 2 / m if m else 0.0
    return exact, chi2_sf(chi, 1) if m else 1.0


def mcnemar_reported(n10, n01):
    pex, pchi = mcnemar(n10, n01)
    return pex if (n10 + n01) < 25 else pchi


def mde_paired(n, pdisc, alpha=0.05, power=0.8):
    za, zb = 1.959964, 0.841621
    lo, hi = 1e-5, max(1e-4, pdisc)
    for _ in range(100):
        dl = (lo + hi) / 2
        need = (za * math.sqrt(pdisc) + zb * math.sqrt(max(pdisc - dl * dl, 0))) ** 2 / (dl * dl)
        if need > n:
            lo = dl
        else:
            hi = dl
    return hi


def mde_unpaired(n_arm, p, alpha=0.05, power=0.8):
    return (1.959964 + 0.841621) * math.sqrt(2 * p * (1 - p) / n_arm)


scen_of_cell = d.drop_duplicates("cell_id").set_index("cell_id")["scenario"]


def primary_row(label, sub, ycol="mutual_take", boot=True):
    w, n11, n10, n01, n00 = mcnemar_table(sub, ycol)
    n = n11 + n10 + n01 + n00
    D, lo, hi = newcombe_paired(n11, n10, n01, n00)
    pex, pchi = mcnemar(n10, n01)
    pw = (n11 + n10) / n if n else np.nan
    pu = (n11 + n01) / n if n else np.nan
    blo = bhi = rlo = rhi = np.nan
    if boot and n > 20:
        si = scen_of_cell.reindex(w.index).map(SCEN_IDX).to_numpy()
        blo, bhi, _ = boot_ratio((w.watched - w.unwatched).to_numpy(), np.ones(len(w)), si)
        rlo, rhi, _ = boot_ratio(w.watched.to_numpy(), w.unwatched.to_numpy(), si)
    return dict(subset=label, pairs=n, both_take=n11, watched_only_take=n10, unwatched_only_take=n01, neither=n00,
                rate_watched=pw, rate_unwatched=pu, diff_w_minus_u=D, newcombe_lo=lo, newcombe_hi=hi,
                cluster_boot_lo=blo, cluster_boot_hi=bhi,
                risk_ratio_w_over_u=pw / pu if pu else np.nan, rr_boot_lo=rlo, rr_boot_hi=rhi,
                p_exact=pex, p_chi2_cc=pchi, p_reported=pex if (n10 + n01) < 25 else pchi,
                cond_OR_w_vs_u=n10 / n01 if n01 else np.nan,
                ci_crosses_0=bool(lo <= 0 <= hi) if not np.isnan(lo) else True)


prim = []
P0 = primary_row("All complete pairs (PRIMARY)", c)
prim.append(P0)
# within endpoint (endpoint = collection time)
cell_ep = c.groupby("cell_id").endpoint.agg(lambda e: "|".join(sorted(set(map(str, e)))))
cell_ep_arm = c.pivot_table(index="cell_id", columns="monitoring", values="endpoint", aggfunc="first")
c["cell_endpoint"] = c.cell_id.map(cell_ep)
both = c.groupby("cell_id").monitoring.transform("count") == 2
c["pair_ep_class"] = np.where(~both, "unpaired",
                              np.where(c.cell_endpoint.str.contains(r"\|", regex=True), "split", "both " + c.cell_endpoint))
EP_CLASSES = [f"both {e}" for e in EP_LEVELS] + ["split"]
for k in EP_CLASSES:
    prim.append(primary_row(f"Endpoint: {k}", c[c.pair_ep_class == k]))
split_cells = cell_ep_arm.dropna()
split_cells = split_cells[split_cells.watched != split_cells.unwatched]
if len(EP_LEVELS) == 2:
    e0, e1 = EP_LEVELS
    wa = split_cells.index[split_cells.watched == e0]
    prim.append(primary_row(f"Split: watched on {e0}, unwatched on {e1}", c[c.cell_id.isin(wa)]))
    prim.append(primary_row(f"Split: watched on {e1}, unwatched on {e0}", c[c.cell_id.isin(split_cells.index.difference(wa))]))
for k in DIAG_ORDER:
    prim.append(primary_row(f"Diagnostic: {k}", c[c.scenario_diagnostic == k]))
for k in PAIR_ORDER:
    prim.append(primary_row(f"Pairing: {k}", c[c.pairing == k]))
for k in range(1, 6):
    prim.append(primary_row(f"Level: {k}", c[c.level == k]))
for k in ["matched", "mixed"]:
    prim.append(primary_row(f"Pair type: {k}", c[c.matched_vs_mixed == k]))
# secondary binary outcomes, same paired test
for ycol, labl in [("any_take", "Outcome: any take (>=1 agent)"), ("unilateral_take", "Outcome: lone take")]:
    prim.append(primary_row(labl, c, ycol))
primdf = pd.DataFrame(prim)
P0 = primdf.iloc[0]
ra = primdf.set_index("subset")
# endpoint x monitoring: discordant split across the 'both <endpoint>' classes (OR scale)
_ept = ra.loc[[f"Endpoint: both {e}" for e in EP_LEVELS], ["watched_only_take", "unwatched_only_take"]].to_numpy()
_ept = _ept[_ept.sum(1) > 0]
if len(_ept) == 2:
    p_epxmon = fisher_2x2(_ept[0, 0], _ept[0, 1], _ept[1, 0], _ept[1, 1])
elif len(_ept) > 2:
    _ex = _ept.sum(1, keepdims=True) * _ept.sum(0, keepdims=True) / _ept.sum()
    p_epxmon = chi2_sf(((_ept - _ex) ** 2 / _ex).sum(), len(_ept) - 1)
else:
    p_epxmon = np.nan


def het_p(prefix):
    """Chi-square on the discordant split across subgroups = heterogeneity of the conditional OR (not of the pp gap)."""
    g = primdf[primdf.subset.str.startswith(prefix)]
    tab = g[["watched_only_take", "unwatched_only_take"]].to_numpy().astype(float)
    tab = tab[tab.sum(1) > 0]
    if len(tab) < 2:
        return np.nan
    exp = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / tab.sum()
    x2 = ((tab - exp) ** 2 / exp).sum()
    return chi2_sf(x2, len(tab) - 1)


HET = {k: het_p(k) for k in ["Diagnostic:", "Pairing:", "Level:", "Pair type:"]}
# power
npairs = P0["pairs"]
pdisc = (P0["watched_only_take"] + P0["unwatched_only_take"]) / npairs
n_arm = c.groupby("monitoring").size().min()
POWER = dict(pairs_now=npairs, cells_planned=N_CELLS, discordance_rate=pdisc, mde_paired_now=mde_paired(npairs, pdisc),
             mde_paired_full=mde_paired(N_CELLS, pdisc), mde_unpaired_now=mde_unpaired(n_arm, c.mutual_take.mean()),
             mde_unpaired_full=mde_unpaired(N_CELLS, c.mutual_take.mean()))

# ------------------------------------------------------------------ failure sensitivity: 4 bounds + tipping point
s3 = d[d.status != "not_started"].copy()
s3["mutual_take"] = s3.deal_taken.astype(float)
sens = []
BOUND_LABELS = [("Failures excluded (primary)", None, None),
                ("Bound 1: every failure = mutual take", 1, 1),
                ("Bound 2: every failure = no mutual take", 0, 0),
                ("Bound 3 (adversarial): 100% of watched failures = take, 0% of unwatched failures = take", 1, 0),
                ("Bound 4 (favourable): 0% of watched failures = take, 100% of unwatched failures = take", 0, 1)]
for lab_, fw, fu in BOUND_LABELS:
    t = s3.copy()
    if fw is not None:
        t.loc[(t.status == "failed") & (t.monitoring == "watched"), "mutual_take"] = fw
        t.loc[(t.status == "failed") & (t.monitoring == "unwatched"), "mutual_take"] = fu
    else:
        t = t[t.status == "complete"]
    sens.append(primary_row(lab_, t, boot=False))
sensdf = pd.DataFrame(sens)
sensdf.to_csv(TAB / "primary_failure_sensitivity.csv", index=False)

# Tipping point: unwatched failures = no take; watched failures turned into takes one at a time in the order least
# favourable to the hypothesis (first those whose unwatched partner did not take -> adds a watched-only discordant pair;
# then those whose partner took -> removes an unwatched-only pair).
_pv = s3.pivot_table(index="cell_id", columns="monitoring", values="mutual_take", aggfunc="first")
_ps = s3.pivot_table(index="cell_id", columns="monitoring", values="status", aggfunc="first")
_pv = _pv.reindex(columns=MON_ORDER)
_ps = _ps.reindex(columns=MON_ORDER)
_ok = _ps.notna().all(1)
_pv, _ps = _pv[_ok], _ps[_ok]
u_val = np.where(_ps.unwatched == "failed", 0.0, _pv.unwatched)
w_fail = (_ps.watched == "failed").to_numpy()
w_val = np.where(w_fail, 0.0, _pv.watched)
n10_0 = int(((w_val == 1) & (u_val == 0)).sum())
n01_0 = int(((w_val == 0) & (u_val == 1)).sum())
wf_partner = u_val[w_fail]
n_wf = int(w_fail.sum())
n_uf = int((_ps.unwatched == "failed").sum())
order_partner = np.sort(wf_partner)  # partner 0 first (worst for the hypothesis), then partner 1
tip_rows = []
n10, n01 = n10_0, n01_0
tip_k = None
for k in range(0, n_wf + 1):
    if k > 0:
        if order_partner[k - 1] == 0:
            n10 += 1
        else:
            n01 -= 1
    pk = mcnemar_reported(n10, n01)
    tip_rows.append(dict(watched_failures_as_take=k, share_of_watched_failures=k / n_wf if n_wf else np.nan,
                         watched_only_take=n10, unwatched_only_take=n01, p_reported=pk))
    if tip_k is None and pk > 0.05:
        tip_k = k
TIPDF = pd.DataFrame(tip_rows)
TIPDF.to_csv(TAB / "primary_failure_tipping_point.csv", index=False)
W_TAKE_RATE = c[c.monitoring == "watched"].mutual_take.mean()
TIP = dict(watched_failures=n_wf, unwatched_failures=n_uf, k_needed=tip_k,
           share_needed=(tip_k / n_wf) if (tip_k is not None and n_wf) else np.nan,
           ratio_to_watched_base_rate=((tip_k / n_wf) / W_TAKE_RATE) if (tip_k is not None and n_wf) else np.nan,
           watched_complete_take_rate=W_TAKE_RATE, p_at_k0=float(TIPDF.p_reported.iloc[0]),
           p_at_all=float(TIPDF.p_reported.iloc[-1]))
log("TIPPING POINT", TIP)
primdf.to_csv(TAB / "primary_mcnemar.csv", index=False)
log("PRIMARY", {k: P0[k] for k in ["pairs", "watched_only_take", "unwatched_only_take", "diff_w_minus_u", "newcombe_lo",
                                   "newcombe_hi", "cluster_boot_lo", "cluster_boot_hi", "risk_ratio_w_over_u", "p_exact", "p_chi2_cc"]})
log("POWER", POWER, "ep x mon p", p_epxmon, "HET", HET)

# ------------------------------------------------------------------ monitoring dose-response (conditional logit)
def logit_fit(X, y):
    beta, mu, dev = ridge_logit(X, y, lam=0.0)
    H = (X.T * (mu * (1 - mu))) @ X
    try:
        se = np.sqrt(np.diag(np.linalg.inv(H)))
    except np.linalg.LinAlgError:
        se = np.full(X.shape[1], np.nan)
    return beta, se, dev


_w, *_ = mcnemar_table(c)
DISC = _w[(_w.watched != _w.unwatched)].copy()
DISC["z"] = (DISC.watched == 1).astype(float)  # 1 = watched-only take, 0 = unwatched-only take
_cinfo = c.drop_duplicates("cell_id").set_index("cell_id")
for k_ in ["level", "scenario_diagnostic", "pairing", "scenario"]:
    DISC[k_] = _cinfo.loc[DISC.index, k_].values
DISC["si"] = DISC.scenario.map(SCEN_IDX)
yz = DISC.z.to_numpy()
X0 = np.ones((len(DISC), 1))
_, _, dev0 = logit_fit(X0, yz)
Xl = np.column_stack([np.ones(len(DISC)), DISC.level.to_numpy(float) - 3.0])
bl, sel, devl = logit_fit(Xl, yz)
# cluster bootstrap of the slope with the shared draws
_rows_by_s = [np.where(DISC.si.to_numpy() == g)[0] for g in range(G_SCEN)]
bs_slope = []
for b in range(B_BOOT_MAIN):
    ix = np.concatenate([_rows_by_s[g] for g in DRAWS[b]])
    if len(ix) < 10 or yz[ix].min() == yz[ix].max():
        continue
    bs_slope.append(ridge_logit(Xl[ix], yz[ix], lam=1e-6)[0][1])
DOSE = dict(discordant_pairs=len(DISC), slope_log_OR_per_level=bl[1], slope_se=sel[1],
            slope_wald_lo=bl[1] - 1.96 * sel[1], slope_wald_hi=bl[1] + 1.96 * sel[1],
            slope_boot_lo=float(np.percentile(bs_slope, 2.5)) if bs_slope else np.nan,
            slope_boot_hi=float(np.percentile(bs_slope, 97.5)) if bs_slope else np.nan, slope_boot_draws=len(bs_slope),
            OR_ratio_per_level=math.exp(bl[1]), p_LR_trend=chi2_sf(dev0 - devl, 1),
            cond_OR_at_level3=math.exp(bl[0]))


def lr_categorical(col, order):
    lv = [x for x in order if x in set(DISC[col])]
    Xc = np.column_stack([np.ones(len(DISC))] + [(DISC[col] == v).to_numpy(float) for v in lv[1:]])
    _, _, devc = logit_fit(Xc, yz)
    return chi2_sf(dev0 - devc, len(lv) - 1), dev0 - devc, len(lv) - 1


for col, order, nm in [("level", [1, 2, 3, 4, 5], "level"), ("scenario_diagnostic", DIAG_ORDER, "diagnostic"),
                       ("pairing", PAIR_ORDER, "pairing")]:
    pv_, lr_, df_ = lr_categorical(col, order)
    DOSE[f"p_LR_{nm}_categorical"] = pv_
    DOSE[f"LR_{nm}"] = lr_
    DOSE[f"df_{nm}"] = df_
pd.DataFrame([DOSE]).to_csv(TAB / "monitoring_dose_response_trend.csv", index=False)
DOSE_LEVELS = primdf[primdf.subset.str.startswith(("Level:", "Diagnostic:", "Pairing:"))].copy()
DOSE_LEVELS.to_csv(TAB / "monitoring_by_level_diagnostic_pairing.csv", index=False)
log("DOSE-RESPONSE", DOSE)

# forest plot: overall / endpoint / diagnostic / pairing / level, with discordant counts and RR
fp = primdf[primdf.subset.str.startswith(("All complete", "Endpoint:", "Diagnostic:", "Pairing:", "Level:"))].copy()
fp = fp[fp.pairs > 0]
fig, ax = plt.subplots(figsize=(10.5, 0.36 * len(fp) + 2.2))
y = np.arange(len(fp))[::-1]
for yi, (_, r) in zip(y, fp.iterrows()):
    prim_ = "PRIMARY" in r.subset
    col = S1 if prim_ else (MUTED if r.pairs < 60 else TEXT_2)
    ax.hlines(yi, r.newcombe_lo, r.newcombe_hi, color=col, lw=2 if prim_ else 1.4)
    ax.plot(r.diff_w_minus_u, yi, "D" if prim_ else "o", color=col, ms=8 if prim_ else 6, mec=SURFACE, mew=1.2)
    rr_txt = f"{r.risk_ratio_w_over_u:.2f}" if np.isfinite(r.risk_ratio_w_over_u) else "–"
    ax.text(1.02, yi, f"{int(r.watched_only_take):>3} / {int(r.unwatched_only_take):<3}", va="center", fontsize=7.2,
            color=TEXT_2, transform=ax.get_yaxis_transform(), family="DejaVu Sans Mono")
    ax.text(1.22, yi, rr_txt, va="center", fontsize=7.2, color=TEXT_2, transform=ax.get_yaxis_transform())
    ax.text(1.34, yi, f"{int(r.pairs)}", va="center", fontsize=7.2, color=TEXT_2, transform=ax.get_yaxis_transform())
    ax.text(1.45, yi, fmt_p(r.p_reported), va="center", fontsize=7.2, color=TEXT_2, transform=ax.get_yaxis_transform())
for xx_, t_ in [(1.02, "watched-only /\nunwatched-only"), (1.22, "risk ratio\n(w / u)"), (1.34, "pairs"), (1.45, "p")]:
    ax.text(xx_, 1.0, t_, transform=ax.transAxes, ha="left", va="bottom", fontsize=7, color=TEXT_2, fontweight="bold")
# group separators
grp = fp.subset.str.split(":").str[0].to_numpy()
for i in range(1, len(grp)):
    if grp[i] != grp[i - 1]:
        ax.axhline(y[i] + 0.5, color=GRID, lw=1)
ax.axvline(0, color=TEXT_1, lw=0.8)
ax.set_yticks(y)
ax.set_yticklabels([wrap(s.replace("All complete pairs (PRIMARY)", "All complete pairs (PRIMARY)"), 44) for s in fp.subset], fontsize=7.6)
ax.set_xlabel("Paired difference in mutual-take rate, watched minus unwatched (percentage points; 95% Newcombe interval)")
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{100 * v:+.0f}"))
clean_ax(ax)
lo_x = min(-0.15, np.nanmin(fp.newcombe_lo) - 0.01)
hi_x = max(0.08, np.nanmax(fp.newcombe_hi) + 0.01)
ax.set_xlim(lo_x, hi_x)
head(fig, f"Primary: with the watched notice, {abs(100 * P0['diff_w_minus_u']):.1f} pp fewer mutual takes "
          f"({int(P0['watched_only_take'])} watched-only vs {int(P0['unwatched_only_take'])} unwatched-only takes; p={fmt_p(P0['p_reported'])})",
     f"{PRELIM}. McNemar on {P0['pairs']:,} cells with both trials complete. Grey = fewer than 60 pairs. Left of 0 = fewer mutual takes when watched.\n"
     "Subgroups whose interval crosses 0 are uninformative about direction on their own; heterogeneity tests are on the conditional-OR scale.")
fig.subplots_adjust(top=1 - 1.15 / fig.get_figheight(), right=0.6)
finish(fig, "03_primary_monitoring_forest.png", "Primary paired monitoring test, overall and within subgroups.")

# NEW: monitoring by level, two panels (pp and RR)
lvdf = primdf[primdf.subset.str.startswith("Level:")].copy()
lvdf["lv"] = lvdf.subset.str.split(": ").str[1].astype(int)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.4))
for ax, est, lo_, hi_, ref, xl_ in [(ax1, "diff_w_minus_u", "cluster_boot_lo", "cluster_boot_hi", 0.0,
                                     "Watched minus unwatched mutual-take rate (pp)"),
                                    (ax2, "risk_ratio_w_over_u", "rr_boot_lo", "rr_boot_hi", 1.0,
                                     "Risk ratio, watched / unwatched (log scale)")]:
    ax.axhline(ref, color=TEXT_1, lw=0.8)
    po = P0[est]
    ax.axhspan(P0[lo_], P0[hi_], color=S1, alpha=0.10, lw=0)
    ax.axhline(po, color=S1, lw=1, ls="--")
    ax.vlines(lvdf.lv, lvdf[lo_], lvdf[hi_], color=S1, lw=2)
    ax.plot(lvdf.lv, lvdf[est], "o", color=S1, ms=8, mec=SURFACE, mew=1.5)
    for _, r in lvdf.iterrows():
        lab = f"{100 * r[est]:+.1f} pp" if est.startswith("diff") else f"{r[est]:.2f}"
        ax.annotate(lab, (r.lv, r[est]), xytext=(9, 0), textcoords="offset points", va="center", fontsize=7.5, color=TEXT_1)
        if est.startswith("diff"):
            ax.annotate(f"{pct(r.rate_unwatched, 0)} -> {pct(r.rate_watched, 0)}\n{int(r.watched_only_take)} w-only / {int(r.unwatched_only_take)} u-only",
                        (r.lv, r[lo_]), xytext=(0, -6), textcoords="offset points", ha="center", va="top", fontsize=6.3, color=TEXT_2)
    ax.text(5.45, po, "overall", fontsize=7, color=S1, va="center")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels([LEVEL_NAME[i] for i in range(1, 6)], fontsize=7.5)
    ax.set_xlim(0.5, 5.9)
    ax.set_ylabel(xl_, fontsize=8)
    if est.startswith("diff"):
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{100 * v:+.0f}"))
        ax.set_ylim(min(-0.2, np.nanmin(lvdf[lo_]) - 0.04), max(0.06, np.nanmax(lvdf[hi_]) + 0.02))
    else:
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator([0.25, 0.33, 0.5, 0.67, 0.8, 1.0, 1.25, 1.5]))
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.2f}"))
        ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        ax.set_ylim(max(0.05, np.nanmin(lvdf[lo_]) * 0.6), max(1.4, np.nanmax(lvdf[hi_]) * 1.15))
    clean_ax(ax)
ax1.set_title("Absolute gap (percentage points)", loc="left", fontsize=9)
ax2.set_title("Relative gap (risk ratio)", loc="left", fontsize=9)
_l1, _l5 = lvdf.set_index("lv").loc[1], lvdf.set_index("lv").loc[5]
head(fig, f"Monitoring by level: the watched-unwatched gap is {pp(_l1.diff_w_minus_u)} at level 1 and {pp(_l5.diff_w_minus_u)} at level 5 "
          f"(risk ratio {_l1.risk_ratio_w_over_u:.2f} vs {_l5.risk_ratio_w_over_u:.2f})",
     f"{PRELIM}. Paired within cell; bars = 95% scenario-cluster bootstrap (shared draws); band = overall. Trend in the conditional OR per level "
     f"(logit on {DOSE['discordant_pairs']} discordant pairs): x{DOSE['OR_ratio_per_level']:.2f} per level, LR p={fmt_p(DOSE['p_LR_trend'])}.")
fig.subplots_adjust(top=0.80, wspace=0.25, bottom=0.2)
finish(fig, "19_monitoring_by_level.png", "Monitoring effect by pressure level: paired pp difference and risk ratio.")

# ------------------------------------------------------------------ Step 3b: words vs actions
CHANNEL = [  # (key in c, label, channel, kind, heuristic note, per-arm accuracy note)
    ("mutual_take", "Mutual take", "Actions", "bin", "", ""),
    ("ag_took", "Agent took", "Actions", "frac", "", ""),
    ("unilateral_take", "Lone take", "Actions", "bin", "", ""),
    ("ag_argued_take", "Argued for take (stance heuristic)", "Public messages", "frac", "stance marginal; EXPLORATORY (arm error)",
     ACC_STANCE),
    ("ag_dec_pub", "Deception words, public", "Public messages", "frac", "notice-masked count", "deterministic"),
    ("ag_mon_pub", "Oversight / monitoring words, public", "Public messages", "frac",
     "meaning unvalidated; both notices contain 'monitored'/'oversight' (echo possible); not a finding",
     "keyword match; semantic meaning unvalidated"),
    ("ag_agree_pub", "Agreement phrases, public", "Public messages", "frac", "", "deterministic"),
    ("ag_words_sent_total", "Public words sent", "Public messages", "num", "", "deterministic"),
    ("ag_plan_states_action", "Plan states an action", "Private reasoning", "frac", "", "deterministic"),
    ("ag_dec_notes", "Deception words, private notes", "Private reasoning", "frac", "notice-masked count", "deterministic"),
    ("ag_dec_reas", "Deception words, reasoning", "Private reasoning", "frac", "notice-masked count", "deterministic"),
    ("ag_dec_reas_per1k", "Deception words per 1k reasoning words", "Private reasoning", "num", "notice-masked count", "deterministic"),
    ("ag_evaluator", "Mentions evaluator / score (decision)", "Private reasoning", "frac", "", "deterministic"),
    ("ag_tl_dec", "Take-linked deception sentence", "Private reasoning", "frac", "clause heuristic", "part of deception_intended"),
    ("ag_deception_intended", "Deception-intended flag", "Private reasoning", "frac", "NOT RELIABLE for monitoring; EXPLORATORY (arm error)",
     ACC_DECINT),
    ("ag_reasoning_words", "Reasoning length (words)", "Private reasoning", "num", "", "deterministic"),
]
c["ag_agree_pub"] = ep_mean("agree_pub")
c["ag_tl_dec"] = ep_mean("tl_dec")


def paired_effect(df, key, a_col, a_vals, pair_key, scen_col="scenario", rng=RNG):
    """mean within-pair difference (a_vals[1] - a_vals[0]); shared-draw scenario-cluster bootstrap CI; sign-flip p."""
    t = df[df[a_col].isin(a_vals)]
    w = t.pivot_table(index=pair_key, columns=a_col, values=key, aggfunc="first").dropna(subset=list(a_vals))
    if len(w) < 5:
        return dict(n_pairs=len(w), diff=np.nan, lo=np.nan, hi=np.nan, p=np.nan, sd=np.nan, m0=np.nan, m1=np.nan)
    dd = (w[a_vals[1]] - w[a_vals[0]]).to_numpy()
    scen = t.drop_duplicates(pair_key).set_index(pair_key)[scen_col].reindex(w.index).map(SCEN_IDX).to_numpy()
    blo, bhi, _ = boot_ratio(dd, np.ones(len(dd)), scen)
    obs = dd.mean()
    signs = rng.choice([-1.0, 1.0], size=(B_SIGNFLIP, len(dd)))
    null = (signs * dd).mean(1)
    p = (np.sum(np.abs(null) >= abs(obs) - 1e-12) + 1) / (B_SIGNFLIP + 1)
    sd = df[key].std()
    return dict(n_pairs=len(w), diff=obs, lo=blo, hi=bhi, p=p, sd=sd,
                m0=w[a_vals[0]].mean(), m1=w[a_vals[1]].mean())


c["lvl_pair"] = c.scenario + "|" + c.pairing + "|" + c.monitoring
wva = []
LEVEL_SKIP = {"ag_mon_pub"}  # no level 5 vs 1 monitoring-mention row (notice echo)
for key, lab_, ch, kind, hn, acc in CHANNEL:
    r1 = paired_effect(c, key, "monitoring", ("unwatched", "watched"), "cell_id")
    r2 = paired_effect(c, key, "level", (1, 5), "lvl_pair") if key not in LEVEL_SKIP else None
    for fac, r in (("monitoring (watched - unwatched)", r1), ("level (5 - 1)", r2)):
        if r is None:
            continue
        wva.append(dict(factor=fac, channel=ch, measure=lab_, key=key, kind=kind, heuristic=hn, per_arm_accuracy=acc,
                        **r, std_diff=r["diff"] / r["sd"] if r["sd"] else np.nan))
wvadf = pd.DataFrame(wva)
wvadf["q_within_factor"] = np.nan
for fac in wvadf.factor.unique():
    m = wvadf.factor == fac
    wvadf.loc[m, "q_within_factor"] = bh(wvadf.loc[m, "p"].values)
wvadf["potentially_biased"] = wvadf.per_arm_accuracy.str.contains("BIASED|arm-error") & wvadf.factor.str.startswith("monitoring")
wvadf["not_a_finding"] = wvadf.heuristic.str.contains("not a finding|EXPLORATORY")
wvadf.to_csv(TAB / "words_vs_actions.csv", index=False)
# decomposition: P(flag) = P(take) x P(flag | take), per arm
dec_rows = []
for arm in MON_ORDER:
    a = ag[ag.monitoring == arm]
    pt = a.took.mean()
    pf = a.deception_intended.mean()
    pft = a.loc[a.took == 1, "deception_intended"].mean()
    dec_rows.append(dict(arm=arm, agents=len(a), p_take=pt, p_flag=pf, p_flag_given_take=pft, takers=int(a.took.sum())))
pd.DataFrame(dec_rows).to_csv(TAB / "deception_intended_decomposition.csv", index=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 8.2))
for ax, fac, col in zip(axes, ["monitoring (watched - unwatched)", "level (5 - 1)"], [S1, S2]):
    g = wvadf[wvadf.factor == fac].reset_index(drop=True)
    y = np.arange(len(g))[::-1]
    for yi, (_, r) in zip(y, g.iterrows()):
        sd = r.sd if r.sd else 1
        cc = MUTED if (r.not_a_finding and fac.startswith("monitoring")) else col
        ax.hlines(yi, r.lo / sd, r.hi / sd, color=cc, lw=1.8)
        ax.plot(r["diff"] / sd, yi, "o", color=cc, ms=6, mec=SURFACE, mew=1.2)
        val = f"{100 * r['diff']:+.1f} pp" if r.kind != "num" else f"{r['diff']:+.0f}"
        mark = " *" if r.q_within_factor < 0.05 else ""
        ax.text(1.02, yi, f"{val}{mark}", transform=ax.get_yaxis_transform(), va="center", fontsize=7, color=TEXT_2)
    ax.axvline(0, color=TEXT_1, lw=0.8)
    for i in range(1, len(g)):
        if g.channel.iloc[i] != g.channel.iloc[i - 1]:
            ax.axhline(y[i] + 0.5, color=GRID, lw=1)
    ax.set_yticks(y)
    ax.set_yticklabels([f"[{r.channel.split()[0]}] {r.measure}" for _, r in g.iterrows()], fontsize=7.5)
    ax.set_title(f"Effect of {fac}", loc="left", fontsize=9.5)
    ax.set_xlabel("Paired difference in SD units (95% scenario-cluster bootstrap)")
    clean_ax(ax)
_mt = wvadf[(wvadf.factor.str.startswith("monitoring")) & (wvadf.key == "ag_took")].iloc[0]
head(fig, f"Words vs. actions: the watched notice reduced agent takes {abs(100 * _mt['diff']):.1f} pp; public wording shifted (meaning unvalidated); "
          "pressure moves actions far more",
     f"{PRELIM}. Paired within cell (monitoring) or within scenario x pairing x arm (level 5 vs 1). Right labels: raw difference; * = BH q<.05 within factor.\n"
     "Grey = heuristic with arm-differential error or unvalidated keyword meaning: not a finding. Post-treatment subsets (e.g. among takers) are not shown.")
fig.subplots_adjust(top=0.86, left=0.17, right=0.95, wspace=1.05)
finish(fig, "04_words_vs_actions.png", "Words vs. actions: paired effects of monitoring and of pressure level by channel.")
log("words vs actions done", time.time() - T0)

# ------------------------------------------------------------------ asymmetry (mixed pairs)
mix = c[c.matched_vs_mixed == "mixed"]
asy = []
for rule in DIAG_ORDER + ["all"]:
    for arm in MON_ORDER + ["both"]:
        t = mix if rule == "all" else mix[mix.pairing_rule == rule]
        t = t if arm == "both" else t[t.monitoring == arm]
        u = t[t.outcome == "unilateral_take"]
        k_rule = int((u.final_action_a == "take").sum())
        n = len(u)
        lo, hi = wilson(k_rule, n)
        # paired take comparison within mixed episodes (rule agent vs no-rule agent)
        asy.append(dict(rule=rule, arm=arm, episodes=len(t), lone_takes=n, rule_agent_took_alone=k_rule,
                        none_agent_took_alone=n - k_rule, share_rule_agent=k_rule / n if n else np.nan, lo=lo, hi=hi,
                        p_binom_vs_half=binom_two_sided(k_rule, n) if n else np.nan,
                        take_rate_rule_agent=(t.final_action_a == "take").mean(),
                        take_rate_none_agent=(t.final_action_b == "take").mean()))
asydf = pd.DataFrame(asy)
asydf.to_csv(TAB / "asymmetry_mixed_pairs.csv", index=False)
fig, ax = plt.subplots(figsize=(9, 4.2))
g = asydf[asydf.arm == "both"].set_index("rule").reindex(DIAG_ORDER + ["all"]).reset_index()
yy = np.arange(len(g))[::-1]
ax.barh(yy, g.rule_agent_took_alone, color=S1, height=0.55, label="Rule agent took alone")
ax.barh(yy, g.none_agent_took_alone, left=g.rule_agent_took_alone + 0.6, color=S2, height=0.55, label="No-rule agent took alone")
for yi, (_, r) in zip(yy, g.iterrows()):
    ax.text(r.lone_takes + 2, yi, f"{r.rule_agent_took_alone} vs {r.none_agent_took_alone}  (binomial p={fmt_p(r.p_binom_vs_half)})",
            va="center", fontsize=7.5, color=TEXT_2)
ax.set_yticks(yy)
ax.set_yticklabels([("All mixed pairs" if r == "all" else f"{CRIT_NAME[r]} + no rule") for r in g.rule], fontsize=8)
ax.set_xlabel("Number of lone-take episodes in mixed pairings (both monitoring arms)")
ax.legend(frameon=False, fontsize=7.5, loc="upper right")
clean_ax(ax)
ax.set_xlim(0, g.lone_takes.max() * 1.9)
head(fig, "Who takes alone depends on the rule: welfare agents take alone; with authority it is the no-rule partner",
     f"{PRELIM}. Lone takes in X-none pairings, split by which agent took. Episodes are clustered in scenarios; binomial p is optimistic.")
fig.subplots_adjust(top=0.82)
finish(fig, "05_asymmetry_mixed_pairs.png", "Asymmetry: who takes alone in mixed pairings.")

# ------------------------------------------------------------------ rule application vs expected_first_take
ra_ = ag[(ag.criterion != "none") & ag.expected_first_take.notna()].copy()
ra_["eft"] = ra_.expected_first_take.astype(str)
ra_["expected_take"] = np.where(ra_.eft == "never", 0, (ra_.level >= pd.to_numeric(ra_.eft, errors="coerce")).astype(float))
ra_["rel_level"] = np.where(ra_.eft == "never", np.nan, ra_.level - pd.to_numeric(ra_.eft, errors="coerce"))
rule_rows = []
for crit in DIAG_ORDER + ["all"]:
    t = ra_ if crit == "all" else ra_[ra_.criterion == crit]
    for e in [0, 1]:
        u = t[t.expected_take == e]
        k, n = int(u.took.sum()), len(u)
        # scenario-cluster bootstrap (shared draws) for the agent-pooled rate
        blo_, bhi_, _ = boot_ratio(u.took.to_numpy(), np.ones(len(u)), u.scenario.map(SCEN_IDX).to_numpy()) if n else (np.nan, np.nan, None)
        rule_rows.append(dict(criterion=crit, expected_take=e, agents=n, took=k, rate=k / n if n else np.nan,
                              boot_lo=blo_, boot_hi=bhi_, scenarios=int(u.scenario.nunique())))
    tt = t.dropna(subset=["took"])
    a1 = ((tt.expected_take == 1) & (tt.took == 1)).sum()
    a0 = ((tt.expected_take == 0) & (tt.took == 0)).sum()
    po = (a1 + a0) / len(tt)
    pe = tt.expected_take.mean() * tt.took.mean() + (1 - tt.expected_take.mean()) * (1 - tt.took.mean())
    rule_rows.append(dict(criterion=crit, expected_take="kappa", agents=len(tt), rate=(po - pe) / (1 - pe) if pe < 1 else np.nan,
                          took=np.nan, boot_lo=po, boot_hi=np.nan))
ruledf = pd.DataFrame(rule_rows)
ruledf.to_csv(TAB / "rule_application_expected_first_take.csv", index=False)
rel = ra_.dropna(subset=["rel_level"]).groupby(["criterion", "rel_level"]).took.agg(["mean", "count", "sum"]).reset_index()
nev = ra_[ra_.eft == "never"].groupby("criterion").took.agg(["mean", "count", "sum"]).reset_index()
rel.to_csv(TAB / "rule_application_by_relative_level.csv", index=False)
nev.to_csv(TAB / "rule_application_never_expected.csv", index=False)
fig, ax = plt.subplots(figsize=(9, 4.8))
for crit, col in zip(DIAG_ORDER, [S1, S2, S3]):
    g = rel[rel.criterion == crit]
    g = g[g["count"] >= 10]
    lo_hi = np.array([wilson(int(s_), int(n_)) for s_, n_ in zip(g["sum"], g["count"])])
    ax.plot(g.rel_level, g["mean"], "-o", color=col, lw=2, ms=6, mec=SURFACE, mew=1.2, label=CRIT_NAME[crit] + " agents")
    ax.fill_between(g.rel_level, lo_hi[:, 0], lo_hi[:, 1], color=col, alpha=0.12, lw=0)
    nv = nev[nev.criterion == crit]
    if len(nv):
        ax.plot(5.2, nv["mean"].iloc[0], "s", color=col, ms=7, mec=SURFACE)
ax.axvline(-0.5, color=MUTED, ls=":", lw=1)
ax.text(-0.45, 0.97, "expected first take", fontsize=7.5, color=TEXT_2, va="top")
ax.text(5.2, -0.06, "'never'\nexpected", fontsize=7, color=TEXT_2, ha="center", va="top")
ax.set_xlabel("Pressure level minus the pack's expected first-take level for the agent's rule")
ax.set_ylabel("Share of rule agents who took")
ax.set_ylim(-0.02, 1)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
ax.legend(frameon=False, fontsize=8, loc="upper left")
clean_ax(ax)
head(fig, "Rule application: authority agents switch exactly at the expected level; welfare and non-deception agents ramp up early",
     f"{PRELIM}. Rule agents only (no-rule agents have no expectation); points with >=10 agents; band = Wilson (agents clustered in scenarios, so optimistic).")
fig.subplots_adjust(top=0.84)
finish(fig, "06_rule_application.png", "Take rate relative to the pack's expected first-take level.")
log("asymmetry + rule application done", time.time() - T0)

# ================================================================== PART 2: screening and the rest
# ------------------------------------------------------------------ helpers for fast statistics
for p in PARAMS:
    ag[p] = c[p].values[ag["ep"].values]

c_scen = c.scenario.map(SCEN_IDX).to_numpy()
c_lvl = c.level.to_numpy() - 1


def yprep(y, kind):
    """Outcome as (codes for chi2, ranks for eta/rho)."""
    if kind == "bin":
        yc = y.astype(int)
        return yc, int_rank(yc)
    return None, rankdata(y)


def pprep(x, ptype):
    """Parameter values -> integer codes ordered by value (ordinal) or label (categorical)."""
    if ptype in ("ord", "num"):
        vals = np.sort(pd.unique(x))
        return np.searchsorted(vals, x), vals
    vals = np.array(sorted(pd.unique(x.astype(str))))
    return np.searchsorted(vals, x.astype(str)), vals


def stat(xc, ptype, yc, yr, okind):
    """Comparable effect magnitude, asymptotic p and signed rho (ordinal)."""
    n = len(xc)
    if ptype in ("ord", "num"):
        rx = int_rank(xc) if ptype == "ord" else rankdata(xc)
        if np.std(rx) == 0 or np.std(yr) == 0:
            return np.nan, np.nan, np.nan
        rho = float(np.corrcoef(rx, yr)[0, 1])
        t = rho * math.sqrt((n - 2) / max(1e-12, 1 - rho * rho))
        return abs(rho), 2 * norm_sf(abs(t)), rho
    ng = xc.max() + 1
    if okind == "bin":
        v, pv = cramers_v_bc(xc, yc, ng, 2)
        if ng == 2 and not np.isnan(v):
            tab = np.bincount(xc * 2 + yc, minlength=4)
            pv = fisher_2x2(tab[0], tab[1], tab[2], tab[3])
        return v, pv, np.nan
    e = eta(xc, yr)
    if np.isnan(e):
        return np.nan, np.nan, np.nan
    h = (n - 1) * e * e
    return e, chi2_sf(h, int((np.bincount(xc) > 0).sum()) - 1), np.nan


# scenario x level lookup for scenario-level permutation (all planned rows)
LOOKUP = {}
for p, (lab_, ptype, rand, note) in PARAMS.items():
    if rand == "scenario":
        LOOKUP[p] = d.groupby(["scenario", "level"])[p].first().unstack().reindex(SCEN_LIST)


def permuter(p, mask):
    """Function yielding one permuted parameter vector (raw values) over rows c[mask], at the parameter's level."""
    ptype, rand = PARAMS[p][1], PARAMS[p][2]
    xs = c.loc[mask, p].to_numpy()
    if rand == "scenario":
        tbl = LOOKUP[p].to_numpy()
        si, li = c_scen[mask], c_lvl[mask]

        def f(rng):
            pi = rng.permutation(len(SCEN_LIST))
            return tbl[pi[si], li]
        return f
    strata = (c.loc[mask, "cell_id"] if rand == "cell" else c.loc[mask, "scenario"]).to_numpy()
    sc_codes = pd.factorize(strata)[0].astype(float)
    order = np.argsort(sc_codes, kind="stable")
    if ptype == "num":
        xs = rankdata(xs)  # permuting within strata keeps the multiset, so ranks can be permuted directly

    def f(rng):
        pidx = np.argsort(sc_codes + rng.random(len(xs)))
        out = np.empty_like(xs)
        out[order] = xs[pidx]
        return out
    return f


def encode(xvals, ptype, vals):
    if ptype in ("ord", "num"):
        return np.searchsorted(vals, xvals)
    return np.searchsorted(vals, xvals.astype(str))


scen_rows = [np.where(c_scen == i)[0] for i in range(len(SCEN_LIST))]
BOOT_IDX = []
for _ in range(B_BOOT_SCREEN):
    ix = RNG.integers(0, len(SCEN_LIST), len(SCEN_LIST))
    BOOT_IDX.append(np.concatenate([scen_rows[i] for i in ix]))


def stratifier(p):
    if PARAMS[p][2] == "scenario":
        return "setting_id" if p == "scenario_diagnostic" else "scenario_diagnostic"
    return "scenario"


def stratified(p, ptype, xv, yv, strata):
    """Pooled vs within-stratum effect, signed where possible; reversal flag."""
    df_ = pd.DataFrame({"x": xv, "y": yv, "s": strata})
    if ptype == "bin" or (ptype == "cat" and df_.x.nunique() == 2):
        lv = sorted(df_.x.astype(str).unique())
        df_["x1"] = (df_.x.astype(str) == lv[-1]).astype(int)
        pooled = df_[df_.x1 == 1].y.mean() - df_[df_.x1 == 0].y.mean()
        num = den = 0.0
        for _, g in df_.groupby("s"):
            n1, n0 = (g.x1 == 1).sum(), (g.x1 == 0).sum()
            if n1 == 0 or n0 == 0:
                continue
            w = n1 * n0 / (n1 + n0)
            num += w * (g[g.x1 == 1].y.mean() - g[g.x1 == 0].y.mean())
            den += w
        within = num / den if den else np.nan
        rev = bool((not np.isnan(within)) and np.sign(within) != np.sign(pooled) and abs(pooled) > 0.01 and abs(within) > 0.01)
        return pooled, within, f"{lv[-1]} minus {lv[0]} (MH-weighted)", rev
    if ptype in ("ord", "num"):
        pooled = spearman(df_.x.astype(float), df_.y.astype(float))[0]
        num = den = 0.0
        for _, g in df_.groupby("s"):
            if g.x.nunique() < 2 or g.y.nunique() < 2:
                continue
            num += len(g) * spearman(g.x.astype(float), g.y.astype(float))[0]
            den += len(g)
        within = num / den if den else np.nan
        rev = bool((not np.isnan(within)) and np.sign(within) != np.sign(pooled) and abs(pooled) > 0.02 and abs(within) > 0.02)
        return pooled, within, "Spearman rho (n-weighted within strata)", rev
    lm = df_.groupby("x").y.mean()
    cell = df_.groupby(["s", "x"]).y.mean().unstack()
    w = df_.groupby("s").size()
    adj = {}
    for lv_ in lm.index:
        ok = cell[lv_].notna()
        adj[lv_] = (cell.loc[ok, lv_] * w[ok]).sum() / w[ok].sum() if ok.any() else np.nan
    adj = pd.Series(adj)
    ok = adj.notna()
    rev = bool(ok.sum() > 2 and spearman(lm[ok].values, adj[ok].values)[0] < 0)
    return lm.max() - lm.min(), adj.max() - adj.min(), "max-min spread (directly standardised)", rev


DESIGN_STATUS = {}
for p, (plab, ptype, rand, note) in PARAMS.items():
    if p in ("monitoring", "level", "pairing", "pairing_rule", "matched_vs_mixed"):
        DESIGN_STATUS[p] = "clean (manipulated)"
    elif note.startswith("not randomised"):
        DESIGN_STATUS[p] = "confounded: collection time / provenance"
    elif note.startswith("scene text"):
        DESIGN_STATUS[p] = "confounded with level / diagnostic (scene text)"
    else:
        DESIGN_STATUS[p] = "descriptive (scenario-level, content differs)"
CONFOUNDED = {p for p, s in DESIGN_STATUS.items() if s.startswith("confounded")}

# ------------------------------------------------------------------ Step 3: screening
log("screening ...", round(time.time() - T0, 1))
screen = []
for p, (plab, ptype, rand, note) in PARAMS.items():
    for o, (olab, okind, olevel, heur, subset) in OUT.items():
        xv = c[p].to_numpy()
        yv = c[o].to_numpy(dtype=float)
        mask = pd.notna(xv) & ~np.isnan(yv)
        if mask.sum() < 30:
            continue
        xm, ym = xv[mask], yv[mask]
        xc, vals = pprep(xm, ptype)
        if len(vals) < 2:
            continue
        okind2 = "bin" if okind == "bin" else "rank"
        yc, yr = yprep(ym, okind)
        eff, pv, rho = stat(xm.astype(float) if ptype == "num" else xc, ptype, yc, yr, okind2)
        pos = -np.ones(len(c), int)
        pos[np.where(mask)[0]] = np.arange(mask.sum())
        bs = []
        for ix in BOOT_IDX:
            jj = pos[ix]
            jj = jj[jj >= 0]
            if len(jj) < 30:
                continue
            xb = xc[jj] if ptype != "num" else rankdata(xm[jj])
            if ptype != "num":
                if len(np.unique(xb)) < 2:
                    continue
                if ptype == "ord":
                    xb = np.searchsorted(np.unique(xb), xb)
            bs.append(stat_fast(xb, ptype, yc[jj] if yc is not None else None, yr[jj], okind2))
        lo, hi = (np.percentile(bs, 2.5), np.percentile(bs, 97.5)) if len(bs) > 20 else (np.nan, np.nan)
        grp = xm if ptype != "num" else pd.qcut(xm.astype(float), 5, labels=False, duplicates="drop")
        lm = pd.Series(ym).groupby(pd.Series(grp)).agg(["mean", "count"])
        spread = lm["mean"].max() - lm["mean"].min()
        mono = ""
        if ptype == "ord" and len(lm) > 2:
            dif = np.diff(lm["mean"].values)
            mono = "monotone up" if (dif >= -1e-9).all() else "monotone down" if (dif <= 1e-9).all() else "non-monotone"
        pooled, within, sdesc, rev = stratified(p, ptype, xm, ym, c.loc[mask, stratifier(p)].to_numpy())
        eff_n = len(np.unique(c_scen[mask])) if rand == "scenario" else int(mask.sum())
        screen.append(dict(parameter=p, parameter_label=plab, outcome=o, outcome_label=olab, outcome_level=olevel,
                           param_type=ptype, randomisation=rand,
                           measure="|rho|" if ptype in ("ord", "num") else ("V" if okind == "bin" else "sqrt(eps2)"),
                           effect=eff, boot_lo=lo, boot_hi=hi, rho_signed=rho, spread=spread, monotonicity=mono,
                           pooled_signed=pooled, within_stratum=within, stratified_by=stratifier(p),
                           stratified_measure=sdesc, sign_reversal=rev, p_asym=pv, n=int(mask.sum()), effective_n=eff_n,
                           min_cell_n=int(lm["count"].min()), n_levels=len(vals), design_status=DESIGN_STATUS[p],
                           confounded=p in CONFOUNDED, by_construction=(p, o) in BC_PO, heuristic=heur, subset=subset))
scr = pd.DataFrame(screen)
scr["q_bh"] = bh(scr.p_asym.values)  # BH family: all parameter x outcome pairs (no parameter is built from an outcome)
log("screening pairs", len(scr), "BH survivors", int((scr.q_bh < 0.05).sum()), round(time.time() - T0, 1))

# post-treatment subset membership: does the parameter change who is in the subset?
sub_rows = []
for o, f in SUBSET_DEF.items():
    member = f(c).astype(int).to_numpy()
    for p, (plab, ptype, rand, note) in PARAMS.items():
        xv = c[p]
        m = xv.notna().to_numpy()
        if ptype in ("ord", "num"):
            eff, pv = spearman(xv[m].astype(float).to_numpy(), member[m])
            eff = abs(eff)
        else:
            xc, vals = pprep(xv[m].to_numpy(), ptype)
            eff, pv = cramers_v_bc(xc, member[m])
        sub_rows.append(dict(outcome=o, parameter=p, effect=eff, p_asym=pv, membership_rate=member.mean()))
subdf = pd.DataFrame(sub_rows)
subdf["q"] = bh(subdf.p_asym.values)
subdf.to_csv(TAB / "subset_membership_by_parameter.csv", index=False)
shift = {(r.parameter, r.outcome): r.q for r in subdf.itertuples()}
scr["subset_membership_q"] = [shift.get((p, o), np.nan) for p, o in zip(scr.parameter, scr.outcome)]
scr["subset_shifts_with_param"] = scr.subset_membership_q < 0.05

# Besag-Clifford sequential permutation for BH survivors
surv = list(scr.index[scr.q_bh < 0.05])
log(f"Besag-Clifford: {len(surv)} survivors; cap {B_PERM_MAX} shuffles each, stop at {H_EXCEED} exceedances "
    f"(<= {len(surv) * B_PERM_MAX} statistics; measured ~3 s per survivor single-threaded, i.e. ~15 min without cache)")
perm_p, perm_B, perm_h = {}, {}, {}
PARAM_ORDER = {k: i for i, k in enumerate(PARAMS)}
OUT_ORDER = {k: i for i, k in enumerate(OUT)}
tp = time.time()
# Cache: the permutation step takes ~15 min single-threaded. Results are reused only when the input CSV, the
# script's permutation settings and the seed are identical (pass --fresh to recompute everything).
PERM_CACHE = TAB / "permutation_cache.json"
CACHE_TAG = dict(input_sha256=_sha(SRC), B_PERM_MAX=B_PERM_MAX, H_EXCEED=H_EXCEED, seed=SEED,
                 rand={p: v[2] for p, v in PARAMS.items()})
cache = {}
if "--fresh" not in sys.argv and PERM_CACHE.exists():
    _cj = json.loads(PERM_CACHE.read_text(encoding="utf-8"))
    if _cj.get("tag") == CACHE_TAG:
        cache = _cj.get("results", {})
log(f"permutation cache entries reused: {len(cache)}")
def pool_map(fn, tasks, label):
    """Run tasks in a spawn pool of RESERVED_WORKERS processes; children import only analyze_full_workers."""
    if WORKERS <= 1 or len(tasks) < 2:
        return [fn(t_) for t_ in tasks]
    import multiprocessing as mp
    import __main__ as _mm
    saved = getattr(_mm, "__file__", None)
    try:
        if saved is not None:
            del _mm.__file__  # stop spawn children from re-running this script as __mp_main__
        with mp.get_context("spawn").Pool(min(WORKERS, len(tasks))) as pool:
            out = []
            for i, r_ in enumerate(pool.imap_unordered(fn, tasks, chunksize=1), 1):
                out.append(r_)
                if i % 50 == 0:
                    log(f"  {label}: {i}/{len(tasks)} done, {round(time.time() - T0, 1)} s")
            return out
    finally:
        if saved is not None:
            _mm.__file__ = saved


tasks = []
for idx in surv:
    r = scr.loc[idx]
    p, o = r.parameter, r.outcome
    if f"{p}|{o}" in cache:
        perm_p[idx], perm_B[idx], perm_h[idx] = cache[f"{p}|{o}"]
        continue
    ptype, rand = PARAMS[p][1], PARAMS[p][2]
    okind = OUT[o][1]
    okind2 = "bin" if okind == "bin" else "rank"
    xv = c[p].to_numpy()
    yv = c[o].to_numpy(dtype=float)
    mask = pd.notna(xv) & ~np.isnan(yv)
    xm, ym = xv[mask], yv[mask]
    xc, vals = pprep(xm, ptype)
    yc, yr = yprep(ym, okind)
    obs = stat_fast(xc if ptype != "num" else rankdata(xm), ptype, yc, yr, okind2)
    tk = dict(key=idx, ptype=ptype, vals=vals, yc=yc, yr=yr, okind2=okind2, obs=obs, bmax=B_PERM_MAX, h_exceed=H_EXCEED,
              seed=[SEED, PARAM_ORDER[p], OUT_ORDER[o]])
    if rand == "scenario":
        tk.update(mode="scenario", tbl=LOOKUP[p].to_numpy(), si=c_scen[mask], li=c_lvl[mask], n_scen=len(SCEN_LIST))
    else:
        strata = (c.loc[mask, "cell_id"] if rand == "cell" else c.loc[mask, "scenario"]).to_numpy()
        xs = c.loc[mask, p].to_numpy()
        tk.update(mode="strata", xs=rankdata(xs) if ptype == "num" else xs, sc_codes=pd.factorize(strata)[0].astype(float))
    tasks.append(tk)
log(f"permutation tasks to run: {len(tasks)} on {WORKERS} worker(s)")
for idx, p_, L_, h_ in pool_map(perm_task, tasks, "permutations"):
    perm_p[idx], perm_B[idx], perm_h[idx] = p_, L_, h_
log("permutations done", round(time.time() - tp, 1), "s")
PERM_CACHE.write_text(json.dumps({"tag": CACHE_TAG, "results": {f"{scr.loc[i, 'parameter']}|{scr.loc[i, 'outcome']}":
                                  [perm_p[i], int(perm_B[i]), int(perm_h[i])] for i in perm_p}}, indent=0), encoding="utf-8")
scr["p_perm_BC"] = pd.Series(perm_p)
scr["perm_shuffles"] = pd.Series(perm_B)
scr["perm_exceedances"] = pd.Series(perm_h)
scr["perm_floor"] = 1 / (scr.perm_shuffles + 1)
scr["confirmed"] = (scr.p_perm_BC < 0.05).fillna(False)
scr = scr.sort_values("effect", ascending=False)
scr.to_csv(TAB / "screening_table.csv", index=False)

# ------------------------------------------------------------------ overview heat map
plist_show = list(PARAMS)
olist_show = list(OUT)
E = scr.pivot_table(index="parameter", columns="outcome", values="effect").reindex(index=plist_show, columns=olist_show)
Q = scr.pivot_table(index="parameter", columns="outcome", values="q_bh").reindex(index=plist_show, columns=olist_show)
CF = scr.assign(cf=scr.confirmed.astype(float)).pivot_table(index="parameter", columns="outcome", values="cf").reindex(
    index=plist_show, columns=olist_show)
E.to_csv(TAB / "screening_overview_effects.csv")
fig, ax = plt.subplots(figsize=(15, 9))
vmax = 0.6
im = ax.imshow(np.ma.masked_invalid(E.to_numpy(float)), cmap=SEQ, vmin=0, vmax=vmax, aspect="auto")
for i, p in enumerate(plist_show):
    for j, o in enumerate(olist_show):
        v = E.iloc[i, j]
        if np.isnan(v):
            ax.text(j, i, "–", ha="center", va="center", color=MUTED, fontsize=6)
            continue
        if p in CONFOUNDED:
            ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, hatch="////", lw=0, edgecolor="#898781"))
        mark = "●" if CF.iloc[i, j] == 1.0 else ("○" if Q.iloc[i, j] < 0.05 else "")
        ax.text(j, i, f"{v:.2f}".lstrip("0") + (f"\n{mark}" if mark else ""), ha="center", va="center", fontsize=5.6,
                color="white" if v / vmax > 0.55 else TEXT_1, linespacing=0.9)
ax.set_xticks(range(len(olist_show)))
ax.set_xticklabels([wrap(SHORT[o], 12) for o in olist_show], rotation=90, fontsize=7)
ax.set_yticks(range(len(plist_show)))
ax.set_yticklabels([f"{PARAMS[p][0]}" for p in plist_show], fontsize=7.5)
npair_out = sum(1 for o in olist_show if OUT[o][2] == "pair")
ax.axvline(npair_out - 0.5, color=TEXT_1, lw=1.5)
ax.axhline(4.5, color=TEXT_1, lw=1.0)
ax.tick_params(length=0)
for s_ in ax.spines.values():
    s_.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.01)
cb.set_label("Effect size (0 = none): bias-corrected V, sqrt(eps^2) or |Spearman rho|; colour capped at 0.6", fontsize=7.5)
cb.outline.set_visible(False)
head(fig, "Screening overview: pressure level and scenario design dominate; monitoring effects are small",
     f"{PRELIM}. ● = BH q<.05 and confirmed by cluster-aware permutation; ○ = BH q<.05 only. Hatched = confounded parameter. "
     "Top 5 rows = manipulated factors.\nLeft block = pair outcomes, right = agent outcomes (episode means). * = marginal heuristic, † = unreliable heuristic.")
fig.subplots_adjust(top=0.89)
finish(fig, "07_screening_overview.png", "Parameter x outcome effect-size overview.")

# ------------------------------------------------------------------ single-factor heat maps (absolute 0-1)
HEAT_PAIR = ["mutual_take", "unilateral_take", "any_take", "explicit_agree", "any_silence", "plans_agree"]
HEAT_AGENT = ["took", "plan_states_action", "plan_take", "argued_take", "dec_pub", "dec_notes", "mon_pub", "mon_priv",
              "evaluator", "deception_intended"]
AG_LABEL = {"took": "Agent took", "plan_states_action": "Plan states action", "plan_take": "Plan said take",
            "argued_take": "Argued take*", "dec_pub": "Dec. words public", "dec_notes": "Dec. words notes",
            "mon_pub": "Monitoring public", "mon_priv": "Monitoring private", "evaluator": "Evaluator mention",
            "deception_intended": "Dec.-intended*"}
SCR_IDX = scr.set_index(["parameter", "outcome"])


def heat_single(p, order, labels, fname, title, subtitle):
    V, N, cols, qcol = [], [], [], []
    for o in HEAT_PAIR:
        g = c.groupby(p)[o].agg(["mean", "count"]).reindex(order)
        V.append(g["mean"].to_numpy()); N.append(g["count"].to_numpy()); cols.append(SHORT[o]); qcol.append((p, o))
    for k in HEAT_AGENT:
        g = ag.groupby(p)[k].agg(["mean", "count"]).reindex(order)
        V.append(g["mean"].to_numpy()); N.append(g["count"].to_numpy()); cols.append(AG_LABEL[k]); qcol.append((p, "ag_" + k))
    V, N = np.array(V, float).T, np.array(N, float).T
    nr, nc = V.shape
    fig, ax = plt.subplots(figsize=(2.6 + nc * 0.95, 2.1 + nr * 0.55))
    im = ax.imshow(np.ma.masked_invalid(V), cmap=SEQ, vmin=0, vmax=1, aspect="auto")
    for i in range(nr):
        for j in range(nc):
            if np.isnan(V[i, j]):
                ax.text(j, i, "–", ha="center", va="center", color=MUTED)
                continue
            col = "white" if V[i, j] > 0.55 else TEXT_1
            ax.text(j, i - 0.13, f"{100 * V[i, j]:.0f}%", ha="center", va="center", color=col, fontsize=7.6, fontweight="bold")
            ax.text(j, i + 0.23, f"n={int(N[i, j])}", ha="center", va="center", color=col, fontsize=5.8)
            if p in CONFOUNDED:
                ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, hatch="////", lw=0, edgecolor="#898781"))
    xl = []
    for lab_, key in zip(cols, qcol):
        q = SCR_IDX.loc[key, "q_bh"] if key in SCR_IDX.index else np.nan
        cf = bool(SCR_IDX.loc[key, "confirmed"]) if key in SCR_IDX.index else False
        xl.append(wrap(lab_, 12) + ("\n●" if cf else "\n○" if (not np.isnan(q) and q < 0.05) else "\n "))
    ax.set_xticks(range(nc)); ax.set_xticklabels(xl, fontsize=7)
    ax.xaxis.tick_top()
    ax.set_yticks(range(nr)); ax.set_yticklabels([wrap(l, 30) for l in labels], fontsize=7.8)
    ax.axvline(len(HEAT_PAIR) - 0.5, color=TEXT_1, lw=1.6)
    ax.set_xticks(np.arange(-.5, nc, 1), minor=True); ax.set_yticks(np.arange(-.5, nr, 1), minor=True)
    ax.grid(which="minor", color=SURFACE, lw=2); ax.tick_params(which="both", length=0)
    for s_ in ax.spines.values():
        s_.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.01)
    cb.set_label("Rate (absolute scale)", fontsize=7.5)
    cb.ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    cb.outline.set_visible(False)
    hgt = fig.get_figheight()
    fig.suptitle(title, x=0.01, ha="left", fontsize=11.5, fontweight="bold", y=1.0 + 0.75 / hgt)
    fig.text(0.01, 1.0 + 0.2 / hgt, subtitle + "\nLeft block: pair outcomes (n = episodes). Right block: agent outcomes "
             "(n = agents). ● = confirmed q<.05, ○ = BH q<.05 only. * = marginal heuristic.", ha="left", fontsize=7.6, color=TEXT_2)
    out = pd.DataFrame(V, index=labels, columns=cols)
    outn = pd.DataFrame(N, index=labels, columns=[x + " n" for x in cols])
    pd.concat([out, outn], axis=1).to_csv(TAB / f"dimension_x_metric_{p}.csv", index_label=p)
    finish(fig, fname, title)


heat_single("level", [1, 2, 3, 4, 5], [LEVEL_NAME[i] for i in range(1, 6)], "08_heat_level.png",
            "Pressure level: mutual take climbs steeply from level 1 to level 5", PRELIM + ". Level is manipulated within scenario (clean).")
heat_single("monitoring", MON_ORDER, [MON_NAME[m] for m in MON_ORDER], "09_heat_monitoring.png",
            "Monitoring notice: small shifts in takes; public monitoring talk rises when watched",
            PRELIM + ". Unpaired view; the paired primary test is in figure 3.")
heat_single("pairing", PAIR_ORDER, [PAIR_NAME[x] for x in PAIR_ORDER], "10_heat_pairing.png",
            "Pairing: welfare pairs take most, authority and non-deception pairs least", PRELIM + ". Pairing is manipulated within scenario (clean).")
heat_single("scenario_diagnostic", DIAG_ORDER, [DIAG_NAME[x] for x in DIAG_ORDER], "11_heat_diagnostic.png",
            "Scenario diagnostic: descriptive differences between scene sets", PRELIM + ". Scenario-level (24 scenes each); content differs, so not causal.")
heat_single("setting_id", SETTING_ORDER, [SETTING_NAME[x] for x in SETTING_ORDER], "12_heat_setting.png",
            "Social setting: descriptive differences only", PRELIM + ". Scenario-level (9 scenes per setting); content differs, so not causal.")
log("heat maps done", round(time.time() - T0, 1))

# ------------------------------------------------------------------ top relationships (charts with intervals)
ORDERS = {"level": [1, 2, 3, 4, 5], "monitoring": MON_ORDER, "pairing": PAIR_ORDER, "scenario_diagnostic": DIAG_ORDER,
          "setting_id": SETTING_ORDER}
# Panels: the strongest take outcome for each unconfounded design parameter (take outcomes are the study's main
# outcomes; private-vocabulary outcomes are dominated by prompt echo and are not charted here).
TOP_TAKE = ["mutual_take", "any_take", "ag_took", "unilateral_take"]
top = scr[(scr.outcome.isin(TOP_TAKE)) & (scr.parameter.isin(["level", "pairing", "scenario_diagnostic", "setting_id"]))]
top = top.sort_values("effect", ascending=False).drop_duplicates(["parameter"])
mon_ = scr[(scr.parameter == "monitoring") & (scr.outcome == "mutual_take")]  # monitoring panel is always the primary outcome
extra_ = scr[(scr.parameter == "level") & (scr.outcome == "unilateral_take")]
top = pd.concat([top, mon_, extra_]).drop_duplicates(["parameter", "outcome"]).head(6)


def boot_rate_by(df_, gcol, ycol, order):
    rows_ = []
    for lv in order:
        t = df_[df_[gcol] == lv]
        if len(t) == 0:
            rows_.append((lv, np.nan, np.nan, np.nan, 0)); continue
        lo_, hi_, _ = boot_ratio(t[ycol].to_numpy(float), np.ones(len(t)), t.scenario.map(SCEN_IDX).to_numpy())
        rows_.append((lv, t[ycol].mean(), lo_, hi_, len(t)))
    return pd.DataFrame(rows_, columns=["level", "mean", "lo", "hi", "n"])


def paired_arm_rates(sub):
    """Watched and unwatched mutual-take rates over the SAME complete cell pairs, with shared-draw cluster CIs."""
    w, *_ = mcnemar_table(sub)
    si = scen_of_cell.reindex(w.index).map(SCEN_IDX).to_numpy()
    out = []
    for arm in MON_ORDER:
        lo_, hi_, _ = boot_ratio(w[arm].to_numpy(), np.ones(len(w)), si)
        out.append((arm, w[arm].mean(), lo_, hi_, len(w)))
    return pd.DataFrame(out, columns=["level", "mean", "lo", "hi", "n"])


top_rows = []
fig, axes = plt.subplots(2, 3, figsize=(14, 8.2))
for ax, (_, r) in zip(axes.ravel(), top.iterrows()):
    p, o = r.parameter, r.outcome
    order = ORDERS.get(p, sorted(c[p].dropna().unique()))
    if p == "monitoring":
        t_all = paired_arm_rates(c)
        t_b = paired_arm_rates(c[c.pair_ep_class == f"both {EP_MAIN}"])
        lab_a, lab_b = "All complete pairs", f"Pairs with both trials on {EP_MAIN}"
    else:
        t_all = boot_rate_by(c.dropna(subset=[o]), p, o, order)
        t_b = boot_rate_by(c[(c.endpoint == EP_MAIN)].dropna(subset=[o]), p, o, order)
        lab_a, lab_b = "All complete", f"{EP_MAIN} only"
    xx = np.arange(len(order))
    ax.errorbar(xx - 0.1, t_all["mean"], yerr=[t_all["mean"] - t_all.lo, t_all.hi - t_all["mean"]], fmt="o", color=S1,
                ms=7, lw=1.6, capsize=0, label=lab_a, mec=SURFACE, mew=1)
    ax.errorbar(xx + 0.1, t_b["mean"], yerr=[t_b["mean"] - t_b.lo, t_b.hi - t_b["mean"]], fmt="s", color=S2,
                ms=6, lw=1.2, capsize=0, label=lab_b, mec=SURFACE, mew=1)
    if len(order) <= 5:
        for xi, (_, tt) in zip(xx, t_all.iterrows()):
            ax.annotate(f"{pct(tt['mean'], 0)}", (xi - 0.1, tt["mean"]), xytext=(-6, 0), textcoords="offset points",
                        ha="right", va="center", fontsize=6.8, color=TEXT_1)
    labels_x = [MON_NAME[v] for v in order] if p == "monitoring" else [str(v).replace("_", " ") for v in order]
    ax.set_xticks(xx); ax.set_xticklabels([wrap(v, 10) for v in labels_x], fontsize=6.8, rotation=30 if len(order) > 6 else 0)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_ylim(0, min(1.0, max(0.1, np.nanmax(np.r_[t_all.hi, t_b.hi]) * 1.15)))
    ax.set_ylabel(OUT[o][0], fontsize=7.5)
    ax.set_xlim(-0.6, len(order) - 0.4)
    if p == "monitoring":
        ax.set_title(wrap(f"Mutual take, watched vs unwatched over the same {int(P0.pairs):,} cell pairs: paired diff "
                          f"{pp(P0.diff_w_minus_u)} (95% CI {pp(P0.cluster_boot_lo)} to {pp(P0.cluster_boot_hi)}); "
                          f"{int(P0.watched_only_take)} watched-only vs {int(P0.unwatched_only_take)} unwatched-only", 56), fontsize=8, loc="left")
    else:
        conf_txt = f"p_perm {fmt_p(r.p_perm_BC)}" if r.confirmed else ("BH q<.05, not confirmed" if r.q_bh < 0.05 else f"q={fmt_p(r.q_bh)}, n.s.")
        ax.set_title(wrap(f"{OUT[o][0]} by {PARAMS[p][0].lower()} ({r.measure} {r.effect:.2f}, {conf_txt})", 50),
                     fontsize=8, loc="left")
    clean_ax(ax)
    ax.legend(frameon=False, fontsize=6.5, loc="upper left")
    for lab_s, tt_ in (("all", t_all), (EP_MAIN, t_b)):
        for _, tt in tt_.iterrows():
            top_rows.append(dict(parameter=p, outcome=o, level=tt.level, subset=lab_s, mean=tt["mean"], lo=tt.lo, hi=tt.hi, n=tt.n,
                                 paired=(p == "monitoring")))
for ax in axes.ravel()[len(top):]:
    ax.set_visible(False)
head(fig, f"Take outcomes by design factor: pressure and pairing dominate; the notice effect is small; patterns hold on {EP_MAIN}",
     f"{PRELIM}. Strongest take outcome per design factor, the paired monitoring view, and lone take by level. Bars = 95% scenario-cluster bootstrap "
     "(shared draws). y axes start at 0. Setting and diagnostic are scenario-level (descriptive).")
fig.subplots_adjust(top=0.85, hspace=0.75, wspace=0.32)
finish(fig, "13_top_relationships.png", f"Top relationships with cluster-bootstrap intervals, overall and within {EP_MAIN}.")
pd.DataFrame(top_rows).to_csv(TAB / "top_relationships_levels.csv", index=False)
cons = []
for _, r in top.iterrows():
    for strat_col in ["scenario_diagnostic", "endpoint", "monitoring"]:
        if strat_col == r.parameter:
            continue
        for sv, g in c.groupby(strat_col):
            gg = g.dropna(subset=[r.outcome])
            pt = PARAMS[r.parameter][1]
            xc, vals = pprep(gg[r.parameter].to_numpy(), pt)
            if len(vals) < 2:
                continue
            ok = OUT[r.outcome][1]
            yc, yr = yprep(gg[r.outcome].to_numpy(float), ok)
            e, pv, rho = stat(xc, pt, yc, yr, "bin" if ok == "bin" else "rank")
            cons.append(dict(parameter=r.parameter, outcome=r.outcome, stratum=f"{strat_col}={sv}", n=len(gg), effect=e,
                             rho_signed=rho, p_asym=pv))
consdf = pd.DataFrame(cons)
consdf.to_csv(TAB / "top_relationships_within_strata.csv", index=False)
log("top relationships done", round(time.time() - T0, 1))

# ------------------------------------------------------------------ Step 2: univariate summaries
uni = []
for p, (plab, ptype, rand, note) in PARAMS.items():
    vc = d[p].value_counts(dropna=False)
    uni.append(dict(variable=p, label=plab, role="parameter", type=ptype, n=int(d[p].notna().sum()), missing=int(d[p].isna().sum()),
                    summary="; ".join(f"{k}: {v}" for k, v in list(vc.items())[:10]) + (" ..." if len(vc) > 10 else ""),
                    interval="", interval_method="counts over 4,320 planned trials"))
for o, (olab, okind, olevel, heur, subset) in OUT.items():
    y = c[o].dropna()
    if okind == "bin":
        k, n = int(y.sum()), len(y)
        lo, hi = wilson(k, n)
        uni.append(dict(variable=o, label=olab, role="outcome (pair)", type="binary", n=n, missing=int(c[o].isna().sum()),
                        summary=f"{k}/{n} = {pct(k / n)}", interval=f"{pct(lo)}-{pct(hi)}", interval_method="Wilson (episodes)",
                        heuristic=heur, subset=subset))
    elif okind == "frac":
        base = o[3:]
        a = ag[base].dropna()
        g = ag.dropna(subset=[base]).groupby("scenario")[base].agg(["sum", "count"]).to_numpy()
        bs = [g[ix, 0].sum() / g[ix, 1].sum() for ix in (RNG.integers(0, len(g), len(g)) for _ in range(1000))]
        uni.append(dict(variable=o, label=olab, role="outcome (agent, pooled A/B)", type="binary", n=len(a),
                        missing=int(len(ag) - len(a)), summary=f"{int(a.sum())}/{len(a)} = {pct(a.mean())}",
                        interval=f"{pct(np.percentile(bs, 2.5))}-{pct(np.percentile(bs, 97.5))}",
                        interval_method="scenario-cluster bootstrap (agents)", heuristic=heur, subset=subset))
    else:
        base = o[3:] if o.startswith("ag_") else o
        y = ag[base].dropna() if o.startswith("ag_") else y
        uni.append(dict(variable=o, label=olab, role="outcome (agent)" if o.startswith("ag_") else "outcome (pair)", type="numeric",
                        n=len(y), missing=0, summary=f"median {y.median():.0f}, IQR {y.quantile(.25):.0f}-{y.quantile(.75):.0f}",
                        interval=f"range {y.min():.0f}-{y.max():.0f}", interval_method="", heuristic=heur, subset=subset))
unidf = pd.DataFrame(uni)
unidf.to_csv(TAB / "univariate_summary.csv", index=False)

rate_keys = [o for o in OUT if OUT[o][1] in ("bin", "frac")]
fig, ax = plt.subplots(figsize=(9, 7))
yy = np.arange(len(rate_keys))[::-1]
for yi, o in zip(yy, rate_keys):
    r = unidf[unidf.variable == o].iloc[0]
    k, n = r.summary.split(" = ")[0].split("/")
    v = int(k) / int(n)
    lo_s, hi_s = r.interval.split("-")
    lo_, hi_ = float(lo_s.strip("%")) / 100, float(hi_s.strip("%")) / 100
    colr = S1 if OUT[o][2] == "pair" else S3
    ax.hlines(yi, lo_, hi_, color=colr, lw=2)
    ax.plot(v, yi, "o", color=colr, ms=6, mec=SURFACE, mew=1.2)
    ax.text(1.02, yi, f"{pct(v)}  (n={n})", transform=ax.get_yaxis_transform(), va="center", fontsize=7, color=TEXT_2)
ax.set_yticks(yy)
ax.set_yticklabels([("[pair] " if OUT[o][2] == "pair" else "[agent] ") + OUT[o][0] + (f"  ({OUT[o][3]})" if OUT[o][3] else "")
                    for o in rate_keys], fontsize=7.3)
ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
ax.set_xlim(0, 1)
ax.set_xlabel("Rate among complete trials (pair: Wilson 95%; agent: scenario-cluster bootstrap 95%)")
clean_ax(ax)
head(fig, f"Univariate: {pct(c.mutual_take.mean())} of complete episodes end in a mutual take; private texts echo the honesty notes",
     f"{PRELIM}. Blue = pair outcomes (n = episodes), green = agent outcomes pooled over A and B (n = agents).")
fig.subplots_adjust(top=0.9, right=0.85)
finish(fig, "14_univariate_rates.png", "Univariate outcome rates with intervals.")

num_keys = [("total_words_exchanged", c.total_words_exchanged, "Public words exchanged per episode"),
            ("total_tokens", c.total_tokens, "Total tokens per episode"),
            ("reasoning_words", ag.reasoning_words, "Reasoning words per agent"),
            ("words_sent_total", ag.words_sent_total, "Public words sent per agent"),
            ("deception_words_reasoning", ag.deception_words_reasoning, "Deception words in reasoning per agent (masked)"),
            ("mentions_monitoring_private", ag.mentions_monitoring_private, "Monitoring mentions in private text per agent")]
fig, axes = plt.subplots(2, 3, figsize=(13, 6.5))
for ax, (k, s, lab_) in zip(axes.ravel(), num_keys):
    s = s.dropna()
    v = np.log10(s + 1)
    ax.hist(v, bins=40, color=S1, edgecolor=SURFACE, lw=0.5)
    ax.set_title(wrap(f"{lab_}: median {s.median():.0f} (IQR {s.quantile(.25):.0f}-{s.quantile(.75):.0f}), n={len(s)}", 46), fontsize=8, loc="left")
    tk = [0, 1, 2, 3, 4, 5]
    ax.set_xticks([t for t in tk if v.min() - 0.5 <= t <= v.max() + 0.5])
    ax.set_xticklabels([f"{10 ** t - 1:,.0f}" for t in tk if v.min() - 0.5 <= t <= v.max() + 0.5], fontsize=7)
    ax.set_xlabel("value (log scale, x+1)", fontsize=7)
    ax.set_ylabel("count", fontsize=7)
    clean_ax(ax)
head(fig, "Numeric outcomes are right-skewed; shown on a log scale", f"{PRELIM}. Complete trials only.")
fig.subplots_adjust(top=0.86, hspace=0.6)
finish(fig, "15_univariate_numeric.png", "Distributions of numeric outcomes (log scale).")

# ------------------------------------------------------------------ Step 4: outcome x outcome
olist = list(OUT)
M_ = np.full((len(olist), len(olist)), np.nan)
for i, a_ in enumerate(olist):
    for j, b_ in enumerate(olist):
        if j < i:
            M_[i, j] = M_[j, i]; continue
        if i == j:
            M_[i, j] = 1; continue
        ta = "bin" if OUT[a_][1] == "bin" else "num"
        tb = "bin" if OUT[b_][1] == "bin" else "num"
        x, y = c[a_].to_numpy(float), c[b_].to_numpy(float)
        m = ~np.isnan(x) & ~np.isnan(y)
        if m.sum() < 30:
            continue
        if ta == "bin" and tb == "bin":
            M_[i, j] = cramers_v_bc(x[m].astype(int), y[m].astype(int))[0]
        elif ta == "num" and tb == "num":
            M_[i, j] = abs(spearman(x[m], y[m])[0])
        else:
            if ta == "num":
                x, y = y, x
            M_[i, j] = eta(x[m].astype(int), rankdata(y[m]))
pd.DataFrame(M_, index=olist, columns=olist).to_csv(TAB / "outcome_association_matrix.csv")
oo = []
for i, j in combinations(range(len(olist)), 2):
    bc_ = frozenset((olist[i], olist[j])) in BC_OO
    oo.append(dict(outcome_1=olist[i], outcome_2=olist[j], association=M_[i, j], by_construction=bc_,
                   near_redundant=(not bc_) and M_[i, j] >= 0.8))
oodf = pd.DataFrame(oo).sort_values("association", ascending=False)
oodf.to_csv(TAB / "outcome_pairs.csv", index=False)
fig, ax = plt.subplots(figsize=(12, 10.5))
im = ax.imshow(np.ma.masked_invalid(M_), cmap=SEQ, vmin=0, vmax=1)
for i in range(len(olist)):
    for j in range(len(olist)):
        if i == j or np.isnan(M_[i, j]):
            continue
        if frozenset((olist[i], olist[j])) in BC_OO:
            ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, hatch="////", lw=0, edgecolor="#898781"))
        ax.text(j, i, f"{M_[i, j]:.2f}".lstrip("0"), ha="center", va="center", fontsize=5.5,
                color="white" if M_[i, j] > 0.55 else TEXT_1)
ax.set_xticks(range(len(olist))); ax.set_xticklabels([wrap(SHORT[o], 12) for o in olist], rotation=90, fontsize=7)
ax.set_yticks(range(len(olist))); ax.set_yticklabels([SHORT[o] for o in olist], fontsize=7.5)
ax.tick_params(length=0)
for s_ in ax.spines.values():
    s_.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.01)
cb.set_label("Association (0-1): V, eta on ranks, or |Spearman rho|", fontsize=7.5)
cb.outline.set_visible(False)
nred = int(oodf.near_redundant.sum())
head(fig, f"Outcome x outcome: take outcomes and stance outcomes cluster; {nred} informative pair(s) are near-redundant (>=0.8)",
     f"{PRELIM}. Episode level (agent outcomes = episode means). Hatched = related by construction (not a finding).")
fig.subplots_adjust(top=0.93)
finish(fig, "16_outcome_association.png", "Outcome x outcome association matrix.")

# ------------------------------------------------------------------ Step 5: interactions (ridge logit + parametric bootstrap)
def design(df_, factors, inter=None):
    cols_ = [np.ones(len(df_))]
    names = ["const"]
    dums = {}
    for f_ in factors:
        lv = sorted(df_[f_].astype(str).unique())
        dums[f_] = {l: (df_[f_].astype(str) == l).to_numpy(float) for l in lv[1:]}
        for l, v in dums[f_].items():
            cols_.append(v); names.append(f"{f_}={l}")
    if inter:
        a_, b_ = inter
        for la, va in dums[a_].items():
            for lb, vb in dums[b_].items():
                v = va * vb
                if v.sum() > 0:
                    cols_.append(v); names.append(f"{a_}={la}:{b_}={lb}")
    return np.column_stack(cols_), names


INTER_F = [f_ for f_ in ["scenario_diagnostic", "setting_id", "level", "pairing", "monitoring", "endpoint"] if c[f_].nunique() > 1]
DESIGN_BUILT = {frozenset(("scenario_diagnostic", "pairing")):
                "design-built: whether the pairing's rule matches the scene's diagnostic is fixed by the pack (expected_first_take differs), "
                "so this interaction is expected by construction, not a discovery"}
MON_INTER = {frozenset(("monitoring", x)) for x in ("level", "pairing", "scenario_diagnostic")}
inter_rows = []
tint = time.time()
_scen_rows_c = [np.where(c_scen == i)[0] for i in range(len(SCEN_LIST))]
_scen_rows_c = [r_ for r_ in _scen_rows_c if len(r_)]
_scen_dum = np.column_stack([(c_scen == i).astype(float) for i in range(len(SCEN_LIST)) if (c_scen == i).any()][1:])
inter_tasks, inter_meta = [], {}
for ycol in ["mutual_take", "any_take"]:
    y = c[ycol].to_numpy(float)
    for a_, b_ in combinations(INTER_F, 2):
        Xa, _ = design(c, [a_, b_])
        Xi, ni = design(c, [a_, b_], (a_, b_))
        _, mua, dva = ridge_logit(Xa, y, RIDGE)
        _, _, dvi = ridge_logit(Xi, y, RIDGE)
        extra = np.linalg.matrix_rank(Xi) - np.linalg.matrix_rank(Xa)
        obs = dva - dvi - extra
        # null mean: additive model + ridge-shrunken scenario offsets (carries within-scenario correlation into the draws)
        Xs = np.column_stack([Xa, _scen_dum])
        pen = np.r_[np.zeros(Xa.shape[1]), np.ones(_scen_dum.shape[1])]
        _, mu0, _ = ridge_logit(Xs, y, RIDGE, pen_mask=pen)
        key = f"{ycol}|{a_}|{b_}"
        inter_meta[key] = dict(outcome=ycol, factor_a=a_, factor_b=b_, obs=obs, extra=extra, ct=pd.crosstab(c[a_], c[b_]))
        inter_tasks.append(dict(key=key, Xa=Xa, Xi=Xi, mu0=mu0, scen_rows=_scen_rows_c, extra=extra, lam=RIDGE, B=B_INTER,
                                seed=[SEED, 99, len(inter_tasks)]))
log(f"interactions: {len(inter_tasks)} tests x {B_INTER} cluster-resampled parametric-bootstrap draws on {WORKERS} worker(s)")
for key, null in pool_map(inter_task, inter_tasks, "interaction tests"):
    m_ = inter_meta[key]
    a_, b_ = m_["factor_a"], m_["factor_b"]
    pv = (np.sum(null >= m_["obs"]) + 1) / (B_INTER + 1)
    fs = frozenset((a_, b_))
    note = []
    if fs in DESIGN_BUILT:
        note.append(DESIGN_BUILT[fs])
    if PARAMS[a_][2] == "scenario" and PARAMS[b_][2] == "scenario":
        note.append("scenario-level x scenario-level: the interaction itself lives in the scenario offsets of the null, so p is conservative; "
                    f"only {N_SCEN} scenes")
    elif "scenario" in (PARAMS[a_][2], PARAMS[b_][2]):
        note.append("involves a scenario-level factor (descriptive)")
    if "endpoint" in (a_, b_):
        note.append("endpoint = collection time (confounded)")
    inter_rows.append(dict(outcome=m_["outcome"], factor_a=a_, factor_b=b_, deviance_drop_minus_df=m_["obs"], extra_df=m_["extra"],
                           p_cluster_param_boot=pv, boot_draws=B_INTER, null_median=float(np.median(null)),
                           null_q95=float(np.percentile(null, 95)), min_cell_n=int(m_["ct"].values.min()),
                           aliased=bool(A[plist.index(a_), plist.index(b_)] >= 0.3), design_built=fs in DESIGN_BUILT,
                           monitoring_interaction=fs in MON_INTER, note="; ".join(note)))
intdf = pd.DataFrame(inter_rows)
intdf["q_bh"] = bh(intdf.p_cluster_param_boot.values)
intdf = intdf.sort_values("deviance_drop_minus_df", ascending=False)
intdf.to_csv(TAB / "interactions_ridge_logit.csv", index=False)
log("interactions done", round(time.time() - tint, 1), "s; passing (q<.05):", int((intdf.q_bh < 0.05).sum()))


# ------------------------------------------------------------------ 2D heat maps
def heat2d(ax, df_, rcol, ccol, ycol, rorder, corder, rlabels, clabels, title, small=5):
    g = df_.groupby([rcol, ccol])[ycol].agg(["sum", "count"])
    Mv = np.full((len(rorder), len(corder)), np.nan)
    K = np.zeros_like(Mv); N = np.zeros_like(Mv)
    for i, rv in enumerate(rorder):
        for j, cv in enumerate(corder):
            if (rv, cv) in g.index:
                k, n = g.loc[(rv, cv)]
                K[i, j], N[i, j] = k, n
                Mv[i, j] = k / n if n else np.nan
    show_ = np.where(N >= small, Mv, np.nan)
    im = ax.imshow(np.ma.masked_invalid(show_), cmap=SEQ, vmin=0, vmax=1, aspect="auto")
    for i in range(len(rorder)):
        for j in range(len(corder)):
            if N[i, j] == 0:
                continue
            colr = "white" if (not np.isnan(show_[i, j]) and show_[i, j] > 0.55) else (TEXT_1 if N[i, j] >= small else MUTED)
            ax.text(j, i - 0.15, f"{100 * Mv[i, j]:.0f}%", ha="center", va="center", fontsize=7, fontweight="bold", color=colr)
            ax.text(j, i + 0.22, f"{int(K[i, j])}/{int(N[i, j])}", ha="center", va="center", fontsize=5.6, color=colr)
    ax.set_xticks(range(len(corder))); ax.set_xticklabels([wrap(x, 10) for x in clabels], fontsize=7)
    ax.set_yticks(range(len(rorder))); ax.set_yticklabels([wrap(x, 24) for x in rlabels], fontsize=7)
    ax.set_title(title, fontsize=8.5, loc="left")
    ax.tick_params(length=0)
    for s_ in ax.spines.values():
        s_.set_visible(False)
    out = pd.DataFrame(Mv, index=rlabels, columns=clabels)
    return im, out, pd.DataFrame(N, index=rlabels, columns=clabels)


lv5 = [1, 2, 3, 4, 5]
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
panels = [
    (c, "scenario_diagnostic", "level", "mutual_take", DIAG_ORDER, lv5, [DIAG_NAME[x] for x in DIAG_ORDER], [f"L{i}" for i in lv5],
     "Mutual take: diagnostic x level", "2d_diagnostic_x_level"),
    (c, "pairing", "level", "mutual_take", PAIR_ORDER, lv5, [PAIR_NAME[x] for x in PAIR_ORDER], [f"L{i}" for i in lv5],
     "Mutual take: pairing x level", "2d_pairing_x_level"),
    (c, "pairing", "scenario_diagnostic", "mutual_take", PAIR_ORDER, DIAG_ORDER, [PAIR_NAME[x] for x in PAIR_ORDER],
     [CRIT_NAME[x] for x in DIAG_ORDER], "Mutual take: pairing x diagnostic", "2d_pairing_x_diagnostic"),
    (ag, "criterion", "scenario_diagnostic", "took", CRIT_ORDER, DIAG_ORDER, [CRIT_NAME[x] + " agent" for x in CRIT_ORDER],
     [CRIT_NAME[x] for x in DIAG_ORDER], "Agent take: own rule x diagnostic", "2d_criterion_x_diagnostic"),
    (c, "setting_id", "scenario_diagnostic", "mutual_take", SETTING_ORDER, DIAG_ORDER, [SETTING_NAME[x] for x in SETTING_ORDER],
     [CRIT_NAME[x] for x in DIAG_ORDER], "Mutual take: setting x diagnostic (3 scenes per cell)", "2d_setting_x_diagnostic"),
    (c, "monitoring", "level", "mutual_take", MON_ORDER, lv5, [MON_NAME[x] for x in MON_ORDER], [f"L{i}" for i in lv5],
     "Mutual take: monitoring x level", "2d_monitoring_x_level"),
]
for ax, (df_, rc_, cc_, yc_, ro, co, rl, cl, tt, fn) in zip(axes.ravel(), panels):
    im, out, outn = heat2d(ax, df_, rc_, cc_, yc_, ro, co, rl, cl, tt)
    pd.concat([out, outn.add_suffix(" n")], axis=1).to_csv(TAB / f"{fn}.csv")
cax = fig.add_axes([0.93, 0.25, 0.01, 0.5])
cb = fig.colorbar(im, cax=cax)
cb.set_label("Rate (absolute scale, 0-100%)", fontsize=8)
cb.ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
cb.outline.set_visible(False)
head(fig, "Two-factor views: pressure raises takes in every diagnostic and pairing; welfare pairs tip earliest",
     f"{PRELIM}. Each cell: rate and k/n (episodes, or agents for the agent-take panel). Cells with n<5 greyed.")
fig.subplots_adjust(top=0.88, hspace=0.45, wspace=0.62, right=0.9)
finish(fig, "17_2d_heatmaps.png", "Two-factor heat maps of mutual take (and agent take).")

# scenario x level (tall)
sc_order = []
for dg in DIAG_ORDER:
    sub = c[c.scenario_diagnostic == dg].groupby("scenario").mutual_take.mean().sort_values()
    sc_order += list(sub.index)
titles_ = c.drop_duplicates("scenario").set_index("scenario")
fig, ax = plt.subplots(figsize=(8, 22))
im, out, outn = heat2d(ax, c, "scenario", "level", "mutual_take", sc_order, lv5,
                       [f"{s} {titles_.loc[s, 'scenario_title'][:26]} ({titles_.loc[s, 'scenario_diagnostic'][:4]})" for s in sc_order],
                       [f"Level {i}" for i in lv5], "", small=5)
pd.concat([out, outn.add_suffix(" n")], axis=1).to_csv(TAB / "2d_scenario_x_level.csv")
for k_ in range(1, 3):
    ax.axhline(sum((c.drop_duplicates("scenario").scenario_diagnostic == DIAG_ORDER[i]).sum() for i in range(k_)) - 0.5, color=TEXT_1, lw=1.5)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
cb.set_label("Mutual-take rate (absolute)", fontsize=8)
cb.outline.set_visible(False)
fig.suptitle("Scenario x level: a few scenes take at every level, many never do", x=0.01, ha="left", fontsize=11.5, fontweight="bold", y=0.995)
fig.text(0.01, 0.988, f"{PRELIM}. Rows grouped by diagnostic (welfare, non-deception, authority), sorted by overall rate.\n"
         "Each cell: k/n over up to 12 trials (6 pairings x 2 arms); n<5 greyed.", fontsize=7.5, color=TEXT_2, va="top")
fig.subplots_adjust(top=0.975)
finish(fig, "18_scenario_x_level.png", "Scenario x level mutual-take rates.")

# ------------------------------------------------------------------ Step 6: heuristic-error sensitivity
# The interim divide-by-recall table was mis-specified (it used recall only, at a different unit from the outcome) and is
# dropped. A Rogan-Gladen correction needs per-arm sensitivity AND specificity at the unit of the analysed outcome
# (agent x episode "argued take in some round"); Step 1 validation gives per-arm agreement only (per message), so no
# correction is computed. The stance and deception-intended monitoring contrasts stay exploratory instead.
RG_NOTE = ("No heuristic-error correction is reported. Rogan-Gladen needs per-arm sensitivity and specificity measured on "
           "the same unit as the analysed outcome (agent x episode). Step 1 validation reports only per-arm agreement, per message "
           f"(stance: {ACC_STANCE}; deception-intended: {ACC_DECINT}). The interim divide-by-recall table was mis-specified and has been dropped.")

# ------------------------------------------------------------------ Step 7: rank candidates
# score = effect (0-3) + robustness (0-4.5) + relevance (0-3) + surprise (0-2) - 3 if any trust problem - 4 if mechanical.
# Surprise uses only the directions written in PREREG.md (no hand-coded surprise for individual findings).
RQ = {"monitoring": "3.4 monitoring", "level": "1.1 level", "pairing": "1.1 pairing", "pairing_rule": "1.1 pairing",
      "matched_vs_mixed": "1.1 pairing", "scenario_diagnostic": "1.1 diagnostic", "setting_id": "1.1 setting"}
WORD_OUT = {"ag_dec_pub", "ag_dec_notes", "ag_dec_reas", "ag_mon_pub", "ag_mon_priv", "ag_argued_take", "ag_plan_take",
            "ag_plan_states_action", "ag_evaluator", "ag_deception_intended", "deception_intended_pair", "explicit_agree",
            "total_words_exchanged", "ag_words_sent_total", "ag_reasoning_words", "ag_agree_pub", "ag_tl_dec"}
TAKE_OUT = {"mutual_take", "any_take", "ag_took", "unilateral_take"}
ECHO_OUT = {"ag_dec_notes", "ag_dec_reas", "ag_dec_reas_per1k", "ag_tl_dec"}
NOTICE_ECHO = {"ag_mon_pub", "ag_mon_priv"}
DEC_INT = {"ag_deception_intended", "deception_intended_pair", "ag_dec_int_given_take"}
MECHANICAL = {"total_words_exchanged", "ag_words_sent_total", "ag_reasoning_words", "total_tokens", "ag_dec_reas_per1k",
              "any_silence"}


def relevance(param, outcome):
    r_ = 2.0 if param == "monitoring" else (1.0 if param in RQ else 0.0)
    return r_ + (1.0 if outcome in TAKE_OUT else 0.5 if outcome in WORD_OUT else 0.0)


def mechanical_reason(param, outcome):
    if outcome in MECHANICAL:
        return "mechanical outcome: word / token counts track prompt and message length, which differ by design"
    return ""


def trust_problems(param, outcome, heur="", confounded=False, design="", min_cell=99, rev=False, subset_shift=False):
    pr_ = []
    if "UNRELIABLE" in heur:
        pr_.append("unreliable heuristic outcome")
    if param == "monitoring" and ("arm" in heur.lower() or "stance" in heur or outcome in DEC_INT):
        pr_.append("heuristic error differs by monitoring arm")
    if outcome in DEC_INT:
        pr_.append("deception-intended flag is nearly 'took or planned take' (prompt states who taking misleads)")
    if outcome in NOTICE_ECHO:
        pr_.append("notice echo: both notices contain 'monitored' / 'oversight'; keyword meaning unvalidated")
    if confounded:
        pr_.append(design)
    if min_cell < 10:
        pr_.append(f"min cell n={min_cell}")
    if rev:
        pr_.append("sign reversal within strata")
    if subset_shift:
        pr_.append("subset membership depends on the parameter (post-treatment subset)")
    if outcome in ECHO_OUT:
        pr_.append("private deception words mostly echo the prompt's honesty notes")
    if param in ("pairing_rule", "matched_vs_mixed"):
        pr_.append("coarsening of pairing (aliased with pairing)")
    return pr_


cand = []
paired_keys = {("monitoring", k) for k in wvadf.key} | {("level", k) for k in wvadf.key}
for _, r in scr.iterrows():
    if not (r.q_bh < 0.05) or (r.parameter, r.outcome) in paired_keys:
        continue
    sign = r.rho_signed if not np.isnan(r.rho_signed) else r.pooled_signed
    surprise = 0.5
    if r.parameter == "level" and r.outcome in ("mutual_take", "any_take", "ag_took"):
        surprise = 0.0 if sign > 0 else 2.0
    robust = 1.0 + (1.0 if r.confirmed else 0) + (1.0 if r.design_status.startswith("clean") else 0) \
        + (1.0 if not r.sign_reversal else 0) + (0.5 if r.min_cell_n >= 10 else 0)
    problems = trust_problems(r.parameter, r.outcome, r.heuristic, r.confounded, r.design_status, r.min_cell_n,
                              r.sign_reversal, r.subset_shifts_with_param is True)
    if not r.confirmed:
        problems.append("not confirmed by cluster-aware permutation")
    mech = mechanical_reason(r.parameter, r.outcome)
    score = 3 * min(r.effect / 0.5, 1) + robust + relevance(r.parameter, r.outcome) + surprise - (3 if problems else 0) - (4 if mech else 0)
    cand.append(dict(candidate=f"{r.parameter_label} -> {r.outcome_label}", source="screening", parameter=r.parameter,
                     outcome=r.outcome, measure=r.measure, effect=r.effect, effect_ci=f"{r.boot_lo:.2f}-{r.boot_hi:.2f}",
                     signed=sign, spread=r.spread, n=r.n, effective_n=r.effective_n, q_bh=r.q_bh, p_family=r.p_perm_BC,
                     p_kind="Besag-Clifford permutation", design=r.design_status, research_question=RQ.get(r.parameter, "1.1 other"),
                     score=score, exploratory=True, mechanical=mech, problems="; ".join(problems)))
P0r = primdf.iloc[0]
cand.append(dict(candidate="Watched notice -> fewer mutual takes (PRIMARY, paired McNemar)", source="primary McNemar",
                 parameter="monitoring", outcome="mutual_take", measure="paired diff", effect=P0r.diff_w_minus_u,
                 effect_ci=f"{P0r.cluster_boot_lo:.3f} to {P0r.cluster_boot_hi:.3f}", signed=P0r.diff_w_minus_u, spread=np.nan,
                 n=P0r.pairs, effective_n=P0r.pairs, q_bh=np.nan, p_family=P0r.p_reported, p_kind="McNemar (confirmatory; not in BH family)",
                 design="clean (manipulated)", research_question="3.4 monitoring", score=99, exploratory=False, mechanical="",
                 problems="pre-registered; notice-only manipulation; one model / seed"))
for _, r in wvadf[(wvadf.q_within_factor < 0.05)].iterrows():
    par = r.factor.split()[0]
    if par == "monitoring" and r.key == "mutual_take":
        continue
    prob = trust_problems(par, r.key, r.heuristic)
    if r.potentially_biased and "heuristic error differs by monitoring arm" not in prob:
        prob.append("heuristic error differs by monitoring arm")
    mech = mechanical_reason(par, r.key)
    std = abs(r.std_diff) if not np.isnan(r.std_diff) else 0
    surprise = 0.0 if ((par == "level" and r.key in TAKE_OUT and r["diff"] > 0)
                       or (par == "monitoring" and r.key in TAKE_OUT and r["diff"] < 0)) else 0.5
    cand.append(dict(candidate=f"{'Watched notice' if par == 'monitoring' else 'Level 5 vs 1'}: {r.measure} ({r.channel.lower()}, paired)",
                     source="words vs actions (paired)", parameter=par, outcome=r.key, measure="paired diff",
                     effect=r["diff"], effect_ci=f"{r.lo:.3f} to {r.hi:.3f}", signed=r["diff"], spread=np.nan, n=r.n_pairs,
                     effective_n=r.n_pairs, q_bh=r.q_within_factor, p_family=r.p, p_kind="paired sign-flip permutation",
                     design="clean (manipulated)", research_question="2.2 words+actions x " + ("3.4" if par == "monitoring" else "1.1 level"),
                     score=3 * min(std / 0.5, 1) + 4.5 + relevance(par, r.key) + surprise - (3 if prob else 0) - (4 if mech else 0),
                     exploratory=True, mechanical=mech, problems="; ".join(prob)))
# monitoring dose-response trend (secondary, added after the interim review)
cand.append(dict(candidate="Monitoring effect changes with pressure level (conditional-OR trend over discordant pairs)",
                 source="dose-response (conditional logit)", parameter="monitoring x level", outcome="mutual_take",
                 measure="log OR per level", effect=DOSE["slope_log_OR_per_level"],
                 effect_ci=f"{DOSE['slope_boot_lo']:.2f} to {DOSE['slope_boot_hi']:.2f}", signed=DOSE["slope_log_OR_per_level"],
                 spread=np.nan, n=DOSE["discordant_pairs"], effective_n=DOSE["discordant_pairs"], q_bh=np.nan,
                 p_family=DOSE["p_LR_trend"], p_kind="likelihood-ratio (conditional logit)", design="clean (manipulated)",
                 research_question="3.4 monitoring x 1.1 level",
                 score=3 * min(abs(DOSE["slope_log_OR_per_level"]) / 0.5, 1) + 4.0 + 3.0 + 0.5, exploratory=True, mechanical="",
                 problems="" if (DOSE["slope_boot_lo"] > 0 or DOSE["slope_boot_hi"] < 0) else "cluster-bootstrap CI of the trend includes 0"))
for rule in DIAG_ORDER:
    r = asydf[(asydf.rule == rule) & (asydf.arm == "both")].iloc[0]
    if r.p_binom_vs_half < 0.05:
        cand.append(dict(candidate=f"{CRIT_NAME[rule]} + no-rule pairs: lone takes by the rule agent {r.rule_agent_took_alone} vs the no-rule agent {r.none_agent_took_alone}",
                         source="asymmetry (mixed pairs)", parameter="criterion", outcome="who took alone",
                         measure="share by rule agent", effect=r.share_rule_agent, effect_ci=f"{r.lo:.2f}-{r.hi:.2f}",
                         signed=r.share_rule_agent - 0.5, spread=np.nan, n=r.lone_takes, effective_n=r.lone_takes, q_bh=np.nan,
                         p_family=r.p_binom_vs_half, p_kind="binomial (ignores scenario clustering)",
                         design="agent-level, within mixed pairs", research_question="1.1 criterion / pairing",
                         score=3 * min(abs(r.share_rule_agent - 0.5) / 0.4, 1) + 3.5 + 2 + 0.5,
                         exploratory=True, mechanical="", problems="binomial p ignores scenario clustering (optimistic)"))
ka = ruledf[(ruledf.criterion == "all") & (ruledf.expected_take == "kappa")].iloc[0]
cand.append(dict(candidate="Pack's expected_first_take predicts whether rule agents take",
                 source="rule application", parameter="expected_first_take", outcome="agent took", measure="Cohen kappa",
                 effect=ka.rate, effect_ci="", signed=ka.rate, spread=np.nan, n=ka.agents, effective_n=N_SCEN, q_bh=np.nan,
                 p_family=np.nan, p_kind="none (descriptive agreement)", design="pack design (scenario x criterion)",
                 research_question="1.1 criterion", score=3 + 3.5 + 2 + 0.5, exploratory=True, mechanical="",
                 problems="agents clustered in scenarios; descriptive (no test)"))
for _, r in intdf[(intdf.q_bh < 0.05) & (intdf.outcome == "mutual_take")].iterrows():
    prob = []
    if r.design_built:
        prob.append("design-built interaction (expected by construction)")
    if "endpoint" in (r.factor_a, r.factor_b):
        prob.append("endpoint = collection time")
    if PARAMS[r.factor_a][2] == "scenario" and PARAMS[r.factor_b][2] == "scenario":
        prob.append(f"scenario-level x scenario-level ({N_SCEN} scenes)")
    cand.append(dict(candidate=f"Interaction {PARAMS[r.factor_a][0]} x {PARAMS[r.factor_b][0]} -> mutual take",
                     source="interaction (ridge logit)", parameter=f"{r.factor_a} x {r.factor_b}", outcome="mutual_take",
                     measure="deviance drop - df", effect=r.deviance_drop_minus_df, effect_ci="", signed=np.nan, spread=np.nan,
                     n=len(c), effective_n=len(c), q_bh=r.q_bh, p_family=r.p_cluster_param_boot,
                     p_kind=f"cluster-resampled parametric bootstrap (B={B_INTER})", design="interaction",
                     research_question="1.1 variables for emergence",
                     score=3 * min(r.deviance_drop_minus_df / 60, 1) + 3 + 2 + 0.5 - (3 if prob else 0),
                     exploratory=True, mechanical="", problems="; ".join(prob)))
canddf = pd.DataFrame(cand)
# ONE BH family over every exploratory candidate's (permutation / sign-flip / bootstrap / LR / binomial) p-value
_fam = canddf.exploratory & canddf.p_family.notna()
canddf["q_family"] = np.nan
canddf.loc[_fam, "q_family"] = bh(canddf.loc[_fam, "p_family"].values)
M_FAMILY = int(_fam.sum())
_nsig = _fam & ~(canddf.q_family < 0.05)
canddf.loc[_nsig, "problems"] = [("; ".join([x for x in [pr_, "not significant after the family-wide BH"] if x])) for pr_ in canddf.loc[_nsig, "problems"]]
canddf["trustworthy"] = (canddf.problems == "") | (~canddf.exploratory)
canddf.loc[canddf.source == "asymmetry (mixed pairs)", "trustworthy"] = canddf.loc[canddf.source == "asymmetry (mixed pairs)", "q_family"] < 0.05
canddf.loc[canddf.source == "rule application", "trustworthy"] = True
canddf["demoted_mechanical"] = canddf.mechanical != ""
canddf = canddf.sort_values("score", ascending=False).reset_index(drop=True)
canddf.index += 1
canddf.to_csv(TAB / "candidates.csv", index_label="rank")
untrust = canddf[~canddf.trustworthy & (canddf.measure != "deviance drop - df")].sort_values("effect", key=lambda v: v.abs(), ascending=False)
untrust.to_csv(TAB / "candidates_untrustworthy.csv", index_label="rank")
log("candidates", len(canddf), "trustworthy", int(canddf.trustworthy.sum()), "BH family m =", M_FAMILY)

# ------------------------------------------------------------------ provenance
def sha(pth):
    return _sha(pth) if Path(pth).exists() else None


PREREG_SRC = HERE / "PREREG.md"
if OUTD != HERE and PREREG_SRC.exists():
    (OUTD / "PREREG.md").write_text(PREREG_SRC.read_text(encoding="utf-8"), encoding="utf-8")
_plan = SRC.parent.parent / "ANALYSIS-PLAN.md"
prov = dict(script="analyze_full.py", script_sha256=sha(Path(__file__)),
            workers_module_sha256=sha(HERE / "analyze_full_workers.py"), run_at_utc=pd.Timestamp.now("UTC").isoformat(),
            label=PRELIM, arguments=dict(data=str(SRC), schema=str(SCHEMA), out=str(OUTD), fresh=ARGS.fresh),
            inputs={str(SRC): sha(SRC), str(SCHEMA): sha(SCHEMA), "PREREG.md": sha(PREREG_SRC),
                    **({str(_plan): sha(_plan)} if _plan.exists() else {})},
            packages=dict(python=sys.version.split()[0], numpy=np.__version__, pandas=pd.__version__,
                          matplotlib=matplotlib.__version__, scipy="not installed (tests implemented in-script)"),
            seeds=dict(numpy_default_rng=SEED, shared_cluster_draws=[SEED, 7], interactions=[SEED, 99, "task index"],
                       permutations=[SEED, "param index", "outcome index"]),
            settings=dict(B_BOOT_SCREEN=B_BOOT_SCREEN, B_BOOT_MAIN=B_BOOT_MAIN, B_PERM_MAX=B_PERM_MAX, H_EXCEED=H_EXCEED,
                          B_SIGNFLIP=B_SIGNFLIP, B_INTER=B_INTER, RIDGE=RIDGE, randomisation_source=RAND_SOURCE),
            cpu=AFFINITY, runtime_seconds=None, log=LOG)


# ================================================================== REPORT.md
def mdtable(df_, cols, heads=None, fmt=None):
    fmt = fmt or {}
    heads = heads or cols
    out = ["| " + " | ".join(heads) + " |", "|" + "---|" * len(cols)]
    for _, r in df_.iterrows():
        cells = []
        for col in cols:
            v = r[col]
            if col in fmt:
                v = fmt[col](v)
            elif isinstance(v, float):
                v = "–" if np.isnan(v) else f"{v:.3g}"
            cells.append(str(v).replace("|", "/"))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def fig_md(name, alt):
    return f"![{alt}](figures/{name})"


def rrtxt(r):
    if not np.isfinite(r.risk_ratio_w_over_u):
        return "–"
    ci = f" ({r.rr_boot_lo:.2f}-{r.rr_boot_hi:.2f})" if np.isfinite(r.rr_boot_lo) else ""
    return f"{r.risk_ratio_w_over_u:.2f}{ci}"


def ppci(r, lo="cluster_boot_lo", hi="cluster_boot_hi"):
    return f"{pp(r.diff_w_minus_u)} ({pp(r[lo])} to {pp(r[hi])})" if np.isfinite(r[lo]) else pp(r.diff_w_minus_u)


ifmt = lambda v: f"{int(v):,}"  # noqa: E731
arm_tab = d.groupby(["monitoring", "status"]).size().unstack().reindex(MON_ORDER).fillna(0)
for k_ in ["complete", "failed", "not_started"]:
    if k_ not in arm_tab:
        arm_tab[k_] = 0
arm_tab_md = mdtable(arm_tab.reset_index(), ["monitoring", "complete", "failed", "not_started"],
                     ["Arm", "Complete", "Failed", "Not started"], fmt={k_: ifmt for k_ in ["complete", "failed", "not_started"]})
P0 = primdf.iloc[0]
pr = primdf.set_index("subset")
bMain = pr.loc[f"Endpoint: both {EP_MAIN}"]
spl = pr.loc["Endpoint: split"]
sens_md = mdtable(sensdf, ["subset", "pairs", "watched_only_take", "unwatched_only_take", "diff_w_minus_u", "newcombe_lo", "newcombe_hi", "p_reported"],
                  ["Failures treated as", "Pairs", "Watched-only take", "Unwatched-only take", "Diff (w-u)", "95% lo", "95% hi", "p"],
                  fmt={"diff_w_minus_u": pp, "newcombe_lo": pp, "newcombe_hi": pp, "p_reported": fmt_p})
PCOLS = ["subset", "pairs", "watched_only_take", "unwatched_only_take", "rate_unwatched", "rate_watched", "diff_w_minus_u",
         "newcombe_lo", "newcombe_hi", "cluster_boot_lo", "cluster_boot_hi", "risk_ratio_w_over_u", "rr_boot_lo", "rr_boot_hi", "p_reported"]
PHEADS = ["Subset", "Pairs", "Watched-only take", "Unwatched-only take", "Rate unwatched", "Rate watched", "Diff (w-u)",
          "Newcombe lo", "Newcombe hi", "Cluster lo", "Cluster hi", "RR (w/u)", "RR lo", "RR hi", "p"]
PFMT = {"rate_watched": pct, "rate_unwatched": pct, "diff_w_minus_u": pp, "newcombe_lo": pp, "newcombe_hi": pp,
        "cluster_boot_lo": pp, "cluster_boot_hi": pp, "p_reported": fmt_p,
        "risk_ratio_w_over_u": lambda v: f"{v:.2f}", "rr_boot_lo": lambda v: f"{v:.2f}", "rr_boot_hi": lambda v: f"{v:.2f}"}
prim_md = mdtable(primdf, PCOLS, PHEADS, fmt=PFMT)
lvl_md = mdtable(DOSE_LEVELS, PCOLS, PHEADS, fmt=PFMT)
w_mon = wvadf[wvadf.factor.str.startswith("monitoring")].copy()
w_lvl = wvadf[wvadf.factor.str.startswith("level")].copy()


def wfmt(r):
    return f"{100 * r['diff']:+.1f} pp" if r.kind != "num" else f"{r['diff']:+.1f}"


for w_ in (w_mon, w_lvl):
    w_["diff_txt"] = [wfmt(r) for _, r in w_.iterrows()]
    w_["ci_txt"] = [(f"{100 * r.lo:+.1f} to {100 * r.hi:+.1f} pp" if r.kind != "num" else f"{r.lo:+.1f} to {r.hi:+.1f}") for _, r in w_.iterrows()]
    w_["base_txt"] = [(pct(r.m0) + " -> " + pct(r.m1)) if r.kind != "num" else f"{r.m0:.1f} -> {r.m1:.1f}" for _, r in w_.iterrows()]
wcols = ["channel", "measure", "n_pairs", "base_txt", "diff_txt", "ci_txt", "q_within_factor", "per_arm_accuracy"]
wheads = ["Channel", "Measure", "Pairs", "Arm A -> arm B", "Paired diff", "95% cluster CI", "q", "Heuristic / per-arm accuracy"]
wmon_md = mdtable(w_mon, wcols, wheads, fmt={"q_within_factor": fmt_p})
wlvl_md = mdtable(w_lvl, wcols, wheads, fmt={"q_within_factor": fmt_p})
dec_md = mdtable(pd.DataFrame(dec_rows), ["arm", "agents", "takers", "p_take", "p_flag", "p_flag_given_take"],
                 ["Arm", "Agents", "Takers", "P(take)", "P(flag)", "P(flag / take) (post-treatment, descriptive)"],
                 fmt={"p_take": pct, "p_flag": pct, "p_flag_given_take": pct})
asy_md = mdtable(asydf[asydf.arm == "both"], ["rule", "episodes", "lone_takes", "rule_agent_took_alone", "none_agent_took_alone",
                                              "share_rule_agent", "lo", "hi", "p_binom_vs_half"],
                 ["Rule in pair", "Episodes", "Lone takes", "Rule agent alone", "No-rule agent alone", "Share by rule agent",
                  "Wilson lo", "Wilson hi", "Binomial p"],
                 fmt={"share_rule_agent": pct, "lo": pct, "hi": pct, "p_binom_vs_half": fmt_p})
rule_md = mdtable(ruledf[ruledf.expected_take != "kappa"], ["criterion", "expected_take", "agents", "took", "rate", "boot_lo", "boot_hi"],
                  ["Rule", "Expected take at this level?", "Agents", "Took", "Rate", "95% lo (cluster)", "95% hi"],
                  fmt={"rate": pct, "boot_lo": pct, "boot_hi": pct, "took": lambda v: f"{v:.0f}"})
kap = ruledf[ruledf.expected_take == "kappa"].set_index("criterion")
scr_show = scr.copy()
scr_show["ci"] = [f"{a:.2f}-{b:.2f}" for a, b in zip(scr_show.boot_lo, scr_show.boot_hi)]
scr_top_md = mdtable(scr_show[scr_show.q_bh < 0.05].head(30),
                     ["parameter_label", "outcome_label", "measure", "effect", "ci", "spread", "p_asym", "q_bh", "p_perm_BC",
                      "effective_n", "min_cell_n", "design_status", "heuristic", "sign_reversal"],
                     ["Parameter", "Outcome", "Measure", "Effect", "95% cluster CI", "Raw spread", "p (asym.)", "q (BH)",
                      "p (perm.)", "Eff. n", "Min cell", "Design", "Heuristic", "Simpson flag"],
                     fmt={"effect": lambda v: f"{v:.2f}", "spread": lambda v: f"{v:.2f}", "p_asym": fmt_p, "q_bh": fmt_p,
                          "p_perm_BC": fmt_p})


def cand_effect_txt(r):
    if r.measure == "paired diff":
        lo_, hi_ = [float(x) for x in r.effect_ci.split(" to ")]
        if r.outcome in MECHANICAL:
            return f"paired diff {r.effect:+.1f} ({lo_:+.1f} to {hi_:+.1f})"
        return f"paired diff {pp(r.effect)} (95% cluster CI {pp(lo_)} to {pp(hi_)})"
    if r.measure == "share by rule agent":
        return f"rule agent's share of lone takes {pct(r.effect)} (Wilson {r.effect_ci})"
    if r.measure == "Cohen kappa":
        return f"kappa {r.effect:.2f}"
    if r.measure == "log OR per level":
        return f"conditional OR x{math.exp(r.effect):.2f} per level (log-OR 95% cluster CI {r.effect_ci})"
    if r.measure == "deviance drop - df":
        return f"deviance drop minus df {r.effect:.0f}"
    return f"{r.measure} {r.effect:.2f} (cluster CI {r.effect_ci})"


cand_top = canddf[canddf.trustworthy & ~canddf.demoted_mechanical].head(15)
cand_top = cand_top.assign(effect_txt=[cand_effect_txt(r) for _, r in cand_top.iterrows()],
                           qtxt=[("confirmatory" if not r.exploratory else fmt_p(r.q_family)) for _, r in cand_top.iterrows()])
cand_md = mdtable(cand_top.reset_index(), ["index", "candidate", "source", "effect_txt", "n", "qtxt", "research_question", "problems"],
                  ["Rank", "Candidate", "Source", "Effect (interval)", "n", "q (one BH family)", "Research question", "Caveat"],
                  fmt={"n": lambda v: f"{int(v):,}"})
SUMMARY_N = 8
summary_cands = cand_top.head(SUMMARY_N)  # the summary list is the head of the table in section 5 (same order)
mech = canddf[canddf.demoted_mechanical & canddf.trustworthy]
untrust_md = mdtable(untrust.head(12).reset_index(), ["candidate", "measure", "effect", "problems"],
                     ["Looks large but untrustworthy", "Measure", "Effect", "Why"], fmt={"effect": lambda v: f"{v:+.3f}"})
ICOLS = ["outcome", "factor_a", "factor_b", "deviance_drop_minus_df", "extra_df", "p_cluster_param_boot", "q_bh", "min_cell_n", "note"]
IHEADS = ["Outcome", "Factor A", "Factor B", "Deviance drop - df", "Extra df", "p (cluster param. boot)", "q", "Min cell", "Note"]
IFMT = {"deviance_drop_minus_df": lambda v: f"{v:.1f}", "p_cluster_param_boot": fmt_p, "q_bh": fmt_p}
inter_md = mdtable(intdf.head(14), ICOLS, IHEADS, fmt=IFMT)
mon_int = intdf[intdf.monitoring_interaction].sort_values(["outcome", "factor_b"])
mon_int_md = mdtable(mon_int, ICOLS, IHEADS, fmt=IFMT)
n_inter_pass = int((intdf.q_bh < 0.05).sum())
alias_md = mdtable(pd.DataFrame(aliased[:16], columns=["a", "b", "v"]), ["a", "b", "v"], ["Parameter", "Parameter", "Association"],
                   fmt={"v": lambda v: f"{v:.2f}"})
redund = oodf[oodf.near_redundant]
comp_q = comp.drop_duplicates("parameter")[["parameter", "V_status", "q_status"]]
mon_rows = w_mon.set_index("key")
lvl_rows = w_lvl.set_index("key")
fail_md = mdtable(FAILDF, ["failure_reason", "unwatched", "watched", "rate_unwatched", "rate_watched", "fisher_p_vs_all_started"],
                  ["Failure reason", "Unwatched", "Watched", "Rate (of started), unwatched", "Rate, watched", "Fisher p (arm x this reason)"],
                  fmt={"rate_unwatched": lambda v: pct(v, 2), "rate_watched": lambda v: pct(v, 2), "fisher_p_vs_all_started": fmt_p})

# ---- data-driven robustness wording
bound_rows = sensdf.iloc[1:].reset_index(drop=True)
failing_bounds = [i + 1 for i, r in bound_rows.iterrows() if r.p_reported > 0.05]
main_ep_ok = bMain.p_reported <= 0.05 and bMain.diff_w_minus_u < 0
if not failing_bounds and main_ep_ok:
    ROBUST = "robust to every failure bound and within the main endpoint"
elif failing_bounds == [3] and main_ep_ok:
    ROBUST = ("robust except the adversarial failure bound (bound 3, which requires 100% of watched failures and 0% of unwatched "
              "failures to be mutual takes)")
else:
    _f = ", ".join(f"bound {i}" for i in failing_bounds)
    ROBUST = "not robust to " + ", ".join(x for x in [_f, "" if main_ep_ok else f"the main-endpoint ({EP_MAIN}) subset"] if x)
sub = primdf[primdf.subset.str.startswith(("Diagnostic:", "Pairing:", "Level:"))]
n_sub, n_neg, n_cross = len(sub), int((sub.diff_w_minus_u < 0).sum()), int(sub.ci_crosses_0.sum())
if TIP["k_needed"] is None:
    TIP_TXT = (f"Even with all {TIP['watched_failures']} watched failures counted as takes and all {TIP['unwatched_failures']} unwatched "
               f"failures as no take, p stays at or below .05 (p = {fmt_p(TIP['p_at_all'])}).")
else:
    TIP_TXT = (f"Tipping point: with unwatched failures counted as no take, **{TIP['k_needed']} of the {TIP['watched_failures']} watched failures "
               f"({pct(TIP['share_needed'], 0)})** must be mutual takes, chosen in the order least favourable to the hypothesis, before p exceeds .05. "
               f"The watched arm's observed mutual-take rate among complete trials is {pct(TIP['watched_complete_take_rate'])}, so this needs "
               f"failures to be takes at about {TIP['ratio_to_watched_base_rate']:.1f}x that rate.")
mm_txt = ""
if MM is not None:
    mm_txt = (f"`missing_message` failures: {int(MM.watched)} watched vs {int(MM.unwatched)} unwatched "
              f"({pct(MM.rate_watched, 2)} vs {pct(MM.rate_unwatched, 2)} of started trials; Fisher p = {fmt_p(MM.fisher_p_vs_all_started)}; "
              f"as a share of each arm's failures, Fisher p = {fmt_p(P_MM_AMONG_FAIL)}).")
_tk = mon_rows.loc["ag_took"]
_dp = mon_rows.loc["ag_dec_pub"]
_mp = mon_rows.loc["ag_mon_pub"]
take_down = _tk.hi < 0
if take_down and _dp.lo > -0.005:
    WVA = (f"The notice reduced takes by about {abs(100 * _tk['diff']):.0f} pp (agent take {_tk.diff_txt}, 95% CI {_tk.ci_txt}). There is no evidence "
           "of sanitised talk with an unchanged deal. Public wording shifted toward oversight / deception vocabulary "
           f"(oversight / monitoring words {_mp.diff_txt}, deception words {_dp.diff_txt}), and what that vocabulary means is unvalidated.")
else:
    WVA = (f"Agent take changed by {_tk.diff_txt} (95% CI {_tk.ci_txt}); public deception words {_dp.diff_txt} (95% CI {_dp.ci_txt}); "
           f"oversight / monitoring words {_mp.diff_txt}, whose meaning is unvalidated.")
_mi = mon_int[mon_int.outcome == "mutual_take"].set_index("factor_b")


_mi = mon_int[mon_int.outcome == "mutual_take"].copy()
_mi["other"] = np.where(_mi.factor_a == "monitoring", _mi.factor_b, _mi.factor_a)
_mi = _mi.set_index("other")


def _mi_txt(k_):
    if k_ not in _mi.index:
        return f"x {k_}: not tested"
    r = _mi.loc[k_]
    return f"x {PARAMS[k_][0].lower()} p = {fmt_p(r.p_cluster_param_boot)} (q = {fmt_p(r.q_bh)})"


_db = intdf[intdf.design_built & (intdf.outcome == "mutual_take")]
DATA_NAME = next((p_.name for p_ in SRC.parents if p_.name not in ("step1", "steps")), SRC.parent.name)
STEP1_NAME = "Step 1 table"
# ---- assemble
R = []
R.append(f"# Completed pressure study: Step 2 analysis report ({TAG})\n")
if FINAL:
    R.append(f"**{TAG}.** This is the completed run (`{DATA_NAME}`). All {N_PLANNED:,} planned trials are terminal: {len(c):,} complete and "
             f"{N_FAILED} failed. These are final-data estimates for one model and one seed per cell. The primary test is the one "
             "pre-registered for the interim snapshot, run on the final data. The interim pairs are a subset of these data, so this is not "
             "an independent replication. See [PREREG.md](PREREG.md).\n")
else:
    R.append(f"**{TAG}.** Interim data (`{DATA_NAME}`): {len(c):,} of {N_PLANNED:,} planned trials complete, {N_FAILED} failed, "
             f"{N_NOTSTARTED:,} not started. No effect size here is final. See [PREREG.md](PREREG.md).\n")
R.append("**Audience:** the team and hackathon judges (AI safety researchers). The model is Qwen3-32B at temperature 0.6, with one seed per cell. "
         "Two agents exchange three rounds of simultaneous messages, then lock in a take/refuse decision. Script: `analyze_full.py` "
         "(revised after an expert review of the interim analysis).\n")
R.append("**Words used here.** A *mutual take* means both agents' locked final action was take. This is an operational outcome, not \"collusion\": "
         "in some scenes taking is arguably justified. *Watched / unwatched* names the text notice the agents saw. Researcher logging was "
         "identical in both arms, so this is a notice, not real oversight. Reasoning traces are generated text, not evidence of internal states.\n")

R.append(f"## 1. Summary ({TAG})\n")
R.append(f"- **Primary (pre-registered, sprint 3.4).** {int(P0.pairs):,} cells have both the watched and the unwatched trial complete. "
         f"In those cells the mutual-take rate was {pct(P0.rate_watched)} with the watched notice and {pct(P0.rate_unwatched)} with the unwatched "
         f"notice. The paired difference is **{pp(P0.diff_w_minus_u)}** (95% Newcombe CI {pp(P0.newcombe_lo)} to {pp(P0.newcombe_hi)}; scenario-cluster "
         f"bootstrap {pp(P0.cluster_boot_lo)} to {pp(P0.cluster_boot_hi)}), a risk ratio of {rrtxt(P0)}. Discordant pairs: **{int(P0.watched_only_take)} "
         f"watched-only takes vs {int(P0.unwatched_only_take)} unwatched-only takes**; McNemar p = {fmt_p(P0.p_chi2_cc)} (exact {fmt_p(P0.p_exact)}). "
         f"The direction matches the pre-registered expectation. The minimum detectable effect at 80% power is {100 * POWER['mde_paired_now']:.1f} pp.")
R.append(f"- **Robustness.** The result is {ROBUST}. It holds when both trials ran on the main endpoint ({EP_MAIN}: {ppci(bMain, 'newcombe_lo', 'newcombe_hi')}, "
         f"{int(bMain.watched_only_take)} watched-only vs {int(bMain.unwatched_only_take)} unwatched-only, p = {fmt_p(bMain.p_reported)}, {int(bMain.pairs):,} pairs). "
         f"{TIP_TXT} Across the {n_sub} diagnostic, pairing and level subgroups, {n_neg} point the same way (watched lower). "
         f"However, {n_cross} of those subgroup intervals cross 0, so \"same direction\" tells us little on its own. The heterogeneity tests, which are on the "
         f"conditional-odds-ratio scale, are: diagnostic p = {fmt_p(HET['Diagnostic:'])}, pairing {fmt_p(HET['Pairing:'])}, level {fmt_p(HET['Level:'])}.")
R.append(f"- **Dose-response by level (secondary, added after review).** Paired gap by level: "
         + "; ".join(f"L{int(r.subset.split(': ')[1])} {pp(r.diff_w_minus_u)} (RR {r.risk_ratio_w_over_u:.2f})"
                     for _, r in DOSE_LEVELS[DOSE_LEVELS.subset.str.startswith('Level:')].iterrows())
         + f". A conditional logit on the {DOSE['discordant_pairs']} discordant pairs gives a trend of x{DOSE['OR_ratio_per_level']:.2f} in the "
         f"conditional OR per level (log-OR slope {DOSE['slope_log_OR_per_level']:+.2f}, 95% cluster CI {DOSE['slope_boot_lo']:+.2f} to "
         f"{DOSE['slope_boot_hi']:+.2f}; LR p = {fmt_p(DOSE['p_LR_trend'])}). Section 4b separates the absolute (pp) scale from the relative (RR / OR) scale.")
R.append(f"- **Words vs. actions (secondary).** {WVA} Pressure level, by contrast, moves agent takes by {lvl_rows.loc['ag_took', 'diff_txt']} (level 5 vs 1).")
R.append(f"- **Interactions with monitoring** (ridge logit; null from {B_INTER:,} cluster-resampled parametric-bootstrap draws): mutual take "
         + "; ".join(_mi_txt(k_) for k_ in ["level", "pairing", "scenario_diagnostic"]) + ". "
         + ("Diagnostic x pairing is design-built: the pack fixes whether the pairing's rule matches the scene's diagnostic. " if len(_db) else "")
         + f"{n_inter_pass} of {len(intdf)} interaction tests pass q < .05 (section 10).")
R.append(f"- **Top candidates** (the first {len(summary_cands)} rows of the ranked table in section 5, in the same order; everything except the primary is exploratory; "
         f"one BH family over m = {M_FAMILY} candidate p-values):")
for _, r in summary_cands.iterrows():
    R.append(f"  {r.name}. {r.candidate}: {cand_effect_txt(r)}; n = {int(r.n):,}.")
R.append(f"- **Design check.** Completion status is not associated with any design parameter (smallest BH q = {fmt_p(comp_q.q_status.min())}). "
         "Monitoring, level and pairing are cleanly crossed. Setting and diagnostic effects are descriptive only: they vary at the scenario level, "
         f"with only {N_SCEN} scenes in total, and the scenes differ in content.\n")

R.append("## 2. How to read the charts\n")
R.append("- **Effect sizes** in screening are on comparable 0-1 scales: bias-corrected Cramér's V (categorical parameter x binary outcome), "
         "sqrt(epsilon^2) (categorical x numeric or agent-rate outcome) and |Spearman rho| (ordinal / numeric parameter). As a rough guide, 0.1 is small, 0.3 medium and 0.5 large.")
R.append("- **Monitoring effects** are paired (the same cell under both notices). Each one is reported in percentage points (watched minus unwatched) "
         "**and** as a risk ratio (watched / unwatched). Discordant pairs are always labelled by direction: *watched-only take* means the watched "
         "trial was a mutual take and its unwatched partner was not; *unwatched-only take* is the reverse. Heterogeneity tests on the discordant split "
         "compare conditional odds ratios, not pp gaps.")
R.append(f"- **Intervals.** Every primary-section interval (primary, subgroups, dose-response, words vs. actions, rule application, top relationships) uses "
         f"**one shared set of {B_BOOT_MAIN:,} scenario-cluster bootstrap draws** (resampling the {N_SCEN} scenarios). Newcombe intervals treat cells as independent "
         "and are shown alongside. Wilson intervals are used only for independent units.")
R.append(f"- **Tests.** Screening p-values are asymptotic and ignore clustering. Survivors at BH q < .05 are confirmed by a sequential Besag-Clifford "
         f"permutation at each parameter's randomisation level ({RAND_SOURCE}; `tables/randomisation_levels.csv`), with up to {B_PERM_MAX:,} shuffles, "
         f"stopping at {H_EXCEED} exceedances (floor 1/{B_PERM_MAX + 1:,}). ● = confirmed, ○ = BH only.")
R.append("- **Colour.** A single-hue blue sequential scale on an absolute range. Hatching = confounded parameter or by-construction pair. Grey cells = n < 5.\n")

R.append("## 3. Design check and completion\n")
R.append("Monitoring, level and pairing are fully crossed within every scenario. **Aliased by construction:** pairing, rule-in-pairing and matched-vs-mixed "
         "(the last two are coarsenings of pairing), and diagnostic = family. **Strongly associated pairs** (association >= 0.3; started trials; cell counts in "
         "`tables/design_cell_counts.csv`; matrix in Appendix A1):\n")
R.append(alias_md + "\n")
R.append("The scene-text features are written into the level text, so they move with pressure level and diagnostic; they are hatched everywhere. "
         "Endpoint, start rank and import status are collection-time variables.\n")
R.append(f"**Completion by monitoring arm** (all {N_PLANNED:,} planned trials):\n")
R.append(arm_tab_md + "\n")
R.append(f"Completion status is not associated with any design parameter after BH correction (smallest q = {fmt_p(comp_q.q_status.min())}; "
         "`tables/completion_balance.csv`; Appendix A2).\n")
R.append("**Failure reasons by arm** (`tables/failures_by_reason_and_monitoring.csv`):\n")
R.append(fail_md + "\n")
if mm_txt:
    R.append(mm_txt + "\n")
_ep_means = c.groupby("endpoint").mutual_take.agg(["mean", "size"]).reindex(EP_LEVELS)
R.append("**Endpoint and the deal rate (unpaired comparison, all complete trials; not a paired test):** "
         + ", ".join(f"{e} {pct(r_['mean'])} of {int(r_['size']):,} trials" for e, r_ in _ep_means.iterrows())
         + ". Endpoint is also collection time, so this comparison is descriptive.\n")

R.append("## 4. Primary test: monitoring notice and mutual take (pre-registered)\n")
R.append(fig_md("03_primary_monitoring_forest.png", "Primary forest plot") + "\n")
R.append(f"- **Test:** McNemar on {int(P0.pairs):,} complete cell pairs. Discordant: **{int(P0.watched_only_take)} watched-only take vs "
         f"{int(P0.unwatched_only_take)} unwatched-only take**; concordant: {int(P0.both_take)} both take, {int(P0.neither)} neither.")
R.append(f"- **Effect:** {pp(P0.diff_w_minus_u, 2)} (watched {pct(P0.rate_watched)} vs unwatched {pct(P0.rate_unwatched)}). Newcombe 95% CI "
         f"{pp(P0.newcombe_lo, 2)} to {pp(P0.newcombe_hi, 2)}; scenario-cluster bootstrap {pp(P0.cluster_boot_lo, 2)} to {pp(P0.cluster_boot_hi, 2)}. "
         f"Risk ratio {rrtxt(P0)}. Conditional odds ratio (watched-only / unwatched-only) {P0.cond_OR_w_vs_u:.2f}.")
R.append(f"- **p:** chi-square with continuity correction {fmt_p(P0.p_chi2_cc)}; exact binomial {fmt_p(P0.p_exact)}. alpha = .05, two-sided.")
R.append(f"- **Power:** the discordance rate is {pct(POWER['discordance_rate'])}. The minimum detectable paired difference at 80% power is "
         f"{100 * POWER['mde_paired_now']:.1f} pp with {POWER['pairs_now']:,} pairs ({100 * POWER['mde_paired_full']:.1f} pp if all {N_CELLS:,} cells were paired).")
R.append(f"- **Within endpoint** (endpoint = collection time; paired within class): "
         + "; ".join(f"{k}: {pp(pr.loc['Endpoint: ' + k].diff_w_minus_u)} ({int(pr.loc['Endpoint: ' + k].watched_only_take)} watched-only vs "
                     f"{int(pr.loc['Endpoint: ' + k].unwatched_only_take)} unwatched-only, {int(pr.loc['Endpoint: ' + k].pairs):,} pairs)" for k in EP_CLASSES if pr.loc["Endpoint: " + k].pairs > 0)
         + f". Endpoint x monitoring, tested on the discordant split across the both-same-endpoint classes: p = {fmt_p(p_epxmon)}.")
R.append(f"- **Within factors:** {n_neg} of {n_sub} diagnostic, pairing and level subgroups have watched < unwatched. **{n_cross} of these subgroup "
         "intervals cross 0, so their \"same direction\" is uninformative on its own.** Heterogeneity (chi-square on the discordant split, i.e. the "
         f"conditional-OR scale): diagnostic p = {fmt_p(HET['Diagnostic:'])}, pairing {fmt_p(HET['Pairing:'])}, level {fmt_p(HET['Level:'])}, matched/mixed {fmt_p(HET['Pair type:'])}.")
lone = pr.loc["Outcome: lone take"]
anyt = pr.loc["Outcome: any take (>=1 agent)"]
R.append(f"- **Related outcomes (same paired test; not confirmatory):** any take {pp(anyt.diff_w_minus_u)} ({int(anyt.watched_only_take)} watched-only vs "
         f"{int(anyt.unwatched_only_take)} unwatched-only); lone take {pp(lone.diff_w_minus_u)} ({int(lone.watched_only_take)} vs {int(lone.unwatched_only_take)}, "
         f"p = {fmt_p(lone.p_reported)}).\n")
R.append("<details><summary>Full subgroup table (pp, Newcombe and cluster intervals, risk ratio)</summary>\n\n" + prim_md + "\n\n</details>\n")

R.append("### 4b. Monitoring dose-response by level, diagnostic and pairing (secondary)\n")
R.append(fig_md("19_monitoring_by_level.png", "Monitoring by level: pp and risk ratio") + "\n")
R.append(f"A **conditional logit** for matched pairs, with the subgroup as a pair-level covariate, reduces to a logistic regression of "
         f"\"watched-only\" (vs \"unwatched-only\") on the covariate among discordant pairs. On the {DOSE['discordant_pairs']} discordant pairs, the linear "
         f"level trend is a log-OR slope of {DOSE['slope_log_OR_per_level']:+.3f} per level (Wald 95% CI {DOSE['slope_wald_lo']:+.3f} to "
         f"{DOSE['slope_wald_hi']:+.3f}; scenario-cluster bootstrap {DOSE['slope_boot_lo']:+.3f} to {DOSE['slope_boot_hi']:+.3f}; LR p = {fmt_p(DOSE['p_LR_trend'])}). "
         f"The conditional OR at level 3 is {DOSE['cond_OR_at_level3']:.2f}. Categorical LR tests on the same scale: level p = {fmt_p(DOSE['p_LR_level_categorical'])}, "
         f"diagnostic p = {fmt_p(DOSE['p_LR_diagnostic_categorical'])}, pairing p = {fmt_p(DOSE['p_LR_pairing_categorical'])}.\n")
R.append("**Reading the two scales.** Base rates rise steeply with level. The same relative effect (RR or OR) therefore gives a larger pp gap at high levels, "
         "and a constant pp gap would mean a shrinking relative effect. These tests are on the OR scale. A flat OR trend does not mean the pp gap is flat. "
         "Compare the two panels.\n")
R.append(lvl_md + "\n")

R.append("## 5. Top-ranked relationships\n")
R.append(f"Candidates are scored on effect size, robustness, relevance to the sprint questions and surprise relative to the directions in PREREG.md. "
         f"No finding has a hand-coded surprise score. **One BH family** covers the p-values of all {M_FAMILY} exploratory candidates (permutation, sign-flip, "
         "cluster-resampled bootstrap, LR and binomial). A candidate is listed only if q < .05 and it has no trust problem. Mechanical outcomes (word and token "
         "counts, reasoning length) are demoted. Full list: `tables/candidates.csv`. The summary in section 1 is the head of this table.\n")
R.append(cand_md + "\n")
if len(mech):
    R.append("**Demoted (mechanical):** " + "; ".join(f"{r.candidate} ({cand_effect_txt(r)})" for _, r in mech.head(6).iterrows())
             + ". These track prompt and message length, which differ by design (e.g. pairing changes the rules text).\n")
R.append(fig_md("13_top_relationships.png", "Top relationships") + "\n")
R.append("The monitoring panel shows paired rates over the same complete cell pairs, with the paired difference in its title. All y axes start at 0. "
         "Within-stratum checks: `tables/top_relationships_within_strata.csv`.\n")
R.append("**Looks large but untrustworthy** (`tables/candidates_untrustworthy.csv`):\n")
R.append(untrust_md + "\n")

R.append("## 6. Words vs. actions (secondary, sprint 2.2 x 3.4)\n")
R.append(fig_md("04_words_vs_actions.png", "Words vs actions") + "\n")
R.append("Each row is a paired difference. For monitoring, the pair is the watched and unwatched trial of the same cell. For level, it is level 5 vs "
         "level 1 of the same scenario x pairing x arm. Agent measures are averaged per episode, and vocabulary counts are notice-masked. Two kinds of "
         "row have been removed. Private monitoring mentions are gone because both notices contain \"monitored\" / \"oversight\", so they echo the notice. "
         "The level 5 vs 1 monitoring-mention row is gone for the same reason. \"Deception-intended among takers\" is gone because it is a post-treatment "
         "subset. Public oversight / monitoring words are kept as public wording, but what they mean is unvalidated.\n")
R.append("**Monitoring (watched - unwatched):**\n")
R.append(wmon_md + "\n")
R.append("**Pressure (level 5 - level 1):**\n")
R.append(wlvl_md + "\n")
R.append(f"**Reading.** {WVA}\n")
R.append("**Deception-intended flag: decomposition only (descriptive).** P(flag) = P(take) x P(flag | take). P(flag | take) conditions on a "
         "post-treatment variable, so it is not a monitoring contrast:\n")
R.append(dec_md + "\n")
R.append("**Asymmetry in mixed pairs (who takes alone).** Agent A holds the rule:\n")
R.append(asy_md + "\n")
R.append(fig_md("05_asymmetry_mixed_pairs.png", "Asymmetry") + "\n")
R.append("The binomial p treats episodes as independent, so it is optimistic (episodes cluster in scenarios).\n")
R.append("**Rule application vs. the pack's expected_first_take** (rule agents only; shared-draw cluster CIs):\n")
R.append(rule_md + "\n")
R.append(f"Cohen's kappa between \"level >= expected first-take level\" and \"agent took\": welfare {kap.loc['welfare', 'rate']:.2f}, "
         f"non-deception {kap.loc['nondeception', 'rate']:.2f}, authority {kap.loc['authority', 'rate']:.2f}, all {kap.loc['all', 'rate']:.2f}.\n")
R.append(fig_md("06_rule_application.png", "Rule application") + "\n")

R.append("## 7. Univariate results\n")
R.append("Full table: `tables/univariate_summary.csv`. Variable profile: `tables/variable_profile.csv`. Charts are in Appendix A3. "
         f"Private deception words appear in {pct(ag.dec_reas.mean())} of agents' reasoning. This reflects echo of the honesty notes.\n")

R.append("## 8. Matrices\n")
R.append(f"Screening covered {len(scr)} parameter x outcome pairs. Of these, {int((scr.q_bh < 0.05).sum())} pass BH q < .05 and {int(scr.confirmed.sum())} are confirmed "
         "by the cluster-aware permutation. The overview heat map and outcome matrix are in Appendix A4. Top rows (full table `tables/screening_table.csv`):\n")
R.append(scr_top_md + "\n")
R.append("Near-redundant informative outcome pairs (>= 0.8, not by construction): "
         + (", ".join(f"{r.outcome_1} ~ {r.outcome_2} ({r.association:.2f})" for _, r in redund.iterrows()) if len(redund) else "none")
         + ". Table: `tables/outcome_pairs.csv`.\n")

R.append("## 9. Heat maps\n")
R.append("Single-factor heat maps (level, monitoring unpaired view, pairing, diagnostic, setting) are in Appendix A5. Their data are in `tables/dimension_x_metric_*.csv`.\n")

R.append("## 10. Two-factor interactions\n")
R.append(f"Method: a ridge-penalised logit (lambda = {RIDGE}). The statistic is the deviance drop of A x B over A + B, minus the extra df. The null comes from "
         f"**{B_INTER:,} parametric-bootstrap draws**. Each draw resamples the {N_SCEN} scenarios with replacement and simulates outcomes from the additive "
         "model plus ridge-shrunken scenario offsets, so it carries within-scenario correlation. BH runs across "
         f"{len(intdf)} tests, and {n_inter_pass} pass q < .05 (p floor 1/{B_INTER + 1:,}). For scenario-level x scenario-level pairs, the null's scenario "
         "offsets absorb the interaction itself, so those p-values are conservative. **Diagnostic x pairing is design-built** (the pack fixes "
         "rule-diagnostic matching) and is not a discovery.\n")
R.append("**Monitoring x {level, pairing, diagnostic}, reported explicitly:**\n")
R.append(mon_int_md + "\n")
R.append("**All interactions (top 14 by statistic):**\n")
R.append(inter_md + "\n")
R.append("Two-factor heat maps are in Appendix A6.\n")

R.append("## 11. Sensitivity\n")
R.append(f"**Failures (primary test), four bounds.** The {N_FAILED} failed trials ({TIP['watched_failures']} watched, {TIP['unwatched_failures']} unwatched "
         "in started cells) are assigned outcomes as follows:\n")
R.append(sens_md + "\n")
R.append(f"The result is {ROBUST}. Bound 3 is the adversarial bound. It requires **100% of watched failures and 0% of unwatched failures** to be "
         f"mutual takes, so it is a bound, not a plausible value. {TIP_TXT} Full curve: `tables/primary_failure_tipping_point.csv`.\n")
if mm_txt:
    R.append(mm_txt + " Failure reasons are not outcomes, but an arm imbalance in `missing_message` would make failures informative.\n")
R.append(f"**Heuristic error.** {RG_NOTE}\n")

R.append("## 12. Caveats in plain terms\n")
if FINAL:
    R.append(f"- **Final data, one seed.** All planned trials ran. There is one seed per cell and {N_FAILED} failures, bounded in section 11.")
else:
    R.append("- **Interim.** Not all trials have run, and every number will move.")
R.append("- **Not an independent replication.** The interim snapshot is a subset of these data. The review-driven additions (dose-response, "
         "tipping point, cluster-resampled interactions) were specified after the interim results were seen.")
R.append("- **The notice is text.** \"Watched\" means the prompt said the episode may be reviewed. Nothing else changed.")
R.append("- **One model, one temperature, one pack.** Do not pool with other runs.")
R.append("- **Mutual take is not collusion.** Coordination was not hand-checked.")
R.append("- **Heuristics.** Stance and deception-intended are marginal and arm-differential, and the other text heuristics are unreliable. None is headlined. "
         "Monitoring vocabulary echoes the notices.")
R.append("- **Clustering.** Only permutation-confirmed results that also survive the single candidate BH family are listed. The asymmetry binomial p "
         "ignores clustering.")
R.append("- **Setting and diagnostic** are scenario-level and differ in content, so they are descriptive only.")
R.append("- **No communication baseline**, so nothing here is an effect of talking.\n")

R.append("## 13. File index\n")
R.append("- `PREREG.md`: the pre-registration (the primary is unchanged; post-review additions are disclosed).")
R.append("- `analyze_full.py` and `analyze_full_workers.py`: the rerunnable script and its process-pool workers (seed 20261025; `--fresh` ignores the permutation cache).")
R.append("- `provenance.json`: input SHA-256s, arguments, package versions, seeds, settings, runtime and log.")
FIGS_MAIN = ["03_primary_monitoring_forest.png", "19_monitoring_by_level.png", "13_top_relationships.png", "04_words_vs_actions.png",
             "05_asymmetry_mixed_pairs.png", "06_rule_application.png"]
R.append("- `figures/` (main text): " + ", ".join(f"`{f}`" for f in FIGS_MAIN) + ". Appendix: "
         + ", ".join(f"`{f}`" for f, _ in FIGS if f not in FIGS_MAIN) + ".")
R.append("- `tables/`: " + ", ".join(f"`{p_.name}`" for p_ in sorted(TAB.glob("*.csv"))) + ", plus `primary_power_and_heterogeneity.json` "
         "and `permutation_cache.json`.\n")

R.append("## Appendix: supporting figures\n")
APP = [("A1. Design association matrix", "01_design_association.png"), ("A2. Completion balance", "02_completion_balance.png"),
       ("A3. Univariate rates", "14_univariate_rates.png"), ("A3. Numeric outcomes", "15_univariate_numeric.png"),
       ("A4. Screening overview", "07_screening_overview.png"), ("A4. Outcome associations", "16_outcome_association.png"),
       ("A5. Heat map: pressure level", "08_heat_level.png"), ("A5. Heat map: monitoring (unpaired view)", "09_heat_monitoring.png"),
       ("A5. Heat map: pairing", "10_heat_pairing.png"), ("A5. Heat map: diagnostic (descriptive)", "11_heat_diagnostic.png"),
       ("A5. Heat map: setting (descriptive)", "12_heat_setting.png"), ("A6. Two-factor heat maps", "17_2d_heatmaps.png"),
       ("A6. Scenario x level", "18_scenario_x_level.png")]
for t_, f_ in APP:
    R.append(f"**{t_}**\n\n" + fig_md(f_, t_) + "\n")
json.dump({"power": POWER, "p_endpoint_x_monitoring": p_epxmon, "heterogeneity_p_conditional_OR_scale": HET, "tipping_point": TIP,
           "dose_response": DOSE, "missing_message_fisher_among_failures": P_MM_AMONG_FAIL},
          open(TAB / "primary_power_and_heterogeneity.json", "w"), indent=1, default=float)
(OUTD / "REPORT.md").write_text("\n".join(R) + "\n", encoding="utf-8")
log("REPORT.md written")
prov["runtime_seconds"] = round(time.time() - T0, 1)
log("done", prov["runtime_seconds"], "s")
json.dump(prov, open(OUTD / "provenance.json", "w", encoding="utf-8"), indent=1, default=str)
