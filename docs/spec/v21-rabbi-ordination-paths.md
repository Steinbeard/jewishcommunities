# V21 Spec: Rabbi Ordination Paths

**Status: PROPOSAL — approved design direction; no implementation.**
**Date: 2026-09-25.** Depends on the existing Rabbi trait, Learn Torah
scheme, community library, Beit Midrash, Chief Rabbi office, and Bet Din
Conference. It supersedes the *future acquisition* portion of the Rabbi-trait
backlog: the trait must no longer be reachable only through history, an office,
or a Bet Din invitation. It does not retcon an existing character's trait or
remove the three current routes before the new route is built and tested.

## 1. Decision

Rabbi is a recognition of sustained rabbinic study, not a generic reward for a
high Learning score and not a button a character can press on day one. The
primary route will therefore be a two-stage loop:

1. an eligible character studies Torah through the existing continuous Learn
   Torah scheme at an accessible community library; then
2. after demonstrating breadth of study, the character seeks *semicha* at a
   Beit Midrash or Yeshiva and receives the `kehillah_rabbi_trait`.

This deliberately combines the two plausible models rather than choosing
between them. Study creates the scholar; an explicit ordination event makes
the social recognition visible and lets the player decide when to take it up.
There is no generic "Become a Rabbi" decision which bypasses a community,
books, and study.

## 2. Who the path is for

The shared eligibility gate is **rabbinic-authority Jewish**, not simply any
faith in `judaism_religion`. The existing
`is_rabbinic_authority_jewish_trigger` is the canonical implementation source:
Rabbinism, Kabarism, and Merkabah. Karaism, Samaritanism, Haymanot, Malabarism,
and a future Jewish faith without rabbinic/Talmudic authority do not receive a
trait called Rabbi by accident. Adding a future rabbinic faith means extending
that one shared trigger, rather than copying faith lists into every decision
and event.

"All" here means no government, rank, or landed-status exclusion: a Kehillah
leader, landed ruler, landless adventurer, and eligible courtier use the same
candidate definition. It does **not** silently overturn the current
male-only religious-leadership rule. `kehillah_leadership_gender_eligible_trigger`
already governs the Rabbi trait, Chief Rabbi office, and semicha under the
default 1066 law; its existing egalitarian-reform hook opens that rule later.
V21 reuses that gate rather than creating an incompatible fourth gender rule.

The player-facing decision is necessarily available only while playing a
character who can take decisions. Courtiers should not receive map-wide
individual decision spam. They remain valid candidates for the same path via
Chief Rabbi appointment, Bet Din invitation, and the future Yeshiva
mentor/education pipeline; that pipeline must call the same candidate and
study-progress effects rather than grant the trait through a separate rule.

## 3. The study-and-ordination loop

### 3.1 Admission to study

`kehillah_learn_torah_decision` and `kehillah_study_torah` should admit either
an existing Rabbi **or** an apprentice who satisfies all of the following:

- adult, free, capable, rabbinic-authority Jewish, and eligible under the
  current leadership-gender rule;
- Learning **8 or higher**;
- access to the existing relevant community library (own Kehillah, a
  co-located community at a landed ruler's capital, or the current location
  of an adventurer); and
- no other active Learn Torah scheme.

Learning 8 is the literacy-and-serious-study floor, not a claim that a
moderately learned person is already a rabbi. It is deliberately reachable by
education, tutors, and later skill growth. No education trait, prestige, gold,
or Piety threshold is required to begin.

The current decision remains a long-running personal scheme. Its first
completion event should explain that an unordained reader is an apprentice,
not award the lifestyle trait immediately.

### 3.2 Apprentice progress

Trait XP is only meaningful after a character has the lifestyle trait. An
apprentice must therefore use separate character-scoped study records, not
attempt to add `kehillah_rabbi_trait` XP before the trait exists.

On a successful new work completion, the scheme records that work in an
apprentice variable list and records its field (Parshanut, Talmudics, or
Hashkafa). Re-reading a work can still be useful for ordinary study flavour,
but cannot advance ordination readiness repeatedly. The initial V21 threshold
is deliberately modest and visible:

```
2 distinct completed works, from 2 distinct fields
```

At the current two-year scheme cadence this is normally about four years,
before Learning speed and interruptions. It rewards a real course of study
without making a playable adult wait a decade before the trait becomes
relevant. The threshold belongs in a script value/trigger, not embedded in an
event, so live results can tune it to three works later without changing the
model.

### 3.3 Seek Semicha

Once ready, an eligible character sees **Seek Semicha**. It is a capstone
decision/event, not an annual random notification. It requires the candidate
to be at, or associated through the same library-resolution rules with, a
community that has at least `kehillah_beit_midrash_01`. A book cache alone is
enough to read; a functioning study hall is the minimum institution that can
recognise an ordination. Tier 3 Yeshiva improves flavour and the ceremony's
prestige/Greatness outcome, but is not required for the basic trait.

