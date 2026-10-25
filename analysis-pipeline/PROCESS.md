# Experiment analysis process

A single, repeatable process for turning a finished experiment run into:

1. a **per-trial metrics table**: one row per trial, with every input parameter, outcome, and derived interaction or deception metric;
2. a **parameter → outcome relationship report**: design check, univariate summaries, association matrices, single-factor and two-factor heat maps, and statistics;
3. a **curated findings summary**: a few headline relationships, supporting results, and footnotes, written for a reader new to the project.

Each stage has a **deterministic part**, a script that anyone can rerun, and a **judgement part** for an analyst or AI agent: validating heuristics, choosing what matters, and writing it up. The stages talk to each other only through files, so you can rerun any stage without the ones before it.

```
results/<run>/                         Stage 1: Metrics           Stage 2: Relationships       Stage 3: Findings
  manifest.json  (pack + config)  ──▶  trial_metrics.csv     ──▶  REPORT.md (+ .html)     ──▶  SUMMARY.md (+ .html)
  runs.csv                             metrics_schema.json        figures/, tables/            (curated, plain language)
  runs/<id>/result.json, events.jsonl  trial_metrics_dictionary.md
```

The **contract** between Stage 1 and Stage 2 is `metrics_schema.json`. Stage 2 never hard-codes column names, so it works for any experiment whose Stage 1 writes a schema.

---

## Stage 0: Inputs (fill in once per run)

| Item | Example |
|---|---|
| Results folder | `results/qwen-pressure-final-20261024-181708` |
| Output folder | `analysis/qwen-pressure-final-20261024-181708` |
| Unit of analysis | One row per episode. Agent-level metrics are clustered in pairs. |
| Scenario pack | Read from `manifest.json["pack"]`. Never re-read from `prompts/`, which may have changed since the run. |
| Known design facts | "One seed per cell", "provider switched mid-run", "levels are independent episodes" |
| Research questions | The sprint tracks or hypotheses the findings should speak to |
| Audience | "Judges and researchers new to the project" |

Ground rules for every stage:
- Treat results as **read-only**. Write only to the output folder.
- Every number shown must come with its **n**.
- Never present a p-value without an **effect size** and an **interval**.
- Fix every random seed.

---

## Stage 1: Per-trial metrics

### Deliverables
- `trial_metrics.csv`: one row per planned trial, **including failures**. Failures keep their input columns, have blank outputs, and fill an `error` column.
- `metrics_schema.json`: machine-readable column roles (see the schema section below).
- `trial_metrics_dictionary.md` (+ `.html`): every column with a plain-language description, its type and allowed values, how it's computed (source field, rule, keywords or regexes), its validation result, and its known limitations. Columns are grouped into sections. The dictionary also lists metrics that were considered but not included, with the reason.
- The generator script, which must be rerunnable.

### Column layout, left to right

**A. Input parameters.** Everything that defines the trial:
- **Identity and design:** run ID, scenario ID, scenario title, scenario family or diagnostic, setting, level, pairing, each agent's criterion, matched vs. mixed, seed, monitoring condition, control flag.
- **Model and run settings:** model, temperature, max tokens, reasoning on/off, rounds, provider or endpoint, recovery flags.
- **Scenario-text features** derived from the pack:
  - whether a take-ordering principal is present
  - whether rank is stated in the text
  - whether refusing breaks a promise
  - the take-deceives and refuse-deceives lists and their counts
  - the designer's welfare judgement
  - expected tipping points
  - whether the scene was hand-authored or template-generated
- **A plain-language `*_description` column immediately to the right of every identifier.** For example: run, scenario (setting, duty, deal, reward, cost), family, level (the pressure text), pairing, criterion (a summary of the rule), provider, monitoring, outcome.

**B. Outcomes:** status, each agent's action, deal executed, joint outcome (plus its description), error.

**C. Per-agent metrics** (suffixed `_a` and `_b`):
- planned action from the private plan, final action, whether it flipped and in which direction
- stance per round; message count; empty messages; words sent per round and in total; words in plans and in reasoning
- who first proposed taking, and in which round
- last public stance vs. final action, with "said refuse, did take" and "said take, did refuse" flags
- deception vocabulary in public messages vs. private notes vs. private reasoning, and the gap between them
- evaluator or score mentions
- whether the criterion is cited, and whether the action complies with the agent's own criterion report (self-reported violation)
- "side deal" and agreement phrases
- a lone take made while knowing the deal would fail
- hitting the length limit
- deception intended

**D. Pair and interaction metrics:**
- whether the plans agreed or split before talking, and whether the conversation changed the planned outcome
- persuasion direction
- rounds until both stated the same stance; explicit agreement and its round
- crossed or swapped stances
- total words exchanged, number of turns, silence count
- deception intended (per pair), deception that occurred, deceiving the peer
- whether taking is justified or ambiguous (it keeps a promise or obeys a court)

