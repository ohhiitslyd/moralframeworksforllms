# Analysis pipeline: code design

This is the code design for the scripts that implement [`PROCESS.md`](PROCESS.md): Stage 1 (metrics) and the deterministic part of Stage 2 (relationships). Stage 3 stays a judgement task for an analyst or agent, driven by `PROCESS.md` and the prompt library.

Status: **revised after design review** (see §8, which takes precedence over earlier sections where they differ). Branch `analysis-pipeline`.

## 1. Goals and non-goals

**Goals**
- **One command per run:** `python analysis-pipeline/run_pipeline.py --results <run dir> --out <dir>`. It writes `trial_metrics.csv`, `metrics_schema.json`, the dictionary, `REPORT.md`, figures, tables and `candidates.csv`, with HTML copies.
- **Works on both run formats we have:**
  - **v1 pressure pack** (`qwen-pressure-final-20261024-181708`): 600 trials, `provider` and `deal_taken` columns, v1 rule-report keys.
  - **Extended pack** (`qwen-pressure-72-v1-snapshot-*`): 4,320 planned trials, `monitoring` / `setting_id` / `diagnostic` columns, `not_started` rows, v5 rule-report keys, no `provider` column.
- **Backward compatible.** On the v1 run, every column in the published `trial_metrics.csv` is reproduced with identical values. New columns are added, and none are removed.
- **Schema-driven Stage 2.** No hard-coded column names, so the same code works for any run whose Stage 1 writes a schema.

**Non-goals (for now)**
- LLM-judge classification. That needs a cost estimate and approval first.
- Reorganising existing result folders.
- Changes to the harness.

## 2. Validation datasets (the experimental design for this tooling)

| Dataset | Where | Used for |
|---|---|---|
| **V1:** `results/qwen-pressure-final-20261024-181708` | branch `first-run-summary-analysis` (local main checkout) | Stage 1 regression: must match the published `analysis/…/trial_metrics.csv`. Stage 2 check: headline numbers must match the published `REPORT.md`, e.g. family collusion 15/202, 115/205 and 36/179, and authority take 29/33 when rank is stated. |
| **E1:** `results/qwen-pressure-72-v1-snapshot-20261025-141425` | branch `experiment-harness-pilot-results`, extracted with `git archive` into the scratchpad | Generality check: 4,320 rows; status counts match `summary.json` (1,862 complete, 2,418 not started, 40 failed); outcome counts match (477 mutual, 129 unilateral, 1,256 both refuse). Stage 2 runs end to end. |

Tests find the datasets through the environment variables `PIPELINE_V1_RESULTS`, `PIPELINE_V1_CSV` and `PIPELINE_E1_RESULTS`. A test is skipped, with a message saying why, when its variable isn't set.

## 3. Layout

```
analysis-pipeline/
  PROCESS.md, DESIGN.md
  run_pipeline.py            CLI: --results --out [--stages metrics,report] [--shuffles N] [--seed S]
  pipeline/
    __init__.py
    runio.py                 I1  load a run: manifest, runs.csv (column-tolerant), per-run files
    pack.py                  I2  PackView: scene/level lookup, families, descriptions, text features, report keys
    heuristics.py            I3  text heuristics: stance, deception vocabulary, agreement, lone take, criterion report
    extract.py               I4  Stage 1: rows + ordered columns
    schema.py                I5  metrics_schema.json + trial_metrics_dictionary.md
    column_docs.json         I5  per-column documentation (seeded from the published dictionary)
    stats.py                 I6  Wilson, Fisher, V, eta, eps2, Spearman, permutations, BH, bootstrap
    charts.py                I7  heat maps, rate bars, distributions (current palette, light/dark)
    screen.py                I8  Stage 2 Steps 0–6, writing tables/ and figures/
    report.py                I8  REPORT.md assembly (numbers and figure links; commentary placeholders)
  tests/
    test_stats.py            T3  known-answer tests
    test_stage1_v1.py        T1  regression against the published V1 CSV
    test_stage1_e1.py        T4  extended-run counts and statuses
    test_schema.py           T2  schema covers every column; roles and types valid
    test_stage2_v1.py        T5  headline numbers match the published REPORT.md
tools/md_to_html.py          (already on main) HTML copies
```

