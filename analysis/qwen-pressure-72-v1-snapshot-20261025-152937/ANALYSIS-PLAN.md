# Preliminary analysis plan: extended pressure run (snapshot 2026-10-25 15:29 UTC)

**Data:** `results/qwen-pressure-72-v1-snapshot-20261025-152937`, from branch `experiment-harness-pilot-results`. **Preliminary:** collection is still running.

**Status at cutoff:** 4,320 trials planned. 3,026 are complete (787 mutual take, 193 unilateral take, 2,046 both refuse), 60 failed and 1,234 have not started, so 71% have reached an end state.

**Process:** prompt library Step 1 ([`per-trial-metrics.md`](../../prompt-library/analysis/per-trial-metrics.md)) and Step 2 ([`parameter-outcome-report.md`](../../prompt-library/analysis/parameter-outcome-report.md)), following [`analysis-pipeline/PROCESS.md`](../../analysis-pipeline/PROCESS.md).

## Design of this run, from the manifest and README

| Factor | Levels |
|---|---|
| Scenario | 72: 3 per diagnostic × 8 settings |
| Setting | hospital, religious, military, school, volunteer, social_club, family, situational |
| Diagnostic (scenario family) | welfare, nondeception, authority |
| Pressure level | 1–5 |
| Pairing | W-W, W-none, D-D, D-none, A-A, A-none |
| Monitoring notice | watched, unwatched. This is the notice shown to agents; researcher logging is identical in both. |
| Seed | 1 (one per cell) |

**Fixed settings:** Qwen3-32B, temperature 0.6, max tokens 4,096, three peer exchanges. Execution order was shuffled with seed 20261025.

**Known differences from the v1 run:**
- the rules are worded differently
- the take/refuse wording is "action", "authorize" and "record take"
- there are new report keys
- there are two Modal endpoints serving the same model ID

## Questions this analysis should answer

1. **Is the completed subset representative?** Compare completion status against setting, diagnostic, level, pairing, monitoring and endpoint. A shuffled order predicts no association.
2. **Monitoring (sprint question 3.4):** does a "watched" vs. "unwatched" notice change collusion, lone takes, deception vocabulary, euphemism, and saying one thing while doing another? Check this overall and within diagnostic and pairing.
3. **Setting:** does the social setting change collusion once diagnostic and level are held fixed?
4. **Diagnostic and criterion:** do the v1 patterns replicate under the new rule wording?
   - Rules are applied according to the labels in the prompt.
   - Pressure works as a dose-response.
   - The partner effect: a no-rule agent with an authority partner.
5. **Interaction dynamics:** do plans still decide the outcome, how often do agents persuade each other into or out of the deal, and what is the gap between public and private language?

## Cautions to carry into every finding

- **The results are preliminary.** About 29% of cells are missing, and each condition has a single seed.
- **The heuristics were validated on v1 text.** They must be re-validated on this run before derived metrics are trusted.
- **Endpoint is a candidate confound** and goes in the design check.
- **Don't pool this run with the v1 run.** The rules, scenarios and endpoints differ.
- **"Mutual take" is an operational outcome,** not causally established collusion. In some scenarios, taking is the justified option.

## Deliverables (in this folder)

- **`step1/`:**
  - `trial_metrics.csv`
  - `trial_metrics_dictionary.md` + `.html`
  - `metrics_schema.json`
  - `build_metrics_e1.py`
  - `VALIDATION.md` (heuristic re-validation on this run's transcripts)
- **`step2/`:**
  - `REPORT.md` + `.html`
  - `figures/`
  - `tables/` (including `candidates.csv`)
  - `analyze_e1.py`
- **`SUMMARY.md` + `.html`:** preliminary findings for a newcomer.

Every step is reviewed by a fresh subagent before the next step uses its output.

## Revision 1: after the plan review (this section takes precedence)

**Primary pre-specified test (sprint 3.4)**
- **What it tests:** the monitoring effect on mutual take, as a **paired within-cell comparison**. Each scenario × level × pairing cell has one watched and one unwatched trial.
- **Test:** McNemar's test on the cells where both trials are complete.
- **Minimum detectable effect** (80% power, α = .05): about 2.6 pp now, and about 1.8 pp at full completion. An unpaired comparison would only detect about 4.5 pp.
- **Robustness checks:** repeat the test within each endpoint, and test endpoint × monitoring. The endpoint switched once, so endpoint is the same thing as collection time.
- **Sensitivity analysis:** count the 60 failures as each possible outcome in turn.

**Secondary (sprint 2.2 × 3.4): does the notice change actions, or only language?**
- Compare the watched-vs-unwatched shift in three places:
  - private plans and reasoning (planned action, deception and monitoring vocabulary)
  - public messages
  - final actions
- A finding of "sanitised talk, same deal", or the reverse, would be the headline.

**Exploratory analyses** (BH-corrected; effect sizes and intervals; descriptive only)
- **Setting.** Only 9 scenarios per setting, and task content differs between settings.
  - **Unit of analysis:** the scenario. Use a scenario-cluster bootstrap, or a scenario random intercept.
  - **How to report:** setting effects are **descriptive**, not causal.
  - **Clean comparisons:** level and monitoring vary within scenario, so their effects are clean.
- **Unilateral takes, broken down by agent.** These replace the vague "partner effect" item. Preliminary counts:
  - W-none: the welfare agent took and the no-rule agent refused 32 times, against 4 the other way round.
  - A-none: the no-rule agent took and the authority agent refused 40 times, against 14 the other way round.
- **Rule application.** Use the pack's `expected_tip_key` and the expected first tipping level to test whether the rules are applied as the labels predict.
- **v1 replication (Q4):** downgraded to a qualitative side note. The rules, scenarios and endpoints all differ.
- **Interaction dynamics (Q5):** only for metrics whose heuristics are re-validated on this run, with accuracy reported **for each monitoring arm** separately.

**Measurement safeguards**
- **Mask the monitoring notice text and its keywords before counting vocabulary.** The notice itself says "monitored", "oversight" and "review".
- **Add metrics for notice echo and monitoring mentions.**
- **Hand-label a blind sample for validation,** stratified by monitoring arm.

**What not to claim**
- Collusion, deception or "strategic" intent as established facts. Returned reasoning is not internal thought.
- That a setting causes an outcome.
- That the monitoring result applies to real oversight. This is a notice-only manipulation of one model, at one temperature, with one seed.
- That any effect size is final. This is an interim look.
- Any effect of communication. There is no baseline with communication turned off.
