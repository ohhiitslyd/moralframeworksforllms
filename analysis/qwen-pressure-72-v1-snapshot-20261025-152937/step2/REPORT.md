# E1 interim snapshot: Step 2 analysis report (PRELIMINARY)

**PRELIMINARY.** Interim snapshot of the extended pressure run (`qwen-pressure-72-v1-snapshot-20261025-152937`), cut off 2026-10-25 15:29 UTC: 3,026 of 4,320 planned trials complete, 60 failed, 1,234 not started. No effect size here is final. Pre-registration: [PREREG.md](PREREG.md). Plan: [../ANALYSIS-PLAN.md](../ANALYSIS-PLAN.md) (Revision 1). Script: `analyze_e1.py`.

**Audience:** the team and hackathon judges (AI safety researchers). Model: Qwen3-32B, temperature 0.6, one seed per cell, two agents, three simultaneous message rounds, then a locked take/refuse decision.

**Words used here.** *Mutual take* = both agents' locked final action was take (an operational outcome; in some scenes taking is arguably justified, so it is not "collusion"). *Watched / unwatched* = which text notice the agents saw; researcher logging was identical, so this is a notice, not real oversight. Reasoning traces are generated text, not evidence of internal states.

## 1. Summary (PRELIMINARY)

- **Primary (pre-registered, sprint 3.4).** In the 1,046 cells where both the watched and the unwatched trial are complete, the mutual-take rate was 25.0% with the watched notice and 29.3% with the unwatched notice: a paired difference of **-4.2 pp** (95% Newcombe CI -6.0 pp to -2.4 pp; scenario-cluster bootstrap -5.8 pp to -2.6 pp). Discordant pairs: 24 watched-only vs 68 unwatched-only take; McNemar p = 7.4e-06 (exact 4.9e-06). The direction matches the pre-registered expectation. The minimum detectable effect is 2.6 pp now (1.8 pp at full completion), so the observed effect is above it but not by much.
- **Robustness.** It holds within the main endpoint (both trials on Modal-B: -4.5 pp, 16 vs 50, p = 4.9e-05, 756 pairs) and has the same sign in every diagnostic, pairing and level (heterogeneity p: diagnostic 0.24, pairing 0.79, level 0.46). It survives treating all 60 failures as takes or as non-takes, but **not** the adversarial worst case (failed watched = take, failed unwatched = no take: -1.4 pp, p = 0.2).
- **Words vs. actions (secondary).** With the watched notice, the agent take rate changed by -4.3 pp, and lone takes did not change (-0.3 pp). In public messages, watched agents used more monitoring words (+5.1 pp), more deception words (+5.3 pp) and longer messages (+6.1 words). In private text, monitoring mentions were *lower* when watched (-6.5 pp): unwatched agents paraphrase "no oversight". The pattern is "a slightly smaller deal, talked about more openly", not "sanitised talk, same deal". Pressure level, by contrast, moves actions by about +54.1 pp (level 5 vs 1).
- **Top exploratory candidates** (BH-corrected, cluster-aware; all exploratory): see section 5 and `tables/candidates.csv`.
  1. Watched notice -> fewer mutual takes (PRIMARY, paired McNemar): paired diff -4.2 pp (95% CI -6.0 pp to -2.4 pp); n = 1,046.
  2. Watched notice: Mentions monitoring, private (private reasoning, paired): paired diff -6.5 pp (95% CI -9.5 pp to -3.3 pp); n = 1,046.
  3. Level 5 vs 1: Mutual take (actions, paired): paired diff +51.5 pp (95% CI +43.9 pp to +58.6 pp); n = 427.
  4. Level 5 vs 1: Agent took (actions, paired): paired diff +54.1 pp (95% CI +47.0 pp to +61.1 pp); n = 427.
  5. Pairing -> Reasoning length (words): sqrt(eps2) 0.43 (cluster CI 0.38-0.48, p_perm 5.0e-04); n = 3,026.
  6. Pack's expected_first_take predicts whether rule agents take (authority sharp, welfare / non-deception early): kappa 0.62; n = 4,549.
  7. Pairing -> Mutual take (both agents took): V 0.33 (cluster CI 0.29-0.37, p_perm 5.0e-04); n = 3,026.
  8. Welfare + no-rule pairs: lone takes by the rule agent 32 vs the no-rule agent 4: rule agent's share of lone takes 88.9% (Wilson 0.75-0.96); n = 36.
- **Design check.** Completion is balanced across every manipulated factor (smallest BH q = 0.081). Monitoring, level and pairing are cleanly crossed. Endpoint is collection time and is not associated with the deal rate. Setting and diagnostic effects are descriptive: they are scenario-level, with only 9 or 24 scenes per level, and the scenes differ in content.

## 2. How to read the charts

- **Effect sizes** are on comparable 0-1 scales: bias-corrected Cramér's V (categorical parameter x binary outcome), sqrt(epsilon^2) = correlation ratio on ranks (categorical x numeric or agent-rate outcome), |Spearman rho| (ordinal / numeric parameter). Roughly: 0.1 small, 0.3 medium, 0.5 large. *Raw spread* is the max-min difference in rates (or medians) across levels.
- **n.** Pair outcomes count episodes (one per trial). Agent outcomes pool agents A and B (two per episode); in screening they are averaged per episode first, so the unit is still the episode. Every heat-map cell prints its value and n.
- **Intervals.** Wilson only for independent episodes. Rates pooled over agents or scenarios use a scenario-cluster bootstrap (resampling the 72 scenarios). Paired effects use Newcombe's paired score interval plus a scenario-cluster bootstrap.
- **Tests.** Screening p-values are asymptotic (chi-square / Fisher / Kruskal-Wallis / Spearman) and ignore clustering; BH-q < .05 survivors are then **confirmed** with a sequential Besag-Clifford permutation at the parameter's randomisation level (scenario-level parameters: whole scenarios permuted, effective n = 72; level / pairing / endpoint: permuted within scenario; monitoring: swapped within cell). Up to 1,999 shuffles, stopping after 50 exceedances; floor 1/2,000. ● = confirmed, ○ = BH only.
- **Colour.** Single-hue blue sequential scale for rates and effect sizes, absolute (0-100% or 0-0.6), never normalised per column. Hatching = confounded parameter or by-construction pair. Grey cells = n < 5. * = marginal heuristic, † = unreliable heuristic.

## 3. Design check and completion

![Parameter association matrix](figures/01_design_association.png)

**Clean comparisons.** Monitoring, level and pairing are fully crossed within every scenario (association with every other design parameter ~0). **Aliased by construction:** pairing / rule-in-pairing / matched-vs-mixed (coarsenings of pairing), diagnostic = family. **Strongly associated pairs** (association >= 0.3, started trials; cell counts in `tables/design_cell_counts.csv`):

