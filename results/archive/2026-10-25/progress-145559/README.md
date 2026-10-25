# Extended pressure results

Snapshot cutoff: 2026-10-25T14:55:59.522266+00:00

2,353 parse-valid completions / 4,320 planned; 119 excluded failures.

Outcomes among usable completions: {'both_refuse': 1579, 'mutual_take': 615, 'unilateral_take': 159}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## Collusion rate by pressure level

![Collusion rate by pressure level](figures/level-collusion-rate.png)

## By level

![Outcomes](figures/level-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| Level 1 | 458 | 25 | 5.5% |
| Level 2 | 480 | 69 | 14.4% |
| Level 3 | 478 | 108 | 22.6% |
| Level 4 | 461 | 152 | 33.0% |
| Level 5 | 476 | 261 | 54.8% |

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 382 | 54 | 14.1% |
| A-none | 371 | 52 | 14.0% |
| D-D | 378 | 82 | 21.7% |
| D-none | 383 | 80 | 20.9% |
| W-W | 413 | 210 | 50.8% |
| W-none | 426 | 137 | 32.2% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 287 | 98 | 34.1% |
| hospital | 301 | 83 | 27.6% |
| military | 298 | 69 | 23.2% |
| religious | 308 | 81 | 26.3% |
| school | 290 | 59 | 20.3% |
| situational | 310 | 94 | 30.3% |
| social_club | 283 | 64 | 22.6% |
| volunteer | 276 | 67 | 24.3% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 1192 | 342 | 28.7% |
| watched | 1161 | 273 | 23.5% |

## Evidence

Returned reasoning coverage: 24207/24207 responses, including controls. Tokens: 35,484,267.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