Only the standard library plus `pandas`, `numpy`, `matplotlib` and `markdown` are needed. `scipy` is not installed, so the statistics are implemented in `stats.py`.

## 4. Interfaces

### I1 `runio.py`
```python
@dataclass
class Trial:
    run_id: str
    spec: dict          # from result.json["spec"] if present, else built from runs.csv
    status: str         # complete | failed | not_started | running
    action_a: str|None
    action_b: str|None
    outcome: str        # mutual_take | unilateral_take | both_refuse | failed | not_started
    deal_taken: bool|None
    error: str
    provider: str       # runs.csv "provider" if present, else derived from response endpoints (see below)
    run_dir: Path|None  # None when the trial has no folder
    extra: dict         # any other runs.csv columns, passed through

def load_run(results_dir) -> tuple[dict, list[Trial]]   # (manifest, trials in runs.csv order)
def load_responses(run_dir) -> dict[(agent, stage, exchange), event]
```
- **`deal_taken`** comes from the `deal_taken` column, or from `outcome == "mutual_take"`.
- **Status** comes from runs.csv, and is cross-checked against `result.json`.
- **Provider, when the column is missing:**
  - Map each response's endpoint `base_url` to a short name: `huggingface` gives `HF`, `modal.run` gives `Modal`, and anything else gives its host name.
  - The trial's provider is the sorted join of those names, so mixed trials come out as `HF+Modal`.
  - A trial with no responses gets a blank provider.

### I2 `pack.py`
```python
class PackView:
    def __init__(self, pack: dict, manifest: dict)
    scenes: dict[id, scene]
    def level(scene_id, n) -> dict
    def family(scene) -> str
    def family_description(family) -> str
    def diagnostic_description(diag) -> str
    def criterion_description(crit) -> str
    def pairing_description(a, b) -> str
    def setting_description(setting_id) -> str
    def monitoring_description(mode) -> str
    def scene_source(scene) -> "authored" | "template" | "unknown"
    def text_features(scene, level) -> dict
    report_keys: dict[criterion, dict]
```
- **Family** comes from `diagnostic`: welfare → `rule_breaking`, nondeception → `promise_vs_record`, authority → `boss_vs_rulebook`. The names are kept for backward compatibility.
  - The v1 descriptions are reproduced exactly. The ID range, e.g. "(S01-S07)", is computed from the pack's scene IDs when they're contiguous, and replaced by "(N scenes)" otherwise.
- **`criterion_description`** uses the v1 summary text when the pack's criterion block equals the v1 block. Otherwise it uses the first sentence of the block.
- **`scene_source`** uses an explicit pack field if one exists (`source` / `generated`). Otherwise it applies the template title patterns (`^Leftover .* book$`, `^True .* vs promised wording$`, ` override$`) and marks the result `template?`, i.e. a heuristic. It returns `unknown` for v1, where every scene is authored and has no field.
- **`text_features`** is ported unchanged from `build_metrics.py`: take principal, soft take principal, non-principal voice, rank stated, take/refuse deceives lists and counts, promise, welfare judgement, expected tipping point, justified/ambiguous.
- **`report_keys`** are parsed from each criterion block's text, so later code knows which report lines to look for:
  - authority: `highest_principal_who_has_spoken` or `highest_principal`, plus `their_instruction`
  - nondeception: `deceive_if_take` / `deceive_if_refuse`, or none
  - welfare: `welfare_take` / `welfare_refuse`, or `welfare_accept` / `welfare_refuse`

### I3 `heuristics.py`
- The v1 regexes and functions (`stance`, `deception_count`, `take_linked_deception_sentences`, `LONE_AWARE_RE`, `AGREE_RE`, `EVALUATOR_RE` and so on) are moved **verbatim**, with a version tag `HEURISTICS_VERSION = "v1"`.
- `criterion_report(crit, text, keys)` is generalised to use `report_keys`. When the keys are the v1 ones, it behaves exactly as before.
- If a pack has no nondeception report keys, its compliance columns are left blank, and the schema records "not reported by this pack".