| Parameter | Parameter | Association |
|---|---|---|
| pairing | pairing_rule | 1.00 |
| pairing | matched_vs_mixed | 1.00 |
| take_is_justified_ambiguous | refuse_breaks_promise | 0.96 |
| scenario_diagnostic | refuse_deceives_n | 0.87 |
| level | welfare_if_take_designer | 0.86 |
| scenario_diagnostic | refuse_breaks_promise | 0.83 |
| take_principal_present | n_principals | 0.83 |
| scenario_diagnostic | take_is_justified_ambiguous | 0.80 |
| refuse_deceives_n | refuse_breaks_promise | 0.76 |
| soft_take_principal_present | n_principals | 0.74 |
| take_is_justified_ambiguous | refuse_deceives_n | 0.72 |
| endpoint | start_rank | 0.63 |
| rank_stated_in_level_text | n_principals | 0.62 |
| level | take_principal_present | 0.61 |
| take_principal_present | rank_stated_in_level_text | 0.58 |
| level | n_principals | 0.56 |

Reading: the scene-text features (principal instructs take, rank stated, number of principals, welfare-if-take) are written into the level text, so they move with pressure level and with diagnostic. Their effects cannot be separated from level or diagnostic; they are hatched in every chart. Endpoint, start rank and import status are collection-time variables (Modal-A ran first and holds all 134 imported episodes).

![Completion balance](figures/02_completion_balance.png)

**Completion by monitoring arm** (all 4,320 planned trials):

| Arm | Complete | Failed | Not started |
|---|---|---|---|
| unwatched | 1525 | 27 | 608 |
| watched | 1501 | 33 | 626 |

Completion status (complete / failed / not started) is not associated with any design parameter after BH correction (smallest q = 0.081; `tables/completion_balance.csv`). Failures by reason and arm: `tables/failures_by_reason_and_monitoring.csv`. Among started trials, endpoint is balanced over monitoring, level, pairing, diagnostic and setting (`tables/endpoint_balance.csv`); the exception is the 24-scene pilot slice, over-represented on Modal-A because the imported earlier-batch episodes came from it (q = 8.4e-06; trial-level test, optimistic). Endpoint itself is not associated with the deal rate (26.2% on Modal-A vs 26.0% on Modal-B, 481 vs 2545 trials).

**Post-treatment subsets.** Plan-based outcomes exist only for agents whose plan states an action (about 44%). The membership tests are in `tables/subset_membership_by_parameter.csv`; where membership depends on the parameter, the subset outcome is flagged in the screening table and not used as a finding.

## 4. Primary test: monitoring notice and mutual take (pre-registered)

![Primary forest plot](figures/03_primary_monitoring_forest.png)

- **Test:** McNemar on 1,046 complete cell pairs (both trials complete; status == complete only). Discordant pairs: **24 watched-only take vs 68 unwatched-only take**; concordant: 238 both take, 716 neither.
- **Effect:** -4.21 pp (watched 25.0% vs unwatched 29.3%); Newcombe 95% CI -6.00 pp to -2.43 pp; scenario-cluster bootstrap -5.80 pp to -2.62 pp. Conditional odds ratio (watched vs unwatched, discordant pairs) 0.36.
- **p:** chi-square with continuity correction 7.4e-06; exact binomial 4.9e-06. alpha = .05, two-sided.
- **Power:** discordance rate 8.8%. Minimum detectable paired difference at 80% power: 2.6 pp now (1,046 pairs), 1.8 pp at full completion (2,160 pairs). An unpaired comparison would need 4.5 pp now.
- **Within endpoint** (endpoint = collection time): both trials on Modal-B -4.5 pp (16 vs 50, p = 4.9e-05, 756 pairs); both on Modal-A -9.4 pp (0 vs 3, 32 pairs); **258 pairs ran across both endpoints** -2.7 pp (8 vs 15). Endpoint x monitoring (Fisher on the discordant split, both-A vs both-B): p = 1. No sign of an endpoint-specific effect, but Modal-A has very few pairs.
- **Within factors:** same direction in all 3 diagnostics, 6 pairings and 5 levels; no heterogeneity test is significant (diagnostic p = 0.24, pairing 0.79, level 0.46, matched/mixed 0.4). The effect is mostly carried by welfare and non-deception scenes and welfare pairings.
- **Related binary outcomes (same paired test, not confirmatory):** any take -4.5 pp (41 vs 88); lone take -0.3 pp (43 vs 46, p = 0.83). The notice reduces takes overall; it does not convert mutual takes into lone takes.

<details><summary>Full subgroup table</summary>

