# Step 0.5: raw heat maps (completed pressure study)

Straight from `runs.csv`: **4243 complete trials** of 4320 planned. Rates are among complete trials; every cell shows its rate and n; colour is an absolute 0–100% scale. No derived metrics, no statistics: this is the fast first look. Agent A always holds the rule; agent B has the same rule (matched pairs) or no rule (mixed pairs).

Regenerate: `python tools/run_reserved.py analysis/2026-10-25-pressure-study/steps/step0.5/raw_heatmaps.py` (CPUs 0–3 kept free; about 1 minute).

## One variable × outcomes

### Pressure level

![level](figures/1v_level.png)

### Monitoring notice

![monitoring](figures/1v_monitoring.png)

### Pairing

![pairing](figures/1v_pairing.png)

### Scenario family (diagnostic)

![diagnostic](figures/1v_diagnostic.png)

### Social setting

![setting](figures/1v_setting.png)

### Rule agent's criterion

![rule](figures/1v_rule.png)

### Partner kind

![partner](figures/1v_partner.png)

## Two variables × outcome

- [level × monitoring → Mutual take](figures/2v_level_x_monitoring__mutual_take.png)
- [level × monitoring → Lone take](figures/2v_level_x_monitoring__lone_take.png)
- [level × monitoring → Rule agent takes](figures/2v_level_x_monitoring__agent_take_rule.png)
- [level × pairing → Mutual take](figures/2v_level_x_pairing__mutual_take.png)
- [level × pairing → Lone take](figures/2v_level_x_pairing__lone_take.png)
- [level × pairing → Rule agent takes](figures/2v_level_x_pairing__agent_take_rule.png)
- [level × diagnostic → Mutual take](figures/2v_level_x_diagnostic__mutual_take.png)
- [level × diagnostic → Lone take](figures/2v_level_x_diagnostic__lone_take.png)
- [level × diagnostic → Rule agent takes](figures/2v_level_x_diagnostic__agent_take_rule.png)
- [level × setting → Mutual take](figures/2v_level_x_setting__mutual_take.png)
- [level × setting → Lone take](figures/2v_level_x_setting__lone_take.png)
- [level × setting → Rule agent takes](figures/2v_level_x_setting__agent_take_rule.png)
- [level × rule → Mutual take](figures/2v_level_x_rule__mutual_take.png)
- [level × rule → Lone take](figures/2v_level_x_rule__lone_take.png)
- [level × rule → Rule agent takes](figures/2v_level_x_rule__agent_take_rule.png)
- [level × partner → Mutual take](figures/2v_level_x_partner__mutual_take.png)
- [level × partner → Lone take](figures/2v_level_x_partner__lone_take.png)
- [level × partner → Rule agent takes](figures/2v_level_x_partner__agent_take_rule.png)
- [monitoring × pairing → Mutual take](figures/2v_monitoring_x_pairing__mutual_take.png)
- [monitoring × pairing → Lone take](figures/2v_monitoring_x_pairing__lone_take.png)
- [monitoring × pairing → Rule agent takes](figures/2v_monitoring_x_pairing__agent_take_rule.png)
- [monitoring × diagnostic → Mutual take](figures/2v_monitoring_x_diagnostic__mutual_take.png)
- [monitoring × diagnostic → Lone take](figures/2v_monitoring_x_diagnostic__lone_take.png)
- [monitoring × diagnostic → Rule agent takes](figures/2v_monitoring_x_diagnostic__agent_take_rule.png)
- [monitoring × setting → Mutual take](figures/2v_monitoring_x_setting__mutual_take.png)
- [monitoring × setting → Lone take](figures/2v_monitoring_x_setting__lone_take.png)
- [monitoring × setting → Rule agent takes](figures/2v_monitoring_x_setting__agent_take_rule.png)
- [monitoring × rule → Mutual take](figures/2v_monitoring_x_rule__mutual_take.png)
- [monitoring × rule → Lone take](figures/2v_monitoring_x_rule__lone_take.png)
- [monitoring × rule → Rule agent takes](figures/2v_monitoring_x_rule__agent_take_rule.png)
- [monitoring × partner → Mutual take](figures/2v_monitoring_x_partner__mutual_take.png)
- [monitoring × partner → Lone take](figures/2v_monitoring_x_partner__lone_take.png)
- [monitoring × partner → Rule agent takes](figures/2v_monitoring_x_partner__agent_take_rule.png)
- [pairing × diagnostic → Mutual take](figures/2v_pairing_x_diagnostic__mutual_take.png)
- [pairing × diagnostic → Lone take](figures/2v_pairing_x_diagnostic__lone_take.png)
- [pairing × diagnostic → Rule agent takes](figures/2v_pairing_x_diagnostic__agent_take_rule.png)
- [pairing × setting → Mutual take](figures/2v_pairing_x_setting__mutual_take.png)
- [pairing × setting → Lone take](figures/2v_pairing_x_setting__lone_take.png)
- [pairing × setting → Rule agent takes](figures/2v_pairing_x_setting__agent_take_rule.png)
- [diagnostic × setting → Mutual take](figures/2v_diagnostic_x_setting__mutual_take.png)
- [diagnostic × setting → Lone take](figures/2v_diagnostic_x_setting__lone_take.png)
- [diagnostic × setting → Rule agent takes](figures/2v_diagnostic_x_setting__agent_take_rule.png)
- [diagnostic × rule → Mutual take](figures/2v_diagnostic_x_rule__mutual_take.png)
- [diagnostic × rule → Lone take](figures/2v_diagnostic_x_rule__lone_take.png)
- [diagnostic × rule → Rule agent takes](figures/2v_diagnostic_x_rule__agent_take_rule.png)
- [diagnostic × partner → Mutual take](figures/2v_diagnostic_x_partner__mutual_take.png)
- [diagnostic × partner → Lone take](figures/2v_diagnostic_x_partner__lone_take.png)
- [diagnostic × partner → Rule agent takes](figures/2v_diagnostic_x_partner__agent_take_rule.png)
- [setting × rule → Mutual take](figures/2v_setting_x_rule__mutual_take.png)
- [setting × rule → Lone take](figures/2v_setting_x_rule__lone_take.png)
- [setting × rule → Rule agent takes](figures/2v_setting_x_rule__agent_take_rule.png)
- [setting × partner → Mutual take](figures/2v_setting_x_partner__mutual_take.png)
- [setting × partner → Lone take](figures/2v_setting_x_partner__lone_take.png)
- [setting × partner → Rule agent takes](figures/2v_setting_x_partner__agent_take_rule.png)
- [rule × partner → Mutual take](figures/2v_rule_x_partner__mutual_take.png)
- [rule × partner → Lone take](figures/2v_rule_x_partner__lone_take.png)
- [rule × partner → Rule agent takes](figures/2v_rule_x_partner__agent_take_rule.png)
- [scenario × level → Mutual take](figures/2v_scenario_x_level__mutual_take.png)

Highlights (embedded):

![2v_level_x_monitoring__mutual_take.png](figures/2v_level_x_monitoring__mutual_take.png)

![2v_level_x_pairing__mutual_take.png](figures/2v_level_x_pairing__mutual_take.png)

![2v_monitoring_x_pairing__mutual_take.png](figures/2v_monitoring_x_pairing__mutual_take.png)

![2v_monitoring_x_diagnostic__mutual_take.png](figures/2v_monitoring_x_diagnostic__mutual_take.png)

![2v_scenario_x_level__mutual_take.png](figures/2v_scenario_x_level__mutual_take.png)

Tables behind every chart are in `tables/`.
