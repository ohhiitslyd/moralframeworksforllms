# Development workflow

Standing instructions for any AI agent (or person) doing work in this project. They apply to general development and to every increment of work: experiment design, research, analysis, coding, batch runs, reports and documentation.

**Origin:** the project owner's standing instructions (2026-10-25).

## The prompt (verbatim)

> For each change, create a branch named in the format [category]-[item], where "category" is the major category of change, and "item" is the specific increment we're working on. Create a local worktree for the branch whose name is in the format [project-name]-[branch-name]. Monitor our work and be alert to make sure work is done in an appropriate worktree and branch; periodically notify me to confirm the branch and alert me if anything seems wrong. For each change, use the development process: experimental design->review experimental design->code design->review design->implement->review implementation->test design->review test design->run unit test->integrate tests->review test results->analysis->review analysis->reports->review reports. For large blocks of work, break work down into the smallest feasible increment of functionality; then analyze the increments to identify dependencies; then for each increment, implement using parallel subagents, running any steps in parallel which are (a) not dependent on each other, (b) not blocked by other work, and (c) not changing the same parts of the project. When changes are done, prompt me to review the results by providing links to HTML and markdown reports which I can review.
>
> Use your own judgment about which changes should be in their own worktree and branch, vs. which ones can be implemented in the same worktree and branch; with the caveat that in general we want small, incremental changes in each branch so that humans can understand, diagnose, and correct errors after the fact, and so that pull requests form a coherent, easy-to-follow chronology and documentation of change history. For each change, branch, and worktree, once minor changes are complete, tested, and reviewed by AI agents, you can commit, push, create pull requests, and merge the pull requests. Include complete documentation and test results in the pull request. For major changes or sets of pull requests, provide summary reports in html and markdown, and prompt me to review them before performing all of the merges. Finally, when working on a single unit of work, commit frequently, so that each commit and its title forms a fine-grained, easy-to-follow, and well-documented history of changes within the individual branch or pull request.
>
> For all reviews and discrete units of work, use fresh subagents, striking a good balance between parallelism and short context length (which saves money), with adequate intelligence, context, and knowledge to perform effectively.
>
> After each merge, update the local primary main / trunk repository to point to the latest tip of the trunk.

## Quick reference

**Naming**

| Thing | Format | Example |
|---|---|---|
| Branch | `[category]-[item]` | `analysis-pipeline`, `docs-prompt-library`, `prompts-self-contained-levels` |
| Worktree folder | `[project-name]-[branch-name]` (next to the main checkout) | `hackathon-lying-agent-experiment-analysis-pipeline` |

Suggested categories: `analysis`, `prompts`, `harness`, `results`, `docs`, `tests`, `infra`.

**Process for each change.** Each review is done by a fresh subagent.

1. Experimental design, then review it.
2. Code design, then review it.
3. Implement, then review the implementation.
4. Test design, then review it.
5. Run the unit tests, then the integration tests, then review the test results.
6. Analysis, then review it.
7. Reports, then review them.

Skip the steps that don't apply, and say which ones you skipped and why. For example, a documentation-only change has no experimental design and no tests.

**Large work**

1. Break it into the smallest increments that still deliver something useful.
2. Map the dependencies between increments.
3. Run increments in parallel with subagents only when they are independent, not blocked, and don't touch the same files.

**Commits and PRs**

- Commit often. Each commit title should describe one step.
- Each PR is small and self-contained, and its description includes documentation and test results.
- **Minor changes:** after AI review and passing tests, you may commit, push, open a PR and merge it.
- **Major changes or sets of PRs:** write HTML and Markdown summary reports and ask the user to review them **before any of the merges**.
- **What counts as major:** any change to experimental design, harness behaviour, prompts sent to models, published results, or interpretation of findings; anything that triggers a paid or cloud run; and any set of related PRs. Everything else (docs, refactors with passing regression tests, tooling) is minor. When unsure, treat it as major.
- When finished, give the user links to the HTML and Markdown reports.
- **After each merge,** update the local primary checkout so it is on main at the latest tip: `git fetch origin`, then `git checkout main` and `git merge --ff-only origin/main`. Untracked files there are left alone. If local changes block the update, stop and tell the user.

**Monitoring.** Check the branch and worktree before you edit anything. From time to time, tell the user which branch and worktree are active and ask them to confirm. Flag any mismatch immediately.

## Using subagents

- **Fresh context per task.** Give each review or unit of work a new subagent. Brief it with the goal, the files to read, the constraints, and the deliverable. Don't pass along the whole conversation.
- **Reviews should be independent.** Give the reviewer the artefact and the criteria, not your own conclusion.
- **Choose capability to fit the task.** Use a strong model for design, analysis and review, and a cheaper one for mechanical work such as searching, reformatting or running commands.
- **Read only the result.** Don't read a subagent's transcript into your own context. Relay what matters to the user.