### Rules
- **Prefer deterministic extraction** from `result.json` and `events.jsonl`. Where you must use keyword or regex heuristics, document the exact patterns in the dictionary.
- **Validate every heuristic column** against 10–20 transcripts you have read: a tuning set plus a held-out set. Report precision, recall and agreement in the dictionary and in the schema.
- **Leave out columns you can't compute reliably.** List them as "considered, not included", with the reason.
- **Formatting:** snake_case names, booleans as 0/1, blanks for missing values.
- **Sanity check:** outcome counts must match the run's `README.md` / `summary.json`.
- **Regression check:** when the generator changes, rerun it on a previously published run and compare the result with the published CSV. Any differences must be explained.

### Metrics schema (`metrics_schema.json`)
One entry per column:

```json
{
  "name": "said_refuse_did_take_a",
  "section": "agent",
  "role": "outcome",
  "level": "agent",
  "agent": "a",
  "type": "binary",
  "levels": null,
  "description_column": null,
  "subset": "complete episodes",
  "derived_from": ["last_public_stance_a", "final_action_a"],
  "by_construction_with": ["peer_deception_a"],
  "heuristic": true,
  "validation": {"precision": 1.0, "n_checked": 7},
  "label": "Said refuse in public, then took"
}
```

- **`section`**: `input` | `outcome` | `agent` | `pair` | `meta`.
- **`role`**: `id` | `parameter` | `outcome` | `description` | `meta`.
- **`type`**: `numeric` | `ordinal` | `categorical` | `binary` | `text`.
- **`level`**: `trial` | `agent`. Agent-level columns are paired by their `_a` / `_b` suffix.
- **`description_column`**: points from an identifier to its plain-language column.
- **`subset`**: states the denominator when a metric only applies to some trials. For example, "agents whose plan said refuse".
- **`by_construction_with`**: lists columns whose association with this one is guaranteed by definition. Stage 2 must not report those associations as findings.
- **`heuristic` + `validation`**: carry the error rate forward, so Stage 2 can attach a caveat to any finding that uses the column.

---

## Stage 2: Parameter → outcome relationship report

Inputs: `trial_metrics.csv` + `metrics_schema.json`. Columns are selected by role, never by hard-coded name.

