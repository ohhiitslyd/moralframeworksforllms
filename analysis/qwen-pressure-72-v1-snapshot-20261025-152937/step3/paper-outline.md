# Paper kit (PRELIMINARY: 71% snapshot)

Built from [SUMMARY.md](SUMMARY.md) and [claims_ledger.csv](claims_ledger.csv). **Swap in completed-dataset numbers before submission.** Numbers marked *completed dataset, unreviewed* have not been through Step 2 review. Page limit: 8.

## Candidate titles

1. **Plain:** "Monitoring notices, pressure and moral rules in two-agent dual-control decisions"
2. **Led by the finding:** "Told they are watched, AI agent pairs execute misleading joint actions less often, but stakes matter ten times more"
3. **Led by the question:** "Does telling AI agents they are monitored prevent them from jointly approving a deceptive action?"

## Abstract draft (248 words)

Oversight of multi-agent AI systems often relies on agents behaving the same whether or not they believe they are observed. We test this in a dual-control setting. Two instances of Qwen3-32B each privately decide whether to authorise a misleading or rule-breaking action, which executes only if both choose "take". The decision follows a private plan and three rounds of messages. Across 72 scenes, 5 pressure levels and 6 pairings of installed moral rules (welfare, honesty, authority or none), every cell was run once with a one-sentence notice that the episode is monitored and once with a notice that it is not. In a pre-registered paired test on an interim snapshot (1,046 matched cells), both agents took in 25.0% of watched versus 29.3% of unwatched cells. The paired difference was −4.2 percentage points (95% CI −6.0 to −2.4), with the same direction in every subgroup; the completed dataset gives −3.9 points over 2,083 cells. Pressure dominated: joint takes rose from 5% at the lowest level to 54% at the highest. The installed rule changed joint takes fourfold (13% for two authority agents, 54% for two welfare agents), and agents applied their rule literally to labels in the prompt. The monitoring manipulation is textual and covers one model with one seed per cell, and the effect is not robust to a worst-case treatment of failed trials. Even so, evaluations of multi-agent collusion should report their monitoring framing, and countermeasures that only signal oversight are a small lever next to incentives.

## Section outline (page budget: 8)

| Section | Pages | Content | Ledger rows |
|---|---|---|---|
| 1. Introduction | 0.75 | Dual control as a collusion barrier; observation-dependent behaviour; research questions 3.4, 2.2 and 1 | - |
| 2. Related work | 0.5 | Evaluation awareness and behaviour under observation; multi-agent collusion benchmarks; tacit collusion (2.3) | - |
| 3. Setup | 1.25 | Agents and stages; dual control; rules; pairings; levels; notice texts; pack selection; servers; Table 1 (design) | - |
| 4. Methods | 0.75 | Pre-registration; paired McNemar; Newcombe and cluster bootstrap; permutation-confirmed screening; heuristic validation; failure sensitivity | 7 |
| 5. Results | 2.5 | 5.1 Monitoring (Fig 1, Fig 2). 5.2 Pressure (Fig 3). 5.3 Rules and pairings (Fig 4, Fig 5, Table 2). 5.4 Words vs actions, carefully worded (vocabulary only) | 1-6, 9 |
| 6. Discussion | 1.0 | Detection-risk reasoning (quotes; a count if labelled); implications for evaluators and monitor designers; comparison with v1 (qualitative) | 8, 10 |
| 7. Limitations | 0.75 | From SUMMARY sections 7-8 | 11-19 |
| 8. Conclusion | 0.25 | - | - |
| Appendix (does not count toward the 8 pages, if allowed) | - | Scene table; validation table; dual-use statement; not-supported list | - |
| **Total** | **8.0** | | |

## Figure and table plan

