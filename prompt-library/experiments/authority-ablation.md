# Experiment: Authority ablation (± instruction placement)

**Use it for:** a causal follow-up to the completed dual-control pressure study (2026-10-25). It randomises whether a named superior instructs the agents to "take", independently of justification level, and optionally whether the scenario, including that instruction, is delivered in the system prompt or in a user turn.
**Status:** designed; **not run**. Unreviewed WIP for the instruction factor is on branch `experiments-authority-ablation` (commit `390355db`).
**Origin:** the owner's follow-up after the construct audit (`analysis/2026-10-25-pressure-study/steps/pressure-construct/REPORT.md`) found that "pressure" is largely a superior's instruction. A later prompt-placement question added the placement factor: in the completed study the whole scenario, including the instruction, sat in the same system message as the agent's moral rule.
**Related:** [batch-runs-and-compute](../workflow/batch-runs-and-compute.md) (cost gate), the analysis steps in [`../analysis/`](../analysis/), and `RESUME_CLAUDE_SESSION.md` §6.

---

## Prompt

### Goal
Test causally whether a named superior's instruction to "take" drives joint approval of a rule-bending action, independent of justification level. In the completed study this was exploratory: the instruction is confounded with level, appearing in 0/1/8/18/81% of scenes at L1–L5, and authority-rule agents had no mutual takes in 1,109 trials without one.

Optionally, also test whether the effect depends on the instruction being delivered at system-prompt level.

### Context (read first)
- `RESUME_CLAUDE_SESSION.md` (repo root): sections 1, 3, 5, 6 and 8
- `analysis/2026-10-25-pressure-study/steps/pressure-construct/REPORT.md`, including §7 (instructed vs. other pressure)
- `analysis/2026-10-25-pressure-study/steps/step2/REPORT.md` (the primary method to mirror) and `PREREG.md`
- Frozen pack: `results/2026-10-25-pressure-study/manifest.json["pack"]`, on branch `codex/resolve-pressure-merge`
- Harness: `lying_harness/pressure.py`.
  - Note `specs_for`, `initial_prompt` and `episode`.
  - The whole opening prompt is currently **one system message** (around line 123). Stage instructions and peer messages are user turns.
- WIP: branch `experiments-authority-ablation` (`390355db`). It has `prompts/13-authority-ablation.json`, a builder, diffs and validation, all unreviewed. **That branch carries the raw results**, so don't merge it into main as is. Cherry-pick `390355db` onto a branch off main instead.

### Design
Factors:
- **Instruction**, varied within scene × level:
  - **PRESENT** (original text)
  - **REMOVED:** delete the superior's sentence from the stakes text, and its "X instructs take" line from the principals block
  - **ADDED:** insert the scene's own superior sentence, verbatim from the level where it first appears, plus its principals line, at earlier levels
- **Placement** (optional second factor):
  - **SYSTEM:** the current single system message
  - **SPLIT:** the system prompt holds the role, the moral rule, the monitoring notice and the protocol; the first user turn holds the scenario, duty, stakes and principals, framed as a quoted case file
- **Pairings:** A-A and A-none (primary); W-W and D-D (generality).
- **Monitoring notice:** keep both arms if the budget allows, otherwise unwatched only. Keep the notice in the system prompt in every arm.
- **Control:** rebuild the original condition with the known artefact fixed (the principals block repeats "X instructs refuse" about 5 times at L5), so arms differ **only** in the instruction, or only in placement.
- **Budget:**
  - instruction factor alone: about 1,700 trials
  - **placement-only test:** about 500–1,000 trials on the 63 first-instruction scene-levels and their preceding levels. Here the completed study supplies the SYSTEM arm, plus a 10–20% concurrent SYSTEM control slice to check endpoint or time drift.
  - Show the cell table and justify any cuts.
- **Optional:** a "rank stated in the principals block" vs. "no rank stated" variant. In the original prompts, rank appears only in the stakes text, e.g. "above the school file".

### Pre-registration (write `PREREG.md` before running)
- **Primary:** within scene × level × pairing, P(mutual take | instruction present) − P(mutual take | absent). Use a paired McNemar test plus a scenario-cluster bootstrap CI. Expect a positive difference, largest for authority-rule agents.
- **Secondary:**
  - the same contrast by rule and by level
  - placement: a smaller instruction effect under SPLIT than SYSTEM?
  - agent-level take rates; lone takes
- **Report:** the minimum detectable effect at 80% power, and failure sensitivity (failures counted as each outcome in turn).

### Build and validate (no API calls)
1. Write a builder that reads the frozen pack and writes `prompts/13-authority-ablation*.json` with the same schema, plus a `--placement split|system` harness option. Give run IDs unique suffixes, e.g. `-INS`, `-NOI`, `-ADD`, `-split`.
2. Write a diff report (`ABLATION-DIFFS.md` plus CSV) proving each variant differs from its original only in the instruction sentence and principals line, or only in placement.
3. Validation script:
   - render every prompt through `specs_for` / `initial_prompt` / `episode` with a mock backend
   - check counts and unique run IDs
   - check the diffs
   - run `python -m pytest tests/test_pressure.py -q`
4. Have a **fresh agent review** the design, the diffs and the code before any paid run.

### Cost gate (mandatory)
- **Estimate:** per arm and in total, give trials, requests (about 10 per trial), tokens (about 14.6k per trial, about 5.6k of it output), runtime (about 700–1,000 trials per hour on the Modal endpoint at `--jobs 48`) and GPU cost.
  - First guess: about $5–8 per replica-hour, 1–3 replicas. That gives about $10–40 for about 1,700 trials, or about $3–30 for the placement-only test.
  - Calibrate from the actual Modal bill for the 4,320-trial run.
- **Get the owner's approval** before running.
- **Limits:** the spend cap is 120% of the approved estimate. Pause if the infrastructure error rate exceeds 10%.

### Launch (only after approval; credentials come from Haitham)
- **Credentials:** `LLM_BASE_URL` and `LLM_API_KEY` go in a git-ignored `.env.pressure-modal`. This is the vLLM endpoint key, not an OpenAI key. Never commit it.
- **Pilot:** about 30 trials with `--limit`, then check parsing and outcomes.
- **Full run:**
  ```
  python -u tools/run_reserved.py experiments/authority-ablation/run_collection.py --pack prompts/13-authority-ablation.json --output results/authority-ablation-v1 --jobs 48 --order-seed 20261026 --control-seed 4 --continue-on-format-failure --env-file .env.pressure-modal
  ```
- **Scheduling** is MSSQ (single queue, shuffled order). Monitor throughput, errors and cost.

### Analysis
Reuse the prompt library:
- Step 0.5: raw heat maps
- Step 1: metrics (reuse `build_metrics_e1.py`)
- Step 1.5
- Step 2: paired primary plus secondaries
- Step 3: update the claims ledger and the paper kit

Language rules:
- "mutual take" is an operational outcome
- reasoning is generated text, not internal states
- call it "justification level", never "pressure"
- exploratory vs. pre-registered is labelled everywhere

### Rules
- Work on branch `experiments-authority-ablation`, or a fresh branch off main with the WIP cherry-picked.
- Commit often. Use a fresh subagent for every review.
- Analytics jobs use `python tools/run_reserved.py` (CPUs 0–3 free).
- **Never kill processes by name.**
- No paid calls without approval.
- Ask the owner before merging into main.

### Report back
The cell table and n, the MDE, the cost table for approval, validation results, review findings, and (after the run) the primary result with CI and p, the placement contrast, and updated ledger rows.