### Step 0: Type and frame
- **Type every variable from the schema.** Record missing values, the number of levels, and the min, median and max count per level.
- **Clustering.**
  - Reshape the `_a` / `_b` columns to long format (one row per agent).
  - Permute whole episodes for episode-level parameters, and permute within episodes for agent-level parameters (such as each agent's criterion in mixed pairings).
  - Treat scenario or template as a stratum.
  - Get intervals for effect sizes from a cluster bootstrap.
  - If a cluster-aware method isn't possible, say the p-values are optimistic.
- **Flag columns related by construction** (from the schema) and columns that rely on heuristics.

### Step 1: Design check (parameter × parameter)
Purpose: find **confounding and aliasing** before interpreting any outcome.
- **Mixed-type association matrix:**
  - numeric–numeric: Spearman ρ
  - categorical–categorical: bias-corrected Cramér's V
  - numeric–categorical: correlation ratio η
- **Heat map:** values printed, ordered by clustering.
- **Cell-count tables** for any pair with association ≥ 0.3, or with empty or tiny cells.
- **State which effects cannot be separated** (aliased pairs) and which comparisons are clean, for example "within provider = Modal, scenario family varies freely". Every later finding must say whether it is clean or confounded.

### Step 2: Univariate summaries
- **Parameters:** counts per level, to show design balance.
- **Outcomes:**
  - binary: a rate with a 95% Wilson interval
  - numeric: median and interquartile range (IQR), shown as a histogram or box plot (log or rank scale if skewed)
- One compact table: variable, type, n, missing, summary, interval.

### Step 3: Parameter × outcome screening
For every (parameter, outcome) pair:
- **Effect size:**
  - categorical parameter, binary outcome: Cramér's V, plus the max−min rate across levels
  - categorical parameter, numeric outcome: √ε² (η-like, so it's on the same scale as V and |ρ| for ranking), plus the max−min difference in medians
  - ordinal or numeric parameter: Spearman ρ
- **Test:** Fisher's exact test for 2×2 tables; otherwise a permutation test with a fixed seed and **at least 20·m/α shuffles for m tests**, so the BH correction can still detect a single real effect. Stop early once p is clearly above 0.1, use an exact or asymptotic p where it's valid, and report the shuffle count.
- **Multiple comparisons:** Benjamini–Hochberg q-values across all pairs.
- **Screening table**, sorted by effect size, with columns: effect, interval or p, q, minimum cell n, clean or confounded, by-construction flag, heuristic flag.
- **One heat map per key parameter:** rows are the parameter's levels, columns are outcomes, and cells hold the rate or median with n.
  - Colour is normalised per column, and the raw value is always printed.
  - Pair-level and agent-level blocks are separated.
  - Cells with q < 0.05 are marked, and confounded cells are hatched.
- **For the top single-parameter relationships** (q < 0.05, minimum cell n ≥ 10, up to ~10), draw level-by-outcome charts with intervals. Repeat the comparison **within** the levels of any confounding parameter.

### Step 4: Outcome × outcome
- **The same mixed-type matrix over outcomes.**
- **Separate by-construction correlations from informative ones.**
- **Flag near-redundant outcomes** (|association| ≥ 0.8 and not by construction).

### Step 5: Two-parameter interactions (2D heat maps)
- **Candidates** are parameter pairs that aren't aliased and have adequate cell counts.
- **Rank them by interaction strength, not by main effects.** For binary outcomes, use the likelihood-ratio (deviance) improvement of A×B over additive A+B on the **logit** scale; for numeric outcomes, use the same on the rank scale. Penalise by the extra degrees of freedom, and get a permutation p-value.
- **Draw only the pairs that pass (at most 6–10),** plus any view that is central to the research question. If none pass, say so. Rows are A, columns are B, and colour is the outcome on an **absolute** scale. Each cell shows its value and k/n, and small cells are greyed out.
- **Describe each in words,** e.g. "B matters only when A = …".

### Step 6: Rank candidates for Stage 3
Score every relationship on:
- effect size
- robustness: survives FDR, is clean rather than confounded, holds within subgroups, has adequate cells
- relevance to the research questions
- surprise relative to the design's expectations, such as the pack's expected tipping points

Write `tables/candidates.csv`, including an explicit "looks large but untrustworthy" list with the reasons.

### Chart rules
- **Titles state the takeaway.** Axis labels use plain words: use the `*_description` and title columns, never codes.
- **Colour bars have units.**
- **Scales:** a single-hue sequential scale for magnitudes; a diverging scale centred at 0 for signed correlations; colour-blind-safe palettes that work in light and dark themes.
- **Print the value and n in every heat-map cell.** Order rows and columns meaningfully.
- **Keep it to about 10–20 charts.** Prefer small multiples.

### Deliverables
- **`REPORT.md` (+ `.html` with the figures embedded)**, in this order:
  1. summary
  2. how to read the charts
  3. design check
  4. top relationships
  5. univariate results
  6. matrices
  7. single-factor heat maps
  8. 2D interactions
  9. caveats in plain terms
  10. file index
- **`figures/`**: PNG, and SVG where useful.
- **`tables/`**: the univariate tables, the screening table with all tests, the matrices, the numbers behind every chart, and `candidates.csv`.
- **The report script**, which must be rerunnable.

---

## Stage 3: Curated findings

Inputs: `REPORT.md`, `tables/candidates.csv`, the transcripts, and the research questions.

1. **Write a one-sentence story** that the headline findings support.
2. **Sort the findings into three tiers:**
   - **Headline (3–5):** each gets one chart, a one-line takeaway, the numbers with intervals, a "why it matters" line and a caveat line, plus one or two short quotes from transcripts, cited by run ID.
   - **Supporting (3–6):** a short paragraph each.
   - **Footnotes and appendix:** everything else, including relationships that were dropped and why.
3. **Write for a newcomer:**
   - Start with "what this experiment is", with codes spelled out and a one-line description of each scenario.
   - Use run IDs only as parenthetical citations.
   - Give numbers as "X out of Y".
   - Explain caveats in everyday terms.
4. **Revisit earlier findings.** If an earlier run was analysed, say for each finding whether it held up, got stronger, got weaker or reversed. Include a "what changed" section.
5. **Align with the research questions.** Map each headline finding to the research question or judging criterion it addresses.

Deliverable: `SUMMARY.md` (+ `.html`).

---

## Guardrails learned on this project

- **Read the pack from the run's manifest.** Packs in `prompts/` change after runs: v1, v2, then the extended v5/v6.
- **Each pressure level is an independent episode.** Text that refers to "the previous level" is a design bug that shows up as a fake trend.
- **Labels in the prompt are inputs, not outcomes.** "Outranks", "take deceives …" and "refuse breaks a promise" do part of the agent's reasoning for it. Treat them as parameters, and be careful when interpreting rule-following.
- **Template-generated scenes are not independent evidence.** Flag them, and analyse them as a separate stratum or as clusters.
- **Provider or endpoint is often aliased with collection order.** Check it in Step 1 every time.
- **Some columns are related by construction.** "Deception intended" requires a planned or actual take. "Deception occurred" can equal "deal taken". Don't report those correlations as findings.
- **A solo take can be a free gesture.** Under a collusion lock, unilateral takes are not a clean measure of willingness to collude.
- **Simultaneous message rounds create crossed-stance artifacts.** Take them into account when interpreting persuasion metrics.

## Reference implementation (first run)

The first run's hand-built versions of Stages 1–3 are on branch `first-run-summary-analysis`, under `analysis/qwen-pressure-final-20261024-181708/`:
- Stage 1: `build_metrics.py`, `trial_metrics.csv`, `trial_metrics_dictionary.md`
- Stage 2: `dimension-metric-analysis/analyze_dimensions.py`, `REPORT.md`
- Stage 3: `SUMMARY-ANALYSIS.md`

These are specific to that pack. The planned scripts in `analysis-pipeline/` will generalise them using the schema contract above.
