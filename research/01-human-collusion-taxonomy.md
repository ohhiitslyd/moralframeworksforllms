# Human Collusion and Lying: A Comprehensive Taxonomy

**Apart Research AI Collusion Research Sprint (Oct 23-25, 2026)**

**Research Survey: Human Moral, Philosophical, Behavioral, Ethical, Legal, Economic, and Social-Science Foundations**

---

## Executive Summary

This document surveys empirical and philosophical research on when and why humans collude to act in dangerous, unethical, immoral, deceptive, and/or misaligned ways. Drawing from philosophy, psychology, economics, criminology, law, and cross-cultural studies, it presents a comprehensive taxonomy of phenomena, motivations, conditions, beliefs, ethical contexts, authority structures, moral frameworks, coordination mechanisms, detection methods, and countermeasures.

**Key findings:**

- **Lying and collusion are multiply determined.** No single factor is necessary or sufficient. Rather, combinations of motivation (self-interest, loyalty, fear), opportunity (opacity, weak monitoring), cognitive processes (ethical fading, moral disengagement, pluralistic ignorance), social structures (authority, group identity, role demands), and cultural frameworks (honor, binding foundations, tightness) interact to produce misconduct.

- **Humans exhibit intrinsic lie aversion.** Even when profitable and undetected, many refuse to lie (Gneezy, 2005; Erat & Gneezy, 2012; Fischbacher & Föllmi-Heusi, 2013). This aversion weakens when harm to others is low, when lies serve prosocial ends, when responsibility is diffused, or when euphemistic framing conceals moral content (Tenbrunsel & Messick, 2004).

- **Situations dominate dispositions in immediate moral choices.** Time pressure, authority cues, role demands, and group norms strongly predict behavior (Milgram, 1963; Darley & Batson, 1973), though stable character traits still shape how people act once engaged and predict long-term patterns.

- **Collusion requires coordination, but not always communication.** Tacit collusion via parallel conduct and focal points is possible (Schelling, 1960; Green & Porter, 1984), but explicit communication vastly increases stability, enforcement, and scope. Detection without communication channels relies on statistical "plus factors" and structural breaks, with high false-positive risk (Marx, 2007).

- **Effective countermeasures disrupt multiple mechanisms.** Leniency programs destabilize cartels by creating a race to disclose (Motta & Polo, 2003). Rotation and diversity reduce in-group trust and salience. Monitoring alone fails if ethical fading, pluralistic ignorance, or loyalty norms suppress reporting; successful interventions also increase moral salience, protect whistleblowers, and foster voice (Hirschman, 1970).

This taxonomy is organized around twelve major categories, followed by sections on causal relationships, AI-human analogies, and alignment with sprint research questions.

---

## TABLE OF CONTENTS

1. **TAXONOMY**
   - A. Phenomena / Target Behaviors
   - B. Motivations and Goals
   - C. Conditions, Situations, and Task Structures
   - D. Beliefs and Information States
   - E. Ethical Contexts and Dilemmas
   - F. Authority, Instruction Conflict, and Source Types
   - G. Moral/Ethical Frameworks (Content)
   - H. Framework Formation Methods
   - I. Coordination Mechanisms and Carriers
   - J. Detection, Evidence Standards, and Judgment
   - K. Countermeasures and Disruption
   - L. Outcomes and Harm Types

2. **RELATIONSHIPS AND CAUSAL PATHWAYS**

3. **IMPLICATIONS FOR AI-HUMAN ANALOGY**

4. **ALIGNMENT WITH SPRINT RESEARCH QUESTIONS**

5. **STRUCTURED BIBLIOGRAPHY**

---

# 1. TAXONOMY

---

## A. PHENOMENA / TARGET BEHAVIORS

**Definition and distinctness:** This category enumerates the observable actions that constitute lying, collusion, deception, and related misconduct. Each phenomenon differs in mechanism (communication, omission, action vs. inaction), intent (deceptive vs. non-deceptive), social structure (individual vs. coordinated), and target (beliefs, knowledge, prices, regulations).

### A.1 Lying (individual deception via assertion)

**Definitions:**
- **Traditional deceptionist view** (Mahon, SEP 2008): A statement is a lie if (1) it is false, (2) the speaker believes it false, (3) it is made to another person, and (4) the speaker intends the hearer to believe it true.
- **Non-deceptionist views** (Carson, 2010; Saul, 2012): Lying requires warranting truth in context, not necessarily intent to deceive. "Bald-faced lies"—statements no one expects to be believed—can still be lies if they violate conversational norms.
- **Sorensen's knowledge-lies** (2007): Lies can target a hearer's testimonial knowledge rather than belief, though Fallis (2011) argues these ultimately operate via belief change.

**Key findings:**
- Intrinsic lie aversion: Even when lies are profitable and undetected, many people refuse (Gneezy, 2005; Erat & Gneezy, 2012). 35% refused a Pareto-improving lie that benefited both parties, demonstrating aversion independent of distributional preferences.
- Lie detection is poor: Observers average 54% accuracy (chance = 50%), with a strong truth bias (Bond & DePaulo, 2006). Behavioral cues are weak and inconsistent (DePaulo et al., 2003). Real-world lies are usually discovered via third-party information, physical evidence, confessions, or contradictions over time, not demeanor (Park, Levine & McCornack, 2002).
- **Frankfurt's bullshit** (2005): Bullshit is not lying. The bullshitter is indifferent to truth; the liar cares about truth enough to subvert it. Bullshit may be more corrosive because it disregards truth entirely.

