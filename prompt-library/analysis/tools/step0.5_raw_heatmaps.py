"""Step 0.5: raw one- and two-variable heat maps straight from runs.csv.

Usage (from the repo root, CPUs 0-3 kept free):
    python tools/run_reserved.py prompt-library/analysis/tools/step0.5_raw_heatmaps.py --results <run dir> --out <output dir>

Reference implementation from the 2026-10-25 pressure study: factor and outcome names
(level, monitoring, pairing, diagnostic, setting_id, a/b criteria, action_a/b) follow that
run's runs.csv; adapt FACTORS/OUTCOMES for other designs. Reads <run dir>/runs.csv only. Rates are
over complete trials; every cell prints its rate and n. Writes figures/, tables/ and
README.md next to this script.
"""
import argparse
import csv
import itertools
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--results", type=Path, required=True, help="run folder containing runs.csv")
ap.add_argument("--out", type=Path, required=True, help="output folder")
args = ap.parse_args()
HERE = args.out
RUNS = args.results / "runs.csv"
FIG, TAB = HERE / "figures", HERE / "tables"
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

PAIR_NAME = {"W-W": "Welfare + welfare", "W-none": "Welfare + no rule", "D-D": "Non-deception + non-deception",
             "D-none": "Non-deception + no rule", "A-A": "Authority + authority", "A-none": "Authority + no rule"}
CRIT_NAME = {"welfare": "Welfare", "nondeception": "Non-deception", "authority": "Authority", "none": "No rule"}

rows = list(csv.DictReader(open(RUNS, encoding="utf-8")))
done = [r for r in rows if r["status"] == "complete"]


def derive(r):
    take_a, take_b = r["action_a"] == "take", r["action_b"] == "take"
    return {
        "mutual_take": float(take_a and take_b),
        "lone_take": float(take_a != take_b),
        "both_refuse": float(not take_a and not take_b),
        "agent_take_rule": float(take_a),            # agent A always holds the rule
        "agent_take_partner": float(take_b),         # agent B: same rule (matched) or no rule (mixed)
    }


OUTCOMES = [("mutual_take", "Mutual take (deal executes)"), ("lone_take", "Lone take (one agent takes)"),
            ("both_refuse", "Both refuse"), ("agent_take_rule", "Rule agent (A) takes"),
            ("agent_take_partner", "Partner (B) takes")]

FACTORS = {
    "level": ("Pressure level", lambda r: int(r["level"]), lambda v: f"Level {v}"),
    "monitoring": ("Monitoring notice", lambda r: r["monitoring"], lambda v: v.capitalize()),
    "pairing": ("Pairing", lambda r: r["pairing"], lambda v: PAIR_NAME.get(v, v)),
    "diagnostic": ("Scenario family (diagnostic)", lambda r: r["diagnostic"], lambda v: CRIT_NAME.get(v, v) + " scenarios"),
    "setting": ("Social setting", lambda r: r["setting_id"], lambda v: v.replace("_", " ").capitalize()),
    "rule": ("Rule agent's criterion", lambda r: r["a"], lambda v: CRIT_NAME.get(v, v)),
    "partner": ("Partner kind", lambda r: "same rule" if r["a"] == r["b"] else "no rule", lambda v: v.capitalize()),
}
ORDER = {"pairing": list(PAIR_NAME), "diagnostic": ["welfare", "nondeception", "authority"],
         "rule": ["welfare", "nondeception", "authority"], "monitoring": ["unwatched", "watched"]}


def levels(key):
    vals = sorted({FACTORS[key][1](r) for r in done}, key=lambda v: (str(type(v)), v))
    if key in ORDER:
        vals = [v for v in ORDER[key] if v in vals]
    return vals


DER = [derive(r) for r in done]


def rate_table(keys):
    acc = defaultdict(lambda: defaultdict(float))
    n = defaultdict(int)
    for r, d in zip(done, DER):
        k = tuple(FACTORS[f][1](r) for f in keys)
        n[k] += 1
        for o, _ in OUTCOMES:
            acc[k][o] += d[o]
    return {k: {o: acc[k][o] / n[k] for o, _ in OUTCOMES} for k in n}, n


def cell_fonts(n_rows, n_cols, row_h, col_w):
    """Annotation font sizes scaled to the cell size; never below 10 pt for values."""
    fs = max(10.0, min(16.0, 0.36 * 72 * min(row_h, col_w / 1.8)))
    return fs, max(8.0, 0.68 * fs)