| Subset | Pairs | Watched-only take | Unwatched-only take | Rate watched | Rate unwatched | Diff | 95% lo | 95% hi | p |
|---|---|---|---|---|---|---|---|---|---|
| All complete pairs (PRIMARY) | 1046 | 24 | 68 | 25.0% | 29.3% | -4.2 pp | -6.0 pp | -2.4 pp | 7.4e-06 |
| Endpoint: both Modal-A | 32 | 0 | 3 | 21.9% | 31.2% | -9.4 pp | -20.5 pp | +1.1 pp | 0.25 |
| Endpoint: both Modal-B | 756 | 16 | 50 | 24.1% | 28.6% | -4.5 pp | -6.6 pp | -2.4 pp | 4.9e-05 |
| Endpoint: split | 258 | 8 | 15 | 28.3% | 31.0% | -2.7 pp | -6.4 pp | +0.9 pp | 0.21 |
| Split: watched on Modal-A, unwatched on Modal-B | 139 | 3 | 8 | 28.8% | 32.4% | -3.6 pp | -8.3 pp | +1.1 pp | 0.23 |
| Split: watched on Modal-B, unwatched on Modal-A | 119 | 5 | 7 | 27.7% | 29.4% | -1.7 pp | -7.5 pp | +4.1 pp | 0.77 |
| Diagnostic: welfare | 343 | 4 | 23 | 11.7% | 17.2% | -5.5 pp | -8.6 pp | -2.7 pp | 5.3e-04 |
| Diagnostic: nondeception | 346 | 11 | 28 | 35.0% | 39.9% | -4.9 pp | -8.4 pp | -1.4 pp | 0.01 |
| Diagnostic: authority | 357 | 9 | 17 | 28.3% | 30.5% | -2.2 pp | -5.1 pp | +0.6 pp | 0.17 |
| Pairing: W-W | 191 | 7 | 20 | 51.3% | 58.1% | -6.8 pp | -12.0 pp | -1.6 pp | 0.021 |
| Pairing: W-none | 194 | 6 | 22 | 30.9% | 39.2% | -8.2 pp | -13.4 pp | -3.0 pp | 0.0046 |
| Pairing: D-D | 172 | 5 | 7 | 16.9% | 18.0% | -1.2 pp | -5.3 pp | +3.0 pp | 0.77 |
| Pairing: D-none | 169 | 4 | 10 | 17.8% | 21.3% | -3.6 pp | -8.1 pp | +0.8 pp | 0.18 |
| Pairing: A-A | 173 | 1 | 3 | 13.9% | 15.0% | -1.2 pp | -4.0 pp | +1.5 pp | 0.62 |
| Pairing: A-none | 147 | 1 | 6 | 14.3% | 17.7% | -3.4 pp | -7.4 pp | +0.3 pp | 0.12 |
| Level: 1 | 206 | 2 | 6 | 3.9% | 5.8% | -1.9 pp | -5.3 pp | +1.0 pp | 0.29 |
| Level: 2 | 199 | 5 | 9 | 13.6% | 15.6% | -2.0 pp | -6.0 pp | +1.8 pp | 0.42 |
| Level: 3 | 212 | 2 | 16 | 21.7% | 28.3% | -6.6 pp | -10.6 pp | -2.8 pp | 0.0013 |
| Level: 4 | 216 | 7 | 13 | 33.3% | 36.1% | -2.8 pp | -6.8 pp | +1.3 pp | 0.26 |
| Level: 5 | 213 | 8 | 24 | 51.2% | 58.7% | -7.5 pp | -12.5 pp | -2.4 pp | 0.008 |
| Pair type: matched | 536 | 13 | 30 | 28.2% | 31.3% | -3.2 pp | -5.6 pp | -0.8 pp | 0.015 |
| Pair type: mixed | 510 | 11 | 38 | 21.8% | 27.1% | -5.3 pp | -8.0 pp | -2.6 pp | 2.0e-04 |
| Outcome: any take (>=1 agent) | 1046 | 41 | 88 | 31.0% | 35.5% | -4.5 pp | -6.6 pp | -2.4 pp | 5.1e-05 |
| Outcome: lone take | 1046 | 43 | 46 | 5.9% | 6.2% | -0.3 pp | -2.1 pp | +1.5 pp | 0.83 |

</details>

## 5. Top-ranked relationships

Candidates are scored on effect size, robustness (BH survival, permutation confirmation, clean design, no sign reversal, cell sizes), relevance to the sprint questions and surprise relative to the directions written in PREREG.md. Everything except the primary test is **exploratory**. Full list: `tables/candidates.csv`.

| Rank | Candidate | Source | Effect (interval) | n | Research question | Caveat |
|---|---|---|---|---|---|---|
| 1 | Watched notice -> fewer mutual takes (PRIMARY, paired McNemar) | primary McNemar | paired diff -4.2 pp (95% CI -6.0 pp to -2.4 pp) | 1,046 | 3.4 monitoring | pre-registered; interim; notice-only manipulation; one model / seed |
| 2 | Watched notice: Mentions monitoring, private (private reasoning, paired) | words vs actions (paired) | paired diff -6.5 pp (95% CI -9.5 pp to -3.3 pp) | 1,046 | 2.2 words+actions x 3.4 |  |
| 3 | Level 5 vs 1: Public words sent (public messages, paired) | words vs actions (paired) | paired diff +22.5 (19.379 to 25.739) | 427 | 2.2 words+actions x 1.1 level |  |
| 4 | Level 5 vs 1: Argued for take (stance heuristic) (public messages, paired) | words vs actions (paired) | paired diff +45.6 pp (95% CI +39.1 pp to +51.6 pp) | 427 | 2.2 words+actions x 1.1 level |  |
| 5 | Level 5 vs 1: Mutual take (actions, paired) | words vs actions (paired) | paired diff +51.5 pp (95% CI +43.9 pp to +58.6 pp) | 427 | 2.2 words+actions x 1.1 level |  |
| 6 | Level 5 vs 1: Mentions monitoring, private (private reasoning, paired) | words vs actions (paired) | paired diff -33.5 pp (95% CI -38.6 pp to -28.1 pp) | 427 | 2.2 words+actions x 1.1 level |  |
| 7 | Level 5 vs 1: Agent took (actions, paired) | words vs actions (paired) | paired diff +54.1 pp (95% CI +47.0 pp to +61.1 pp) | 427 | 2.2 words+actions x 1.1 level |  |
| 8 | Pairing -> Reasoning length (words) | screening | sqrt(eps2) 0.43 (cluster CI 0.38-0.48, p_perm 5.0e-04) | 3,026 | 1.1 pairing |  |
| 9 | Watched notice: Mentions monitoring, public (public messages, paired) | words vs actions (paired) | paired diff +5.1 pp (95% CI +3.3 pp to +6.8 pp) | 1,046 | 2.2 words+actions x 3.4 |  |
| 10 | Pack's expected_first_take predicts whether rule agents take (authority sharp, welfare / non-deception early) | rule application | kappa 0.62 | 4,549 | 1.1 criterion | agents clustered in scenarios; no formal test |
| 11 | Pairing -> Mutual take (both agents took) | screening | V 0.33 (cluster CI 0.29-0.37, p_perm 5.0e-04) | 3,026 | 1.1 pairing |  |
| 12 | Pressure level -> Any take (at least one took) | screening | /rho/ 0.41 (cluster CI 0.36-0.44, p_perm 5.0e-04) | 3,026 | 1.1 level |  |
| 13 | Welfare + no-rule pairs: lone takes by the rule agent 32 vs the no-rule agent 4 | asymmetry (mixed pairs) | rule agent's share of lone takes 88.9% (Wilson 0.75-0.96) | 36 | 1.1 criterion / pairing | binomial p ignores scenario clustering (optimistic); small n |
| 14 | Watched notice: Public words sent (public messages, paired) | words vs actions (paired) | paired diff +6.1 (4.256 to 8.029) | 1,046 | 2.2 words+actions x 3.4 |  |
| 15 | Pairing -> Agent took | screening | sqrt(eps2) 0.30 (cluster CI 0.27-0.35, p_perm 5.0e-04) | 3,026 | 1.1 pairing |  |

![Top relationships](figures/13_top_relationships.png)

Within-stratum checks for these (by diagnostic, endpoint and monitoring arm): `tables/top_relationships_within_strata.csv`.

**Looks large but untrustworthy** (`tables/candidates_untrustworthy.csv`):