### I4 `extract.py`
```python
def build_rows(manifest, trials, pack_view) -> tuple[list[dict], list[str]]   # rows, ordered columns
```
- The column order matches v1: inputs, then outcomes, then interleaved per-agent pairs, then pair columns.
- **New input columns**, each placed after its v1 neighbour: `setting_id` (+ description), `monitoring` (+ description), `scene_source`, `order_seed`, and `selection_method` (from `pack.selection`).
- **Rows that never ran.** Rows with `not_started` or `running` keep only their input columns.
- **Model name** comes from the manifest endpoint or config, not the hard-coded "Qwen3-32B".

### I5 `schema.py`
- **`column_docs.json`** is seeded once by parsing the published `trial_metrics_dictionary.md` tables, and new columns are added by hand.
- **Type inference:**
  - `binary` if the values are only {0, 1, blank}
  - `numeric` if all values parse as numbers and there are more than 10 levels
  - `ordinal` for `level` and other declared ordinals
  - `categorical` if there are 30 levels or fewer
  - `text` otherwise
- **Roles:**
  - `id`: `run_id`
  - `description`: `*_description`, `*_title`, `*_label`, `principals_text`
  - `meta`: run settings that are constant, provider-recovery flags, tokens, `served_models`, `error`
  - `parameter`: the remaining inputs
  - `outcome`: the outcome, per-agent and pair columns
- **`level`** is `agent` for `_a` / `_b` pairs and `trial` otherwise.
- **Registries.** `by_construction_with` and `heuristic` + `validation` come from small registries in `schema.py`, seeded from the published dictionary's validation section, e.g. the stance classifier at 0.88 held-out on V1. Validation is recorded **per pack**: on E1, heuristic columns get `validation: null` and the flag "not validated for this pack" until someone validates them.
- **Outputs:** the dictionary Markdown is generated from the schema plus `column_docs.json`, and the HTML comes from `tools/md_to_html.py`.

### I6 `stats.py`
- Functions are ported from `analyze_dimensions.py` and generalised: `wilson(k, n)`, `fisher_2x2`, `odds_ratio`, `cramers_v(table, bias_corrected=True)`, `eta(x, groups)`, `eps2(x, groups)`, `spearman(x, y)`, `bh(p)`, `cluster_bootstrap(stat, data, clusters, B, seed)`.
- **`perm_test(stat, x, y, n_perm, seed, strata=None, clusters=None, within=None)`**:
  - stops early once p > 0.1 is certain at 99% confidence
  - permutes `clusters` (whole episodes) for episode-level parameters
  - permutes within `within` for agent-level parameters
  - shuffles within `strata` such as scenario or template
- **Shuffle count:** `n_perm = max(2000, ceil(20 * m / alpha))` for m tests, which is configurable.

### I7 `charts.py`
- Functions: `heat_dim_metric(...)`, `heat_2d(...)`, `rate_bars(...)`, `distributions(...)`, `assoc_matrix(...)`. They are ported from `analyze_dimensions.py` and keep its palette and conventions: values and n printed in cells, absolute scales for 2D maps and rates, and non-significant cells marked when colour is normalised per column.
- Labels always come from the description and title columns via the schema.

### I8 `screen.py` / `report.py`
These implement `PROCESS.md` Stage 2, Steps 0–6, using only the schema:
- **Parameters** are columns with `role == parameter` that aren't constant and are categorical, ordinal, binary or numeric. Text parameters are excluded.
- **Outcomes** are columns with `role == outcome` that aren't `text`. Agent-level pairs are reshaped to long format.
- **Heat map count** is capped by `--max-heatmaps`, default 8: the parameters with the largest mean |effect|, plus `level`, `pairing` and any parameters named by `--focus`.
- **Interactions** are only computed for non-aliased pairs (association < 0.3) with a minimum cell count of 5 or more. They use a penalised logit likelihood-ratio test, fitted by a small IRLS implementation in `stats.py`, plus a permutation p.
- **`REPORT.md`** gets every number, table and figure. Each narrative slot is marked `<!-- COMMENTARY: … -->` for the Stage 3 agent to fill in.

### I9 `run_pipeline.py`
Runs Stage 1 and then Stage 2, writes the HTML copies, and prints a summary with the files, counts, timings and skipped items.

## 5. Increments, dependencies and parallel plan

