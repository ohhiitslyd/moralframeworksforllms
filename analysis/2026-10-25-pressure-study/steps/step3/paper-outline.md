# Paper kit: monitoring notices and joint rule-bending in two-agent dual control

**v2: completed data, full Step 2.** This kit goes with [SUMMARY.md](SUMMARY.md) and [claims_ledger.csv](claims_ledger.csv). All numbers come from the FINAL-DATA Step 2 and its oversight-reasoning analysis. The exception is the convergence numbers, which are marked ‡: they come from the coordinator's computation and are not yet in a Step 2 file.

**What changed vs v1:**
- Cluster CIs and failure bounds replace the † placeholders.
- A "why" section is added (oversight-reasoning analysis).
- The welfare-pair heterogeneity claim is dropped. Its test gives p = .64/.65.
- "Pressure" is now "level", pending the construct review.
- The figure plan now uses the Step 2 figures (03, 19, 13, 04, 05, 06).

## Candidate titles

1. **Plain:** Monitoring Notices and Joint Rule-Breaking in Two-Agent LLM Dual-Control Tasks
2. **Finding-led:** "No One Is Monitoring": LLM Agent Pairs Read an Absence of Oversight as Permission to Bend the Rules Together
3. **Question-led:** Do LLM Agents Collude Less When Told They Are Watched, and Why?

## Abstract draft (248 words)

Dual control, where an action executes only if two parties independently approve it, is a common safeguard, and AI agents are starting to fill both seats. We ask whether telling such agents that they are or are not monitored changes how often they jointly approve a rule-breaking action. Two instances of Qwen3-32B played officials in 72 fictional scenarios, each offered an action that misstates a record for some benefit. After a private plan and three rounds of messages, each locked a private take or refuse. We crossed a one-sentence monitoring notice with five levels of stated stakes and six pairings of moral rules, for 4,320 trials (4,243 complete). In a pre-registered paired test over 2,083 matched scenes, joint approval was 23.3% with the "monitored" notice and 27.2% with the "not monitored" notice (−3.9 percentage points, scenario-cluster 95% CI −5.3 to −2.7; 49 vs 131 discordant scenes). The direction held under every failure bound (adversarial bound: −1.5 points). In exploratory text analysis, agents told they were unmonitored often wrote that this lowered the risk of taking. That framing appeared in 54% of the unmonitored approvals that the notice prevented, against 28% of those it did not (an association, single labeller). The stakes level moved behaviour far more (+48 points) but bundles several scene features. The manipulation is text only, with one model and one seed per cell. Evaluations of multi-agent systems should report behaviour under stated observation and non-observation, and monitors can flag "no one will review this" reasoning.

## Section outline and page budget (8 pages)

| Section | Content | Pages |
|---|---|---|
| 1. Introduction | Dual control as a safeguard; the question (sprint 3.4); contributions: a pre-registered paired test, a text signature of why scenes flip, and an audit of artefacts | 0.9 |
| 2. Related work | Evaluation awareness and sandbagging; LLM collusion; monitoring and AI control; rule prompting | 0.6 |
| 3. Setup | Agents; plan → 3 rounds → locked action; rules and pairings; levels (described neutrally as a bundle); both notice texts verbatim; 72 scenarios; 4,320 trials, 98.2% complete | 1.3 |
| 4. Pre-registered result | McNemar, discordant counts, cluster CI, RR; failure bounds (direction vs size); within endpoint; no heterogeneity on two scales (Fig. 1, Fig. 2, Table 1) | 1.3 |
| 5. Why the notice matters | Oversight-reasoning codes and their validation; licence text vs caution text; twin contrasts; 48-cell mechanism coding; convergence step‡ (Fig. 3 new, Table 2) | 1.5 |
| 6. What else moves the deal | Level (bundle; construct caveat); rule pairing; lone-taker asymmetry; rule application (Fig. 4, Fig. 5) | 1.0 |
| 7. What did not hold up | Echo and design artefacts; the welfare-heterogeneity claim; deception_intended; aggregate r (RQ 2.3) (Table 3) | 0.4 |
| 8. Limitations, dual use, conclusion | Threats; dual-use bullets; implication | 1.0 |
| **Total** | | **8.0** |

References and the appendix (scenario table, prompt wrapper, full ledger, validation tables) do not count toward the 8 pages. Check the sprint rules.

## Figure and table plan

