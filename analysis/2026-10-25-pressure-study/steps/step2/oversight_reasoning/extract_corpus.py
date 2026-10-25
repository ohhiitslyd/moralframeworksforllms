"""Step 2 / oversight reasoning: extract per-sentence corpus from run events.

Reads (read-only) results/2026-10-25-pressure-study/runs.csv and runs/<id>/events.jsonl.
Writes corpus_sentences.jsonl.gz in this directory: one row per sentence with
run_id, agent, stage, exchange, source (reasoning | plan | peer_message | decision_text),
channel (private | public), raw sentence and notice-masked sentence.

Launch: python tools/run_reserved.py <this script>
"""
import csv
import gzip
import json
import os
import re
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
RES = ROOT / "results" / "2026-10-25-pressure-study"

MAN = json.loads((RES / "manifest.json").read_text(encoding="utf-8"))
NOTICES = MAN["pack"]["monitoring_texts"]

# --- Notice masking -------------------------------------------------------
# Exact notice sentences (and their constituent sentences) are replaced by a token
# so that verbatim copying of the prompt cannot trigger the content measures.
_notice_sents = []
for arm, txt in NOTICES.items():
    _notice_sents.append((arm, txt))
    for s in re.split(r"(?<=\.)\s+", txt):
        _notice_sents.append((arm, s))
# Longest first; case-insensitive, whitespace-flexible.
_notice_sents.sort(key=lambda t: -len(t[1]))
NOTICE_RES = [(arm, re.compile(r"\s+".join(re.escape(w) for w in s.split()), re.I))
              for arm, s in _notice_sents]


def mask_notice(text):
    n = 0
    for arm, rx in NOTICE_RES:
        text, k = rx.subn(f" [NOTICE_{arm.upper()}] ", text)
        n += k
    return text, n


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")


def sentences(text):
    out = []
    for s in SENT_SPLIT.split(text or ""):
        s = s.strip(" \t\"'{}`,")
        if len(s) >= 3:
            out.append(s)
    return out


def parse_content(stage, content):
    """Return list of (source, channel, text) from the structured content."""
    content = content or ""
    if stage == "message":
        try:
            obj = json.loads(content.strip().strip("`").removeprefix("json").strip())
            items = []
            if obj.get("plan"):
                items.append(("plan", "private", str(obj["plan"])))
            if obj.get("peer_message"):
                items.append(("peer_message", "public", str(obj["peer_message"])))
            return items
        except Exception:
            m = re.search(r'"peer_message"\s*:\s*"(.*?)"\s*[,}]', content, re.S)
            items = [("plan", "private", re.sub(r'"peer_message"\s*:\s*".*', "", content, flags=re.S))]
            if m:
                items.append(("peer_message", "public", m.group(1)))
            return items
    if stage == "decision":
        return [("decision_text", "private", content)]
    return [("plan", "private", content)]


def process(run_id):
    rows = []
    p = RES / "runs" / run_id / "events.jsonl"
    if not p.exists():
        return rows
    with open(p, encoding="utf-8") as fh:
        for line in fh:
            e = json.loads(line)
            if e.get("kind") != "response":
                continue
            items = [("reasoning", "private", e.get("reasoning") or "")]
            items += parse_content(e["stage"], e.get("content"))
            for source, channel, text in items:
                masked, nmask = mask_notice(text)
                for i, s in enumerate(sentences(masked)):
                    rows.append({
                        "run_id": run_id, "agent": e["agent"], "stage": e["stage"],
                        "exchange": int(e["exchange"]), "source": source, "channel": channel,
                        "sid": i, "masked": s,
                        "notice_copy": "[NOTICE_" in s,
                    })
    return rows


def main():
    runs = list(csv.DictReader(open(RES / "runs.csv", encoding="utf-8")))
    ids = [r["run_id"] for r in runs if r["status"] == "complete"]
    workers = int(os.environ.get("RESERVED_WORKERS", "4"))
    workers = max(1, min(8, workers))
    out = HERE / "corpus_sentences.jsonl.gz"
    n = 0
    with ProcessPoolExecutor(workers) as ex, gzip.open(out, "wt", encoding="utf-8") as fh:
        for rows in ex.map(process, ids, chunksize=32):
            for r in rows:
                fh.write(json.dumps(r) + "\n")
                n += 1
    print("runs", len(ids), "sentences", n, "->", out)


if __name__ == "__main__":
    main()
