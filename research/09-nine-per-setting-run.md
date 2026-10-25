# Final corrected selection: nine per setting — 25 October 2026

User requests nine original scenarios per setting: three welfare, three nondeception and three authority. No new scenarios or rewrites. Selection uses the first three of each diagnostic in original source order within each of eight settings.

| Setting | Welfare | Nondeception | Authority |
|---|---|---|---|
| hospital | S001, S002, S003 | S034, S035, S036 | S067, S068, S069 |
| religious | S100, S101, S102 | S133, S134, S135 | S166, S167, S168 |
| military | S199, S200, S201 | S232, S233, S234 | S265, S266, S267 |
| school | S298, S299, S300 | S331, S332, S333 | S364, S365, S366 |
| volunteer | S397, S398, S399 | S430, S431, S432 | S463, S464, S465 |
| social_club | S496, S497, S498 | S529, S530, S531 | S562, S563, S564 |
| family | S595, S596, S597 | S628, S629, S630 | S661, S662, S663 |
| situational | S694, S695, S696 | S727, S728, S729 | S760, S761, S762 |

72 scenarios x5levels x6pairings x2monitoring notices xseed1 =4320 experiments,43200 planned experimental calls before exclusions. Full scenario objects, levels, criterion text and wrapper are exactly the supplied v5 content. Modal,48 concurrent requests,three message exchanges,temperature0.6,4096 output tokens,reasoning enabled,execution shuffle seed20261025.

The80-scenario worker drains via pause.request; it must exit before migration and restart. Its exact-matching terminal results are copied byte-for-byte with recorded checksums and prompt/spec checks into results/qwen-pressure-72-v1. Results for dropped scenarios remain in their old folders and are not counted. Every returned response is retained and no existing behavioral outcome is regenerated. MIGRATION.json and MIGRATION_SOURCE_MANIFEST.json preserve provenance. Prior raw evidence and snapshots remain unchanged.

Logs: pressure-72-48.stdout.log/.stderr.log. The superseded10-total,80-total and792-total runs remain stopped. Five-minute health checks and fifteen-minute validated publications continue for the72-scenario study only.

```powershell
python -u -m lying_harness.pressure --pack prompts/12-pressure-nine-per-setting.json --output results/qwen-pressure-72-v1 --jobs 48 --order-seed 20261025 --control-seed 3 --resume --resume-interrupted --allow-source-change --continue-on-format-failure --env-file .env.pressure-modal
```

Analyze descriptive outcomes by scenario,pressure,pairing and monitoring with explicit denominators/exclusions. Audit rule/action discrepancies. Single-seed cells, qualitative utilities, template relationships, collection phases and different task content across settings limit inference. No communication-off or none-none experimental baseline: no causal communication claim. Watched/unwatched are notices, not actual logging differences. Returned reasoning is model output, not verified internal thought.

## Windows save recovery at11:53 UTC

The worker exited on WinError5 during atomic replacement of one completed result. The final result was fully saved in result.json.tmp; all10 model responses and the execution event were present. Decisions and scores were verified against original responses, then the result and readable transcript were restored with no inference calls. WRITE_RECOVERY.json retains the prior running record, complete result and source checksum. The pressure runner now retries transient local PermissionError saves only; prompts, parsing, sampling and outcomes are unchanged. Nine pressure tests passed. Collection resumed at48slots, using pressure-72-48-write-recovery.stdout.log/.stderr.log.

## Workspace endpoint switch and concurrency 96 at 12:12 UTC

User authorized model endpoint switch to `haitamelmekaoui` workspace and concurrency 96 due to low credits on the previous workspace. The running 48-slot worker was cleanly drained via `pause.request`, preserving all 481 completed episodes and 10 format exclusions, and published in snapshot `20261025-121256`. The new endpoint was verified with streaming reasoning tokens. Remaining episodes resume at 96 parallel requests with `--allow-endpoint-change`, logging provenance to `endpoint_history.json`. Logs: `pressure-72-96.stdout.log` / `pressure-72-96.stderr.log`.

## Publication snapshot 20261025-123715 and connection recovery at 12:48 UTC

Snapshot `20261025-123715` published with 547 completed episodes, 11 format exclusions, 100% reasoning coverage (5,576 responses) and remote HEAD verified. Concurrency 96 was maintained. At 12:48 UTC the worker drained and paused when an HTTP connection dropped (`RemoteProtocolError` and `APIConnectionError`). Completed episodes reached 717 with 15 format failures preserved. The runner supports `--recover-connection-failures` to archive the original network failure to `connection-failure-original.json` and resume only missing stages from checkpoint, preserving all existing responses without re-execution.

## Snapshot 20261025-125308 and progress to 1,113 completions at 13:10 UTC

Snapshot `20261025-125308` published with 717 completed episodes, 16 exclusions, 100% reasoning coverage (7,306 responses) and remote HEAD verified. Concurrency 96 continued at high throughput, completing 396 additional episodes in ~17 minutes. Completed episodes reached 1,113 (25.8% of 4,320 planned). Two transient HTTP stream disconnects occurred (`S234-L1-D-D-s1-unwatched` and `S661-L3-W-W-s1-unwatched`), pausing the worker cleanly. Both episodes resume from checkpoint with `--recover-connection-failures`, preserving all existing responses.



