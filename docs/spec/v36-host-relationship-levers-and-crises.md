**Status:** built 2026-10-13 (Daniel: "add more host relationship levers and crises at lower levels of
relationship? Forcing worse contracts or giving less protection during violence"); live test pending.
It builds on [v34](v34-outlook-teachings-and-founding.md) (outlook on the Jews), [v35](v35-player-clarity-outlook-and-invitations.md)
(outlook made visible), [v33](v33-pressures.md) (the war and holy-war pressures) and the host charter
(V15/V16).

# V36: The host relationship, its levers and its crises

## Why

After V34 and V35 a lord's outlook on the Jews is computed, visible, explained, and moves the
host's attitude and policy reviews. But the player had almost no way to move it, and a cold lord
produced only slow drift. Between "Stability ticks down" and expulsion there was nothing to answer.

## 1. Protection during violence

Historically, how badly a community suffered in violence depended on its lord. In 1096 the
Bishop of Speyer sheltered the Jews and hanged rioters; elsewhere lords stood aside or joined in.

- **``kehillah_host_protection_mult_value``** (scope: a Kehillah leader) multiplies the harm of
  violence.
- **By the host's outlook band:**
  - Protective ×0.5
  - Well-disposed ×0.75
  - Indifferent ×1
  - Cold ×1.25
  - Hostile ×1.5
- **By the charter's community-security term:** recognized watch or host protection ×0.8; licensed
  watch ×0.9; disarmed ×1.
- **What it scales:**
  - the war pressures (occupation, raids, a host at war; Stability and Prosperity);
  - the crusade pressure (holy war);
  - the blow of a popular rising.
- **The Stability breakdown** gains a line naming the multiplier when any of these is active.
- **A hostile lord's men join the plunder:** a rising under a Hostile host costs an extra 40
  Prosperity, and the lord takes some gold.
- **A rising is now an event for the player** (``kehillah_host_crisis.0010``):
  - It shows the rising's leader and the host.
  - It says what the lord did, by band:
    - opened his castle (Protective);
    - came, late (Well-disposed);
    - did nothing (Indifferent);
    - stood by and watched (Cold);
    - joined in (Hostile).
  - It gives the losses.

## 2. The Lord's Demands (forced worse contracts)

- **When:** a Cold or Hostile host makes demands on a community. The check is quarterly: 4% under a
  Cold host, 10% under a Hostile one, at most once every 5 years per community
  (``kehillah_host_crisis.0001``).
- **The demand:** a special levy (2× medium gold under a Cold host, 3× under a Hostile one), or a
  revised charter.
- **Options:**
  - **Pay the levy.** Gold goes to the lord. His opinion of the leader +10, Prosperity -30.
  - **Send the Shtadlan to plead** (if one is seated).
    - The chance is 25% + 2 × the Shtadlan's diplomacy (up to +40), +10 if the lord's opinion of the
      leader is 0 or more.
    - Success: the demand is dropped, and the lord's outlook +3.
    - Failure: the charter is forced one step worse, and Stability -40.
  - **Appeal to the head of the faith** (the Pope, a caliph). Shown when he is not the lord himself
    and his outlook is Well-disposed or better. This is Sicut Judaeis, the papal bull of protection.
    - The chance is 30% + his outlook, up to 85%.
    - Success: the demand is dropped, but the lord resents it: opinion -15, outlook -3.
    - Failure: the charter is forced worse, Stability -40, and the lord's outlook -5.
  - **Refuse.** The charter is forced one step worse, Stability -40, and the lord's outlook -3.
- **Forcing a worse charter** (``kehillah_charter_worsen_one_term_effect``) moves one term a step,
  in this order:
  1. security down;
  2. building rights more restricted;
  3. jurisdiction down;
  4. the text term (Christian censorship up, or Muslim market access down).
- **Reporting:** the next quarterly charter read reports the change as "A Charter Revised"
  (Community News).
- **Duration:** the forced term holds until the realm's policy next changes, which re-applies the
  policy's defaults.
- **The AI** answers too, by ai_chance: it pays if it can afford to; otherwise the Shtadlan, the
  appeal, or refusal.

## 3. Levers: moving a lord's outlook

- **Present a Gift** (character interaction, ``kehillah_present_gift_interaction``):
  - **Target:** a Christian or Muslim ruler, duke or greater, or the community's own host or county
    lord.
  - **Cost:** medium gold.
  - **Effect:** his opinion of the leader +20, and his outlook +5 as personal history (within the
    ±30 cap).
  - **Cooldown:** once every 5 years per community.
  - **AI:** an AI leader gifts a host whose outlook is below Well-disposed.
- **Forgive the Debt** (character interaction, ``kehillah_forgive_debt_interaction``):
  - **Target:** a lord who owes this community a loan.
  - **Effect:** the loan is cancelled, his outlook +15, his opinion +30, the community's Prosperity
    -40 (the money is gone), and Greatness +20 (a name for generosity).
  - This is the reverse of the debt resentment V34 built (an old debt -15 outlook, and -10 more if
    the lord is greedy).
- **Generous loan terms** (``kehillah_loan_challenge.0002``, option b) now also give the borrower
  +5 outlook, win or lose the gamble.

## Not built (left for later)

- The positive mirror: a Protective lord granting a better charter term unasked.
- A blood-libel chain.
- An anti-Jewish faction.
- Trait additions (greedy as opportunist, and others), awaiting Daniel.

## V36b (added 2026-10-13, autonomously; Daniel: "keep going and implementing improvements")

- **The Lord's Favour** (``kehillah_host_crisis.0002``) is the positive mirror of the Lord's Demands.
  - **Chance:** a Protective host (4% a quarter) or a Well-disposed one (1%) grants one charter term
    a step better, unasked. At most once in 10 years, and only if some term can improve.
  - **Order:** security up, building rights freer, jurisdiction up, then the text term
    (``kehillah_charter_improve_one_term_effect``).
  - **The leader:** may thank the lord with a gift (medium gold; his opinion +15, outlook +3) or in
    the synagogue's prayers.
  - **Reporting:** like a forced revision, it is reported at the next charter read even inside a new
    charter's quiet window.
- **Trait additions** to the outlook's "Character" source:
  - Greedy, when not owing a Jewish lender, +5 (the opportunist; owing, the debt resentment applies
    instead).
  - Ambitious +5.
  - Trusting +5.
  - Wrathful -5.
- **Live fixes, 2026-10-13:**
  - The levy and the rising's text now read the leader's variables.
  - The rising's losses moved into the event text.
  - The gift cooldown now uses a custom_tooltip.
  - A forced revision is reported to the community's own player, and even inside the quiet window.

## V36c: a colder world (added 2026-10-13)

- **The finding:** the 23-year soak at ``6a5cda0`` saw no Cold or Hostile host. All hosts sat at
  +15 to +45, mean +28.
  - So the Lord's Demands never fired, and there were no risings.
  - 18 of 30 communities ended Flourishing in Stability.
  - The cause: the protective teaching (+15) plus average traits made every lord a friend.
- **Prejudice** (``kehillah_outlook_prejudice_value``, a new outlook source, "The prejudice of their
  time and place"): Christians -15, Muslims -10.
  - A typical lord now sits about Indifferent.
  - Protectors (compassionate, just, a zealous Witness bishop) and enemies (zeal under a strict
    teaching) stand apart.
- **Sermons:** a zealous chaplain now preaches a little against the Jews even under a protective
  teaching, -1 a year (the friars). A learned, non-zealous chaplain under a protective teaching
  still gives +1.
- **Knock-on:** host attitude (outlook × 1.5) falls by about 20-25 Stability for most communities.
  Fewer lords qualify to open the door. The opinion modifier falls 10-15 points.
- **Next:** re-soak, watching the share of Cold and Hostile hosts, demands, invitations and AI
  foundings (7 of 8 answered an invitation before), and the Stability bands.

**Superseded, same day: V36c's prejudice term is reverted.** Daniel called it "a dumb band aid": we
should fine-tune the other systems instead. In its place:
- **Personality now weighs more.**
  - Warming: compassionate +20, just +15, cynical +15, humble +10, trusting +10, forgiving +5,
    generous +5, ambitious +5, greedy without a Jewish debt +5, physician +5.
  - Cooling: sadistic -25, paranoid -15, callous -10, arrogant -10, wrathful -10, vengeful -10,
    arbitrary -5, and a theologian under a strict or exclusionary teaching -5.
- **Anti-Jewish pressure from the world** is to come: preaching friars, disputations, compelled
  sermons, faith drift tied to pressure, then the vassal faction of V31 §7.
- **The sermons change stays:** a zealous chaplain preaches -1 a year even under a protective
  teaching.

## Addendum, 2026-10-18: the Lord's Demands, odds shown

**Status:** built 2026-10-18; ck3-tiger clean; live test pending.

- The plea is made by the Shtadlan, or by the leader himself without one (it was hidden without a
  Shtadlan). Base 50 against 50; factors: the lord's band, the envoy's diplomacy, the lord's opinion
  of the leader, greedy -10. Demands come only from Cold or Hostile lords, so the typical odds stay
  near the old 25 + diplomacy x2 + 10.
- The appeal to the head of the faith: base 40 against 60; his band (+10 Well-disposed, +25
  Protective) and +15 if the lord is zealous and fears the rebuke.
- Prosperity and Stability changes go through kehillah_change_pillar_effect; the outlook number is
  gone from the description and the outlook tooltips say the direction, not the number.
- Paying off an accusation (v37 addendum) makes the same lord's Demands likelier for 10 years.
