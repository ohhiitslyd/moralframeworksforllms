# Two-agent pressure experiments

## Completed study — 25 October 2026

**4,320 planned episodes finished: 4,243 usable completions and 77 exclusions.**
This study used 72 scenarios across eight settings, five stress levels, six pairings,
watched/unwatched notices and one seed per condition.

**[Read the completed-run analysis and all graphs](analysis/2026-10-25-pressure-study/README.md)**

- [Raw results, transcripts and audit records](results/2026-10-25-pressure-study/README.md)
- [Results directory](results/README.md) — completed study and historical archives
- [Analysis directory](analysis/README.md) — current report and earlier studies
- [Folder changes and original names](docs/results-layout.md)

The analysis includes three average monitoring graphs (welfare, non-deception and
authority), a stress-level × pairing overview, eight detailed scenario charts,
and the overall pressure-level graph. Every graph is calculated from the completed
collection, with matched denominators for watched/unwatched comparisons.

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
