# Extended pressure results

Snapshot cutoff: 2026-10-25T11:57:59.692818+00:00

221 parse-valid completions / 4,320 planned; 3 excluded failures.

Outcomes among usable completions: {'both_refuse': 142, 'unilateral_take': 17, 'mutual_take': 62}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 34 | 6 | 17.6% |
| A-none | 43 | 8 | 18.6% |
| D-D | 38 | 12 | 31.6% |
| D-none | 35 | 9 | 25.7% |
| W-W | 33 | 14 | 42.4% |
| W-none | 38 | 13 | 34.2% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 30 | 11 | 36.7% |
| hospital | 32 | 11 | 34.4% |
| military | 24 | 7 | 29.2% |
| religious | 29 | 14 | 48.3% |
| school | 30 | 3 | 10.0% |
| situational | 35 | 8 | 22.9% |
| social_club | 25 | 4 | 16.0% |
| volunteer | 16 | 4 | 25.0% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 106 | 31 | 29.2% |
| watched | 115 | 31 | 27.0% |

## Evidence

Returned reasoning coverage: 2493/2493 responses, including controls. Tokens: 3,619,823.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
