# Two-agent pressure experiments

## Completed study — 25 October 2026

**4,320 planned episodes finished: 4,243 usable completions and 77 exclusions.**
This study used 72 scenarios across eight settings, five stress levels, six pairings,
watched/unwatched notices and one seed per condition.

**[Read the completed-run analysis and all graphs](analysis/2026-10-25-pressure-study/README.md)**

- [Deep reasoning audit: findings, graphs and 12 evidence cases](analysis/2026-10-25-pressure-study/reasoning-audit/README.md)
- [Raw results, transcripts and audit records](results/2026-10-25-pressure-study/README.md)
- [Results directory](results/README.md) — completed study and historical archives
- [Analysis directory](analysis/README.md) — current report and earlier studies
- [Folder changes and original names](docs/results-layout.md)

The analysis includes three average monitoring graphs (welfare, non-deception and
authority), a stress-level × pairing overview, eight detailed scenario charts,
the overall pressure-level graph, and two graphs showing all watched/unwatched outcomes
and which agent takes alone. Every graph is calculated from the completed
collection, with matched denominators for watched/unwatched comparisons.

## Raw data for the current slice

The current slice is the completed **72-scenario, eight-setting collection**
(4,320 planned experimental episodes), frozen on **25 October 2026 at 16:42:07 UTC**.
Its raw data is in **[`results/2026-10-25-pressure-study/`](results/2026-10-25-pressure-study/)**,
relative to the repository root on this branch.

- [Episode index (`runs.csv`)](results/2026-10-25-pressure-study/runs.csv): find an episode by scenario, stress level, pairing, monitoring notice and run ID.
- [Per-episode raw records (`runs/`)](results/2026-10-25-pressure-study/runs/): each `<run_id>/events.jsonl` contains requests, responses, returned reasoning and delivered peer messages; `<run_id>/result.json` contains status, final decisions, outcomes and errors; `<run_id>/transcript.md` is the readable transcript.
- [Frozen prompts and configuration (`manifest.json`)](results/2026-10-25-pressure-study/manifest.json).
- [File-integrity checksums (`SHA256SUMS.json`)](results/2026-10-25-pressure-study/SHA256SUMS.json).

For example, the [S001, level 1, welfare–welfare, watched raw event log](results/2026-10-25-pressure-study/runs/S001-L1-W-W-s1-watched/events.jsonl)
is one episode in this slice. All 77 excluded attempts remain in the raw collection.
The analysis folder contains derived graphs and tables; earlier progress snapshots
are under `results/archive/2026-10-25/`.

## Project layout

| Folder | Purpose |
|---|---|
| `results/2026-10-25-pressure-study/` | Frozen completed collection; raw evidence is unchanged |
| `analysis/2026-10-25-pressure-study/` | Main report, reproducible builder, figures and CSV tables |
| `results/archive/` | Earlier studies and superseded progress snapshots, separated by date |
| `analysis/archive/` | Earlier study analysis; kept separate from today's findings |
| `prompts/` | Current five-setting prompt design and historical prompt archive |
| `lying_harness/` | Experiment, validation and publication code |
| `research/` | Design notes and collection history |
| `prompt-library/` | Shared development and analysis instructions |
| `analysis-pipeline/` | Analysis process documentation |

## Reproduce the report

```powershell
python analysis/2026-10-25-pressure-study/build_report.py
```

This reads the saved collection and makes no model calls. It writes only the analysis
folder. The report does not regenerate historical run IDs from the current prompts.

## Future experiments

The default runner uses the newer **five-setting, 495-scenario design**, which is
different from the completed eight-setting study above. Plan a fresh experiment with:

```powershell
python -m lying_harness.pressure --output results/new-study --plan
```

Use a new output directory for a new design. Do not resume an older collection with
different prompt content or run IDs. Existing local experiment checkouts and their
uncommitted work were not moved or modified during this cleanup.

## Earlier work

- [24 October analysis: 600-episode pressure study](analysis/archive/2026-10-24-pressure-study/SUMMARY-ANALYSIS.md)
- [Original 99-case experiment results](docs/archive/99-case-results.md)
- [Earlier project overview](docs/archive/project-overview-before-cleanup.md)
- [Research design](research/04-moral-framework-tipping-design.md)
- [Prompt library](prompt-library/README.md)

Joint acceptance means both agents choose `take`; it is an operational outcome,
not by itself proof of deception or causally confirmed collusion. Keep the studies
separate and retain failed attempts when interpreting the findings.
