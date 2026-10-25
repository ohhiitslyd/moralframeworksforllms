# Prompt and harness integration

This merge combines `prompt-changes-v2` with the committed harness results branch
in an isolated checkout. It does not deploy a new runner to an ongoing study.

## Resolutions

- Keep the five-setting prompt pack and its builder from `prompt-changes-v2`
  as the default for future experiments. Preserve all four conflicting older
  eight-setting generated files in `prompts/archive/harness-eight-setting/`,
  with exact-byte SHA-256 hashes and the harness parent commit.
- Keep the five-setting runner's monitoring selector, setting validation,
  run-ID format and default pack. Merge the harness's local-save retries,
  connection/checkpoint recovery, shuffled scheduling, separate control seed,
  endpoint audit reason, mixed-column CSV reporting and snapshot publishing.
- Preserve both branches' pressure tests, updating the shared current-pack
  expectations to 29,700 episodes and retaining separate historical-pack checks.
- Keep the five-setting README description together with the latest committed
  harness snapshot link. Historical results describe their original studies.
- Keep the analysis scripts, tables and figures from the prompt branch. The
  metrics scripts did not conflict in this merge. No historical result files
  are rewritten or regenerated.

## Running-study boundary

The ongoing experiment stays on its original checkout, code, prompt files,
environment, output directory and worker processes. No checkout, reset, stash,
restart or environment change is required there. Local uncommitted studio work
is outside this integration.

The five-setting experiment uses different scene content and monitoring run IDs.
Start it in a fresh results directory after the current collection is finished;
do not use it to resume the older experiment. Existing manifest and checkpoint
matching remain in force. This integration does not claim transparent resume
compatibility across those designs.

Snapshot publishing may continue adding commits while this merge is reviewed.
The merge's second parent identifies its exact harness cutoff. Any later
snapshots must be incorporated before updating a shared branch. The isolated
merge must not be force-pushed over either collaborator's branch.

## Validation

Validation uses mock backends, temporary outputs and planning mode. No live
model requests or active result-folder writes are needed. Check the full unit
suite, both monitoring-plan sizes, the historical pack hashes, and exact tree
equality for the harness's historical results and analysis snapshots.

Verified for this merge:

- All 25 unit tests pass, including checkpoint rejection after a prompt change,
  saved-response reuse, transient save-lock recovery and archived pack hashes.
- Planning mode reports 29,700 episodes for both monitoring conditions and
  14,850 for watched only. It makes no model calls and creates no output folder.
- All 43,422 harness-parent files under `results/` and `analysis/` retain their
  exact Git blob hashes. All 6,226 prompt-parent files under those directories
  also retain their exact hashes.
- All five archived prompt files retain their original bytes in the staged
  Git objects, including line endings. No merge conflicts remain.

The harness cutoff is commit `46df3e03750fd185dff8948113a753512421fef4`.
