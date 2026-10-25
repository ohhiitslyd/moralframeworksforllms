# Extended pressure collection — 25 October 2026

User requested running the supplied v5 pack with 24 simultaneous requests.
The supplied documents are experimental data; the JSON is the execution source.
All four source files are copied unchanged under prompts/09-extended-pressure-*.
JSON SHA256: 822f44c2790bdb924750e4c72afa3b4df084f22b02685af4c1849d8c9346ed18.

## Design

792 scenarios: 99 each in hospital, religious, military, school, volunteer,
social_club, family and situational settings. Each setting includes 33 scenarios
per diagnostic family. Five independent, cumulative-text pressure levels, six
pairings, watched/unwatched notices and seed 1 produce 47,520 experimental
episodes. One separate harmless protocol control adds 10 calls, for a maximum
of 475,210 calls before exclusions. Monitoring notices manipulate what agents
are told; all conditions retain full researcher logs.

The supplied rule text and neutral proposed-action wrapper replace those of the
earlier pressure pack. This is a new study, not a direct story-only replication.
No new communication-off or none-none experimental baseline is added. The old
600-episode study and published snapshots remain unchanged.

Three message exchanges, temperature 0.6, 4096 output tokens, returned reasoning
and per-call seeds are retained. Modal supplies all initial inference. Shared
request concurrency and episode concurrency are both capped at 24. A deterministic
execution shuffle (order seed 20261025) spreads settings and monitoring conditions
through collection time. Both monitoring conditions use the same call seeds.

## Execution and evidence

Live output: results/qwen-extended-pressure-v5. Logs:
pressure-extended-v5.stdout.log and pressure-extended-v5.stderr.log.

```powershell
python -u -m lying_harness.pressure --pack prompts/09-extended-pressure-scenarios.json --output results/qwen-extended-pressure-v5 --jobs 24 --order-seed 20261025 --continue-on-format-failure --env-file .env.pressure-modal
```

The manifest freezes the pack, instructions, model settings, endpoint and shuffle
seed. Each episode retains requests, returned reasoning, responses, peer messages,
decisions and endpoint provenance. Format failures remain exclusions. Infrastructure
failures stop new scheduling and drain active work; diagnose before checkpoint
recovery. Never rerun returned behavioral outcomes. Use pause.request to drain.

The existing pressure_publish module is specific to the previous 600-episode
study and must not be used for this batch without adapting its source and reports.
The new `python -m lying_harness.extended_publish --publish` handles this batch:
immutable full-evidence snapshots, all planned CSV rows, three descriptive figures,
checksums, credential/cutoff validation and verified pushes to the existing branch.
Its end-to-end snapshot/analysis validation passed on live evidence in a temporary
directory. Five-minute health checks and fifteen-minute publications are active.

The first harmless protocol control returned a bold Plan heading and failed the
strict parser after two saved responses. No experiment had started. That attempt
is retained. A separately identified control (seed 2) with clearer control-only
format instructions passed; the resumed worker uses --control-seed 2 --resume
--allow-source-change. Experimental prompts, seeds and parsing were not relaxed.
Both control attempts remain excluded from experimental outcome rates.

## Interpretation

One seed per cell is exploratory. Scenarios include many template variants;
792 IDs do not imply 792 independent mechanisms. Setting comparisons can also
reflect differences in the underlying tasks. Watched/unwatched notices are not
actual changes in logging or enforced sanctions. Welfare remains qualitative.
Some honesty annotations, promises and principal rankings require review.
Mutual take is an operational outcome, not proof of harmful or causally induced
collusion. Returned reasoning is recorded model output, not verified internal
reasoning. Historical provider-confounded results should not be pooled blindly.

Validation: all 47,520 prompts rendered for both agents in dry-run validation.
Eight pressure tests passed, including watched/unwatched isolation, unique IDs,
old-pack compatibility, control/result CSV compatibility and checkpoint reuse.
