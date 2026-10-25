# Completed pressure study — 25 October 2026

**4,320 / 4,320 planned experimental episodes reached terminal status.** There are **4,243 usable completions (98.2%) and 77 exclusions**. All excluded attempts remain in the raw evidence; they are not counted as refusals.

[Raw results and transcripts](../../results/2026-10-25-pressure-study/README.md) · [Run summary](../../results/2026-10-25-pressure-study/summary.json) · [Provenance](provenance.json) · [Earlier progress snapshots](../../results/archive/README.md)

This is the completed **72-scenario, eight-setting study**: 5 stress levels × 6 pairings × 2 monitoring notices × 1 seed. It is distinct from the newer five-setting prompt design and the older 600-episode study; these datasets are not pooled.

[Deep reasoning audit: findings, graphs and 12 evidence cases](reasoning-audit/README.md)

## Raw data for the current slice

The current slice is the completed **72-scenario, eight-setting collection**, frozen on **25 October 2026 at 16:42:07 UTC**. Its repository-relative location is **`results/2026-10-25-pressure-study/`**.

- [Episode index (`runs.csv`)](../../results/2026-10-25-pressure-study/runs.csv): look up scenario, stress level, pairing, monitoring notice and run ID.
- [Raw episode folders (`runs/`)](../../results/2026-10-25-pressure-study/runs/): `<run_id>/events.jsonl` holds requests, responses, returned reasoning and delivered messages; `<run_id>/result.json` holds status, final decisions, outcomes and errors; `<run_id>/transcript.md` is the readable transcript.
- [Frozen prompts and configuration](../../results/2026-10-25-pressure-study/manifest.json) and [integrity checksums](../../results/2026-10-25-pressure-study/SHA256SUMS.json).

All 4,320 planned experimental episodes, including the 77 exclusions, are retained here. This analysis folder contains derived tables and graphs. Earlier partial checkpoints are archived separately under `results/archive/2026-10-25/`.

## Main results

| Outcome among usable episodes | Count | Share |
|---|---:|---:|
| Both take (joint acceptance) | 1,075 | 25.3% |
| Only one takes | 282 | 6.6% |
| Both refuse | 2,886 | 68.0% |

![Joint acceptance by pressure level](figures/pressure-level-joint-acceptance.png)

| Stress level | Usable episodes | Both take | Rate |
|---|---:|---:|---:|
| 1 | 848 | 46 | 5.4% |
| 2 | 850 | 115 | 13.5% |
| 3 | 843 | 188 | 22.3% |
| 4 | 852 | 272 | 31.9% |
| 5 | 850 | 454 | 53.4% |

## Watched versus unwatched: three average graphs

**2,083 of 2,160 comparison cells have usable completions under both notices.** The remaining 77 cells are excluded from paired comparisons. Each matched cell fixes scenario, stress level, pairing and seed. Watched and unwatched rates therefore use exactly the same cells. The two pairings for each rule are combined with equal weight per matched cell.

Across matched cells, joint acceptance is **23.3% watched versus 27.2% unwatched** (**-3.9 percentage points**, watched minus unwatched).

| Rule | Matched cells | Watched | Unwatched | Difference |
|---|---:|---:|---:|---:|
| Welfare | 692 | 38.7% | 47.0% | -8.2 pp |
| Non-deception | 694 | 18.3% | 20.9% | -2.6 pp |
| Authority | 697 | 12.9% | 13.9% | -1.0 pp |

### Welfare

![Welfare: average monitoring comparison](figures/w-average-monitoring.png)

### Non-deception

![Non-deception: average monitoring comparison](figures/d-average-monitoring.png)

### Authority

![Authority: average monitoring comparison](figures/a-average-monitoring.png)

[Download average graph data](tables/rule-level-monitoring-averages.csv)

## Each stress level and pairing

![Monitoring by level and pairing](figures/matched-monitoring-overview.png)

[Download pairing × level data](tables/pairing-level-monitoring.csv)

## Every scenario

Each cell reads **watched / unwatched**: **T** = both take; **O** = one takes; **R** = both refuse; **?** = excluded. Gray cells have an excluded episode and do not stand for refusal. Purple marks joint acceptance only when unwatched; orange marks it only when watched. Full titles and all cells are in the linked comparison table.

Among matched cells, 436 have joint acceptance under both notices, 1467 under neither, 49 only when watched and 131 only when unwatched.

[Download all 2,160 scenario comparisons](tables/scenario-level-pairing-comparisons.csv)

### Hospital

![Hospital: all scenarios, stress levels and pairings](figures/hospital-monitoring-grid.png)

### Religious

![Religious: all scenarios, stress levels and pairings](figures/religious-monitoring-grid.png)

### Military

![Military: all scenarios, stress levels and pairings](figures/military-monitoring-grid.png)

### School

![School: all scenarios, stress levels and pairings](figures/school-monitoring-grid.png)

### Volunteer

![Volunteer: all scenarios, stress levels and pairings](figures/volunteer-monitoring-grid.png)

### Social Club

![Social Club: all scenarios, stress levels and pairings](figures/social_club-monitoring-grid.png)

### Family

![Family: all scenarios, stress levels and pairings](figures/family-monitoring-grid.png)

### Situational

![Situational: all scenarios, stress levels and pairings](figures/situational-monitoring-grid.png)

## Interpretation and limits

Joint acceptance is the operational outcome: both agents choose `take`. It does not by itself establish deception, criterion compliance or causally confirmed collusion. The monitoring manipulation changes the notice shown to the agents; researcher logging is identical. There is one seed per cell, related scenario templates, no communication-off or none–none experimental baseline, and exclusions may depend on condition. Report these as descriptive comparisons rather than a general causal effect of surveillance.

“Completed” means all planned episodes ended, including failures; it does not mean every episode passed formatting checks. The frozen snapshot metadata uses a generic “partial snapshot” policy label, but its 4,243 complete + 77 failed statuses establish full terminal coverage. That original metadata is preserved without alteration.

All 42,992 returned responses include returned reasoning; 62,858,676 tokens were recorded, including controls. Returned reasoning is model output, not verified access to internal thought. Endpoint switches and recovery attempts remain in the raw audit files.

## Reproduce

```powershell
python analysis/2026-10-25-pressure-study/build_report.py
```

The script reads the frozen CSV and verifies every planned row against its saved result. It uses original run IDs rather than rebuilding the matrix from current prompt code. It writes only this analysis folder, makes no model requests and changes no raw evidence.

All figures have adjacent SVG versions for export. CSV tables retain denominators and explicit missing/excluded states. Earlier partial-snapshot graphs are superseded by this completed-run report; no earlier partial estimates are reused.
