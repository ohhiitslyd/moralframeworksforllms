# Extended pressure run: preliminary analysis (snapshot 2026-10-25 15:29 UTC)

**Status: PRELIMINARY.** This analyses an interim snapshot: 3,026 of 4,320 trials complete, 60 failed and 1,234 not started (71% finished). The completed run (4,243 of 4,320) is analysed separately on branch `analysis-full-pressure-study`. Use this folder for the method and early results, not as final numbers.

| Step | Status | Start here |
|---|---|---|
| Plan | Done; revised after review | [ANALYSIS-PLAN.md](ANALYSIS-PLAN.md) |
| **Step 1:** extract, organise, augment | Done. Small schema gaps remain (randomisation level, `paired_by`, run status), to be fixed in the full-run version | [step1/trial_metrics_dictionary.md](step1/trial_metrics_dictionary.md) |
| **Step 2:** analyse and report | Done. A review flagged overclaims, to be fixed in the full-run version (see caveats below) | [step2/REPORT.md](step2/REPORT.md) |
| **Step 3:** findings briefing and paper kit | Not run on the snapshot; it will be run on the completed dataset | — |

## Contents

**Plan**
- [ANALYSIS-PLAN.md](ANALYSIS-PLAN.md) ([HTML](ANALYSIS-PLAN.html)): questions, the pre-specified primary test (Revision 1) and what not to claim

**Step 1** ([`step1/`](step1/))
- [trial_metrics.csv](step1/trial_metrics.csv): 4,320 planned trials × 188 columns
- [trial_metrics_dictionary.md](step1/trial_metrics_dictionary.md) ([HTML](step1/trial_metrics_dictionary.html)):
  - conventions
  - reliability summary
  - A. inputs (65)
  - B. outcomes (8)
  - C. per-agent (94)
  - D. pair (21)
  - changes from v1
  - considered, not included
  - caveats
  - regex appendix
- [VALIDATION.md](step1/VALIDATION.md) ([HTML](step1/VALIDATION.html)): blind, arm-stratified checks of each heuristic against hand labels
- [metrics_schema.json](step1/metrics_schema.json), [validation_results.json](step1/validation_results.json) and `validation/labels_*.csv` (hand labels)
- Scripts: [build_metrics_e1.py](step1/build_metrics_e1.py), [validate_e1.py](step1/validate_e1.py), [gen_docs.py](step1/gen_docs.py)

**Step 2** ([`step2/`](step2/))
- [PREREG.md](step2/PREREG.md) ([HTML](step2/PREREG.html)): primary hypothesis and test, written before the outcome numbers
- [REPORT.md](step2/REPORT.md) ([HTML](step2/REPORT.html)), with these sections:
  1. Summary
  2. How to read the charts
  3. Design check and completion
  4. **Primary test** (monitoring notice → mutual take)
  5. Top-ranked relationships
  6. Words vs. actions
  7. Univariate results
  8. Matrices
  9. **Heat maps**
  10. Two-factor interactions
  11. Sensitivity
  12. Caveats in plain terms
  13. File index
- [figures/](step2/figures/) (18 PNGs):
  - Headline figures:
    - [03 primary forest](step2/figures/03_primary_monitoring_forest.png)
    - [05 asymmetry](step2/figures/05_asymmetry_mixed_pairs.png)
    - [06 rule application](step2/figures/06_rule_application.png)
  - Heat maps:
    - [07 overview](step2/figures/07_screening_overview.png)
    - [08 level](step2/figures/08_heat_level.png)
    - [09 monitoring](step2/figures/09_heat_monitoring.png)
    - [10 pairing](step2/figures/10_heat_pairing.png)
    - [11 diagnostic](step2/figures/11_heat_diagnostic.png)
    - [12 setting](step2/figures/12_heat_setting.png)
    - [16 outcome × outcome](step2/figures/16_outcome_association.png)
    - [17 2D](step2/figures/17_2d_heatmaps.png)
    - [18 scenario × level](step2/figures/18_scenario_x_level.png)
- [tables/](step2/tables/): the CSV behind every chart, plus `candidates.csv` and `candidates_untrustworthy.csv`
- Script: [analyze_e1.py](step2/analyze_e1.py), plus [provenance.json](step2/provenance.json)

## Headline (preliminary)

**The monitoring notice reduces mutual take.** 25.0% of watched trials ended in a mutual take, against 29.3% unwatched: a paired difference of **−4.2 pp** (95% CI −6.0 to −2.4).
- The comparison uses the 1,046 cells where both trials completed. In the cells where the two differ, 68 took only when unwatched and 24 only when watched (McNemar p = 7×10⁻⁶).
- The effect is the same sign in every factor, and the same on both endpoints.
- It does **not** survive the worst-case failure assumption: −1.4 pp, p = 0.20.
- On the completed dataset it is −3.9 pp (131 vs 49 discordant cells, p = 8×10⁻¹⁰).

## Known overclaims (from the Step 2 review; fixed in the full-run version)

- "A slightly smaller deal, talked about more openly" is **not supported**. The public-vocabulary shift is probably an audience effect, and its meaning hasn't been validated.
- The private monitoring-mention finding is mostly agents echoing the notice text. Drop it.
- The interaction p-values sit at the floor of a 100-draw bootstrap, and diagnostic × pairing is built into the design.
- The heuristic-error sensitivity table is mis-specified.
