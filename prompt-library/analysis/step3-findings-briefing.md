# Step 3: Findings briefing and paper kit

**Use it for:** turning Step 2 outputs into a briefing that lets the team quickly grasp what the data shows, how much to trust each claim, what to put in the paper, and what to do next to raise the judging scores.
**Pipeline stage:** Stage 3 of [`analysis-pipeline/PROCESS.md`](../../analysis-pipeline/PROCESS.md). **This prompt is authoritative for method.** `PROCESS.md` defines the file contracts. **Previous:** [Step 2](step2-analyze-and-report.md).
**Origin:** generalised from `SUMMARY-ANALYSIS.md` and `dimension-metric-analysis/REPORT.md` of the first pressure-pack run (branch `first-run-summary-analysis`), extended for the Apart Research AI collusion sprint deliverable (2026-10-25). It supersedes the former `plain-language-rewrite.md`: every rule from that prompt is kept under "Writing rules" and "Lite mode".

---

## Prompt

You are writing for the **team**, not the judges: smart people who must decide in minutes what to claim, what to show and what to run next. Interpret and rank; do not re-analyse. Every number you show must already exist in a Step 2 output. If you need one that doesn't, list it under "Next steps" as an analysis to run.

**Inputs (fill in)**
- Step 2 folder: `<STEP2_DIR>` (`REPORT.md`, `tables/candidates.csv`, `figures/`, `tables/`)
- Step 1 dictionary and validation: `<STEP1_DIR>` (`trial_metrics_dictionary.md`, `VALIDATION.md` if present)
- Transcripts: `<RUNS_DIR>` (`runs/<id>/result.json`, `events.jsonl`). Read the scenario pack from `manifest.json`, never from `prompts/`.
- Analysis plan (pre-specified tests, "what not to claim"): `<PLAN>`, or "none"
- Earlier summary to compare against: `<EARLIER_SUMMARY>`, or "none"
- Research questions: `<RESEARCH_QUESTIONS>` (default: sprint tracks 1 emergence and markets; 2.1-2.3 detection, audit, standards of evidence; 3.1-3.4 carriers and countermeasures)
- Judging criteria: Impact & Innovation, Execution Quality, Presentation & Clarity (1-5 each)
- Time and budget left: `<HOURS_LEFT>`, `<BUDGET>`. Paper limit: `<PAGES>` (default 8). Output folder: `<OUTPUT>`

**Writing rules** (kept from the plain-language rewrite)
- Replace codes with words, or define each one where it first appears: criteria, pairings, levels, scenarios, outcomes, endpoints or providers, seed, statistical terms. Give each scenario a one-line plain description.
- Use run IDs only as parenthetical citations, never as the subject of a sentence.
- Give numbers as "X out of Y (Z%, 95% CI a-b)", with a plain explanation of what they mean. Keep tables simple, with every column labelled in words.
- Explain caveats in everyday terms ("the runs that colluded most also ran on a different server, so we can't tell which caused it").
- Label every result **pre-specified** or **exploratory**. Returned reasoning is text the model produced, not its internal thought.
- Quotes: verbatim, at most 40 words, read in full context first, labelled *private plan*, *message* or *final reasoning*, and cited by run ID. Say whether each is typical or a contrasting case.

