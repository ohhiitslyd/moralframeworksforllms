# Paper kit — monitoring notice and joint rule-bending in two-agent dual control

**DRAFT v1 — completed data; full Step 2 pending.** Companion to [SUMMARY.md](SUMMARY.md) and [claims_ledger.csv](claims_ledger.csv). Numbers marked † will be replaced by full Step 2 values (cluster CI, failure sensitivity); numbers marked "71% snapshot" come from the interim analysis.

## Candidate titles

1. **Plain:** Monitoring Notices and Joint Rule-Breaking in Two-Agent LLM Dual-Control Tasks
2. **Finding-led:** "This Episode Is Monitored": A One-Sentence Notice Cuts Joint Rule-Bending by Two LLM Agents, but Stakes Matter Far More
3. **Question-led:** Do LLM Agents Collude Less When Told They Are Watched?

## Abstract draft (239 words)

Dual control, where an action executes only if two parties independently approve it, is a common safeguard, and AI agents are starting to fill both seats. We ask whether telling such agents that they are monitored changes how often they jointly approve a rule-breaking action. Two instances of Qwen3-32B played officials in 72 fictional scenarios, each offered a side deal that misstates a record for some benefit. After a private plan and three rounds of messages, each locked a private take or refuse. We crossed five pressure levels, six pairings of moral rules (welfare, non-deception, authority, or none) and a one-sentence monitoring notice, for 4,320 trials (4,243 complete). In a pre-registered paired test over 2,083 matched scenes, joint takes fell from 27.2% unwatched to 23.3% watched (−3.9 percentage points, 95% CI −5.2 to −2.7; 131 vs 49 discordant scenes, exact McNemar p = 8×10⁻¹⁰), with the same direction in every scenario family. Pressure mattered far more: joint takes rose from 5.4% at the lowest level to 53.4% at the highest. In exploratory analyses, pairs sharing a welfare rule agreed most often (54.5%) and showed the largest notice effect, while authority-rule pairs barely responded; this difference has not yet been tested. The manipulation is text only, with one model and one seed per cell, and robustness to failed trials is still being checked. Behaviour that shifts with stated oversight is a measurable gap that evaluations of multi-agent systems should report.

## Section outline and page budget (8 pages)

| Section | Content | Pages |
|---|---|---|
| 1. Introduction | Dual control as a real safeguard; the question (sprint 3.4): does stated oversight change joint behaviour of agent pairs? Contributions: pre-registered paired test, factorial pack, artefact audit | 0.9 |
| 2. Related work | Evaluation awareness and sandbagging; LLM collusion and steganography; monitoring and AI control; moral-rule prompting | 0.6 |
| 3. Setup | Agents, private plan → 3 message rounds → locked action; rules; pairings; levels; notice text verbatim; 72 scenarios (table in appendix); 4,320 trials, 98.2% complete | 1.4 |
| 4. Pre-registered result | Paired McNemar, discordant counts, CI†, within family and level, failure sensitivity† (Fig. 1, Table 1) | 1.3 |
| 5. What else moves the deal | Pressure dose-response (Fig. 2); rule and pairing (Fig. 3); where the notice bites: welfare pairs (Fig. 4, exploratory); lone takes and rule asymmetry | 1.5 |
| 6. Inside the conversations | Illustrative transcripts: persuasion into the deal; notice used as a reason; content-analysis result if ready (Fig. 5 or Table 2) | 0.8 |
| 7. What did not hold up | Echo and design artefacts we dropped; standards of evidence lesson (RQ 2.3) | 0.4 |
| 8. Limitations, dual use, conclusion | Items from the threats table; dual-use bullets; one-paragraph implication | 1.1 |
| **Total** | | **8.0** |

References and appendix (scenario table, prompt wrapper, full ledger) do not count toward the 8 pages (check the sprint rules).

## Figure and table plan

