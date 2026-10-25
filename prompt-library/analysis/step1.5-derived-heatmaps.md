# Step 1.5: Derived-metric heat maps

**Use it for:** a fast visual of every **derived or engineered** outcome from Step 1: interaction metrics, vocabulary, plans vs. actions, and deception flags, broken down by every design factor. It runs straight after Step 1, before any statistics.
**Pipeline stage:** after [Step 1](step1-extract-organize-augment.md), before [Step 2](step2-analyze-and-report.md). Like Step 0.5, it can feed a Step 3 draft early.
**Origin:** owner request (2026-10-25): *"add step 1.5 for any derived / engineered feature output variables."* The reference implementation is [`tools/step1.5_derived_heatmaps.py`](tools/step1.5_derived_heatmaps.py). On a 3,026-episode table it produced 71 figures in about 90 seconds.
**Previous:** [Step 0.5](step0.5-raw-heatmaps.md) (raw outcomes) and Step 1.

**Reference script:** [`tools/step1.5_derived_heatmaps.py`](tools/step1.5_derived_heatmaps.py) is specific to the 2026-10-25 pressure study's Step 1 table. Pass `--table`, `--schema` and `--out` explicitly, because its defaults assume that run's folder layout. Adapt `FACTORS` / `ALIASES` for other designs.

---

## Prompt

Make heat maps of the derived metrics in `<TABLE>`, using `<SCHEMA>`, and write them to `<OUTPUT_DIR>`.

**Inputs (fill in)**
- `<TABLE>`: Step 1's `trial_metrics.csv`
- `<SCHEMA>`: Step 1's `metrics_schema.json`
- `<OUTPUT_DIR>`
- `<FACTORS>`: default is level, monitoring, pairing, diagnostic or family, setting, and, for agent-level metrics, the agent's own criterion

**Rules**
- **Pick metrics from the schema:** role `outcome`, in the `agent` or `pair` sections, of type `binary`, `numeric` or `ordinal`. Skip `empty` and `constant` columns.
- **Agent-level metrics:** pool each `_a` / `_b` pair into one metric over agents, and use the agent's own criterion as a factor.
- **Binary metrics:** show rates on an **absolute** 0–100% scale.
- **Numeric metrics:** show medians, shaded within their column, with the value printed. Say clearly that the shading is per column.
- **Mark validation status in the labels:**
  - **⚠ unreliable:** heuristics whose schema validation says `reliable: false`
  - **(unvalidated):** heuristics with no validation
- **Monitoring contrasts:** when a heuristic's accuracy differs by experimental arm, state it in the README, and don't read anything into its watched vs. unwatched difference.
- **Column names:** tolerate naming differences between table versions, e.g. `diagnostic` vs. `scenario_diagnostic`. Skip a factor that's absent, rather than failing.
- **Every cell prints its value and n.** Write a CSV behind every chart. Use plain-word labels.
- **Legible on screen.** Size the cell numbers to the cell, never below 10 pt for values at the saved size. Show the value bold, with n on a smaller second line. On large heat maps, enlarge the figure or cells instead of shrinking the text, and split very wide maps into chunks. Open the saved image to check it before reporting.
- **Local compute:** run under the reserved-CPU launcher (`python tools/run_reserved.py <script>`). Never kill processes by name.
- **Interim snapshots:** label every figure **PRELIMINARY**.

**Deliverables**
1. **One factor × derived metrics:** pair-level and agent-level separately, with rates and medians separately. Split into chunks of about 10 metrics per figure.
2. **Two factors × derived metric:** for the binary metrics that vary most across the main factor (e.g. pressure level), heat maps of level × monitoring, pairing × monitoring, family × monitoring, and level × pairing.
3. **`README.md` (+ `.html`):** the source table, the metric counts, the reliability legend, how to regenerate, every figure linked, and the highlights embedded.
4. **The script**, so it can be rerun.

**Report back:** the figure count, the runtime, how many metrics were included and excluded, and 3–5 patterns that stand out. Label those patterns descriptive, and caveat any that involve ⚠ columns.

**Don't:** run statistical tests or headline ⚠ columns here. Step 2 does the inference.
