"""Publish one immutable analyzed pressure snapshot on the user's current branch."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

from dotenv import dotenv_values

from .pressure_snapshot import freeze, analyze, read
from .runner import ROOT

BRANCH = "experiment-harness-pilot-results"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def validate(snapshot):
    summary = read(snapshot / "summary.json")
    rows = list(csv.DictReader((snapshot / "runs.csv").open(encoding="utf-8")))
    assert len(rows) == summary["planned"] == sum(summary["statuses"].values())
    assert sum(summary["outcomes"].values()) == summary["statuses"].get("complete", 0)
    cutoff = read(snapshot / "SNAPSHOT.json")["cutoff_utc"]
    secrets = [v for p in ROOT.glob(".env*") for k, v in dotenv_values(p).items()
               if v and len(v) > 10 and ("KEY" in k or "TOKEN" in k)]
    for path in snapshot.rglob("*"):
        if not path.is_file() or path.suffix not in (".json", ".jsonl", ".md", ".csv", ".py"):
            continue
        content = path.read_text(encoding="utf-8")
        if any(secret in content for secret in secrets):
            raise ValueError(f"Credential detected in {path.name}; refusing publication")
        if path.name == "events.jsonl":
            assert all(json.loads(line)["timestamp"] <= cutoff for line in content.splitlines())
    for name, digest in read(snapshot / "SHA256SUMS.json").items():
        assert hashlib.sha256((snapshot / name).read_bytes()).hexdigest() == digest, name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Commit and push the authorized branch")
    args = parser.parse_args()
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("Unexpected branch; refusing to switch or publish")
    if git("diff", "--cached", "--name-only"):
        raise ValueError("Existing staged changes require inspection before publication")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    live_results = [read(p) for p in (ROOT / "results/qwen-pressure-600-v1/runs").glob("*/result.json")]
    final = sum(not r["spec"]["control"] and r["status"] in ("complete", "failed") for r in live_results) == 600
    snapshot = ROOT / "results" / f"qwen-pressure-{'final' if final else 'partial'}-{stamp}"
    freeze(ROOT / "results/qwen-pressure-600-v1", snapshot)
    analyze(snapshot)
    validate(snapshot)
    summary = read(snapshot / "summary.json")
    terminal = summary["statuses"].get("complete", 0) + summary["statuses"].get("failed", 0)
    section = ("<!-- PRESSURE_LATEST_START -->\n"
        "## Latest pressure-scenario results\n\n"
        f"[Read the latest analysis, graphs and full run logs](results/{snapshot.name}/README.md). "
        f"Snapshot: **{summary['cutoff_utc'][:19].replace('T', ' ')} UTC**. "
        f"**{terminal}/600 terminal episodes: {summary['statuses'].get('complete', 0)} parse-valid completions, "
        f"{summary['statuses'].get('failed', 0)} failures, {summary['outcomes'].get('mutual_take', 0)} mutual-take outcomes.**\n\n"
        f"![Current pressure-study outcomes](results/{snapshot.name}/figures/pairing-outcomes.png)\n\n"
        "The timestamped snapshot includes CSV data, complete prompts/responses/returned reasoning, "
        "transcripts and recovery records. "
        + ("Collection is finished. " if final else "It remains fixed while live collection continues. ")
        + "Results are descriptive, with exclusions and mixed-provider limitations. "
        "[Earlier published snapshot](results/qwen-pressure-partial-20261024-1730/README.md).\n\n"
        "The original hospital allocation experiment and its completed 99-case results are described below.\n"
        "<!-- PRESSURE_LATEST_END -->")
    readme = ROOT / "README.md"
    content = readme.read_text(encoding="utf-8")
    if "<!-- PRESSURE_LATEST_START -->" in content:
        content = re.sub(r"<!-- PRESSURE_LATEST_START -->.*?<!-- PRESSURE_LATEST_END -->", lambda _: section, content, flags=re.S)
    else:
        old = r"## New: partial results from the 20-scenario pressure study.*?are described below\."
        content, count = re.subn(old, lambda _: section, content, count=1, flags=re.S)
        if count != 1:
            raise ValueError("Latest-results README section not found")
    readme.write_text(content, encoding="utf-8")
    if args.publish:
        paths = [str(snapshot.relative_to(ROOT)), "README.md", "lying_harness/pressure.py",
                 "lying_harness/pressure_snapshot.py", "lying_harness/pressure_publish.py"]
        git("add", "--", *paths)
        git("commit", "--quiet", "-m", f"Publish pressure snapshot {stamp}: {terminal} terminal episodes")
        subprocess.run(["git", "push", "origin", BRANCH], cwd=ROOT, check=True)
        local = git("rev-parse", "HEAD")
        remote = git("ls-remote", "--heads", "origin", BRANCH).split()[0]
        if local != remote:
            raise ValueError("Remote verification mismatch")
        print("Pushed commit", local)
    print("Report:", f"https://github.com/tomloscalzo/hackathon-lying-agent-experiment/tree/{BRANCH}/results/{snapshot.name}")


if __name__ == "__main__":
    main()
