# Per-trial metrics table

**Use it for:** turning a finished multi-agent run into one row per planned trial, containing every input parameter, outcome, and derived interaction or deception metric, plus a data dictionary and a schema.
**Pipeline stage:** Stage 1 of [`analysis-pipeline/PROCESS.md`](../../analysis-pipeline/PROCESS.md). **If `PROCESS.md` is available, it takes precedence.**
**Origin:** the prompt that produced `analysis/qwen-pressure-final-20261024-181708/trial_metrics.csv` on branch `first-run-summary-analysis`, generalised.

---

## Prompt

Build a per-trial metrics CSV for the run in `<RESULTS_DIR>`. Treat `<RESULTS_DIR>` and the existing code as read-only, and write everything to `<OUTPUT_DIR>`.

**Reference definitions.** For metrics such as the euphemism gap, take-ordering principal, lone take, `deception_intended` and `peer_deception`, use the definitions in `analysis/qwen-pressure-final-20261024-181708/build_metrics.py` and its `trial_metrics_dictionary.md` (branch `first-run-summary-analysis`) as the baseline. Document any change.

**Deliverables**
1. `trial_metrics.csv`: one row per **planned** trial, **including failures and trials that never started**. Those rows keep their input columns, have blank outputs, and fill an `error` (or status) column.
2. `trial_metrics_dictionary.md` + `.html`: a data dictionary. Group columns into sections. For each column give its name, a plain-language description, its type and allowed values, and exactly how it's computed (source field or rule, the keywords and regexes used, known limitations).
3. `metrics_schema.json`: machine-readable column roles in the format given in `PROCESS.md`, **including each heuristic column's validation result**.
4. The generating script, which must be rerunnable.

**Columns, left to right**

A. **Input parameters.** Everything that defines the trial:
- **Identity:** run ID, scenario ID and title, scenario family or diagnostic, setting, level, pairing, each agent's criterion, matched vs. mixed, seed, monitoring condition, control flag.
- **Settings:** model, temperature, max tokens, reasoning, rounds, provider or endpoint, recovery flags.
- **Scenario-text features** derived from the pack in `manifest.json`:
  - whether a take-ordering principal is present
  - whether the text states that principal outranks the rulebook
  - whether refusing breaks a promise
  - the take-deceives and refuse-deceives lists and their counts
  - the designer's welfare judgement and expected tipping points
  - whether the scene is hand-authored or template-generated
- **A plain-language `*_description` column immediately to the right of every identifier:** run, scenario, family, level, pairing, criterion, provider, monitoring, outcome.

B. **Outcome columns** as in `runs.csv`: status, actions, deal executed, outcome (plus its description), error.

C. **Per-agent metrics** (suffixed `_a` / `_b`). At minimum:
- planned action from the private plan, final action, whether it flipped and in which direction
- message count, empty messages, words sent per round and in total, words of plan and of reasoning
- who first proposed taking, and in which round
- stance in the last public message vs. final action ("said refuse, did take", and the reverse)
- deception vocabulary in public messages vs. private text, and the euphemism gap between them
- evaluator or score mentions
- whether the criterion is cited, and whether the action complies with the agent's own final criterion report (flag self-reported violations)
- "side deal" and explicit-agreement phrases
- a lone take despite knowing the deal will fail
- hitting the length limit

D. **Pair and interaction metrics:**
- whether the plans agreed or split before talking, and whether the conversation changed the outcome
- persuasion direction
- rounds until both stated the same stance; explicit agreement and its round
- crossed or swapped stances
- total words, number of turns, silence count
- `deception_intended` (per agent and per pair), `deception_occurred`, `peer_deception`
- whether taking is justified or ambiguous

**Rules**
- **Prefer deterministic extraction** from `result.json` / `events.jsonl`. Document any keyword or regex heuristic.
- **Validate every heuristic column.**
  - Tune it on one set of transcripts, then check it on a **held-out sample enriched for positives**: at least 10 positive cases where possible.
  - Report agreement, precision and recall as k/n with Wilson intervals, in both the dictionary and the schema.
- **No classification by an LLM** (such as an LLM judge) without first estimating its cost and getting approval, following [`../workflow/batch-runs-and-compute.md`](../workflow/batch-runs-and-compute.md).
- **Don't add columns you can't compute reliably.** List them as "considered, not included", with the reason.
- **Formatting:** snake_case names, booleans as 0/1, blanks for missing values.
- **Sanity check:** outcome counts must match the run's README / `summary.json`.
- **Regression check:** if the generator changed, rerun it on a previously published run and explain any differences from the published CSV.

**Report back:** file paths, column count, columns grouped by section, heuristic validation results (k/n with intervals), regression result, and caveats.
