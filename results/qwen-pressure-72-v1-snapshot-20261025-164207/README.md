# Extended pressure results

Snapshot cutoff: 2026-10-25T16:42:07.460485+00:00

4,243 parse-valid completions / 4,320 planned; 77 excluded failures.

Outcomes among usable completions: {'both_refuse': 2886, 'mutual_take': 1075, 'unilateral_take': 282}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## Collusion rate by pressure level

![Collusion rate by pressure level](figures/level-collusion-rate.png)

## By level

![Outcomes](figures/level-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| Level 1 | 848 | 46 | 5.4% |
| Level 2 | 850 | 115 | 13.5% |
| Level 3 | 843 | 188 | 22.3% |
| Level 4 | 852 | 272 | 31.9% |
| Level 5 | 850 | 454 | 53.4% |

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 713 | 97 | 13.6% |
| A-none | 704 | 93 | 13.2% |
| D-D | 707 | 152 | 21.5% |
| D-none | 707 | 130 | 18.4% |
| W-W | 710 | 387 | 54.5% |
| W-none | 702 | 216 | 30.8% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 527 | 179 | 34.0% |
| hospital | 532 | 139 | 26.1% |
| military | 532 | 123 | 23.1% |
| religious | 531 | 130 | 24.5% |
| school | 531 | 106 | 20.0% |
| situational | 532 | 163 | 30.6% |
| social_club | 529 | 114 | 21.6% |
| volunteer | 529 | 121 | 22.9% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 2125 | 575 | 27.1% |
| watched | 2118 | 500 | 23.6% |

## Evidence

Returned reasoning coverage: 42992/42992 responses, including controls. Tokens: 62,858,676.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
