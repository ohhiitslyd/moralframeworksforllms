# Prompt library

Reusable prompts for this project. Each one is meant to be copied into an AI agent session, or followed by an agent that is pointed at the file. The library only adds new files. Existing prompts stay where they are and are linked from here.

| Prompt | Use it for | Location |
|---|---|---|
| **Starter research prompt** | Survey human and AI collusion and deception research, build a taxonomy, and propose experiments aligned with the sprint | [`starter-prompts/starter-prompts.txt`](../starter-prompts/starter-prompts.txt) (original location, unchanged) |
| **Development workflow** | Standing process for all work (design, research, analysis, coding, batch runs): branch and worktree naming, staged reviews, parallel subagents, commits, PRs, review gates | [`workflow/development-workflow.md`](workflow/development-workflow.md) |
| **Batch runs and major compute** | Review simulations, batch jobs and analyses for performance, reliability, parallelism, cost and experimental design; estimate cost and get approval before paid runs; MSSQ scheduling with longest jobs first; check alignment with the sprint's criteria and research questions | [`workflow/batch-runs-and-compute.md`](workflow/batch-runs-and-compute.md) |
| **Experiment analysis process** | The end-to-end process from a finished run to findings (Stages 1–3) and the contract between the stages | [`analysis-pipeline/PROCESS.md`](../analysis-pipeline/PROCESS.md) |
| **Per-trial metrics table** | Stage 1: one row per trial with inputs, outcomes and interaction and deception metrics, plus a dictionary and schema | [`analysis/per-trial-metrics.md`](analysis/per-trial-metrics.md) |
| **Parameter → outcome report** | Stage 2: design check, matrices, screening, single-factor and 2D heat maps, statistics, curation | [`analysis/parameter-outcome-report.md`](analysis/parameter-outcome-report.md) |
| **Plain-language rewrite** | Stage 3: make a findings report readable for newcomers | [`analysis/plain-language-rewrite.md`](analysis/plain-language-rewrite.md) |

## Conventions

- **One prompt per file.** Each file has a short header (what it's for, which pipeline stage, where it came from), followed by the prompt itself.
- **Placeholders** look like `<RESULTS_DIR>`. Fill them in before use.
- **Every prompt has an `.html` copy** for easy reading.
- **Add new prompts** as new files, in a folder named for their category (`workflow/`, `analysis/`, `research/`, `design/`, …), and list them in the table above.
