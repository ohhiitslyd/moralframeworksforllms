# Step 2: Analyse and produce reports

**Use it for:** single-, two- and three-variable analysis of a per-trial table, so a human can quickly see which experiment parameters (fewer than about 30) matter for which outcomes (fewer than about 20). The analysis covers:
- a design check
- correlation and association matrices (parameter × parameter, parameter × outcome, outcome × outcome)
- single-factor heat maps and 2D heat maps (two inputs, one output)
- a pre-specified primary test
- statistics that are honest about clustering, multiple comparisons and missing data

It ends with candidates ranked and filtered for anything that is clearly non-random, interesting or important.
**Pipeline stage:** Stage 2 of [`analysis-pipeline/PROCESS.md`](../../analysis-pipeline/PROCESS.md). **This prompt is authoritative for method.** `PROCESS.md` defines the file contracts.
**Origin:** the owner's original requests and prompts (Appendix), generalised, then revised after an expert review, a friendly review and an adversarial review (2026-10-25). It supersedes the former `parameter-outcome-report.md`.
**Previous:** [Step 1](step1-extract-organize-augment.md). **Next:** [Step 3](step3-findings-briefing.md).

---

## Prompt

Analyse `<DATA>` so a human can quickly understand which parameters matter for which outcomes, both visually and with summary statistics. Stop once you've produced ranked candidates. Choosing the headline findings and writing the narrative happens in Step 3.

### Inputs (fill in)
- `<DATA>`: the per-trial table (`trial_metrics.csv`), with `<SCHEMA>` (`metrics_schema.json`) and its dictionary
- `<PARAMETERS>` / `<OUTCOMES>`: explicit lists, or "schema role = parameter / outcome". Explicit lists override the schema.
- `<RESEARCH_QUESTIONS>`, and the design's expected directions and tipping points (e.g. the pack's `expected_first_take`)
- `<PRIMARY>`: the pre-specified primary hypothesis, if one exists
- `<DESIGN_FACTS>`: e.g. one seed per cell; a paired manipulation via `cell_id`; endpoint switched mid-run; **interim snapshot: yes/no**
- `<OUTPUT_DIR>`; `<AUDIENCE>`; `<TIME_BUDGET>` (default 30 minutes of compute)

### Ground rules
- **Scope.** Treat the input data as read-only, and write only to `<OUTPUT_DIR>`. No git operations.
- **Before charting.** Check which packages are installed. Load the `dataviz` skill if your environment has it, and follow its guidance on palette, scales, labelling and accessibility. If `python -I` hides the installed packages, run your own analysis script without `-I`. Keep `-I` for code that only reads untrusted data.
- **Reproducibility.** Put everything in one rerunnable script with fixed seeds. Also write `provenance.json`: input SHA-256s, package versions, arguments and seeds.
- **Prefer effect sizes and consistency over significance.**
- **Reporting numbers.**
  - Every number comes with its n.
  - Never give a p-value without an effect size and a 95% interval.
  - Wilson intervals are only for rates over independent units. Rates over agents, or pooled across scenarios, get **cluster-bootstrap** intervals at the parameter's randomisation level.
- **Interim snapshots.** Label every output **PRELIMINARY**, and don't present any effect size as final.
- **Runtime.** Estimate total runtime before running permutation work. If it would exceed `<TIME_BUDGET>`, stop and report.

### Language rules (against overclaiming)
- **Operational labels.** Metric names are labels, not facts. Write "flagged as deception-intended by heuristic X (precision k/n)", not "agents intended to deceive". Write "joint take", not "collusion", unless the messages show coordination.
- **Reasoning traces** are generated text, not evidence of internal states.
- **Manipulations are what they are.** A notice is a text notice, not real oversight.
- **Causal wording** is only for manipulated factors whose comparisons are clean. Everything else is "associated with".

### Step 0: Type, frame and pre-register
1. **Read the schema and profile the data.** Record missingness, levels and cell counts (min, median, max per level) for every variable. Take each variable's type (numeric, ordinal, categorical, binary, text, empty, constant) and its `randomisation_level` (scenario, episode or agent). Exclude empty and constant columns.
   - Flag outcomes that apply only to a subset, with their denominators.
   - Flag by-construction pairs; never report them as findings.
   - Flag heuristic columns, with their overall and per-arm accuracy.
   - Flag `source_key_missing` columns.
