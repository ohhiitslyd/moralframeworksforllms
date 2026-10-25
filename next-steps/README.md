# next-steps/: handoff package

This folder is everything an engineer (or an AI agent) needs to continue the dual-control collusion experiment after the 2026-10-25 sprint pause. Read the files in order:

| # | File | What it gives you |
|---|---|---|
| 0 | [RESUME_CLAUDE_SESSION.md](RESUME_CLAUDE_SESSION.md) | Full context: results, where everything lives, rules, history, pitfalls. **Start here.** |
| 1 | [01-separate-system-prompt.md](01-separate-system-prompt.md) | Harness change: the moral rule stays in the system prompt; the scenario, stakes and principals move to a user turn. Includes code-level steps and tests. |
| 2 | [02-branch-cleanup.md](02-branch-cleanup.md) | Which branches and worktrees to keep, archive or delete, with safe commands and checks |
| 3 | [03-authority-ablation.md](03-authority-ablation.md) | The authority-ablation experiment (± prompt placement): what's built, what's missing, and how to finish it |
| 4 | [04-arm-selection.md](04-arm-selection.md) | Which experimental arms to run next and which to drop, with exact cells, counts and cost |
| 5 | [05-plan-and-timeline.md](05-plan-and-timeline.md) | A pre-defined plan with phases, dependencies, gates and timeline |

**Status at handoff:**
- **Completed study:** analysed. The results are on `main` in `analysis/2026-10-25-pressure-study/steps/`.
- **Report:** a first draft is on branch `report-final-draft` (`final_report/REPORT.md`). It's AI-assisted and needs team revision.
- **Follow-up experiments:** designed, not run. Running them needs the owner's cost approval and Haitham's Modal endpoint credentials.

**Non-negotiable rules:**
- Leave CPUs 0–3 free for analytics jobs. Use `python tools/run_reserved.py <script>`.
- Never kill processes by name.
- No paid runs without a cost estimate and approval.
- Use small branches and PRs, with a fresh-agent review for each change.

The details are in `prompt-library/workflow/`.
