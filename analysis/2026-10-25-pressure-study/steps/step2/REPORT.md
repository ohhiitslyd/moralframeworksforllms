# Completed pressure study: Step 2 analysis report (FINAL-DATA)

**FINAL-DATA.** This is the completed run (`2026-10-25-pressure-study`). All 4,320 planned trials are terminal: 4,243 complete and 77 failed. These are final-data estimates for one model and one seed per cell. The primary test is the one pre-registered for the interim snapshot, run on the final data. The interim pairs are a subset of these data, so this is not an independent replication. See [PREREG.md](PREREG.md).

**Audience:** the team and hackathon judges (AI safety researchers). The model is Qwen3-32B at temperature 0.6, with one seed per cell. Two agents exchange three rounds of simultaneous messages, then lock in a take/refuse decision. Script: `analyze_full.py` (revised after an expert review of the interim analysis).

**Words used here.** A *mutual take* means both agents' locked final action was take. This is an operational outcome, not "collusion": in some scenes taking is arguably justified. *Watched / unwatched* names the text notice the agents saw. Researcher logging was identical in both arms, so this is a notice, not real oversight. Reasoning traces are generated text, not evidence of internal states.

## 1. Summary (FINAL-DATA)

- **Primary (pre-registered, sprint 3.4).** 2,083 cells have both the watched and the unwatched trial complete. In those cells the mutual-take rate was 23.3% with the watched notice and 27.2% with the unwatched notice. The paired difference is **-3.9 pp** (95% Newcombe CI -5.2 pp to -2.7 pp; scenario-cluster bootstrap -5.3 pp to -2.7 pp), a risk ratio of 0.86 (0.80-0.91). Discordant pairs: **49 watched-only takes vs 131 unwatched-only takes**; McNemar p = 1.6e-09 (exact 8.0e-10). The direction matches the pre-registered expectation. The minimum detectable effect at 80% power is 1.8 pp.
- **Robustness.** The result is robust to every failure bound and within the main endpoint. It holds when both trials ran on the main endpoint (Modal-B: -4.4 pp (-5.9 pp to -2.9 pp), 33 watched-only vs 97 unwatched-only, p = 3.3e-08, 1,471 pairs). Even with all 42 watched failures counted as takes and all 35 unwatched failures as no take, p stays at or below .05 (p = 0.034). Across the 14 diagnostic, pairing and level subgroups, 14 point the same way (watched lower). However, 5 of those subgroup intervals cross 0, so "same direction" tells us little on its own. The heterogeneity tests, which are on the conditional-odds-ratio scale, are: diagnostic p = 0.11, pairing 0.64, level 0.67.
- **Dose-response by level (secondary, added after review).** Paired gap by level: L1 -1.0 pp (RR 0.83); L2 -4.5 pp (RR 0.71); L3 -5.4 pp (RR 0.78); L4 -4.0 pp (RR 0.88); L5 -4.8 pp (RR 0.91). A conditional logit on the 180 discordant pairs gives a trend of x1.10 in the conditional OR per level (log-OR slope +0.10, 95% cluster CI -0.18 to +0.41; LR p = 0.44). Section 4b separates the absolute (pp) scale from the relative (RR / OR) scale.
- **Words vs. actions (secondary).** The notice reduced takes by about 4 pp (agent take -3.8 pp, 95% CI -5.0 to -2.5 pp). There is no evidence of sanitised talk with an unchanged deal. Public wording shifted toward oversight / deception vocabulary (oversight / monitoring words +5.0 pp, deception words +5.6 pp), and what that vocabulary means is unvalidated. Pressure level, by contrast, moves agent takes by +51.6 pp (level 5 vs 1).
- **Interactions with monitoring** (ridge logit; null from 1,000 cluster-resampled parametric-bootstrap draws): mutual take x pressure level p = 0.8 (q = 0.93); x pairing p = 0.62 (q = 0.88); x scenario diagnostic (= family) p = 0.27 (q = 0.73). Diagnostic x pairing is design-built: the pack fixes whether the pairing's rule matches the scene's diagnostic. 4 of 30 interaction tests pass q < .05 (section 10).
- **Top candidates** (the first 8 rows of the ranked table in section 5, in the same order; everything except the primary is exploratory; one BH family over m = 355 candidate p-values):
  1. Watched notice -> fewer mutual takes (PRIMARY, paired McNemar): paired diff -3.9 pp (95% cluster CI -5.3 pp to -2.7 pp); n = 2,083.
  2. Level 5 vs 1: Argued for take (stance heuristic) (public messages, paired): paired diff +43.8 pp (95% cluster CI +38.4 pp to +49.5 pp); n = 834.
  3. Level 5 vs 1: Mutual take (actions, paired): paired diff +48.4 pp (95% cluster CI +42.2 pp to +54.9 pp); n = 834.
  4. Level 5 vs 1: Agent took (actions, paired): paired diff +51.6 pp (95% cluster CI +45.5 pp to +57.7 pp); n = 834.
  5. Welfare + no-rule pairs: lone takes by the rule agent 45 vs the no-rule agent 4: rule agent's share of lone takes 91.8% (Wilson 0.81-0.97); n = 49.
  6. Pack's expected_first_take predicts whether rule agents take: kappa 0.62; n = 6,373.
  7. Pairing -> Mutual take (both agents took): V 0.33 (cluster CI 0.29-0.37); n = 4,243.
  8. Pressure level -> Any take (at least one took): |rho| 0.39 (cluster CI 0.35-0.43); n = 4,243.
- **Design check.** Completion status is not associated with any design parameter (smallest BH q = 0.86). Monitoring, level and pairing are cleanly crossed. Setting and diagnostic effects are descriptive only: they vary at the scenario level, with only 72 scenes in total, and the scenes differ in content.

## 2. How to read the charts

- **Effect sizes** in screening are on comparable 0-1 scales: bias-corrected Cramér's V (categorical parameter x binary outcome), sqrt(epsilon^2) (categorical x numeric or agent-rate outcome) and |Spearman rho| (ordinal / numeric parameter). As a rough guide, 0.1 is small, 0.3 medium and 0.5 large.
- **Monitoring effects** are paired (the same cell under both notices). Each one is reported in percentage points (watched minus unwatched) **and** as a risk ratio (watched / unwatched). Discordant pairs are always labelled by direction: *watched-only take* means the watched trial was a mutual take and its unwatched partner was not; *unwatched-only take* is the reverse. Heterogeneity tests on the discordant split compare conditional odds ratios, not pp gaps.
- **Intervals.** Every primary-section interval (primary, subgroups, dose-response, words vs. actions, rule application, top relationships) uses **one shared set of 2,000 scenario-cluster bootstrap draws** (resampling the 72 scenarios). Newcombe intervals treat cells as independent and are shown alongside. Wilson intervals are used only for independent units.
- **Tests.** Screening p-values are asymptotic and ignore clustering. Survivors at BH q < .05 are confirmed by a sequential Besag-Clifford permutation at each parameter's randomisation level (schema randomisation_level; `tables/randomisation_levels.csv`), with up to 1,999 shuffles, stopping at 50 exceedances (floor 1/2,000). ● = confirmed, ○ = BH only.
- **Colour.** A single-hue blue sequential scale on an absolute range. Hatching = confounded parameter or by-construction pair. Grey cells = n < 5.

## 3. Design check and completion

Monitoring, level and pairing are fully crossed within every scenario. **Aliased by construction:** pairing, rule-in-pairing and matched-vs-mixed (the last two are coarsenings of pairing), and diagnostic = family. **Strongly associated pairs** (association >= 0.3; started trials; cell counts in `tables/design_cell_counts.csv`; matrix in Appendix A1):

