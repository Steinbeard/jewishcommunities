# Peoplehood: a Jewish doctrine that keeps Jews in a Jewish culture — 2026-11-11

**Status:** Implemented 2026-11-11 at Daniel's request; xTiger-clean; not yet checked live
(checklist at the end). Builds on
[the native-culture layer](2026-11-08-jewish-cultures-map.md) and
[its dynamics](2026-11-10-jewish-culture-dynamics.md).

## Renamed; a path to found a new Jewish people (addendum, later 2026-11-11)

**Renamed.** Daniel found "A People Dwelling Apart" (Numbers 23:9) a little xenophobic. The
doctrine is now **Covenantal Peoplehood** (`kehillah_peoplehood_covenantal`): the covenant binds a
people as well as a faith.

**Join the Jewish People** now finds a people in four steps:

1. one matching the character's language;
2. the local Jewish culture of their capital, then of where they are;
3. **new:** a Jewish culture native anywhere in their realm;
4. **new:** otherwise they found a new Jewish people.

That last step is Daniel's "a pathway for a theoretical king of Hungary"
(`kehillah_found_hebrew_people_effect`):

- Their culture is hybridized (`create_hybrid_culture`) with their region's Jewish culture. For
  example, Canaani in eastern Europe before it is absorbed, then Ashkenazi; Mizrahi in the Middle
  East; Radhanite in Persia and Asia.
- The hybrid is given the Israelite heritage (`set_culture_pillar = heritage_israelite`).
- It takes a name from the list below.
- The character and their children under 16 of the same faith join it.

The existing hooks then make it native in their lands. It shows pink on the Jewish Cultures map.
Its language is the hybrid's random pick of the two parents', as for any CK3 hybrid.

| Founding culture's language | New people (noun / collective) | Source of the name |
|---|---|---|
| Magyar | Hagari / Hagarim | Hagar, Hungary in medieval Hebrew |
| Turkic, Oghur | Togarmi / Togarmim | Togarmah, the Turks |
| Norse, Finnic, Sami, Volga Finnic, Ugro-Permian | Tzefoni / Tzefonim | tzafon, the north |
| Baltic | Litvak / Litvakim | the later name of Lithuanian Jewry |
| Goidelic, Brythonic | Iyyi / Iyyim | iyyim, the isles |
| Armenian | Ararati / Araratim | Ararat |
| Georgian | Gruzini / Gruzinim | the modern name of Georgian Jewry |
| Mongolic | Mongoli / Mongolim | |
| Chinese | Sini / Sinim | Sinim, Isaiah 49:12 |
| anything else | "<Culture> Jewish" / "<Culture> Jews" | |

**Cost and AI.** Founding costs 200 piety, against 50 for joining. The AI weight for founding is
×0.1, so the AI joins readily and founds rarely.

xTiger reports `scope:new_culture` as unset in `kehillah_found_hebrew_people_effect`. That is a
false positive: `create_hybrid_culture` saves `scope:new_culture` (game documentation).

**Live test.** In the console, give a Hungarian Catholic ruler Rabbinic Judaism, with nothing
Jewish in his realm, then take the decision. Check:

- a new culture named "Hagari" appears;
- it has the Israelite heritage;
- the ruler and his young children take it;
- his counties show it on the Jewish Cultures map;
- `error.log` stays clean.

## What Daniel asked for

A Jewish faith doctrine or tenet that:

- makes Jews of a Hebrew-heritage culture less likely to move to a non-Hebrew one;
- makes Jews of a non-Hebrew culture more likely to adopt a Hebrew one, with a decision;
- leaves Kabarism alone, so the Khazars stay distinct.

## Why a doctrine, not a tenet

Every Jewish faith should have it without spending one of its three tenet slots. A tenet would
also overlap the tenet work in progress elsewhere.

A doctrine group follows the mod's existing Jewish groups: Interfaith Marriage, Jewish Descent and
Proselytism.

- The religion sets the default, so every Jewish faith inherits it, including custom faiths.
- Kabarism overrides it with the group's other option. Both the faith and the rite carry it, since
  vanilla repeats Kabarism's doctrines in both and the mechanics read the rite.

## What base CK3 already does

Nothing in vanilla ties culture change to faith. Culture conversion is held back by four
traditions:

