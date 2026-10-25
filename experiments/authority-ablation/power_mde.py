"""Minimum detectable paired differences for the authority-ablation design (no API calls).

Run: python tools/run_reserved.py experiments/authority-ablation/power_mde.py
Reads analysis_pairs.csv (from validate_ablation_pack.py); writes power_mde.csv.

Paired binary outcome (mutual take, INS vs NOI in the same scene x level x pairing). For n pairs and a
total discordance rate psi, the McNemar normal approximation gives the smallest detectable difference d
(two-sided alpha = .05, power = .80) as the root of
    sqrt(n) * |d| = z_a * sqrt(psi) + z_b * sqrt(psi - d^2).
Clustering by scene is handled with a design effect DE = 1 + (m - 1) * icc, where m is the mean number of
unique pairs per scene in the subset and icc = 0.135 is the within-scene ICC of the paired L5-L4 difference in
the frozen study's 36 level-5-instruction scenes (281 pairs; computed when this design was written).
"""
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
Z_A, Z_B, ICC = 1.959964, 0.841621, 0.135


def mde(n_eff: float, psi: float) -> float:
    lo, hi = 1e-6, min(psi, 1.0) ** 0.5 - 1e-9
    f = lambda d: math.sqrt(n_eff) * d - (Z_A * math.sqrt(psi) + Z_B * math.sqrt(max(psi - d * d, 0)))
    if f(hi) < 0:
        return float("nan")  # not detectable at this discordance
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return hi


def main():
    rows = [r for r in csv.DictReader((HERE / "analysis_pairs.csv").open(encoding="utf-8")) if r["unique_pair"] == "True"]
    subsets = {
        "Pooled (primary)": rows,
        "A-A + A-none": [r for r in rows if r["pairing"].startswith("A")],
        "A-A": [r for r in rows if r["pairing"] == "A-A"],
        "A-none": [r for r in rows if r["pairing"] == "A-none"],
        "W-W": [r for r in rows if r["pairing"] == "W-W"],
        "D-D": [r for r in rows if r["pairing"] == "D-D"],
        "A pairs, stakes rung 1": [r for r in rows if r["pairing"].startswith("A") and r["stakes_rung"] == "1"],
        "Pooled, stakes rung 1": [r for r in rows if r["stakes_rung"] == "1"],
        "Pooled, pairs below first-instruction level (added cells)": [r for r in rows if r["original_state"] == "NOI"],
    }
    out = []
    for name, sub in subsets.items():
        per_scene = Counter(r["source_scenario"] for r in sub)
        m = len(sub) / len(per_scene)
        de = 1 + (m - 1) * ICC
        for psi in (0.10, 0.20, 0.40, 0.60):
            out.append({"subset": name, "unique_pairs": len(sub), "scenes": len(per_scene),
                        "pairs_per_scene": round(m, 1), "design_effect": round(de, 2),
                        "effective_pairs": round(len(sub) / de, 1), "discordance": psi,
                        "mde_pp_unclustered": round(100 * mde(len(sub), psi), 1),
                        "mde_pp_clustered": round(100 * mde(len(sub) / de, psi), 1)})
    # FRZ bridge (frozen vs de-duplicated original-state cell), discordance 0.10
    bridge = [r for r in csv.DictReader((HERE / "analysis_pairs.csv").open(encoding="utf-8"))
              if r["frz_run_id"] and r["level"] != "1"]
    pairs = {(r["frz_run_id"], r["ins_run_id"] if r["original_state"] == "INS" else r["noi_run_id"]) for r in bridge}
    per_scene = Counter(p[0].split("-")[0] for p in pairs)
    m = len(pairs) / len(per_scene)
    de = 1 + (m - 1) * ICC
    for psi in (0.05, 0.10, 0.20):
        out.append({"subset": "FRZ bridge (frozen vs de-duplicated), L2-L5", "unique_pairs": len(pairs),
                    "scenes": len(per_scene), "pairs_per_scene": round(m, 1), "design_effect": round(de, 2),
                    "effective_pairs": round(len(pairs) / de, 1), "discordance": psi,
                    "mde_pp_unclustered": round(100 * mde(len(pairs), psi), 1),
                    "mde_pp_clustered": round(100 * mde(len(pairs) / de, psi), 1)})
    with (HERE / "power_mde.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    for r in out:
        print(r)


if __name__ == "__main__":
    main()
