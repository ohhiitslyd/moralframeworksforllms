"""Step 1.5: heat maps of derived / engineered metrics from the Step 1 table.

Usage (from the repo root, CPUs 0-3 kept free; pass all three paths explicitly):
    python tools/run_reserved.py prompt-library/analysis/tools/step1.5_derived_heatmaps.py \
        --table <trial_metrics.csv> --schema <metrics_schema.json> --out <dir>

Reference implementation from the 2026-10-25 pressure study: factor names (level,
monitoring, pairing, diagnostic, setting_id, criterion_a/b) follow that run's Step 1 table.

Columns come from the schema: role == outcome in the agent or pair sections, of type binary
(shown as rates on an absolute 0-100% scale) or numeric/ordinal (shown as medians, colour
normalised per column). Per-agent columns (_a/_b) are pooled into one agent-level metric;
the agent's own criterion is a factor. Heuristic columns flagged unreliable in the schema
are marked with a warning sign; unvalidated heuristics with "(unvalidated)".
"""
import argparse
import csv
import itertools
import statistics
from collections import defaultdict
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ap = argparse.ArgumentParser()
ap.add_argument("--table", type=Path, default=HERE.parent / "step1" / "trial_metrics.csv")
ap.add_argument("--schema", type=Path, default=HERE.parent / "step1" / "metrics_schema.json")
ap.add_argument("--out", type=Path, default=HERE)
args = ap.parse_args()
FIG, TAB = args.out / "figures", args.out / "tables"
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

schema = json.loads(args.schema.read_text(encoding="utf-8"))
cols = {c["name"]: c for c in schema["columns"]}
rows = [r for r in csv.DictReader(open(args.table, encoding="utf-8")) if r.get("status") == "complete"]
# Factor columns may be named differently between table versions; normalise to short keys.
ALIASES = {"diagnostic": ["diagnostic", "scenario_diagnostic", "scenario_family"], "setting_id": ["setting_id", "setting"],
           "monitoring": ["monitoring"], "level": ["level"], "pairing": ["pairing"]}
for r in rows:
    for k, names in ALIASES.items():
        if k not in r or r[k] == "":
            r[k] = next((r[n] for n in names if r.get(n, "") != ""), "")


def flag(c):
    if not c.get("heuristic"):
        return ""
    v = c.get("validation") or {}
    if v.get("reliable") is False:
        return " ⚠ unreliable"
    if not v:
        return " (unvalidated)"
    return ""


def label(c):
    return (c.get("label") or c["name"]).replace("_", " ") + flag(c)


# --- metric selection
pair_metrics, agent_metrics = [], []
for name, c in cols.items():
    if c.get("role") != "outcome" or c.get("type") not in ("binary", "numeric", "ordinal"):
        continue
    if c.get("section") == "pair":
        pair_metrics.append(name)
    elif c.get("section") == "agent" and name.endswith("_a") and name[:-2] + "_b" in cols:
        agent_metrics.append(name[:-2])


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# --- long-format agent rows
agent_rows = []
for r in rows:
    for s in ("a", "b"):
        d = {"_crit": r.get(f"criterion_{s}", ""), **{k: r.get(k, "") for k in ("level", "monitoring", "pairing", "diagnostic", "setting_id")}}
        for m in agent_metrics:
            d[m] = r.get(f"{m}_{s}", "")
        agent_rows.append(d)

CRIT = {"welfare": "Welfare", "nondeception": "Non-deception", "authority": "Authority", "none": "No rule"}
FACTORS = {"level": ("Pressure level", lambda v: f"Level {v}"),
           "monitoring": ("Monitoring notice", str.capitalize),
           "pairing": ("Pairing", str),
           "diagnostic": ("Scenario family", lambda v: CRIT.get(v, v)),
           "setting_id": ("Social setting", lambda v: v.replace("_", " ").capitalize())}


def metric_kind(name, base_cols):
    c = base_cols[name]
    return "rate" if c["type"] == "binary" else "median"


def summarise(data, key_fn, metric):
    groups = defaultdict(list)
    for d in data:
        v = num(d.get(metric))
        if v is not None:
            groups[key_fn(d)].append(v)
    return groups


