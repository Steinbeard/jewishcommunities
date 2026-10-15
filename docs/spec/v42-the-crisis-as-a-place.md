**Status:** slice 1 built (not yet live-tested), 2026-10-14, from Daniel's review of the V41 mob preparation.
It supersedes the hub layout of [V39 slice 1c](v39-pogroms-and-the-popular-crusade.md) (`kehillah_mob.0100`
and its visits) and the "factors in the tooltip" pilot of
[V41](v41-danger-incidents-and-the-pogrom-unfolding.md) ("Tooltips by vanilla systems"). The mob's
mechanics (the march, the siege, the pogrom) are unchanged except for the timing in section 5.

# V42 The crisis as a place: navigating the mob's approach

## 1. What Daniel asked for

- **Vanilla only.** Odds show as vanilla shows them: each outcome's percentage, and a skill-challenge
  header (`duel`) where one person's skill meets another's. No text lists factors or numbers.
- **The player can see their standing.** While preparing, the player sees:
  - what protection they have secured;
  - what failed;
  - what is still pending;
  - what each has done;
  - the overall outlook.
- **Three or four choices per event,** with "something else..." as the last when there are more, as
  in vanilla's adventurer settlement visit (`ep3_laamp_decision_event.1000`, ".h: I was thinking of
  something else...").
- **A core navigation event** for the crisis, branching to pages and scenes.
- **The one asked answers in a scene of their own,** to the leader or the messenger, explaining the
  decision.
- **Protective lords and overlords generally try to help.** It may not be enough.
- **More time** between the warning and the host's arrival, if that helps.

## 2. The navigation

**`.0100` The Elders Gather (the hub).** The text is the state of things (section 3). Choices:
1. **Seek protection** goes to `.0101`.
2. **See to our own defence** goes to `.0103`: the Rosh ha-Shmirah, arms, the villages.
3. **Go out to the preacher** goes to `.0140`.
4. **Enough for now.** The hub reopens when news comes, as now.

**`.0101` Protection.** The lord, the overlord, the Church (`.0102`: the lord's chaplain, the head of
the faith), and "Back". A person already asked is not offered again.

**Each person:** "Go yourself" or "Send [the Shtadlan]".
- **Going yourself** takes the leader there; you cannot do anything else meanwhile.
- **Sending a messenger** runs in parallel; the answer comes back later.
- **Only one messenger can be on the road at a time.** The Shtadlan if there is one; otherwise a
  trusted courtier.

**Before the person** (`.0110` lord or overlord, `.0130` churchman, `.0140` the preacher): at most
three requests and "Take your leave". For the lord, these are:
- refuge in the castle;
- his men;
- what you can offer, which goes to `.0112`, listing the leader's own levers: silver, a debt, a
  hook, friendship, a physician's service.

  When there are more than three levers, the third choice is "something else...", which rotates in
  the rest.

**The answer is a scene,** `.0111` / `.0131` / `.0141`. The one asked gives a decision, with their
portrait and the leader's or the messenger's. The text varies by outcome and by who they are:
- the protective lord's open gate;
- the greedy lord's price;
- the zealous lord's refusal;
- the cautious lord's half-measure.

The roll happens in the request, which shows its percentage. The scene shows its result.

## 3. The state of things (the hub's text, a status display)

The hub text lists:
- **The host:** its size, how far, and how many days until it reaches the town at its pace.
- **Secured,** each with what it does:
  - refuge in the castle (the host must take the castle);
  - the Church's condemnation (the host thinned);
  - the lord's men (how many);
  - the watch;
  - arms;
  - the scattering.
- **Refused,** by whom.
- **On the road:** who was sent where, and when they are expected back.
- **The outlook:** the harm if the host strikes now, from `kehillah_mob_severity_value` as a band
  (light / grave / devastating). Whether the lord's men stand between the host and the town.

This is the status-display exception in the "no effects or odds in localization" rule.

## 4. Lords who help

The answer to "refuge" and "his men" follows the lord's outlook band first:

| Outlook | Refuge | His men |
|---|---|---|
| Protective | almost always | usually |
| Well-disposed | usually | sometimes |
| Indifferent | sometimes | seldom |
| Cold | seldom | rarely |
| Hostile | rarely | never |

