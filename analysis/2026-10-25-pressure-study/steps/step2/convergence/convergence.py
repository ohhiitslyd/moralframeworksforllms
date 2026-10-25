"""Convergence-step mechanics of the monitoring effect (completed study).

For paired cells (scenario|level|pairing), compares round-1 public stances and final
outcomes of watched vs unwatched twins, split by discordance direction. Uses Step 1
stance columns (classifier 81% held-out; undercounts take stances as unclear) and
exact final actions. Run from the worktree root:
    python tools/run_reserved.py analysis/2026-10-25-pressure-study/steps/step2/convergence/convergence.py
"""
import pandas as pd
from collections import Counter
d = pd.read_csv("analysis/2026-10-25-pressure-study/steps/step1/trial_metrics.csv", low_memory=False)
d = d[d.status == "complete"].copy()
d["mt"] = d.outcome == "mutual_take"
w = d[d.monitoring == "watched"].set_index("cell_id"); u = d[d.monitoring == "unwatched"].set_index("cell_id")
cells = w.index.intersection(u.index)
def traj(r):
    def ag(s):
        return "".join({"take":"T","refuse":"R","unclear":"?","silent":"-"}.get(str(r[f"stance_r{i}_{s}"]),"·") for i in (1,2,3))
    return ag("a") + "|" + ag("b")
def kind(r):
    st = [str(r[f"stance_r1_{s}"]) for s in "ab"]
    fin = [r.action_a, r.action_b]
    r1 = "both take" if st == ["take","take"] else "both refuse" if st == ["refuse","refuse"] else "split/unclear"
    return r1
groups = {"take only UNWATCHED": [c for c in cells if u.at[c,"mt"] and not w.at[c,"mt"]],
          "take only WATCHED":   [c for c in cells if w.at[c,"mt"] and not u.at[c,"mt"]],
          "take in BOTH":        [c for c in cells if w.at[c,"mt"] and u.at[c,"mt"]]}
for g, cs in groups.items():
    print(f"\n== {g}: {len(cs)} cells")
    for arm, df in (("unwatched", u), ("watched", w)):
        r1 = Counter(kind(df.loc[c]) for c in cs)
        fin = Counter("mutual take" if df.at[c,"mt"] else ("lone take" if df.at[c,"outcome"]=="unilateral_take" else "both refuse") for c in cs)
        conv = sum(1 for c in cs if kind(df.loc[c]) != "both take" and df.at[c,"mt"])
        print(f"  {arm:9s} round-1 public stance: {dict(r1)}")
        print(f"  {arm:9s} final outcome:          {dict(fin)}   |  reached mutual take without both saying 'take' in round 1: {conv}")
# persuasion within mutual takes overall
mt = d[d.mt]
r1both = (mt.stance_r1_a == "take") & (mt.stance_r1_b == "take")
print(f"\nAll mutual takes: {len(mt)}; both said take in round 1: {r1both.sum()} ({r1both.mean():.0%}); otherwise reached later: {(~r1both).sum()}")
for arm in ("unwatched","watched"):
    m = mt[mt.monitoring == arm]; b = (m.stance_r1_a=="take")&(m.stance_r1_b=="take")
    print(f"  {arm}: {len(m)} mutual takes, {b.mean():.0%} with both 'take' in round 1")