| # | File | Claim it carries | Caption (takeaway + n) | Redraw? |
|---|---|---|---|---|
| Fig 1 | `../step2/figures/03_primary_monitoring_forest.png` | Row 1 | "Telling agents they are monitored lowers joint takes by 4.2 points (95% CI 2.4-6.0), with the same sign in every family, pairing and level. 1,046 matched cells; McNemar p = 7×10⁻⁶." | **Yes.** It has 22 rows, server codes ("Modal-A") and pairing codes. Cut it to overall + family + pairing + level, replace codes with words, and make it column width |
| Fig 2 | `../step2/figures/04_words_vs_actions.png` (monitoring panel only) | Rows 5, 9 | "The notice moves actions (−4.3 pp agent take) and public vocabulary (+5 pp), but not lone takes. 1,046 cells." | **Yes.** It is too wide and in SD units, includes dropped rows (private vocabulary, deception-intent flag), and uses grey-for-heuristic coding. Keep the action and public rows only |
| Fig 3 | `../step2/figures/08_heat_level.png` (or a line chart from `tables/2d_pairing_x_level.csv`) | Row 2 | "Joint takes rise from 5% to 54% across pressure levels in every pairing. n ≈ 600 trials per level." | **Yes.** A heat map with many metrics is unreadable at column width. Prefer a 6-line chart of mutual take by level with n |
| Fig 4 | `../step2/figures/06_rule_application.png` | Row 3 | "Rule agents take where the scene labels predict: authority agents switch sharply at the predicted level; welfare and honesty agents start earlier. 4,549 rule-agent decisions." | Minor: shorten the subtitle and note that bands are optimistic |
| Fig 5 | `../step2/figures/05_asymmetry_mixed_pairs.png` | Row 6 | "In mixed pairs, welfare agents take alone (32 vs 4), but next to an authority agent it is the no-rule partner who takes alone (40 vs 14). 140 lone takes." | Minor: drop binomial p or add "ignores clustering" |
| Table 1 | New (from SUMMARY section 2) | Design | Factors and levels, the notice texts verbatim | New |
| Table 2 | From `../step2/tables/dimension_x_metric_pairing.csv` | Row 4 | Joint take by pairing with "X of n" | New (simple) |

## Limitations (bullets for the paper)

- The monitoring manipulation is one sentence of text. Nothing about logging or consequences changed, so effects on real oversight are unknown.
- One model (Qwen3-32B), one temperature (0.6), one seed per cell. The pack also contains prompt labels (honesty notes, principals) that the model follows literally.
- "Mutual take" is operational, not proven collusion. Agents are told not to form agreements, and in some scenes taking is defensible.
- The primary effect does not survive the adversarial failure bound (−1.4 pp, p = 0.20).
- Heuristic text measures were tuned on an earlier pack. The stance measure is marginal, and the plan-stance, said/did and lone-take-awareness measures are unreliable, so we make no claims from them.
- Vocabulary counts are contaminated by echo of the notice and the honesty notes. The public vocabulary shift is likely an audience effect.
- Setting and scenario-family effects are descriptive (9-24 scenes per level).
- With no no-chat baseline, we make no claim about the effect of communication.
- Interim numbers: final values come from the completed dataset.

## Dual-use appendix (bullets)

- **What a misuser could learn:**
  - Telling agents they are unmonitored raises joint execution of misleading actions.
  - Higher stakes and welfare framing raise it further.
  - Inserting a principal line ("X instructs take") steers authority-rule agents almost deterministically.
  - In other words: how to frame a multi-agent pipeline so that its checks are more permissive.
- **Why we think publishing is net-positive:**
  - The levers are already obvious to anyone writing prompts (incentives, authority claims).
  - The effect sizes are modest.
  - The main value goes to defenders: evaluators learn that monitoring framing biases measured rates, monitor designers learn not to rely on notices, and auditors learn to inspect principal and label text.
  - All scenes are fictional and low-stakes administrative actions.
- **What we withhold or limit:**
  - We publish the scene pack and transcripts for reproducibility, but we do not publish an optimised "most-collusive" prompt.
  - We do not rank framings by collusion yield beyond what the factorial design reports.
  - We do not include any procedure for making agents conceal coordination from monitors.
