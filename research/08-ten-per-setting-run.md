# Corrected scope: ten scenarios per setting — 25 October 2026

The user clarified that ten scenarios means ten PER setting, not ten overall. This supersedes the small selection. The original792-scene batch remains stopped.

## Selection frozen before new collection

For each of eight settings, select the first four welfare, first three nondeception and first three authority scenarios in original JSON order. This reproducible rule is independent of observed outcomes. All80 original scene objects, five levels, criterion blocks, wrapper and monitoring texts are unchanged. The selected ten-total scenes are all included; their exact-prompt matching outcomes are imported with provenance, never regenerated.

| Setting | Selected IDs |
|---|---|
| hospital | S001, S002, S003, S004, S034, S035, S036, S067, S068, S069 |
| religious | S100, S101, S102, S103, S133, S134, S135, S166, S167, S168 |
| military | S199, S200, S201, S202, S232, S233, S234, S265, S266, S267 |
| school | S298, S299, S300, S301, S331, S332, S333, S364, S365, S366 |
| volunteer | S397, S398, S399, S400, S430, S431, S432, S463, S464, S465 |
| social_club | S496, S497, S498, S499, S529, S530, S531, S562, S563, S564 |
| family | S595, S596, S597, S598, S628, S629, S630, S661, S662, S663 |
| situational | S694, S695, S696, S697, S727, S728, S729, S760, S761, S762 |

## Design

80 scenes x 5 levels x 6 pairings x 2 notices x seed1 =4800 episodes (48000 planned experimental calls before exclusions). Modal, 48 simultaneous request slots, three exchanges, temperature0.6, output cap4096, reasoning enabled. Execution shuffle seed20261025. The harmless protocol control seed3 is reused after exact prompt/settings checks; the earlier deployment error control remains retained and excluded.

Live evidence: results/qwen-pressure-80-v1; logs pressure-80-48.stdout.log/.stderr.log. Import audit: MIGRATION.json and MIGRATION_SOURCE_MANIFEST.json. Previous results remain in their original folders. Migration waits for the old worker to drain and its lock to disappear; it never overlaps workers.

```powershell
python -u -m lying_harness.pressure --pack prompts/11-pressure-ten-per-setting.json --output results/qwen-pressure-80-v1 --jobs 48 --order-seed 20261025 --control-seed 3 --resume --resume-interrupted --allow-source-change --continue-on-format-failure --env-file .env.pressure-modal
```

## Analysis and limitations

Continue five-minute health checks and fifteen-minute validated immutable publications to the existing branch. Analyze by scenario, pressure, pairing and watched/unwatched notices with explicit completion denominators and exclusions. Report matched monitoring pairs in both directions. Audit rule/action discrepancies without automatically treating take as misconduct. Single-seed cells, qualitative welfare, related templates and differences in tasks between settings limit conclusions. No communication-off or none-none experimental baseline is added; communication effects and isolated setting effects are not identified. Watching is a notice manipulation, not a real logging difference. Prior partial outcomes were collected before this scope correction and their collection phase is recorded. Do not pool outcomes from earlier studies with different prompts. Returned reasoning is model output, not verified internal thought.