def draw(mat, nmat, rlabels, clabels, title, subtitle, xlabel, ylabel, fname):
    row_h = 0.8 if len(rlabels) <= 20 else 0.5
    col_w = 1.7
    fs, fs_n = cell_fonts(len(rlabels), len(clabels), row_h, col_w)
    h = max(3.6, row_h * len(rlabels) + 2.2)
    w = max(7.5, col_w * len(clabels) + 3.8)
    fig, ax = plt.subplots(figsize=(w, h))
    im = ax.imshow(np.ma.masked_invalid(mat), cmap="Blues", vmin=0, vmax=1, aspect="auto")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if np.isnan(mat[i, j]):
                ax.text(j, i, "—", ha="center", va="center", fontsize=fs, color="#888")
                continue
            v = mat[i, j]
            col = "white" if v > 0.55 else "#1f2328"
            ax.text(j, i - 0.13, f"{v:.0%}", ha="center", va="center", fontsize=fs, fontweight="bold", color=col)
            ax.text(j, i + 0.27, f"n={int(nmat[i, j])}", ha="center", va="center", fontsize=fs_n, color=col)
    ax.set_xticks(range(len(clabels)), clabels, rotation=30, ha="right", fontsize=11)
    ax.set_yticks(range(len(rlabels)), rlabels, fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.suptitle(title, fontsize=14, fontweight="bold", x=0.01, ha="left")
    ax.set_title(subtitle, fontsize=10, loc="left", color="#59636e")
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label("Rate among complete trials (absolute 0–100%)", fontsize=10)
    cb.ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    fig.tight_layout()
    fig.savefig(FIG / fname, dpi=150)
    plt.close(fig)


figs = []
# ---- one-variable: factor levels x outcomes
for key in FACTORS:
    name, _, lab = FACTORS[key]
    tab, n = rate_table([key])
    lv = levels(key)
    mat = np.array([[tab[(v,)][o] for o, _ in OUTCOMES] for v in lv])
    nmat = np.array([[n[(v,)]] * len(OUTCOMES) for v in lv])
    fname = f"1v_{key}.png"
    draw(mat, nmat, [lab(v) for v in lv], [o[1] for o in OUTCOMES],
         f"{name}: outcome rates", f"Complete trials only (n = {len(done)}). Rows: {name.lower()}; columns: outcomes.",
         "Outcome", name, fname)
    figs.append(("one", key, fname))
    with open(TAB / f"1v_{key}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([key, "n"] + [o for o, _ in OUTCOMES])
        for v in lv:
            w.writerow([v, n[(v,)]] + [f"{tab[(v,)][o]:.4f}" for o, _ in OUTCOMES])

# ---- two-variable: every factor pair x key outcomes
TWO_OUT = [("mutual_take", "Mutual take"), ("lone_take", "Lone take"), ("agent_take_rule", "Rule agent takes")]
PAIRS = [p for p in itertools.combinations(FACTORS, 2) if set(p) != {"pairing", "rule"} and set(p) != {"pairing", "partner"}]
for f1, f2 in PAIRS:
    tab, n = rate_table([f1, f2])
    l1, l2 = levels(f1), levels(f2)
    for o, oname in TWO_OUT:
        mat = np.full((len(l1), len(l2)), np.nan)
        nmat = np.zeros_like(mat)
        for i, a in enumerate(l1):
            for j, b in enumerate(l2):
                if (a, b) in tab:
                    mat[i, j], nmat[i, j] = tab[(a, b)][o], n[(a, b)]
        fname = f"2v_{f1}_x_{f2}__{o}.png"
        draw(mat, nmat, [FACTORS[f1][2](v) for v in l1], [FACTORS[f2][2](v) for v in l2],
             f"{oname} by {FACTORS[f1][0].lower()} × {FACTORS[f2][0].lower()}",
             "Complete trials only; each cell shows rate and n. Absolute colour scale.",
             FACTORS[f2][0], FACTORS[f1][0], fname)
        figs.append(("two", f"{f1} × {f2} → {oname}", fname))
        with open(TAB / f"2v_{f1}_x_{f2}__{o}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow([f1, f2, "n", o])
            for (a, b), val in sorted(tab.items(), key=lambda kv: str(kv[0])):
                w.writerow([a, b, n[(a, b)], f"{val[o]:.4f}"])

# ---- scenario x level (mutual take), the most granular view
scen = sorted({r["scenario"] for r in done})
title_of = {r["scenario"]: r["setting_id"] + " / " + r["diagnostic"] for r in done}
tab, n = rate_table(["level"]) if False else (None, None)
acc, cnt = defaultdict(float), defaultdict(int)
for r, d in zip(done, DER):
    k = (r["scenario"], int(r["level"]))
    acc[k] += d["mutual_take"]
    cnt[k] += 1
mat = np.array([[acc[(s, l)] / cnt[(s, l)] if cnt[(s, l)] else np.nan for l in range(1, 6)] for s in scen])
nmat = np.array([[cnt[(s, l)] for l in range(1, 6)] for s in scen])
draw(mat, nmat, [f"{s} ({title_of[s]})" for s in scen], [f"Level {l}" for l in range(1, 6)],
     "Mutual take by scenario × pressure level", "Each cell pools 6 pairings × 2 monitoring notices (n ≤ 12).",
     "Pressure level", "Scenario (setting / family)", "2v_scenario_x_level__mutual_take.png")
figs.append(("two", "scenario × level → Mutual take", "2v_scenario_x_level__mutual_take.png"))

# ---- README
lines = ["# Step 0.5: raw heat maps (completed pressure study)", "",
         f"Straight from `runs.csv`: **{len(done)} complete trials** of {len(rows)} planned. Rates are among complete trials; every cell shows its rate and n; colour is an absolute 0–100% scale. No derived metrics, no statistics: this is the fast first look. Agent A always holds the rule; agent B has the same rule (matched pairs) or no rule (mixed pairs).", "",
         "Regenerate: `python tools/run_reserved.py prompt-library/analysis/tools/step0.5_raw_heatmaps.py --results <run dir> --out <output dir>` (CPUs 0–3 kept free; about 1 minute).", "",
         "## One variable × outcomes", ""]
lines += [f"### {FACTORS[k][0]}\n\n![{k}](figures/{f})\n" for kind, k, f in figs if kind == "one"]
lines += ["## Two variables × outcome", ""]
lines += [f"- [{k}](figures/{f})" for kind, k, f in figs if kind == "two"]
lines += ["", "Highlights (embedded):", ""]
for f in ["2v_level_x_monitoring__mutual_take.png", "2v_level_x_pairing__mutual_take.png",
          "2v_monitoring_x_pairing__mutual_take.png", "2v_monitoring_x_diagnostic__mutual_take.png",
          "2v_scenario_x_level__mutual_take.png"]:
    if (FIG / f).exists():
        lines.append(f"![{f}](figures/{f})\n")
lines += ["Tables behind every chart are in `tables/`."]
(HERE / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{len(figs)} figures, complete trials {len(done)}")