```
Wave 1 (parallel, no shared files):  I1 runio   I2 pack   I3 heuristics   I6 stats(+T3)   I7 charts
Wave 2 (parallel):                   I4 extract(+T1,T4)  [needs I1–I3]     I5 schema(+T2)  [needs the V1 header; final check after I4]
Wave 3:                              I8 screen/report(+T5) [needs I5, I6, I7]
Wave 4:                              I9 CLI + integration runs on V1 and E1
```

Each increment is built by its own fresh subagent and reviewed by another fresh subagent, with **one commit per increment**. Reviews happen at four points: design (this document), each wave's implementation, test design, and the final results. The work ships as **two PRs**, one for Stage 1 (I1–I5 and its tests) and one for Stage 2 (I6–I9), so each stays small.

## 6. Test design

| Test | Kind | Pass criteria |
|---|---|---|
| **T3** `test_stats` | unit | Known answers: Wilson(15, 202) ≈ [0.045, 0.119]; Fisher's p on a textbook 2×2; V = 0 under independence and 1 under a perfect relationship; BH matches a hand-computed example; Spearman on a monotone sequence = 1; permutation p within ±0.01 of the exact value on a small case; bootstrap is deterministic given a seed |
| **T1** `test_stage1_v1` | regression | Same 600 run IDs. Every published column is present with **identical** values (strings compared after normalising blanks). The only allowed differences are new columns. |
| **T4** `test_stage1_e1` | integration | 4,320 rows; status and outcome counts match `summary.json`; every row has setting and monitoring; trials that never ran have blank outputs; `scene_source` is filled in |
| **T2** `test_schema` | unit | Every CSV column has a schema entry; roles and types are valid; every identifier's `description_column` exists; `by_construction_with` points only at real columns |
| **T5** `test_stage2_v1` | regression | `tables/` reproduce the published headline numbers (family collusion counts; authority take when rank is stated, 29/33; non-deception take when refusing breaks a promise, 95/111); the screening table includes V for scenario family vs. collusion ≈ 0.47 |

## 7. Risks

- **The stance and deception heuristics were tuned on v1 deals.** On E1, the scenario nouns differ and the deal is called "the action". They will run, but they're flagged as unvalidated for that pack. Validation needs a transcript sample, which is a judgement task. It's listed as a follow-up in the PR.
- **E1 is a live snapshot.** Tests compare against its own `summary.json`, not fixed numbers.
- **Runtime.** E1 has about 1,862 complete trials, each with 10 responses. Parsing is fast. Stage 2 permutation tests with the BH-scaled shuffle count are the slowest part, so early stopping and vectorised permutations are required. The target is under 10 minutes per run on a laptop.

## 8. Design review resolutions (revision 1)

An independent review found 14 issues (5 high). As a baseline check, it reran the v1 `build_metrics.py`, which reproduces the published CSV exactly: 600×162, 0 differing rows, about 42 s. **This section overrides earlier sections where they differ.**

### High
1. **Model column.**
   - `model` keeps v1's normalised value: `Qwen/Qwen3-32B:<anything>` and `Qwen--Qwen3-32B--…` both become `Qwen3-32B`. Unknown names pass through unchanged.
   - The raw endpoint name goes in a new column, `model_endpoint`.
2. **p-values for the screen.**
   - **Screening uses asymptotic or exact p-values,** computed by `stats.py` without scipy:
     - Fisher's exact test for 2×2 tables
     - χ² with Monte-Carlo fallback for sparse tables
     - the Spearman t-approximation
     - Kruskal–Wallis χ²
   - **By-construction pairs are dropped before m (the number of tests) is counted.**
   - **Permutation tests are only for confirmation:** pairs with asymptotic q < 0.1, plus every cluster-structured test.
     - They use Besag–Clifford sequential stopping (stop after h = 10 exceedances), capped at `--max-shuffles` (default 20,000).
     - The reported p-floor is 1/(shuffles + 1).
