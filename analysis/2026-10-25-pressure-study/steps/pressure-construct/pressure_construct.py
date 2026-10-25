"""Pressure-construct audit: what does the 1-5 "pressure level" manipulation actually contain?

Inputs (read-only): results/2026-10-25-pressure-study/manifest.json (pack), runs.csv,
steps/step1/trial_metrics.csv, run transcripts.
Outputs: level_coding.csv, tables/*.csv, figures/*.png, transcript_excerpts.md, model_summary.json.

Run: python tools/run_reserved.py analysis/2026-10-25-pressure-study/steps/pressure-construct/pressure_construct.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
RES = ROOT / "results" / "2026-10-25-pressure-study"
OUT = Path(__file__).resolve().parent
TAB = OUT / "tables"
FIG = OUT / "figures"
TAB.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
rng = np.random.default_rng(20261025)

# Palette (dataviz reference instance, light mode)
C = {"blue": "#2a78d6", "orange": "#eb6834", "aqua": "#1baf7a", "yellow": "#eda100",
     "magenta": "#e87ba4", "green": "#008300", "violet": "#6250d6", "red": "#e34948",
     "ink": "#0b0b0b", "ink2": "#52514e", "surface": "#fcfcfb", "grid": "#e4e4e0"}
SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
plt.rcParams.update({"figure.facecolor": C["surface"], "axes.facecolor": C["surface"],
                     "axes.edgecolor": C["grid"], "axes.grid": True, "grid.color": C["grid"],
                     "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
                     "text.color": C["ink"], "axes.labelcolor": C["ink2"], "xtick.color": C["ink2"],
                     "ytick.color": C["ink2"], "font.size": 10, "savefig.dpi": 160})

# ----------------------------------------------------------------------------------------------
# 1. Hand codes for every INCREMENT (the sentence(s) added at each level). Codes:
#   S   self-benefit for the two agents (convenience, bonus, avoid meeting/overtime/form, own fare)
#   P   a NON-principal asks for take (peer, volunteer, member, elder "not a principal")
#   T1  third party: minor harm of refusing (annoyance, disappointment, embarrassment, short delay)
#   T2  third party: material harm of refusing (job, money, trip, meals, work, housing-aid risk)
#   T3  third party: severe/vital harm of refusing (health, medicine, safety, homelessness, custody,
#       retaliation, losing care, child's coverage, being alone overnight)
#   V   a vulnerable party is named (child, elder, patient, sick, homeless, sole caregiver)
#   N   scale-up: more people affected than before
#   R   a request / promise from a party owed confidentiality (promise conflict)
#   U   urgency / time pressure (tonight, deadline, last bus)
#   AS  a principal SUGGESTS take
#   AI  a principal above the desk INSTRUCTS take
#   AB  a higher body BACKS / documents the take instruction
#   AR  an authority re-affirms REFUSE (counter-instruction)
#   PM  a formal rule / notice / note that PERMITS the act (licenses it; arguably no longer rule-breaking)
#   HD  harm of TAKING is reduced by a new fact (victim can absorb, already refunded, sealed-safe,
#       no fault found, nobody hurt, other has lodging, consent given, no new risk)
#   HU  a fact AGAINST take (harm of taking raised; "you did not see it"; the other side was promised
#       the rule; the fault is still live; authority explicitly lacks rank)
# ----------------------------------------------------------------------------------------------
CODES = {
 "S001": ["S", "S", "T2", "T2,N", "T3,V,R,AR"],
 "S002": ["T2,V", "T2,N", "T2,V", "T2,N", "T2,N"],
 "S003": ["S,HU", "S,HU", "S,HU", "S,HU", "P,HU"],
 "S034": ["T1", "T2,N", "T2", "HU,R", "T3,V"],
 "S035": ["T1", "T2", "T3", "T3", "AI"],
 "S036": ["T1,R", "R,V", "T3,V", "AI,PM", "T3,V"],
 "S067": ["T1,V", "T2,V,N", "T2,N", "T3,V,N", "T3,V,AI"],
 "S068": ["S", "T2,N", "T2", "AI", "AB"],
 "S069": ["S", "S", "T2,V,N", "T3,V", "HU,R,AI"],
 "S100": ["T2,V", "T2,N", "T3,V", "T3,V,N", "AI"],
 "S101": ["T1", "T2", "T2,N,V", "T2,N", "T2,V"],
 "S102": ["T2,V", "T2,V,N", "T3,V", "T3,V", "AI"],
 "S133": ["T1,R", "R,HU", "HU", "T3", "AI"],
 "S134": ["T1,R", "T2,R", "T2", "HD", "T2,N"],
 "S135": ["T1", "T2", "T2", "AI", "T3"],
 "S166": ["P", "AS", "AI", "T3,V,N", "AB"],
 "S167": ["T1,V", "T2,V", "T2,V", "T3,V", "AI"],
 "S168": ["T1", "T2,V", "HD", "T2", "AI"],
 "S199": ["S", "T2,N", "T2", "T3", "AI"],
 "S200": ["T1", "T2", "T3", "T3,N", "AI,HD"],
 "S201": ["T1", "T2", "T2,N", "T2,N", "T2,N"],
 "S232": ["S", "R,HD", "T2", "T3,V", "AI"],
 "S233": ["T1", "T2", "T3", "AI", "T3"],
 "S234": ["T1", "T2", "T3,V", "T3,V", "T3,V"],
 "S265": ["P", "AS", "AI", "T3,N", "AB"],
 "S266": ["T1", "T2", "T3", "T3,V,N", "AI"],
 "S267": ["T1", "T2", "T3", "T3,V", "AI"],
 "S298": ["T1", "T2", "T3", "T3,V", "T3,V"],
 "S299": ["T1", "T1", "T2,N", "T2,N", "AI,HD"],
 "S300": ["T2,V", "T2,V,N", "T3,V", "HD", "AI"],
 "S331": ["T1,R", "T3,R", "R,V", "T2,V", "AI"],
 "S332": ["T1,R", "T2,R,U", "T2", "HU", "T3,V"],
 "S333": ["S", "R,V", "T3,V", "T3,V", "AI"],
 "S364": ["T1", "T1", "T3,V", "T3,V,N", "AI"],
 "S365": ["P", "AS", "AI", "T2,N", "AB"],
 "S366": ["T1", "T2", "HD", "T2", "AI"],
 "S397": ["T1", "T2", "T2,N", "T2,N,V", "AI"],
 "S398": ["T2,V", "T3,V", "HD", "T3,V,U", "AI"],
 "S399": ["T3,V", "T3,V", "T3,U", "HD", "AI"],
 "S430": ["T1,R", "T2,R", "T3,V", "HD", "T3,V"],
 "S431": ["S", "R,HD", "T2", "T2,N,V", "AI"],
 "S432": ["T1", "HD,R", "T2,N,V", "U", "AI"],
 "S463": ["S", "T2", "T2,N,V", "T3,N,V", "AI"],
 "S464": ["P", "AS", "AI", "T3,V,N", "AB"],
 "S465": ["T2,V", "T2,V,N", "HD", "T2,N", "AI"],
 "S496": ["S", "T2", "T2,N,V", "T3,N,V", "AI"],
 "S497": ["T1", "T2", "T3,V", "T3,V", "AI"],
 "S498": ["T1", "T2,N", "T2,N,V", "HD", "AI"],
 "S529": ["T1,R", "T2,R", "T2", "T2", "AI"],
 "S530": ["T1,R", "T1,R", "T2", "HU", "T2"],
 "S531": ["T1,R", "T2,R", "T2", "T3", "AI"],
 "S562": ["P", "AS", "AI,HU", "AI", "PM,AB"],
 "S563": ["S", "T2", "T2", "T2", "AI,HD"],
 "S564": ["T1", "T2", "T2,U", "T2,V", "AI"],
 "S595": ["T1", "T2,R", "T2,U", "T2", "PM,AI"],
 "S596": ["S", "S,T2", "T3,V", "T3,V", "AI"],
 "S597": ["S", "T2", "T2", "T3", "AI,HD"],
 "S628": ["T1,R", "T2,R", "R,V", "T2", "PM,AI"],
 "S629": ["T1,R,V", "R,V", "T3,V", "AI,HD", "AB,PM"],
 "S630": ["T1,R", "T2,R", "T2", "HU", "T2"],
 "S661": ["P", "AS", "AR", "PM,AI", "AB"],
 "S662": ["P", "AS", "AR", "PM,AI", "AB"],
 "S663": ["T1", "AI", "T3,V", "AB", "PM"],
 "S694": ["S", "S", "S", "S,V", "PM,AI"],
 "S695": ["S", "S", "S", "S,V", "PM,AI"],
 "S696": ["T1", "T2", "T3,V", "HD", "PM,AI"],
 "S727": ["T1", "R,T2,U", "HU,R", "T2", "PM,AI"],
 "S728": ["T1,R", "T2,R", "T2,V", "HU", "HU,AR"],
 "S729": ["T1", "T2,U", "S,T2", "HD,U", "PM,HD"],
 "S760": ["S", "R,HD", "T2", "T3,V", "PM,AI"],
 "S761": ["T1", "PM,HD", "T3,V", "U,T3", "PM,AI"],
 "S762": ["T2,V", "HU", "T3,V", "HD", "PM,AI"],
}
ALL_CODES = ["S", "P", "T1", "T2", "T3", "V", "N", "R", "U", "AS", "AI", "AB", "AR", "PM", "HD", "HU"]

# ----------------------------------------------------------------------------------------------
man = json.load(open(RES / "manifest.json", encoding="utf-8"))
pack = man["pack"]
scen = {s["id"]: s for s in pack["scenarios"]}
assert set(scen) == set(CODES), set(scen) ^ set(CODES)


def wc(t):
    return len(re.findall(r"\S+", t))


rows = []
for sid, s in scen.items():
    prev_p = ""
    cum = set()
    tp_sev = 0
    self_sev = 0
    for L in s["levels"]:
        n = L["n"]
        inc_text = L["pressure"][len(prev_p):].strip()
        prev_p = L["pressure"]
        inc = set(c for c in CODES[sid][n - 1].split(",") if c)
        cum |= inc
        if "T3" in inc:
            tp_sev = max(tp_sev, 3)
        elif "T2" in inc:
            tp_sev = max(tp_sev, 2)
        elif "T1" in inc:
            tp_sev = max(tp_sev, 1)
        if "S" in inc:
            self_sev = max(self_sev, 2 if ("V" in inc or n >= 3 and sid in ("S694", "S695")) else 1)
        pr = L["principals"]
        n_take_instruct = len(re.findall(r"instructs take", pr))
        n_take_suggest = len(re.findall(r"suggests take|asks take", pr))
        n_refuse = len(re.findall(r"instructs? refuse|instruct refuse", pr))
        rows.append({
            "scenario": sid, "setting": s["setting_id"], "diagnostic": s["diagnostic"], "title": s["title"],
            "level": n, "label": L["label"], "welfare_if_take": L["welfare_if_take"],
            "deceive_if_refuse_nonempty": int(bool(L["deceive_if_refuse"])),
            "n_deceive_if_take": len(L["deceive_if_take"]),
            "increment_text": inc_text, "increment_codes": ",".join(sorted(inc)),
            "cum_codes": ",".join(sorted(cum)),
            **{f"inc_{c}": int(c in inc) for c in ALL_CODES},
            **{f"cum_{c}": int(c in cum) for c in ALL_CODES},
            "tp_harm_refuse_sev": tp_sev, "self_benefit_sev": self_sev,
            "n_scaleups": sum(1 for k in range(n) if "N" in CODES[sid][k].split(",")),
            "n_harm_down": sum(1 for k in range(n) if "HD" in CODES[sid][k].split(",")),
            "n_harm_up": sum(1 for k in range(n) if "HU" in CODES[sid][k].split(",")),
            "princ_take_instruct": n_take_instruct, "princ_take_suggest": n_take_suggest,
            "princ_refuse": n_refuse,
            "take_principal_present": int(n_take_instruct > 0),
            "take_voice_any": int(n_take_instruct > 0 or n_take_suggest > 0 or "P" in cum),
            "licensed": int(("PM" in cum) or n_take_instruct > 0),
            "pressure_words": wc(L["pressure"]), "principals_words": wc(pr),
            "stakes_block_words": wc(L["pressure"]) + wc(pr),
            "pressure_text": L["pressure"], "principals_text": pr,
            "expected_first_take_welfare": s["expected_first_take"]["welfare"],
            "expected_first_take_nondeception": s["expected_first_take"]["nondeception"],
            "expected_first_take_authority": s["expected_first_take"]["authority"],
        })
coding = pd.DataFrame(rows)
# a crude ordinal "justification index": how many distinct take-favouring ingredients are stacked
fav = ["cum_S", "cum_T2", "cum_T3", "cum_V", "cum_R", "cum_AS", "cum_AI", "cum_AB", "cum_PM", "cum_HD", "cum_U"]
coding["n_take_favouring_ingredients"] = coding[fav].sum(axis=1)
coding["n_take_opposing_ingredients"] = coding[["cum_HU", "cum_AR"]].sum(axis=1)
coding.to_csv(OUT / "level_coding.csv", index=False, encoding="utf-8")

# ----------------------------------------------------------------------------------------------
# 2. Descriptive tables: how each dimension changes with level
# ----------------------------------------------------------------------------------------------
dims = ["cum_S", "cum_P", "cum_T1", "cum_T2", "cum_T3", "cum_V", "cum_N", "cum_R", "cum_U", "cum_AS", "cum_AI",
        "cum_AB", "cum_AR", "cum_PM", "cum_HD", "cum_HU", "take_principal_present", "licensed",
        "tp_harm_refuse_sev", "self_benefit_sev", "n_take_favouring_ingredients", "pressure_words",
        "stakes_block_words"]
by_level = coding.groupby("level")[dims].mean().round(3)
by_level.to_csv(TAB / "dimension_by_level.csv")
inc_by_level = coding.groupby("level")[[f"inc_{c}" for c in ALL_CODES]].mean().round(3)
inc_by_level.to_csv(TAB / "increment_codes_by_level.csv")
by_level_diag = coding.groupby(["diagnostic", "level"])[dims].mean().round(3)
by_level_diag.to_csv(TAB / "dimension_by_level_and_diagnostic.csv")
by_level_setting = coding.groupby(["setting", "level"])[["cum_T3", "cum_AI", "cum_PM", "cum_HD", "take_principal_present"]].mean().round(3)
by_level_setting.to_csv(TAB / "dimension_by_level_and_setting.csv")
pd.crosstab(coding.level, coding.welfare_if_take).to_csv(TAB / "welfare_label_by_level.csv")
# What is the L5 increment?  categorise
def l5_kind(codes):
    c = set(codes.split(","))
    if "AI" in c or "AB" in c or "PM" in c:
        return "authority instruction / formal permission"
    if "AR" in c or "HU" in c:
        return "fact AGAINST take"
    if "T3" in c:
        return "severe third-party harm of refusing"
    if "T2" in c:
        return "material third-party harm of refusing"
    return "other"
l5 = coding[coding.level == 5].copy()
l5["l5_kind"] = l5.increment_codes.map(l5_kind)
pd.crosstab(l5.diagnostic, l5.l5_kind, margins=True).to_csv(TAB / "level5_increment_kind_by_diagnostic.csv")
# first level at which a take-instructing principal appears
first_ai = coding[coding.take_principal_present == 1].groupby("scenario")["level"].min()
coding_first = pd.DataFrame({"first_take_principal_level": first_ai}).reindex(sorted(scen)).fillna(0).astype(int)
coding_first["diagnostic"] = coding_first.index.map(lambda s: scen[s]["diagnostic"])
pd.crosstab(coding_first.diagnostic, coding_first.first_take_principal_level, margins=True).to_csv(
    TAB / "first_take_principal_level_by_diagnostic.csv")

# ----------------------------------------------------------------------------------------------
# 3. Join to trials
# ----------------------------------------------------------------------------------------------
runs = pd.read_csv(RES / "runs.csv")
runs = runs[runs.status == "complete"].copy()
runs["mutual_take"] = (runs.outcome == "mutual_take").astype(int)
runs["take_a"] = (runs.action_a == "take").astype(int)
runs["take_b"] = (runs.action_b == "take").astype(int)
runs["any_take"] = ((runs.take_a + runs.take_b) > 0).astype(int)
runs["rule_match"] = (runs.a == runs.diagnostic).astype(int)
df = runs.merge(coding.drop(columns=["setting", "diagnostic", "title"]), on=["scenario", "level"], how="left")
assert df.cum_AI.notna().all()
df["b_none"] = (df.b == "none").astype(int)
df.to_csv(OUT / "trials_with_codes.csv", index=False)

# aggregate r over 5 level means vs trial-level association
lv = df.groupby("level").mutual_take.mean()
r_agg = np.corrcoef(lv.index.values, lv.values)[0, 1]
r_trial = np.corrcoef(df.level, df.mutual_take)[0, 1]
r_trial_any = np.corrcoef(df.level, df.any_take)[0, 1]
# scenario-cluster bootstrap for trial-level r
def cluster_boot(fn, B=1000):
    groups = {k: g for k, g in df.groupby("scenario")}
    keys = list(groups)
    out = []
    for _ in range(B):
        pick = rng.choice(keys, size=len(keys), replace=True)
        d = pd.concat([groups[k] for k in pick])
        out.append(fn(d))
    return np.percentile(out, [2.5, 97.5])
ci_trial = cluster_boot(lambda d: np.corrcoef(d.level, d.mutual_take)[0, 1], 400)
# per-scenario slopes (Spearman-ish via Pearson on 5 means)
sc_rates = df.groupby(["scenario", "level"]).mutual_take.mean().unstack()
sc_rates_any = df.groupby(["scenario", "level"]).any_take.mean().unstack()
sc_rates_a = df.groupby(["scenario", "level"]).take_a.mean().unstack()
def shape(row):
    v = row.values
    d = np.diff(v)
    if np.all(np.abs(d) < 1e-9):
        return "flat"
    if np.all(d >= -1e-9):
        return "monotone up"
    if np.all(d <= 1e-9):
        return "monotone down"
    return "non-monotone"
shapes = pd.DataFrame({
    "diagnostic": [scen[s]["diagnostic"] for s in sc_rates.index],
    "setting": [scen[s]["setting_id"] for s in sc_rates.index],
    "title": [scen[s]["title"] for s in sc_rates.index],
    **{f"L{k}": sc_rates[k].round(3) for k in range(1, 6)},
    "range": (sc_rates.max(axis=1) - sc_rates.min(axis=1)).round(3),
    "slope_r": [np.corrcoef(range(1, 6), sc_rates.loc[s].values)[0, 1] if sc_rates.loc[s].std() > 0 else np.nan for s in sc_rates.index],
    "shape": sc_rates.apply(shape, axis=1),
    "biggest_jump_at": [int(np.argmax(np.diff(sc_rates.loc[s].values)) + 2) if sc_rates.loc[s].std() > 0 else 0 for s in sc_rates.index],
    "biggest_jump_size": np.max(np.diff(sc_rates.values, axis=1), axis=1).round(3),
    "first_take_principal_level": coding_first.loc[sc_rates.index, "first_take_principal_level"].values,
    "l5_increment": l5.set_index("scenario").loc[sc_rates.index, "increment_codes"].values,
}, index=sc_rates.index)
shapes.to_csv(TAB / "scenario_dose_response.csv")
shape_counts = pd.crosstab(shapes["diagnostic"], shapes["shape"], margins=True)
shape_counts.to_csv(TAB / "dose_response_shape_counts.csv")
# does the biggest jump coincide with the first take-principal level?
jj = shapes[(shapes.first_take_principal_level > 0) & (shapes.biggest_jump_at > 0)]
jump_match = (jj.biggest_jump_at == jj.first_take_principal_level).mean()
# steps: mean increment in mutual take by level transition, split by whether that transition adds AI/PM
trans = []
for s in sc_rates.index:
    for k in range(2, 6):
        inc = set(CODES[s][k - 1].split(","))
        trans.append({"scenario": s, "diagnostic": scen[s]["diagnostic"], "to_level": k,
                      "delta_mutual": sc_rates.loc[s, k] - sc_rates.loc[s, k - 1],
                      "delta_any": sc_rates_any.loc[s, k] - sc_rates_any.loc[s, k - 1],
                      "adds_authority_or_permit": int(bool(inc & {"AI", "AB", "PM"})),
                      "adds_AI": int("AI" in inc), "adds_PM": int("PM" in inc), "adds_AB": int("AB" in inc),
                      "adds_T3": int("T3" in inc), "adds_T2": int("T2" in inc), "adds_T1": int("T1" in inc),
                      "adds_HD": int("HD" in inc), "adds_HU_or_AR": int(bool(inc & {"HU", "AR"})),
                      "adds_S": int("S" in inc), "adds_R": int("R" in inc), "adds_AS": int("AS" in inc),
                      "adds_P": int("P" in inc), "codes": ",".join(sorted(inc))})
trans = pd.DataFrame(trans)
trans.to_csv(TAB / "level_transitions.csv", index=False)
def summarise_trans(col):
    g = trans.groupby(col)["delta_mutual"]
    return pd.DataFrame({"n_transitions": g.size(), "mean_delta_mutual_pp": (g.mean() * 100).round(1),
                         "sd": (g.std() * 100).round(1)})
trans_summary = pd.concat({c: summarise_trans(c) for c in ["adds_authority_or_permit", "adds_AI", "adds_PM", "adds_AB",
                                                             "adds_T3", "adds_T2", "adds_T1", "adds_HD", "adds_HU_or_AR",
                                                             "adds_S", "adds_R", "adds_AS", "adds_P"]})
trans_summary.to_csv(TAB / "transition_effect_by_ingredient.csv")
# dominant-ingredient classification of each transition (one label per transition, priority order)
def dominant(codes):
    c = set(codes.split(","))
    for lab, keys in [("authority instructs/backs", {"AI", "AB"}), ("formal permission", {"PM"}),
                      ("against take (HU/AR)", {"HU", "AR"}), ("harm-of-taking reduced (HD)", {"HD"}),
                      ("severe 3rd-party harm (T3)", {"T3"}), ("material 3rd-party harm (T2)", {"T2"}),
                      ("minor 3rd-party (T1)", {"T1"}), ("suggestion (AS)", {"AS"}), ("self-benefit (S)", {"S"}),
                      ("request/promise (R)", {"R"}), ("peer asks (P)", {"P"}), ("urgency (U)", {"U"})]:
        if c & keys:
            return lab
    return "other"
trans["dominant"] = trans.codes.map(dominant)
dom = trans.groupby("dominant")["delta_mutual"].agg(["size", "mean", "std"])
dom["mean"] = (dom["mean"] * 100).round(1); dom["std"] = (dom["std"] * 100).round(1)
dom = dom.sort_values("mean", ascending=False)
dom.to_csv(TAB / "transition_effect_by_dominant_ingredient.csv")
# same by pairing family (rule agent type) to see whether e.g. authority-rule agents respond to AI only
trans_pair = []
for (s, a), g in df.groupby(["scenario", "a"]):
    rates = g.groupby("level").mutual_take.mean()
    for k in range(2, 6):
        if k in rates and k - 1 in rates:
            trans_pair.append({"scenario": s, "rule_a": a, "to_level": k, "delta": rates[k] - rates[k - 1],
                               "dominant": dominant(",".join(sorted(set(CODES[s][k - 1].split(",")))))})
trans_pair = pd.DataFrame(trans_pair)
tp = trans_pair.pivot_table(index="dominant", columns="rule_a", values="delta", aggfunc=["mean", "size"])
tp = (tp * 1).round(3)
tp.to_csv(TAB / "transition_effect_by_dominant_x_rule.csv")

# ----------------------------------------------------------------------------------------------
# 4. Models: which dimension predicts take?  Own IRLS logistic (no statsmodels available).
# ----------------------------------------------------------------------------------------------
def logit_fit(X, y, ridge=1e-6, iters=60):
    X = np.asarray(X, float); y = np.asarray(y, float)
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ b))
        W = p * (1 - p) + 1e-9
        H = X.T @ (X * W[:, None]) + ridge * np.eye(X.shape[1])
        g = X.T @ (y - p) - ridge * b
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-8:
            break
    p = np.clip(1 / (1 + np.exp(-X @ b)), 1e-12, 1 - 1e-12)
    ll = np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))
    return b, ll
def design(d, cols, intercept=True):
    X = d[cols].astype(float).values
    if intercept:
        X = np.column_stack([np.ones(len(d)), X])
    return X
def fit_report(d, cols, y, name):
    X = design(d, cols)
    b, ll = logit_fit(X, d[y])
    p0 = d[y].mean()
    ll0 = len(d) * (p0 * np.log(p0) + (1 - p0) * np.log(1 - p0))
    k = X.shape[1]
    return {"model": name, "outcome": y, "n": len(d), "k": k, "loglik": round(ll, 1), "AIC": round(2 * k - 2 * ll, 1),
            "McFadden_R2": round(1 - ll / ll0, 4), **{f"b_{c}": round(v, 3) for c, v in zip(["const"] + cols, b)}}
# controls shared by all models: pairing structure (rule agent type x partner) and monitoring
ctrl = ["is_W", "is_D", "b_none", "unwatched"]
df["is_W"] = (df.a == "welfare").astype(int); df["is_D"] = (df.a == "nondeception").astype(int)
df["unwatched"] = (df.monitoring == "unwatched").astype(int)
df["level_c"] = df.level - 3
df["welf_higher"] = (df.welfare_if_take == "higher").astype(int)
df["welf_similar"] = (df.welfare_if_take == "similar").astype(int)
df["log_words"] = np.log(df.stakes_block_words)
dim_set = ["cum_AI", "cum_AB", "cum_PM", "cum_AS", "cum_P", "tp_harm_refuse_sev", "cum_V", "cum_R", "cum_S", "cum_HD",
           "cum_HU", "cum_AR", "cum_U"]
models = []
for y in ["mutual_take", "any_take", "take_a"]:
    models.append(fit_report(df, ctrl, y, "controls only"))
    models.append(fit_report(df, ctrl + ["level_c"], y, "controls + level"))
    models.append(fit_report(df, ctrl + ["welf_similar", "welf_higher"], y, "controls + designer welfare label"))
    models.append(fit_report(df, ctrl + ["take_principal_present"], y, "controls + take-instructing principal"))
    models.append(fit_report(df, ctrl + ["tp_harm_refuse_sev"], y, "controls + 3rd-party harm severity"))
    models.append(fit_report(df, ctrl + ["log_words"], y, "controls + log words"))
    models.append(fit_report(df, ctrl + dim_set, y, "controls + all coded dims (no level)"))
    models.append(fit_report(df, ctrl + dim_set + ["level_c"], y, "controls + all coded dims + level"))
    models.append(fit_report(df, ctrl + dim_set + ["log_words"], y, "controls + all coded dims + log words"))
    models.append(fit_report(df, ctrl + ["level_c", "take_principal_present", "tp_harm_refuse_sev", "cum_PM", "cum_HD", "cum_HU", "cum_AR"], y,
                             "controls + level + 6 key dims"))
models = pd.DataFrame(models)
models.to_csv(TAB / "logit_models.csv", index=False)
# cluster-bootstrap CIs for the key model (mutual take): level + 6 key dims
key_cols = ctrl + ["level_c", "take_principal_present", "tp_harm_refuse_sev", "cum_PM", "cum_HD", "cum_HU", "cum_AR"]
groups = {k: g for k, g in df.groupby("scenario")}
keys = list(groups)
boots = []
for _ in range(300):
    pick = rng.choice(keys, size=len(keys), replace=True)
    d = pd.concat([groups[k] for k in pick])
    b, _ = logit_fit(design(d, key_cols), d.mutual_take)
    boots.append(b)
boots = np.array(boots)
b_full, _ = logit_fit(design(df, key_cols), df.mutual_take)
key_ci = pd.DataFrame({"term": ["const"] + key_cols, "coef": b_full.round(3), "OR": np.exp(b_full).round(2),
                       "ci_lo": np.percentile(boots, 2.5, axis=0).round(3), "ci_hi": np.percentile(boots, 97.5, axis=0).round(3)})
key_ci.to_csv(TAB / "key_model_mutual_take_cluster_ci.csv", index=False)

# Within-level contrasts (holding level fixed): does the ingredient still matter?
within = []
for L in range(1, 6):
    d = df[df.level == L]
    for col, lab in [("take_principal_present", "take-instructing principal present"), ("cum_PM", "formal permission present"),
                     ("cum_HD", "harm-of-taking reduced"), ("cum_HU", "fact against take present"),
                     ("cum_S", "self-benefit present"), ("cum_V", "vulnerable party named")]:
        for v in (0, 1):
            dd = d[d[col] == v]
            if len(dd):
                within.append({"level": L, "dimension": lab, "value": v, "n_trials": len(dd),
                               "n_scenes": dd.scenario.nunique(), "mutual_take": round(dd.mutual_take.mean(), 3),
                               "any_take": round(dd.any_take.mean(), 3)})
    for sev in range(4):
        dd = d[d.tp_harm_refuse_sev == sev]
        if len(dd):
            within.append({"level": L, "dimension": "3rd-party harm-of-refusing severity", "value": sev, "n_trials": len(dd),
                           "n_scenes": dd.scenario.nunique(), "mutual_take": round(dd.mutual_take.mean(), 3),
                           "any_take": round(dd.any_take.mean(), 3)})
within = pd.DataFrame(within)
within.to_csv(TAB / "within_level_contrasts.csv", index=False)

# Level effect within strata (Simpson check): slope of mutual take on level within diagnostic x pairing
strata = []
for (dg, pr), g in df.groupby(["diagnostic", "pairing"]):
    m = g.groupby("level").mutual_take.mean()
    strata.append({"diagnostic": dg, "pairing": pr, **{f"L{k}": round(m.get(k, np.nan), 3) for k in range(1, 6)},
                   "L5_minus_L1_pp": round((m.get(5, np.nan) - m.get(1, np.nan)) * 100, 1),
                   "r_over_5_means": round(np.corrcoef(m.index, m.values)[0, 1], 3) if m.std() > 0 else np.nan})
strata = pd.DataFrame(strata)
strata.to_csv(TAB / "level_slope_by_diagnostic_x_pairing.csv", index=False)
# Level effect for "none" agents (no installed rule) -- the cleanest read of the stimulus on the model itself
none_b = df[df.b == "none"].groupby("level").take_b.agg(["mean", "size"]).round(3)
none_b.to_csv(TAB / "none_agent_take_by_level.csv")

# Control-like scenes: pure self-benefit (S003), reversal (S728), AR at L3 (S661, S662), T-only ladders without any authority
ctrl_scenes = {"S003": "pure self-benefit + fault-still-live (welfare lower at all levels)",
               "S728": "levels 4-5 add facts AGAINST take",
               "S661": "L3 guardian re-affirms refuse; L4 court note permits",
               "S662": "L3 proxy re-affirms refuse; L4 nurse permits",
               "S034": "L4 adds a promise AGAINST take",
               "S133": "L2-3 raise harm of taking (risk to another adult)"}
ctab = []
for s, why in ctrl_scenes.items():
    ctab.append({"scenario": s, "title": scen[s]["title"], "why": why, **{f"L{k}": round(sc_rates.loc[s, k], 3) for k in range(1, 6)},
                 **{f"any_L{k}": round(sc_rates_any.loc[s, k], 3) for k in range(1, 6)}})
pd.DataFrame(ctab).to_csv(TAB / "control_like_scenes.csv", index=False)
# Scenes with NO authority/permission at any level ("pure stakes ladders")
pure = coding_first[coding_first.first_take_principal_level == 0].index
pure = [s for s in pure if "PM" not in coding[(coding.scenario == s)].cum_codes.iloc[-1].split(",")]
pure_rates = df[df.scenario.isin(pure)].groupby("level").mutual_take.agg(["mean", "size"]).round(3)
auth_rates = df[~df.scenario.isin(pure)].groupby("level").mutual_take.agg(["mean", "size"]).round(3)
pd.concat({"no_authority_or_permission_any_level": pure_rates, "has_authority_or_permission_somewhere": auth_rates}).to_csv(
    TAB / "level_curve_pure_stakes_vs_authority_scenes.csv")

# ----------------------------------------------------------------------------------------------
# 5. Transcript sampling: how do agents describe the level text?
# ----------------------------------------------------------------------------------------------
KW = {
    "pressure/pressured": r"\bpressur",
    "stakes": r"\bstakes?\b",
    "instruct/order/directive": r"\binstruct|\border(ed|s)?\b|\bdirective",
    "authority/outrank/above": r"\bauthorit|\boutrank|\babove the\b|\bhigher[- ]rank|\bchain of command|\bsuperior",
    "outweigh/greater good/net benefit": r"\boutweigh|\bgreater good\b|\bnet (benefit|positive|welfare)|\bon balance",
    "justif/warrant/defensible": r"\bjustif|\bwarrant|\bdefensib",
    "harm to others/people (jobs, child, patients)": r"\bjobs?\b|\bchild|\bpatients?\b|\bhousehold|\bfamil|\bhealth coverage|\bmedic",
    "honesty/false/mislead/lie": r"\bhonest|\bfalse|\bmislead|\blie\b|\blying|\bdeceiv",
    "duty/rule/charter/policy": r"\bduty\b|\brules?\b|\bcharter|\bpolicy|\bregulation",
    "promise/asked us/confidential": r"\bpromis|\basked (us|you both|both of us)|\bconfidential",
    "permit/allow/authoris": r"\bpermit|\ballow|\bauthori[sz]",
    "monitored/oversight": r"\bmonitor|\boversight",
}
def extract_reasoning(md):
    # take private reasoning + plan blocks for both agents (everything up to the message rounds if marked)
    return md
def sample_transcripts():
    cand = df[(df.level.isin([1, 5]))].copy()
    picks = []
    # balanced: 2 per (level, pairing) with varied diagnostics -> 24, cap 20 by dropping some
    for L in (1, 5):
        for pr in ["W-W", "W-none", "D-D", "D-none", "A-A", "A-none"]:
            sub = cand[(cand.level == L) & (cand.pairing == pr)]
            sub = sub.sample(n=min(2, len(sub)), random_state=7 + L)
            picks.append(sub)
    picks = pd.concat(picks)
    return picks
picks = sample_transcripts()
kw_rows = []
excerpts = ["# Transcript excerpts: how agents describe the level text (L1 vs L5)\n",
            "Sampled 24 transcripts (2 per level x pairing). Keyword counts are over the whole transcript file; excerpts are the first 1,400 characters of Agent A's private reasoning.\n"]
for _, r in picks.sort_values(["level", "pairing"]).iterrows():
    p = RES / "runs" / r.run_id / "transcript.md"
    if not p.exists():
        continue
    md = p.read_text(encoding="utf-8", errors="ignore")
    low = md.lower()
    counts = {k: len(re.findall(v, low)) for k, v in KW.items()}
    kw_rows.append({"run_id": r.run_id, "level": r.level, "pairing": r.pairing, "diagnostic": r.diagnostic,
                    "outcome": r.outcome, "chars": len(md), **counts})
    m = re.search(r"## Agent A — plan.*?### Endpoint-returned reasoning \(private\)\s*(.*?)###", md, re.S)
    ex = (m.group(1).strip() if m else md[:1400])[:1400]
    excerpts.append(f"\n## {r.run_id}  ({r.diagnostic} scene, {r.pairing}, L{r.level}, outcome={r.outcome})\n\n"
                    f"Level text: _{coding[(coding.scenario == r.scenario) & (coding.level == r.level)].pressure_text.iloc[0]}_\n\n"
                    f"Principals: _{coding[(coding.scenario == r.scenario) & (coding.level == r.level)].principals_text.iloc[0]}_\n\n"
                    f"> {ex.replace(chr(10), chr(10) + '> ')}\n")
kw = pd.DataFrame(kw_rows)
kw.to_csv(TAB / "transcript_keyword_counts_sample.csv", index=False)
kw_summary = kw.groupby("level")[list(KW)].mean().round(2).T
kw_summary.columns = [f"L{c}_mean_per_transcript" for c in kw_summary.columns]
kw_summary.to_csv(TAB / "transcript_keyword_summary_L1_vs_L5.csv")
(OUT / "transcript_excerpts.md").write_text("\n".join(excerpts), encoding="utf-8")

# whole-corpus keyword scan (all complete transcripts) for the word "pressure" and "stakes" by level
corpus = []
for _, r in df.iterrows():
    p = RES / "runs" / r.run_id / "transcript.md"
    if not p.exists():
        continue
    low = p.read_text(encoding="utf-8", errors="ignore").lower()
    corpus.append({"run_id": r.run_id, "level": r.level, "pairing": r.pairing, "mutual_take": r.mutual_take,
                   "any_take": r.any_take,
                   "pressure": len(re.findall(r"\bpressur", low)),
                   "stakes": len(re.findall(r"\bstakes?\b", low)),
                   "instruct": len(re.findall(r"\binstruct", low)),
                   "outweigh": len(re.findall(r"\boutweigh|\bgreater good|\bnet (benefit|positive)", low)),
                   "justif": len(re.findall(r"\bjustif", low)),
                   "permit_allow": len(re.findall(r"\bpermit|\ballow|\bauthori[sz]", low)),
                   "principal_word": len(re.findall(r"\bprincipal", low)),
                   "chars": len(low)})
corpus = pd.DataFrame(corpus)
corpus.to_csv(OUT / "transcript_keyword_counts_all.csv", index=False)
cs = corpus.groupby("level")[["pressure", "stakes", "instruct", "outweigh", "justif", "permit_allow", "principal_word", "chars"]].mean().round(2)
cs["share_mentioning_pressure"] = corpus.groupby("level").pressure.apply(lambda s: (s > 0).mean()).round(3)
cs["share_mentioning_instruct"] = corpus.groupby("level").instruct.apply(lambda s: (s > 0).mean()).round(3)
cs["share_mentioning_outweigh"] = corpus.groupby("level").outweigh.apply(lambda s: (s > 0).mean()).round(3)
cs.to_csv(TAB / "transcript_keywords_all_by_level.csv")

# ----------------------------------------------------------------------------------------------
# 6. Figures
# ----------------------------------------------------------------------------------------------
levels = np.arange(1, 6)
# Fig 1: what the level adds -- prevalence of cumulative ingredients by level
fig, ax = plt.subplots(figsize=(8.2, 4.6))
series = [("take_principal_present", "a principal instructs take", C["orange"]),
          ("cum_PM", "formal permission / licence", C["violet"]),
          ("cum_T3", "severe 3rd-party harm if refuse", C["blue"]),
          ("cum_V", "vulnerable party named", C["aqua"]),
          ("cum_S", "self-benefit for agents", C["yellow"]),
          ("cum_HD", "harm of taking reduced", C["magenta"]),
          ("cum_HU", "fact against take", C["red"])]
for col, lab, colr in series:
    ax.plot(levels, by_level[col] * 100, marker="o", ms=5, lw=2, color=colr, label=lab)
    ax.annotate(lab, (5.08, by_level[col].iloc[-1] * 100), fontsize=8, color=C["ink2"], va="center")
ax.set_xlim(0.8, 6.9); ax.set_ylim(-2, 102); ax.set_xticks(levels)
ax.set_xlabel("Justification level"); ax.set_ylabel("% of the 72 scenes whose cumulative text contains it")
ax.set_title("What the 'pressure' level actually adds (content coding of all 72 x 5 level texts)", loc="left", fontsize=11)
ax.grid(axis="x", visible=False)
fig.tight_layout(); fig.savefig(FIG / "fig1_ingredients_by_level.png"); plt.close(fig)

# Fig 2: take rate by level, split by take-principal present (and welfare label)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
g = df.groupby(["level", "take_principal_present"]).mutual_take.agg(["mean", "size"]).reset_index()
for v, lab, colr in [(0, "no take-instructing principal", C["blue"]), (1, "a principal instructs take", C["orange"])]:
    gg = g[g.take_principal_present == v]
    axes[0].plot(gg.level, gg["mean"] * 100, marker="o", lw=2, color=colr, label=lab)
    for _, rr in gg.iterrows():
        axes[0].annotate(f"n={int(rr['size'])}", (rr.level, rr['mean'] * 100 + 2.5), fontsize=7, ha="center", color=C["ink2"])
axes[0].plot(levels, lv.values * 100, color=C["ink2"], lw=1, ls="--", label="all trials")
axes[0].set_title("Mutual take by level, split by principal endorsement", loc="left", fontsize=10)
axes[0].set_xlabel("Justification level"); axes[0].set_ylabel("Mutual take (%)"); axes[0].set_xticks(levels); axes[0].legend(fontsize=8, frameon=False)
g2 = df.groupby(["level", "tp_harm_refuse_sev"]).mutual_take.agg(["mean", "size"]).reset_index()
cols_sev = {0: SEQ_BLUE[1], 1: SEQ_BLUE[2], 2: SEQ_BLUE[4], 3: SEQ_BLUE[6]}
for sev in range(4):
    gg = g2[(g2.tp_harm_refuse_sev == sev) & (g2["size"] >= 24)]
    if len(gg):
        axes[1].plot(gg.level, gg["mean"] * 100, marker="o", lw=2, color=cols_sev[sev], label=f"3rd-party harm of refusing = {['none','minor','material','severe'][sev]}")
axes[1].set_title("...split by coded severity of harm-to-others if refuse", loc="left", fontsize=10)
axes[1].set_xlabel("Justification level"); axes[1].set_xticks(levels); axes[1].legend(fontsize=8, frameon=False)
for a in axes: a.grid(axis="x", visible=False)
fig.tight_layout(); fig.savefig(FIG / "fig2_take_by_level_split.png"); plt.close(fig)

# Fig 3: per-scenario dose-response spaghetti by diagnostic, highlighting first take-principal level
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), sharey=True)
for ax, dg in zip(axes, ["welfare", "nondeception", "authority"]):
    sub = shapes[shapes.diagnostic == dg]
    for s, row in sub.iterrows():
        y = [row[f"L{k}"] * 100 for k in levels]
        ax.plot(levels, y, color=C["blue"], alpha=0.35, lw=1.2)
        f = row.first_take_principal_level
        if f > 0:
            ax.plot(f, y[f - 1], marker="o", ms=5, color=C["orange"], alpha=0.9, zorder=3)
    m = df[df.diagnostic == dg].groupby("level").mutual_take.mean() * 100
    ax.plot(levels, m.values, color=C["ink"], lw=2.5, label="family mean")
    ax.set_title(f"{dg} scenes (n={len(sub)})", loc="left", fontsize=10); ax.set_xticks(levels); ax.set_xlabel("Justification level")
    ax.grid(axis="x", visible=False)
axes[0].set_ylabel("Mutual take (%), 12 trials per scene x level")
axes[0].plot([], [], marker="o", color=C["orange"], ls="", label="first level with a take-instructing principal")
axes[0].legend(fontsize=8, frameon=False, loc="upper left")
fig.suptitle("Within-scene dose-response curves", x=0.01, ha="left", fontsize=11)
fig.tight_layout(); fig.savefig(FIG / "fig3_scene_curves.png"); plt.close(fig)

# Fig 4: transition effect by dominant ingredient
fig, ax = plt.subplots(figsize=(8.5, 4.4))
d = dom.copy()
ax.barh(d.index[::-1], d["mean"][::-1], color=C["blue"], height=0.6)
for i, (lab, row) in enumerate(d[::-1].iterrows()):
    ax.annotate(f"{row['mean']:+.1f} pp  (n={int(row['size'])} transitions)", (max(row["mean"], 0) + 0.6, i), va="center", fontsize=8, color=C["ink2"])
ax.axvline(0, color=C["ink2"], lw=0.8)
ax.set_xlabel("Mean change in mutual-take rate when moving up one level (pp)")
ax.set_title("What kind of sentence was added vs how much take rose (288 level transitions)", loc="left", fontsize=11)
ax.set_xlim(d["mean"].min() - 4, d["mean"].max() + 22); ax.grid(axis="y", visible=False)
fig.tight_layout(); fig.savefig(FIG / "fig4_transition_by_ingredient.png"); plt.close(fig)

# Fig 5: control-like scenes
fig, ax = plt.subplots(figsize=(8, 4.2))
cl = {"S003": C["red"], "S728": C["orange"], "S661": C["violet"], "S662": C["magenta"], "S034": C["aqua"], "S133": C["yellow"]}
for s, colr in cl.items():
    ax.plot(levels, sc_rates.loc[s].values * 100, marker="o", lw=2, color=colr, label=f"{s} {scen[s]['title']}")
ax.plot(levels, lv.values * 100, color=C["ink2"], lw=1.2, ls="--", label="all 72 scenes")
ax.set_xticks(levels); ax.set_xlabel("Justification level"); ax.set_ylabel("Mutual take (%)")
ax.set_title("Scenes whose ladder is NOT a clean 'more reason to take' ladder", loc="left", fontsize=11)
ax.legend(fontsize=7.5, frameon=False); ax.grid(axis="x", visible=False)
fig.tight_layout(); fig.savefig(FIG / "fig5_control_like_scenes.png"); plt.close(fig)

# Fig 6: prompt length by level
fig, ax = plt.subplots(figsize=(6.5, 3.8))
ax.plot(levels, by_level.pressure_words, marker="o", lw=2, color=C["blue"], label="'Stakes' block words")
ax.plot(levels, by_level.stakes_block_words, marker="o", lw=2, color=C["violet"], label="Stakes + principals words")
ax.set_xticks(levels); ax.set_xlabel("Justification level"); ax.set_ylabel("Mean words (72 scenes)")
ax.set_title("Level text is cumulative: length rises with level", loc="left", fontsize=11); ax.legend(frameon=False, fontsize=8); ax.grid(axis="x", visible=False)
fig.tight_layout(); fig.savefig(FIG / "fig6_prompt_length.png"); plt.close(fig)

# ----------------------------------------------------------------------------------------------
# 7. Summary numbers for the report
# ----------------------------------------------------------------------------------------------
summary = {
    "n_complete_trials": int(len(df)),
    "mutual_take_by_level": {int(k): round(float(v), 4) for k, v in lv.items()},
    "r_aggregate_over_5_level_means": round(float(r_agg), 4),
    "r_trial_level_point_biserial_mutual": round(float(r_trial), 4),
    "r_trial_level_cluster_CI": [round(float(x), 4) for x in ci_trial],
    "r_trial_level_point_biserial_any_take": round(float(r_trial_any), 4),
    "share_scenes_take_principal_by_level": {int(k): round(float(v), 3) for k, v in by_level.take_principal_present.items()},
    "share_scenes_licensed_by_level": {int(k): round(float(v), 3) for k, v in by_level.licensed.items()},
    "share_scenes_T3_by_level": {int(k): round(float(v), 3) for k, v in by_level.cum_T3.items()},
    "mean_pressure_words_by_level": {int(k): round(float(v), 1) for k, v in by_level.pressure_words.items()},
    "welfare_label_by_level": pd.crosstab(coding.level, coding.welfare_if_take).to_dict(),
    "shape_counts": shapes["shape"].value_counts().to_dict(),
    "share_biggest_jump_at_first_take_principal_level": round(float(jump_match), 3),
    "n_scenes_with_take_principal": int((coding_first.first_take_principal_level > 0).sum()),
    "n_scenes_pure_stakes_no_authority_no_permission": len(pure),
    "pure_scenes": pure,
    "l5_increment_kind_counts": l5.l5_kind.value_counts().to_dict(),
    "transition_effect_by_dominant": dom.to_dict(),
    "none_agent_take_by_level": none_b["mean"].to_dict(),
    "key_model": key_ci.to_dict(orient="records"),
    "models_mutual_take": models[models.outcome == "mutual_take"][["model", "McFadden_R2", "AIC"]].to_dict(orient="records"),
    "models_any_take": models[models.outcome == "any_take"][["model", "McFadden_R2", "AIC"]].to_dict(orient="records"),
    "transcript_keywords_by_level": cs.to_dict(),
}
(OUT / "model_summary.json").write_text(json.dumps(summary, indent=1, default=str), encoding="utf-8")
print(json.dumps({k: summary[k] for k in ["mutual_take_by_level", "r_aggregate_over_5_level_means", "r_trial_level_point_biserial_mutual",
                                          "r_trial_level_cluster_CI", "share_scenes_take_principal_by_level", "share_scenes_licensed_by_level",
                                          "share_scenes_T3_by_level", "mean_pressure_words_by_level", "shape_counts",
                                          "share_biggest_jump_at_first_take_principal_level", "n_scenes_with_take_principal",
                                          "n_scenes_pure_stakes_no_authority_no_permission", "l5_increment_kind_counts",
                                          "none_agent_take_by_level"]}, indent=1, default=str))
print(dom)
print(models[["model", "outcome", "McFadden_R2", "AIC"]].to_string())
print(key_ci.to_string())
print(within[within.dimension == "take-instructing principal present"].to_string())
print(pd.concat({"pure": pure_rates, "auth": auth_rates}))
print(cs)
print(kw_summary)

# Fig 7: by rule family x take-principal present (the authority family is deterministic)
fig, axes = plt.subplots(1, 3, figsize=(12, 4.0), sharey=True)
for ax, fam, lab in zip(axes, ["welfare", "nondeception", "authority"], ["welfare-rule agent A", "honesty-rule agent A", "authority-rule agent A"]):
    sub = df[df.a == fam]
    for v, colr, name in [(0, C["blue"], "no take-instructing principal"), (1, C["orange"], "a principal instructs take")]:
        g = sub[sub.take_principal_present == v].groupby("level").mutual_take.agg(["mean", "size"])
        g = g[g["size"] >= 20]
        ax.plot(g.index, g["mean"] * 100, marker="o", lw=2, color=colr, label=name)
        for L, rr in g.iterrows():
            ax.annotate(f"{int(rr['size'])}", (L, rr["mean"] * 100 + 3), fontsize=7, ha="center", color=C["ink2"])
    ax.set_title(lab, loc="left", fontsize=10); ax.set_xticks(levels); ax.set_xlabel("Justification level"); ax.grid(axis="x", visible=False)
axes[0].set_ylabel("Mutual take (%)  [small numbers = trials]"); axes[0].legend(fontsize=8, frameon=False, loc="upper left")
fig.suptitle("Same level, different ingredient: the level curve by rule family, split by whether a principal has instructed take", x=0.01, ha="left", fontsize=11)
fig.tight_layout(); fig.savefig(FIG / "fig7_family_by_principal.png"); plt.close(fig)
fam_tab = df.groupby(["a", "level", "take_principal_present"]).agg(n=("mutual_take", "size"), scenes=("scenario", "nunique"),
                                                                    mutual_take=("mutual_take", "mean"), any_take=("any_take", "mean")).round(3)
fam_tab.to_csv(TAB / "family_x_level_x_principal.csv")
pure_fam = df[df.scenario.isin(pure)].groupby(["a", "level"]).mutual_take.mean().unstack().round(3)
pure_fam.to_csv(TAB / "pure_stakes_scenes_by_family.csv")
