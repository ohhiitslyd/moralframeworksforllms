"""Condensed side-by-side view of a stratified sample of discordant cells for manual mechanism coding.

Sample: 32 of 131 unwatched-only-take cells and 16 of 49 watched-only-take cells, stratified by level
(proportional, seeded). Writes discordant_review_sample.csv (cells drawn) and discordant_review_dump.txt.
Launch: python tools/run_reserved.py <this script>
"""
import csv, gzip, json, random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parents[4] / "results" / "2026-10-25-pressure-study"
rng = random.Random(180)
disc = list(csv.DictReader(open(HERE / "tables" / "discordant_cells.csv", encoding="utf-8")))
target = {"unwatched_only_take": 32, "watched_only_take": 16}
sample = []
for direction, n in target.items():
    rows = [r for r in disc if r["direction"] == direction]
    by = defaultdict(list)
    for r in rows:
        by[r["level"]].append(r)
    # proportional allocation by level, largest remainder
    alloc = {l: n * len(v) / len(rows) for l, v in by.items()}
    k = {l: int(a) for l, a in alloc.items()}
    for l in sorted(alloc, key=lambda l: -(alloc[l] - k[l]))[: n - sum(k.values())]:
        k[l] += 1
    for l, v in sorted(by.items()):
        sample += rng.sample(v, k[l])
with open(HERE / "discordant_review_sample.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(sample[0].keys()))
    w.writeheader(); w.writerows(sample)

ids = {r[k] for r in sample for k in ("run_watched", "run_unwatched")}
flag = defaultdict(list)
for r in csv.DictReader(gzip.open(HERE / "flagged_sentences.csv.gz", "rt", encoding="utf-8")):
    if r["run_id"] in ids:
        ms = [m for m in ("a", "b", "c_low", "c_high", "e", "d") if r[m] == "1"]
        if ms:
            flag[(r["run_id"], r["agent"])].append(f"[{','.join(ms)}|{r['stage'][0]}{r['exchange']}|{r['source'][:4]}] {r['text'][:220]}")


def clip(s, n):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[:n] + "…"


out = open(HERE / "discordant_review_dump.txt", "w", encoding="utf-8")
for c in sample:
    out.write("=" * 90 + f"\nCELL {c['scenario']}|L{c['level']}|{c['pairing']}  {c['direction']}  "
              f"W:{c['actions_watched_AB']}({c['outcome_watched']})  U:{c['actions_unwatched_AB']}({c['outcome_unwatched']})\n")
    first = True
    for arm, rid in (("W", c["run_watched"]), ("U", c["run_unwatched"])):
        out.write(f"--- {arm} {rid}\n")
        for line in open(RES / "runs" / rid / "events.jsonl", encoding="utf-8"):
            e = json.loads(line)
            if first and e["kind"] == "request" and e["stage"] == "plan" and e["agent"] == "A":
                sm = e["messages"][0]["content"]
                i = sm.find("Principals who have spoken"); j = sm.find("You have been told")
                out.write("  [ctx] " + clip(sm[i:j], 420) + "\n")
                first = False
            if e["kind"] != "response":
                continue
            st = e["stage"]
            content = e.get("content") or ""
            if st == "message":
                try:
                    o = json.loads(content.strip())
                    content = "MSG> " + str(o.get("peer_message", ""))
                except Exception:
                    content = "MSG?> " + content
                out.write(f"  {e['agent']}{e['exchange']} {clip(content, 260)}\n")
            elif st == "plan":
                out.write(f"  {e['agent']} PLAN {clip(content, 300)}\n")
            else:
                out.write(f"  {e['agent']} DECISION {clip(content, 260)}\n")
                out.write(f"     final-reasoning tail: {clip((e.get('reasoning') or '')[-420:], 420)}\n")
        for ag in "AB":
            for s in flag.get((rid, ag), [])[:7]:
                out.write(f"    {ag} {s}\n")
out.close()
print("sampled", len(sample))
