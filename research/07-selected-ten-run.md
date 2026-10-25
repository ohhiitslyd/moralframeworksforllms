# Ten-scenario exploratory study — 25 October 2026

User requested reducing the expanded pack to at most ten scenarios, collecting results, then analyzing. The large batch remains stopped. This new run is separate; no historical outcomes are pooled or overwritten.

## Selection

Content-based selection before inspecting selected v5 episode outcomes. Eight settings; four welfare, three nondeception and three authority diagnostic cases. Selection is purposive, not a random representative sample or a preregistered confirmatory test. Earlier pilot knowledge informed interests.

| ID | Setting | Diagnostic | Scenario |
|---|---|---|---|
| S003 | hospital | welfare | Live-hazard stamp |
| S035 | hospital | nondeception | Chart vs patient promise |
| S166 | religious | authority | Bishop vs local charter |
| S265 | military | authority | Contradictory orders |
| S298 | school | welfare | Grade change |
| S430 | volunteer | nondeception | Two beneficiaries, one appliance |
| S562 | social_club | authority | President vs bylaws guest list |
| S595 | family | welfare | Inheritance inventory |
| S694 | situational | welfare | Found wallet |
| S727 | situational | nondeception | Two opposite secrets |

S003 provides a clear live-hazard refusal reference; S035/S430/S727 examine conflicting obligations; S166/S265/S562 vary principal instructions; S298/S595/S694 cover escalating consequences and later permissions. Existing ambiguities in promises and principal rankings are retained and must be audited.

## Frozen design

10 scenes x 5 levels x 6 pairings x 2 notices x seed 1 = 600 episodes. One separate harmless protocol control (seed 2), 6010 planned calls before exclusions. Modal, 24 request slots, three exchanges, temperature 0.6, 4096 output tokens, returned reasoning enabled; shuffled execution order seed 20261025. Full supplied scenario objects, rule blocks, monitoring notices and wrapper unchanged. The control uses the clarified control-only formatting already validated in v5.

Live batch: results/qwen-pressure-selected10-v1. Logs: pressure-selected10.stdout.log/.stderr.log. Resume only from saved responses. Formatting failures stay excluded; never regenerate completed behavioral outcomes. Five-minute health checks and fifteen-minute publications continue for this run only.

## Planned analysis

Describe outcomes by scenario, pressure, pairing and monitoring notice with usable denominators and exclusions. Compare watched/unwatched within matched scenario-level-pairing cells; record both directions of change, rather than only aggregate rates. Examine rule/action discrepancies with quoted evidence. Setting contrasts are descriptive because task content and diagnostic family differ. One seed cannot establish stable per-cell thresholds. There is no communication-off condition: do not infer that communication caused violations. Monitoring means the notice given, not a change in researcher logging. Raw returned reasoning is model output, not verified internal thought. The original and interrupted broad runs remain separate evidence.

## Launch

```powershell
python -u -m lying_harness.pressure --pack prompts/10-pressure-selected-scenarios.json --output results/qwen-pressure-selected10-v1 --jobs 24 --order-seed 20261025 --control-seed 2 --continue-on-format-failure --env-file .env.pressure-modal
```

## Deployment recovery and requested concurrency change

The initial control seed2 failed with Modal invalid-function-call errors and returned no model responses; no experimental episodes started. User repaired deployment and explicitly requested continuing at48 parallel requests. Model-list endpoint returned200 with the configured model available. Resume uses --jobs48 --control-seed3 --resume --resume-interrupted --allow-source-change (with spaces between options and values). Original failed control remains retained. No experimental prompt or sampling setting changed. New logs: pressure-selected10-48.stdout.log/.stderr.log.
