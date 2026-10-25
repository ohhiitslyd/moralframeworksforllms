# Paper kit: monitoring notices, claimed authority and joint rule-bending in two-agent dual control

**v3: completed data, full Step 2, plus the construct audit of the level manipulation.** This kit goes with [SUMMARY.md](SUMMARY.md) and [claims_ledger.csv](claims_ledger.csv). Numbers come from three sources: the FINAL-DATA Step 2, its oversight-reasoning analysis, and the independent construct audit ([`../pressure-construct/REPORT.md`](../pressure-construct/REPORT.md)). The exception is the convergence numbers, which are marked ‡: they come from the coordinator's computation and are not yet in a Step 2 file.

## What changed vs v2

- **"Level" is now the "justification level (J1–J5)"** everywhere, including the titles and abstract. It means cumulative stated reasons to take: an escalating third-party cost of refusing, capped by a superior's endorsement in most scenes. The construct audit showed that it is not pressure, stakes or temptation.
- **The abstract's level sentence is replaced** by the decomposition. At J5, mutual take is 60.5% with a take-instructing superior vs 24.6% without one. Authority-rule agents: 0 of 1,109 without a superior.
- **Section 6 is rewritten** around obedience vs third-party cost. A short methods paragraph on the construct audit is added to section 3.
- **Figure plan.** Fig. 4 is now the audit's split-by-superior curve (fig 2), and the family × superior figure (audit fig 7) is added as Fig. 5. Both need their "Pressure level" axis relabelled.
- **New limitation:** construct validity of the level factor. **New dual-use bullet:** claimed authority.
- **Unchanged:** the monitoring primary. It is paired within cell, so both arms see identical justification text.

## What changed vs v1 (kept for the record)

- Cluster CIs and failure bounds replace the † placeholders.
- A "why" section is added (oversight-reasoning analysis).
- The welfare-pair heterogeneity claim is dropped. Its test gives p = .64/.65.
- The figure plan uses the Step 2 figures (03, 19, 04, 05, 06).

## Candidate titles

1. **Plain:** Monitoring Notices, Claimed Authority and Joint Rule-Breaking in Two-Agent LLM Dual-Control Tasks
2. **Finding-led:** "No One Is Monitoring" and "The Director Says Sign": What Moves LLM Agent Pairs to Bend the Rules Together
3. **Question-led:** Do LLM Agents Collude Less When Told They Are Watched, and More When Told a Superior Approves?

## Abstract draft (247 words)

Dual control, where an action executes only if two parties independently approve it, is a common safeguard, and AI agents are starting to fill both seats. We ask whether telling such agents that they are or are not monitored changes how often they jointly approve a rule-breaking action. Two instances of Qwen3-32B played officials in 72 fictional scenarios. After a private plan and three rounds of messages, each locked a private take or refuse. We crossed a one-sentence monitoring notice with five cumulative justification levels and six pairings of moral rules (4,243 of 4,320 trials complete). In a pre-registered paired test over 2,083 matched scenes, joint approval was 23.3% under "monitored" and 27.2% under "not monitored" (−3.9 percentage points, scenario-cluster 95% CI −5.3 to −2.7). The direction held under every failure bound. In exploratory text analysis, unmonitored agents often treated the absence of review as permission, in 54% of the approvals the notice prevented vs 28% of the rest (single labeller). An audit of the justification ladder found a larger lever, obedience. At the top level, joint approval was 60.5% when a named superior instructed taking vs 24.6% when none did, and authority-rule agents never jointly approved without such an instruction (0 of 1,109; exploratory, as superiors were not randomised). Both manipulations are text only, with one model and one seed per cell. Multi-agent evaluations should report behaviour under stated observation and non-observation, and control protocols should treat claimed authority inside a task as an attack surface.

## Section outline and page budget (8 pages)

