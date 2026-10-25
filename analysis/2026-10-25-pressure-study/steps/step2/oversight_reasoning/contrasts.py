"""Outcome-held-fixed contrasts: is oversight-linked text more common in the notice-dependent runs?

(1) Among UNWATCHED runs that ended in mutual take: share with >=1 agent showing measure (a),
    when the watched twin did NOT reach mutual take (unwatched-only cells) vs did (both-take cells).
(2) Among WATCHED runs that did NOT reach mutual take: share with >=1 agent showing (b),
    when the unwatched twin DID take (unwatched-only cells) vs did not (neither cells).
Same for plan-stage-only text (exchange 0, before any peer message). Fisher exact p (two-sided).
Writes tables/outcome_held_contrasts.csv. Launch via tools/run_reserved.py.
"""
import csv
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parents[4] / "results" / "2026-10-25-pressure-study"


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0, c - h), min(1, c + h)


def fisher(a, b, c, d):
    """two-sided Fisher exact for [[a,b],[c,d]]"""
    n = a + b + c + d; r1 = a + b; c1 = a + c
    def lp(x):
        return (math.lgamma(r1 + 1) + math.lgamma(n - r1 + 1) + math.lgamma(c1 + 1) + math.lgamma(n - c1 + 1)
                - math.lgamma(x + 1) - math.lgamma(r1 - x + 1) - math.lgamma(c1 - x + 1) - math.lgamma(n - r1 - c1 + x + 1)
                - math.lgamma(n + 1))
    p0 = lp(a)
    lo, hi = max(0, r1 + c1 - n), min(r1, c1)
    return min(1.0, sum(math.exp(lp(x)) for x in range(lo, hi + 1) if lp(x) <= p0 + 1e-9))


runs = {r["run_id"]: r for r in csv.DictReader(open(RES / "runs.csv", encoding="utf-8")) if r["status"] == "complete"}
am = defaultdict(dict)
for r in csv.DictReader(open(HERE / "agent_measures.csv", encoding="utf-8")):
    am[r["run_id"]][r["agent"]] = r
cells = defaultdict(dict)
for rid, r in runs.items():
    cells[(r["scenario"], r["level"], r["pairing"])][r["monitoring"]] = rid
cells = {k: v for k, v in cells.items() if len(v) == 2}


def has(rid, m, scope):
    cols = {"any": [f"{m}_private", f"{m}_public"], "plan": [f"{m}_planstage"], "public": [f"{m}_public"]}[scope]
    return any(int(am[rid].get(ag, {}).get(c, 0) or 0) > 0 for ag in "AB" for c in cols)


rows = []
for scope in ("any", "plan", "public"):
    for m, arm, cond_fixed, grp_a, grp_b in (
            ("a", "unwatched", "unwatched run = mutual take", "unwatched_only_take", "both_take"),
            ("e", "unwatched", "unwatched run = mutual take", "unwatched_only_take", "both_take"),
            ("b", "watched", "watched run != mutual take", "unwatched_only_take", "neither_take"),
            ("c_high", "watched", "watched run != mutual take", "unwatched_only_take", "neither_take")):
        cnt = {grp_a: [0, 0], grp_b: [0, 0]}
        for k, v in cells.items():
            mw = runs[v["watched"]]["outcome"] == "mutual_take"; mu = runs[v["unwatched"]]["outcome"] == "mutual_take"
            t = "unwatched_only_take" if mu and not mw else "watched_only_take" if mw and not mu else \
                "both_take" if mw else "neither_take"
            if t in cnt:
                cnt[t][0] += has(v[arm], m, scope); cnt[t][1] += 1
        (k1, n1), (k2, n2) = cnt[grp_a], cnt[grp_b]
        l1, h1 = wilson(k1, n1); l2, h2 = wilson(k2, n2)
        rows.append([scope, m, arm, cond_fixed, f"{grp_a}: {k1}/{n1} ({k1/n1:.0%}; {l1:.0%}-{h1:.0%})",
                     f"{grp_b}: {k2}/{n2} ({k2/n2:.0%}; {l2:.0%}-{h2:.0%})", f"{k1/n1-k2/n2:+.1%}",
                     f"{fisher(k1, n1-k1, k2, n2-k2):.2g}"])
with open(HERE / "tables" / "outcome_held_contrasts.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["text_scope", "measure", "arm_measured", "held_fixed", "notice-dependent cells", "comparison cells",
                "difference", "fisher_p"])
    w.writerows(rows)
for r in rows:
    print(r)