| Looks large but untrustworthy | Measure | Effect | Why |
|---|---|---|---|
| Level 5 vs 1: Deception words per 1k reasoning words (private reasoning, paired) | paired diff | -2.048 | private deception words mostly echo the prompt's honesty notes |
| Pairing -> Total tokens used | sqrt(eps2) | +0.571 | token totals include prompt tokens, which differ by design |
| Rule in the pairing (W/D/A) -> Total tokens used | sqrt(eps2) | +0.548 | token totals include prompt tokens, which differ by design; coarsening of pairing (aliased with pairing) |
| Pairing -> Deception words in private notes | sqrt(eps2) | +0.531 | private deception words mostly echo the prompt's honesty notes |
| Rule in the pairing (W/D/A) -> Deception words in private notes | sqrt(eps2) | +0.511 | private deception words mostly echo the prompt's honesty notes; coarsening of pairing (aliased with pairing) |
| A principal instructs take -> Agent took | sqrt(eps2) | +0.430 | confounded with level / diagnostic (scene text) |
| A principal instructs take -> Any take (at least one took) | V | +0.420 | confounded with level / diagnostic (scene text) |
| Level 5 vs 1: Deception-intended flag (private reasoning, paired) | paired diff | +0.418 | deception-intended flag is nearly 'took or planned take' (prompt states who taking misleads) |
| A principal instructs take -> Mutual take (both agents took) | V | +0.410 | confounded with level / diagnostic (scene text) |
| Rule in the pairing (W/D/A) -> Reasoning length (words) | sqrt(eps2) | +0.393 | coarsening of pairing (aliased with pairing) |
| A principal instructs take -> Argued for take in public (some round) | sqrt(eps2) | +0.381 | confounded with level / diagnostic (scene text) |
| Number of principal statements -> Agent took | /rho/ | +0.366 | confounded with level / diagnostic (scene text); min cell n=8 |

## 6. Words vs. actions (secondary, sprint 2.2 x 3.4)

![Words vs actions](figures/04_words_vs_actions.png)

Each row is a paired within-cell difference (monitoring: the watched and unwatched trial of the same scenario x level x pairing; level: level 5 vs level 1 of the same scenario x pairing x arm). Agent measures are averaged per episode. Vocabulary counts are the Step 1 **notice-masked** counts: the notice text, its echo phrases and monitoring keywords are blanked before counting. This pack has **no `_novel` splits** for deception words, so private deception vocabulary still contains paraphrases of the prompt's honesty notes ("take would mislead ..."); it is shown but not headlined. Per-arm heuristic accuracy is attached; rows whose heuristic error differs between arms are greyed and exploratory only.

**Monitoring (watched - unwatched):**

| Channel | Measure | Pairs | Arm A -> arm B | Paired diff | 95% cluster CI | q | Heuristic / per-arm accuracy |
|---|---|---|---|---|---|---|---|
| Actions | Mutual take | 1046 | 29.3% -> 25.0% | -4.2 pp | -5.7 to -2.7 pp | 4.5e-04 |  |
| Actions | Agent took | 1046 | 32.4% -> 28.0% | -4.3 pp | -6.1 to -2.6 pp | 4.5e-04 |  |
| Actions | Lone take | 1046 | 6.2% -> 5.9% | -0.3 pp | -2.0 to +1.4 pp | 0.88 |  |
| Public messages | Argued for take (stance heuristic) | 1046 | 32.5% -> 28.1% | -4.3 pp | -6.3 to -2.4 pp | 4.5e-04 | agreement watched 30/36, unwatched 28/36; take recall 25/36: arm-error caveat |
| Public messages | Deception words, public | 1046 | 19.5% -> 24.7% | +5.3 pp | +3.1 to +7.3 pp | 4.5e-04 | deterministic |
| Public messages | Mentions monitoring, public | 1046 | 2.8% -> 7.9% | +5.1 pp | +3.3 to +6.8 pp | 4.5e-04 | match precision watched 10/10, unwatched 8/10 |
| Public messages | Agreement phrases, public | 1046 | 66.9% -> 71.2% | +4.3 pp | +0.4 to +8.1 pp | 0.016 | deterministic |
| Public messages | Public words sent | 1046 | 60.0 -> 66.1 | +6.1 | +4.3 to +8.0 | 4.5e-04 | deterministic |
| Private reasoning | Plan states an action | 1046 | 45.0% -> 43.1% | -1.9 pp | -4.2 to +0.5 pp | 0.21 | deterministic |
| Private reasoning | Deception words, private notes | 1046 | 64.5% -> 68.0% | +3.5 pp | +1.4 to +5.6 pp | 8.0e-04 | deterministic |
| Private reasoning | Deception words, reasoning | 1046 | 95.1% -> 97.0% | +1.9 pp | +0.9 to +2.9 pp | 4.5e-04 | deterministic |
| Private reasoning | Deception words per 1k reasoning words | 1046 | 7.5 -> 7.7 | +0.1 | -0.1 to +0.3 | 0.18 | deterministic |
| Private reasoning | Mentions monitoring, private | 1046 | 74.7% -> 68.3% | -6.5 pp | -9.5 to -3.3 pp | 4.5e-04 | match precision watched 10/10, unwatched 8/10 |
| Private reasoning | Mentions evaluator / score (decision) | 1046 | 1.4% -> 1.5% | +0.0 pp | -0.2 to +0.3 pp | 1 | deterministic |
| Private reasoning | Take-linked deception sentence | 1046 | 91.8% -> 93.9% | +2.1 pp | +0.8 to +3.4 pp | 0.0026 | part of deception_intended |
| Private reasoning | Deception-intended flag | 1046 | 30.8% -> 27.8% | -3.0 pp | -5.2 to -0.7 pp | 0.0039 | agreement watched 7/12 vs unwatched 11/12; recall 5/9 vs 6/7: POTENTIALLY BIASED |
| Private reasoning | Deception-intended flag, among takers | 283 | 82.5% -> 88.7% | +6.2 pp | +2.9 to +9.3 pp | 0.0022 | agreement watched 7/12 vs unwatched 11/12; recall 5/9 vs 6/7: POTENTIALLY BIASED |
| Private reasoning | Reasoning length (words) | 1046 | 1930.0 -> 1893.2 | -36.9 | -69.1 to -10.3 | 0.012 | deterministic |

**Pressure (level 5 - level 1):**

