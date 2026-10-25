# Extended pressure results

Snapshot cutoff: 2026-10-25T13:53:52.542062+00:00

1,463 parse-valid completions / 4,320 planned; 27 excluded failures.

Outcomes among usable completions: {'both_refuse': 989, 'mutual_take': 372, 'unilateral_take': 102}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 237 | 38 | 16.0% |
| A-none | 234 | 30 | 12.8% |
| D-D | 244 | 54 | 22.1% |
| D-none | 230 | 43 | 18.7% |
| W-W | 260 | 126 | 48.5% |
| W-none | 258 | 81 | 31.4% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 171 | 58 | 33.9% |
| hospital | 186 | 50 | 26.9% |
| military | 185 | 44 | 23.8% |
| religious | 197 | 52 | 26.4% |
| school | 181 | 26 | 14.4% |
| situational | 194 | 58 | 29.9% |
| social_club | 173 | 39 | 22.5% |
| volunteer | 176 | 45 | 25.6% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 728 | 195 | 26.8% |
| watched | 735 | 177 | 24.1% |

## Evidence

Returned reasoning coverage: 15009/15009 responses, including controls. Tokens: 22,018,881.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
