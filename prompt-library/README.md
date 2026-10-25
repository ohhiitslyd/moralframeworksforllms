# Prompt library

Reusable prompts for this project. Each one is meant to be copied into an AI agent session, or followed by an agent that is pointed at the file. The library only adds new files. Existing prompts stay where they are and are linked from here.

| Prompt | Use it for | Location |
|---|---|---|
| **Starter research prompt** | Survey human and AI collusion and deception research, build a taxonomy, and propose experiments aligned with the sprint | [`starter-prompts/starter-prompts.txt`](../starter-prompts/starter-prompts.txt) (original location, unchanged) |
| **Development workflow** | Standing process for all work (design, research, analysis, coding, batch runs): branch and worktree naming, staged reviews, parallel subagents, commits, PRs, review gates | [`workflow/development-workflow.md`](workflow/development-workflow.md) |
| **Batch runs and major compute** | Review simulations, batch jobs and analyses for performance, reliability, parallelism, cost and experimental design; estimate cost and get approval before paid runs; MSSQ scheduling with longest jobs first; check alignment with the sprint's criteria and research questions | [`workflow/batch-runs-and-compute.md`](workflow/batch-runs-and-compute.md) |
| **Experiment analysis process** | The end-to-end process from a finished run to findings (Stages 1–3) and the contract between the stages | [`analysis-pipeline/PROCESS.md`](../analysis-pipeline/PROCESS.md) |

### Analysis, Step 1 (`PROCESS.md` Stage 1): Extract, organise and augment raw results

| Prompt | Use it for | Location |
|---|---|---|
| **Per-trial metrics table** (recommended) | One row per trial with inputs (each with a description column), outcomes, and interaction and deception metrics, plus a dictionary and schema. Generalised and expert-reviewed. | [`analysis/per-trial-metrics.md`](analysis/per-trial-metrics.md) |
| **Step 1 original prompts** | The owner's original requests (augment `runs.csv` with derived metrics; put a description next to every identifier) and the exact prompt used on the first run | [`analysis/step1-extract-organize-augment.md`](analysis/step1-extract-organize-augment.md) |

### Analysis, Step 2 (`PROCESS.md` Stage 2): Analyse and produce reports

| Prompt | Use it for | Location |
|---|---|---|
| **Parameter → outcome report** (recommended) | One-, two- and three-variable analysis: design check, correlation matrices, screening, single-factor and 2D heat maps, statistics, ranked candidates for Stage 3. Generalised and expert-reviewed. | [`analysis/parameter-outcome-report.md`](analysis/parameter-outcome-report.md) |
| **Step 2 original prompts** | The owner's original requests (univariate and bivariate heat maps with commentary; a general-purpose relationship report), the exact prompt used on the first run, and the general prompt as first proposed | [`analysis/step2-analyze-and-report.md`](analysis/step2-analyze-and-report.md) |

### Analysis, `PROCESS.md` Stage 3: Findings

| Prompt | Use it for | Location |
|---|---|---|
| **Plain-language rewrite** | Stage 3 helper: final readability pass on a findings report (the full Stage 3 steps are in `PROCESS.md`) | [`analysis/plain-language-rewrite.md`](analysis/plain-language-rewrite.md) |

## Conventions

- **One prompt per file.** Each file in `prompt-library/` has a short header (what it's for, which pipeline stage, origin), followed by the prompt itself. Prompts kept in their original locations, such as `starter-prompts/`, are linked as they are.
- **Placeholders** look like `<RESULTS_DIR>`. Fill them in before use.
- **HTML copies.** Every Markdown file in `prompt-library/` has an `.html` copy. Regenerate the copies whenever you edit the Markdown, with `python tools/md_to_html.py . <file.md> ...` from the repo root (needs the `markdown` package), and commit both in the same commit.
- **Add new prompts** as new files, in a folder named for their category (`workflow/`, `analysis/`, `research/`, `design/`, …), and list them in the table above.
