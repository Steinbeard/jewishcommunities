# Revival tenets and integration audit

**Status:** BUILT, source-tested; engine/UI/save/pilgrimage checks UNRUN
(2026-11-15). Implements Daniel's expanded request for active messianism,
prophetic authority, and a Temple Service pilgrimage intent with separate
Gerizim and Jerusalem conditions. Supersedes the passive-effect proposals in
[the draft](../spec/2026-11-15-messianic-prophetic-and-temple-tenets.md).

## Three new tenets

Each has separate follower and personal modifiers/parameters, an English
heading, a short historical glossary link, and a distinct installed 260×400
transparent DDS icon. Source PNGs are in `scripts/tenet_icon_sources`.

### Messianic Hope

- Followers: +10% Monthly Piety and +5 Same Faith Opinion. Zealous and Ambitious
  are virtues; Cynical is sinful. This is the active movement-oriented version
  Daniel requested, not a claim that all Jewish messianic expectations require
  immediate political action.
- Personal: +1 Diplomacy, +10% Spiritual Fulfillment Gain, +50 Piety when a
  supporter joins, and +25 Piety for a successful sermon during the mission.
- **Proclaim a Messianic Mission** costs 250 Piety, requires devotion level 2,
  and publicly promises same-faith rule of the holy-city county within three
  years. A claimant receives a visible mission modifier and can seek support.
  The current faith must not already rule the city. The three-year deadline is
  an explicit gameplay commitment, not a historical date calculation.
- **Seek Messianic Support** sends the recipient a real choice: transfer a
  minor Gold pledge, spend 50 Piety lending public support, or refuse. The
  payment uses one captured amount for debit and credit. Support is recorded
  against the named claimant, carries a public pledge marker, and a human claimant receives a pledge toast.
  An existing commitment blocks repeated recruitment. The interaction has a
  recipient cooldown and a separate three-month claimant cadence.
- A landed claimant can use the existing **Recover Holy Site** war for
  `c_jerusalem` during the mission, with ordinary holy-war restrictions.
  The county contains both Jerusalem and Gerizim in vanilla. Landless leaders
  gain political/fundraising actions, not a landed conquest power.
- At the deadline, actual same-faith control is checked against the faith
  promised at the beginning. Success grants 750 Prestige and 500 Piety, and
  supporters receive 100 Piety. Failure costs reputation and Stress, creates
  five years of disillusion, and leaves supporters angry. Conversion cannot
  manufacture success by changing which faith the claimant promised to serve.
  Supporter markers are cleared on resolution; the mission cannot pay twice.

### Prophetic Revelation

- Followers: +1 Learning and +10% Monthly Piety. Possessed and Honest are
  virtues; Deceitful is sinful. The historical glossary distinguishes the game
  trait from a medical diagnosis of historical prophets.
- Personal: +15% Spiritual Fulfillment Gain and +25 Piety from successful
  communal sermons. Personal and core adherents can admonish rulers.
- Dormant in the starting rosters. A Jewish adult with Possessed or Mystic,
  Learning 12 and devotion level 2 can **Announce a Revelation**. Its event
  offers a public calling and explicit personal adoption, or learned examination
  without adopting the tenet. The decision costs 100 Piety and has a ten-year
  cooldown. It does not silently change a faith's cores, canon, or headship.
- **Admonish Ruler** targets an actual same-faith ruler with Arbitrary, Callous,
  or Deceitful. The text identifies the relevant conduct. The ruler receives
  the event and chooses: publicly accept restraint (five years of -20% Tyranny
  Gain, plus Piety) or reject the claim and worsen relations with the speaker.
  This is not an automatic crime, imprisonment, or loss of a personality trait.
- A proclaimed calling, recognition by an admonished ruler, or membership in
  a rite already accepting prophecy unlocks personal adoption. Core adoption
  requires recognized revival. Both native selection and the existing synod
  reform path enforce the gate; pending reforms revalidate before replacing
  a core, so loss of eligibility cannot leave a two-tenet rite.

### Temple Service

- Followers: +10% Monthly Piety and +5 Clergy Opinion. Kohen, Levite and
  Diligent are virtues; Lazy is sinful.
- Personal: +10% Spiritual Fulfillment Gain and +100 Piety on a completed
  sacrifice, in addition to the follower's ritual reward.
- **Samaritan starting core:** replaces Ritual Celebrations, keeping Covenant
  Community and Literalism. The starting High Priest must remain an alive,
  capable, free adult male Kohen for service to be available. The branch follows
  the rite's Samaritan authority doctrine, including derived rites, rather than
  treating every Jewish faith as Rabbinic.
- **Jerusalem:** remembered historically but unavailable until service is
  endowed. A Jewish non-Gerizim ruler must directly hold same-faith Jerusalem,
  possess its major sanctuary building, have an available adult male Kohen of
  the same faith (the ruler or a courtier), be at peace and devotion level 3,
  and pay 1,000 Gold and 1,000 Piety. This establishes a title-level service
  marker and permits the tenet. It does not create a High Priest, replace
  the Gaonate, or make conquest alone restore sacrifices. It abstracts the
  endowed service through the existing sanctuary building; no new building
  model or special-building replacement is introduced.
