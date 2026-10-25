# 02: Branch and worktree cleanup

Goal: leave only branches that carry live work or are needed for provenance. **Do nothing destructive without checking first.** Every delete below is safe only if `git branch -r --merged origin/main` (or the stated condition) confirms it. Haitham's and Lydia's branches are **theirs to delete**, so ask them.

## Decision table (state at 2026-10-25 ~21:00 UTC; run `git fetch --prune` first)

| Branch | Decision | Condition / reason |
|---|---|---|
| `main` | **keep** | trunk |
| `codex/resolve-pressure-merge` (Haitham) | **keep → merge into main** after team review | It has the raw completed-study data, the reorganised layout, Haitham's `reasoning-audit/`, and the resolved harness, merging in both `experiment-harness-pilot-results` and `prompt-changes-v2`. Main isn't its ancestor, so merging will need conflict checks. |
| `analysis-full-pressure-study` | keep until codex is merged, **then delete** | Working branch = codex plus our `steps/` (identical to main). Once codex is merged, everything it has is on main. |
| `experiments-authority-ablation` | **keep (WIP)** | Unreviewed ablation build (`390355db`). Based on the working branch, so it carries the raw data. **Don't merge it into main as is**; cherry-pick `390355db` (see 03). |
| `report-final-draft` | **keep** until the paper is final | Report draft in `final_report/` |
| `analysis-pipeline` | **archive** (tag, then delete), or keep if anyone builds the pipeline | Design only (`DESIGN.md`); no code |
| `analysis-e1-preliminary` | **archive** (tag `archive/e1-snapshot-analysis`), then delete | Snapshot (71%) analysis, superseded by the completed study |
| `self-contained-pressure-levels` (PR #1) | **close PR #1 unmerged, then delete** | v2 fixes for the *v1* pack; the v1 pack isn't being rerun. Lydia's line also has an identical copy. |
| `experiment-harness-pilot-results` (Haitham), `prompt-changes-v2` (Lydia) | delete **after** codex is merged (owners' call) | Both already merged into codex |
| `working/constraint-tipping` (Lydia) | delete (owner's call) | Duplicates content on main |
| `first-run-summary-analysis` | delete | Merged (PR #2) |
| `docs-prompt-library`, `docs-prompt-library-analysis-steps`, `docs-prompt-library-steps-consolidation`, `docs-prompt-library-cpu-reservation`, `docs-prompt-library-steps-0.5-1.5`, `docs-prompt-library-authority-ablation`, `docs-heatmap-legibility`, `docs-resume-claude-session`, `analysis-heatmaps-pressure-study`, `analysis-steps-pressure-study`, `analysis-steps2-pressure-study`, `analysis-construct-addendum` | **delete** | All merged (PRs #3–#14) |

## Safe procedure

```bash
git fetch --prune origin
git branch -r --merged origin/main          # candidates that are fully merged
# Archive before deleting anything unmerged:
git tag archive/e1-snapshot-analysis origin/analysis-e1-preliminary
git tag archive/analysis-pipeline-design origin/analysis-pipeline
git push origin archive/e1-snapshot-analysis archive/analysis-pipeline-design
# Delete merged remote branches (repeat per branch after confirming it is in the --merged list):
git push origin --delete docs-prompt-library
```

**Close PR #1:**
```bash
gh pr close 1 --comment "Superseded: v1 pack not being rerun."
git push origin --delete self-contained-pressure-levels
```

**Local worktrees** sit next to the main checkout in `C:\Users\Tom\hackathon2\`. Folder names don't always match branches, e.g. `…-analysis-heatmaps-pressure-study` holds `docs-heatmap-legibility`. Always check first:
```bash
git worktree list
git -C <worktree> status --short      # must be empty, or only throwaway files
git worktree remove <worktree>         # add --force only if the only changes are known scratch files
git branch -d <branch>                 # -d refuses unmerged branches; use -D only after archiving
git worktree prune
```

**Windows notes:**
- `git worktree remove` / `move` can fail with "Permission denied" if an editor or indexer holds the folder. Close it and retry.
- Never delete the primary checkout `hackathon-lying-agent-experiment`.
- Leave the untracked `analysis/qwen-pressure-final-20261024-181708/trial_metrics.xlsx` in the main checkout (the owner's file).

## After cleanup, the expected remaining branches
`main`, `codex/resolve-pressure-merge` (until merged), `experiments-authority-ablation` (or its replacement off main), `report-final-draft` (until the paper is final), plus the archive tags.
