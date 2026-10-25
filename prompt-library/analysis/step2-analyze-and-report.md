# Step 2: Analyse and produce reports (original prompts)

**Use it for:** single-variable, two-variable and three-variable analysis of a per-trial table. That covers distributions, correlation matrices (parameter × parameter, parameter × outcome, outcome × outcome), single-factor heat maps, and two-input × one-output heat maps, filtered down to the relationships that are non-random, interesting or important, with written commentary.
**Pipeline stage:** Stage 2 of [`analysis-pipeline/PROCESS.md`](../../analysis-pipeline/PROCESS.md), with its curation step leading into Stage 3.
**Origin:** the requests and prompts actually used on the first pressure-pack run (2026-10-24). They produced `analysis/qwen-pressure-final-20261024-181708/dimension-metric-analysis/` on branch `first-run-summary-analysis`.
**Recommended version:** [`parameter-outcome-report.md`](parameter-outcome-report.md) is the generalised, expert-reviewed prompt built from these, with corrected statistics. Use it for new runs. This page keeps the originals for provenance and reuse.

---

## 1. Original requests (verbatim, from the project owner)

**Request C: univariate and bivariate analysis with heat maps**

> OK thanks, can you also perform univariate and bivariate analysis of dimensions vs. metrics, producing heat maps for each (in some easily digestible format), and providing analysis or commentary on the most interesting relationships?

**Request D: a general-purpose prompt for this kind of report**

> Thanks, what's the best way to prepare reports for a human to quickly, visually and via summary-statistics, grok the relationships between a small number of experiment parameters (let's say fewer than 30) and a small number of outcome metrics (let's say fewer than 20)? I'm thinking, maybe correlation matrices (parameter-parameter, parameter-outcome, outcome-outcome), heat maps of the least random single-dimension relationships and 2d heatmaps (2 input variables vs. one output variable), also filtered for anything clearly non-random, experimentally interesting, correlated, or otherwise exhibiting important relationships? Please produce a general purpose prompt for this

## 2. Prompt sent to the analysis agent for Request C (verbatim)

The scratchpad and worktree paths have been replaced by placeholders.

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

## 3. General-purpose prompt as first proposed for Request D (verbatim)

This is the version proposed in answer to Request D, before the expert review. The reviewed version, [`parameter-outcome-report.md`](parameter-outcome-report.md), fixes several statistical issues: permutation resolution under the Benjamini–Hochberg correction, comparable effect-size scales, logit-scale interaction tests, and cluster-aware testing. **Prefer the reviewed version.**

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