**Lite mode: readability rewrite only.** If you only need to make an existing report readable (`<REPORT>`) for a smart reader with no background, who hasn't seen the harness, the scenario pack or AI-safety jargon, for example a Step 2 `REPORT.md` or an older summary, do this instead of Steps A–C:
- Apply the Writing rules.
- Open with section 2, "What this experiment is".
- Add "why it matters" as one sentence per finding.
- Add section 3, "What changed", if `<EARLIER_SUMMARY>` is given.
- Keep the same findings and add no new analysis claims. Aim for roughly the original length, or slightly longer.
- Save to `<OUTPUT>/SUMMARY.md` (or another file name you're given) plus an `.html` copy.

**Step A: Build the claims ledger first.** Write `<OUTPUT>/claims_ledger.csv`: one row per candidate claim from `candidates.csv`, `REPORT.md` and `<EARLIER_SUMMARY>`, with columns
`rank, claim (one plain sentence), evidence (X of Y, effect, CI, source table or figure), strength, robustness checks passed/failed, main caveat, pre-specified/exploratory, research question(s), judging criterion served, novelty (known / new angle / new), paper-ready (yes / with caveat / not yet: what's missing), example run IDs`.
- **Strength.** *Strong:* survives FDR, clean of known confounds, holds within subgroups, adequate n. *Moderate:* one of these fails but the direction is consistent. *Suggestive:* exploratory, small n or confounded. *Not supported:* include it anyway, so the team stops repeating it.
- **Rank** by strength x relevance to the research questions x surprise. Carry Step 2's "looks large but untrustworthy" list in as *Suggestive* or *Not supported* rows.

**Step B: Write `<OUTPUT>/SUMMARY.md` (+ `.html`, figures embedded), in this order**
1. **60-second briefing** (at most 150 words): the one-sentence story; the 3 numbers that matter most; the biggest caveat; the single action with the best score lift per hour.
2. **What this experiment is:** the agents; private plan, then messages, then private final choice; what take and refuse mean and what is needed for the deal to execute; the moral rules; pressure levels; the evaluator; any manipulated factor (e.g. the monitoring notice). A scenario table with one line each.
3. **What changed** (only with `<EARLIER_SUMMARY>`): for each earlier finding, held up / stronger / weaker / reversed / not testable, with one line on why.
4. **Claims ledger:** the top 10 rows as a readable table, linking the CSV.
5. **Headline findings (3-5).** For each:
   - a title that states the takeaway
   - the numbers, one figure, and 1-2 quotes
   - **so what:** one sentence on why it matters for the research question
   - **theory of change:** who would act differently (monitor designers, evaluators, auditors, model developers) and what they would do
   - the caveat, and the research question and criterion it serves
6. **Supporting findings (3-6),** a short paragraph each, then **dropped findings** with the reason.
7. **What we do not claim.** Explicit non-claims, starting from `<PLAN>`'s list: intent, causation from factors that were not randomised, transfer to real oversight or other models, final effect sizes from preliminary data, effects of communication without a no-chat baseline.
8. **Threats to validity:** a table of threat, type (internal / construct / external / statistical), claims affected, severity, and the test that would resolve it. Include the `PROCESS.md` guardrails that apply.
9. **Judge lens.** One line each for AI control, monitoring, lie detection, evaluation honesty, multi-agent safety, and antitrust-style standards of evidence (2.3): the finding that group would care about, and the sentence we'd use. Then a **self-assessed score** (1-5) for each judging criterion, with the evidence for it and what is holding it below 5.
10. **Next steps, decision-oriented:** a table of action, kind (analysis only / new runs / writing), criterion and research question it lifts, expected lift (e.g. "Execution 3 to 4"), cost (API $, compute hours, person-hours), time to result, risk, and "do before deadline?". Sort by lift per hour. Estimate cost from `<BUDGET>` and the run's logged throughput, and mark guesses as guesses.
11. **Open questions:** what the data raises but cannot answer.
12. **Glossary:** every term and code used, one line each.

**Step C: Paper kit.** Write `<OUTPUT>/paper-outline.md` (+ `.html`), or a final `SUMMARY.md` section if time is short:
- **3 candidate titles:** one plain, one led by the finding, one led by the question.
- **Abstract draft, 150-250 words,** with the word count stated: problem, setup, the 2-3 strongest claims with numbers, main limitation, implication.
- **Section outline with a page budget** that sums to `<PAGES>`.
- **Figure plan:** 4-6 figures and 1-2 tables from `figures/`. For each: file path, the claim it carries, and a caption that states the takeaway and the n. Flag any figure that needs redrawing (codes on axes, missing n, unreadable at column width).
- **Limitations and dual-use appendix bullets.** Limitations come from items 7-8. Dual-use covers what a misuser could learn (e.g. which framings or notices make agents collude or conceal it), and why publishing is net-positive or what we withhold.

**Before finishing, check that:**
- every number traces to a Step 2 file and shows its n
- no claim in the briefing or abstract below *Moderate* appears without a caveat in the same sentence
- every quote was read in context and is cited
- no undefined code remains
- the `.html` copies render with their figures (`python tools/md_to_html.py . <file.md>`)

Then report the paths, the one-sentence story and the top three next steps.
