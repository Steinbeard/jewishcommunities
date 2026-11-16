# Jewish faith, rite, tenet, and holiday revision

**Status:** BUILT, source-tested; runtime/save/UI verification UNRUN (2026-11-14).
Implements the [revision specification](../spec/2026-11-14-jewish-faith-rite-tenet-and-holiday-revision.md)
with Daniel's decisions during implementation. Supersedes the starting rosters,
tenet-status initialization, and retired-tenet hooks described in the November
8–13 records where they conflict. The remaining runtime work is listed in
[the verification record](../testing/2026-11-14-faith-rite-tenet-holiday-revision.md).

## Decisions and resulting roster

Daniel approved generic Religious Legal Pronouncements (Option A), with
Rabbinic adjudication gated by authority doctrine; Malabar keeps its current
Toraic doctrine pending a separate historical review. He chose Legalism for
Kabarism and a new, DLC-independent Jewish liturgical tenet, making Poet a
virtue, for Yordei Merkavah. The scholarly equivalent is also independent of
By God Alone. No Midrash tenet or Warmongering core was introduced.

| Rite | Three cores |
|---|---|
| Bavel | Religious Legal Pronouncements; Scholarly Study; Communal Identity |
| Ashkenaz | Asceticism; Legalism; Communal Identity |
| Sepharad | Hokhmah; Religious Legal Pronouncements; Sacred Liturgy |
| Yerushalmi | Sacred Homeland; Ritual Celebrations; Communal Identity |
| Yordei Merkavah | Esotericism; Inner Journey; Sacred Liturgy |
| Karaite | Literalism; Legalism; Communal Identity |
| Haymanot | Communal Identity; Asceticism; Ritual Celebrations |
| Malabar | Communal Identity; Adaptive; Eastern Syncretism |
| Samaritan | Communal Identity; Literalism; Ritual Celebrations |
| Kabarism | Adaptive; Religious Legal Pronouncements; Legalism |

Scholarly Study displays as **Iyyun ha-Talmud** under Rabbinic authority.
Sacred Liturgy displays as **Piyyut** for Jewish rites, with `lifestyle_poet`
as its virtue. These are modest new tenets, not copies of the DLC tenets:
they grant none of By God Alone's university, choir, artifact, or education
unlocks. Both work without the DLC. Literalism displays as **Peshuto shel
Miqra** for Jewish rites. Pesak Halakha is the Rabbinic name for the generic
Legal Pronouncements tenet; non-Rabbinic adherents retain its generic name.

## Canon and offices

Jewish library access and ordinary study no longer require Talmud Torah or
Ba'alei ha-Miqra. Canon standing still follows the existing Temple Authority
doctrines, with the existing Samaritan/Orit and Bavli/Yerushalmi distinctions.
An explicitly selected authority on a rite now takes precedence over its
parent faith's authority. Personal adoption never supplies that authority.
Canonical rereading now checks the book's actual standing in the reader's
rite, rather than a work-wide canon label.

The ordinary Jewish education bonus does not give non-Rabbinic readers a
Talmudics mastery bonus. Scholarly Study favors Talmudics under Rabbinic
authority and scriptural interpretation in other traditions. Literalism
improves scriptural interpretation independently of Oral Torah authority.

**Institutional Headship** replaces Prophecy of Malachi wherever the latter
was configured. It preserves the vanilla `block_from_create_hof_parameter`
gate: removing the old name must not open generic headship creation. The
existing Gaonate and Sanhedrin remain distinct institutional routes; Gaonic
merit explicitly requires Rabbinic authority and Recognition of the Sages.
The old Geonut acclamation threshold and annual head modifier now read that
recognition instead of a tenet. Existing title succession and excommunication
rules have not been redesigned. A new Jerusalem High Priesthood/Temple
restoration is not implemented by this revision.

The existing Samaritan High Priesthood remains separate. The installed
`00_other_titles.txt` assigns **Eleazar X** in 867, **Simeon I** in 1066, and
**Aaron IV** in 1178. The pre-existing mod file wrongly labeled Akabon VIII
as the 867 holder; he actually begins in 901. Eleazar's complete installed
character record is now overridden with the Kohen trait as well. Akabon's
existing override is preserved. No title dates or succession laws changed.