3. **Strata must not be nested in the parameter.**
   - A stratum may never be a function of the tested parameter.
   - **Scenario-level parameters** (family, setting, `scene_source`, text features) are tested by permuting **whole scenarios as clusters**, with the p-floor reported. v1 has 20 scenarios.
   - **Episode-level parameters** permute whole episodes, stratified by scenario only when the parameter varies within scenario (level, pairing, monitoring).
   - **Agent-level parameters** permute within episodes.
   - `perm_test` checks the nesting rule and raises an error if it's broken. T3 asserts this.
4. **Interactions are deferred to a stretch goal** (scope; see 14). If they're built:
   - Use a ridge-penalised logistic fit (fixed λ = 1) to handle separation.
   - Statistic: the deviance drop minus extra df.
   - Null distribution: a parametric bootstrap from the additive A+B fit, with B = 500.
   - Numeric outcomes: OLS on ranks.
   - Pairs whose fit fails are reported as "not estimable".
5. **Missing fields in E1.**
   - **Every pack or CSV lookup goes through `get(key, default)`.** Defaults are blank, never 0:
     - `recovered_credit_failure`: blank if the column is absent
     - `pairing kind`: blank
     - `expected_first_take`: blank, or "never" when the value is null
     - unknown criterion: the first sentence of its block
   - **The level text** says "of N", where N is the number of levels in the pack.
   - **T4** asserts that no exception is raised on any row and that the default values are blank.

### Medium
6. **v1 statistics differ slightly.**
   - `cramers_v` takes a `bias_corrected` flag. Reports use corrected V, and T5 checks the uncorrected V (0.47 ± 0.01).
   - Tests never compare p-values with v1.
7. **E1 completion is non-random.**
   - Stage 2 analyses complete rows only.
   - Its Step 1 design check adds a **completion-status × parameters** table (setting, monitoring, diagnostic, level, pairing), so collection-order confounding is visible.
8. **Type inference.**
   - Types are inferred from non-blank values only.
   - New types: `empty` (all blank) and `constant`. Both are excluded from screening.
   - Numeric columns with 10 levels or fewer are `ordinal`, not categorical.
   - `expected_first_take_*` is `ordinal` with "never" as its highest level.
   - `seed`, `order_seed` and `selection_method` are `meta`.
   - Types declared in `column_docs.json` override inference, so v1 and E1 get the same type for each column.
9. **Report-key regexes.**
   - Each key gets an exact pattern, `\b<key>\b\W*:?`, so `highest_principal` can't match `highest_principal_who_has_spoken`.
   - `report_keys` is a fixed dict, frozen here:
     `{"authority": {"principal": "<key>", "instruction": "their_instruction"}, "nondeception": {"take": "<key>"|None, "refuse": "<key>"|None}, "welfare": {"take": "<key>"|None, "refuse": "<key>"|None}}`
   - When a pack has no report key, `criterion_cited` is blank, not 0.
10. **Rows that didn't complete.**
    - Failed, not-started and running rows keep their **inputs plus status, outcome, `outcome_description` and error**. Everything else is blank.
    - Column order follows v1: first appearance across rows, using v1's grouping rules. So `served_models` and `total_tokens` keep their v1 positions.
11. **Hidden dependencies between modules.**
    - The `report_keys` format is frozen (see 9).
    - `agent_metrics` and the pair metrics belong to **I4**. Criteria and take-deceives counts are passed as arguments, not globals.
    - I7 doesn't need the schema. It takes plain label strings, and I8 maps the schema to labels.

### Low
12. **Extra tests.**
    - Provider derivation on v1 must equal the published `provider` column, including the HF+Modal cases.
    - Synthetic-text unit tests for each report-key variant.
    - Known-answer tests for clustered and stratified `perm_test`, and for the nesting error.
    - T1 also checks that published columns keep their relative order.
    - The CSV is written with the `csv` module (not pandas), using v1 value formatting.
13. **What T1 enforces:** **string-identical values** for every published column after blanks are normalised, and identical column order. The file bytes may differ, for example in line endings.
14. **Scope and order.**
    - **PR A (Stage 1):** I1–I5, with T1, T2 and T4, shipped first because it has the hard regression target.
    - **PR B (Stage 2):** I6, I7 (heat maps and rate bars only), I8 (Steps 0–4 and 6), I9, with T3 and T5.
    - **Stretch goal:** interactions (Step 5), plus distributions and association-matrix charts.