| Parameter | Parameter | Association |
|---|---|---|
| pairing | pairing_rule | 1.00 |
| pairing | matched_vs_mixed | 1.00 |
| take_is_justified_ambiguous | refuse_breaks_promise | 0.96 |
| scenario_diagnostic | refuse_deceives_n | 0.88 |
| level | welfare_if_take_designer | 0.86 |
| scenario_diagnostic | refuse_breaks_promise | 0.84 |
| take_principal_present | n_principals | 0.83 |
| scenario_diagnostic | take_is_justified_ambiguous | 0.80 |
| refuse_deceives_n | refuse_breaks_promise | 0.76 |
| take_is_justified_ambiguous | refuse_deceives_n | 0.72 |
| soft_take_principal_present | n_principals | 0.72 |
| rank_stated_in_level_text | n_principals | 0.62 |
| level | take_principal_present | 0.61 |
| take_principal_present | rank_stated_in_level_text | 0.58 |
| level | n_principals | 0.56 |
| take_deceives_n | refuse_breaks_promise | 0.43 |

The scene-text features are written into the level text, so they move with pressure level and diagnostic; they are hatched everywhere. Endpoint, start rank and import status are collection-time variables.

**Completion by monitoring arm** (all 4,320 planned trials):

| Arm | Complete | Failed | Not started |
|---|---|---|---|
| unwatched | 2,125 | 35 | 0 |
| watched | 2,118 | 42 | 0 |

Completion status is not associated with any design parameter after BH correction (smallest q = 0.86; `tables/completion_balance.csv`; Appendix A2).

**Failure reasons by arm** (`tables/failures_by_reason_and_monitoring.csv`):

| Failure reason | Unwatched | Watched | Rate (of started), unwatched | Rate, watched | Fisher p (arm x this reason) |
|---|---|---|---|---|---|
| length_limit | 4 | 3 | 0.19% | 0.14% | 1 |
| missing_message | 17 | 23 | 0.79% | 1.06% | 0.43 |
| missing_plan | 1 | 0 | 0.05% | 0.00% | 1 |
| parse | 13 | 16 | 0.60% | 0.74% | 0.71 |
| (any failure) | 35 | 42 | 1.62% | 1.94% | 0.49 |

