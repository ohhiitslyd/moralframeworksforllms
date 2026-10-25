"""Draw the stratified held-out validation sample (v2 rules; excludes dev-round texts) (precision + recall strata), arm hidden.

Writes validation_sample_key.csv (item_id, stratum, arm, flags, text) and
validation_sheet_blind.csv (item_id, text only; shuffled) for hand labelling.
Launch: python tools/run_reserved.py <this script>
"""
import csv, gzip, json, random, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
M = ["a", "b", "c_low", "c_high", "e", "d"]
BROAD = re.compile(r"monitor|oversight|watched|review|scrutin|caught|detect|discover|found out|no one|nobody|get away", re.I)
rng = random.Random(20261026)  # held-out round (dev round used seed 20261025 and v1 rules)
DEV = set()
if (HERE / "dev_v1_sample_key.csv").exists():
    DEV = {r["text"] for r in csv.DictReader(open(HERE / "dev_v1_sample_key.csv", encoding="utf-8"))}
flagged = {}
for r in csv.DictReader(gzip.open(HERE / "flagged_sentences.csv.gz", "rt", encoding="utf-8")):
    flagged[(r["run_id"], r["agent"], r["stage"], r["exchange"], r["source"], r["sid"])] = r
# precision strata
items = []
for m in M:
    for arm in ("watched", "unwatched"):
        pool = [r for r in flagged.values() if r["arm"] == arm and r[m] == "1" and r["text"] not in DEV]
        for r in rng.sample(pool, min(20, len(pool))):
            items.append(("prec_" + m, arm, r["text"], {k: r[k] for k in M}))
# recall strata: broad-keyword sentences; reservoir sample unflagged ones
unfl = {"watched": [], "unwatched": []}; seen = {"watched": 0, "unwatched": 0}
for line in gzip.open(HERE / "corpus_sentences.jsonl.gz", "rt", encoding="utf-8"):
    r = json.loads(line)
    s = r["masked"]
    if not BROAD.search(s):
        continue
    k = (r["run_id"], r["agent"], r["stage"], str(r["exchange"]), r["source"], str(r["sid"]))
    if k in flagged or s in DEV:
        continue
    arm = r["run_id"].rsplit("-", 1)[1]
    seen[arm] += 1
    L = unfl[arm]
    if len(L) < 25:
        L.append(s)
    else:
        j = rng.randrange(seen[arm])
        if j < 25:
            L[j] = s
for arm in unfl:
    for s in unfl[arm]:
        items.append(("recall_unflagged", arm, s, {k: "0" for k in M}))
print("unflagged broad pool sizes", seen)
rng.shuffle(items)
with open(HERE / "validation_sample_key.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["item_id", "stratum", "arm"] + M + ["text"])
    for i, (st, arm, s, f) in enumerate(items):
        w.writerow([i, st, arm] + [f[k] for k in M] + [s])
with open(HERE / "validation_sheet_blind.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["item_id", "text"])
    for i, (st, arm, s, f) in enumerate(items):
        w.writerow([i, s])
json.dump(seen, open(HERE / "recall_pool_sizes.json", "w"))
print("items", len(items))
