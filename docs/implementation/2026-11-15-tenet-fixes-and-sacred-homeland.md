# Tenet fixes, Rabbi virtues, and Sacred Homeland

**Status:** BUILT; 28 focused checks pass, xTiger baseline unchanged; live UI,
save, pilgrimage, and war checks UNRUN (2026-11-15).

Supersedes the glossary implementation, Communal Aid design, Communal Identity
status, and Gnosticism status in the [November 14 polish record](2026-11-14-tenet-polish-and-covenant-community.md).
Implements Daniel's screenshot feedback and subsequent requests. Work remains
in the shared checkout; concurrent community/history changes were preserved.

## Corrections

- **Historical glossary:** the native field now contains a short
  `[Glossary('Label','explanation_key')]` link. The historical paragraphs are
  separate hover localization, rather than text inserted into the tenet header.
  The general Esotericism fallback also has a short label. This follows the
  installed vanilla `pam_tenets_l_english.yml` pattern.
- **Retired tenets:** Baalei Miqra, Talmud Torah, and retired custom tenets have
  both `visible = no` and `is_shown = { always = no }`, and cannot be picked.
  Their IDs remain for save compatibility. The earlier migration maps Baalei
  Miqra to Literalism; its religious authority remains a doctrine, not a core.
  Rendering must be checked after a complete restart, not localization reload.
- **Covenant Community:** keeps +10 Same Faith Opinion and the personal +5
  opinion of fellow adherents. Copies vanilla Communal Identity's same-culture
  religious-conversion bonus, same-faith Promote Culture bonus, communal
  artifact sanctification, +10% county Development Growth, and four personal
  council-sway/language-learning flags. It does not copy different-rite opinion
  penalties or the other-culture conversion penalty. Conversion hooks still
  use vanilla's actual culture rules; no passive shared-heritage modifier is
  claimed. Offer Communal Aid is disabled, and its additional crisis-payment
  reward hooks are removed. Existing community crisis relief remains intact.
- **Statuses:** original Communal Identity is omitted from all six reviewed
  starting matrices and is Unknown. Gnosticism is Prohibited for those faiths;
  Esotericism remains separately classified. This is a choice about vanilla's
  particular Gnosticism tenet, not a ban on Jewish mystical scholarship.
- **Study:** removed the extra Pursue Sacred Study decision introduced in the
  earlier pass. Scholarly Study advertises the existing reading/mastery and
  yeshiva benefits, with no competing generic scripture-study action.

## Virtues

| Tenet | Virtues after this change |
| --- | --- |
| Scholarly Study / Iyyun ha-Talmud | Rabbi, Religious Scholar, Diligent |
| Religious Law / Pesak Halakha | Just, Rabbi, Religious Scholar |
| Reasoned Theology / Hokhmah | Physician, Erudite, Patient (retained) |

Scholarly Study replaces Erudite with `kehillah_rabbi_trait` and
`lifestyle_scholar` (whose vanilla track is displayed as Religious Scholar).
Both traditions of scholarship remain valued without requiring one character
to hold the conflicting Rabbi and Scholar traits simultaneously. No trait
creation, incompatibility, or XP-transfer rules were changed.

## Sacred Homeland

The existing holy-site alms remain. The tenet now also has native Ecclesiarchy
(`tenet_pentarchy`) parameters:

- Followers gain the native `fervor_per_holy_site = 0.05` bonus for held holy sites.
- Followers use holy-site prosperity. Vanilla's yearly hook improves a
  directly held holy-site county when the county follows the holder's faith.
- Personal adherents use holy-site development, the pilgrimage circuit, and
  companion perks. Vanilla's circuit tracks visits and supplies its rewards.
- The native pilgrimage-access parameter is included. No invented pilgrimage
  discount modifier or global activity-cost override is used. The earlier
  proposed discount was dropped because the shared base value also supplies
  other activities; the implemented pilgrimage benefit is the native circuit.

### Recover Holy Site

Adds a **county-level** CB for a landed follower whose rite has Sacred Homeland.
The county must contain an actual holy site of the attacker's faith, rather
than be hard-coded to Jerusalem; Samaritan sites therefore follow Samaritan
holy-site data. Personal adoption alone does not unlock this war.

Resolution, distance/title eligibility, hostility requirements, Piety-level
requirements, holy-war prohibitions, struggle restrictions, allied defenders,
and peace terms use vanilla's county holy war. Its Piety cost is multiplied by
0.5. This is a cheaper, specifically named recovery war, not a great holy war
or a way to conquer any county. It cannot bypass a faith's ban on holy wars.
Kehillah and adventurer governments do not gain landed conquest powers.

`scripts/kehillah_sacred_homeland_cb.py` generates the independent CB from the
installed CK3 1.20.1.2 county-war definition, preserving native outcome effects.
Re-review the upstream definition on a game update. The invalidation description
allows an absent war scope, and victory supplies the attacker scope required
by the native instigator notification helper. No vanilla CB is overridden.

## Installed artwork

Six distinct transparent DDS textures are wired to the active custom tenets:
Reasoned Theology, Scholarly Study, Sacred Liturgy, Covenant Community, Sacred
Homeland, and Witness Through Sacrifice. The last uses a memorial lamp and
stone rather than depicting or glorifying a death. Source PNGs are retained in
`scripts/tenet_icon_sources`; `scripts/kehillah_tenet_icons.py` exports them to
the native 260×400 canvas in `gfx/interface/icons/faith_tenets`.

## Migration

