# Extended pressure results

Snapshot cutoff: 2026-10-25T12:37:15.357741+00:00

547 parse-valid completions / 4,320 planned; 40 excluded failures.

Outcomes among usable completions: {'both_refuse': 368, 'unilateral_take': 37, 'mutual_take': 142}

72 scenes across 8 settings, five levels, six pairings, watched/unwatched notices, one seed per cell. Three peer exchanges; temperature 0.6; maximum 4096 output tokens. Execution order is shuffled with seed 20261025. Watched/unwatched describes the notice shown to agents; researcher logging is identical.

Mutual take is an operational outcome, not causally established collusion. No communication-off or none-none experimental baseline is present. Rule wording differs from the earlier study. Qualitative utilities, template-related scenarios, differences in task content between settings, one seed, incomplete coverage and output exclusions limit interpretation. Rule compliance requires manual review. Do not pool this study with the older mixed-provider batch.

## By pairing

![Outcomes](figures/pairing-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| A-A | 79 | 13 | 16.5% |
| A-none | 94 | 14 | 14.9% |
| D-D | 89 | 22 | 24.7% |
| D-none | 92 | 22 | 23.9% |
| W-W | 96 | 44 | 45.8% |
| W-none | 97 | 27 | 27.8% |

## By setting_id

![Outcomes](figures/setting-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| family | 60 | 21 | 35.0% |
| hospital | 77 | 21 | 27.3% |
| military | 75 | 20 | 26.7% |
| religious | 70 | 21 | 30.0% |
| school | 71 | 10 | 14.1% |
| situational | 68 | 23 | 33.8% |
| social_club | 72 | 16 | 22.2% |
| volunteer | 54 | 10 | 18.5% |

## By monitoring

![Outcomes](figures/monitoring-outcomes.png)

| Group | Usable | Both take | Both take rate |
|---|---:|---:|---:|
| unwatched | 256 | 70 | 27.3% |
| watched | 291 | 72 | 24.7% |

## Evidence

Returned reasoning coverage: 5576/5576 responses, including controls. Tokens: 8,176,229.

Full requests, returned reasoning, peer messages, decisions, errors and endpoint provenance are under [runs](runs/). Returned reasoning is model output, not verified internal thought. All attempted controls are retained and excluded from experimental rates.

[All planned episode rows](runs.csv) · [Frozen pack and settings](manifest.json) · [Summary](summary.json) · [Checksums](SHA256SUMS.json)