## General and personal practices

- **Scholarly Study:** +10% Learning lifestyle experience for followers;
  personal Learning and spiritual fulfillment; an annual study/teaching
  choice usable without a communal government. Its library bonus is 3
  points, replaced by 6 for personal commitment. A Rabbinic yeshiva's
  quarterly fame contribution applies once even when rite and head both
  support it.
- **Piyyut:** modest follower Piety/Prestige and personal Diplomacy/spiritual
  fulfillment. Annual composition uses Learning, Diplomacy, Poet, and personal
  commitment. Three successful compositions earn Poet. Performance offers a
  reliable Piety/stress alternative. A personally committed preacher also
  receives the former devotional sermon bonus. No canon is implied by the
  prayer text, and no Rabbinic text is assigned to a non-Rabbinic worshipper.
- **Hokhmah:** no longer makes Zealous sinful. A separate discussion interaction
  has AI courtier/vassal targets, a one-year actor cooldown, and a three-year
  recipient cooldown. Learning and Diplomacy determine success, clamped at
  15–85%; personal commitment improves the chance and outcome. Success adds
  support only to an already-known teaching, never a new core or conversion.
  An exchange of questions remains available without a supported topic.
- **Legal Pronouncements:** vanilla condemnation, law-cost, personal tyranny,
  and virtue/sin mechanics are retained. A small follower clergy-opinion
  modifier and personal Learning are portable. Rabbinic adjudication adds 2 Learning units for the
  rite or 3 for personal commitment, rather than adding both. This does not
  re-enable the disabled responsa consultation path.
- **Sacred Homeland:** retains the old numeric ID, uses its general name,
  and replaces Jerusalem-only alms with a choice at an actual holy site of
  the giver's faith. One offering has one modeled recipient: a resident
  same-faith community, otherwise a same-faith custodian where represented.
  Samaritans use their own holy sites, including Gerizim. All governments
  receive the general reward; personal commitment adds consolation and Piety.
- **Communal Identity:** receives the former communal-sermon/festival
  solidarity hooks. The festival Stability award is capped once a year.
  Ritual Celebrations keeps its separate festival rewards and eligible-scene
  cadence; personal adoption qualifies without a second roll.

Vanilla Literalist Debate remains separate from the new reasoned discussion.
Literalism's existing merit, +5 advantage against co-religionists, and
`literalism_holy_war_cb_active` parameter are retained, rather than quietly
rebalancing the vanilla tenet. Esotericism retains its vanilla mechanics but
uses the Kabbalah name only under Rabbinic authority. The optional
`historical_glossary` fields copied with the vanilla tenets are supported by
the installed game's `_tenet_types.info`, despite xTiger reporting them.

## Persecution and remembrance

Kiddush ha-Shem no longer supplies an extra death branch during forced
conversion. The per-martyr Greatness award and the captured leader's death
reward are removed. Existing personality-driven choices remain character
choices, without a reward for dying.

A Grave-or-higher attack, with at least one death or forced conversion,
teaches Witness Through Sacrifice to the **original affected faith**. The
faith and attack grade are saved before coercion or crisis cleanup can
change them. Neighbouring faiths do not automatically learn it. A player
may choose personal adoption; the old automatic personal roll is AI-only.

The shared vanilla Demand Conversion acceptance calculation gains resistance
of 20 for an adherent and another 10 for personal commitment. Periodic
remembrance/aid choices reward the living. The community remembrance award
is a fixed 5 Greatness, at most once in three years, never a casualty
multiplier. It has an explicit effect tooltip.

## Festival selection and text