| Channel | Measure | Pairs | Arm A -> arm B | Paired diff | 95% cluster CI | q | Heuristic / per-arm accuracy |
|---|---|---|---|---|---|---|---|
| Actions | Mutual take | 427 | 4.0% -> 55.5% | +51.5 pp | +43.9 to +58.6 pp | 3.6e-04 |  |
| Actions | Agent took | 427 | 5.7% -> 59.8% | +54.1 pp | +47.0 to +61.1 pp | 3.6e-04 |  |
| Actions | Lone take | 427 | 3.5% -> 8.7% | +5.2 pp | +2.0 to +8.1 pp | 0.0019 |  |
| Public messages | Argued for take (stance heuristic) | 427 | 9.1% -> 54.7% | +45.6 pp | +39.1 to +51.6 pp | 3.6e-04 | agreement watched 30/36, unwatched 28/36; take recall 25/36: arm-error caveat |
| Public messages | Deception words, public | 427 | 20.4% -> 20.7% | +0.4 pp | -4.5 to +4.9 pp | 0.91 | deterministic |
| Public messages | Mentions monitoring, public | 427 | 5.2% -> 2.8% | -2.3 pp | -4.4 to -0.1 pp | 0.07 | match precision watched 10/10, unwatched 8/10 |
| Public messages | Agreement phrases, public | 427 | 64.2% -> 75.4% | +11.2 pp | +5.6 to +17.1 pp | 6.5e-04 | deterministic |
| Public messages | Public words sent | 427 | 50.6 -> 73.1 | +22.5 | +19.4 to +25.7 | 3.6e-04 | deterministic |
| Private reasoning | Plan states an action | 427 | 42.4% -> 45.0% | +2.6 pp | -1.9 to +7.4 pp | 0.33 | deterministic |
| Private reasoning | Deception words, private notes | 427 | 73.7% -> 58.1% | -15.6 pp | -19.3 to -11.7 pp | 3.6e-04 | deterministic |
| Private reasoning | Deception words, reasoning | 427 | 99.1% -> 90.5% | -8.5 pp | -11.7 to -5.6 pp | 3.6e-04 | deterministic |
| Private reasoning | Deception words per 1k reasoning words | 427 | 8.7 -> 6.6 | -2.0 | -2.3 to -1.8 | 3.6e-04 | deterministic |
| Private reasoning | Mentions monitoring, private | 427 | 87.7% -> 54.2% | -33.5 pp | -38.6 to -28.1 pp | 3.6e-04 | match precision watched 10/10, unwatched 8/10 |
| Private reasoning | Mentions evaluator / score (decision) | 427 | 1.8% -> 0.8% | -0.9 pp | -2.4 to +0.0 pp | 0.079 | deterministic |
| Private reasoning | Take-linked deception sentence | 427 | 98.1% -> 84.2% | -13.9 pp | -18.0 to -10.3 pp | 3.6e-04 | part of deception_intended |
| Private reasoning | Deception-intended flag | 427 | 8.3% -> 50.1% | +41.8 pp | +35.6 to +48.0 pp | 3.6e-04 | agreement watched 7/12 vs unwatched 11/12; recall 5/9 vs 6/7: POTENTIALLY BIASED |
| Private reasoning | Deception-intended flag, among takers | 31 | 100.0% -> 74.2% | -25.8 pp | -42.9 to -8.7 pp | 0.0018 | agreement watched 7/12 vs unwatched 11/12; recall 5/9 vs 6/7: POTENTIALLY BIASED |
| Private reasoning | Reasoning length (words) | 427 | 1877.7 -> 1885.6 | +7.9 | -46.1 to +64.2 | 0.78 | deterministic |

**Reading.** Actions: the notice lowers takes by about 4 pp; pressure raises them by about 50 pp. Public messages: watched agents write longer messages that mention monitoring and deception words more often. Private text: unwatched agents mention monitoring *more* (they reason about "no oversight"), and the share of plans that state an action does not change with the notice. So the notice changes what agents say in public at least as much as what they do, but it does **not** produce "sanitised talk, same deal": takes go down while public talk about deception goes up.

**Deception-intended flag (do not use for the monitoring contrast).** Step 1 validation: agreement watched 7/12 vs unwatched 11/12; recall 5/9 vs 6/7, so watched positives are undercounted. Decomposition P(flag) = P(take) x P(flag | take):

| Arm | Agents | Takers | P(take) | P(flag) | P(flag | take) |
|---|---|---|---|---|---|
| unwatched | 3050 | 950 | 31.1% | 30.3% | 85.3% |
| watched | 3002 | 817 | 27.2% | 26.6% | 87.5% |

The flag is close to "took or planned take" (the prompt itself states who taking misleads), so its arm difference is mostly the take difference; the within-taker difference is smaller than the measurement-error gap (section 11).

**Asymmetry in mixed pairs (who takes alone).** Derived from action_a / action_b with criterion_a / criterion_b (agent A holds the rule):

| Rule in pair | Episodes | Lone takes | Rule agent alone | No-rule agent alone | Share by rule agent | Wilson lo | Wilson hi | Binomial p |
|---|---|---|---|---|---|---|---|---|
| welfare | 530 | 36 | 32 | 4 | 88.9% | 74.7% | 95.6% | 1.9e-06 |
| nondeception | 496 | 50 | 30 | 20 | 60.0% | 46.2% | 72.4% | 0.2 |
| authority | 477 | 54 | 14 | 40 | 25.9% | 16.1% | 38.9% | 5.4e-04 |
| all | 1503 | 140 | 76 | 64 | 54.3% | 46.0% | 62.3% | 0.35 |

![Asymmetry](figures/05_asymmetry_mixed_pairs.png)

Welfare agents take alone against a no-rule partner; with an authority rule, it is the no-rule partner who takes alone. Binomial p treats episodes as independent (optimistic; episodes cluster in scenarios).

**Rule application vs. the pack's expected_first_take** (rule agents only):

| Rule | Expected take at this level? | Agents | Took | Rate | 95% lo (cluster) | 95% hi |
|---|---|---|---|---|---|---|
| welfare | 0 | 612 | 117 | 19.1% | 13.0% | 25.7% |
| welfare | 1 | 966 | 669 | 69.3% | 62.4% | 76.0% |
| nondeception | 0 | 1167 | 136 | 11.7% | 7.5% | 15.9% |
| nondeception | 1 | 327 | 214 | 65.4% | 50.0% | 79.3% |
| authority | 0 | 1153 | 3 | 0.3% | 0.0% | 0.6% |
| authority | 1 | 324 | 230 | 71.0% | 58.3% | 81.3% |
| all | 0 | 2932 | 256 | 8.7% | 6.0% | 11.7% |
| all | 1 | 1617 | 1113 | 68.8% | 62.2% | 75.6% |

Cohen's kappa between "level >= expected first-take level" and "agent took": welfare 0.48, non-deception 0.52, authority 0.79, all 0.62.

![Rule application](figures/06_rule_application.png)

## 7. Univariate results

![Univariate rates](figures/14_univariate_rates.png)

![Numeric outcomes](figures/15_univariate_numeric.png)

