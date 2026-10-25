# Results layout and provenance

Cleanup was performed on `codex/resolve-pressure-merge` in an isolated checkout. The original experiment checkout, environments, outputs and local studio work were left in place.

## Canonical completed study

The full 4,320-episode run is `results/2026-10-25-pressure-study/`. It is the frozen `20261025-164207` snapshot from commit `82b644ce5439c6fc6f28e4cdeaedf032a28cc848`. Its 4,243 completed and 77 failed episodes account for every planned episode. The snapshot still contains its original generic partial-snapshot policy text; the saved terminal counts establish collection completion. No metadata was rewritten.

The main report is `analysis/2026-10-25-pressure-study/README.md`. Graphs are regenerated from the completed evidence, not copied from the earlier partial analysis.

## Directory map

| Previous directory | Current directory |
|---|---|
| `results/hf-provider-probe-20261024-125118/` | `results/archive/2026-10-24/hf-provider-probe-20261024-125118/` |
| `results/hf-provider-probe-20261024-130409/` | `results/archive/2026-10-24/hf-provider-probe-20261024-130409/` |
| `results/mechanical-check-v1/` | `results/archive/2026-10-24/mechanical-check-v1/` |
| `results/qwen-full-99-v1/` | `results/archive/2026-10-24/qwen-full-99-v1/` |
| `results/qwen-pilot-v1/` | `results/archive/2026-10-24/qwen-pilot-v1/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-115759/` | `results/archive/2026-10-25/progress-115759/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-121256/` | `results/archive/2026-10-25/progress-121256/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-123715/` | `results/archive/2026-10-25/progress-123715/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-125308/` | `results/archive/2026-10-25/progress-125308/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-131134/` | `results/archive/2026-10-25/progress-131134/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-135352/` | `results/archive/2026-10-25/progress-135352/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-141425/` | `results/archive/2026-10-25/progress-141425/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-145559/` | `results/archive/2026-10-25/progress-145559/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-152937/` | `results/archive/2026-10-25/progress-152937/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-155819/` | `results/archive/2026-10-25/progress-155819/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-161829/` | `results/archive/2026-10-25/progress-161829/` |
| `results/qwen-pressure-72-v1-snapshot-20261025-164207/` | `results/2026-10-25-pressure-study/` |
| `results/qwen-pressure-final-20261024-181708/` | `results/archive/2026-10-24/qwen-pressure-final-20261024-181708/` |
| `results/qwen-pressure-partial-20261024-1730/` | `results/archive/2026-10-24/qwen-pressure-partial-20261024-1730/` |
| `results/qwen-pressure-partial-20261024-174425/` | `results/archive/2026-10-24/qwen-pressure-partial-20261024-174425/` |
| `results/qwen-pressure-partial-20261024-180119/` | `results/archive/2026-10-24/qwen-pressure-partial-20261024-180119/` |
| `analysis/qwen-pressure-final-20261024-181708/` | `analysis/archive/2026-10-24-pressure-study/` |

All moved raw result files keep their original Git blob and byte contents. Run IDs and within-snapshot paths are unchanged, so checksum manifests remain valid. Historical analysis documents and the metrics builder have updated paths; data tables and plots are retained. Earlier project-level reports are under `docs/archive/`.

Transient process logs and local shortcuts are ignored by Git. They were not deleted from the experiment checkout. This branch does not rename any live output directory or change collection behavior.

## Validation

- All 25 unit tests pass.
- All 80,381 moved raw result files retain their original Git blob hashes.
- All 13,017 checksums in the completed collection pass after the move.
- All 124 links in the new Markdown and HTML navigation pages resolve in the staged tree.
- All 4,320 final CSV rows are checked against their saved result records before plotting.
- The report contains 13 figures, each exported as PNG and SVG, plus four CSV tables.

Run `python tools/verify_results_layout.py` to repeat the raw-file and link checks.
