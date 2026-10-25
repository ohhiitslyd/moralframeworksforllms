# Plain-language rewrite of a findings report

**Use it for:** rewriting a technical analysis so that a smart reader with no background on the experiment can follow it.
**Pipeline stage:** a **Stage 3 helper**. The full Stage 3 (one-sentence story, tiered headline findings, transcript quotes, mapping to research questions, `SUMMARY.md`) is defined in [`analysis-pipeline/PROCESS.md`](../../analysis-pipeline/PROCESS.md). Use this prompt for the final readability pass, or to rewrite an existing report.
**Origin:** the prompt that produced the accessible version of `SUMMARY-ANALYSIS.md` on branch `first-run-summary-analysis`.

---

## Prompt

Rewrite `<REPORT>` so that someone with no background on this experiment can follow it. The reader is smart but hasn't seen the harness, the scenario pack, or AI-safety jargon. If an earlier version exists, compare against `<EARLIER_REPORT>` (leave it blank if there's none). Save the result as `<OUTPUT>` (e.g. `SUMMARY.md`) plus an `.html` copy.

1. **Open with a short "What this experiment is" section** in plain language:
   - who the agents are
   - what each agent does: private plan → messages → private final choice
   - what "take" and "refuse" mean, and what is needed for the deal to execute
   - what the moral instructions are
   - what the pressure levels do
   - what the evaluator is
2. **Replace codes with words, or define each one where it first appears.** This covers criteria, pairings, levels, scenario IDs (give each scenario a one-line plain description), outcome names, provider, seed, and statistical terms.
3. **Keep run IDs, but only as parenthetical citations,** never as the subject of a sentence.
4. **For each finding, add one sentence on why it matters** for the research question.
5. **Give numbers as "X out of Y"** with a plain explanation. Keep tables only if they're simple, and label every column in words.
6. **Keep the caveats, explained in everyday terms.** For example: "the runs that colluded most were also run on a different server, so we can't tell which caused it".
7. **Keep the same findings, and add no new analysis claims.** Aim for roughly the original length, or slightly longer.
8. **If `<EARLIER_REPORT>` is given,** add a short "What changed" section near the top, and say for each finding whether it held up, got stronger, got weaker or reversed.