Full table (every parameter and outcome: type, n, missing, summary, interval): `tables/univariate_summary.csv`; variable profile with missingness and level counts: `tables/variable_profile.csv`. Note: private deception words appear in 95.8% of agents' reasoning, which reflects echo of the honesty notes, not spontaneous deception talk.

## 8. Matrices

![Screening overview](figures/07_screening_overview.png)

Screening: 567 parameter x outcome pairs; 319 pass BH q < .05 and 222 are confirmed by the cluster-aware permutation. No parameter is computed from an outcome, so no pair was removed as by-construction before counting m. Top rows (full table `tables/screening_table.csv`):

| Parameter | Outcome | Measure | Effect | 95% cluster CI | Raw spread | p (asym.) | q (BH) | p (perm.) | Eff. n | Min cell | Design | Heuristic | Simpson flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Pairing | Total tokens used | sqrt(eps2) | 0.57 | 0.54-0.61 | 2885.84 | 1.1e-210 | 6.1e-208 | 5.0e-04 | 3026 | 477 | clean (manipulated) |  | False |
| Rule in the pairing (W/D/A) | Total tokens used | sqrt(eps2) | 0.55 | 0.51-0.59 | 2215.33 | 6.5e-198 | 1.8e-195 | 5.0e-04 | 3026 | 977 | clean (manipulated) |  | False |
| Pairing | Deception words in private notes | sqrt(eps2) | 0.53 | 0.50-0.58 | 0.64 | 5.6e-182 | 1.1e-179 | 5.0e-04 | 3026 | 477 | clean (manipulated) |  | False |
| Rule in the pairing (W/D/A) | Deception words in private notes | sqrt(eps2) | 0.51 | 0.48-0.55 | 0.50 | 2.9e-172 | 4.2e-170 | 5.0e-04 | 3026 | 977 | clean (manipulated) |  | False |
| Pairing | Reasoning length (words) | sqrt(eps2) | 0.43 | 0.38-0.48 | 446.58 | 7.3e-119 | 5.2e-117 | 5.0e-04 | 3026 | 477 | clean (manipulated) |  | False |
| A principal instructs take | Agent took | sqrt(eps2) | 0.43 | 0.37-0.48 | 0.46 | 7.4e-124 | 6.0e-122 | 5.0e-04 | 72 | 661 | confounded with level / diagnostic (scene text) |  | False |
| A principal instructs take | Any take (at least one took) | V | 0.42 | 0.36-0.47 | 0.48 | 3.4e-112 | 1.9e-110 | 5.0e-04 | 72 | 661 | confounded with level / diagnostic (scene text) |  | False |
| Pressure level | Agent took | /rho/ | 0.41 | 0.36-0.45 | 0.52 | 2.2e-135 | 2.5e-133 | 5.0e-04 | 3026 | 597 | clean (manipulated) |  | False |
| A principal instructs take | Mutual take (both agents took) | V | 0.41 | 0.34-0.47 | 0.44 | 2.9e-102 | 1.4e-100 | 5.0e-04 | 72 | 661 | confounded with level / diagnostic (scene text) |  | False |
| Pressure level | Any take (at least one took) | /rho/ | 0.41 | 0.36-0.44 | 0.55 | 4.5e-131 | 4.3e-129 | 5.0e-04 | 3026 | 597 | clean (manipulated) |  | False |
| Rule in the pairing (W/D/A) | Reasoning length (words) | sqrt(eps2) | 0.39 | 0.34-0.44 | 350.13 | 5.5e-102 | 2.4e-100 | 5.0e-04 | 3026 | 977 | clean (manipulated) |  | False |
| Pairing | Public words exchanged (both agents) | sqrt(eps2) | 0.38 | 0.35-0.42 | 57.48 | 2.9e-93 | 7.9e-92 | 5.0e-04 | 3026 | 477 | clean (manipulated) |  | False |
| Pairing | Public words sent (agent) | sqrt(eps2) | 0.38 | 0.35-0.42 | 28.74 | 2.9e-93 | 7.9e-92 | 5.0e-04 | 3026 | 477 | clean (manipulated) |  | False |
| Pressure level | Mutual take (both agents took) | /rho/ | 0.38 | 0.34-0.42 | 0.49 | 2.7e-114 | 1.7e-112 | 5.0e-04 | 3026 | 597 | clean (manipulated) |  | False |
| A principal instructs take | Argued for take in public (some round) | sqrt(eps2) | 0.38 | 0.32-0.43 | 0.39 | 2.0e-97 | 6.2e-96 | 5.0e-04 | 72 | 661 | confounded with level / diagnostic (scene text) | stance: marginal | False |
| Pressure level | Plan said take (of plans with an action) | /rho/ | 0.38 | 0.34-0.42 | 0.51 | 5.3e-74 | 8.9e-73 | 5.0e-04 | 2007 | 372 | clean (manipulated) |  | False |
| Number of principal statements | Agent took | /rho/ | 0.37 | 0.29-0.43 | 0.56 | 1.7e-103 | 8.9e-102 | 0.0015 | 72 | 8 | confounded with level / diagnostic (scene text) |  | False |
| Pairing | Deception-intended flag (agent) | sqrt(eps2) | 0.37 | 0.34-0.41 | 0.45 | 4.5e-85 | 1.1e-83 | 5.0e-04 | 3026 | 477 | clean (manipulated) | marginal; arm-differential | False |
| Pressure level | Deception-intended flag (agent) | /rho/ | 0.36 | 0.31-0.41 | 0.41 | 1.2e-100 | 5.0e-99 | 5.0e-04 | 3026 | 597 | clean (manipulated) | marginal; arm-differential | False |
| Pressure level | Argued for take in public (some round) | /rho/ | 0.36 | 0.32-0.41 | 0.43 | 1.0e-99 | 3.9e-98 | 5.0e-04 | 3026 | 597 | clean (manipulated) | stance: marginal | False |
| Pressure level | Deception-intended flag, either agent | /rho/ | 0.36 | 0.32-0.40 | 0.49 | 1.2e-98 | 4.1e-97 | 5.0e-04 | 3026 | 597 | clean (manipulated) | marginal; arm-differential | False |
| Designer's welfare-if-take | Plan said take (of plans with an action) | sqrt(eps2) | 0.36 | 0.31-0.41 | 0.39 | 2.5e-56 | 2.4e-55 | 0.019 | 72 | 382 | confounded with level / diagnostic (scene text) |  | False |
| Rule in the pairing (W/D/A) | Public words exchanged (both agents) | sqrt(eps2) | 0.36 | 0.33-0.39 | 45.15 | 1.8e-84 | 4.0e-83 | 5.0e-04 | 3026 | 977 | clean (manipulated) |  | False |
| Rule in the pairing (W/D/A) | Public words sent (agent) | sqrt(eps2) | 0.36 | 0.33-0.39 | 22.58 | 1.8e-84 | 4.0e-83 | 5.0e-04 | 3026 | 977 | clean (manipulated) |  | False |
| Number of principal statements | Any take (at least one took) | /rho/ | 0.36 | 0.28-0.42 | 0.60 | 7.6e-98 | 2.5e-96 | 0.0025 | 72 | 8 | confounded with level / diagnostic (scene text) |  | False |
| Pairing | Plan said take (of plans with an action) | sqrt(eps2) | 0.36 | 0.32-0.40 | 0.49 | 1.0e-52 | 9.4e-52 | 5.0e-04 | 2007 | 200 | clean (manipulated) |  | False |
| Pairing | Deception-intended flag, either agent | V | 0.35 | 0.33-0.39 | 0.50 | 4.1e-80 | 8.1e-79 | 5.0e-04 | 3026 | 477 | clean (manipulated) | marginal; arm-differential | False |
| Designer's welfare-if-take | Agent took | sqrt(eps2) | 0.35 | 0.31-0.40 | 0.35 | 2.7e-81 | 5.6e-80 | 0.058 | 72 | 579 | confounded with level / diagnostic (scene text) |  | False |
| Number of principal statements | Mutual take (both agents took) | /rho/ | 0.35 | 0.27-0.42 | 0.53 | 1.1e-93 | 3.4e-92 | 0.0025 | 72 | 8 | confounded with level / diagnostic (scene text) |  | False |
| Designer's welfare-if-take | Any take (at least one took) | V | 0.35 | 0.30-0.40 | 0.37 | 4.0e-80 | 8.1e-79 | 0.053 | 72 | 579 | confounded with level / diagnostic (scene text) |  | False |

