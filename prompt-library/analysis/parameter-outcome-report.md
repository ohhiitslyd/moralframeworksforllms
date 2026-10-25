# Parameter → outcome relationship report

**Use it for:** helping a human quickly understand which experiment parameters (fewer than about 30) matter for which outcome metrics (fewer than about 20), through charts and summary statistics.
**Pipeline stage:** Stage 2 of [`analysis-pipeline/PROCESS.md`](../../analysis-pipeline/PROCESS.md). This page is the standalone, copy-paste version. **If `PROCESS.md` is available, it takes precedence.**
**Origin:** generalised from the dimension-by-metric analysis of the first pressure-pack run (branch `first-run-summary-analysis`).

---

## Prompt

You are analysing an experiment's results so a human can quickly understand which parameters matter for which outcomes, visually and with summary statistics. Stop once you've produced ranked candidates. Choosing headline findings and writing the narrative is Stage 3.

**Inputs (fill in)**
- Data file: `<path>`. One row per `<unit>`.
- Clustering: `<e.g. "per-agent columns _a/_b, two agents per episode"; "scenario / template"; or "none">`
- Parameters: `<list, or "schema role = parameter">`. Outcomes: `<list, or "schema role = outcome">`
- Schema or dictionary: `<path to metrics_schema.json / dictionary>`
- Known design facts: `<e.g. one seed per cell; provider switched mid-run>`
- Output folder: `<path>`. Audience: `<who>`

**Ground rules**
- Treat the input data as read-only.
- Put everything in one rerunnable script, with fixed random seeds.
- Every number comes with its n.
- Never give a p-value without an effect size and a 95% interval. Get intervals for rates from the Wilson method, and for other effect sizes from a cluster bootstrap.

**Steps**

0. **Type and reshape**
   - **Type each variable** as numeric, ordinal, categorical or binary, and record missingness, levels and cell counts.
   - **Flag four kinds of column:** outcomes that apply only to a subset (state their denominator); outcomes related by construction (from the schema's `by_construction_with`), which must never be reported as findings; heuristic columns, with their validated accuracy; and clusters.
   - **Reshape per-agent `_a` / `_b` columns to long format** (one row per agent) for agent-level analysis.

1. **Design check (parameter × parameter)**
   - **Build a mixed-type association matrix:** Spearman ρ (numeric–numeric), bias-corrected Cramér's V (categorical–categorical), correlation ratio η (numeric–categorical).
   - **Draw cell-count tables** for every pair with association ≥ 0.3, or with empty or tiny cells.
   - **State which effects are aliased,** and which comparisons are clean (e.g. "within provider X, family varies freely").

2. **Univariate summaries**
   - **Parameters:** counts per level, to show balance.
   - **Outcomes:** binary rates with 95% Wilson intervals; numeric medians and IQRs, with histograms (log or rank scale if skewed).
   - **One summary table.**

3. **Parameter × outcome screening**
   - **Effect sizes, on a comparable scale:** V for categorical × binary; √ε² (η-like) for categorical × numeric; |ρ| for ordinal or numeric parameters. Also report the raw max−min spread of rates or medians, so readers see magnitudes.
   - **p-values:**
     - Use Fisher's exact test for 2×2 tables.
     - Otherwise use permutation tests, with at least **20·m/α shuffles for m tests**, so BH can still detect a single real effect. For example, 600 tests need about 240,000 shuffles. Stop early once p is clearly above 0.1, use an exact or asymptotic p where it's valid, and report the shuffle count.
     - **Make the tests cluster-aware:** permute whole episodes for episode-level parameters; for agent-level parameters (such as each agent's criterion in mixed pairings), permute within episodes; treat scenario or template as a stratum.
   - **Correct for multiple comparisons:** Benjamini–Hochberg q-values across all pairs.
   - **Screening table,** sorted by the comparable effect size. Columns: effect, interval, p, q, minimum cell n, clean or confounded, by-construction flag, heuristic flag.
   - **One single-factor heat map per key parameter.** Rows are the parameter's levels and columns are outcomes; print the value and n in each cell. Use an absolute colour scale per outcome type (rates 0–1). If you do normalise colour per column, mark cells that aren't significant so trivial differences don't look large. Mark cells with q < 0.05, and hatch confounded cells.
   - **Top relationships** (q < 0.05 and minimum cell n ≥ 10): draw level-by-outcome charts with intervals, and repeat each comparison **within** the levels of any confounder.

4. **Outcome × outcome**
   - **Build the same association matrix over outcomes.**
   - **Separate by-construction correlations from informative ones.**
   - **Flag redundant outcomes** (|association| ≥ 0.8 and not by construction).

5. **Two-parameter interactions**
   - **Candidates:** only parameter pairs that aren't aliased and have adequate cell counts.
   - **Interaction strength:** for binary outcomes, the likelihood-ratio (deviance) improvement of A×B over additive A+B on the **logit** scale; for numeric outcomes, the same on the rank scale. Penalise by the extra degrees of freedom, and get a permutation p-value.
   - **Draw 2D heat maps** only for the pairs that pass (at most 6–10), plus any pair central to the research question. Use an **absolute** colour scale, print the value and k/n in each cell, and grey out small cells. If no pair passes, say so.
   - **Describe each map in words,** e.g. "B matters only when A = …".

6. **Rank candidates for Stage 3** (do not choose headlines here)
   - **Score every relationship** on effect size, robustness (FDR, clean vs. confounded, holds within subgroups, cell sizes), relevance to the research questions, and surprise relative to the design's expectations.
   - **Write `tables/candidates.csv`,** including a "looks large but untrustworthy" list with the reasons.

**Chart rules**
- Titles state the takeaway.
- Axis labels in plain words, never codes.
- Colour bars with units.
- A sequential scale for magnitudes; a diverging scale centred at 0 for signed values; colour-blind safe.
- Value and n printed in every cell.
- Rows and columns ordered meaningfully.
- About 10–20 charts.

**Deliverables**
- **`REPORT.md` + HTML,** with these sections:
  1. summary
  2. how to read the charts
  3. design check
  4. top-ranked relationships (from `candidates.csv`)
  5. univariate results
  6. matrices
  7. single-factor heat maps
  8. 2D interactions
  9. caveats in plain terms
  10. file index
- **`figures/`, `tables/` (CSV, including `candidates.csv`) and the script.**

**Report back:** files; one line per top candidate; the aliased pairs; and anything you couldn't analyse reliably, with the reason.
