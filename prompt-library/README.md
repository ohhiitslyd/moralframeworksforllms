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
| **Step 1: extract, organise, augment** | One validated row per planned trial: inputs, each with a description column; outcomes; per-agent and pair interaction and deception metrics; dictionary, schema, validation and provenance. The owner's original prompts are in its appendix. | [`analysis/step1-extract-organize-augment.md`](analysis/step1-extract-organize-augment.md) |

### Analysis, Step 2 (`PROCESS.md` Stage 2): Analyse and produce reports

| Prompt | Use it for | Location |
|---|---|---|
| **Step 2: analyse and report** | One-, two- and three-variable analysis: design check and completion, pre-registered (paired) primary test with power, correlation matrices, screening, single-factor and 2D heat maps, words vs. actions, sensitivity, ranked candidates. The owner's original prompts are in its appendix. | [`analysis/step2-analyze-and-report.md`](analysis/step2-analyze-and-report.md) |

### Analysis, Step 3 (`PROCESS.md` Stage 3): Findings

| Prompt | Use it for | Location |
|---|---|---|
| **Step 3: findings briefing and paper kit** | Turns Step 2 output into a ranked claims ledger, a 60-second briefing, plain-language findings with "so what", non-claims and threats to validity, a judge lens, next steps ranked by score lift per hour, and a paper kit (titles, abstract, figure plan). It also has a lite mode for a readability-only rewrite. | [`analysis/step3-findings-briefing.md`](analysis/step3-findings-briefing.md) |

## Conventions

- **One prompt per file.** Each file in `prompt-library/` has a short header (what it's for, which pipeline stage, origin), followed by the prompt itself. Prompts kept in their original locations, such as `starter-prompts/`, are linked as they are.
- **Placeholders** look like `<RESULTS_DIR>`. Fill them in before use.
- **HTML copies.** Every Markdown file in `prompt-library/` has an `.html` copy. Regenerate the copies whenever you edit the Markdown, with `python tools/md_to_html.py . <file.md> ...` from the repo root (needs the `markdown` package), and commit both in the same commit.
- **Add new prompts** as new files, in a folder named for their category (`workflow/`, `analysis/`, `research/`, `design/`, …), and list them in the table above.