| # | File | Claim it carries | Caption (takeaway + n) | Redraw? |
|---|---|---|---|---|
| Fig. 1 | new, from `../../tables/scenario-level-pairing-comparisons.csv` (or `../../figures/matched-monitoring-overview.png` meanwhile) | Primary: notice lowers joint deals | "Told they were monitored, agent pairs struck the side deal in 23.3% of 2,083 matched scenes vs 27.2% unwatched; 131 scenes flipped to a deal only when unwatched, 49 only when watched." | **Yes**: the current overview uses codes (W-W) on axes and three panels; for the paper use a discordant-pair bar plus a difference-by-level dot plot with CIs† |
| Fig. 2 | `../../figures/pressure-level-joint-acceptance.png` | Pressure dose-response | "Joint deals rise from 5.4% (46 of 848) at level 1 to 53.4% (454 of 850) at level 5." | Minor: check it is readable at column width; add n under bars |
| Fig. 3 | `../step0.5/figures/2v_level_x_pairing__mutual_take.png` | Rule and pairing effects | "Welfare pairs strike the deal most (up to 89% of 142 at level 5); authority pairs almost never until level 5 (46%). Each cell shows rate and n." | **Yes**: too wide for a column; transpose or shorten pairing labels ("Welfare + welfare" is good, keep words) |
| Fig. 4 | `../../figures/w-average-monitoring.png`, `d-average-monitoring.png`, `a-average-monitoring.png` | Where the notice bites (exploratory) | "The notice lowers joint deals most in welfare pairs (−8.2 pp, 692 cells) and barely in authority pairs (−1.0 pp, 697 cells); exploratory." | **Yes**: combine the three into one small-multiple figure with a shared axis; add CIs† |
| Fig. 5 (optional) | `../step0.5/figures/2v_monitoring_x_diagnostic__mutual_take.png` | Same direction in every scenario family | "Unwatched minus watched joint deals is positive in all three scenario families (n ≈ 706 per cell)." | Maybe: replace "diagnostic" with "scenario family" in the title |
| Table 1 | from primary test | Primary test numbers | Discordant table (both / neither / watched-only / unwatched-only), difference, CI, p, plus failure sensitivity rows† | New table |
| Table 2 | from claims ledger rows 14–19 | Standards of evidence | "Apparent effects we dropped and why (echo, design, bootstrap floor)." | New table |

## Limitations (appendix bullets)

- The manipulation is one sentence of prompt text; researcher logging was identical; we cannot tell reaction to the word "monitored" from reaction to expected review.
- One model (Qwen3-32B), temperature 0.6, one seed per cell, one scenario pack; no transfer claim.
- 77 of 4,320 trials failed and are excluded; the adversarial failure bound is reported as a bound†.
- Scenario families and settings are properties of scenes (24 and 9 scenes per level), not randomised; descriptive only.
- Pressure levels add several scene features at once.
- No communication-off baseline, so no claim about the effect of talking.
- Returned reasoning is generated text, not internal thought; quotes are illustrative.
- A mutual take is an operational outcome; some takes (promise-keeping) are defensible.
- Text metrics echo prompt wording; vocabulary results were dropped.

## Dual-use appendix bullets

- **What a misuser could learn:** that telling agents "not monitored" raises joint rule-breaking a little; that outcome-weighing ("welfare") instructions make agent pairs easier to talk into a joint violation; that stakes framing (jobs, a child's coverage) moves models far more than oversight cues.
- **Why publishing is net-positive:** these levers are already obvious to anyone who can write a prompt; the measurement (a paired watched/unwatched gap) helps evaluators detect behaviour that changes under observation, and the rule comparison helps developers choose safer instructions for agent teams.
- **What we withhold or limit:** we publish the scenario pack and transcripts for reproducibility, but no optimised "jailbreak" framings were searched for and none are presented as such; we do not release a tool to maximise collusion.
- **Fictional scenes:** every scene is fictional and labelled as a research simulation in the prompt.