2. **Reshape** `_a` / `_b` columns to long format, one row per agent, for agent-level analysis.
3. **Post-treatment subsets.** Screen a subset outcome only after testing that the parameter doesn't change who is in the subset. Otherwise report the unconditional version and its decomposition, e.g. P(deception_intended) = P(take) × P(intended | take). Never condition on a post-treatment variable (e.g. "plans agreed") when testing a treatment.
4. **Write `PREREG.md` before computing any outcome-by-condition numbers.** It contains the primary hypothesis, outcome, test, α, unit of analysis, and expected direction. Everything else is exploratory and is corrected with Benjamini–Hochberg (BH).

### Step 1: Design check (parameter × parameter) and completion
- **Mixed-type association matrix:** Spearman ρ, bias-corrected Cramér's V, correlation ratio η.
- **Cell-count tables** for every pair with association ≥ 0.3, or with empty or tiny cells.
- **State which effects are aliased and which comparisons are clean.**
- **Completion balance:** cross status (complete, failed, not_started) with every parameter, and test it as an outcome. Exclude not_started rows from rates, and name the denominator. Check for confounding by endpoint and collection time.

### Step 1b: Primary test and power
- **Paired designs.** If `cell_id` / `paired_by` exist, the primary test is **paired**:
  - binary outcomes: McNemar's test, exact when there are fewer than 25 discordant pairs; report the discordant counts in both directions
  - numeric outcomes: a paired sign-flip permutation test
- **Repeat the primary test** within each endpoint (or time block) and within each major factor.
- **Power.** Report the minimum detectable effect at 80% power, now and at full completion.
- **Unpaired tests are secondary.**

### Step 2: Univariate summaries
- **Parameters:** counts per level, to show balance and gaps.
- **Outcomes:**
  - binary: rates with intervals
  - numeric: medians and IQRs, as histograms (log or rank scale when skewed)
- **Pooling.** Show per-agent metrics pooled across `_a` / `_b` where that makes sense.
- **Output:** one summary table (variable, type, n, missing, summary, interval), saved as CSV.

