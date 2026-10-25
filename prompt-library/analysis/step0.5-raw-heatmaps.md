# Step 0.5: Raw heat maps (fast first look)

**Use it for:** the quickest, highest-value view of a finished (or partial) run. One-variable and two-variable heat maps of the **raw outcome rates** straight from `runs.csv`, before any derived metrics or statistics. It takes minutes, not hours.
**Pipeline stage:** before Step 1. Its output feeds Step 3 directly, so a findings draft can start before Steps 1–2 finish.
**Origin:** owner request (2026-10-25): *"raw heat maps for 1-variable and 2-variable vs. output metric pairs … This is the highest value item."* The reference implementation is [`tools/step0.5_raw_heatmaps.py`](tools/step0.5_raw_heatmaps.py). On the completed pressure study it produced 65 figures in about 1 minute.
**Next:** [Step 1](step1-extract-organize-augment.md), and [Step 3](step3-findings-briefing.md) for an early draft.

**Reference script:** [`tools/step0.5_raw_heatmaps.py`](tools/step0.5_raw_heatmaps.py) is specific to the 2026-10-25 pressure study (its factor and outcome names follow that `runs.csv`). Run it with `--results <RESULTS_DIR> --out <OUTPUT_DIR>`, and adapt `FACTORS` / `OUTCOMES` for other designs.

---

## Prompt

Make raw heat maps for the run in `<RESULTS_DIR>`, and write them to `<OUTPUT_DIR>`. Do this before anything else, and keep it fast.

**Inputs (fill in)**
- `<RESULTS_DIR>`: the run folder, containing `runs.csv`, with `manifest.json` for labels
- `<OUTPUT_DIR>`
- `<FACTORS>`: the design columns. Default: every manipulated or design column in `runs.csv`, e.g. level, monitoring, pairing, diagnostic or family, setting, each agent's criterion, and matched vs. mixed partner.
- `<OUTCOMES>`: the raw outcome rates you can compute directly from `runs.csv`, e.g. mutual take, lone take, both refuse, and each agent's take rate.

**Rules**
- **Use `runs.csv` only.** No derived metrics, no transcripts, no LLM calls.
- **Denominator:** rates are among **complete** trials, and the denominator is stated. Report how many trials are complete, failed and not started.
- **Every cell prints its rate and n.**
- **Colour:** an **absolute** 0–100% scale. Use one sequential colour map for everything.
- **Plain-word labels** from the pack: e.g. "Welfare + no rule", not `W-none`. Rows and columns go in a meaningful order (level 1→5, a fixed pairing order).
- **Data files:** write a CSV behind every chart.
- **Local compute:** run under the reserved-CPU launcher (`python tools/run_reserved.py <script>`). Never kill processes by name.
- **Interim snapshots:** label every figure **PRELIMINARY**.

**Deliverables**
1. **One variable × outcomes:** one heat map per factor. Rows are the factor's levels, columns are the outcomes.
2. **Two variables × outcome:** for every pair of factors (skip pairs that are identical by design, e.g. pairing vs. rule), a heat map for each key outcome (mutual take, lone take, rule-agent take). Rows are factor A, columns are factor B.
3. **The most granular view:** scenario × level for the main outcome.
4. **`README.md` (+ `.html`):** what was counted, how to regenerate, every figure linked, and 4–6 highlight figures embedded (e.g. level × monitoring, level × pairing, monitoring × pairing, scenario × level).
5. **The script**, so it can be rerun.

**Report back:** the figure count, the runtime, the complete, failed and not-started counts, and 3–5 patterns that stand out. Label those patterns descriptive, not tested.

**Don't:** run significance tests or make causal claims here. Step 2 does that. Step 0.5 shows where to look.