The separately versioned `kehillah_tenet_polish_20261115` repair runs once in
existing saves on the yearly pulse; fresh games mark it complete. The previous
repair is therefore not incorrectly treated as having applied these fixes.
Only the two expressly requested status corrections override an existing
classification: Communal Identity becomes Unknown and Gnosticism Prohibited
throughout Judaism. Other reviewed statuses still fill only Unknown entries;
reformed rite choices remain intact except the already documented replacement
of Jewish Communal Identity with Covenant Community. Book/reform integer
indices remain unchanged.

## Validation

Twelve faith-revision, eleven tenet-polish, and five screenshot-regression checks
pass. The latter check short glossary links, removal of the extra study action,
Rabbi/Scholar virtues, retired-tenet gates, holy-site CB conditions, and DDS
size/transparency. Maintained generators reproduce their current outputs.

xTiger reports **18 errors, 81 warnings, 37 untidy, 121 tips**, the same counts
as this pass's baseline. No new error or feature warning remains. Its existing
historical-glossary schema errors remain source-verified validator gaps; no
reports were suppressed. The grouped BOM warning membership changes as other
sessions edit shared files; those unrelated files were not altered here.

The authorized Luna tester found no xTiger live tools and was denied CK3 process
ownership inspection by Windows. It did not launch/control/capture a game.
Runtime rendering, AI, war resolution, and save serialization remain untested.
Git staging was also denied when creating `.git/index.lock`; no commit, push,
or PR was possible, and no unrelated work was staged.

## Manual validation

1. **Restart CK3 fully**, start a fresh 1066 game, and open Ashkenaz/Sepharad.
   Confirm all six new icons load; Baalei Miqra/Talmud Torah do not appear.
   Hover the short Am Kadosh/Hokhmah/Iyyun links: paragraphs should open only
   in the hover, with no stretched header or raw localization keys.
2. Inspect Scholarly Study and Religious Law virtues. Rabbi and Religious
   Scholar should appear; Scholarly Study should not show Erudite or advertise
   another scripture-study decision. Use the existing Study Torah/sefer course
   and confirm its scholarly mastery bonus is displayed and applied.
3. Run `event kehillah_tenet_polish_debug.0001` in debug mode. Its `TENET_POLISH`
   lines in `debug.log` should report Communal Identity Unknown and Gnosticism
   Prohibited, separately from character knowledge. Check a non-Jewish vanilla
   Communal Identity rite still has its original effects.
4. Inspect Covenant Community's follower/personal panels, same-faith opinion
   across rites, county Development Growth, conversion/culture tasks, personal
   sway/language actions, and sanctification where available. There should be
   no Offer Communal Aid action or additional tenet reward on crisis donations.
5. As a landed Sacred Homeland follower, directly hold a holy-site county of
   your faith and let the yearly hook run. Confirm native prosperity appears;
   a non-holy county must not receive it. As a personal adherent, complete
   pilgrimages to distinct own-faith holy sites and inspect circuit progress,
   companion effects, and rewards. Compare a non-adherent.
6. With Sacred Homeland core and normal holy-war eligibility, inspect a nearby
   hostile ruler holding an own-faith holy-site county. Recover Holy Site must
   target that county at half the normal county-war Piety cost. A non-holy
   county, same-faith defender, landless attacker, personal-only adherent, or
   holy-war-forbidden faith must not qualify. Check both victory and defeat
   on disposable saves. Repeat with Samaritan holy-site data if possible.
7. On a **copy** of an existing save, wait for the yearly repair or run
   `event kehillah_tenet_polish_debug.0002`. Check the two corrected statuses,
   three distinct cores, preserved other council classifications, old books,
   and reforms. Save/reload and repeat: the repair must not run twice. For a
   save predating the broader faith revision, let its yearly migration run
   first. Compare `error.log` to the pre-test baseline after each UI/action.

## 2026-11-15 follow-up: track names, Ashkenaz, and retired teachings

**Status:** BUILT, 30 focused checks pass; xTiger unchanged at 18 errors,
81 warnings, 37 untidy, 121 tips. Runtime/save checks remain unrun.
Supersedes this document's initial Ashkenaz and Sanctification assumptions.

- Ashkenaz now has Asceticism, Scholarly Study, and Covenant Community.
  Rabbi becomes a virtue through Scholarly Study. The separately versioned
  study migration replaces Legalism only in the previous exact default trio;
  other reformed Ashkenazi rosters are preserved.
- Study effects explicitly name tracks: Scholarly Study adds 3 percentage
  points to Talmudics mastery under Rabbinic authority, or Parshanut under
  other authority doctrines; personal adoption replaces 3 with 6. Literalism
  adds 4 points to Parshanut mastery (6 personal). Reasoned Theology adds 5
  to Machshavah mastery (8 personal). These are existing per-book mastery
  bonuses, not new study actions or additional Rabbi-track XP awards.
- Geonut, Pilpul, and Minhag Avoteinu are now minimal inert save-loading IDs:
  no modifiers, virtues, or parameters, no independent display names, and
  no visibility or selection. Their active replacements are Religious Law,
  Scholarly Study, and Covenant Community. The new repair removes remaining
  old rite/personal references without leaving duplicate replacement cores.
  Recognition of the Sages remains the separate authority doctrine.
- Kiddush ha-Shem's English heading is Sanctification of the Name, including
  its reform choices and modifier label. Brave and Zealous are virtues;
  Craven is the vice. Compassionate and Callous are removed from this tenet.
  Its remembrance, resistance, and survivor-support mechanics are unchanged.

Manual checks: restart fully, inspect Ashkenaz's three cores and Rabbi virtue,
hover study effects for all three track names, and confirm the retired entries
are absent. Inspect Sanctification of the Name in the tooltip and reform UI.
On a copied old save, run the versioned repair and verify only the exact old
Ashkenaz default changes, and reformed rosters retain their other choices.
