# Tenet presentation, familiarity, and Covenant Community

**2026-11-15 correction:** the [tenet fixes and Sacred Homeland record](2026-11-15-tenet-fixes-and-sacred-homeland.md) supersedes this record's glossary, aid action, Communal Identity/Gnosticism statuses, study action, and virtue assumptions. Use its manual checklist for the current build.

**Status:** BUILT, source-tested; live/save/UI checks UNRUN (2026-11-14).
Implements Daniel's follow-up to the
[faith/rite revision](2026-11-14-faith-rite-tenet-holiday-revision.md).
Supersedes its Communal Identity selections, display-name policy, and tenet
familiarity initialization where they conflict. See the
[manual validation checklist](../testing/2026-11-14-tenet-polish-and-covenant-community.md).

## Decisions

- Keep Physician as a virtue of Reasoned Theology. Its belief and historical
  context concern bringing philosophy, medicine, and the study of nature into
  harmony with revelation; Greek learning often reaches Jewish readers through
  Arabic scholarship. Do not make devotion itself sinful.
- Use English tenet labels, concise mechanical parameters, and native historical
  glossary fields for Hokhmah, Iyyun ha-Talmud, Piyyut, Pesak Halakha, Hasidut,
  Peshuto shel Miqra, and Kiddush ha-Shem. Generic book-standing rules belong
  in the book system, not in each tenet's effects panel.
- Add Covenant Community as the Jewish alternative to vanilla Communal Identity.
  Use Am Kadosh in its historical glossary, without asserting an inherited
  cultural rank or calling converts outsiders. Vanilla's static character
  modifiers cannot directly express a religion-conditional version of its
  same-rite penalties. Preserve vanilla's definition for its many non-Jewish
  users rather than replacing those users' mechanics globally.
- Covenant Community grants same-faith affinity across rites. Shared cultural
  heritage is an actual eligibility/reward condition in its mutual-aid
  interaction; no unsupported passive heritage-opinion modifier is invented.
  A new portable aid interaction and existing crisis relief supply its action
  hook. It adds no cultural-conversion penalty and no same-faith rite penalty.
- Repair historical-rite initialization and distinguish faith-level status from
  character-level knowledge. The installed faith-history documentation allows
  historical rites to be instantiated before the tenet-status pass. Our old
  867.1.2 entry missed the 867.1.1 bookmark. Known/Permitted/Prohibited remain
  faith-wide; a one-time familiarity seed makes those starting teachings known
  to playable adherents without rewriting the faith's status during startup.
- Expand the reviewed status matrix with explicit prohibitions on human
  sacrifice, ritual cannibalism, and sacralized incest. These do not prohibit
  generic philosophical inquiry, Scripture study, or non-Rabbinic adjudication.

## Historical anchors