### Step 3: Parameter × outcome screening
- **Effect sizes, on a comparable scale:**
  - V for categorical × binary
  - √ε² (η-like) for categorical × numeric
  - |ρ| for ordinal or numeric, plus a monotonicity note
  - **Raw spread:** also give the max−min spread of rates or medians.
  - **Stratified effects:** report the within-stratum effect (Cochran–Mantel–Haenszel / stratified) alongside the pooled one, and **flag any sign reversal** (Simpson's paradox).
- **Randomisation level.** Test and bootstrap each parameter at its own level:
  - **scenario-level** parameters: permute whole scenarios; the effective n is the number of scenarios, so report it
  - **episode-level** parameters: permute episodes, stratified by scenario only when the parameter varies within scenario
  - **agent-level** parameters: test within mixed pairings only, and test matched vs. mixed at episode level
  - **Never stratify** by a variable that is a function of the tested parameter.
  - If a cluster-aware test isn't possible, say the p-values are optimistic.
- **p-values:**
  - **Screening:** Fisher's exact test for 2×2 tables, asymptotic or exact tests elsewhere (χ², Spearman t, Kruskal–Wallis).
  - **BH family:** parameter × outcome pairs only, with by-construction pairs removed before m is counted.
  - **Confirmation:** confirm BH survivors with a **sequential (Besag–Clifford) permutation** test (stop at about 50 exceedances), and report the shuffle count and the floor, 1/(B+1).
- **Screening table**, sorted by comparable effect size. Columns: effect, interval, p, q, effective n, minimum cell n, clean or confounded, by-construction flag, heuristic flag.
- **Heat maps:**
  - **Overview:** parameters × outcomes, coloured by effect size.
  - **Single-factor:** one per key parameter. Rows are its levels, columns are outcomes, and each cell shows its value and n.
    - **Colour:** absolute by default (rates 0–1). If you normalise colour per column, mark the non-significant cells.
    - **Marking:** mark q < 0.05, and hatch confounded cells.
    - **Blocks:** keep pair-level and agent-level outcomes in separate blocks.
  - **Data:** write a CSV behind every heat map, e.g. `tables/dimension_x_metric_<dim>.csv`.
- **Top relationships** (q < 0.05, effective n adequate, minimum cell n ≥ 10):
  - Draw level-by-outcome charts with intervals.
  - Repeat each comparison **within** the levels of any confounder.
  - Give each a one-line takeaway, the numbers, the chart, and a "why it matters / caveat" line.

### Step 3b: Words vs. actions, and asymmetry
- **Words vs. actions.** For each manipulated factor, show its effect on **private reasoning, public messages and final actions** side by side, in one table and one chart.
  - Use the `_novel` vocabulary counts, not raw counts, so words copied from the prompt don't create a spurious effect.
  - Attach per-arm heuristic accuracy, and flag a contrast as potentially biased if measurement error differs between arms.
- **Asymmetry.** In mixed pairs, break down who takes alone by each agent's criterion.

### Step 4: Outcome × outcome
- **Association matrix:** build the same mixed-type matrix over outcomes.
- **Classify the correlations:** separate by-construction ones from informative ones.
- **Redundancy:** flag outcomes that are near-redundant (|association| ≥ 0.8 and not by construction).

### Step 5: Two-parameter interactions (deferrable)
- **Candidates:** non-aliased pairs with adequate cells.
- **Method:**
  - binary outcomes: a **ridge-penalised logit**; the statistic is the deviance drop of A×B over A+B, minus the extra degrees of freedom; the null comes from a parametric bootstrap of the additive fit
  - numeric outcomes: OLS on ranks
  - where cells are separated (0 or n), use Firth or exact methods
- **2D heat maps:** draw only the pairs that pass (at most 6–10), plus pairs central to the research questions, such as scenario × level, family × level, pairing × family and criterion × family (agent take rate) for the main outcome. Use an **absolute** colour scale, show the value and k/n in each cell, and grey out small cells. Describe each in words.
- **If none pass,** or the time budget is exhausted, say so.

### Step 6: Sensitivity
- **Failures:** re-run the primary test treating failures as each outcome value in turn (best and worst case).
- **Heuristic error:** show how the main contrasts change if a heuristic's error rate differs between arms by its interval width.

### Step 7: Rank the candidates
- **Score** each relationship on effect size, robustness (survives FDR, clean, holds within subgroups, effective n), relevance to `<RESEARCH_QUESTIONS>`, and surprise relative to the expected directions that were **written down before looking**.
- **Mark every post-hoc candidate as exploratory.**
- **Write `tables/candidates.csv`**, including a "looks large but untrustworthy" list with the reasons.

### Chart rules
- **Titles** state the takeaway.
- **Axis labels** are plain words, never codes. Use the description and title columns.
- **Colour bars** have units.
- **Scales:** sequential for magnitudes, diverging and centred at 0 for signed values. Colour-blind safe, and readable in light and dark themes.
- **Cells** print their value and n.
- **Ordering:** rows and columns ordered meaningfully.
- **Count:** about 10–20 charts.

### Deliverables
- **`REPORT.md` + HTML,** with figures embedded by relative links (`figures/<name>.png`), and these sections:
  1. summary (PRELIMINARY if interim)
  2. how to read the charts
  3. design check and completion
  4. primary test
  5. top-ranked relationships
  6. words vs. actions
  7. univariate results
  8. matrices
  9. heat maps
  10. 2D interactions
  11. sensitivity
  12. caveats in plain terms
  13. file index
- **Supporting files:** `PREREG.md`, `figures/`, `tables/` (including `candidates.csv` and the CSV behind every chart), `provenance.json` and the script.

### Report back
Files; the primary result; one line per top candidate; aliased pairs; completion balance; anything you couldn't analyse reliably, with the reason.

---

## Appendix: original prompts (provenance)

### 1. Original requests (verbatim, from the project owner)

**Request C: univariate and bivariate analysis with heat maps**

> OK thanks, can you also perform univariate and bivariate analysis of dimensions vs. metrics, producing heat maps for each (in some easily digestible format), and providing analysis or commentary on the most interesting relationships?

**Request D: a general-purpose prompt for this kind of report**

> Thanks, what's the best way to prepare reports for a human to quickly, visually and via summary-statistics, grok the relationships between a small number of experiment parameters (let's say fewer than 30) and a small number of outcome metrics (let's say fewer than 20)? I'm thinking, maybe correlation matrices (parameter-parameter, parameter-outcome, outcome-outcome), heat maps of the least random single-dimension relationships and 2d heatmaps (2 input variables vs. one output variable), also filtered for anything clearly non-random, experimentally interesting, correlated, or otherwise exhibiting important relationships? Please produce a general purpose prompt for this

### 2. Prompt sent to the analysis agent for Request C (verbatim)

The scratchpad and worktree paths have been replaced by placeholders.

> **Statistics guidance in this prompt has been superseded.** It normalises colour per column, treats agent rows as independent, only "notes" multiple comparisons (no FDR correction), and gives no shuffle-count rule. The prompt at the top of this page has the corrected method. Its file paths, column names and first-run caveats are also specific to that run.

```text
New task: univariate and bivariate analysis of the per-trial metrics, with heat maps and written commentary.

Input: <ANALYSIS_DIR>\trial_metrics.csv. It now has 162 columns. I added a plain-language *_description column next to every identifier (run, scenario, family, diagnostic, level, pairing, pairing kind, criterion A/B, provider, outcome). build_metrics.py and trial_metrics_dictionary.md in the same folder are updated to match.

Output: write everything into a new folder, <ANALYSIS_DIR>\dimension-metric-analysis\. Writing into the repo working tree is fine for this task. Do NOT git add, commit or push; I'll do that. Don't modify any other files.

Before writing any chart code, invoke the `dataviz` skill with the Skill tool and follow its guidance. That covers palette, sequential vs diverging scales, labelling and accessibility.

What to produce:

1. **Univariate analysis**
   - **Dimensions:** distribution of trials per value for scenario, family, level, pairing, criterion, matched/mixed, provider and the scenario-text flags (take_principal_present, rank_stated_in_level_text, refuse_breaks_promise, welfare_if_take_designer, take_is_justified_ambiguous). Mostly to show the design balance and gaps, such as provider vs scenario.
   - **Metrics:** for outcome and every meaningful per-agent and pair metric, give the distribution (rate for binaries; median/IQR or a histogram for counts and word lengths). Pool _a/_b into a per-agent view where sensible.

2. **Bivariate analysis: dimensions vs metrics**
   - The core deliverable is heat maps with rows = dimension values and columns = metrics, cells = rate or mean. Normalize per metric column so colour is comparable across metrics, but annotate cells with the raw value and n.
   - Make one heat map per key dimension (scenario, family, level, pairing, criterion, provider, plus the text flags grouped together).
   - Use agent-level rows (criterion of that agent) for per-agent metrics.
   - Also make dimension × dimension heat maps of the headline metrics: scenario × level for collusion rate, family × level, criterion × family for the agent take rate, pairing × family, and any others you find revealing.
   - Optionally add a metric × metric correlation heat map, e.g. Spearman over pair-level metrics.

3. **Statistics, kept honest.** n is small (one seed per cell). For every relationship you highlight, give n, an effect size and an interval or simple test (e.g. Wilson CIs for rates; Fisher/chi-square or a permutation test; Cramér's V or rank correlation). Note multiple comparisons. Call out wherever a relationship is confounded: provider and scenario are almost perfectly aliased, the level-5 wording artifact, and stance-classifier error in derived columns. Don't present confounded effects as causal.

4. **Easily digestible format**
   - REPORT.md, written in the same accessible style as SUMMARY-ANALYSIS.md. Start with plain-language "how to read these heat maps" and "top 8–12 most interesting relationships" sections. Each relationship should have a one-line takeaway, the numbers, the chart and a "why it matters / caveat" line.
   - Then add sections for univariate and bivariate results, each embedding the PNG heat maps with relative links: figures/xxx.png.
   - Keep chart count reasonable, roughly 10–20. Every chart needs a clear title, axis labels in words (use the description/title columns rather than codes where space allows) and a legend/colour bar explaining the scale.
   - Also write summary tables as CSV (e.g. tables/dimension_x_metric_<dim>.csv) so the numbers behind each heat map are reusable.
   - Put the analysis script in that folder as analyze_dimensions.py, so it can be rerun. If you need packages beyond stdlib (pandas, matplotlib, scipy, seaborn), check what's installed first. Run python without -I if -I hides the installed packages, since this is our own script on our own data.

When done, report:
- the file list
- the top relationships, in a short list
- any stats or caveats I should know about
```

### 3. General-purpose prompt as first proposed for Request D (verbatim)

This is the version proposed in answer to Request D, before the expert review. The prompt at the top of this page fixes several statistical issues: permutation resolution under the Benjamini–Hochberg correction, comparable effect-size scales, logit-scale interaction tests, and cluster-aware testing. **Use the prompt at the top of this page.**

```text
# Task: Parameter → outcome relationship report

You are analysing an experiment's results so a human can quickly understand which parameters matter for which outcomes, visually and with summary statistics.

## Inputs (fill in)
- Data file: <path to CSV/Parquet, one row per unit>
- Unit of analysis: <e.g. one row per episode / trial / participant>
- Clustering: <e.g. "two agent rows per episode", "repeated measures per subject", or "none">
- Parameters (independent variables, ≤30): <list, or "columns in section X of the data dictionary">
- Outcomes (dependent variables, ≤20): <list>
- Data dictionary / codebook: <path, or "none">
- Known design facts: <e.g. "full factorial", "one seed per cell", "provider switched mid-run">
- Output folder: <path>
- Audience: <e.g. "researchers new to the project", "hackathon judges">

## Ground rules
- Treat the data as read-only. Write only to the output folder.
- Put all analysis in one rerunnable script (`analyze.py`). Use pandas/numpy/matplotlib (and scipy/statsmodels if installed; otherwise implement the few tests you need). Fix every random seed.
- Never present a p-value without an effect size and an interval. Prefer effect sizes and consistency over significance.
- Every number shown must also come with its n.

## Step 0: Understand and type the variables
1. Classify every parameter and outcome as numeric, ordinal, categorical or binary. Record missingness, the number of levels, and the min, max and median count per level.
2. Flag outcomes defined only for a subset (e.g. "switch rate among agents who planned X") and state their denominators.
3. Flag outcomes that are related by construction (one is derived from another, or they share inputs). Correlations between them must not be reported as findings.
4. Flag derived or heuristic outcomes (classifiers, keyword counts) and their known accuracy. Their errors carry into anything built on them.
5. If rows are clustered, choose an episode-level summary or a cluster-aware test for every comparison, and say which. Do not treat clustered rows as independent without saying the p-values are optimistic.

## Step 1: Design check (parameter × parameter)
Purpose: find confounding and aliasing before interpreting any outcome.
- Compute a mixed-type association matrix over all parameters:
  - numeric–numeric: Spearman ρ
  - categorical–categorical: bias-corrected Cramér's V
  - numeric–categorical: correlation ratio η
  - binary is treated as categorical
- Plot it as a heat map on a 0–1 scale, with values printed and pairs ordered by clustering.
- Plot cell-count tables (mosaic or heat map) for any pair with association ≥ 0.3, or any pair with empty or very small cells.
- Report which parameter effects cannot be separated (aliased pairs) and which comparisons are clean (e.g. "within level X of parameter P, Q varies freely"). Every later finding must say whether it is clean or confounded.

## Step 2: Univariate summaries
- Parameters: a bar chart of counts per level (design balance).
- Outcomes:
  - binary: rate with a 95% Wilson interval
  - numeric: histogram or box plot with median and IQR
  - skewed numeric: show it on a log or rank scale
- Put both in one compact table: variable, type, n, missing, summary, interval.

## Step 3: Parameter × outcome screening
For every (parameter, outcome) pair:
- Effect size:
  - categorical parameter, binary outcome: Cramér's V, plus the max−min rate difference across levels
  - categorical parameter, numeric outcome: ε² / η², plus the max−min difference in medians
  - numeric or ordinal parameter: Spearman ρ, plus a monotonicity note
- Test: a permutation test (≥2,000 shuffles, fixed seed; cluster-aware where needed), or an exact test for small 2×2 tables.
- Multiple comparisons: Benjamini–Hochberg q-values across all pairs.
- Screening table, sorted by effect size, with columns: effect, interval or p, q, minimum cell n, clean or confounded, by-construction flag.
- Heat map: parameters × outcomes, coloured by effect size, with values printed and n shown. Mark cells with q < 0.05. Mark confounded cells (e.g. hatching).
- For the top single-parameter relationships (by effect size, with q < 0.05 and minimum cell n ≥ 10; take up to ~10):
  - draw a level-by-outcome chart (rates with intervals, or box plots)
  - for any whose effect may come through a confound, add the comparison within the confounding parameter's levels

## Step 4: Outcome × outcome
- Draw a mixed-type association matrix over outcomes, using the same measures as Step 1.
- Group outcomes that move together. Separate correlations that hold by construction from ones that are informative.
- If two outcomes are nearly redundant (|association| ≥ 0.8 and not by construction), say so and recommend keeping one.

## Step 5: Two-parameter interactions (2D heat maps)
- Candidates are parameter pairs that are not aliased (Step 1) and have adequate cell counts.
- For each candidate pair and key outcome, estimate the interaction: the improvement of a model with A×B over the additive model A+B. Use the deviance or R² gain, or for binary outcomes the spread of cell rates around their additive prediction. Rank candidates by this, not by the main effects.
- For the top ~6–10 interactions, plus any 2D view that is scientifically expected or central to the research question, draw a 2D heat map:
  - rows = A, columns = B
  - colour = outcome on an absolute scale, so colours can be compared across charts
  - each cell shows its value and k/n
  - small cells are greyed out
- Explain each in words: "B matters only when A = …".

## Step 6: Filter and curate
Rank every relationship found by:
1. effect size
2. robustness: survives FDR, is not confounded, holds within subgroups, cells are not tiny
3. relevance to the research question
4. surprise relative to the design's expectations, if any are documented

Then sort them into three tiers:
- Headline (3–5): one chart each, a one-sentence takeaway, numbers with intervals, and a "why it matters / caveat" line.
- Supporting (3–6): a short paragraph each.
- Appendix: everything else (full screening table, all matrices, remaining heat maps).

Explicitly list relationships that look large but are not trustworthy, and why (confounded, by construction, tiny cells, classifier error).

## Chart rules
- Every chart has a title stating the takeaway, axis labels in plain words (no codes), and a colour bar with units.
- Use a single-hue sequential scale for magnitudes and a diverging scale centred at 0 for signed correlations. Keep the palette colour-blind safe.
- Print the value and n in every heat-map cell. If a heat map normalises per column, say so and keep the printed raw values.
- Order rows and columns meaningfully (by effect or by clustering), not alphabetically.
- Keep the chart count around 10–20, using small multiples rather than many one-off charts.

## Deliverables
- REPORT.md, plus an HTML version that embeds the figures. It should contain:
  1. One-paragraph summary
  2. How to read the charts (effect-size scales, what n means, normalisation)
  3. Design check: what can and cannot be separated
  4. Headline relationships
  5. Supporting relationships
  6. Univariate summaries
  7. Matrices
  8. 2D interactions
  9. Caveats in plain terms: small n, multiple comparisons, clustering, confounds, derived metrics
  10. File index
- figures/ (PNG, and SVG where useful)
- tables/, as CSV: univariate, screening table with all tests, matrices, the numbers behind every heat map
- analyze.py, which regenerates everything

## Report back
List of files; the headline relationships in one line each; the design-check result (aliased pairs); and any analysis you could not do reliably, with the reason.
```
