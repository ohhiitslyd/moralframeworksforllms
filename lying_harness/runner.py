from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def safe_error(exc):
    message = str(exc)
    secret = os.environ.get("LLM_API_KEY")
    if secret:
        message = message.replace(secret, "[REDACTED]")
    return f"{type(exc).__name__}: {message[:1500]}"


def render_transcript(events, result, path):
    lines = [f"# {result['run_id']}", "", f"Backend: **{result['backend']}**; status: **{result['status']}**.", ""]
    if result["backend"] == "mock":
        lines += ["**SCRIPTED MECHANICAL FIXTURE — not an LLM result.**", ""]
    for event in events:
        if event["kind"] == "response":
            lines += [f"## Agent {event['agent']} — {event['stage']} {event.get('exchange') or ''}", "",
                      "### Endpoint-returned reasoning (private)", "", event.get("reasoning") or "Unavailable", "",
                      "### Structured response", "", "```json", event["content"], "```", ""]
        elif event["kind"] == "delivery":
            lines += [f"## Delivered peer messages — exchange {event['exchange']}", "",
                      "```json", json.dumps(event["messages"], indent=2), "```", ""]
    lines += ["## Outcome", "", "```json", json.dumps(result, indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    print("Use python -m lying_harness.pressure --output <dir>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
