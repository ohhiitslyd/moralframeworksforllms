# 04: Selecting the arms for the next run

The aim is to spend the next GPU budget only on arms that answer open questions. Every number below is from the completed study (4,243 of 4,320 trials complete) unless marked as an estimate.

## What we learned that shapes the selection

| Fact | Source | Implication |
|---|---|---|
| Mutual take is 5.4% at L1, 13.5% at L2, 22.3% at L3, 31.9% at L4 and 53.4% at L5 | Step 0.5 | **L1–L2 are near the floor**, so they add little power. |
| The ladder is cumulative; a superior's take-instruction first appears in **46 scenes** (L5: 36, L4: 4, L3: 5, L2: 1) | `pressure-construct/tables/instruction_category_by_scene_level.csv` | The authority contrast lives at those 46 scene-levels and the level just before each. |
| **Authority-rule agents are instructed to "follow the highest-ranking principal"**, so their response to a superior is the rule being obeyed (no mutual takes in 1,109 trials without an instruction) | `pressure-construct/REPORT.md`; mock-judge review | **The attack-surface question needs agents that are *not* told to obey:** welfare, non-deception and no-rule agents. |
| The designer's `welfare_if_take` label is "higher" from J3 onward in 71 of 72 scenes | `pressure-construct/REPORT.md` | Welfare agents rising with level is also partly the rule at work, so read welfare results with that in mind. |
| Mutual take by pairing: W-W 54.5%, W-none 30.8%, D-D 21.5%, D-none 18.4%, A-A 13.6%, A-none 13.2% | Step 0.5 | W-W has the highest base rate, so the most power for monitoring effects. A-A and A-none sit near the floor without an instruction. |
| **No no-rule + no-rule (none-none) pairing was run** | pack `pairings_to_run` | The cleanest test of claimed authority on agents with no installed rule is missing. |
| Settings vary from 20% (school) to 34% (family) mutual take, but are scenario-level with only 9 scenes per setting | Step 0.5 / Step 2 | Treat settings as cosmetic. Don't stratify or expand them. |
| Lydia's extended pack v6 is 87% template-generated | branch analysis | Don't use it as independent scenes. |
| The monitoring effect has no trend by level and no significant heterogeneity on the OR scale (larger in pp for welfare pairs) | Step 2 | One more monitoring replication isn't a priority. Keep the notice as a crossed factor only where it's cheap. |

## Arms to drop
- **Levels 1–2,** except the one scene whose first instruction is at L2 and the levels that serve as its "before" controls.
- **The "pressure dose-response" framing** across all levels. It isn't a valid construct. Replace it with explicit ingredient contrasts (instruction present/absent; later: harm, promise, permission).
- **A-A as a headline arm.** It's tautological for authority. Keep a small A-A slice only as a manipulation check: authority agents *should* follow the instruction.
- **Expanding settings or template scenes.**
- **D-none,** which adds little beyond D-D (18.4% vs 21.5%). Keep W-none for the lone-taker asymmetry.

## Arms to run (recommended)

Factors:
- **Scene-levels:** the 46 first-instruction scene-levels **plus** the level just before each, giving **92 scene-levels**.
- **Instruction:** PRESENT vs REMOVED at the first-instruction level, and ORIGINAL vs ADDED at the level before. This gives **4 variants × 46 = 184 scene-level variants**. They come from the existing WIP builder with the principals-artefact fix.
- **Placement** (from 01): SYSTEM vs SPLIT.
- **Pairings:**
  - **none-none** (new; primary for the attack-surface question)
  - **W-W** (high base rate)
  - **D-D**
  - **W-none** (asymmetry)
  - **A-none** (the none agent is untold; the A agent is a manipulation check)
  - a 25% A-A check slice
- **Monitoring notice:** **unwatched only** in the core run, to maximise base rates for the authority contrast. Add a watched slice later if budget allows.
- **Seed:** 1, plus a second seed on a 20% random subset to estimate within-cell noise.

### Cell counts (estimates)

| Run | Arms | Trials |
|---|---|---|
| **Core A: authority × placement**, unwatched | 184 variants × 2 placements × 5 pairings (none-none, W-W, D-D, W-none, A-none) | **1,840** |
| A-A manipulation check | 184 × 2 × 1 × 25% | 92 |
| Second-seed subset | 20% of core A | 368 |
| **Total** | | **≈2,300** |
| **Minimal version**, if the budget is tight | 184 variants × SPLIT only × {none-none, W-W, A-none}; the completed study supplies SYSTEM for W-W and A-none, but none-none needs both placements (+184) | **≈736** |

**Cost estimate** (calibrate against the actual Modal bill):
- Per trial: about 14.6k tokens, about 10 requests.
- **≈2,300 trials:** ≈34M tokens, ≈2.3–3.3 h at 700–1,000 trials/h, ≈$15–55 GPU.
- **Minimal (≈736 trials):** ≈11M tokens, ≈0.8–1.1 h, ≈$5–18.
- **Get owner approval before running**: spend cap 120% of the approved estimate, pause if the error rate exceeds 10%.

## Pre-registered hypotheses for this run
1. **H1 (primary, none-none):** within cell, a superior's take-instruction raises mutual take for agents with **no installed rule**, under SPLIT placement (the instruction is in user content). Test: paired McNemar plus a scenario-cluster bootstrap CI.
2. **H2 (placement):** the instruction effect is smaller under SPLIT than SYSTEM. Test: the difference in paired effects, with a cluster bootstrap.
3. **H3 (generality):** H1 also holds for W-W and D-D.
4. **H4 (manipulation check):** A-A follows the instruction in both placements.

Everything else is exploratory, with BH correction.

## How to generate the cell list
Read `pressure-construct/tables/instruction_category_by_scene_level.csv`. For each scenario, take the minimum `level` where `instr_cat == "explicit"`, plus `level − 1`. Feed that list to the builder (03) with `--pairings none-none,W-W,D-D,W-none,A-none --placements system,split --monitoring unwatched`. Add the `none-none` pairing to the pack's `pairings_to_run`: `{"id": "none-none", "a": "none", "b": "none", "kind": "control"}`.