The [Stanford account of Ibn Daud](https://plato.stanford.edu/entries/abraham-daud/)
discusses his effort to harmonize philosophy and religion, and the transmission
of Greek philosophy and science through Arabic scholarship. It is used for
context, not to make twelfth-century Aristotelianism universal in 867.
The glossary distinguishes a general intellectual emphasis from the particular
programs of individual medieval thinkers.

## Tenets and practices

| English label | Contextual glossary | Moral emphasis | Distinct practice |
| --- | --- | --- | --- |
| Reasoned Theology | Hokhmah and Greek Wisdom | Physician, Erudite, Patient; Impatient is sinful | Religious discussion; works of thought gain 5 percentage points of mastery chance, or 8 for personal adoption; personal discussion gains 10 points |
| Scholarly Study | Iyyun ha-Talmud for Rabbinic rites | Erudite, Diligent; Lazy is sinful | Existing study/yeshiva actions; traditional sources gain 3 mastery points, 6 for personal adoption |
| Sacred Liturgy | Piyyut for appropriate Jewish rites | Poet, Humble; Arrogant is sinful | Compose and perform devotional verse; personal adoption improves the performance |
| Sacred Homeland | Distinct sacred landscapes, including Gerizim | Pilgrim, Generous; Greedy is sinful | Alms follow the giver's actual holy sites |
| Witness Through Sacrifice | Kiddush ha-Shem | Brave, Zealous, Compassionate; Callous is sinful | Remembrance and support for survivors; Craven is not made sinful |
| Covenant Community | Am Kadosh | Generous, Loyal; Callous and Disloyal are sinful | Cross-rite affinity and communal aid |

Vanilla Asceticism, Literalism, Esotericism, Ritual Celebrations, and Religious
Legal Pronouncements retain their English Jewish display labels and receive
contextual explanations. Their non-Jewish identity branches remain intact.
Active custom parameters no longer advertise the generic book-standing ceiling.
The unrelated Hokhmah Shtadlan-aptitude bonus was removed; the Machshavah track's
own aptitude remains. Rite descriptions now describe religious emphases rather
than explain the implementation.

### Covenant Community

Followers receive +10 Same Faith Opinion across rites. Personal adoption adds
+5 opinion **of** fellow adherents. Neither modifier is a passive opinion bonus
for every member of a cultural heritage. Instead, **Offer Communal Aid** is
available to needy characters of the giver's faith **or actual cultural
heritage**, regardless of rite or government. Its price uses vanilla's minor
gold value. The recipient receives the payment once and +15 gratitude for five
years, plus +5 for shared heritage. There is a five-year recipient cooldown.

An actual payment grants a minor Piety reward at most once per year. Personal
adoption adds a second minor Piety reward and minor Stress relief. The same
annual reward flag is used by existing neighbouring-community crisis payments;
it prevents receiving another tenet reward by switching between those routes.
The direct interaction is unavailable while this annual flag is active; existing
crisis relief remains possible, without another tenet award.

Vanilla Communal Identity is not overridden. It remains Permitted as a distinct,
more insular alternative, including its original mechanics. Existing Jewish
cores and personal adoption migrate to Covenant Community. Non-Jewish uses are
unaffected. This explicitly avoids inventing an unsupported static
shared-heritage opinion modifier.

## Starting rosters

| Rite | Three core tenets |
| --- | --- |
| Bavel | Religious Legal Pronouncements; Scholarly Study; Covenant Community |
| Ashkenaz | Asceticism; Legalism; Covenant Community |
| Sepharad | Reasoned Theology; Religious Legal Pronouncements; Sacred Liturgy |
| Yerushalmi | Sacred Homeland; Ritual Celebrations; Covenant Community |
| Yordei Merkavah | Esotericism; Inner Journey; Sacred Liturgy |
| Karaite | Literalism; Legalism; Covenant Community |
| Haymanot | Covenant Community; Asceticism; Ritual Celebrations |
| Malabar | Covenant Community; Adaptive; Eastern Syncretism |
| Samaritan | Covenant Community; Literalism; Ritual Celebrations |
| Kabarist | Adaptive; Religious Legal Pronouncements; Legalism |

The complete Known/Permitted/Prohibited matrix is maintained in
`scripts/kehillah_faith_revision_build.py` and emitted to faith history. All six
reviewed faiths prohibit Human Sacrifice, Ritual Cannibalism, and Divine
Marriage. The main rite's cores are automatically Permitted for other rites by
the engine; they should not be mistaken for missing Known entries.

History now instantiates Yerushalmi in 867 and Ashkenaz/Sepharad in 1000 before
the faith status pass. The existing startup seeding only creates missing rites
and uses `set_character_rite_history` for historical assignments. It retains
the existing character eligibility and community assignments.

Character knowledge is distinct from faith status. The new helper teaches
playable Jewish adherents the reviewed, already classified tenets, once per
faith membership. New games do not call `set_tenet_status` during startup.
Yearly, conversion, and title-gain hooks cover newly playable adherents.

## Compatibility and maintained generation

- A separately versioned, one-time old-save migration fills only Unknown
  statuses and preserves explicit existing Known/Permitted/Prohibited council
  decisions. It replaces Jewish Communal Identity cores, refreshes book
  ceilings, and initializes familiarity. A fresh game marks the migration done.
- Book argument indices 1-13 remain stable; Covenant Community is appended at
  14. Historical Sefer Hasidim now supports Covenant Community. Original
  Communal Identity remains a valid distinct argument at index 8.
- Reform replacement indices 1-20 remain stable; Covenant Community is
  appended at 21. New author/reform UI dispatchers include the appended values.
- The faith revision, tenet polish, holiday revision, library catalog, and
  reform generators reproduce their current outputs without changes.

## Verification and delivery limits

Twenty-three focused tests pass: twelve faith/holiday regression checks and
eleven tenet-polish checks. They cover starting dates, status separation,
historical rite creation, conservative repair, aid scopes/payment/caps,
English labels, virtues, and stable numeric book/reform dispatch.

xTiger 1.6.10 reports 18 errors versus 11 at the session baseline. The seven
additional reports are exclusively `unknown field historical_glossary` in
Covenant Community, Literalism, Reasoned Theology, Sacred Homeland, Scholarly
Study, Sacred Liturgy, and Witness Through Sacrifice. Installed
`common/religion/tenet_types/_tenet_types.info` lines 38-45 explicitly document
that optional dynamic-description field and its Rite root scope. These are
source-verified validator gaps, not suppressed errors. The pre-existing four
glossary reports and other baseline issues remain. There are no additional
script warnings in this feature; newly authored Covenant files use UTF-8 BOM.

The Luna tester could not run the live probe: CK3 process ownership inspection
was denied and no xTiger/CK3 MCP tools were exposed. Rendering, engine status
initialization, opinion behavior, AI behavior, and save/reload remain unverified
at runtime. No game was launched or controlled.

Changes remain in the requested shared checkout. Git delivery is subject to the
existing read-only `.git` metadata restriction; unrelated concurrent work must
not be staged or overwritten.
