**Status:** proposal, 2026-11-01. Nothing below is built. Daniel: "For the decrees and other crises we should have randomness and variety but make sure that the impact of the decree if passed actually matches the variety chosen. Maybe that's tricky and needs to be thought carefully?" This builds on the [decree situation](2026-11-01-decree-situation.md) and applies its rule to the [Talmud trial](2026-11-01-talmud-trial-situation.md), the accusation and the attack. The notification pools (`dc0899f`) already follow the writing half of it.

# Variety that matches its consequences

## The rule

Every way a crisis can differ is one of two kinds, and the code says which:

1. **Colour.** It changes the words only: the decree's colour or shape, who read it out, the weather. Colour must never claim an effect. If a text says "a Jew found without it will be fined", fines must exist in the game; otherwise the text does not say it.
2. **Terms.** It changes what happens: what the decree restricts, who is exempt, how hard it presses. Each term has its own effect, shown in the native tooltip, and a text for it.

**Rolled once, read everywhere.** A crisis rolls its details when it begins and stores them on its situation. Every scene, notification and verdict reads the stored details, so all of them describe the same decree. Nothing re-rolls along the way.

## The decree: what can vary

| Axis | Kind | Values (weighted by faith, region, era, the lord) | What it changes |
| --- | --- | --- | --- |
| **What it restricts** | terms | the mark (badge, ghiyar); servants and offices; **new:** no new synagogue; Easter seclusion; the oath *more judaico* (a humiliating court oath) | The enforced effect: each kind has its own effect bundle, below. |
| **Its form** | colour | the badge: the rouelle (France), the white tablets (England, 1218), the pointed hat (the Empire), a coloured sash or a sign over the door (under Islam); its colour | Text only. All forms of the mark apply the same badge effect. |
| **Who pushed it** | terms, light | the lord's bishop or chaplain (named); a friar at court (a generated character); a church council's ruling; the lord's own zeal; the town's merchants | Which answers work best. Against a bishop, the head of the faith's letter is weaker. Against merchants, silver goes further. Against the lord's own zeal, petitions are harder. The named instigator is a participant and appears in the notifications. |
| **Why now** | colour, with one light term | a council's canon; blame after a plague or a lost war; a pious new spouse; a quarrel over a loan; another lord's example | Text, plus a small push on the clerks' pressure where the motive is anger, such as plague or a loan. |
| **Exemptions** | terms | none; the leader's household (if bought at the start); a Jewish physician at the lord's court (historically common) | Who carries the effect. An exempt physician keeps his office and is named in the text. |
| **Penalty** | terms, or not said | fines; nothing said | If fines: a small gold drain each year while it is enforced, with its own tooltip line. Corporal penalties are not modelled, so no text names them. |
| **Duration** | terms | years until it lapses (20–40) | The enforced effect's length, so nothing reads "for ever" when it lapses. |

**The enforced effect of each kind:**
- **The mark:** the existing badge effect and modifier. Danger rises: marked Jews are easier to find.
- **Servants and offices:** the existing servants' decree effect.
- **No new synagogue:** the charter's construction term moves to "forbidden" while it lasts. Building in the Quarter is blocked.
- **Easter seclusion:** each Holy Week the community stays indoors, with a minor Prosperity penalty in those weeks. Holy Week violence is a little less likely, because the community is out of sight.
- **The oath *more judaico*:** the Bet Din's outside cases go worse, and Stability takes a minor penalty while it lasts.

Each new kind needs its own scenes and verdict texts, and is a slice of its own. The mark and the servants come first: they exist, and they get the axes above.

## Applying the rule to the other crises

- **The Talmud trial.**
  - **The accuser's story** is colour: a former student, a disappointed son-in-law, or a scholar who quarrelled with the rabbi.
  - **His patron** is terms. A friar makes the clerical judges harsher. A bishop gives the condemnation a monthly push. A royal official makes silver work better.
  - **The articles** are colour that must match the verdict. If the articles attack the Talmud's stories (aggadah), expurgation strikes those. If they claim it insults the faith, condemnation burns everything.
- **The accusation.**
  - The charge (blood libel, desecration, blasphemy, mockery) is already rolled and kept.
  - **Where and who** is colour: the place the body was "found", the witness's trade, the day it happened (Easter week weighs more). It is rolled once and named in every later scene.
  - The witness is a generated character, a participant, and the man the Shtadlan can question.
- **The attack.**
  - **The agitator's kind** is terms: a wandering friar, a hermit, a disgraced knight, a debtor-noble.
    - A knight brings armed men: the muster is shorter, and the siege presses harder.
    - A friar draws crowds: the monthly push is larger.
    - A debtor-noble can be bought off: silver goes further.
  - **What he preaches** is colour, and it must not contradict his kind.

## Testing it

- Debug event `kehillah_decree_debug.9` rolls a hundred decrees for the current community without starting them. It logs each combination, to check the weights: no tablets in Castile, no rouelle under Islam.
- For each terms value, a live check that the verdict's tooltip shows that term's effect, and that no text claims what the tooltip does not.

## Order of work, if approved

1. The decree's colour axes (form, why now) and the instigator, with the mark and the servants as they are. Their texts compose from the stored details.
2. The decree's terms: exemptions, fines and duration, each with its effect.
3. The trial's accuser and patron.
4. The accusation's place and witness.
5. The attack's agitator kinds.
6. New decree kinds (synagogue, Easter seclusion, the oath), one slice each.