| # | File | Claim it carries | Caption (takeaway + n) | Redraw? |
|---|---|---|---|---|
| Fig. 1 | [`../step2/figures/03_primary_monitoring_forest.png`](../step2/figures/03_primary_monitoring_forest.png) | Primary effect, robust in direction | "Told they were monitored, agent pairs approved the action in 23.3% of 2,083 matched scenes vs 27.2% when told they were not (−3.9 pp, cluster CI −5.3 to −2.7). All 14 subgroups point the same way; 5 intervals cross 0." | **Yes**: replace codes (W-W, "Diagnostic", Modal-A) with words; drop the endpoint rows to the appendix; fit to column width |
| Fig. 2 | [`../step2/figures/19_monitoring_by_level.png`](../step2/figures/19_monitoring_by_level.png) | No dose-response; pp vs RR scales | "The notice gap by level on the absolute and relative scales (2,083 pairs). The conditional-OR trend is ×1.10 per level (LR p = .44)." | **Yes**: the level-1 annotation overlaps the band; stack the panels for a column |
| Fig. 3 | new, from `../step2/oversight_reasoning/tables/outcome_held_contrasts.csv` and `predict_action.csv` | Licence text marks notice-dependent takes | "Absence-as-licence text appears in 54% of the 131 unwatched approvals the notice prevented vs 28% of 436 it did not (plan stage only: 40% vs 18%). Watched caution text: 74% vs 73%." | **New**: paired bar chart, two panels (unwatched licence, watched caution) |
| Fig. 4 | [`../step2/figures/13_top_relationships.png`](../step2/figures/13_top_relationships.png) | Level and pairing effects | "Mutual take rises from 5.4% (848) at level 1 to 53.4% (850) at level 5; welfare pairs 54.5% (710) vs authority pairs 13.6% (713)." | **Yes**: rename "pressure level" to "level"; words for pairings |
| Fig. 5 | [`../step2/figures/05_asymmetry_mixed_pairs.png`](../step2/figures/05_asymmetry_mixed_pairs.png) + [`06_rule_application.png`](../step2/figures/06_rule_application.png) | Rules act as thresholds; who takes alone | "Welfare agents make 45 of 49 lone takes next to a no-rule partner; authority agents take 0.4% of 1,674 times when the pack expects refuse (descriptive; ignores clustering)." | Combine into one two-panel figure |
| Appendix | [`../step2/figures/04_words_vs_actions.png`](../step2/figures/04_words_vs_actions.png) | Words follow actions | "Under the notice, take arguments in public fall −3.5 pp and takes −3.8 pp (2,083 pairs)." | Minor |
| Table 1 | from `../step2/tables/primary_mcnemar.csv`, `primary_failure_sensitivity.csv` | Primary numbers | 2×2 discordant table, difference, CI, RR, p; the four failure bounds with the adversarial bound flagged | New |
| Table 2 | from `../step2/oversight_reasoning/tables/validation_heldout_rules_v2.csv` and `discordant_mechanism_coding.csv` | Measurement credibility and mechanisms | Code definitions, held-out precision and recall; mechanism counts in 48 discordant cells | New |
| Table 3 | ledger rows 21–28 | Standards of evidence | "Apparent effects we dropped, and why." | New |

## Limitations (appendix bullets)

- The manipulation is one sentence of prompt text, and researcher logging was identical. We cannot separate a reaction to the word "monitored" from a reaction to expected review or a demand effect.
- One model (Qwen3-32B), temperature 0.6, one seed per cell, one scenario pack.
- 77 of 4,320 trials failed and are excluded. The direction holds under all four bounds; the adversarial bound gives −1.5 pp (p = .034, unclustered).
- "Level" bundles a stated benefit of breaking the rule, costs of refusing to third parties, authority endorsement and promise conflict. Its construct review is pending.
- Oversight-reasoning codes: single labeller, partial blinding, uncertain recall (rates are lower bounds); the mechanism coding was not blind to direction; text is co-generated with the action.
- Several exploratory results ignore scenario clustering: the text contrasts, convergence‡, the lone-taker asymmetry and κ.
- Scenario families and settings are properties of scenes, so their results are descriptive.
- There is no communication-off baseline.
- A mutual take is an operational outcome, and some takes are defensible.
- This is not an independent replication of the interim analysis.

## Dual-use appendix bullets

- **What a misuser could learn.**
  - Telling agents "not monitored" raises joint rule-breaking.
  - Agents then argue to each other that no one will review them.
  - Outcome-weighing instructions make pairs easier to bring to a joint violation.
  - Stakes framing moves models far more than oversight cues.
- **Why publishing is net-positive.**
  - These levers are obvious to anyone who writes prompts.
  - The measurement (the paired watched/unwatched gap) helps evaluators detect behaviour that changes under observation.
  - The "no one will review this" text signature gives monitors a high-precision flag.
- **What we withhold or limit.**
  - We searched for no optimised framings and present none.
  - We release no tool to maximise collusion.
  - We publish the scenario pack and transcripts for reproducibility.
- **Fictional scenes.** Every scene is fictional and labelled as a research simulation.