Opinion, traits (just, compassionate, greedy, zealous, craven) and the lever offered move these.
Help is not certain to be enough:
- the lord's men are fewer than the host and may desert;
- refuge makes the host take the castle, which it may.

AI communities ask through the same values (`kehillah_mob_ai_answers_effect`).

## 5. Time

- **The host forms farther away:** 150-300 map pixels (was 100-200), about half as much time again.
- **Its pace stays at one county every 4 days.** The march tick also counts siege days in four-day
  steps (`kehillah_mob_tick_effect`), so slowing it would have lengthened the sieges too.
- **Effect:** a lord's visit (2-4 days each way), the overlord (6-12) and the head of the faith
  (10-20) fit better, more so with a messenger running in parallel.
- **Unchanged:** a mob that rises in the town itself (an accusation or a riot) still gives no
  warning.

## 6. Slices

1. **The navigation:**
   - the hub and its pages;
   - the state of things;
   - the messenger;
   - the timing.
2. **The answers as scenes:** the lord, the overlord, the churchman and the preacher, with the outlook
   table of section 4.
3. **Vanilla-only odds in all V41 events:**
   - duels where one person's skill meets another's;
   - percentages elsewhere;
   - `kehillah_change_pillar_effect` for pillar changes;
   - no numbers or odds in the text.
4. **Cleanup** of numbers in older text: the Bet Din expansion, missions, Bet Din sources, host
   crisis, Anusim, the mob warning.

Each slice: ck3-tiger, a live test, a commit.

## Addendum, 2026-10-14: decisions per host, and a Muslim mob in its own terms

**Slice 1 live test: passed.**
- The hub, messenger, answer scenes, Church letter, preacher duels and own defence all worked.
- The warning came 28 days before the host reached the gates.
- **Fixed:**
  - The offer page appears only with something to offer.
  - "Something else..." appears only with more to offer.
  - A letter shows as on the road.
  - The preacher duels' outcomes say what they do.

**One decision per person per host (Daniel: "the pope doesn't need to condemn the mob twice").**
- **Where they are kept:** lists on the host's leader (`kehillah_mob_condemned_by`,
  `kehillah_mob_condemn_refused_list`, `kehillah_mob_men_refused_list`).
- **A condemnation holds at every town** the host targets. The tick carries it to the new target, and
  the host is thinned only once.
- **Whoever has decided is not asked again,** by a player or an AI community. The hub shows the
  decision.
- **Refuge stays per community,** since it is one castle and one town.

**A Muslim mob in its own terms (Daniel: not "Preacher").**
- **The leader is a Wa'iz (Wa'iza),** the popular preacher, by flavorization. The prose noun is
  `KehillahPreacher`, read off the leader himself: "preacher" or "wa'iz".
- **The clergy are the ulama,** and the law the Pact of Umar.
- **The conversion scene is The Square:** a qadi has each person say the shahada. A Muslim mob has no
  river scene.
- **Shared lines are faith-neutral:** "converted", "the blood of the faithful", "the men of religion".
- **The army is "The Wa'iz's Host".**
- **The detection:** `kehillah_mob_is_muslim_trigger` uses the mob leader's faith, or the county's
  once the host is gone.
- **Live test of 226165f:** passed. The words still Christian in shared lines (the report, the
  warning, the hub, the market scene, the forced-conversion notice) are fixed in the commit after
  it.

**Martyrdom under a Muslim mob (Daniel: "Muslims less likely to martyr themselves").**
- **The history:** under the Almohads (1140s) most Jews converted outwardly and kept their faith in
  secret. Maimonides' *Epistle on Martyrdom* held that outward conversion to Islam, which is not
  idolatry, did not demand death. In Ashkenaz in 1096, forced baptism was met with Kiddush ha-Shem.
- **The rule, before a Muslim mob:**
  - the zealous choose death half the time, not always;
  - where the rite teaches Kiddush ha-Shem, others choose death a quarter of the time, not half;
  - converts keep their faith in secret 85% of the time (cynics 50%), against 70% (cynics 30%);
  - afterwards Kiddush ha-Shem weighs 20 against asceticism's 40 as the tenet taken, not 60.
- **Unchanged:** the severity, deaths and conversions overall still follow the pogrom. Only the choice
  between death and conversion changes.

