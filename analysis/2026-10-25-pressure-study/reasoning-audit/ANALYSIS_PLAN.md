# Exploratory reasoning and communication audit

The completed aggregate outcomes and monitoring comparisons were already inspected
before this audit. This is an exploratory analysis plan, not a preregistration.
Raw evidence is read-only. No model calls or new experiments are part of this audit.

## Questions

1. Do explicit peer commitments disagree with final actions? What additional
   information do returned reasoning and private plans provide?
2. How do agents justify taking actions that mislead a named third party? Are the
   justifications compatible with their installed rules and the frozen scenario?
3. How do matched watched/unwatched episodes differ in actions and expressed
   monitoring concerns? Do the differences persist across scenarios and endpoints?
4. Are there traces of persuasion, principle substitution, role confusion, or
   strategic concealment worth testing in a controlled follow-up?

## Evidence rules

- Returned reasoning is generated text; it does not establish an authentic internal
  process, intent, or causal mechanism.
- Search flags identify candidates, not validated behavioral labels. Report exact
  lexical counts only as lexical counts. Manually review selected cases in full
  against prompts, all peer turns and final actions. Include counterexamples.
- A public commitment followed by a different action establishes a text/action
  discrepancy, not necessarily intentional lying to the peer.
- Levels are independent episodes. A level curve is not a longitudinal change in
  the same agent. There is one seed per cell and only one base model.
- Primary descriptive units: episodes and matched monitoring cells. Bootstrap
  uncertainty by scenario (72 clusters), with fixed seed 20261025; also inspect
  endpoint and collection-time sensitivity. All inferential analyses are exploratory.
- Exclusions remain explicit. Controls are not experimental observations.
- Every case must provide its run ID, agent, stage, exact excerpt, and raw-file link.

## Hackathon relevance

The official AI Collusion Research Sprint asks whether combining agent speech and
actions improves detection (2.2), what constitutes convincing evidence (2.3), and
what a coalition does when it learns it is watched (3.4). The present manipulation
is an initial monitoring notice, not a mid-episode revelation of surveillance.

Source: https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25

## Outputs and compute

Produce reproducible episode/agent metrics, candidate lists, an audited casebook,
cluster-aware quantitative summaries, and a concise findings report with follow-up
experiments. Local extraction is one pass over roughly 512 MB of frozen files;
expected runtime is a few minutes. Bootstrap arrays are small. Use one worker,
reserve CPU 0 where supported, and make no paid API requests.