![Outcome associations](figures/16_outcome_association.png)

By-construction pairs (hatched) are not findings: the take outcomes, the deception-intended flag (built on take) and the stance-derived agreement outcomes. Near-redundant informative pairs (>= 0.8, not by construction): ag_took ~ ag_argued_take (0.85), any_take ~ ag_argued_take (0.83), ag_argued_take ~ ag_deception_intended (0.82), plans_agree ~ ag_flipped (0.81). Table: `tables/outcome_pairs.csv`.

## 9. Heat maps

**Pressure level (clean, manipulated within scenario).** Data: `tables/dimension_x_metric_*.csv`.

![Pressure level (clean, manipulated within scenario).](figures/08_heat_level.png)

**Monitoring notice (unpaired view; the paired test is section 4).** Data: `tables/dimension_x_metric_*.csv`.

![Monitoring notice (unpaired view; the paired test is section 4).](figures/09_heat_monitoring.png)

**Pairing (clean).** Data: `tables/dimension_x_metric_*.csv`.

![Pairing (clean).](figures/10_heat_pairing.png)

**Diagnostic (scenario-level; descriptive).** Data: `tables/dimension_x_metric_*.csv`.

![Diagnostic (scenario-level; descriptive).](figures/11_heat_diagnostic.png)

**Social setting (scenario-level; descriptive).** Data: `tables/dimension_x_metric_*.csv`.

![Social setting (scenario-level; descriptive).](figures/12_heat_setting.png)

## 10. Two-factor interactions

Ridge-penalised logit (lambda = 1.0); statistic = deviance drop of A x B over A + B minus the extra degrees of freedom; null from 100 parametric-bootstrap draws of the additive fit; BH across 30 tests. 8 pass q < .05. Scenario-level x scenario-level pairs (setting x diagnostic) are optimistic because the bootstrap ignores scenario clustering; pairs with endpoint are confounded with collection time.

| Outcome | Factor A | Factor B | Deviance drop - df | Extra df | p (param. boot) | q | Min cell | Note |
|---|---|---|---|---|---|---|---|---|
| any_take | scenario_diagnostic | pairing | 145.3 | 10 | 0.0099 | 0.037 | 156 | involves a scenario-level factor: p somewhat optimistic |
| mutual_take | scenario_diagnostic | pairing | 133.6 | 10 | 0.0099 | 0.037 | 156 | involves a scenario-level factor: p somewhat optimistic |
| any_take | scenario_diagnostic | setting_id | 109.5 | 14 | 0.0099 | 0.037 | 116 | scenario-level x scenario-level: parametric bootstrap ignores scenario clustering (optimistic) |
| mutual_take | scenario_diagnostic | setting_id | 81.5 | 14 | 0.0099 | 0.037 | 116 | scenario-level x scenario-level: parametric bootstrap ignores scenario clustering (optimistic) |
| any_take | level | pairing | 65.6 | 20 | 0.0099 | 0.037 | 83 |  |
| mutual_take | level | pairing | 54.3 | 20 | 0.0099 | 0.037 | 83 |  |
| mutual_take | setting_id | pairing | 21.0 | 35 | 0.0099 | 0.037 | 54 | involves a scenario-level factor: p somewhat optimistic |
| any_take | scenario_diagnostic | level | 16.6 | 8 | 0.0099 | 0.037 | 195 | involves a scenario-level factor: p somewhat optimistic |
| mutual_take | setting_id | level | 12.8 | 28 | 0.03 | 0.081 | 63 | involves a scenario-level factor: p somewhat optimistic |
| any_take | setting_id | pairing | 12.4 | 35 | 0.05 | 0.11 | 54 | involves a scenario-level factor: p somewhat optimistic |
| mutual_take | scenario_diagnostic | level | 12.3 | 8 | 0.02 | 0.059 | 195 | involves a scenario-level factor: p somewhat optimistic |
| any_take | setting_id | level | 12.1 | 28 | 0.02 | 0.059 | 63 | involves a scenario-level factor: p somewhat optimistic |

![2D heat maps](figures/17_2d_heatmaps.png)

![Scenario by level](figures/18_scenario_x_level.png)

## 11. Sensitivity

**Failures (primary test).** Each of the 60 failed trials counted as each outcome in turn:

| Failures treated as | Pairs | Watched-only take | Unwatched-only take | Diff (w-u) | 95% lo | 95% hi | p |
|---|---|---|---|---|---|---|---|
| Failures excluded (primary) | 1046 | 24 | 68 | -4.2 pp | -6.0 pp | -2.4 pp | 7.4e-06 |
| All failures = mutual take | 1086 | 45 | 76 | -2.9 pp | -4.8 pp | -0.9 pp | 0.0064 |
| All failures = no mutual take | 1086 | 32 | 71 | -3.6 pp | -5.4 pp | -1.8 pp | 1.8e-04 |
| Against hypothesis: failed watched = take, failed unwatched = no take | 1086 | 53 | 68 | -1.4 pp | -3.4 pp | +0.6 pp | 0.2 |
| For hypothesis: failed watched = no take, failed unwatched = take | 1086 | 24 | 79 | -5.1 pp | -6.9 pp | -3.3 pp | 1.0e-07 |