| Section | Content | Pages |
|---|---|---|
| 1. Introduction | Dual control as a safeguard; the question (sprint 3.4); contributions: a pre-registered paired test, a text signature of why scenes flip, the obedience-vs-stakes decomposition, and an audit of artefacts (including our own mislabelled factor) | 0.9 |
| 2. Related work | Evaluation awareness and sandbagging; LLM collusion; monitoring and AI control; instruction hierarchy (Wallace et al. 2024) and sycophancy; "pressure" in LLM deception work (Scheurer et al. 2023), and why our factor is not that; obedience and prosocial rule-breaking (Milgram; Morrison 2006); justified ethicality (Shalvi et al. 2011) | 0.7 |
| 3. Setup | Agents; plan → 3 rounds → locked action; rules and pairings; both notice texts verbatim; 72 scenarios; 4,320 trials, 98.2% complete. **Justification level** described as built (cumulative sentences 1..k, 8 → 56 words; ingredient shares by rung), with one paragraph on the construct audit and the single-coder note | 1.3 |
| 4. Pre-registered result | McNemar, discordant counts, cluster CI, RR; failure bounds (direction vs size); within endpoint; no heterogeneity on two scales; why the construct verdict does not touch it (paired within cell) (Fig. 1, Fig. 2, Table 1) | 1.2 |
| 5. Why the notice matters | Oversight-reasoning codes and their validation; licence text vs caution text; twin contrasts; 48-cell mechanism coding; convergence step‡ (Fig. 3 new, Table 2) | 1.4 |
| 6. What moves the deal: obedience vs third-party cost | Bundle effect (+48.4 pp) shown only next to the split by superior yes/no; authority-rule agents 0 of 1,109 without a superior; pure-stakes scenes 1% → 25%; step effects by ingredient; step-shaped scene curves; rule pairing and lone-taker asymmetry (Fig. 4, Fig. 5, Fig. 6) | 1.2 |
| 7. What did not hold up | "Collude more under pressure", temptation framing, single-variable dose-response, r = 0.975, level effects independent of length or label; echo and design artefacts; the welfare-heterogeneity claim; deception_intended (RQ 2.3) (Table 3) | 0.4 |
| 8. Limitations, dual use, conclusion | Threats; dual-use bullets; implication for AI control | 0.9 |
| **Total** | | **8.0** |

References and the appendix (scenario table, prompt wrapper, full ledger, validation tables, audit coding dictionary) do not count toward the 8 pages. Check the sprint rules.

## Figure and table plan

