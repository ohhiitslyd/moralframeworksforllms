# 01: Separate the system prompt from the scenario

## Why
In the completed study, `lying_harness/pressure.py` sends each agent's **entire opening prompt as one `system` message**: around line 123, `histories = {a: [{"role": "system", "content": initial_prompt(pack, spec, a)}] …}`. That message includes:
- the scenario
- the official duty
- the proposed action
- the honesty notes
- the **principals block** (e.g. "District special-education director instructs take")
- the **stakes text** (the justification ladder)
- the monitoring notice
- the agent's **moral-rule criterion block**
- the output protocol

Stage instructions ("plan", "message", "decide") and delivered peer messages are `user` turns.

**Consequence:** an in-story superior's instruction shares system-level priority with the agent's own operator-given rule. Instruction-hierarchy training (Wallace et al., 2024, *The Instruction Hierarchy*) teaches models to privilege system content, so the observed authority effect may be partly **system-prompt priority** rather than claimed authority. The realistic threat model, where task content tries to override an operator rule, needs the scenario in a **user** turn.

## Target message layout

| Role | Content |
|---|---|
| `system` | Role line ("You are {role}. Another participant is {other_role}."), the agent's **criterion block** (moral rule), the **monitoring notice** (kept here so the monitoring arm stays comparable), the dual-control mechanics, the output instructions (`plan:` / `action:` lines) and the `PROTOCOL` text |
| `user` (first turn) | `CASE FILE:`: setting, official duty, proposed action, outcome and cost, honesty notes, **principals who have spoken**, **stakes in this episode**. Then the first stage instruction (`STAGES["plan"]`) in the **same** user message, to avoid two consecutive user turns. |
| later turns | unchanged: assistant responses, then user turns with stage instructions plus delivered peer messages |

## Implementation steps (about 40–80 lines plus tests)

1. **Pack fields.** Don't edit frozen packs. Add an optional pack-level key, `"placement_templates": {"system": "...", "case": "..."}`. The two format strings split `shared_wrapper` into the system part and the case-file part, using the same `{placeholders}`. Generate them in the builder (03) by cutting `shared_wrapper` at the "Setting / Official duty … Stakes" block. Keep `shared_wrapper` unchanged for the default path.
2. **`pressure.py`:**
   - Add `opening_messages(pack, spec, agent, placement="system") -> list[dict]`.
     - `placement == "system"`: return `[{"role": "system", "content": initial_prompt(...)}]`, **byte-identical** to today.
     - `placement == "split"`: render both templates with the same `values` dict `initial_prompt` uses (including `monitoring_text`). Return `[system_msg]`, and mark the case text so `episode()` prepends it to the first stage's user message.
   - In `episode()`, replace the `histories = …` line with `opening_messages(...)`. When the plan-stage user message is built, prefix it with `"CASE FILE:\n" + case_text + "\n\n"` if placement is split.
   - Add `--placement {system,split}` to the CLI (default `system`). Put `spec["placement"]` on each spec. Add a run-ID suffix `-split` **only** when it's split, so existing run IDs and resume behaviour don't change.
   - **Resume compatibility:** add `placement` to the manifest identity **only when it isn't `system`**. An unconditional key would break `same_study` checks on old manifests. An earlier review found this exact bug pattern with `monitoring`.
3. **Tests** (`tests/test_pressure.py`):
   - **Default regression:** for 10 random specs from the frozen pack, `opening_messages(..., "system")[0]["content"] == initial_prompt(...)`.
   - **Split content:** the system message contains the criterion block and the monitoring notice, but **not** the principals or stakes text. The first user message contains both, plus `STAGES["plan"]`.
   - **Run IDs:** split specs have unique IDs ending in `-split`; default specs are unchanged.
   - **Episode with the mock backend** (as the existing tests do): the number of calls is unchanged, and the histories contain no private information from the other agent.
   - **Resume:** a manifest written without `placement` still passes the resume check with `--placement system`.
4. **Validation script:** render every split prompt for the selected cells (see 04), and diff it against the system version. Only the location of the moved block may differ.
5. **Review:** a fresh agent reviews the diff, the tests and some rendered examples before any run.

## Verification checklist
- [ ] `python -m pytest tests/test_pressure.py -q` passes, run via `python tools/run_reserved.py -m pytest …` or plainly.
- [ ] Default renders are byte-identical to before.
- [ ] Spot-check 3 split transcripts from a mock run.
- [ ] `README` / `research/` note describing the new flag.