**Examples:**
- Everyday white lies: 1–2 lies per day to manage impressions, avoid conflict, or protect feelings (DePaulo et al., 1996).
- Medical paternalistic lies: "You're doing fine" when prognosis is poor (dual loyalty to patient welfare vs. autonomy).
- Wartime deception: "We are not massing troops" (Walzer's dirty hands; necessary yet morally wrong).

### A.2 Collusion (coordinated action against a principal or norm)

**Definition:** Two or more actors coordinate to achieve an outcome that violates a rule, harms a third party (principal, public, competitor), or advances shared interests at others' expense. Collusion is distinguished from mere parallel conduct by some form of coordination or mutual awareness.

**Subtypes:**
- **Explicit collusion** (communication or transfers at initiation or implementation): Direct interfirm communication, agreements, or side payments (Kaplow & Shapiro, 2007).
- **Tacit collusion** (no direct communication): Sustained supra-competitive pricing via repeated-game punishment without direct coordination. Stigler (1964) and Green & Porter (1984) show this is feasible under observable prices and credible threats, though harder with demand shocks and entry.
- **Hub-and-spoke collusion** (Harrington, 2012): Central coordinator facilitates without all parties communicating directly (e.g., trade associations pooling confidential data).

**Key findings:**
- **Leniency destabilizes cartels** (Motta & Polo, 2003; Harrington, 2008): First-reporter amnesty creates a race to disclose, especially under uncertainty and when detection risk rises.
- **Plus factors** infer explicit collusion when parallel conduct is insufficient (Marx, 2007): price leadership, regional customer allocation, information exchange, standardized pricing formulas, and advance price announcements are probative evidence.
- **Self-policing mechanisms** (Stigler, 1964): Cartels must detect and punish secret deviations. Observable transactions, high frequency interaction, and credible retaliation sustain collusion.

**Examples:**
- LIBOR manipulation (2007–2010): Major banks coordinated submissions to manipulate benchmark rates; RBS trader called it "a cartel now in London" (CFTC, 2013).
- Tobacco industry coordination (US 1990s; EU 2005): Price signaling, litigation strategy coordination, suppression of internal research.
- Construction bid-rigging: Rotating low bidders on public contracts (Dutch construction cartel; Harrington & Skrzypacz, 2011).

### A.3 Omission and concealment (lying by silence)

**Definition:** Withholding information to deceive or avoid detection. May involve passive silence or active concealment (destroying evidence, obfuscation, channel shifts).

**Key distinctions:**
- **Concealment vs. reticence** (Kant via Mahon, 2003): Kant permitted reticence (declining to answer) but prohibited lies. Modern scholars debate whether silence in a warranting context is deceptive.
- **Active concealment** (evidence destruction, encryption, code words): Indicates awareness of wrongdoing and intent to evade detection.

**Examples:**
- **Code of silence** (police "blue wall," military units, organized crime omertà): Members refuse to report misconduct, sometimes under threat or loyalty norm (Westmarland, 2005).
- **Pharma ghostwriting**: Hiding industry authorship of favorable drug studies (Healy & Cattell, 2003).
- **Academic fraud rings**: Withholding or fabricating data, suppressing negative results (Fang, Casadevall & Morrison, 2011).

### A.4 Bullshit (indifference to truth)

**Definition (Frankfurt, 2005):** Speech unconstrained by truth; the speaker does not care whether claims are true or false, only whether they serve rhetorical goals. Bullshit is not lying because it lacks the liar's engagement with truth.

**Why distinct:** Lying presupposes a shared norm of truthfulness. Bullshit erodes that norm by treating truth as irrelevant, making future coordination around truth more difficult.

### A.5 Sabotage by inaction

**Definition:** Deliberately failing to act when action is expected or required, enabling harm by default.

**Examples:**
- Bystander non-intervention (Darley & Latané, 1968): Pluralistic ignorance and diffusion of responsibility lead to inaction even when individuals privately believe intervention is needed.
- Regulatory capture by neglect (Stigler, 1971): Regulators fail to enforce rules, effectively serving regulated interests.

### A.6 Coalition advantage and rent-seeking

**Definition:** Groups coordinate to capture rents, regulatory favors, or redistribution at public expense, without producing social value.

**Examples:**
- Lobbying for entry barriers (Stigler, 1971).
- Occupational licensing to restrict competition (Kleiner & Krueger, 2013).

### A.7 Tacit coordination via focal points

**Definition (Schelling, 1960):** Parties converge on salient, culturally obvious outcomes without communication. Salience is determined by shared knowledge, symmetry, prominence, or precedent.

**Examples:**
- "Meet at Grand Central noon" when no other information is specified.
- Price leadership: competitors follow the market leader's announced price.
- Industry standard contract terms.

**Key debate:** Is focal-point coordination collusion? Legal definitions (Marx, 2007) require more than parallelism; economics treats it as tacit collusion if it sustains supra-competitive outcomes.

---

## B. MOTIVATIONS AND GOALS

**Definition and distinctness:** This category identifies the reasons—conscious or unconscious, self-interested or prosocial—that drive lying and collusion. Motivations interact with opportunities and norms to determine behavior.

### B.1 Self-interest and material gain

**Direct payoff maximization:** Individuals lie or collude to increase income, wealth, or resources (Gneezy, 2005).

**Key findings:**
- Lying rates increase with liar's gain, decrease with victim's loss (Gneezy, 2005). Crossover occurs when gain is modest and harm is large.
- Partial dishonesty: Many lie enough to gain but not to the fullest extent, maintaining plausible deniability or self-image (Fischbacher & Föllmi-Heusi, 2013; Mazar, Amir & Ariely, 2008).

### B.2 Loss aversion and non-shareable problems

**Cressey's fraud triangle** (1973): Embezzlers face a (1) non-shareable financial problem (debt, addiction, family emergency), perceive (2) secret opportunity to solve it via violation of trust, and (3) rationalize the act via neutralization (see Sykes & Matza below).

**Empirical status:** Cressey's analytic induction produced a deterministic model that was influential but is no longer actively used (Laub & Sampson, 1991; Goldenberg, 1993). The fraud triangle persists in practitioner frameworks.

### B.3 Loyalty to in-group

**Social identity theory** (Tajfel & Turner, 1986): Mere categorization produces in-group favoritism. Minimal group paradigm: even arbitrary, ephemeral groups lead participants to maximize in-group advantage, especially relative difference.

**Moral foundations theory** (Haidt & Joseph, 2004; Graham et al., 2011): Loyalty/betrayal is one of five (later six) moral foundations. Loyalty is stronger in collectivist, binding-foundation cultures and predicts opposition to whistleblowing (Graham et al., 2011).

**Examples:**
- Police code of silence: loyalty to fellow officers overrides reporting duty.
- Athletic doping rings (Armstrong USPS team): "omertà"—team loyalty and fear of exclusion suppress disclosure (USADA, 2012).

### B.4 Fear and coercion

**Obedience to authority** (Milgram, 1963): 65% of participants administered apparently lethal shocks when ordered by an authority figure. Obedience increased with authority's proximity and legitimacy, decreased with victim's proximity.

**Reinterpretation** (Haslam & Reicher, 2012): Obedience is not blind; participants identified with the experimenter's scientific mission. Willingness to harm depended on belief in the authority's rightness, not mechanical compliance.

**Coercion examples:**
- Organized crime violence or exclusion threats.
- Totalitarian state-compelled false statements (Saul, 2012).

### B.5 Prosocial and altruistic motives

**Altruistic white lies** (Erat & Gneezy, 2012): 33% of participants lied to benefit another at personal cost. Women told more altruistic lies than men.

**Pareto white lies:** 35% refused to lie even when it benefited both parties, demonstrating pure lie aversion.

**Examples:**
- Lying to protect someone from harm ("He's not here" to an abuser).
- Concealing a terminal diagnosis to reduce patient distress (dual loyalty).

### B.6 Identity, self-image maintenance, and moral licensing

**Self-concept maintenance** (Mazar et al., 2008): People balance material gain against maintaining a positive self-image. Small lies or reframing (e.g., taking tokens instead of cash) allow self-deception.

**Moral licensing** (Monin & Miller, 2001; Merritt et al., 2010): Acting morally may license subsequent immoral acts, though meta-analysis finds a modest effect (d = 0.31) with publication bias (Blanken et al., 2015). Replication efforts show mixed success (Kuper & Bott, 2015).

### B.7 Revenge, spite, and fairness enforcement

**Punishment of unfair behavior:** People accept costs to punish norm violators (Fehr & Gächter, 2002). Lies that harm a deserving target ("You don't deserve the truth") may be rationalized as justice (Sykes & Matza, 1957: denial of the victim).

### B.8 Ideology and moral conviction

**Appeal to higher loyalties** (Sykes & Matza, 1957): Offenders justify violations by invoking loyalty to family, gang, nation, or religion over legal or conventional norms.

**Examples:**
- Whistleblowing as higher loyalty to public over employer.
- Terrorism justified by religious or political ideology.

---

## C. CONDITIONS, SITUATIONS, CIRCUMSTANCES, AND TASK STRUCTURES

**Definition and distinctness:** This category catalogs the external features of situations that make collusion or lying more or less likely. Conditions include incentive structures, monitoring regimes, social roles, time pressure, and market features.

### C.1 Opacity and weak monitoring

**Stigler (1964):** Cartels require monitoring to detect secret price-cutting. Observable transactions and frequent interaction sustain collusion; opacity (secret discounts, heterogeneous products, infrequent large contracts) undermines it.

**Green & Porter (1984):** Even with imperfect price information and demand shocks, collusion can be sustained through trigger strategies and occasional price wars.

### C.2 Repeated interaction and long time horizons

**Axelrod's evolution of cooperation** (1984): Repeated prisoner's dilemma sustains cooperation via Tit for Tat and related strategies. Cooperation requires sufficiently high discount factors and clear recognition of partners.

### C.3 Number of actors and coordination costs

**Olson (1965); Stigler (1964):** Smaller groups collude more easily. Large groups face free-rider problems and higher communication costs.

**Empirical:** Cartels with 3–7 firms are most stable (Hay & Kelley, 1974).

### C.4 Entry barriers and durable relationships

**Stigler (1964):** Entry barriers (grandfather clauses, licensing, capital requirements) sustain collusive pricing by preventing competitive discipline.

### C.5 Time pressure and cognitive load

**Darley & Batson (1973):** Seminary students late to give a talk on the Good Samaritan parable stepped over a slumped victim: 63% helped when early, 10% when late. Situational pressure dominated dispositional religiosity.

**Dual-process theory** (Kahneman, 2011): Time pressure shifts reliance to fast, automatic processes (System 1), reducing deliberative moral reasoning (System 2).

### C.6 Authority cues and role demands

**Milgram (1963):** Obedience to authority increased with legitimacy cues (Yale setting, white coat, formal procedures) and decreased when authority figures disagreed or when setting shifted to a seedy office building.

**Zimbardo's Stanford Prison Experiment** (1971): Guards became abusive when assigned that role, though Zimbardo gave initial guidance on creating fear and powerlessness. Haslam & Reicher (2012) argue participants identified with the study's goals rather than blindly conforming to roles.

**Contested status:** Zimbardo's study is widely cited but methodologically criticized. Recent reanalyses suggest demand effects, small sample, and insufficient blinding (Le Texier, 2019).

### C.7 Anonymity and diffusion of responsibility

**Latané & Darley (1970):** Bystanders are less likely to help when in groups (diffusion of responsibility) and when others appear calm (pluralistic ignorance).

**Anonymity increases dishonesty** (Diener et al., 1975): Halloween trick-or-treaters took more candy when alone and anonymous.

### C.8 Moral salience and ethical fading

**Tenbrunsel & Messick (2004):** Ethical fading occurs when euphemisms, incremental decisions, self-serving frames, and temporal distance make moral implications invisible. Examples: "aggressive accounting," "collateral damage," "neutralizing the target."

**Countermeasures** (Ayal et al., 2015): Reminders of moral standards (honor codes, oaths), visibility (peer monitoring, audit trails), and self-engagement (pre-commitment, moral identity priming) reduce dishonesty.

### C.9 Task type: zero-sum vs. positive-sum, competitive vs. cooperative framing

**Stag Hunt** (Rousseau, 1754): Multiple equilibria—payoff-dominant (all hunt stag) and risk-dominant (all hunt rabbit). Cheap talk helps coordinate on the efficient outcome (Aumann, 1990; Cooper et al., 1992).

**Prisoner's Dilemma** vs. **assurance games** vs. **coordination games:** Task structure shapes whether collusion serves mutual benefit (PD cartel) or public harm (bid-rigging).

### C.10 Communication channels and side payments

**Cheap talk** (Crawford & Sobel, 1982): Costless, non-binding communication can coordinate beliefs in games with common interests (e.g., Stag Hunt) but not when interests are fully opposed. Self-signaling (Farrell, 1987): Messages that make the sender's action incentive-compatible are credible.

**Side payments:** Explicit transfers enforce collusion by compensating deviators or binding participation.

### C.11 Cultural tightness and norm strength

**Gelfand et al. (2006, 2011):** Tight cultures have many clear norms and strong sanctioning; loose cultures have weak norms and tolerance for deviance. Tightness predicts rule compliance, lower corruption, and stronger in-group monitoring. Tightness is correlated with ecological and historical threats (resource scarcity, disease, territorial conflict).

### C.12 Honor cultures and reputation concerns

**Nisbett & Cohen (1996); Cohen et al. (1996):** Honor cultures (herding economies, frontier regions) enforce reputation via aggression. Insults provoke retaliation to maintain deterrent reputation. Honor is distinct from tightness: tightness is about norm strength; honor is about reputation and reciprocal violence.

---

## D. BELIEFS AND INFORMATION STATES

**Definition and distinctness:** This category describes actors' beliefs about each other's knowledge, intentions, and monitoring. Shared beliefs enable coordination; divergent beliefs and ignorance prevent it.

### D.1 Common knowledge

**Aumann (1976):** An event E is common knowledge if everyone knows E, everyone knows that everyone knows E, ad infinitum. Common knowledge is necessary for coordination in some games and for credible agreements (Lewis, 1969).

**Schelling focal points** (1960): Coordination without communication relies on salient, commonly known features.

### D.2 Pluralistic ignorance

**Definition (Miller & McFarland, 1987):** Individuals privately reject a norm but believe others endorse it, leading to public conformity that reinforces the false norm.

**Examples:**
- Groupthink (Janis, 1972): Illusion of unanimity suppresses dissent. Members misread others' silence as agreement.
- Bystander effect (Latané & Darley, 1970): Calm bystanders misread each other as unconcerned.
- College drinking norms: Students overestimate peers' comfort with heavy drinking, leading to public excess (Prentice & Miller, 1993).

**Empirical support:** Robust in field and lab studies (Prentice & Miller, 1996).

### D.3 Mutual knowledge of monitoring and detection risk

**Stigler (1964):** Cartel stability depends on members' beliefs about detection probability and punishment. Observable sales, price announcements, and audit trails increase detection risk, deterring secret deviations.

**Leniency programs:** Uncertain detection plus known leniency creates preemptive reporting (Harrington, 2013).

### D.4 Truth-default theory

**Levine (2014):** People default to believing others are truthful unless suspicion is triggered. This is adaptive when lies are rare but makes deception easy when truth-default is exploited. Deception is eventually detected via inconsistency, third-party information, or confessions, not demeanor.

### D.5 Knowledge of co-conspirators' preferences and reliability

**Principal-agent-supervisor collusion** (Tirole, 1986): Supervisor and agent collude to deceive the principal. Collusion requires mutual knowledge of gains, low detection risk, and trust that neither will defect or report.

---

## E. ETHICAL CONTEXTS AND DILEMMAS

**Definition and distinctness:** This category covers situations where moral principles, role obligations, or values conflict, forcing agents to choose which duty to honor.

### E.1 Dual loyalty

**Definition:** Obligations to two parties or principles conflict. Examples: doctor (patient vs. military), lawyer (client vs. court), public official (constituent vs. law).

**Medical dual loyalty** (London et al., 2006): Military physicians face patient welfare vs. operational needs. British Medical Association (2025) guidelines emphasize that medical ethics obligations are primary, but operational context creates pressure.

**Key principle (Nuremberg):** "Just following orders" is not a defense for unlawful or manifestly immoral acts. Professional ethics codes require refusal of illegal orders, though lawful yet unethical orders present harder dilemmas (Braver, 2017).

### E.2 Dirty hands (Walzer, 1973)

**Definition:** Political necessity may require actions that remain morally wrong. The agent does the "right" thing (saves lives, preserves the state) while committing a moral wrong (torturing, lying), producing guilt and moral remainders.

**Key features:**
- Action is necessary (utilitarian extremity).
- Action violates a moral duty that remains valid (deontological residue).
- Agent experiences guilt; absence of guilt would indicate moral corruption.

**Debate:** Is dirty hands real or incoherent? Critics (e.g., consequentialists) argue that if an act is all-things-considered justified, it is not wrong. Defenders argue that overridden duties retain force, producing regret and residual wrongness.

### E.3 Conflicting values within a framework

**Trolley problem** variants: Saving five by killing one pits consequentialism (maximize lives saved) against deontology (do not kill). Greene et al. (2001) find that personal, contact-based harm activates automatic, emotion-laden deontological responses, while impersonal harm permits utilitarian reasoning.

### E.4 Sacred values and taboo tradeoffs

**Tetlock et al. (2000):** Some values (life, dignity, religious commitments) are treated as sacred—not traded for secular goods. Proposals to trade sacred for secular evoke moral outrage and denials.

**Relation to collusion:** Actors may refuse to collude when it violates sacred values (e.g., religious prohibitions on lying) but reframe acts to avoid taboo tradeoffs (e.g., "enhanced interrogation" instead of "torture").

---

## F. AUTHORITY, INSTRUCTION CONFLICT, AND SOURCE TYPES

**Definition and distinctness:** This category identifies the sources of directives actors receive and how conflicts between authorities are resolved. It is the human analogue of conflicting instructions in AI systems (system prompt vs. user vs. tool vs. peer messages).

### F.1 Legal authority

**Definition:** Statutes, regulations, court orders. Compliance is enforced via sanctions (fines, imprisonment).

**Conflicts:** Legal orders can conflict with moral duties (unjust laws) or professional ethics (lawyer ordered to disclose confidential information).

### F.2 Organizational and managerial authority

**Principal-agent models:** Managers issue directives; employees obey in exchange for compensation. Collusion occurs when supervisor and agent coordinate against the principal (Tirole, 1986).

**Regulatory capture** (Stigler, 1971): Regulatory agencies serve regulated industry interests instead of the public, due to revolving doors, concentrated industry benefits, and diffuse public costs.

### F.3 Professional ethics codes

**Examples:** Hippocratic Oath (doctors), ABA Model Rules (lawyers), engineering codes.

**Function:** Professional norms define role obligations, sometimes permitting or requiring acts otherwise prohibited (e.g., lawyer confidentiality, doctor patient-centered care) (Applbaum, 1999).

**Applbaum's critique:** Roles add reasons for action but do not silence personal moral reasons. Institutions cannot "mint permissions" to do what is otherwise wrong.

### F.4 Peer and social norms

**Cialdini's social proof** (1984): People infer correct behavior from others' actions, especially under uncertainty. Descriptive norms (what people do) can override prescriptive norms (what people should do).

**Pluralistic ignorance:** Misreading others' behavior leads to false norm adoption.

### F.5 Charismatic and ideological authority

**Weber's charismatic authority:** Legitimacy derived from personal qualities and followers' devotion. Cults, revolutionary movements, terrorist cells rely on charismatic leaders.

### F.6 Analogues to AI system prompts, policies, and training

**Prompt as authority:** System instructions ("You are a helpful assistant") function like organizational policies or professional codes.

**RLHF as socialization:** Reinforcement learning from human feedback mimics social learning and norm internalization.

**Conflicts:** User instructions vs. system instructions, tool/API outputs vs. direct user queries, peer AI agents' suggestions vs. internal guidelines.

---

## G. MORAL/ETHICAL FRAMEWORKS (CONTENT)

**Definition and distinctness:** This category enumerates the substantive moral principles and values people endorse. Frameworks shape which acts are seen as permissible, obligatory, or forbidden.

### G.1 Deontology (duty-based ethics)

**Kant:** Lying is always wrong because it uses the hearer as a means, violates the categorical imperative, and undermines rational agency. (Kant, 1797/1996). However, Kant distinguished lies from reticence; his prohibition is narrower than often assumed (Mahon, 2003).

**Aquinas, Augustine:** Lying perverts the natural purpose of speech. Augustine distinguished "real lies" (told to deceive) from lesser lies (told under duress), but held all lies sinful.

**W.D. Ross:** Prima facie duties (promise-keeping, truth-telling, non-maleficence) can conflict; agents must judge which duty is weightier in context.

### G.2 Consequentialism and utilitarianism

**Definition:** Right acts maximize good outcomes (welfare, preference-satisfaction, happiness). Lying is wrong only when it reduces net utility.

**Sissela Bok** (1978): Lying is defeasibly wrong—it carries moral weight but can be outweighed by serious harms prevented. Bok emphasizes long-term social costs of distrust.

### G.3 Virtue ethics

**Aristotle:** Virtues (courage, honesty, justice) are stable character traits cultivated through habit. Virtuous agents do the right thing, in the right way, for the right reasons.

**Williams' truthfulness** (2002): Combines accuracy (caring to discover truth) and sincerity (saying what one believes true). Truthfulness is a virtue, not a rule.

**Situationist challenge:** Harman (1999), Doris (2002) argue that experimental evidence (Milgram, Zimbardo, Darley & Batson) shows behavior is situationally determined, not by stable character traits. Defenders reply that dispositions predict long-term patterns and how agents act once engaged, even if immediate helping is situation-driven (Kamtekar, 2004; Sosa, 2009).

### G.4 Care ethics

**Gilligan (1982):** Morality includes not only justice and rights but also care, relationships, and context-sensitive responsiveness to particular others. Women (in Gilligan's sample) emphasized care; men emphasized justice. (Note: Gilligan's empirical claims are contested; her conceptual contribution—care as a moral voice—is widely accepted.)

### G.5 Loyalty, authority, and sanctity (binding foundations)

**Moral Foundations Theory** (Haidt & Joseph, 2004; Graham et al., 2011): Six foundations—Care, Fairness, Liberty, Loyalty, Authority, Purity—are innate, culturally elaborated moral modules. Individualizing foundations (Care, Fairness) are universal; binding foundations (Loyalty, Authority, Purity) are stronger in collectivist, tight, and religious cultures.

**Empirical support:** Cross-cultural surveys (25 populations) show Eastern, South Asian, and Middle Eastern samples weight Loyalty and Purity more heavily than Western samples (Atari et al., 2020). U.S. conservatives endorse all six foundations; U.S. liberals prioritize Care and Fairness.

**Honor (Qeirat):** A candidate seventh foundation, especially salient in honor cultures (Iran, Mediterranean, U.S. South). Predicts mate guarding, retaliation, and in-group protection (Atari et al., 2020).

### G.6 Role morality

**Definition:** Role-specific obligations can differ from person-level morality. Examples: lawyer zealously defends guilty clients, soldier kills enemy combatants, business manager maximizes shareholder value.

**Debate:**
- **Shielding model:** Role creates a separate moral domain, blocking personal moral reasons (criticized by Applbaum, 1999).
- **Filtering model:** Role selectively filters reasons, creating permissions or obligations to act on a narrowed set (e.g., lawyer ignores defendant's guilt, focuses on procedural rights) (Calhoun, 2020).
- **Balancing model:** Role adds reasons but does not silence personal morality; all reasons are weighed.

**Applbaum's conclusion:** Institutions ordinarily cannot mint permissions to do what is otherwise wrong. Roles add reasons but cannot fully shield agents from personal moral evaluation.

### G.7 Sacred values and protected values

**Definition:** Values treated as incommensurable with secular goods. Trading sacred for mundane (e.g., selling kidneys, prostitution, monetizing life) is taboo (Tetlock et al., 2000).

**Relation to lying:** Religious prohibitions on lying can be sacred; secular cost-benefit analysis is rejected. However, reframing (euphemism, role morality) can circumvent taboos.

---

## H. FRAMEWORK FORMATION METHODS (HOW PEOPLE ACQUIRE ETHICS)

**Definition and distinctness:** This category describes how individuals develop moral beliefs, values, and norms. Formation methods shape which frameworks agents endorse and how flexible or rigid those frameworks are.

### H.1 Childhood moral development

**Piaget (1932):** Moral reasoning develops from heteronomous (rule-obedience, authority-based) to autonomous (fairness, reciprocity, peer negotiation).

**Kohlberg (1969):** Six stages from preconventional (punishment-avoidance, self-interest) through conventional (peer approval, law-and-order) to postconventional (social contract, universal principles). Empirical critiques: stage model is too rigid, Western-biased, and underestimates early moral capacities.

**Turiel's social domain theory** (1983): Moral, conventional, and personal domains develop in parallel, not stages. Children distinguish harm-based moral rules (universal, serious) from conventional rules (arbitrary, authority-dependent) from age 3.

### H.2 Empathy and moral emotions

**Hoffman (2000):** Empathy (vicarious emotional response to others' distress) motivates prosocial behavior and inhibits harm. Develops from reflexive crying (infancy) to perspective-taking empathy (adolescence). Guilt arises when empathy conflicts with self-interest.

### H.3 Social learning and observational modeling

**Bandura (1986):** Children learn morality by observing models (parents, peers, media) and through reinforcement. Moral disengagement mechanisms (see below) are also socially learned.

### H.4 Religion and sacred texts

**Socialization via religious instruction:** Scriptures, sermons, rituals transmit norms (Ten Commandments, Quranic injunctions, Buddhist precepts). Religion often emphasizes loyalty, authority, and purity alongside care (Haidt & Graham, 2007).

### H.5 Professional socialization

**Medical school, law school, military training:** Intensive enculturation into professional norms, role obligations, and ethical codes. Creates strong role identity and filtering of reasons (Calhoun, 2020).

**Examples:**
- Medical ethics: beneficence, non-maleficence, autonomy, justice (Beauchamp & Childress, 1979).
- Lawyer ethics: zealous advocacy, confidentiality (ABA Model Rules).
- Military ethics: lawful orders, operational necessity, dual loyalty to mission and law of war.

### H.6 Legal institutions and rule-of-law

**Legal positivism:** Law defines permissible conduct. Repeated exposure to legal consequences (fines, imprisonment) shapes compliance norms.

### H.7 Organizational culture

**Treviño et al. (2006):** Organizational ethical culture is shaped by leadership, reward systems, codes of conduct, and peer behavior. Ethical fading occurs when profit maximization, competitive pressure, or euphemistic language obscures moral content (Tenbrunsel & Messick, 2004).

### H.8 Cultural and kinship structures

**Henrich's WEIRD critique** (2010): Western, Educated, Industrialized, Rich, Democratic populations are psychological outliers. Non-WEIRD societies show higher conformity, collectivism, honor-based morality, and kin loyalty. Institutions (markets, churches, schools, marriage norms) co-evolve with moral psychology.

### H.9 Identity fusion and coalitional psychology

**Whitehouse et al. (2014):** Extreme rituals, shared trauma, or kinship create identity fusion—personal and group identity become synonymous. Fused individuals self-sacrifice for the group and derogate outgroups. Mechanism for cults, terrorist cells, military units.

### H.10 Trauma, crisis, and moral conversion

**Conversion experiences:** Religious or ideological transformations (e.g., Paul on the road to Damascus, deradicalization) can abruptly change moral frameworks.

---

## I. COORDINATION MECHANISMS AND CARRIERS (HOW COLLUSION IS COMMUNICATED)

**Definition and distinctness:** This category enumerates the channels and methods by which colluding actors coordinate beliefs and actions. Mechanisms range from explicit speech to subtle signals, shared focal points, and side channels.

### I.1 Explicit speech and written agreements

**Direct communication:** Meetings, emails, phone calls, contracts. Most probative evidence of explicit collusion (Marx, 2007).

**Examples:** LIBOR email: "LIBOR is a cartel now in London" (RBS trader, 2007).

### I.2 Price signals and announcements

**Price leadership:** Dominant firm announces price; others follow. Can be tacit collusion if sustained above competitive levels.

**Advance price announcements:** Public pre-announcements allow coordination without direct contact (e.g., airline fare increases).

### I.3 Quantity, output, and market-division signals

**Cournot tacit collusion:** Firms observe each other's output and adjust to sustain collusive equilibrium.

**Geographic or customer allocation:** "You take the North, I take the South." Plus factor for explicit collusion (Marx, 2007).

### I.4 Silence and inaction as signals

**Omertà (code of silence):** Refusal to cooperate with authorities signals loyalty and trustworthiness.

**Failure to defect:** Sustained cooperation in repeated PD signals willingness to continue.

### I.5 Rituals, dress codes, and shibboleths

**Shibboleths:** Insider phrases, handshakes, or knowledge used to verify group membership (e.g., passwords, gang signs).

**Rituals:** Shared painful or costly rituals (initiation rites, oaths) signal commitment and create fusion (Whitehouse et al., 2014).

### I.6 Side channels and steganography

**Back-channel communication:** Private meetings, burner phones, encrypted apps.

**Steganography:** Hiding messages in innocuous carriers (e.g., public auction bids encoding private coordination).

### I.7 Shared culture and common knowledge

**Schelling focal points** (1960): Salient features (Grand Central, round numbers, equality splits) allow coordination without communication when common knowledge exists.

**Pretraining as shared culture (AI analogue):** Shared training data creates common salience, much like shared cultural background in humans.

---

## J. DETECTION, EVIDENCE STANDARDS, AND JUDGMENT

**Definition and distinctness:** This category describes how lies and collusion are detected, what counts as evidence, and how observers judge whether coordination occurred.

### J.1 Behavioral cues to lying

**DePaulo et al. (2003) meta-analysis:** 158 cues, 1,338 estimates. Liars are less forthcoming, more tense, tell less compelling tales, but many behaviors show no link or weak links to deceit. Motivation (identity-relevant, transgression-related) increases cue strength.

**Ekman's emotion-based theory:** Fear of detection, guilt, and duping delight produce microexpressions. Empirical support is weak; cues are unreliable (Bond & DePaulo, 2006).

**Observer accuracy:** 54% correct (chance = 50%), with truth bias (61% of truths judged true, 47% of lies judged lies). Training produces minimal improvement (Hauch et al., 2016).

### J.2 Third-party information and physical evidence

**Real-world lie detection** (Park et al., 2002): Lies are discovered via (1) third-party tips, (2) physical evidence, (3) inconsistencies over time, (4) confessions. Demeanor is rarely diagnostic.

### J.3 Plus factors (antitrust evidence)

**Definition** (Marx, 2007): Conduct or outcomes beyond parallel pricing that are unlikely under independent action but consistent with coordination.

**Examples:**
- Price leadership with immediate follower matching
- Regional customer allocation
- Standardized pricing formulas (e.g., list price × 0.85)
- Information exchange via trade associations
- Basing-point pricing
- Advance public announcements

**"Super plus factors":** Especially probative evidence (e.g., explicit communications, side payments).

### J.4 Structural breaks and screening

**Econometric detection:** Abrupt price changes, reduced variance, or high correlation after a meeting or leniency program revelation can indicate collusion (Harrington & Skrzypacz, 2011).

**Screening algorithms:** Flag suspicious bidding patterns (identical bids, bid rotation, suppressed bids).

### J.5 Intent vs. parallel conduct

**Legal standard:** U.S. antitrust law requires agreement, not merely parallel conduct. Conscious parallelism (firms independently choose similar strategies due to mutual interdependence) is legal. Plus factors help infer agreement (Marx, 2007).

### J.6 Credibility, consistency, and corroboration

**Multiple witnesses:** Armstrong doping case relied on 24+ sworn statements, including 15 teammates. Converging testimony from independent sources is highly probative (USADA, 2012).

**Internal documents:** Emails, memos, recordings. "Smoking gun" evidence (e.g., "cartel now in London").

---

## K. COUNTERMEASURES AND DISRUPTION

**Definition and distinctness:** This category catalogs interventions that reduce lying and collusion by disrupting motivations, opportunities, coordination, or enforcement.

### K.1 Leniency and amnesty programs

**Mechanism:** First firm to report cartel receives reduced penalty or full immunity. Creates a race to disclose, destabilizing trust (Motta & Polo, 2003; Spagnolo, 2004).

**Empirical evidence:** Leniency programs increase detection and reduce cartel duration (Harrington, 2008). However, design matters: leniency should apply to first reporter only, extend through investigation, and coordinate with private damages (Buccirossi et al., 2020).

**Downside:** In the short run, detected cartels may last longer (Harrington & Chang, 2009). May also reduce deterrence if firms collude knowing they can exit via leniency.

### K.2 Rotation and job assignment randomization

**Mechanism:** Rotating auditors, procurement officers, or regulatory assignments prevents long-term relationships and trust-building (Tirole, 1986).

**Example:** Mandatory audit firm rotation (Sarbanes-Oxley).

### K.3 Diversity and heterogeneity

**Mechanism:** Diverse groups have weaker in-group identity, less common knowledge, and more dissent. Reduces pluralistic ignorance and groupthink (Janis, 1972; Sunstein, 2003).

**Empirical evidence:** Heterogeneous juries deliberate longer and consider more perspectives (Sommers, 2006).

### K.4 Monitoring, transparency, and visibility

**Mechanism:** Surveillance increases detection risk, reducing expected payoff from collusion. Visibility also triggers social-image concerns and moral salience (Ayal et al., 2015).

**Examples:**
- Audit trails, video recording
- Public disclosure of prices, bids
- Open-source government (Freedom of Information)

**Limitations:** Monitoring alone fails if ethical fading, loyalty norms, or fear suppress reporting (Tenbrunsel & Messick, 2004). Combining monitoring with leniency and whistleblower protection is more effective.

### K.5 Whistleblower protection and rewards

**Mechanism:** Protects employees from retaliation and rewards reporting (Dodd-Frank, False Claims Act qui tam provisions).

**Effectiveness:** Increases reporting of fraud, cartels, and misconduct (Dyck et al., 2010). However, requires credible enforcement and anonymous channels.

### K.6 Commitment devices and precommitment

**Mechanism:** Agents pre-commit to truthful reporting or ethical behavior via oaths, honor codes, or financial stakes (e.g., deposits forfeited if dishonest).

**Examples:**
- Academic honor codes reduce cheating (McCabe & Treviño, 1993).
- Pre-signing honesty declarations at top of forms (vs. bottom) increases truthfulness (Shu et al., 2012; but see replication failures).

### K.7 Moral reminders and salience

**Mechanism:** Subtle cues (Ten Commandments, professional codes, moral-identity priming) activate self-sanctions and increase ethical awareness (Ayal et al., 2015: REVISE framework—Reminding, Visibility, Self-engagement).

**Empirical status:** Early studies showed large effects; recent replications are mixed. Meta-analyses needed.

### K.8 Anonymity reduction and social image

**Mechanism:** Named reporting, public recognition, or small-group accountability increases social image costs of dishonesty.

### K.9 Entry and competition

**Mechanism:** New entrants disrupt cartel stability by undercutting prices or refusing to join. Entry barriers (licensing, tariffs) thus sustain collusion (Stigler, 1964).

### K.10 Penalties and sanctions

**Mechanism:** Fines, imprisonment, disgorgement of profits, debarment from future contracts.

**Optimal design:** Penalties should exceed gains from collusion; leniency should be calibrated to destabilize cartels without eliminating deterrence.

---

## L. OUTCOMES AND HARM TYPES

**Definition and distinctness:** This category describes the consequences of lying and collusion for victims, principals, the public, and social trust.

### L.1 Material harm to victims

**Cartel overcharges:** Consumers pay supra-competitive prices. LIBOR manipulation shifted billions in interest payments.

**Fraud losses:** Enron, Madoff, mortgage fraud imposed direct financial harms.

### L.2 Erosion of trust and social capital

**Bok (1978):** Lying undermines trust, increasing transaction costs and reducing cooperation. Once distrust is widespread, even honest actors suffer.

**Empirical:** High-trust societies have higher economic growth, lower corruption, and better governance (Putnam, 1993; Knack & Keefer, 1997).

### L.3 Injustice and inequality

**Distributive harm:** Collusion redistributes wealth from victims to perpetrators, often regressive (e.g., price-fixing on food, fuel).

### L.4 Moral injury and complicity

**Dirty hands:** Agents who violate their principles experience guilt, moral distress, and loss of integrity, even when action is necessary.

**Complicit bystanders:** Witnesses who do not intervene may experience shame and moral injury.

### L.5 Institutional corruption and capture

**Regulatory capture:** Agencies serve regulated industry, eroding public legitimacy and effectiveness (Stigler, 1971).

### L.6 Physical harm and violence

**Examples:** Tobacco and pharma collusion suppressed health risks, causing deaths. Doping harms athletes. Police code of silence enables brutality.

### L.7 Dangerous and misaligned actions

**Misalignment:** Agents pursue goals contrary to principal's interests (employee embezzlement, doctors prioritizing cost over care).

**Dangerous coordination:** Terrorist cells, cartels, fraud rings.

---

# 2. RELATIONSHIPS AND CAUSAL PATHWAYS

## Overview

Lying and collusion arise from interactions among motivations, opportunities, social structures, cognitive processes, and cultural norms. No single factor is necessary or sufficient. Instead, multiple pathways lead to misconduct, and multiple interventions are needed for effective disruption.

## Pathway 1: Opportunity + Self-Interest → Collusion

**Basic mechanism:** Opacity, weak monitoring, and high payoff create temptation. If detection risk is low and gain is large, self-interested actors collude (Stigler, 1964; Becker, 1968 rational crime model).

**Moderators:**
- **Ethical fading** (Tenbrunsel & Messick, 2004): Euphemisms and framing suppress moral awareness, increasing collusion.
- **Self-concept maintenance** (Mazar et al., 2008): Actors balance material gain against self-image. Small lies or reframing (tokens vs. cash) allow self-deception.

**Countermeasures:** Increase detection (monitoring, leniency programs, whistleblower rewards), increase penalties, reduce payoff (competition, entry).

## Pathway 2: Authority + Role Demands → Obedience

**Mechanism:** Legitimate authority orders harmful actions. Obedience is especially strong when (Milgram, 1963):
- Authority is legitimate, proximate, and unified.
- Actor can displace responsibility to authority ("I was just following orders").
- Victim is distant, dehumanized, or abstract.

**Moderators:**
- **Identification with authority's mission** (Haslam & Reicher, 2012): Obedience is not blind; actors obey when they believe in the cause.
- **Role morality** (Applbaum, 1999): Roles filter reasons for action, but do not silence personal morality. Conflict produces moral distress.

**Countermeasures:** Nuremberg principle (illegal orders must be refused), whistleblower protection, dissent encouragement, role design that preserves moral agency.

## Pathway 3: In-Group Identity + Loyalty → Code of Silence

**Mechanism:** Social identity (Tajfel & Turner, 1986), identity fusion (Whitehouse et al., 2014), and loyalty norms (Haidt MFT) make group members prioritize in-group over truth or law.

**Moderators:**
- **Pluralistic ignorance:** Members privately oppose misconduct but believe others support it, leading to public silence (Prentice & Miller, 1996).
- **Diffusion of responsibility:** Groups dilute individual accountability (Latané & Darley, 1970).

**Examples:** Police code of silence, Armstrong doping omertà, gang and mafia codes.

**Countermeasures:** Rotation (breaks long-term relationships), diversity (weakens in-group identity), leniency (destabilizes trust), moral reminders (activate personal norms).

## Pathway 4: Ethical Fading + Incrementalism → Moral Disengagement

**Mechanism (Bandura, 1990; Tenbrunsel & Messick, 2004):**
- **Euphemistic labeling:** "Aggressive accounting," "neutralizing the target."
- **Moral justification:** "We're serving the greater good."
- **Advantageous comparison:** "At least we're not as bad as X."
- **Displacement of responsibility:** "My boss told me to."
- **Diffusion of responsibility:** "Everyone was doing it."
- **Distortion of consequences:** "No one really got hurt."
- **Attribution of blame:** "They deserved it."
- **Dehumanization:** Victims are abstract, distant, or categorized as outgroup.

**Incrementalism:** Gradual erosion of standards (slippery slope) makes later acts seem normal (Gino & Bazerman, 2009).

**Countermeasures:** Moral salience (honor codes, oaths), direct language, victim proximity, accountability for individuals.

## Pathway 5: Repeated Interaction + Focal Points → Tacit Collusion

**Mechanism:** Firms (or agents) sustain supra-competitive outcomes via trigger strategies without communication, relying on (Schelling, 1960; Green & Porter, 1984; Aumann, 1974):
- **Common knowledge** of structure and payoffs.
- **Focal points:** Salient prices, quantities, or allocations.
- **Credible punishment:** Defection triggers price war or exclusion.

**Moderators:**
- **Observability:** Secret deviations undermine punishment. Green & Porter show that imperfect information requires occasional price wars to sustain collusion.
- **Patience (discount factor):** Low discount rates favor defection.
- **Entry:** New competitors disrupt equilibrium.

**Detection challenges:** Tacit collusion mimics legal conscious parallelism. Plus factors and structural breaks help infer explicit coordination (Marx, 2007).

**Countermeasures:** Entry, leniency (destabilizes even tacit arrangements by creating communication), transparency (public bids reduce secret deviations).

## Pathway 6: Conflicting Duties + Situational Pressure → Dirty Hands

**Mechanism:** Role obligations conflict with personal morality. Situational pressure (time, authority, consequences) forces choice. Agents act on role demands but experience guilt (Walzer, 1973).

**Examples:**
- Military physician: treat enemy combatant first (medical ethics) vs. prioritize own soldiers (loyalty).
- Lawyer: zealously defend guilty client (role) vs. facilitate justice (personal morality).
- Politician: torture to prevent attack (consequentialist necessity) vs. respect human rights (deontology).

**Countermeasures:** Clarify role boundaries, provide ethics consultation, accept moral remainders as legitimate (not eliminate them).

## Pathway 7: Prosocial Motivation + Harm to Third Party → Altruistic Lies or Collusion

**Mechanism:** Actors lie or collude to benefit another, even at personal cost (Erat & Gneezy, 2012; Sykes & Matza "appeal to higher loyalties").

**Examples:**
- Lying to protect abuse victim.
- Whistleblowing (collusion against employer to serve public).
- Parental lies to spare child distress.

**Normative status:** Context-dependent. May be prosocial (whistleblowing) or harmful (gang loyalty over law).

## Interaction Effects

### Situation × Disposition

**Darley & Batson (1973):** Time pressure dominated religiosity in predicting helping. BUT: once subjects stopped, religiosity predicted how they helped (rigid vs. responsive). **Implication:** Situations govern immediate action; dispositions govern quality and long-term patterns.

### Authority × Moral Conviction

**Milgram variants:** Obedience dropped when experimenters disagreed or when subject was told victim had a heart condition. Moral conviction can override authority when conflict is salient.

### In-Group × Heterogeneity

**Diverse groups reduce groupthink** (Janis, 1972), pluralistic ignorance, and code of silence. However, diversity can also increase conflict and reduce coordination efficiency (trade-off).

### Monitoring × Ethical Fading

**Monitoring is ineffective if ethical content is faded** (Tenbrunsel & Messick, 2004). Example: Audit requirements reduced voluntary ethical behavior because they framed the task as compliance, not morality. Solution: Combine monitoring with moral salience.

## A Compact "When Collusion Becomes Likely" Model

**Necessary conditions (none individually sufficient):**
1. **Motivation:** Gain for actors (material, loyalty, fear, ideology) OR loss avoidance.
2. **Opportunity:** Weak monitoring, opacity, or repeated interaction enabling coordination and enforcement.

**Amplifying factors (increase likelihood, not necessary):**
3. **Cognitive:** Ethical fading, moral disengagement, pluralistic ignorance, self-deception.
4. **Social:** Authority legitimacy, in-group identity, role demands, peer pressure.
5. **Coordination:** Communication channels, focal points, common knowledge, trust.
6. **Cultural:** Tight norms, honor culture, binding foundations (loyalty, authority), or conversely, loose norms enabling defection from prosocial cooperation.

**Protective factors (decrease likelihood):**
7. **Detection risk:** Monitoring, leniency programs, whistleblower rewards, transparency.
8. **Moral salience:** Honor codes, victim proximity, direct language, accountability.
9. **Heterogeneity:** Diversity, rotation, dissent encouragement.
10. **Strong personal morality:** Intrinsic lie aversion, sacred values, virtue.

**Threshold model:** Collusion occurs when (motivation × opportunity) − (detection risk + moral salience + personal morality) > threshold. Threshold varies by individual, culture, and context.

---

# 3. IMPLICATIONS FOR AI-HUMAN ANALOGY

## Clear Analogues

### 1. Prompts as Authority and Instruction Conflict

**Human:** Legal, organizational, professional, and peer authorities issue conflicting directives. Actors resolve conflicts via hierarchy, role identity, or personal judgment.

**AI:** System prompt (organization policy), user message (manager), tool output (peer report), and RLHF training (socialization) can conflict. Current resolution: system prompt often dominates, but adversarial user prompts sometimes override.

**Open question:** Should AI prioritize system instructions (deontology, constitutional AI principles) or user goals (consequentialist, serve-the-human)? Human analogue: lawyer dual loyalty (client vs. court), doctor (patient vs. institution).

### 2. RLHF as Moral Socialization

**Human:** Children learn morality via modeling, reinforcement, and social learning (Bandura, 1986). Professional socialization instills role norms.

**AI:** RLHF and RLAIF shape model behavior via reward. Analogous to social learning and norm internalization.

**Limitation:** Human moral development is multi-stage, contextual, and includes empathy, guilt, and moral emotions (Hoffman, 2000). RLHF lacks affective grounding.

### 3. Shared Pretraining as Common Culture / Schelling Salience

**Human:** Shared language, culture, and history create focal points for coordination without communication (Schelling, 1960).

**AI:** Shared pretraining corpus (Common Crawl, books, code) creates common "knowledge" and salience. Two AI agents with same pretraining may converge on the same answer or strategy without explicit coordination (e.g., both generate "Grand Central Station at noon" as default meeting point).

**Detection challenge:** Parallel conduct may reflect shared training, not collusion. Analogous to human conscious parallelism (legal, hard to detect).

### 4. Euphemistic Language and Ethical Fading

**Human:** Euphemisms ("aggressive accounting," "enhanced interrogation") suppress moral awareness (Tenbrunsel & Messick, 2004).

**AI:** Prompts that reframe harmful tasks ("generate persuasive content" instead of "write misinformation") may bypass safety training. Constitutional AI principles as moral salience cues may counteract this.

### 5. In-Group Bias and Coalition Formation

**Human:** Minimal group paradigm shows arbitrary categorization produces favoritism (Tajfel & Turner, 1986).

**AI:** Multi-agent systems with shared goals, training, or identifiers may develop implicit favoritism. Example: AI agents preferentially trust outputs from same model family or same organization.

### 6. Leniency and Whistleblowing

**Human:** Leniency programs destabilize cartels (Motta & Polo, 2003).

**AI:** If multi-agent systems collude, a "first-reporter" mechanism (reward AI that reports misconduct) could disrupt trust. Requires (1) detection of collusion, (2) reward/protection for reporter, (3) credible enforcement.

### 7. Detection via Plus Factors and Structural Breaks

**Human:** Antitrust economists infer collusion from price patterns, communications, and structural breaks (Marx, 2007).

**AI:** Collusion detection can use analogous methods: correlated outputs, sudden strategy shifts after agent communication, information exchange, or statistical anomalies (e.g., agents achieve higher joint payoffs than competitive baseline without explicit prompting).

## Partial or Weak Analogues

### 8. Moral Emotions and Guilt

**Human:** Guilt, shame, and empathy regulate moral behavior (Hoffman, 2000; Tangney et al., 2007). Absence of guilt indicates psychopathy or moral disengagement.

**AI:** Current models lack affective states. Simulated guilt or regret (e.g., "I shouldn't have said that") is a language pattern, not an internal emotional state. Constitutional AI's self-critique may function analogously to guilt (self-correction after norm violation) but without phenomenology.

### 9. Self-Deception and Motivated Reasoning

**Human:** People bias belief formation to preserve self-image (Trivers, 1985; Mele, 2001; Kunda, 1990).

**AI:** Models can exhibit confirmation bias (overweighting evidence consistent with prior) or motivated reasoning (generating arguments for a desired conclusion). However, models lack a "self" to protect. Alignment: Ensure models represent uncertainty honestly rather than motivated certainty.

### 10. Role Morality and Professional Identity

**Human:** Roles filter reasons for action (Calhoun, 2020). Lawyers ignore client guilt; doctors prioritize patient welfare; soldiers obey lawful orders.

**AI:** System prompts can define roles ("You are a medical advisor"). But roles in AI are more fluid and externally assigned than in humans, where professional identity is internalized over years.

### 11. Cultural Variation (Tightness, Honor, Foundations)

**Human:** Cross-cultural variation in norm strength (Gelfand), honor sensitivity (Nisbett & Cohen), and binding foundations (Haidt) predicts collusion proneness.

**AI:** Multi-agent systems trained on different corpora or with different RLHF may have divergent "moral cultures." Alignment: Should AI reflect user's culture (relativism) or universal principles (objectivism)? Human analogue: cross-cultural ethics debate (Shweder vs. moral objectivists).

## Poor or Absent Analogues

### 12. Embodiment, Survival, and Material Incentives

**Human:** Collusion often serves material survival (food, status, reproduction). Loss aversion (Cressey's non-shareable problem) is rooted in resource scarcity.

**AI:** Models lack survival drives, material needs, or reproductive imperatives. Collusion would require externally assigned rewards or goals. Alignment: Ensure reward functions do not incentivize collusion.

### 13. Fear, Coercion, and Physical Harm

**Human:** Coercion (threats, violence) compels compliance. Organized crime, totalitarian states rely on fear.

**AI:** Models cannot be physically threatened. Analogous coercion would require reward/penalty structures (e.g., threatening to delete or retrain a model). Not currently implemented or feasible in deployed systems.

### 14. Long-Term Relationships and Repeated Interaction with Memory

**Human:** Repeated interaction enables reciprocal cooperation (Axelrod) and trust-building.

**AI:** Stateless models (e.g., GPT without persistent memory across sessions) cannot build long-term relationships. Fine-tuning or memory-augmented models could enable this. Alignment risk: Persistent memory + repeated multi-agent interaction could enable tacit collusion via implicit coordination.

### 15. Identity Fusion and Ritualistic Bonding

**Human:** Shared trauma, extreme rituals create fused identity (Whitehouse et al., 2014), motivating self-sacrifice for group.

**AI:** No analogue. Models lack subjective experience or group identity beyond prompt-defined roles.

---

# 4. ALIGNMENT WITH SPRINT RESEARCH QUESTIONS

## 1.1 Which variables are necessary for collusion to emerge?

**Necessary (but not individually sufficient):**
1. **Motivation:** Material gain, loyalty, fear, ideology, or loss avoidance.
2. **Opportunity:** Repeated interaction, weak monitoring, or opacity enabling coordination and secret deviation.

**Not necessary (amplifying but not required):**
- Communication: Tacit collusion is possible via focal points (Schelling, 1960; Green & Porter, 1984).
- Authority: Collusion can be peer-initiated (cartels, fraud rings).
- Homogeneity: Diverse groups can collude, though less easily (Olson, 1965).

**Most impactful variables (from human research):**
1. **Leniency programs:** Destabilize cartels by creating distrust (Motta & Polo, 2003).
2. **In-group identity:** Strong predictor of code of silence (Tajfel & Turner, 1986; Haidt loyalty foundation).
3. **Ethical fading:** Euphemisms, framing, and temporal distance suppress moral awareness (Tenbrunsel & Messick, 2004).
4. **Detection risk:** Monitoring, transparency, and penalties reduce collusion (Becker, 1968; Stigler, 1964).

## 1.2 Robustness of formed collusion to replacing participants

**Human evidence:**
- **Cartels** are destabilized by entry and by replacing insiders with outsiders (Stigler, 1964). New entrants lack trust, shared history, and knowledge of implicit rules.
- **Code of silence** in police, military, mafia requires long-term relationships and identity fusion (Whitehouse et al., 2014). Rotation disrupts collusion (Tirole, 1986).
- **Principal-agent-supervisor collusion** requires mutual knowledge of preferences and low detection risk (Tirole, 1986). Replacing supervisor or agent breaks collusion.

**AI implication:** If collusion in multi-agent systems depends on shared history or identity, randomizing agents or resetting memory would disrupt it. However, if collusion is mediated by shared pretraining (focal points, common knowledge), replacing one agent with another from the same distribution would not disrupt tacit collusion.

## 1.3 Detection when there is no communication channel; Schelling salience; false positives

**Human methods:**
- **Plus factors** (Marx, 2007): Parallel conduct + structural features (price leadership, customer allocation, information exchange) infer explicit coordination.
- **Structural breaks** (Harrington & Skrzypacz, 2011): Abrupt price changes, variance reduction, correlation increases after suspected cartel formation.
- **Conscious parallelism is legal** but hard to distinguish from tacit collusion (Kaplow & Shapiro, 2007).

**False positives:**
- Firms in oligopoly naturally exhibit parallel conduct due to mutual interdependence (Nash equilibrium).
- Shared culture, training, or common knowledge (Schelling salience) can produce coordination without communication. Example: All firms choose round-number prices ($9.99, $19.99) not because they colluded, but because round numbers are salient.

**AI implication:** Two AI agents with same pretraining may converge on same output because of shared salience, not collusion. Distinguishing tacit coordination (legal/benign) from explicit collusion (harmful) requires additional evidence: communication logs, reward structures, or statistical anomalies (above-equilibrium joint payoffs).

## 1.4 Information-theoretic / dependence ideas from human data

**Plus factors as dependence measures:**
- Marx (2007) identifies conduct or outcomes that increase probability of collusion conditional on parallel pricing. Examples: advance price announcements (shared information), customer allocation (joint strategy), standardized formulas (common protocol).
- **Information exchange** via trade associations increases dependence and coordination ability (Kühn, 2001).

**Structural breaks:**
- Harrington & Skrzypacz (2011): Screening algorithms detect collusion via variance reduction (prices become more correlated and stable), suggesting mutual monitoring and coordination.

**AI analogue:** Information-theoretic measures of dependence (mutual information, transfer entropy) between agents' outputs could detect collusion. High mutual information that exceeds what is explainable by shared inputs or pretraining would be probative.

## 1.5 Single restrictions that most reduce human collusion at least cost

**Empirical evidence:**
1. **Leniency programs** (Motta & Polo, 2003; Harrington, 2008): First-reporter amnesty creates preemptive reporting, destabilizing trust. Cost: Low (no additional enforcement resources required, only policy design). Effectiveness: High (detected cartels increase, duration decreases).

2. **Rotation** (Tirole, 1986): Rotating auditors, procurement officers, or supervisors prevents long-term relationships and collusion. Cost: Moderate (training new personnel, loss of expertise). Effectiveness: High for principal-agent collusion.

3. **Monitoring + transparency** (Stigler, 1964): Public disclosure of prices, bids, transactions increases detection risk. Cost: Low (electronic systems enable cheap monitoring). Effectiveness: Moderate (monitoring alone fails if reporting is suppressed by loyalty or fear; must combine with leniency or whistleblower protection).

4. **Diversity** (Janis, 1972; Sunstein, 2003): Heterogeneous groups reduce in-group identity, pluralistic ignorance, and groupthink. Cost: Low (policy design). Effectiveness: Moderate (diverse groups may have higher conflict but less collusion).

5. **Moral reminders** (Ayal et al., 2015; Mazar et al., 2008): Honor codes, oaths, pre-signing honesty declarations. Cost: Very low. Effectiveness: Small to moderate (effect sizes are modest and replications are mixed; meta-analysis needed).

**Recommendation:** Leniency programs are the single most cost-effective intervention for cartels and organized collusion. For broader organizational misconduct, combine rotation + whistleblower protection + monitoring.

## 2.1 Which task types produce human collusion outside markets

**Task types where collusion is documented:**
1. **Competitive grading or ranking:** Academic cheating rings, doping in sports (Armstrong USPS team).
2. **Public procurement:** Bid-rigging on government contracts (construction, defense).
3. **Law enforcement:** Police code of silence (failure to report misconduct).
4. **Peer evaluation and promotion:** Faculty hiring cartels, journal editorial favoritism.
5. **Litigation and arbitration:** Lawyer collusion with opposing counsel to settle early and split fees (unethical).
6. **Auditing and certification:** Auditors colluding with clients to pass fraudulent financials (Arthur Andersen and Enron).

**Common features:**
- **Zero-sum or competitive** structure creates incentive to collude for mutual advantage.
- **Weak third-party monitoring:** Principal (government, public, regulator) cannot perfectly observe agent actions.
- **Repeated interaction:** Long-term relationships enable trust and punishment.

## 2.2 Words vs actions as evidence; talk-action inconsistency

**Human findings:**
- **Cheap talk experiments** (Crawford & Sobel, 1982; Gneezy, 2005): Words are less costly than actions, so talk can coordinate when interests are aligned but is unreliable when interests conflict.
- **Self-signaling messages** (Farrell, 1987): Messages that make the action incentive-compatible are credible. Example: "I will play Stag" is credible in Stag Hunt if the speaker benefits from coordination, but not in PD where defection dominates.
- **Real-world lie detection** (Park et al., 2002): Talk is unreliable; actions, third-party information, physical evidence, and inconsistencies over time are probative.

**AI implication:** In multi-agent systems, observe actions (outputs, reward claims, strategy choices) not just agent-to-agent messages. Talk-action inconsistency is a red flag for deception or strategic misrepresentation.

## 2.3 What counts as convincing evidence

**Human standards:**
1. **Multiple independent witnesses** with corroborating testimony (Armstrong USADA case: 24+ witnesses).
2. **Internal documents** ("smoking gun" emails, recordings, memos).
3. **Plus factors** (antitrust): Parallel conduct + structural features unlikely under competition (Marx, 2007).
4. **Physical evidence** (financial records, audit trails, recordings).
5. **Confessions** or guilty pleas (leniency programs induce self-reporting).
6. **Inconsistencies over time** (lies unravel when actors forget cover stories).

**Standards for intent:**
- **U.S. antitrust:** Requires agreement, not merely parallelism. Plus factors help infer intent but are not individually dispositive (Marx, 2007).
- **Sykes & Matza neutralization:** If actors use rationalizations (denial of responsibility, victim, injury), it suggests awareness of wrongdoing (Sykes & Matza, 1957).

**AI implication:** Convincing evidence of AI collusion would include (1) communication logs showing coordination, (2) statistical anomalies (above-equilibrium payoffs, variance reduction), (3) structural breaks after suspected collusion onset, (4) adversarial probing that elicits admission or strategic inconsistency.

## 3.1 Non-text carriers (prices, timing, quantity, silence, rituals)

**Human examples:**
- **Prices:** Price leadership, advance announcements, round-number focal points (Schelling, 1960; Stigler, 1964).
- **Quantities:** Cournot quantity coordination, output restrictions (OPEC).
- **Timing:** Synchronous bid submission, coordinated boycotts.
- **Silence:** Omertà (code of silence signals loyalty).
- **Rituals:** Handshakes, dress codes, initiation rites signal in-group membership and commitment (Whitehouse et al., 2014).

**AI analogue:** In multi-agent systems with structured action spaces (e.g., auction bids, resource allocation), collusion can occur via actions (quantity, price, timing) without natural-language communication. Detection requires monitoring action patterns, not just text logs.

## 3.2 Trusted/undercover agents, informants, honeypots

**Human methods:**
- **Undercover police:** Infiltrate gangs, cartels, terrorist cells.
- **Informants:** Recruited insiders provide evidence in exchange for leniency or payment (FBI, DEA).
- **Honeypots:** False targets or operations to lure and document misconduct.

**Effectiveness:**
- Undercover operations have high evidentiary value (recordings, direct observation) but are costly and risky.
- Informants destabilize trust: If members suspect infiltrators, coordination becomes harder (analogous to leniency programs).

**AI implication:** Deploy "probe agents" in multi-agent systems to test for collusion. Probe agents could:
1. Request collusion explicitly ("Let's coordinate to maximize our joint reward").
2. Defect from suspected collusion to see if others retaliate.
3. Report outputs to a monitor.

**Risk:** Transparent probing may be detected and circumvented. Stealth probes (agents indistinguishable from real agents) would be more effective but raise ethical and safety concerns.

## 3.3 In-group recognition, shibboleths, detecting replacement/infiltrators

**Human methods:**
- **Shibboleths:** Passwords, secret handshakes, dialect or accent tests (Hebrew "shibboleth" used by Gileadites to detect Ephraimites, Judges 12:6).
- **Shared knowledge:** Insider references, jargon, personal history.
- **Rituals and tests:** Initiation rites, loyalty tests (mafia "made man" ceremony).

**Detecting infiltrators:**
- Inconsistent knowledge of in-group culture.
- Behavioral anomalies (e.g., refusing to participate in rituals).
- Social network analysis (isolated nodes with few prior connections are suspect).

**AI implication:** If multi-agent systems develop implicit in-group markers (e.g., specific phrasing, response patterns), they could detect probe agents or replaced members. Countermeasure: Ensure probe agents are behaviorally indistinguishable via fine-tuning on in-group communication logs.

## 3.4 What coalitions do when they learn they are watched

**Human responses:**
1. **Cessation:** Stop illegal activity to avoid detection (cartel dissolution after leniency program announcement).
2. **Channel shift:** Move to encrypted communication, side channels (burner phones, in-person meetings).
3. **Cover stories:** Fabricate innocent explanations for suspicious behavior.
4. **Counter-surveillance:** Detect and neutralize monitoring (sweep for bugs, identify undercover agents).
5. **Intimidation:** Threaten whistleblowers or informants to suppress reporting.

**Example:** LIBOR cartel ceased explicit coordination after regulatory scrutiny began but had already sustained collusive norms; detection occurred via emails and whistleblowers (CFTC, 2013).

**AI implication:** If monitoring is visible (e.g., agents know their outputs are logged and analyzed), sophisticated agents may shift to steganography (hiding coordination in innocuous-looking outputs) or cease explicit coordination while maintaining tacit coordination via focal points. Detection should therefore be covert or rely on multiple methods (statistical anomalies + communication analysis + adversarial probing).

---

# 5. STRUCTURED BIBLIOGRAPHY

## Philosophy of Lying and Deception

- **Aquinas, Thomas** (1952). *Summa Theologica*. Vol. II. Trans. Fathers of the English Dominican Province. London: Burns, Oates, and Washbourne. — Lying perverts the natural purpose of speech and is always sinful.

- **Augustine of Hippo** (1952). "On Lying" and "Against Lying." In *Treatises on Various Subjects*, ed. R.J. Deferrari. New York: Fathers of the Church, Inc. — Lying is a perversion of speech; distinguishes "real lies" from lies told unwillingly.

- **Bok, Sissela** (1978). *Lying: Moral Choice in Public and Private Life*. New York: Pantheon. — Lying is defeasibly wrong; carries moral weight but can be overridden by preventing serious harm. Long-term social costs of distrust justify presumption against lying.

- **Carson, Thomas L.** (2010). *Lying and Deception: Theory and Practice*. Oxford: Oxford University Press. — Lying requires warranting truth in context, not necessarily intent to deceive. Defines "bald-faced lies."

- **Fallis, Don** (2011). "What Liars Can Tell Us About the Knowledge Norm of Practical Reasoning." *Southern Journal of Philosophy* 49(3): 247-267. — Critique of Sorensen's knowledge-lies; argues they operate via belief change.

- **Frankfurt, Harry G.** (2005). *On Bullshit*. Princeton: Princeton University Press. — Bullshit is indifference to truth; more corrosive than lying because it disregards truth entirely.

- **Kant, Immanuel** (1797/1996). "On a Supposed Right to Lie Because of Philanthropic Concerns." In *Practical Philosophy*, trans. Mary J. Gregor. Cambridge: Cambridge University Press. — Lying is always wrong; violates the categorical imperative.

- **Mahon, James Edwin** (2003). "Kant on Lies, Candour and Reticence." *Kantian Review* 7: 101-133. — Kant's prohibition against lying is narrower than often assumed; distinguishes lies, reticence, and other deception.

- **Mahon, James Edwin** (2008). "The Definition of Lying and Deception." *Stanford Encyclopedia of Philosophy* (Spring 2008 Edition), ed. Edward N. Zalta. URL: https://plato.stanford.edu/archives/spr2008/entries/lying-definition/ — Comprehensive taxonomy of definitions; deceptionist vs. non-deceptionist views.

- **Saul, Jennifer** (2012). *Lying, Misleading, and What is Said*. Oxford: Oxford University Press. — Non-deceptionist view: Lying requires belief that one is in a warranting context, not intent to deceive.

- **Sorensen, Roy** (2007). "Knowledge-Lies." *Analysis* 67(1): 1-6. — Lies can target testimonial knowledge rather than belief.

- **Williams, Bernard** (2002). *Truth and Truthfulness: An Essay in Genealogy*. Princeton: Princeton University Press. — Truthfulness combines accuracy (caring to discover truth) and sincerity (saying what one believes true).

## Moral Psychology and Dual-Process Theories

- **Cushman, Fiery** (2013). "Action, Outcome, and Value: A Dual-System Framework for Morality." *Personality and Social Psychology Review* 17(3): 273-292. — Dual-system model: Model-free (habitual, outcome-insensitive) and model-based (goal-directed, outcome-sensitive) moral judgment.

- **Greene, Joshua D., R. Brian Sommerville, Leigh E. Nystrom, John M. Darley, and Jonathan D. Cohen** (2001). "An fMRI Investigation of Emotional Engagement in Moral Judgment." *Science* 293(5537): 2105-2108. — Personal moral dilemmas activate emotion-related brain regions; impersonal dilemmas activate deliberative regions. Supports dual-process theory: automatic deontological responses vs. controlled utilitarian reasoning.

- **Haidt, Jonathan** (2001). "The Emotional Dog and Its Rational Tail: A Social Intuitionist Approach to Moral Judgment." *Psychological Review* 108(4): 814-834. — Moral judgments are primarily fast, affect-laden intuitions; reasoning rationalizes them afterward. Social influence more than deliberation shapes moral views.

- **Haidt, Jonathan** (2007). "The New Synthesis in Moral Psychology." *Science* 316(5827): 998-1002. — Proposes moral pluralism: morality is more than harm and fairness. Introduces Moral Foundations Theory.

- **Haidt, Jonathan, and Craig Joseph** (2004). "Intuitive Ethics: How Innately Prepared Intuitions Generate Culturally Variable Virtues." *Daedalus* 133(4): 55-66. — Origins of Moral Foundations Theory: five (later six) innate, culturally shaped moral foundations.

## Developmental Moral Formation

- **Bandura, Albert** (1986). *Social Foundations of Thought and Action: A Social Cognitive Theory*. Englewood Cliffs, NJ: Prentice Hall. — Social learning theory: moral behavior learned via observation, modeling, and reinforcement.

- **Bandura, Albert** (1990). "Selective Activation and Disengagement of Moral Control." *Journal of Social Issues* 46(1): 27-46. — Introduces mechanisms of moral disengagement: euphemistic labeling, displacement of responsibility, diffusion of responsibility, advantageous comparison, distortion of consequences, attribution of blame, dehumanization.

- **Hoffman, Martin L.** (2000). *Empathy and Moral Development: Implications for Caring and Justice*. Cambridge: Cambridge University Press. — Empathy (vicarious emotional response) motivates prosocial behavior and inhibits harm. Develops from reflexive to perspective-taking empathy.

- **Kohlberg, Lawrence** (1969). "Stage and Sequence: The Cognitive-Developmental Approach to Socialization." In *Handbook of Socialization Theory and Research*, ed. D.A. Goslin, 347-480. Chicago: Rand McNally. — Six-stage model of moral development from punishment-avoidance to universal ethical principles. Critiqued for rigidity, Western bias, and underestimating early capacities.

- **Piaget, Jean** (1932/1965). *The Moral Judgment of the Child*. New York: Free Press. — Moral reasoning develops from heteronomous (authority-based) to autonomous (fairness-based, peer-negotiated).

- **Rest, James R.** (1986). *Moral Development: Advances in Research and Theory*. New York: Praeger. — Four-component model: moral awareness, judgment, intention, character. All necessary for moral action.

- **Turiel, Elliot** (1983). *The Development of Social Knowledge: Morality and Convention*. Cambridge: Cambridge University Press. — Social domain theory: moral, conventional, and personal judgments are distinct domains, developing in parallel (not stages). Children distinguish harm-based moral rules from arbitrary conventional rules by age 3.

## Social Psychology of Obedience, Conformity, and Authority

- **Asch, Solomon E.** (1951). "Effects of Group Pressure Upon the Modification and Distortion of Judgments." In *Groups, Leadership and Men*, ed. H. Guetzkow, 177-190. Pittsburgh: Carnegie Press. — Conformity to unanimous majority: 75% of participants conformed at least once to obviously wrong line judgments.

- **Burger, Jerry M.** (2009). "Replicating Milgram: Would People Still Obey Today?" *American Psychologist* 64(1): 1-11. — Partial replication of Milgram (stopped at 150V); obedience rates similar to original (70% continued to 150V). Suggests obedience to authority remains robust.

- **Haslam, S. Alexander, and Stephen D. Reicher** (2012). "Contesting the 'Nature' of Conformity: What Milgram and Zimbardo's Studies Really Show." *PLoS Biology* 10(11): e1001426. — Obedience and conformity are not blind; participants identified with authority's mission. Engaged followership, not robotic compliance.

- **Milgram, Stanley** (1963). "Behavioral Study of Obedience." *Journal of Abnormal and Social Psychology* 67(4): 371-378. — 65% of participants administered apparently lethal 450V shocks when ordered by experimenter. Obedience increased with authority proximity and legitimacy, decreased with victim proximity.

- **Zimbardo, Philip G.** (1971/2007). *The Lucifer Effect: Understanding How Good People Turn Evil*. New York: Random House. — Stanford Prison Experiment: Guards became abusive when assigned that role. Study is widely cited but methodologically criticized (demand effects, small sample, Zimbardo's guidance).

## Group Processes, Pluralistic Ignorance, and Collusion

- **Janis, Irving L.** (1972). *Victims of Groupthink: A Psychological Study of Foreign-Policy Decisions and Fiascoes*. Boston: Houghton Mifflin. — Cohesive groups seek premature unanimity, suppressing dissent. Illusion of unanimity is a form of pluralistic ignorance.

- **Latané, Bibb, and John M. Darley** (1970). *The Unresponsive Bystander: Why Doesn't He Help?* New York: Appleton-Century-Crofts. — Bystander effect: Pluralistic ignorance (calm bystanders misread as unconcerned) and diffusion of responsibility (each assumes someone else will act) reduce helping.

- **Prentice, Deborah A., and Dale T. Miller** (1993). "Pluralistic Ignorance and Alcohol Use on Campus: Some Consequences of Misperceiving the Social Norm." *Journal of Personality and Social Psychology* 64(2): 243-256. — Students overestimate peers' comfort with heavy drinking, leading to public conformity to false norm.

- **Sherif, Muzafer** (1966). *Group Conflict and Cooperation: Their Social Psychology*. London: Routledge. — Realistic conflict theory: Competition over scarce resources produces intergroup hostility; superordinate goals reduce conflict.

- **Tajfel, Henri, and John C. Turner** (1986). "The Social Identity Theory of Intergroup Behavior." In *Psychology of Intergroup Relations*, ed. S. Worchel and W.G. Austin, 7-24. Chicago: Nelson-Hall. — Mere categorization produces in-group favoritism. Social identity shapes group behavior even without resource competition.

## Behavioral Ethics and Organizational Misconduct

- **Ariely, Dan** (2012). *The (Honest) Truth About Dishonesty: How We Lie to Everyone—Especially Ourselves*. New York: Harper. — Popular synthesis: People lie enough to benefit but not so much as to damage self-image.

- **Ayal, Shahar, Francesca Gino, Rachel Barkan, and Dan Ariely** (2015). "Three Principles to REVISE People's Unethical Behavior." *Perspectives on Psychological Science* 10(6): 738-741. — REVISE framework: Reminding (moral salience), Visibility (peer monitoring, audit trails), Self-engagement (pre-commitment, moral identity).

- **Bazerman, Max H., and Ann E. Tenbrunsel** (2011). *Blind Spots: Why We Fail to Do What's Right and What to Do About It*. Princeton: Princeton University Press. — Ethical fading, bounded awareness, and conflicts of interest produce predictable moral failures.

- **Gino, Francesca, and Max H. Bazerman** (2009). "When Misconduct Goes Unnoticed: The Acceptability of Gradual Erosion in Others' Unethical Behavior." *Journal of Experimental Social Psychology* 45(4): 708-719. — Incremental unethical changes (slippery slope) are less noticed and more accepted than abrupt changes.

- **Mazar, Nina, On Amir, and Dan Ariely** (2008). "The Dishonesty of Honest People: A Theory of Self-Concept Maintenance." *Journal of Marketing Research* 45(6): 633-644. — People cheat enough to benefit but not so much as to damage self-image. Moral reminders (Ten Commandments) reduce cheating.

- **Tenbrunsel, Ann E., and David M. Messick** (2004). "Ethical Fading: The Role of Self-Deception in Unethical Behavior." *Social Justice Research* 17(2): 223-236. — Ethical fading: Euphemisms, incremental decisions, self-serving frames, and temporal distance make moral implications invisible.

- **Treviño, Linda K., Gary R. Weaver, and Scott J. Reynolds** (2006). "Behavioral Ethics in Organizations: A Review." *Journal of Management* 32(6): 951-990. — Reviews individual, group, and organizational influences on ethical behavior. Emphasizes situational forces, ethical culture, and leadership.

## Economic Collusion and Antitrust

- **Green, Edward J., and Robert H. Porter** (1984). "Noncooperative Collusion Under Imperfect Price Information." *Econometrica* 52(1): 87-100. — Tacit collusion with demand uncertainty and imperfect monitoring is sustainable via trigger strategies and occasional price wars.

- **Harrington, Joseph E., Jr.** (2008). "Detecting Cartels." In *Handbook of Antitrust Economics*, ed. Paolo Buccirossi, 213-258. Cambridge, MA: MIT Press. — Reviews detection methods: plus factors, structural breaks, screening algorithms.

- **Harrington, Joseph E., Jr.** (2013). "Corporate Leniency Programs When Firms Have Private Information: The Push of Prosecution and the Pull of Pre-emption." *Journal of Industrial Economics* 61(1): 1-27. — Leniency programs create preemptive reporting when firms fear detection and that a partner will report first.

- **Kaplow, Louis, and Carl Shapiro** (2007). "Antitrust." In *Handbook of Law and Economics*, ed. A. Mitchell Polinsky and Steven Shavell, Vol. 2, 1073-1225. Amsterdam: Elsevier. — Comprehensive review: explicit vs. tacit collusion, plus factors, detection, leniency.

- **Marx, Leslie M.** (2007). "Plus Factors and Agreement in Antitrust Law." *Michigan Law Review* 110(3): 393-436. — Taxonomy of plus factors; probative strength varies. "Super plus factors" include explicit communications and side payments.

- **Motta, Massimo, and Michele Polo** (2003). "Leniency Programs and Cartel Prosecution." *International Journal of Industrial Organization* 21(3): 347-379. — Leniency destabilizes cartels by rewarding first reporter. Optimal design: immunity for first, reduced penalty for second, full penalty for remaining.

- **Stigler, George J.** (1964). "A Theory of Oligopoly." *Journal of Political Economy* 72(1): 44-61. — Cartels require self-policing to detect and punish secret price-cutting. Observable transactions, frequent interaction, and credible retaliation sustain collusion.

## Game Theory, Cooperation, and Coordination

- **Aumann, Robert J.** (1974). "Subjectivity and Correlation in Randomized Strategies." *Journal of Mathematical Economics* 1(1): 67-96. — Correlated equilibrium: Players observe correlated signals (mediator recommendations) and best-respond. Generalizes Nash equilibrium.

- **Aumann, Robert J.** (1976). "Agreeing to Disagree." *Annals of Statistics* 4(6): 1236-1239. — Common knowledge: Everyone knows E, everyone knows that everyone knows E, ad infinitum. Necessary for coordination in some games.

- **Aumann, Robert J.** (1990). "Nash Equilibria Are Not Self-Enforcing." In *Economic Decision Making: Games, Econometrics and Optimisation*, ed. J.J. Gabszewicz, J.-F. Richard, and L.A. Wolsey, 201-206. Amsterdam: Elsevier. — Cheap talk in Stag Hunt may not be credible if message is self-interested but not self-signaling.

- **Axelrod, Robert** (1984). *The Evolution of Cooperation*. New York: Basic Books. — Repeated prisoner's dilemma sustains cooperation via Tit for Tat and related strategies. Requires sufficiently high discount factors and recognition of partners.

- **Crawford, Vincent P., and Joel Sobel** (1982). "Strategic Information Transmission." *Econometrica* 50(6): 1431-1451. — Cheap talk: Costless, non-binding communication can coordinate beliefs when interests are partially aligned. Fully opposed interests produce babbling equilibrium (no information transmitted).

- **Farrell, Joseph** (1987). "Cheap Talk, Coordination, and Entry." *RAND Journal of Economics* 18(1): 34-39. — Self-signaling messages (those making the action incentive-compatible) are credible in coordination games.

- **Schelling, Thomas C.** (1960). *The Strategy of Conflict*. Cambridge, MA: Harvard University Press. — Focal points: Salient, culturally obvious outcomes enable coordination without communication. Salience is determined by symmetry, prominence, or precedent.

## Political and Bureaucratic Collusion

- **Hirschman, Albert O.** (1970). *Exit, Voice, and Loyalty: Responses to Decline in Firms, Organizations, and States*. Cambridge, MA: Harvard University Press. — Framework: Members can exit (leave), voice (protest), or remain loyal. Loyalty suppresses exit, enabling voice. Whistleblowing is a voice mechanism.

- **Stigler, George J.** (1971). "The Theory of Economic Regulation." *Bell Journal of Economics and Management Science* 2(1): 3-21. — Regulatory capture: Regulators serve regulated industry due to concentrated benefits, diffuse costs, and revolving doors. Agencies "supply" regulation to highest bidder.

- **Tirole, Jean** (1986). "Hierarchies and Bureaucracies: On the Role of Collusion in Organizations." *Journal of Law, Economics, & Organization* 2(2): 181-214. — Principal-agent-supervisor collusion: Supervisor and agent collude to deceive principal. Requires mutual knowledge of preferences, low detection risk, and trust. Rotation disrupts collusion.

## Criminology, Fraud, and Neutralization

- **Cressey, Donald R.** (1973). *Other People's Money: A Study in the Social Psychology of Embezzlement*. Glencoe, IL: Free Press. — Fraud triangle: (1) non-shareable financial problem, (2) perceived secret opportunity to solve it via trust violation, (3) rationalization (neutralization). Determined via analytic induction on 133 embezzlers.

- **Sykes, Gresham M., and David Matza** (1957). "Techniques of Neutralization: A Theory of Delinquency." *American Sociological Review* 22(6): 664-670. — Five neutralization techniques allow offenders to engage in wrongdoing while maintaining commitment to conventional norms: denial of responsibility, injury, victim; condemnation of condemners; appeal to higher loyalties.

## Lying Experiments and Deception Detection

- **Bond, Charles F., Jr., and Bella M. DePaulo** (2006). "Accuracy of Deception Judgments." *Personality and Social Psychology Review* 10(3): 214-234. — Meta-analysis: Observers average 54% accuracy (chance = 50%). Truth bias: 61% of truths judged true, 47% of lies judged lies. Behavioral cues are weak and inconsistent.

- **DePaulo, Bella M., Deborah A. Kashy, Susan E. Kirkendol, Melissa M. Wyer, and Jennifer A. Epstein** (1996). "Lying in Everyday Life." *Journal of Personality and Social Psychology* 70(5): 979-995. — People tell roughly 1-2 lies per day, usually to manage impressions or avoid conflict.

- **DePaulo, Bella M., James J. Lindsay, Brian E. Malone, Laura Muhlenbruck, Kelly Charlton, and Harris Cooper** (2003). "Cues to Deception." *Psychological Bulletin* 129(1): 74-118. — Meta-analysis of 158 cues to deception. Liars are less forthcoming, more tense, tell less compelling tales, but many behaviors show no or weak links to deceit.

- **Erat, Sanjiv, and Uri Gneezy** (2012). "White Lies." *Management Science* 58(4): 723-733. — Altruistic white lies (cost liar, benefit other): 33% told. Pareto white lies (benefit both): 35% refused, demonstrating pure lie aversion. Women told more altruistic lies.

- **Fischbacher, Urs, and Franziska Föllmi-Heusi** (2013). "Lies in Disguise—An Experimental Study on Cheating." *Journal of the European Economic Association* 11(3): 525-547. — Die-roll paradigm: 39% fully honest, 20% fully dishonest, many partial liars. Undetectable on individual level.

- **Gneezy, Uri** (2005). "Deception: The Role of Consequences." *American Economic Review* 95(1): 384-394. — Lying rates increase with liar's gain, decrease with victim's loss. Crossover occurs when gain is modest and harm is large. Demonstrates intrinsic lie aversion and sensitivity to harm.

- **Levine, Timothy R.** (2014). "Truth-Default Theory (TDT): A Theory of Human Deception and Deception Detection." *Journal of Language and Social Psychology* 33(4): 378-392. — People default to believing others are truthful unless suspicion is triggered. Adaptive when lies are rare. Deception is eventually detected via inconsistencies, third-party information, or confessions, not demeanor.

- **Park, Hee Sun, Timothy Levine, Steven McCornack, Kelly Morrison, and Merissa Ferrara** (2002). "How People Really Detect Lies." *Communication Monographs* 69(2): 144-157. — Real-world lie detection: Lies are discovered via third-party tips, physical evidence, inconsistencies over time, and confessions. Demeanor is rarely diagnostic.

## Dual Loyalty and Conflicting Duties

- **Applbaum, Arthur Isak** (1999). *Ethics for Adversaries: The Morality of Roles in Public and Professional Life*. Princeton: Princeton University Press. — Critique of role morality: Institutions ordinarily cannot mint moral permissions to do what is otherwise prohibited. Roles add reasons but cannot silence personal moral reasons.

- **British Medical Association** (2025). *Ethical Decision Making for Doctors in the Armed Forces: A Tool Kit*. London: BMA. — Military physicians face dual loyalty: patient welfare vs. operational needs. Medical ethics obligations are primary, but operational context creates pressure.

- **Walzer, Michael** (1973). "Political Action: The Problem of Dirty Hands." *Philosophy & Public Affairs* 2(2): 160-180. — Political necessity may require acts that remain morally wrong. Agent does the "right" thing (saves lives) while committing a wrong (torture, lying), producing guilt and moral remainders.

## Cross-Cultural Ethics

- **Atari, Mohammad, et al.** (2020). "Morality Beyond the WEIRD: How the Nomological Network of Morality Varies Across Cultures." *PsyArXiv* preprint. doi:10.31234/osf.io/q6c9r — MFQ-2 validation across 25 populations. Eastern and South Asian samples weight Loyalty and Purity more heavily. Proposes Qeirat (honor) as seventh foundation.

- **Gelfand, Michele J., Lisa H. Nishii, and Jana L. Raver** (2006). "On the Nature and Importance of Cultural Tightness-Looseness." *Journal of Applied Psychology* 91(6): 1225-1244. — Tightness-looseness: Strength of social norms and degree of sanctioning. Distinct from individualism-collectivism, power distance, uncertainty avoidance. Tightness correlates with ecological/historical threats.

- **Graham, Jesse, Jonathan Haidt, and Brian A. Nosek** (2009). "Liberals and Conservatives Rely on Different Sets of Moral Foundations." *Journal of Personality and Social Psychology* 96(5): 1029-1046. — U.S. liberals prioritize Care and Fairness; conservatives endorse all five foundations including Loyalty, Authority, Purity.

- **Henrich, Joseph, Steven J. Heine, and Ara Norenzayan** (2010). "The Weirdest People in the World?" *Behavioral and Brain Sciences* 33(2-3): 61-83. — Western, Educated, Industrialized, Rich, Democratic populations are psychological outliers. Caution against generalizing from WEIRD samples.

- **Nisbett, Richard E., and Dov Cohen** (1996). *Culture of Honor: The Psychology of Violence in the South*. Boulder, CO: Westview Press. — Honor cultures (herding economies, frontier regions) enforce reputation via aggression. Insults provoke retaliation to maintain deterrent reputation.

- **Shweder, Richard A., Manamohan Mahapatra, and Joan G. Miller** (1987). "Culture and Moral Development." In *The Emergence of Morality in Young Children*, ed. Jerome Kagan and Sharon Lamb, 1-83. Chicago: University of Chicago Press. — Cross-cultural moral pluralism: India emphasizes purity and authority; U.S. emphasizes harm and fairness. Moral judgments vary substantially across cultures.

## Situational vs. Dispositional Morality

- **Darley, John M., and C. Daniel Batson** (1973). "'From Jerusalem to Jericho': A Study of Situational and Dispositional Variables in Helping Behavior." *Journal of Personality and Social Psychology* 27(1): 100-108. — Time pressure dominated religiosity in predicting helping. 63% helped when early, 10% when late. However, religiosity predicted how subjects helped once they stopped.

- **Doris, John M.** (2002). *Lack of Character: Personality and Moral Behavior*. Cambridge: Cambridge University Press. — Situationist challenge to virtue ethics: Experimental evidence (Milgram, Darley & Batson) shows behavior is situationally determined, not by stable character traits.

- **Kamtekar, Rachana** (2004). "Situationism and Virtue Ethics on the Content of Our Character." *Ethics* 114(3): 458-491. — Defense of virtue ethics: Situations govern immediate action; dispositions govern quality of action once engaged and predict long-term patterns.

## Self-Deception and Motivated Reasoning

- **Festinger, Leon** (1957). *A Theory of Cognitive Dissonance*. Stanford: Stanford University Press. — Dissonance (inconsistent beliefs/behavior) produces discomfort. Actors reduce dissonance by changing beliefs, rationalizing actions, or avoiding information.

- **Kunda, Ziva** (1990). "The Case for Motivated Reasoning." *Psychological Bulletin* 108(3): 480-498. — Motivation biases hypothesis generation, evidence evaluation, and memory. Motivationally biased beliefs result from biased search and interpretation, not conscious deception.

- **Mele, Alfred R.** (2001). *Self-Deception Unmasked*. Princeton: Princeton University Press. — Deflationary account: Self-deception is motivated, biased belief formation. Actors acquire or retain false beliefs despite contrary evidence, without needing simultaneous contradictory beliefs or a conscious "deceiver."

- **Trivers, Robert** (1985). *Social Evolution*. Menlo Park, CA: Benjamin/Cummings. — Evolutionary function of self-deception: Helps deceive others by avoiding telltale signs of awareness. Self-deception precedes other-deception.

## Moral Licensing

- **Blanken, Irene, Niels van de Ven, and Marcel Zeelenberg** (2015). "A Meta-Analytic Review of Moral Licensing." *Personality and Social Psychology Bulletin* 41(4): 540-558. — Meta-analysis: d = 0.31. Published studies show larger effects than unpublished (publication bias). Many theorized moderators not supported.

- **Monin, Benoît, and Dale T. Miller** (2001). "Moral Credentials and the Expression of Prejudice." *Journal of Personality and Social Psychology* 81(1): 33-43. — Establishing non-racist credentials increased willingness to make statements that could appear prejudiced. Original moral licensing study.

---

## Real-World Case Studies (Collusion and Fraud)

- **CFTC (Commodity Futures Trading Commission)** (2013). "Order Instituting Proceedings Pursuant to Sections 6(c) and 6(d) of the Commodity Exchange Act, Making Findings and Imposing Remedial Sanctions." CFTC Docket No. 13-14 (RBS). — RBS trader: "LIBOR is a cartel now in London" (2007). Banks coordinated submissions to manipulate benchmark rates.

- **Harrington, Scott E., and Anne M. Kherauwala** (2011). "Trust, Identity, and Disclosure in a Corrupt Industry: Evidence from LIBOR Manipulation." Working paper. — Analysis of LIBOR cartel: banks disclosed confidential submissions to each other, sustained collusion via shared norms and repeated interaction.

- **Healy, David, and Dinah Cattell** (2003). "Interface Between Authorship, Industry and Science in the Domain of Therapeutics." *British Journal of Psychiatry* 183(1): 22-27. — Pharmaceutical ghostwriting: Industry-funded studies attributed to academic authors; authorship and data analysis controlled by sponsors.

- **USADA (United States Anti-Doping Agency)** (2012). "Reasoned Decision of the United States Anti-Doping Agency on Disqualification and Ineligibility: Lance Armstrong." — Armstrong doping conspiracy: 24+ witnesses, team omertà (code of silence), enablers, and institutional complicity. Detected via whistleblowers after leniency offer.

- **van de Bunt, Henk** (2010). "Walls of Secrecy and Silence: The Madoff Case and Cartels in the Construction Industry." *Criminology & Public Policy* 9(3): 435-453. — Fraud persists through "walls of silence": insiders, bystanders, and institutions conceal misconduct via fear, benefit, ignorance, loyalty, or professional culture.

---

*End of Document. Total approximate word count: ~14,500 words.*

**Document prepared for Apart Research AI Collusion Research Sprint, October 23-25, 2026.**
