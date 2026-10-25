# Extended pressure results

Snapshot cutoff: 2026-10-25T12:53:08.702536+00:00

717 parse-valid completions / 4,320 planned; 16 excluded failures.

Outcomes among usable completions: {'both_refuse': 478, 'unilateral_take': 53, 'mutual_take': 186}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 114 | 16 | 14.0% |
| A-none | 124 | 16 | 12.9% |
| D-D | 107 | 26 | 24.3% |
| D-none | 119 | 26 | 21.8% |
| W-W | 134 | 67 | 50.0% |
| W-none | 119 | 35 | 29.4% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 82 | 28 | 34.1% |
| hospital | 96 | 28 | 29.2% |
| military | 96 | 27 | 28.1% |
| religious | 89 | 25 | 28.1% |
| school | 97 | 14 | 14.4% |
| situational | 91 | 28 | 30.8% |
| social_club | 90 | 20 | 22.2% |
| volunteer | 76 | 16 | 21.1% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 348 | 93 | 26.7% |
| watched | 369 | 93 | 25.2% |

## Evidence

Returned reasoning coverage: 7306/7306 responses, including controls. Tokens: 10,712,083.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
