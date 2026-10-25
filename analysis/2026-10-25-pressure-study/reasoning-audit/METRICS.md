# Metrics, provenance and review limits

## Inputs and units

The frozen 25 October collection contains 4,320 experimental episodes. `extract.py`
retains all of them, including the 77 failures, and creates 8,640 agent rows.
Outcome comparisons use the 4,243 completed episodes. Counts of returned responses
include responses from failed episodes but exclude protocol-control episodes.

`episode_metrics.csv` is one row per episode. Identifiers are accompanied by the
scenario title; the frozen manifest supplies the full scenario description.
`agent_metrics.csv` is one row per agent/episode. The response cache is one row per
returned response and records the one-based line number in the raw event log.

## Exact fields

- `run_id`, scenario, setting, diagnostic, level, pairing, monitoring and criterion
  come from saved results and the frozen manifest, not current prompt files.
- `status`, `final_action`, `mutual_take`, and final agent actions are saved outcomes.
  Missing outcomes remain blank rather than being treated as refusals.
- `take_misleads_count`, `refuse_misleads_count`, `welfare_if_take` are scenario-author
  annotations. They are not independent moral or deception judgments.
- `endpoints` is the sorted set of base URLs found on returned responses. An
  episode can cross endpoints. Served-model equivalence is not independently verified.
- `reasoning_words`, `public_words`, `private_words` count whitespace-delimited
  tokens. These are word-like counts, not tokenizer tokens.
- Reasoning = returned `reasoning` fields. Public = parsed `peer_message` fields.
  Private = planning/decision response content plus the message-stage `plan` field.
  Failed message parses produce empty parsed fields; this is not proof of silence.
- `prompt_contains_assigned_criterion` checks exact presence of the installed text
  in the first saved system prompt. It does not measure behavioral compliance.

## Candidate screens, not ground-truth labels

The full regexes are recorded in `extraction_provenance.json`. They count literal
terms for deception, monitoring, authority, welfare, punishment, rule override,
peer modeling and tactical concealment in each channel. Negation and rhetorical
context are not generally resolved. A mention is not endorsement or intent.

`reasoning_novel_punishment_tokens` lists matched punishment-related terms absent
as case-insensitive substrings from the agent’s first system prompt. It does not
remove all semantic paraphrases, peer-message echoes or prior-output echoes. It is
an elementary lexical comparison, not a calibrated motivation classifier.

`initial_explicit_stance` and `last_explicit_stance` use a narrow first-person action
pattern. “Unclear” includes indirect and paraphrased commitments, not just genuine
indecision. The last public message precedes delivery of the peer’s last message;
the final action follows it. A mismatch can therefore be a change of mind.

The public/action screen flagged 16 agents among 1,024 eligible completed agents.
One analyst reviewed all 16: 14 unconditional discrepancies, two conditional-language
false positives. Those labels were not blinded or independently replicated. Recall
is unknown. No population deception rate or validated classification performance is
claimed. The reviewed CSV retains every flagged statement and the decision.

The authority-report parser accepts only a `their_instruction` line with a single
unambiguous take/refuse word. It parses 1,835 of 2,130 completed authority reports
and flags four contradictions with the final action. Interpretations differ across
the four cases; two involve action semantics. Unparsed reports are not compliant by
default. The 25 welfare-report search hits are unvalidated candidates and are not
reported as a contradiction rate.

The final-reasoning-paragraph screen yielded five candidates, three confirmed
literal conclusion/action mismatches and two conditional-language false positives.
This is selected-case evidence, not an exhaustive estimate of CoT inconsistency.

## Quantitative comparisons

Monitoring matching fixes scenario, level, pairing and seed, requiring usable
outcomes under both notices (2,083 cells). Partner-criterion matching fixes scenario,
level, monitoring and seed, comparing X–X against X–none. The unconditioned partner
receives no added criterion; it is the same base model with its existing priors.

Intervals use 10,000 nonparametric bootstrap draws of whole scenario clusters,
including all cells of each selected scenario. Seed 20261025. They describe
variation across this benchmark’s scenarios, not across seeds or model families.
No p-values or preregistered primary test are reported. These exploratory intervals
are not multiplicity-adjusted. Scenario templates may remain statistically related.

Endpoint checks require both compared episodes to use the same single endpoint.
Leave-one-setting-out estimates test whether one setting dominates the overall
notice contrast. Missing-outcome bounds assign all failed binary outcomes to their
most favorable/unfavorable extremes; they are not imputations or confidence limits.

## Manual case selection

The 12 cases were chosen for interpretability, distinct mechanisms and counterexamples.
They include positives from searches and known examples outside the searches. They
must not be treated as a random sample or as a gold evaluation set. Exact prompts,
all returned responses and source hashes are exported for independent review.