The normal outcome is reliable: meeting the published study, Learning, faith,
and institution requirements grants `kehillah_rabbi_trait`. There must be no
permanent random rejection after a player has made the investment. Learning
should affect study speed and the scholarly quality of the ceremony; Piety may
affect flavour, a modest Piety cost/reward, and how warmly peers receive the
candidate. Neither should create a second opaque hard gate. A defer option may
leave the candidate studying, but must not erase their recorded progress.

After ordination, the existing Learn Torah effect switches naturally to its
current behaviour: completed works train the three Rabbi trait tracks. The
apprentice records stay as biography/debug information only and no longer
award readiness again.

## 4. Existing institutional routes

Existing routes remain meaningful rather than being invalidated by a new
personal curriculum:

- **Historical starts:** documented historical rabbis retain the trait.
- **Chief Rabbi appointment:** appointment is institutional recognition and
  continues to confer the trait. It must use the same rabbinic-faith and
  leadership-gender eligibility checks as the ordinary route.
- **Bet Din:** panel service remains a prestigious alternative evidence of
  competence. Its semicha offer should be widened from the current
  Kehillah-government-only event trigger to an eligible rabbinic-authority
  Jewish panelist, while preserving its stale-host safety guard. The panel
  route is an institutional exception to the two-work requirement, not a
  covert second version of Learn Torah.

This keeps a learned traveller or courtier from needing to become a community
leader merely to be recognised, while still making ordinary ordination arise
from study.

## 5. AI, UI, and balance boundaries

AI should stay deliberately bounded in the first implementation. Existing AI
Learn Torah behaviour is limited to Kehillah leaders; retain that scope until
a live test proves the expanded candidate state does not start schemes across
the map. Non-player landed rulers and adventurers can still gain the trait
through a player-controlled run, office appointment, or Bet Din service. A
later AI policy can select candidates based on Learning, pious/scholarly
traits, local Yeshiva strength, and an actual need for a Chief Rabbi.

The UI needs only three additions to familiar places:

- Learn Torah's tooltip identifies an apprentice and displays completed
  fields/works, e.g. `Ordination study: 1 of 2 fields`.
- Its unavailable tooltip states the precise missing condition: rabbinic
  authority, Learning 8, an accessible work, or a usable study hall.
- Seek Semicha states the two completed fields and its institution. The event
  names the community/teacher where scope permits; it never pretends that a
  distant library is the character's own court.

No pillar receives a direct ad-hoc ordination bonus. The economic incentive is
structural: a Beit Midrash makes study and ordination possible, a Rabbi can
fill Chief Rabbi and improve the existing Greatness baseline, and learned
characters can later write works. That preserves the dynamic-pillar model
instead of hiding a one-time reward in an unrelated score.

## 6. Implementation slices

1. Add a named reusable **rabbi-ordination candidate** trigger that composes
   the rabbinic-authority, adult/free/capable, Learning, and current gender
   checks. Do not paste the conditions into Learn Torah, the scheme, office,
   and event separately.
2. Widen the existing decision/scheme from trait-holder-only to
   trait-holder-or-candidate. Split the completion effect into current trait
   XP and new apprentice-work recording.
3. Add the readiness trigger, a Beit-Midrash-aware institution resolver, the
   Seek Semicha decision/event, and localisation/debug output.
4. Reconcile Chief Rabbi and Bet Din grants with the shared faith gate without
   removing historical trait holders. Preserve the Bet Din event's
   `exists = global_var:kehillah_bet_din_convening_title` safeguard.
5. Integrate the later mentor/education pipeline by recording the same work
   progress, rather than by inventing a child-only trait grant.

## 7. Required spikes and live playtests

- **Traitless scheme spike:** prove a self-targeted scheme may safely remain
  valid for an apprentice, complete a work, and store character progress
  without trait XP or error-log noise. Confirm a trait holder still receives
  exactly the current XP result.
- **Location resolver:** live-test each existing access branch—Kehillah
  leader, landed Jewish ruler at a community, and rabbinic adventurer at a
  community—then move away or remove the Beit Midrash to prove semicha is
  correctly unavailable while ordinary reading/validity messages remain
  truthful.
- **Timing and repetition:** complete two different fields, re-read one, and
  verify only the two distinct fields count; defer semicha and confirm the
  record survives save/load, travel, and a new scheme.
- **Institutional regression:** confirm Chief Rabbi appointment, a Bet Din
  co-judge, and a historical Rabbi still behave correctly; specifically check
  the deferred Semicha guard does not reintroduce the 2026-09-24 stale-global
  error.
- **Balance:** measure real calendar time and Piety cost from Learning 8, 12,
  and 20 candidates. The target is that a competent adult with a supplied
  library can ordinarily gain ordination in roughly four to six years, not in
  one click and not only after middle age.
- **AI load:** run an observer test before expanding AI beyond Kehillah
  leaders; count schemes and inspect `error.log`/save growth rather than
  assuming the narrow existing policy remains safe once candidates broaden.
