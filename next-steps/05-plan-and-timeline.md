# 05: Plan and timeline

Durations are estimates: working time for one engineer with AI agents, plus wall-clock time for runs. ⛔ marks **gates** that need a human decision.

## Phases

| # | Phase | Work | Depends on | Est. time | Output |
|---|---|---|---|---|---|
| 0 | **Orient** | Read `RESUME_CLAUDE_SESSION.md` and this folder; `git fetch`; confirm the worktree layout | — | 0.5 h | — |
| 1 | **Reconcile and merge data** | ⛔ The team decides how to merge `codex/resolve-pressure-merge` into main. Reconcile Haitham's `reasoning-audit/` numbers and wording with `steps/`. | 0 | 1–2 h | main has the raw data and one agreed set of numbers |
| 2 | **Branch cleanup** | Follow 02: archive tags, delete merged branches, close PR #1 | 1 (partly) | 0.5 h | lean branch list |
| 3 | **Placement split** (01) | Harness change, tests, validation renders; fresh-agent review | 1 or the manifest copy | 2–3 h | `--placement split`; tests green |
| 4 | **Ablation pack v2** (03 + 04) | Cherry-pick `390355db` onto a branch off main; add the none-none pairing and placement; select the 92 scene-levels; rebuild; diff report; validation; `DESIGN.md`, `PREREG.md`, `LAUNCH.md` | 3 | 2–3 h | pack 13 v2, validated |
| 5 | **Review** | A fresh agent reviews the design, diffs and code (friendly + adversarial); fix findings | 4 | 1 h | review notes resolved |
| 6 | ⛔ **Cost approval and credentials** | Cost table per arm (04); owner approval; Haitham provides `.env.pressure-modal` or launches | 5 | depends on people | approval recorded |
| 7 | **Pilot** | About 30 trials with `--limit`; check parsing, placement rendering and outcomes | 6 | 0.5 h | go / no-go |
| 8 | **Full run** | MSSQ, `--jobs 48`; monitor throughput, errors and spend against the cap | 7 | 2.7–3.9 h wall (minimal ≈1 h) | `results/authority-ablation-v1/` |
| 9 | **Analysis** | Steps 0.5 → 1 → 1.5 → 2 (primary H1–H4) → 3, via `tools/run_reserved.py` | 8 | 1.5–2 h | step outputs plus updated claims ledger |
| 10 | **Paper update** | Fold the results into `final_report/REPORT.md` (reframe the authority contribution around none-none / SPLIT); team rewrite; references verified | 9 | 2–4 h | submission-ready report |

## Timeline (one engineer, starting at T0)

```
T0      +2h      +4h      +6h      +8h      +10h     +12h     +14h
|--0,1--|        |        |        |        |        |        |
   |-2-|
        |---3---|
                 |---4----|
                          |-5-|
                              ⛔6 (approval/credentials; can overlap 5)
                                 |7|
                                   |------8 run------|
                                                     |--9--|
                                                           |--10--|
```

- **Critical path:** 1 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10. That's about **12–16 working hours** with prompt approvals, or **about 1.5–2 calendar days** realistically.
- **Can run in parallel:**
  - phase 2 alongside 3
  - drafting `PREREG.md` (in phase 4) alongside the placement tests (3)
  - the paper rewrite of the existing results (10, first half) alongside the runs (8)
- **If the hackathon deadline still applies** (11:59 PM AoE, 2026-10-25): skip 2–9 and submit the current results. Use `final_report/REPORT.md` after applying the review fixes (see `report-final-draft`). List H1–H4 as future work.

## Decision points
- ⛔ **Phase 1:** how to merge codex (Haitham's layout changes), and whose figures and wording the paper uses.
- ⛔ **Phase 6:** the budget (full ≈2,740 trials ≈$18–65, or minimal ≈736 ≈$5–18) and who launches.
- **After phase 7:** go / no-go on the pilot.
- **After phase 9:** whether the results change the paper's headline. They would if H1 holds: "claimed authority in user content overrides …".

## Rules that apply throughout
- Use branches named `[category]-[item]`, with worktrees named `hackathon-lying-agent-experiment-[branch]`.
- Commit often. Use fresh-agent reviews. Merge minor changes after review; ask the owner before merging major ones.
- After each merge, fast-forward the primary checkout to main.
- Leave CPUs 0–3 free (`tools/run_reserved.py`). Never kill processes by name. No paid runs without approval.