- Continued same-faith control, the sanctuary, and an available officiant
  remain requirements for Jerusalem participation. Knowing or personally
  adopting the tenet cannot bypass them.

## Offer Sacrifice: actual pilgrimage integration

The native pilgrimage is overridden at its original filename. All native
content is preserved, with exactly two additions: the new host intent and a
completion hook while `scope:activity` still exists. The source test compares
the entire copied activity with installed CK3 after removing those additions.
Compatibility with another mod replacing the same pilgrimage definition needs
the usual merge; this file must be reviewed after a game update.

- The planner must have Temple Service personally or as core. The intent
  displays its institutional and funding requirements.
- Actual destination is the **barony**, not county: `b_nablus` for Gerizim and
  `b_jerusalem` for Jerusalem. Both sites occupy `c_jerusalem` in installed CK3.
- Gerizim offerings require the April Passover window. This is an explicit
  seasonal approximation, not an implemented Hebrew/Samaritan calendar.
  Jerusalem service can support offerings throughout the year.
- At completion the code rechecks tenet, current authority, destination,
  institution, officiant, funds and the calendar-year ritual-reward cap. A successful
  offering charges `minor_gold_value` once, grants 200 Piety (300 personal),
  removes 20 Stress and grants +0.5 Monthly Piety for three years. The intent
  is explicitly completed and the pilgrim receives a narrative result.
- Wrong site, unavailable institution, wrong Gerizim season, missing funds,
  or an active reward cooldown produces a failure explanation without payment
  or additional rewards. Ordinary pilgrimage rewards remain native.
- This is a **host intent**. Guest pilgrimage intents were not broadened.

## Personal tenet and system audit

**All nine active custom tenets have personal modifiers and personal
parameters**, as do the adapted vanilla Literalism and Religious Law. Inert
retired migration IDs are not active tenets.

| Tenet | Existing system connection | Personal difference |
| --- | --- | --- |
| Scholarly Study | Talmudics mastery under Rabbinic authority, Parshanut under other authority; yeshiva teaching | Mastery bonus 6 rather than 3 percentage points; Learning/fulfillment and teaching effects |
| Reasoned Theology | Machshavah mastery; Discuss a Religious Teaching | Mastery 8 rather than 5 points; discussion success +10 points; Learning/opinion |
| Sacred Liturgy | Compose/perform sacred verse; successful communal sermons | Better composition chance, sermon Piety, Diplomacy/fulfillment |
| Covenant Community | Cross-rite opinion; culture/conversion/development; communal sermons; native sanctification | Opinion of fellow adherents and native personal sway/language hooks |
| Sacred Homeland | Alms to own-faith holy sites; holy-site fervor/prosperity; county recovery war | Enhanced alms, native pilgrim circuit/companions and fulfillment |
| Sanctification of the Name | Persecution aftermath, remembrance, survivor support, resistance | Stronger resistance/remembrance and personal fulfillment/Stress modifiers |
| Messianic Hope | Public mission, supporters/pledges, temporary holy-city war, successful campaign sermons | Extra Piety from supporters/preaching, Diplomacy and fulfillment |
| Prophetic Revelation | Revival claim, ruler admonition, recognition, communal preaching | Sermon Piety and fulfillment; personal adoption opens its actions |
| Temple Service | Priesthood/service availability; actual pilgrimage sacrifice | Ritual Piety 300 rather than 200 and fulfillment |
| Literalism (adapted vanilla) | Parshanut mastery; native scriptural debate | Mastery 6 rather than 4 points; native personal perks |
| Religious Law (adapted vanilla) | Judicial Learning used by Bet Din, disputes and responsa; named legal-source convictions | Judicial bonus 3 rather than 2 under Rabbinic authority; native personal perks |

### Sefarim, reviews, and reform

The common book-argument system links every listed tenet to book ceilings,
reviewer stances, haskamah/cherem judgments, teaching, personal conviction and
Machloket/reform proposals. These are general book-system rules; they are not
advertised as a unique advantage on every tenet card.

New argument indices are append-only: Messianic Hope **15**, Prophetic
Revelation **16**, Temple Service **17**. Old indices 1-14 stay stable.
Author choices, handwritten dispatches, dynamically authored books, generated
standing/review/Minds code and reform motions all include the new values.
Replacement choices append at **22-24**, retaining existing 1-21.

Historical connections: Saadia's Emunot ve-Deot supports Messianic Hope;
Nevi'im supports historical prophetic authority; Bavli Kodashim supports Temple
Service. Their existing composition dates, canon/tradition gates and author
metadata remain. Learning from Nevi'im does not itself revive prophecy, and
reading Kodashim does not create a Temple. Samaritan canon is not expanded to
include the Rabbinic Talmud or Nevi'im by adding this argument metadata.

