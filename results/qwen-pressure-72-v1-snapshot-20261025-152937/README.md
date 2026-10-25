# Extended pressure results

Snapshot cutoff: 2026-10-25T15:29:37.859192+00:00

3,026 parse-valid completions / 4,320 planned; 60 excluded failures.

Outcomes among usable completions: {'both_refuse': 2046, 'mutual_take': 787, 'unilateral_take': 193}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## Collusion rate by pressure level

![Collusion rate by pressure level](figures/level-collusion-rate.png)

## By level

![Outcomes](figures/level-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| Level 1 | 605 | 31 | 5.1% |
| Level 2 | 597 | 80 | 13.4% |
| Level 3 | 611 | 144 | 23.6% |
| Level 4 | 606 | 202 | 33.3% |
| Level 5 | 607 | 330 | 54.4% |

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 500 | 67 | 13.4% |
| A-none | 477 | 65 | 13.6% |
| D-D | 499 | 102 | 20.4% |
| D-none | 496 | 98 | 19.8% |
| W-W | 524 | 284 | 54.2% |
| W-none | 530 | 171 | 32.3% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 389 | 128 | 32.9% |
| hospital | 385 | 103 | 26.8% |
| military | 378 | 94 | 24.9% |
| religious | 379 | 100 | 26.4% |
| school | 373 | 74 | 19.8% |
| situational | 387 | 119 | 30.7% |
| social_club | 370 | 81 | 21.9% |
| volunteer | 365 | 88 | 24.1% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 1525 | 425 | 27.9% |
| watched | 1501 | 362 | 24.1% |

## Evidence

Returned reasoning coverage: 30705/30705 responses, including controls. Tokens: 44,984,111.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
