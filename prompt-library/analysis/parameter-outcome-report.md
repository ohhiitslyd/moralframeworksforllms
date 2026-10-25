# Parameter → outcome relationship report

**Use it for:** helping a human quickly understand which experiment parameters (fewer than about 30) matter for which outcome metrics (fewer than about 20), through charts and summary statistics.
**Pipeline stage:** Stage 2 of [`analysis-pipeline/PROCESS.md`](../../analysis-pipeline/PROCESS.md). The full step-by-step specification is there. This page is the standalone, copy-paste version.

---

## Prompt

You are analysing an experiment's results so a human can quickly understand which parameters matter for which outcomes, visually and with summary statistics.

**Inputs (fill in)**
- Data file: `<path>`. One row per `<unit>`.
- Clustering: `<e.g. two agent rows per episode / none>`
- Parameters: `<list, or "schema role = parameter">`. Outcomes: `<list, or "schema role = outcome">`
- Data dictionary or schema: `<path>`
- Known design facts: `<e.g. one seed per cell; provider switched mid-run>`
- Output folder: `<path>`. Audience: `<who>`

**Ground rules**
- Treat the data as read-only.
- Put everything in one rerunnable script, with fixed random seeds.
- Every number comes with its n.
- Never give a p-value without an effect size and an interval.

**Steps**
0. **Type the variables.** Mark each as numeric, ordinal, categorical or binary. Record missingness, levels and cell counts. Flag outcomes that only apply to a subset, outcomes related by construction, heuristic columns (with their accuracy), and clustering.
1. **Design check (parameter × parameter).**
   - Build a mixed-type association matrix: Spearman ρ, bias-corrected Cramér's V, correlation ratio η.
   - Draw cell-count tables for associated or sparse pairs.
   - State which effects are aliased and which comparisons are clean.
2. **Univariate summaries.**
   - Parameter balance.
   - Binary outcome rates with Wilson intervals; medians and IQRs, with histograms.
   - One summary table.
3. **Parameter × outcome screening.**
   - Effect sizes: V plus rate spread, ε² plus median spread, or ρ.
   - Permutation tests, cluster-aware where needed.
   - Benjamini–Hochberg q-values.
   - A screening table, plus one heat map per key parameter: values and n printed, colour normalised per column, significant cells marked, confounded cells hatched.
   - Level-by-outcome charts for the top relationships, with the comparison repeated *within* the levels of any confounder.
4. **Outcome × outcome.**
   - Draw the association matrix.
   - Separate by-construction correlations from informative ones.
   - Flag redundant outcomes.
5. **Two-parameter interactions.**
   - Use only pairs that aren't aliased.
   - Rank them by interaction strength (A×B vs. additive A+B), not by main effects.
   - Draw 6–10 2D heat maps on an **absolute** colour scale, each cell showing its value and k/n, with small cells greyed out.
   - Describe each in words.
6. **Filter and curate.**
   - Rank by effect size, robustness, relevance and surprise.
   - Tier the results: headline (3–5), supporting (3–6), appendix.
   - List the relationships that look large but aren't trustworthy, and why.

**Chart rules**
- Titles state the takeaway.
- Axis labels in plain words; no codes.
- Colour bars with units.
- A sequential scale for magnitudes and a diverging scale centred at 0 for signed values. Colour-blind safe.
- Value and n printed in every cell.
- Rows and columns ordered meaningfully.
- About 10–20 charts.

**Deliverables**
- `REPORT.md` + HTML, containing:
  1. summary
  2. how to read the charts
  3. design check
  4. headline relationships
  5. supporting relationships
  6. univariate results
  7. matrices
  8. 2D interactions
  9. caveats in plain terms
  10. file index
- `figures/`, `tables/` (CSV) and the script.

**Report back:** files, one line per headline relationship, the aliased pairs, and anything you could not analyse reliably, with the reason.