`jewish_holiday_scripted_triggers.txt` provides doctrine-driven compatibility
entry points; the generated capability file separates occasions from
Rabbinic practices. Thirteen original scenes remain available to their
proper practitioners. Eleven non-Rabbinic counterparts have complete text
and share only the existing option mechanics. Samaritan Passover has its
own Gerizim-aware opening; it does not presume the character traveled there
or restored the Jerusalem Temple. The generic variants avoid Rabbinic seder,
Purim obligations, outdoor sukkah roof rules, and all-night study assumptions.
No uncertain medieval Sigd date or modern liturgical detail was invented.
The Hanukkah game also no longer names a dreidel.

| Tradition | Occasion pool before household requirements |
|---|---|
| Rabbinic rites, Kabarism | All thirteen scenes |
| Karaite, Malabar with retained Toraic doctrine | All except the two Hanukkah scenes |
| Haymanot, Samaritan | Also exclude the two Purim scenes |

Children/courtiers needed by a scene are checked **before** the draw, at queue
time, and at display. Non-Rabbinic variants retain these structural conditions.
The annual draw is 60%/75% for players and 12%/16% for AI, with the higher
rate supplied by rite **or** personal Ritual Celebrations. It uses
`random_yearly_everyone_pulse` once, so ordinary courtiers are included and
rulers do not receive an extra draw. A pending scene schedules a single
monthly callback into the existing broad seasonal windows. Conversion or
incapacity clears invalid pending flags; a second queue is rejected. Old
pending flags can resume their callback from the yearly hook.

The feast overlay now requires Rabbinic practice for seder/outdoor-sukkah
wording. Passover food substitutions require the host's Passover capability.
General Jewish food replacements remain available where they do not imply
a disputed festival custom. These windows remain approximations, not a
Hebrew, Karaite, Samaritan, or Ethiopian calendar implementation.

## Save compatibility and generated data

The hidden retired definitions remain as loading bridges. Their numeric
identities are not reused. History supplies the shared starting statuses;
fresh games mark the revision without runtime `set_tenet_status` calls.
An existing save migrates once at its next yearly global pulse, with the
existing quiet-message helper. Exact old default triplets migrate to the
new roster; reformed rites retain their non-retired choices. Personal
convictions, leanings, and learned-book tenet flags migrate as well.

| Existing authored-book index | Resolved teaching |
|---|---|
| 1, 6 | Scholarly Study |
| 2 | Literalism |
| 3 | Hokhmah |
| 4 | Unrelenting Faith, replacing private devotional conviction |
| 5, 7 | Religious Legal Pronouncements |
| 8 | Communal Identity |
| 9 | Sacred Homeland, same existing ID |
| 10, 11, 12 | Esotericism, Asceticism, Kiddush ha-Shem respectively |
| 13, newly appended | Sacred Liturgy |

No saved integer is renumbered. Reform replacement ordinals 13–19 also stay
unchanged; the new replacement choice is appended separately. UI choices
deduplicate converged aliases, while dispatchers still understand them.
Two arguments converging on the same teaching count once. Historical book
IDs, authors, composition dates, languages and other non-argument metadata
are preserved. The four source generators are idempotent.

Historical arguments were reviewed separately from mechanical migrations.
Saadia's anti-Karaite position no longer becomes an attack on generic
Literalism; the Guide's old anti-simple-faith tag no longer becomes an
attack on liturgical poetry or devotion generally. The Kuzari's devotional
tag maps to Unrelenting Faith. Seder Rav Amram and the Samaritan Defter now
support Sacred Liturgy. The controversy dossier locates the disagreement
over Saadia's authority in doctrine, not in a generic personal peshat tenet.

## Historical sourcing limits

The implementation checked the researcher's
[Karaite philosophy summary](https://cris.bgu.ac.il/en/publications/karaite-philosophy/)
and [Mourners of Zion study](https://cris.bgu.ac.il/en/publications/karaite-mourning-of-zion-as-an-ascetic-movement/),
and the [Samaritan community's calendar account](https://www.israelite-samaritans.com/religion/calendar/).
These support keeping legal interpretation, philosophy, and specific
ascetic movements distinct. A modern community account is not treated as
proof of every medieval domestic custom. Malabar's canon review and new
Ethiopian/Samaritan occasion scenes remain separate research work.