- Staunch Traditionalists;
- Isolationist;
- Ruling Caste;
- Cultural Primacy.

They carry `less_likely_to_culture_convert` or `expensive_convert_to_local_culture`. That makes
the Convert to Local Culture decision cost three times as much, adds stress, and multiplies the
AI's wish to take it by 0.1. Diasporic, which every Jewish culture has, changes none of this.

This doctrine copies that pattern for faith.

## What it does

**The doctrine group** is `kehillah_peoplehood` (category: marriage). It has two doctrines:

- **Covenantal Peoplehood** (`kehillah_peoplehood_covenantal`) is the default for every
  Jewish faith. Its tooltip lists the mechanics, through two doctrine parameters.
- **Open Peoplehood** (`kehillah_peoplehood_open`) is for Kabarism only.

All the mechanics test `kehillah_keeps_hebrew_peoplehood_trigger`, which reads the rite.

**Leaving a Hebrew culture.** Vanilla's Convert to Local Culture decision is overridden
(`common/decisions/kehillah_convert_to_local_culture_override.txt`). It is vanilla 1.20.1, plus
three fenced blocks. They apply when a Hebrew-culture Jew under the doctrine would convert to a
non-Hebrew capital culture:

- the prestige cost is multiplied by 3;
- the decision costs a medium piety loss and adds medium stress;
- the AI weight is multiplied by 0, so the AI never does it.

**Joining a Hebrew culture.**

- **The decision.** The same decision gets AI weight +200 when a non-Hebrew Jew under the doctrine
  rules from a Hebrew-culture capital.
- **Join the Jewish People** (`common/decisions/kehillah_peoplehood_decisions.txt`). This is for
  any playable non-Hebrew Jew under the doctrine. It costs 50 piety.
  - It picks the Jewish people closest to the character's own culture: the same language table
    hybrids use, so German gives Ashkenazi, Castilian Sephardi, Ge'ez Beta Israel and so on.
  - Failing that, it picks the local Jewish culture of their capital, then of where they are.
  - The character and their children under 16 of the same faith take it up.
  - AI weight is 100, checked every 24 months.

**Vassals following a new culture.** `request_culture_conversion_interaction` is overridden
(`common/character_interactions/kehillah_culture_conversion_override.txt`). This is the request a
new hybrid's or divergence's founder sends to vassals. Under the doctrine:

- a Hebrew-culture Jew gets −200 to follow a non-Hebrew culture;
- a non-Hebrew Jew gets +50 to follow a Hebrew one.

*Uncertain:* vanilla's own comment says acceptance is checked before the conversion. So
`scope:actor.culture` may still be the founder's old culture at that point. If so, these two
modifiers read the culture the founder is leaving. Check live.

## Not covered

- **Children** inherit their parents' culture through the engine.
- **Wards** may take their guardian's culture in childhood events.
- **The AI's own hybridization or divergence** away from a Hebrew culture is not discouraged. The
  hybrid table already turns most Jewish hybrids into Hebrew cultures.
- **Courtiers** cannot take decisions. A non-Hebrew Jewish courtier changes only through these
  routes, or through the courtier creation that already uses the local Jewish culture.

**If the override files fall behind.** Both overrides are whole copies of vanilla objects:

- `common/decisions/kehillah_convert_to_local_culture_override.txt`;
- `common/character_interactions/kehillah_culture_conversion_override.txt`;
- `common/religion/rite_types/kehillah_kabarism_rite_override.txt`.

After a game update, re-copy each and keep the fenced blocks.

## Live-test checklist

1. **The doctrine.** Open the faith view for Rabbinism and for Karaism: Peoplehood shows **Covenantal
   Peoplehood**, with both parameter lines. Kabarism shows **Open Peoplehood**.
2. **Join the Jewish People.**
   - Play a Haymanot ruler made Ethiopian. Reseed first if needed.
   - The decision shows and costs 50 piety.
   - Taking it makes the ruler Beta Israel, along with their young children.
3. **Convert to Local Culture.** As a Jewish ruler of a Hebrew culture holding a non-Jewish
   capital, the decision costs three times the prestige, and its tooltip shows the piety loss and
   stress.
4. **Khazars.** A Kabarite ruler sees neither change.
5. **`error.log`** is clean after opening the decisions and the faith view.