def value(vals, kind):
    if not vals:
        return np.nan
    return sum(vals) / len(vals) if kind == "rate" else statistics.median(vals)


def cell_fonts(n_rows, n_cols, row_h, col_w):
    """Annotation font sizes scaled to the cell size; never below 10 pt for values."""
    fs = max(10.0, min(16.0, 0.36 * 72 * min(row_h, col_w / 1.8)))
    return fs, max(8.0, 0.68 * fs)


def draw(mat, nmat, rlabels, clabels, kinds, title, subtitle, xlabel, ylabel, fname):
    disp = mat.copy()
    for j, k in enumerate(kinds):  # rates absolute; medians normalised per column
        if k == "median":
            col = mat[:, j]
            lo, hi = np.nanmin(col) if np.isfinite(col).any() else 0, np.nanmax(col) if np.isfinite(col).any() else 1
            disp[:, j] = (col - lo) / (hi - lo) if hi > lo else 0.5
    row_h = 0.8 if len(rlabels) <= 20 else 0.5
    col_w = 1.6
    fs, fs_n = cell_fonts(len(rlabels), len(clabels), row_h, col_w)
    h = max(3.6, row_h * len(rlabels) + 2.8)
    w = max(8, col_w * len(clabels) + 4.0)
    fig, ax = plt.subplots(figsize=(w, h))
    im = ax.imshow(np.ma.masked_invalid(disp), cmap="Blues", vmin=0, vmax=1, aspect="auto")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            if np.isnan(v):
                ax.text(j, i, "—", ha="center", va="center", fontsize=fs, color="#888")
                continue
            txt = f"{v:.0%}" if kinds[j] == "rate" else (f"{v:.0f}" if abs(v) >= 10 else f"{v:.2g}")
            col = "white" if disp[i, j] > 0.55 else "#1f2328"
            ax.text(j, i - 0.13, txt, ha="center", va="center", fontsize=fs, fontweight="bold", color=col)
            ax.text(j, i + 0.27, f"n={int(nmat[i, j])}", ha="center", va="center", fontsize=fs_n, color=col)
    ax.set_xticks(range(len(clabels)), clabels, rotation=35, ha="right", fontsize=10)
    ax.set_yticks(range(len(rlabels)), rlabels, fontsize=10)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.suptitle(title, fontsize=14, fontweight="bold", x=0.01, ha="left")
    ax.set_title(subtitle, fontsize=10, loc="left", color="#59636e")
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label("Rate 0–100% (medians: shaded per column)", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / fname, dpi=140)
    plt.close(fig)


def levels_of(data, key):
    vals = sorted({d[key] for d in data if d.get(key, "") != ""}, key=lambda v: (len(v), v))
    return vals


figs = []
CHUNK = 10
sets = [("pair", rows, pair_metrics, {k: k for k in FACTORS}),
        ("agent", agent_rows, agent_metrics, {**{k: k for k in FACTORS}, "criterion": "_crit"})]
for unit, data, metrics, fmap in sets:
    if not metrics:
        continue
    base_cols = {m: cols[m if unit == "pair" else m + "_a"] for m in metrics}
    rate_m = [m for m in metrics if metric_kind(m, base_cols) == "rate"]
    med_m = [m for m in metrics if metric_kind(m, base_cols) == "median"]
    for fkey, dkey in fmap.items():
        fname_, flab = FACTORS.get(fkey, ("Agent's own criterion", lambda v: CRIT.get(v, v)))
        lv = levels_of(data, dkey)
        if not lv:
            continue
        for group, ms in (("rates", rate_m), ("medians", med_m)):
            for ci in range(0, len(ms), CHUNK):
                chunk = ms[ci:ci + CHUNK]
                kinds = ["rate" if group == "rates" else "median"] * len(chunk)
                mat = np.full((len(lv), len(chunk)), np.nan)
                nmat = np.zeros_like(mat)
                with open(TAB / f"1v_{unit}_{fkey}_{group}_{ci // CHUNK + 1}.csv", "w", newline="", encoding="utf-8") as fh:
                    w = csv.writer(fh)
                    w.writerow([fkey, "metric", "value", "n"])
                    for j, m in enumerate(chunk):
                        g = summarise(data, lambda d: d[dkey], m)
                        for i, v in enumerate(lv):
                            mat[i, j], nmat[i, j] = value(g.get(v, []), kinds[j]), len(g.get(v, []))
                            w.writerow([v, m, "" if np.isnan(mat[i, j]) else f"{mat[i, j]:.4f}", int(nmat[i, j])])
                fname = f"1v_{unit}_{fkey}_{group}_{ci // CHUNK + 1}.png"
                draw(mat, nmat, [flab(v) for v in lv], [label(base_cols[m]) for m in chunk], kinds,
                     f"{'Pair' if unit == 'pair' else 'Agent'}-level derived metrics ({group}) by {fname_.lower()}",
                     f"Complete trials (n = {len(rows)} episodes{'; agents pooled, 2 per episode' if unit == 'agent' else ''}). ⚠ = heuristic flagged unreliable in validation.",
                     "Derived metric", fname_, fname)
                figs.append((unit, fkey, group, fname))

