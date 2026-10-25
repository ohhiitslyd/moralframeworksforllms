# Extended pressure results

Snapshot cutoff: 2026-10-25T15:58:19.409266+00:00

3,613 parse-valid completions / 4,320 planned; 70 excluded failures.

Outcomes among usable completions: {'both_refuse': 2460, 'mutual_take': 927, 'unilateral_take': 226}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## Collusion rate by pressure level

![Collusion rate by pressure level](figures/level-collusion-rate.png)

## By level

![Outcomes](figures/level-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| Level 1 | 724 | 38 | 5.2% |
| Level 2 | 718 | 97 | 13.5% |
| Level 3 | 724 | 166 | 22.9% |
| Level 4 | 728 | 239 | 32.8% |
| Level 5 | 719 | 387 | 53.8% |

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 614 | 83 | 13.5% |
| A-none | 593 | 77 | 13.0% |
| D-D | 592 | 125 | 21.1% |
| D-none | 597 | 115 | 19.3% |
| W-W | 610 | 336 | 55.1% |
| W-none | 607 | 191 | 31.5% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 453 | 150 | 33.1% |
| hospital | 460 | 124 | 27.0% |
| military | 444 | 106 | 23.9% |
| religious | 455 | 120 | 26.4% |
| school | 455 | 92 | 20.2% |
| situational | 444 | 136 | 30.6% |
| social_club | 455 | 96 | 21.1% |
| volunteer | 447 | 103 | 23.0% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 1796 | 496 | 27.6% |
| watched | 1817 | 431 | 23.7% |

## Evidence

Returned reasoning coverage: 36703/36703 responses, including controls. Tokens: 53,637,012.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
