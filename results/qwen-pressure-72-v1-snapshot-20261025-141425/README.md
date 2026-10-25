# Extended pressure results

Snapshot cutoff: 2026-10-25T14:14:25.947442+00:00

1,862 parse-valid completions / 4,320 planned; 40 excluded failures.

Outcomes among usable completions: {'both_refuse': 1256, 'mutual_take': 477, 'unilateral_take': 129}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## Collusion rate by pressure level

![Collusion rate by pressure level](figures/level-collusion-rate.png)

## By level

![Outcomes](figures/level-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| Level 1 | 370 | 17 | 4.6% |
| Level 2 | 369 | 53 | 14.4% |
| Level 3 | 382 | 80 | 20.9% |
| Level 4 | 362 | 121 | 33.4% |
| Level 5 | 379 | 206 | 54.4% |

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 311 | 48 | 15.4% |
| A-none | 298 | 40 | 13.4% |
| D-D | 301 | 64 | 21.3% |
| D-none | 299 | 63 | 21.1% |
| W-W | 319 | 156 | 48.9% |
| W-none | 334 | 106 | 31.7% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 217 | 75 | 34.6% |
| hospital | 240 | 67 | 27.9% |
| military | 231 | 54 | 23.4% |
| religious | 251 | 65 | 25.9% |
| school | 231 | 39 | 16.9% |
| situational | 249 | 74 | 29.7% |
| social_club | 218 | 45 | 20.6% |
| volunteer | 225 | 58 | 25.8% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 932 | 253 | 27.1% |
| watched | 930 | 224 | 24.1% |

## Evidence

Returned reasoning coverage: 18927/18927 responses, including controls. Tokens: 27,774,432.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