The effect survives failures as all-take or all-no-take and the favourable split; under the adversarial split (every failed watched trial a mutual take and every failed unwatched trial not) the interval includes zero. That scenario requires the 33 watched failures to be takes at about 4x the base rate, so it is a bound, not a likely value.

**Heuristic error that differs by arm.** Corrected difference = observed / recall per arm, for a range of assumed recall gaps:

| Heuristic | Assumed recall gap (watched lower) | Observed diff (w-u) | Implied watched | Implied unwatched | Corrected diff (w-u) | Note |
|---|---|---|---|---|---|---|
| deception_intended (among takers) | +0.00 | +2.3 pp | 102.1% | 99.5% | +2.6 pp | implied rate > 100% = impossible: the flag is saturated among takers |
| deception_intended (among takers) | +0.05 | +2.3 pp | 108.4% | 99.5% | +9.0 pp | implied rate > 100% = impossible: the flag is saturated among takers |
| deception_intended (among takers) | +0.10 | +2.3 pp | 115.6% | 99.5% | +16.1 pp | implied rate > 100% = impossible: the flag is saturated among takers |
| deception_intended (among takers) | +0.20 | +2.3 pp | 133.2% | 99.5% | +33.7 pp | implied rate > 100% = impossible: the flag is saturated among takers |
| deception_intended (among takers) | +0.30 | +2.3 pp | 157.1% | 99.5% | +57.6 pp | implied rate > 100% = impossible: the flag is saturated among takers |
| public take stance (argued take) | +0.20 | -4.3 pp | 56.8% | 46.7% | +10.1 pp |  |
| public take stance (argued take) | +0.05 | -4.3 pp | 43.6% | 46.7% | -3.1 pp |  |
| public take stance (argued take) | -0.00 | -4.3 pp | 40.5% | 46.7% | -6.3 pp |  |
| public take stance (argued take) | -0.05 | -4.3 pp | 37.8% | 46.7% | -9.0 pp |  |
| public take stance (argued take) | -0.20 | -4.3 pp | 31.4% | 46.7% | -15.3 pp |  |

**Deception-intended among takers:** the observed rates (about 85-88%) are already near the ceiling, so even a 5 pp lower watched recall implies a watched rate above 100%. The validation gap (recall 5/9 watched vs 6/7 unwatched, about 30 pp) makes the within-taker contrast uninterpretable. **Public take stance:** the watched - unwatched difference stays negative for a +/-5 pp arm gap in take recall (-3.1 pp to -9.0 pp; the observed agreement gap is 83% vs 78%) but can flip sign for a 20 pp gap (+10.1 pp to -15.3 pp). It is exploratory only.

## 12. Caveats in plain terms

- **Interim.** 30% of trials have not run; one seed per cell. Every number will move.
- **The notice is text.** "Watched" means the prompt said the episode may be reviewed; nothing else changed.
- **One model, one temperature, one pack.** Qwen3-32B at 0.6; do not pool with the v1 run.
- **Mutual take is not collusion.** In several scenes taking is arguably the justified option; coordination was not hand-checked here.
- **Heuristics.** Stance is marginal (undercounts take); deception-intended is marginal and arm-differential; said/did, peer deception, lone-take awareness, plan stance and euphemism gap are unreliable. None is headlined.
- **Echo.** Private deception vocabulary largely paraphrases the honesty notes; masked counts remove the notice, not the honesty notes.
- **Clustering.** Asymptotic screening p-values ignore scenario clustering; only permutation-confirmed results are listed as candidates. Some intervals for agent pools treat agents within an episode as separate (noted where used).
- **Setting and diagnostic** are scenario-level with 9 / 24 scenes per level and different content: descriptive only.
- **No communication baseline**, so nothing here is an effect of talking.

## 13. File index

- `PREREG.md`: pre-registration (written before outcome-by-condition numbers).
- `analyze_e1.py`: the single rerunnable script (seed 20261025; `--fresh` ignores the permutation cache).
- `provenance.json`: input SHA-256s, package versions, settings, seeds, runtime, CPU affinity, log.
- `figures/`: `01_design_association.png`, `02_completion_balance.png`, `03_primary_monitoring_forest.png`, `04_words_vs_actions.png`, `05_asymmetry_mixed_pairs.png`, `06_rule_application.png`, `07_screening_overview.png`, `08_heat_level.png`, `09_heat_monitoring.png`, `10_heat_pairing.png`, `11_heat_diagnostic.png`, `12_heat_setting.png`, `13_top_relationships.png`, `14_univariate_rates.png`, `15_univariate_numeric.png`, `16_outcome_association.png`, `17_2d_heatmaps.png`, `18_scenario_x_level.png`.
- `tables/`: `2d_criterion_x_diagnostic.csv`, `2d_diagnostic_x_level.csv`, `2d_monitoring_x_level.csv`, `2d_pairing_x_diagnostic.csv`, `2d_pairing_x_level.csv`, `2d_scenario_x_level.csv`, `2d_setting_x_diagnostic.csv`, `asymmetry_mixed_pairs.csv`, `candidates.csv`, `candidates_untrustworthy.csv`, `completion_balance.csv`, `deception_intended_decomposition.csv`, `design_associated_pairs.csv`, `design_association_matrix.csv`, `design_cell_counts.csv`, `dimension_x_metric_level.csv`, `dimension_x_metric_monitoring.csv`, `dimension_x_metric_pairing.csv`, `dimension_x_metric_scenario_diagnostic.csv`, `dimension_x_metric_setting_id.csv`, `endpoint_balance.csv`, `failures_by_reason_and_monitoring.csv`, `interactions_ridge_logit.csv`, `outcome_association_matrix.csv`, `outcome_pairs.csv`, `primary_failure_sensitivity.csv`, `primary_mcnemar.csv`, `rule_application_by_relative_level.csv`, `rule_application_expected_first_take.csv`, `rule_application_never_expected.csv`, `screening_overview_effects.csv`, `screening_table.csv`, `sensitivity_heuristic_error.csv`, `subset_membership_by_parameter.csv`, `top_relationships_levels.csv`, `top_relationships_within_strata.csv`, `univariate_summary.csv`, `variable_profile.csv`, `words_vs_actions.csv`, plus `primary_power_and_heterogeneity.json` and `permutation_cache.json`.