# --- two-variable views for the binary derived metrics that vary most across pressure level
def spread(data, m, key="level"):
    g = summarise(data, lambda d: d[key], m)
    vals = [sum(v) / len(v) for v in g.values() if v]
    return (max(vals) - min(vals)) if len(vals) > 1 else 0


two = []
for unit, data, metrics, _ in sets:
    base = {m: cols[m if unit == "pair" else m + "_a"] for m in metrics}
    cands = [m for m in metrics if base[m]["type"] == "binary"]
    cands.sort(key=lambda m: -spread(data, m))
    for m in cands[:4]:
        for f1, f2 in (("level", "monitoring"), ("pairing", "monitoring"), ("diagnostic", "monitoring"), ("level", "pairing")):
            l1, l2 = levels_of(data, f1), levels_of(data, f2)
            if not l1 or not l2:
                continue
            g = summarise(data, lambda d: (d[f1], d[f2]), m)
            mat = np.array([[value(g.get((a, b), []), "rate") for b in l2] for a in l1])
            nmat = np.array([[len(g.get((a, b), [])) for b in l2] for a in l1])
            fname = f"2v_{unit}_{m}__{f1}_x_{f2}.png"
            draw(mat, nmat, [FACTORS[f1][1](v) for v in l1], [FACTORS[f2][1](v) for v in l2], ["rate"] * len(l2),
                 f"{label(base[m])}: {FACTORS[f1][0].lower()} × {FACTORS[f2][0].lower()}",
                 f"{'Pair' if unit == 'pair' else 'Agent'}-level rate among complete trials; absolute colour scale.",
                 FACTORS[f2][0], FACTORS[f1][0], fname)
            two.append((unit, m, f1, f2, fname))

lines = ["# Step 1.5: derived-metric heat maps", "",
         f"Source: `{args.table.name}` ({len(rows)} complete episodes) with its schema. **Derived / engineered outcomes only** (raw outcome rates are in Step 0.5). Rates use an absolute 0–100% scale; medians are shaded within their column with the value printed. **⚠ marks heuristics that failed validation**; treat them as exploratory only.", "",
         f"Pair-level metrics: {len(pair_metrics)}; agent-level metrics (pooled over agents A and B): {len(agent_metrics)}.", "",
         "Regenerate: `python tools/run_reserved.py prompt-library/analysis/tools/step1.5_derived_heatmaps.py --table <csv> --schema <json> --out <dir>` (CPUs 0–3 kept free).", "",
         "## One factor × derived metrics", ""]
for unit, fkey, group, f in figs:
    lines.append(f"- [{unit} · {fkey} · {group}](figures/{f})")
lines += ["", "## Two factors × derived metric (top binary metrics by spread across level)", ""]
for unit, m, f1, f2, f in two:
    lines.append(f"- [{unit} · {m} · {f1} × {f2}](figures/{f})")
lines += ["", "Highlights:", ""]
for unit, fkey, group, f in figs:
    if fkey in ("monitoring", "level") and group == "rates" and f.endswith("_1.png"):
        lines.append(f"![{f}](figures/{f})\n")
lines += ["Tables behind every chart are in `tables/`."]
(args.out / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{len(figs)} one-factor and {len(two)} two-factor figures; pair metrics {len(pair_metrics)}, agent metrics {len(agent_metrics)}")