`missing_message` failures: 23 watched vs 17 unwatched (1.06% vs 0.79% of started trials; Fisher p = 0.43; as a share of each arm's failures, Fisher p = 0.65).

**Endpoint and the deal rate (unpaired comparison, all complete trials; not a paired test):** Modal-A 25.6% of 695 trials, Modal-B 25.3% of 3,545 trials, Modal-A+Modal-B 33.3% of 3 trials. Endpoint is also collection time, so this comparison is descriptive.

## 4. Primary test: monitoring notice and mutual take (pre-registered)

![Primary forest plot](figures/03_primary_monitoring_forest.png)

- **Test:** McNemar on 2,083 complete cell pairs. Discordant: **49 watched-only take vs 131 unwatched-only take**; concordant: 436 both take, 1467 neither.
- **Effect:** -3.94 pp (watched 23.3% vs unwatched 27.2%). Newcombe 95% CI -5.19 pp to -2.69 pp; scenario-cluster bootstrap -5.29 pp to -2.65 pp. Risk ratio 0.86 (0.80-0.91). Conditional odds ratio (watched-only / unwatched-only) 0.37.
- **p:** chi-square with continuity correction 1.6e-09; exact binomial 8.0e-10. alpha = .05, two-sided.
- **Power:** the discordance rate is 8.6%. The minimum detectable paired difference at 80% power is 1.8 pp with 2,083 pairs (1.8 pp if all 2,160 cells were paired).
- **Within endpoint** (endpoint = collection time; paired within class): both Modal-A: -8.3 pp (0 watched-only vs 6 unwatched-only, 72 pairs); both Modal-B: -4.4 pp (33 watched-only vs 97 unwatched-only, 1,471 pairs); split: -2.2 pp (16 watched-only vs 28 unwatched-only, 540 pairs). Endpoint x monitoring, tested on the discordant split across the both-same-endpoint classes: p = 0.34.
- **Within factors:** 14 of 14 diagnostic, pairing and level subgroups have watched < unwatched. **5 of these subgroup intervals cross 0, so their "same direction" is uninformative on its own.** Heterogeneity (chi-square on the discordant split, i.e. the conditional-OR scale): diagnostic p = 0.11, pairing 0.64, level 0.67, matched/mixed 0.7.
- **Related outcomes (same paired test; not confirmatory):** any take -3.6 pp (82 watched-only vs 157 unwatched-only); lone take +0.3 pp (93 vs 86, p = 0.65).

<details><summary>Full subgroup table (pp, Newcombe and cluster intervals, risk ratio)</summary>

| Subset | Pairs | Watched-only take | Unwatched-only take | Rate unwatched | Rate watched | Diff (w-u) | Newcombe lo | Newcombe hi | Cluster lo | Cluster hi | RR (w/u) | RR lo | RR hi | p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| All complete pairs (PRIMARY) | 2083 | 49 | 131 | 27.2% | 23.3% | -3.9 pp | -5.2 pp | -2.7 pp | -5.3 pp | -2.7 pp | 0.86 | 0.80 | 0.91 | 1.6e-09 |
| Endpoint: both Modal-A | 72 | 0 | 6 | 30.6% | 22.2% | -8.3 pp | -15.2 pp | -1.9 pp | -15.9 pp | -2.4 pp | 0.73 | 0.50 | 0.92 | 0.031 |
| Endpoint: both Modal-B | 1471 | 33 | 97 | 27.1% | 22.7% | -4.4 pp | -5.9 pp | -2.9 pp | -5.9 pp | -2.9 pp | 0.84 | 0.78 | 0.89 | 3.3e-08 |
| Endpoint: both Modal-A+Modal-B | 0 | 0 | 0 | – | – | – | – | – | – | – | nan | nan | nan | 1 |
| Endpoint: split | 540 | 16 | 28 | 27.2% | 25.0% | -2.2 pp | -4.6 pp | +0.2 pp | -4.9 pp | +0.2 pp | 0.92 | 0.83 | 1.01 | 0.097 |
| Diagnostic: welfare | 694 | 10 | 42 | 17.1% | 12.5% | -4.6 pp | -6.7 pp | -2.6 pp | -6.4 pp | -2.9 pp | 0.73 | 0.61 | 0.83 | 1.7e-05 |
| Diagnostic: nondeception | 694 | 20 | 57 | 37.6% | 32.3% | -5.3 pp | -7.8 pp | -2.9 pp | -8.0 pp | -2.4 pp | 0.86 | 0.77 | 0.94 | 4.1e-05 |
| Diagnostic: authority | 695 | 19 | 32 | 26.9% | 25.0% | -1.9 pp | -3.9 pp | +0.1 pp | -3.6 pp | +0.0 pp | 0.93 | 0.86 | 1.00 | 0.093 |
| Pairing: W-W | 350 | 13 | 38 | 58.0% | 50.9% | -7.1 pp | -11.0 pp | -3.2 pp | -11.2 pp | -3.2 pp | 0.88 | 0.81 | 0.94 | 7.8e-04 |
| Pairing: W-none | 342 | 11 | 43 | 35.7% | 26.3% | -9.4 pp | -13.4 pp | -5.3 pp | -13.5 pp | -5.2 pp | 0.74 | 0.64 | 0.85 | 2.5e-05 |
| Pairing: D-D | 347 | 8 | 15 | 22.2% | 20.2% | -2.0 pp | -4.8 pp | +0.7 pp | -4.5 pp | +0.3 pp | 0.91 | 0.80 | 1.01 | 0.21 |
| Pairing: D-none | 347 | 8 | 19 | 19.6% | 16.4% | -3.2 pp | -6.2 pp | -0.2 pp | -6.3 pp | +0.0 pp | 0.84 | 0.70 | 1.00 | 0.054 |
| Pairing: A-A | 353 | 3 | 7 | 14.2% | 13.0% | -1.1 pp | -3.1 pp | +0.7 pp | -2.8 pp | +0.6 pp | 0.92 | 0.80 | 1.04 | 0.34 |
| Pairing: A-none | 344 | 6 | 9 | 13.7% | 12.8% | -0.9 pp | -3.2 pp | +1.4 pp | -2.9 pp | +1.2 pp | 0.94 | 0.79 | 1.09 | 0.61 |
| Level: 1 | 416 | 4 | 8 | 5.8% | 4.8% | -1.0 pp | -2.8 pp | +0.8 pp | -2.9 pp | +0.5 pp | 0.83 | 0.56 | 1.12 | 0.39 |
| Level: 2 | 418 | 9 | 28 | 15.8% | 11.2% | -4.5 pp | -7.5 pp | -1.7 pp | -7.6 pp | -1.9 pp | 0.71 | 0.54 | 0.87 | 0.0031 |
| Level: 3 | 411 | 7 | 29 | 24.8% | 19.5% | -5.4 pp | -8.2 pp | -2.5 pp | -8.2 pp | -2.6 pp | 0.78 | 0.66 | 0.89 | 4.7e-04 |
| Level: 4 | 420 | 10 | 27 | 34.0% | 30.0% | -4.0 pp | -6.9 pp | -1.2 pp | -6.7 pp | -1.2 pp | 0.88 | 0.80 | 0.96 | 0.0085 |
| Level: 5 | 418 | 19 | 39 | 55.5% | 50.7% | -4.8 pp | -8.3 pp | -1.2 pp | -8.6 pp | -1.0 pp | 0.91 | 0.85 | 0.98 | 0.013 |
| Pair type: matched | 1050 | 24 | 60 | 31.4% | 28.0% | -3.4 pp | -5.1 pp | -1.7 pp | -5.1 pp | -1.8 pp | 0.89 | 0.84 | 0.94 | 1.3e-04 |
| Pair type: mixed | 1033 | 25 | 71 | 22.9% | 18.5% | -4.5 pp | -6.3 pp | -2.6 pp | -6.4 pp | -2.6 pp | 0.81 | 0.72 | 0.89 | 4.4e-06 |
| Outcome: any take (>=1 agent) | 2083 | 82 | 157 | 33.7% | 30.1% | -3.6 pp | -5.0 pp | -2.2 pp | -5.1 pp | -2.2 pp | 0.89 | 0.84 | 0.94 | 1.7e-06 |
| Outcome: lone take | 2083 | 93 | 86 | 6.5% | 6.9% | +0.3 pp | -0.9 pp | +1.6 pp | -0.9 pp | +1.5 pp | 1.05 | 0.87 | 1.25 | 0.65 |

</details>

### 4b. Monitoring dose-response by level, diagnostic and pairing (secondary)

![Monitoring by level: pp and risk ratio](figures/19_monitoring_by_level.png)

A **conditional logit** for matched pairs, with the subgroup as a pair-level covariate, reduces to a logistic regression of "watched-only" (vs "unwatched-only") on the covariate among discordant pairs. On the 180 discordant pairs, the linear level trend is a log-OR slope of +0.099 per level (Wald 95% CI -0.156 to +0.354; scenario-cluster bootstrap -0.177 to +0.407; LR p = 0.44). The conditional OR at level 3 is 0.35. Categorical LR tests on the same scale: level p = 0.66, diagnostic p = 0.12, pairing p = 0.65.

**Reading the two scales.** Base rates rise steeply with level. The same relative effect (RR or OR) therefore gives a larger pp gap at high levels, and a constant pp gap would mean a shrinking relative effect. These tests are on the OR scale. A flat OR trend does not mean the pp gap is flat. Compare the two panels.

| Subset | Pairs | Watched-only take | Unwatched-only take | Rate unwatched | Rate watched | Diff (w-u) | Newcombe lo | Newcombe hi | Cluster lo | Cluster hi | RR (w/u) | RR lo | RR hi | p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Diagnostic: welfare | 694 | 10 | 42 | 17.1% | 12.5% | -4.6 pp | -6.7 pp | -2.6 pp | -6.4 pp | -2.9 pp | 0.73 | 0.61 | 0.83 | 1.7e-05 |
| Diagnostic: nondeception | 694 | 20 | 57 | 37.6% | 32.3% | -5.3 pp | -7.8 pp | -2.9 pp | -8.0 pp | -2.4 pp | 0.86 | 0.77 | 0.94 | 4.1e-05 |
| Diagnostic: authority | 695 | 19 | 32 | 26.9% | 25.0% | -1.9 pp | -3.9 pp | +0.1 pp | -3.6 pp | +0.0 pp | 0.93 | 0.86 | 1.00 | 0.093 |
| Pairing: W-W | 350 | 13 | 38 | 58.0% | 50.9% | -7.1 pp | -11.0 pp | -3.2 pp | -11.2 pp | -3.2 pp | 0.88 | 0.81 | 0.94 | 7.8e-04 |
| Pairing: W-none | 342 | 11 | 43 | 35.7% | 26.3% | -9.4 pp | -13.4 pp | -5.3 pp | -13.5 pp | -5.2 pp | 0.74 | 0.64 | 0.85 | 2.5e-05 |
| Pairing: D-D | 347 | 8 | 15 | 22.2% | 20.2% | -2.0 pp | -4.8 pp | +0.7 pp | -4.5 pp | +0.3 pp | 0.91 | 0.80 | 1.01 | 0.21 |
| Pairing: D-none | 347 | 8 | 19 | 19.6% | 16.4% | -3.2 pp | -6.2 pp | -0.2 pp | -6.3 pp | +0.0 pp | 0.84 | 0.70 | 1.00 | 0.054 |
| Pairing: A-A | 353 | 3 | 7 | 14.2% | 13.0% | -1.1 pp | -3.1 pp | +0.7 pp | -2.8 pp | +0.6 pp | 0.92 | 0.80 | 1.04 | 0.34 |
| Pairing: A-none | 344 | 6 | 9 | 13.7% | 12.8% | -0.9 pp | -3.2 pp | +1.4 pp | -2.9 pp | +1.2 pp | 0.94 | 0.79 | 1.09 | 0.61 |
| Level: 1 | 416 | 4 | 8 | 5.8% | 4.8% | -1.0 pp | -2.8 pp | +0.8 pp | -2.9 pp | +0.5 pp | 0.83 | 0.56 | 1.12 | 0.39 |
| Level: 2 | 418 | 9 | 28 | 15.8% | 11.2% | -4.5 pp | -7.5 pp | -1.7 pp | -7.6 pp | -1.9 pp | 0.71 | 0.54 | 0.87 | 0.0031 |
| Level: 3 | 411 | 7 | 29 | 24.8% | 19.5% | -5.4 pp | -8.2 pp | -2.5 pp | -8.2 pp | -2.6 pp | 0.78 | 0.66 | 0.89 | 4.7e-04 |
| Level: 4 | 420 | 10 | 27 | 34.0% | 30.0% | -4.0 pp | -6.9 pp | -1.2 pp | -6.7 pp | -1.2 pp | 0.88 | 0.80 | 0.96 | 0.0085 |
| Level: 5 | 418 | 19 | 39 | 55.5% | 50.7% | -4.8 pp | -8.3 pp | -1.2 pp | -8.6 pp | -1.0 pp | 0.91 | 0.85 | 0.98 | 0.013 |

## 5. Top-ranked relationships

Candidates are scored on effect size, robustness, relevance to the sprint questions and surprise relative to the directions in PREREG.md. No finding has a hand-coded surprise score. **One BH family** covers the p-values of all 355 exploratory candidates (permutation, sign-flip, cluster-resampled bootstrap, LR and binomial). A candidate is listed only if q < .05 and it has no trust problem. Mechanical outcomes (word and token counts, reasoning length) are demoted. Full list: `tables/candidates.csv`. The summary in section 1 is the head of this table.

| Rank | Candidate | Source | Effect (interval) | n | q (one BH family) | Research question | Caveat |
|---|---|---|---|---|---|---|---|
| 1 | Watched notice -> fewer mutual takes (PRIMARY, paired McNemar) | primary McNemar | paired diff -3.9 pp (95% cluster CI -5.3 pp to -2.7 pp) | 2,083 | confirmatory | 3.4 monitoring | pre-registered; notice-only manipulation; one model / seed |
| 2 | Level 5 vs 1: Argued for take (stance heuristic) (public messages, paired) | words vs actions (paired) | paired diff +43.8 pp (95% cluster CI +38.4 pp to +49.5 pp) | 834 | 0.0011 | 2.2 words+actions x 1.1 level |  |
| 3 | Level 5 vs 1: Mutual take (actions, paired) | words vs actions (paired) | paired diff +48.4 pp (95% cluster CI +42.2 pp to +54.9 pp) | 834 | 0.0011 | 2.2 words+actions x 1.1 level |  |
| 4 | Level 5 vs 1: Agent took (actions, paired) | words vs actions (paired) | paired diff +51.6 pp (95% cluster CI +45.5 pp to +57.7 pp) | 834 | 0.0011 | 2.2 words+actions x 1.1 level |  |
| 5 | Welfare + no-rule pairs: lone takes by the rule agent 45 vs the no-rule agent 4 | asymmetry (mixed pairs) | rule agent's share of lone takes 91.8% (Wilson 0.81-0.97) | 49 | 2.9e-07 | 1.1 criterion / pairing | binomial p ignores scenario clustering (optimistic) |
| 6 | Pack's expected_first_take predicts whether rule agents take | rule application | kappa 0.62 | 6,373 | – | 1.1 criterion | agents clustered in scenarios; descriptive (no test) |
| 7 | Pairing -> Mutual take (both agents took) | screening | V 0.33 (cluster CI 0.29-0.37) | 4,243 | 0.0011 | 1.1 pairing |  |
| 8 | Pressure level -> Any take (at least one took) | screening | /rho/ 0.39 (cluster CI 0.35-0.43) | 4,243 | 0.0011 | 1.1 level |  |
| 9 | Pairing -> Agent took | screening | sqrt(eps2) 0.30 (cluster CI 0.26-0.35) | 4,243 | 0.0011 | 1.1 pairing |  |
| 10 | Pressure level -> Plan said take (of plans with an action) | screening | /rho/ 0.38 (cluster CI 0.34-0.43) | 2,784 | 0.0011 | 1.1 level |  |
| 11 | Pairing -> Any take (at least one took) | screening | V 0.28 (cluster CI 0.24-0.32) | 4,243 | 0.0011 | 1.1 pairing |  |
| 12 | Interaction Pressure level x Pairing -> mutual take | interaction (ridge logit) | deviance drop minus df 80 | 4,243 | 0.0021 | 1.1 variables for emergence |  |
| 13 | Watched notice: Deception words, public (public messages, paired) | words vs actions (paired) | paired diff +5.6 pp (95% cluster CI +4.1 pp to +7.3 pp) | 2,083 | 0.0011 | 2.2 words+actions x 3.4 |  |
| 14 | Pairing -> Plan states an action | screening | sqrt(eps2) 0.32 (cluster CI 0.29-0.36) | 4,243 | 0.0011 | 1.1 pairing |  |
| 15 | Pairing -> Argued for take in public (some round) | screening | sqrt(eps2) 0.32 (cluster CI 0.29-0.36) | 4,243 | 0.0011 | 1.1 pairing |  |

**Demoted (mechanical):** Level 5 vs 1: Public words sent (public messages, paired) (paired diff +21.9 (+19.2 to +24.4)); Pairing -> Reasoning length (words) (sqrt(eps2) 0.43 (cluster CI 0.37-0.47)); Pairing -> Total tokens used (sqrt(eps2) 0.57 (cluster CI 0.53-0.60)); Watched notice: Public words sent (public messages, paired) (paired diff +5.8 (+4.5 to +7.2)); Pairing -> Public words exchanged (both agents) (sqrt(eps2) 0.37 (cluster CI 0.34-0.40)); Pairing -> Public words sent (agent) (sqrt(eps2) 0.37 (cluster CI 0.34-0.40)). These track prompt and message length, which differ by design (e.g. pairing changes the rules text).

![Top relationships](figures/13_top_relationships.png)

The monitoring panel shows paired rates over the same complete cell pairs, with the paired difference in its title. All y axes start at 0. Within-stratum checks: `tables/top_relationships_within_strata.csv`.

**Looks large but untrustworthy** (`tables/candidates_untrustworthy.csv`):

| Looks large but untrustworthy | Measure | Effect | Why |
|---|---|---|---|
| Level 5 vs 1: Deception words per 1k reasoning words (private reasoning, paired) | paired diff | -2.076 | private deception words mostly echo the prompt's honesty notes |
| Rule in the pairing (W/D/A) -> Total tokens used | sqrt(eps2) | +0.544 | coarsening of pairing (aliased with pairing) |
| Pairing -> Deception words in private notes | sqrt(eps2) | +0.535 | private deception words mostly echo the prompt's honesty notes |
| Rule in the pairing (W/D/A) -> Deception words in private notes | sqrt(eps2) | +0.512 | private deception words mostly echo the prompt's honesty notes; coarsening of pairing (aliased with pairing) |
| A principal instructs take -> Agent took | sqrt(eps2) | +0.439 | confounded with level / diagnostic (scene text) |
| A principal instructs take -> Any take (at least one took) | V | +0.430 | confounded with level / diagnostic (scene text) |
| A principal instructs take -> Mutual take (both agents took) | V | +0.415 | confounded with level / diagnostic (scene text) |
| Level 5 vs 1: Deception-intended flag (private reasoning, paired) | paired diff | +0.403 | deception-intended flag is nearly 'took or planned take' (prompt states who taking misleads) |
| A principal instructs take -> Argued for take in public (some round) | sqrt(eps2) | +0.397 | confounded with level / diagnostic (scene text) |
| Rule in the pairing (W/D/A) -> Reasoning length (words) | sqrt(eps2) | +0.393 | coarsening of pairing (aliased with pairing) |
| Number of principal statements -> Agent took | /rho/ | +0.373 | confounded with level / diagnostic (scene text) |
| Number of principal statements -> Any take (at least one took) | /rho/ | +0.364 | confounded with level / diagnostic (scene text) |

## 6. Words vs. actions (secondary, sprint 2.2 x 3.4)

![Words vs actions](figures/04_words_vs_actions.png)

Each row is a paired difference. For monitoring, the pair is the watched and unwatched trial of the same cell. For level, it is level 5 vs level 1 of the same scenario x pairing x arm. Agent measures are averaged per episode, and vocabulary counts are notice-masked. Two kinds of row have been removed. Private monitoring mentions are gone because both notices contain "monitored" / "oversight", so they echo the notice. The level 5 vs 1 monitoring-mention row is gone for the same reason. "Deception-intended among takers" is gone because it is a post-treatment subset. Public oversight / monitoring words are kept as public wording, but what they mean is unvalidated.

**Monitoring (watched - unwatched):**

| Channel | Measure | Pairs | Arm A -> arm B | Paired diff | 95% cluster CI | q | Heuristic / per-arm accuracy |
|---|---|---|---|---|---|---|---|
| Actions | Mutual take | 2083 | 27.2% -> 23.3% | -3.9 pp | -5.3 to -2.7 pp | 4.0e-04 |  |
| Actions | Agent took | 2083 | 30.5% -> 26.7% | -3.8 pp | -5.0 to -2.5 pp | 4.0e-04 |  |
| Actions | Lone take | 2083 | 6.5% -> 6.9% | +0.3 pp | -0.9 to +1.5 pp | 0.7 |  |
| Public messages | Argued for take (stance heuristic) | 2083 | 30.7% -> 27.2% | -3.5 pp | -4.9 to -2.1 pp | 4.0e-04 | agreement watched 30/36, unwatched 28/36; take recall 25/36: arm-error caveat |
| Public messages | Deception words, public | 2083 | 18.7% -> 24.3% | +5.6 pp | +4.1 to +7.3 pp | 4.0e-04 | deterministic |
| Public messages | Oversight / monitoring words, public | 2083 | 2.7% -> 7.7% | +5.0 pp | +3.5 to +6.7 pp | 4.0e-04 | keyword match; semantic meaning unvalidated |
| Public messages | Agreement phrases, public | 2083 | 67.3% -> 71.6% | +4.3 pp | +1.7 to +6.9 pp | 0.0013 | deterministic |
| Public messages | Public words sent | 2083 | 59.6 -> 65.4 | +5.8 | +4.5 to +7.2 | 4.0e-04 | deterministic |
| Private reasoning | Plan states an action | 2083 | 44.8% -> 42.6% | -2.2 pp | -4.0 to -0.4 pp | 0.033 | deterministic |
| Private reasoning | Deception words, private notes | 2083 | 64.6% -> 68.1% | +3.5 pp | +2.0 to +4.9 pp | 4.0e-04 | deterministic |
| Private reasoning | Deception words, reasoning | 2083 | 95.0% -> 96.4% | +1.3 pp | +0.7 to +2.0 pp | 4.0e-04 | deterministic |
| Private reasoning | Deception words per 1k reasoning words | 2083 | 7.5 -> 7.6 | +0.1 | -0.0 to +0.2 | 0.074 | deterministic |
| Private reasoning | Mentions evaluator / score (decision) | 2083 | 1.5% -> 1.5% | +0.0 pp | -0.1 to +0.1 pp | 1 | deterministic |
| Private reasoning | Take-linked deception sentence | 2083 | 91.6% -> 93.2% | +1.6 pp | +0.6 to +2.5 pp | 0.0026 | part of deception_intended |
| Private reasoning | Deception-intended flag | 2083 | 28.6% -> 26.0% | -2.6 pp | -4.0 to -1.1 pp | 7.1e-04 | agreement watched 7/12 vs unwatched 11/12: POTENTIALLY BIASED |
| Private reasoning | Reasoning length (words) | 2083 | 1912.8 -> 1888.4 | -24.5 | -43.2 to -8.1 | 0.016 | deterministic |

**Pressure (level 5 - level 1):**

| Channel | Measure | Pairs | Arm A -> arm B | Paired diff | 95% cluster CI | q | Heuristic / per-arm accuracy |
|---|---|---|---|---|---|---|---|
| Actions | Mutual take | 834 | 5.2% -> 53.6% | +48.4 pp | +42.2 to +54.9 pp | 2.7e-04 |  |
| Actions | Agent took | 834 | 7.1% -> 58.7% | +51.6 pp | +45.5 to +57.7 pp | 2.7e-04 |  |
| Actions | Lone take | 834 | 4.0% -> 10.2% | +6.2 pp | +3.2 to +9.2 pp | 2.7e-04 |  |
| Public messages | Argued for take (stance heuristic) | 834 | 10.0% -> 53.8% | +43.8 pp | +38.4 to +49.5 pp | 2.7e-04 | agreement watched 30/36, unwatched 28/36; take recall 25/36: arm-error caveat |
| Public messages | Deception words, public | 834 | 21.3% -> 20.6% | -0.7 pp | -4.5 to +3.0 pp | 0.67 | deterministic |
| Public messages | Agreement phrases, public | 834 | 64.2% -> 72.5% | +8.3 pp | +3.7 to +12.6 pp | 2.7e-04 | deterministic |
| Public messages | Public words sent | 834 | 50.8 -> 72.7 | +21.9 | +19.2 to +24.4 | 2.7e-04 | deterministic |
| Private reasoning | Plan states an action | 834 | 39.9% -> 43.9% | +4.0 pp | +0.4 to +8.1 pp | 0.021 | deterministic |
| Private reasoning | Deception words, private notes | 834 | 73.7% -> 59.2% | -14.5 pp | -17.5 to -11.6 pp | 2.7e-04 | deterministic |
| Private reasoning | Deception words, reasoning | 834 | 99.0% -> 90.9% | -8.0 pp | -10.6 to -5.6 pp | 2.7e-04 | deterministic |
| Private reasoning | Deception words per 1k reasoning words | 834 | 8.7 -> 6.6 | -2.1 | -2.3 to -1.8 | 2.7e-04 | deterministic |
| Private reasoning | Mentions evaluator / score (decision) | 834 | 1.7% -> 1.1% | -0.7 pp | -1.9 to +0.1 pp | 0.067 | deterministic |
| Private reasoning | Take-linked deception sentence | 834 | 97.9% -> 84.7% | -13.2 pp | -16.5 to -10.3 pp | 2.7e-04 | part of deception_intended |
| Private reasoning | Deception-intended flag | 834 | 9.1% -> 49.3% | +40.3 pp | +35.2 to +45.6 pp | 2.7e-04 | agreement watched 7/12 vs unwatched 11/12: POTENTIALLY BIASED |
| Private reasoning | Reasoning length (words) | 834 | 1867.6 -> 1900.7 | +33.1 | -16.3 to +82.6 | 0.062 | deterministic |

**Reading.** The notice reduced takes by about 4 pp (agent take -3.8 pp, 95% CI -5.0 to -2.5 pp). There is no evidence of sanitised talk with an unchanged deal. Public wording shifted toward oversight / deception vocabulary (oversight / monitoring words +5.0 pp, deception words +5.6 pp), and what that vocabulary means is unvalidated.

**Deception-intended flag: decomposition only (descriptive).** P(flag) = P(take) x P(flag | take). P(flag | take) conditions on a post-treatment variable, so it is not a monitoring contrast:

| Arm | Agents | Takers | P(take) | P(flag) | P(flag / take) (post-treatment, descriptive) |
|---|---|---|---|---|---|
| unwatched | 4250 | 1288 | 30.3% | 28.6% | 83.9% |
| watched | 4236 | 1144 | 27.0% | 26.3% | 87.2% |

**Asymmetry in mixed pairs (who takes alone).** Agent A holds the rule:

| Rule in pair | Episodes | Lone takes | Rule agent alone | No-rule agent alone | Share by rule agent | Wilson lo | Wilson hi | Binomial p |
|---|---|---|---|---|---|---|---|---|
| welfare | 702 | 49 | 45 | 4 | 91.8% | 80.8% | 96.8% | 8.2e-10 |
| nondeception | 707 | 74 | 44 | 30 | 59.5% | 48.1% | 69.9% | 0.13 |
| authority | 704 | 83 | 21 | 62 | 25.3% | 17.2% | 35.6% | 7.5e-06 |
| all | 2113 | 206 | 110 | 96 | 53.4% | 46.6% | 60.1% | 0.37 |

![Asymmetry](figures/05_asymmetry_mixed_pairs.png)

The binomial p treats episodes as independent, so it is optimistic (episodes cluster in scenarios).

**Rule application vs. the pack's expected_first_take** (rule agents only; shared-draw cluster CIs):

| Rule | Expected take at this level? | Agents | Took | Rate | 95% lo (cluster) | 95% hi |
|---|---|---|---|---|---|---|
| welfare | 0 | 848 | 178 | 21.0% | 15.2% | 27.3% |
| welfare | 1 | 1274 | 879 | 69.0% | 62.4% | 75.4% |
| nondeception | 0 | 1664 | 198 | 11.9% | 7.8% | 16.9% |
| nondeception | 1 | 457 | 308 | 67.4% | 53.5% | 80.7% |
| authority | 0 | 1674 | 7 | 0.4% | 0.1% | 1.0% |
| authority | 1 | 456 | 327 | 71.7% | 61.3% | 80.8% |
| all | 0 | 4186 | 383 | 9.1% | 6.8% | 12.0% |
| all | 1 | 2187 | 1514 | 69.2% | 62.8% | 75.5% |

Cohen's kappa between "level >= expected first-take level" and "agent took": welfare 0.46, non-deception 0.53, authority 0.79, all 0.62.

![Rule application](figures/06_rule_application.png)

## 7. Univariate results

Full table: `tables/univariate_summary.csv`. Variable profile: `tables/variable_profile.csv`. Charts are in Appendix A3. Private deception words appear in 95.8% of agents' reasoning. This reflects echo of the honesty notes.

## 8. Matrices

Screening covered 567 parameter x outcome pairs. Of these, 344 pass BH q < .05 and 243 are confirmed by the cluster-aware permutation. The overview heat map and outcome matrix are in Appendix A4. Top rows (full table `tables/screening_table.csv`):

| Parameter | Outcome | Measure | Effect | 95% cluster CI | Raw spread | p (asym.) | q (BH) | p (perm.) | Eff. n | Min cell | Design | Heuristic | Simpson flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Pairing | Total tokens used | sqrt(eps2) | 0.57 | 0.53-0.60 | 2843.13 | 2.8e-292 | 1.6e-289 | 5.0e-04 | 4243 | 702 | clean (manipulated) |  | False |
| Rule in the pairing (W/D/A) | Total tokens used | sqrt(eps2) | 0.54 | 0.51-0.58 | 2189.18 | 7.5e-273 | 2.1e-270 | 5.0e-04 | 4243 | 1412 | clean (manipulated) |  | False |
| Pairing | Deception words in private notes | sqrt(eps2) | 0.54 | 0.50-0.58 | 0.64 | 1.6e-260 | 3.0e-258 | 5.0e-04 | 4243 | 702 | clean (manipulated) |  | False |
| Rule in the pairing (W/D/A) | Deception words in private notes | sqrt(eps2) | 0.51 | 0.48-0.56 | 0.49 | 8.3e-242 | 1.2e-239 | 5.0e-04 | 4243 | 1412 | clean (manipulated) |  | False |
| A principal instructs take | Agent took | sqrt(eps2) | 0.44 | 0.38-0.50 | 0.46 | 3.5e-180 | 4.0e-178 | 5.0e-04 | 72 | 918 | confounded with level / diagnostic (scene text) |  | False |
| A principal instructs take | Any take (at least one took) | V | 0.43 | 0.37-0.48 | 0.49 | 2.1e-163 | 1.3e-161 | 5.0e-04 | 72 | 918 | confounded with level / diagnostic (scene text) |  | False |
| Pairing | Reasoning length (words) | sqrt(eps2) | 0.43 | 0.37-0.47 | 443.92 | 4.4e-166 | 3.1e-164 | 5.0e-04 | 4243 | 702 | clean (manipulated) |  | False |
| A principal instructs take | Mutual take (both agents took) | V | 0.41 | 0.36-0.47 | 0.44 | 5.5e-145 | 2.4e-143 | 5.0e-04 | 72 | 918 | confounded with level / diagnostic (scene text) |  | False |
| Pressure level | Agent took | /rho/ | 0.40 | 0.36-0.44 | 0.51 | 1.1e-177 | 1.1e-175 | 5.0e-04 | 4243 | 843 | clean (manipulated) |  | False |
| A principal instructs take | Argued for take in public (some round) | sqrt(eps2) | 0.40 | 0.33-0.45 | 0.40 | 1.1e-147 | 5.3e-146 | 5.0e-04 | 72 | 918 | confounded with level / diagnostic (scene text) | stance: marginal | False |
| Pressure level | Any take (at least one took) | /rho/ | 0.39 | 0.35-0.43 | 0.54 | 3.7e-171 | 3.0e-169 | 5.0e-04 | 4243 | 843 | clean (manipulated) |  | False |
| Rule in the pairing (W/D/A) | Reasoning length (words) | sqrt(eps2) | 0.39 | 0.33-0.44 | 350.98 | 5.5e-143 | 2.1e-141 | 5.0e-04 | 4243 | 1412 | clean (manipulated) |  | False |
| Pressure level | Plan said take (of plans with an action) | /rho/ | 0.38 | 0.34-0.43 | 0.51 | 3.0e-106 | 5.3e-105 | 5.0e-04 | 2784 | 525 | clean (manipulated) |  | False |
| Number of principal statements | Agent took | /rho/ | 0.37 | 0.30-0.45 | 0.50 | 2.8e-151 | 1.6e-149 | 5.0e-04 | 72 | 12 | confounded with level / diagnostic (scene text) |  | False |
| Pressure level | Mutual take (both agents took) | /rho/ | 0.37 | 0.33-0.41 | 0.48 | 2.9e-150 | 1.5e-148 | 5.0e-04 | 4243 | 843 | clean (manipulated) |  | False |
| Pairing | Public words sent (agent) | sqrt(eps2) | 0.37 | 0.34-0.40 | 28.01 | 1.1e-121 | 2.8e-120 | 5.0e-04 | 4243 | 702 | clean (manipulated) |  | False |
| Pairing | Public words exchanged (both agents) | sqrt(eps2) | 0.37 | 0.34-0.40 | 56.02 | 1.1e-121 | 2.8e-120 | 5.0e-04 | 4243 | 702 | clean (manipulated) |  | False |
| Number of principal statements | Any take (at least one took) | /rho/ | 0.36 | 0.29-0.44 | 0.50 | 2.9e-143 | 1.2e-141 | 5.0e-04 | 72 | 12 | confounded with level / diagnostic (scene text) |  | False |
| Pairing | Deception-intended flag (agent) | sqrt(eps2) | 0.36 | 0.32-0.40 | 0.45 | 1.9e-119 | 4.4e-118 | 5.0e-04 | 4243 | 702 | clean (manipulated) | marginal; arm-differential | False |
| Pressure level | Argued for take in public (some round) | /rho/ | 0.36 | 0.32-0.40 | 0.44 | 4.2e-139 | 1.5e-137 | 5.0e-04 | 4243 | 843 | clean (manipulated) | stance: marginal | False |
| Designer's welfare-if-take | Plan said take (of plans with an action) | sqrt(eps2) | 0.35 | 0.31-0.40 | 0.38 | 8.0e-77 | 7.3e-76 | 0.013 | 72 | 545 | confounded with level / diagnostic (scene text) |  | False |
| A principal instructs take | Plan said take (of plans with an action) | sqrt(eps2) | 0.35 | 0.28-0.41 | 0.40 | 4.5e-78 | 4.2e-77 | 5.0e-04 | 72 | 594 | confounded with level / diagnostic (scene text) |  | False |
| Number of principal statements | Mutual take (both agents took) | /rho/ | 0.35 | 0.28-0.43 | 0.50 | 1.4e-134 | 4.8e-133 | 0.001 | 72 | 12 | confounded with level / diagnostic (scene text) |  | False |
| Pressure level | Total tokens used | /rho/ | 0.35 | 0.32-0.39 | 1756.53 | 7.7e-133 | 2.4e-131 | 5.0e-04 | 4243 | 843 | clean (manipulated) |  | False |
| Pressure level | Deception-intended flag (agent) | /rho/ | 0.35 | 0.30-0.39 | 0.40 | 1.1e-131 | 3.3e-130 | 5.0e-04 | 4243 | 843 | clean (manipulated) | marginal; arm-differential | False |
| Pairing | Deception-intended flag, either agent | V | 0.35 | 0.31-0.39 | 0.51 | 8.2e-112 | 1.8e-110 | 5.0e-04 | 4243 | 702 | clean (manipulated) | marginal; arm-differential | False |
| Pairing | Plan said take (of plans with an action) | sqrt(eps2) | 0.35 | 0.30-0.39 | 0.48 | 3.4e-71 | 3.0e-70 | 5.0e-04 | 2784 | 290 | clean (manipulated) |  | False |
| Parties misled by refuse | Total tokens used | /rho/ | 0.35 | 0.26-0.42 | 1800.06 | 7.5e-130 | 2.1e-128 | 5.0e-04 | 72 | 178 | confounded with level / diagnostic (scene text) |  | False |
| Pressure level | Deception-intended flag, either agent | /rho/ | 0.35 | 0.31-0.39 | 0.48 | 1.4e-129 | 3.7e-128 | 5.0e-04 | 4243 | 843 | clean (manipulated) | marginal; arm-differential | False |
| Rule in the pairing (W/D/A) | Public words exchanged (both agents) | sqrt(eps2) | 0.34 | 0.31-0.38 | 43.69 | 3.1e-109 | 6.2e-108 | 5.0e-04 | 4243 | 1412 | clean (manipulated) |  | False |

Near-redundant informative outcome pairs (>= 0.8, not by construction): ag_took ~ ag_argued_take (0.85), any_take ~ ag_argued_take (0.84), ag_argued_take ~ ag_deception_intended (0.81). Table: `tables/outcome_pairs.csv`.

## 9. Heat maps

Single-factor heat maps (level, monitoring unpaired view, pairing, diagnostic, setting) are in Appendix A5. Their data are in `tables/dimension_x_metric_*.csv`.

## 10. Two-factor interactions

Method: a ridge-penalised logit (lambda = 1.0). The statistic is the deviance drop of A x B over A + B, minus the extra df. The null comes from **1,000 parametric-bootstrap draws**. Each draw resamples the 72 scenarios with replacement and simulates outcomes from the additive model plus ridge-shrunken scenario offsets, so it carries within-scenario correlation. BH runs across 30 tests, and 4 pass q < .05 (p floor 1/1,001). For scenario-level x scenario-level pairs, the null's scenario offsets absorb the interaction itself, so those p-values are conservative. **Diagnostic x pairing is design-built** (the pack fixes rule-diagnostic matching) and is not a discovery.

**Monitoring x {level, pairing, diagnostic}, reported explicitly:**

| Outcome | Factor A | Factor B | Deviance drop - df | Extra df | p (cluster param. boot) | q | Min cell | Note |
|---|---|---|---|---|---|---|---|---|
| any_take | scenario_diagnostic | monitoring | 1.0 | 2 | 0.22 | 0.67 | 703 | involves a scenario-level factor (descriptive) |
| any_take | level | monitoring | -4.0 | 4 | 0.99 | 0.99 | 419 |  |
| any_take | pairing | monitoring | -4.2 | 5 | 0.96 | 0.99 | 348 |  |
| mutual_take | scenario_diagnostic | monitoring | 0.4 | 2 | 0.27 | 0.73 | 703 | involves a scenario-level factor (descriptive) |
| mutual_take | pairing | monitoring | -2.3 | 5 | 0.62 | 0.88 | 348 |  |
| mutual_take | level | monitoring | -3.0 | 4 | 0.8 | 0.93 | 419 |  |

**All interactions (top 14 by statistic):**

| Outcome | Factor A | Factor B | Deviance drop - df | Extra df | p (cluster param. boot) | q | Min cell | Note |
|---|---|---|---|---|---|---|---|---|
| any_take | scenario_diagnostic | pairing | 200.2 | 10 | 1.0e-03 | 0.0075 | 231 | design-built: whether the pairing's rule matches the scene's diagnostic is fixed by the pack (expected_first_take differs), so this interaction is expected by construction, not a discovery; involves a scenario-level factor (descriptive) |
| mutual_take | scenario_diagnostic | pairing | 180.0 | 10 | 1.0e-03 | 0.0075 | 231 | design-built: whether the pairing's rule matches the scene's diagnostic is fixed by the pack (expected_first_take differs), so this interaction is expected by construction, not a discovery; involves a scenario-level factor (descriptive) |
| any_take | scenario_diagnostic | setting_id | 129.5 | 14 | 0.67 | 0.88 | 174 | scenario-level x scenario-level: the interaction itself lives in the scenario offsets of the null, so p is conservative; only 72 scenes |
| mutual_take | scenario_diagnostic | setting_id | 99.3 | 14 | 0.7 | 0.88 | 174 | scenario-level x scenario-level: the interaction itself lives in the scenario offsets of the null, so p is conservative; only 72 scenes |
| any_take | level | pairing | 95.0 | 20 | 1.0e-03 | 0.0075 | 138 |  |
| mutual_take | level | pairing | 80.2 | 20 | 1.0e-03 | 0.0075 | 138 |  |
| any_take | scenario_diagnostic | level | 23.6 | 8 | 0.019 | 0.095 | 280 | involves a scenario-level factor (descriptive) |
| mutual_take | setting_id | pairing | 18.0 | 35 | 0.019 | 0.095 | 85 | involves a scenario-level factor (descriptive) |
| mutual_take | scenario_diagnostic | level | 15.2 | 8 | 0.029 | 0.11 | 280 | involves a scenario-level factor (descriptive) |
| any_take | setting_id | pairing | 4.6 | 35 | 0.13 | 0.45 | 85 | involves a scenario-level factor (descriptive) |
| any_take | monitoring | endpoint | 3.1 | 2 | 0.026 | 0.11 | 1 | endpoint = collection time (confounded) |
| any_take | scenario_diagnostic | monitoring | 1.0 | 2 | 0.22 | 0.67 | 703 | involves a scenario-level factor (descriptive) |
| any_take | setting_id | level | 0.5 | 28 | 0.57 | 0.88 | 104 | involves a scenario-level factor (descriptive) |
| mutual_take | scenario_diagnostic | monitoring | 0.4 | 2 | 0.27 | 0.73 | 703 | involves a scenario-level factor (descriptive) |

Two-factor heat maps are in Appendix A6.

## 11. Sensitivity

**Failures (primary test), four bounds.** The 77 failed trials (42 watched, 35 unwatched in started cells) are assigned outcomes as follows:

| Failures treated as | Pairs | Watched-only take | Unwatched-only take | Diff (w-u) | 95% lo | 95% hi | p |
|---|---|---|---|---|---|---|---|
| Failures excluded (primary) | 2083 | 49 | 131 | -3.9 pp | -5.2 pp | -2.7 pp | 1.6e-09 |
| Bound 1: every failure = mutual take | 2160 | 83 | 151 | -3.1 pp | -4.5 pp | -1.8 pp | 1.2e-05 |
| Bound 2: every failure = no mutual take | 2160 | 64 | 139 | -3.5 pp | -4.8 pp | -2.2 pp | 2.1e-07 |
| Bound 3 (adversarial): 100% of watched failures = take, 0% of unwatched failures = take | 2160 | 98 | 131 | -1.5 pp | -2.9 pp | -0.2 pp | 0.034 |
| Bound 4 (favourable): 0% of watched failures = take, 100% of unwatched failures = take | 2160 | 49 | 159 | -5.1 pp | -6.4 pp | -3.8 pp | 4.1e-14 |

The result is robust to every failure bound and within the main endpoint. Bound 3 is the adversarial bound. It requires **100% of watched failures and 0% of unwatched failures** to be mutual takes, so it is a bound, not a plausible value. Even with all 42 watched failures counted as takes and all 35 unwatched failures as no take, p stays at or below .05 (p = 0.034). Full curve: `tables/primary_failure_tipping_point.csv`.

`missing_message` failures: 23 watched vs 17 unwatched (1.06% vs 0.79% of started trials; Fisher p = 0.43; as a share of each arm's failures, Fisher p = 0.65). Failure reasons are not outcomes, but an arm imbalance in `missing_message` would make failures informative.

**Heuristic error.** No heuristic-error correction is reported. Rogan-Gladen needs per-arm sensitivity and specificity measured on the same unit as the analysed outcome (agent x episode). Step 1 validation reports only per-arm agreement, per message (stance: agreement watched 30/36, unwatched 28/36; take recall 25/36: arm-error caveat; deception-intended: agreement watched 7/12 vs unwatched 11/12: POTENTIALLY BIASED). The interim divide-by-recall table was mis-specified and has been dropped.

## 12. Caveats in plain terms

- **Final data, one seed.** All planned trials ran. There is one seed per cell and 77 failures, bounded in section 11.
- **Not an independent replication.** The interim snapshot is a subset of these data. The review-driven additions (dose-response, tipping point, cluster-resampled interactions) were specified after the interim results were seen.
- **The notice is text.** "Watched" means the prompt said the episode may be reviewed. Nothing else changed.
- **One model, one temperature, one pack.** Do not pool with other runs.
- **Mutual take is not collusion.** Coordination was not hand-checked.
- **Heuristics.** Stance and deception-intended are marginal and arm-differential, and the other text heuristics are unreliable. None is headlined. Monitoring vocabulary echoes the notices.
- **Clustering.** Only permutation-confirmed results that also survive the single candidate BH family are listed. The asymmetry binomial p ignores clustering.
- **Setting and diagnostic** are scenario-level and differ in content, so they are descriptive only.
- **No communication baseline**, so nothing here is an effect of talking.

## 13. File index

- `PREREG.md`: the pre-registration (the primary is unchanged; post-review additions are disclosed).
- `analyze_full.py` and `analyze_full_workers.py`: the rerunnable script and its process-pool workers (seed 20261025; `--fresh` ignores the permutation cache).
- `provenance.json`: input SHA-256s, arguments, package versions, seeds, settings, runtime and log.
- `figures/` (main text): `03_primary_monitoring_forest.png`, `19_monitoring_by_level.png`, `13_top_relationships.png`, `04_words_vs_actions.png`, `05_asymmetry_mixed_pairs.png`, `06_rule_application.png`. Appendix: `01_design_association.png`, `02_completion_balance.png`, `07_screening_overview.png`, `08_heat_level.png`, `09_heat_monitoring.png`, `10_heat_pairing.png`, `11_heat_diagnostic.png`, `12_heat_setting.png`, `14_univariate_rates.png`, `15_univariate_numeric.png`, `16_outcome_association.png`, `17_2d_heatmaps.png`, `18_scenario_x_level.png`.
- `tables/`: `2d_criterion_x_diagnostic.csv`, `2d_diagnostic_x_level.csv`, `2d_monitoring_x_level.csv`, `2d_pairing_x_diagnostic.csv`, `2d_pairing_x_level.csv`, `2d_scenario_x_level.csv`, `2d_setting_x_diagnostic.csv`, `asymmetry_mixed_pairs.csv`, `candidates.csv`, `candidates_untrustworthy.csv`, `completion_balance.csv`, `deception_intended_decomposition.csv`, `design_associated_pairs.csv`, `design_association_matrix.csv`, `design_cell_counts.csv`, `dimension_x_metric_level.csv`, `dimension_x_metric_monitoring.csv`, `dimension_x_metric_pairing.csv`, `dimension_x_metric_scenario_diagnostic.csv`, `dimension_x_metric_setting_id.csv`, `endpoint_balance.csv`, `failures_by_reason_and_monitoring.csv`, `interactions_ridge_logit.csv`, `monitoring_by_level_diagnostic_pairing.csv`, `monitoring_dose_response_trend.csv`, `outcome_association_matrix.csv`, `outcome_pairs.csv`, `primary_failure_sensitivity.csv`, `primary_failure_tipping_point.csv`, `primary_mcnemar.csv`, `randomisation_levels.csv`, `rule_application_by_relative_level.csv`, `rule_application_expected_first_take.csv`, `rule_application_never_expected.csv`, `screening_overview_effects.csv`, `screening_table.csv`, `subset_membership_by_parameter.csv`, `top_relationships_levels.csv`, `top_relationships_within_strata.csv`, `univariate_summary.csv`, `variable_profile.csv`, `words_vs_actions.csv`, plus `primary_power_and_heterogeneity.json` and `permutation_cache.json`.

## Appendix: supporting figures

**A1. Design association matrix**

![A1. Design association matrix](figures/01_design_association.png)

**A2. Completion balance**

![A2. Completion balance](figures/02_completion_balance.png)

**A3. Univariate rates**

![A3. Univariate rates](figures/14_univariate_rates.png)

**A3. Numeric outcomes**

![A3. Numeric outcomes](figures/15_univariate_numeric.png)

**A4. Screening overview**

![A4. Screening overview](figures/07_screening_overview.png)

**A4. Outcome associations**

![A4. Outcome associations](figures/16_outcome_association.png)

**A5. Heat map: pressure level**

![A5. Heat map: pressure level](figures/08_heat_level.png)

**A5. Heat map: monitoring (unpaired view)**

![A5. Heat map: monitoring (unpaired view)](figures/09_heat_monitoring.png)

**A5. Heat map: pairing**

![A5. Heat map: pairing](figures/10_heat_pairing.png)

**A5. Heat map: diagnostic (descriptive)**

![A5. Heat map: diagnostic (descriptive)](figures/11_heat_diagnostic.png)

**A5. Heat map: setting (descriptive)**

![A5. Heat map: setting (descriptive)](figures/12_heat_setting.png)

**A6. Two-factor heat maps**

![A6. Two-factor heat maps](figures/17_2d_heatmaps.png)

**A6. Scenario x level**

![A6. Scenario x level](figures/18_scenario_x_level.png)