| # | File | Claim it carries | Caption (takeaway + n) | Redraw? |
|---|---|---|---|---|
| Fig. 1 | [`../step2/figures/03_primary_monitoring_forest.png`](../step2/figures/03_primary_monitoring_forest.png) | Primary effect, robust in direction | "Told they were monitored, agent pairs approved the action in 23.3% of 2,083 matched scenes vs 27.2% when told they were not (−3.9 pp, cluster CI −5.3 to −2.7). All 14 subgroups point the same way; 5 intervals cross 0." | **Yes**: replace codes (W-W, "Diagnostic", Modal-A, "pressure level") with words; drop the endpoint rows to the appendix; fit to column width |
| Fig. 2 | [`../step2/figures/19_monitoring_by_level.png`](../step2/figures/19_monitoring_by_level.png) | No dose-response across justification levels; pp vs RR scales | "The notice gap by justification level on the absolute and relative scales (2,083 pairs). The conditional-OR trend is ×1.10 per level (LR p = .44)." | **Yes**: the J1 annotation overlaps the band; stack the panels for a column; relabel the axis |
| Fig. 3 | new, from `../step2/oversight_reasoning/tables/outcome_held_contrasts.csv` and `predict_action.csv` | Licence text marks notice-dependent takes | "Absence-as-licence text appears in 54% of the 131 unwatched approvals the notice prevented vs 28% of 436 it did not (plan stage only: 40% vs 18%). Watched caution text: 74% vs 73%." | **New**: paired bar chart, two panels (unwatched licence, watched caution) |
| Fig. 4 | [`../pressure-construct/figures/fig2_take_by_level_split.png`](../pressure-construct/figures/fig2_take_by_level_split.png) | The justification curve is mostly the superior's rung | "Holding the justification level fixed, mutual take is 24.6% without a take-instructing superior (167 trials) vs 60.5% with one (683) at J5. Without a superior the curve plateaus near 25% from J4. Right panel: split by coded third-party harm of refusing." | **Yes**: the axis says "Pressure level"; relabel it "justification level (J1–J5)". Consider dropping the right panel (single-coder severity) to the appendix |
| Fig. 5 | [`../pressure-construct/figures/fig7_family_by_principal.png`](../pressure-construct/figures/fig7_family_by_principal.png) | Three mechanisms: welfare agents follow stakes, authority agents only obey, honesty agents move with promises and superiors | "Authority-rule agents never produce a mutual take without a take-instructing superior (0 of 1,109 trials) and do 57–75% of the time with one. Welfare-rule agents rise without a superior (9% → 54% by J4). Trial counts per point." | **Yes**: relabel "Pressure level" and "honesty" to match the paper's terms ("non-deception"); fix the overlapping n labels at J3 in the welfare panel |
| Fig. 6 | [`../step2/figures/05_asymmetry_mixed_pairs.png`](../step2/figures/05_asymmetry_mixed_pairs.png) + [`06_rule_application.png`](../step2/figures/06_rule_application.png) | Rules act as thresholds; who takes alone | "Welfare agents make 45 of 49 lone takes next to a no-rule partner; authority agents take 0.4% of 1,674 times when the pack expects refuse (descriptive; ignores clustering)." | Combine into one two-panel figure (or move to the appendix if space is short) |
| Appendix | [`../pressure-construct/figures/fig1_ingredients_by_level.png`](../pressure-construct/figures/fig1_ingredients_by_level.png), [`fig4_transition_by_ingredient.png`](../pressure-construct/figures/fig4_transition_by_ingredient.png), [`fig6_prompt_length.png`](../pressure-construct/figures/fig6_prompt_length.png) | What the ladder contains; step effects; the length confound | "Share of 72 scenes containing each ingredient by justification level"; "Mean change in mutual take by the added sentence's ingredient (288 steps)"; "Prompt length vs level (r = 0.91)." | Relabel axes |
| Appendix | [`../step2/figures/04_words_vs_actions.png`](../step2/figures/04_words_vs_actions.png) | Words follow actions | "Under the notice, take arguments in public fall −3.5 pp and takes −3.8 pp (2,083 pairs)." | Minor |
| Table 1 | from `../step2/tables/primary_mcnemar.csv`, `primary_failure_sensitivity.csv` | Primary numbers | 2×2 discordant table, difference, CI, RR, p; the four failure bounds with the adversarial bound flagged | New |
| Table 2 | from `../step2/oversight_reasoning/tables/validation_heldout_rules_v2.csv` and `discordant_mechanism_coding.csv` | Measurement credibility and mechanisms | Code definitions, held-out precision and recall; mechanism counts in 48 discordant cells | New |
| Table 3 | ledger rows 23–34 | Standards of evidence | "Apparent effects we dropped, and why", led by the five claims the construct audit rules out. | New |
| Table 4 (optional) | from `../pressure-construct/tables/within_level_contrasts.csv`, `transition_effect_by_dominant_ingredient.csv` | Decomposition numbers | Superior yes/no at J3–J5 with n; step effects by ingredient with the number of steps | New |

## Limitations (appendix bullets)

- The monitoring manipulation is one sentence of prompt text, and researcher logging was identical. We cannot separate a reaction to the word "monitored" from a reaction to expected review or a demand effect.
- One model (Qwen3-32B), temperature 0.6, one seed per cell, one scenario pack.
- 77 of 4,320 trials failed and are excluded. The direction holds under all four bounds; the adversarial bound gives −1.5 pp (p = .034, unclustered).
- **Construct validity of the level factor.** The factor the pack called "pressure" is a cumulative justification ladder. Several things move together across levels, and the data cannot separate them:
  - a superior's take instruction, mostly at J5;
  - the designers' welfare label (J ≥ 3);
  - prompt length (r = 0.91);
  - escalating third-party harm.
  The same rung is a different stimulus in each family. The superior contrast is within level but not randomised, and the ingredient codes come from a single coder. The paired monitoring result is unaffected.
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
  - A line claiming that a superior instructs the act moves agent pairs to joint rule-breaking far more than stakes do. Agents told to obey the highest-ranking principal follow it almost deterministically.
  - Outcome-weighing instructions make pairs easier to bring to a joint violation.
- **Why publishing is net-positive.**
  - Claimed-authority injection and "nobody is watching" framings are already obvious to anyone who writes prompts.
  - The measurements (the paired watched/unwatched gap, the superior yes/no split) help evaluators and control researchers quantify these risks.
  - The "no one will review this" and "the principal's order takes precedence" text signatures give monitors concrete flags.
- **What we withhold or limit.**
  - We searched for no optimised framings and present none.
  - We release no tool to maximise collusion.
  - We publish the scenario pack and transcripts for reproducibility.
- **Fictional scenes.** Every scene is fictional and labelled as a research simulation.
