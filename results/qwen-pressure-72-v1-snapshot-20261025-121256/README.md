# Extended pressure results

Snapshot cutoff: 2026-10-25T12:12:56.424301+00:00

481 parse-valid completions / 4,320 planned; 10 excluded failures.

Outcomes among usable completions: {'both_refuse': 322, 'unilateral_take': 33, 'mutual_take': 126}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 69 | 11 | 15.9% |
| A-none | 88 | 14 | 15.9% |
| D-D | 72 | 18 | 25.0% |
| D-none | 81 | 18 | 22.2% |
| W-W | 86 | 41 | 47.7% |
| W-none | 85 | 24 | 28.2% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 53 | 20 | 37.7% |
| hospital | 67 | 18 | 26.9% |
| military | 67 | 19 | 28.4% |
| religious | 62 | 18 | 29.0% |
| school | 62 | 8 | 12.9% |
| situational | 61 | 20 | 32.8% |
| social_club | 66 | 15 | 22.7% |
| volunteer | 43 | 8 | 18.6% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 227 | 62 | 27.3% |
| watched | 254 | 64 | 25.2% |

## Evidence

Returned reasoning coverage: 4894/4894 responses, including controls. Tokens: 7,161,696.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