### Bet Din and sermons

Religious Law directly adds the judicial bonus in
`common/script_values/kehillah_track_values.txt`. Existing Bet Din source
citations can also express a judge's convictions when a relevant named work
supports the teaching. The new tenets participate in the already existing
belief-reform motions where that council is available; no unrelated blanket
bonus is added to every legal case. A prophecy does not replace judicial
authority or rewrite canon.

`kehillah_revival_sermon_effect` is called inside the successful-preacher reward
path. A mission preacher gains 25 Prestige; personal Messianic Hope adds 25
Piety. Personal Prophetic Revelation adds 25 Piety. Existing sermon cadence,
topic selection, text citation, Parshanut XP and outcome rolls remain intact.
Sacred Liturgy's preaching reward and Covenant Community's stability effect
remain in that path. No new general Study Scripture decision was introduced.

## Migration and validation

The newly versioned `kehillah_tenet_polish_20261115_revival` migration fills
reviewed missing knowledge/status data and replaces only the previous exact
Samaritan default trio with Temple Service. Reformed Samaritan choices are
preserved. Legacy Communal Identity is converted before matching that default;
older council classifications are not reset merely because this feature adds a
new migration version. Fresh games initialize from faith/rite history and mark the runtime
repair complete. The three teachings are historically Known; Messianic Hope
and Prophetic Revelation are not forced into other default cores.

The 30 existing focused checks and eight new revival checks pass (38 total).
All eight maintained generators reproduce their outputs unchanged. The new checks
cover personal effects/art, exact native pilgrimage preservation, barony
separation, default Samaritan service, once-only payment/personal reward,
append-only dispatches, mission reckoning and recipient agency/revival gates.

Final xTiger counts are 21 errors, 83 warnings, 37 untidy, and 122 tips,
against 18 errors, 81 warnings, 37 untidy, and 121 tips before this feature.
xTiger has three additional historical-glossary schema errors, matching its
known gap documented against installed `_tenet_types.info`. It also reports
two unchanged native pilgrimage audio paths from the copied activity. These
are documented imported-source warnings, not newly invented sound paths. No
new feature script error or dangling reference remains. No report was suppressed.

The Luna tester found no live xTiger tools; Windows denied CK3 process ownership
inspection. No game was launched, controlled or captured. Runtime intent
completion, GUI, AI behavior, delayed-event scopes and save serialization are
**not** established by the source checks. Git staging remains blocked by
read-only metadata; unrelated shared work must not be staged or overwritten.

## Manual playtest

1. Restart fully and start each bookmark. Inspect Samaritan cores and all three
   new icons/glossary hovers. Run `event kehillah_revival_debug.0001` and inspect
   its `REVIVAL` lines for the service/priest/tenet distinctions.
2. As a Samaritan host with Temple Service, plan Gerizim/Nablus with **Offer
   Sacrifice**, arriving in April. Record Gold/Piety/Stress. Verify one payment,
   200 Piety, -20 Stress, the modifier and completed intent. Repeat with personal
   adoption for 300 Piety. Test another month, Jerusalem barony, funds spent
   during travel, priest unavailable, conversion en route and repeat within a
   year: no ritual reward or payment on failure.
3. As a non-Samaritan, owning/converting Jerusalem alone must not enable
   sacrifice. Endow the service with the stated resources, building and Kohen;
   then adopt Temple Service and complete the Jerusalem intent. Test loss of
   same-faith control or officiant before arrival. Reformed Samaritan authority
   must still route to Gerizim rather than Jerusalem.
4. Adopt Messianic Hope and start a mission. Request a supporter and play both
   sides: monetary pledge, public voice, refusal and delayed response. Check one
   debit/credit, toast and cooldown. On separate copies, test success/failure
   after three years, claimant conversion, supporter death, save/reload, and
   re-firing resolution. Temporary recovery war must target only the holy-city
   county for a mission-only claimant and retain native holy-war restrictions.
5. As Possessed/Mystic with the required Learning/devotion, announce a calling
   or choose examination. Test both ruler responses to a concrete admonition.
   Inspect Tyranny Gain, opinion, recognition, personal adoption and reform
   locks. Books alone must not bypass the prophecy/service gates. A queued
   Temple core replacement must lapse safely if service becomes unavailable.
6. Author works supporting indices 15-17, review/study them, inspect personal
   conviction changes and propose council reforms. Existing books/replacements
   must retain meanings. Compare successful sermons with/without the personal
   new tenets, including a failed sermon (no successful-preacher reward).
7. On a copied old save, apply the versioned repair and save/reload twice.
   Confirm the exact old Samaritan trio upgrades, custom reforms remain,
   knowledge/status initialization is quiet, and errors do not grow after UI
   interactions. Compare `error.log` to a pre-test baseline.

Debug `.0001` is read-only. `.0002` starts a mission without normal eligibility
or costs; `.0003` resolves it immediately. Use the latter two only on disposable
test saves. The three-year queued resolution is guarded against repeat reward.
