# Native Jewish cultures in play: hybrids, borders that move, Sephardi's language — 2026-11-10

**Status:** Part implemented 2026-11-10 at Daniel's request; xTiger-clean; not yet checked live
(checklist at the end). Builds on [the native-culture layer](2026-11-08-jewish-cultures-map.md).
Two parts are proposed, not built: the full historical-character pass and the faith tenet. See
"Still to do".

## What Daniel asked for

1. A way for the culture map to change in play:
   - a community founded where no Jewish culture is native should make its culture native there;
   - a ruler who hybridizes should bring his county along with him.
2. Communities and historical characters seeded with the correct cultures.
3. Hybrids that produce the historical culture (Jewish + German → Ashkenazi, and so on).
4. Sephardi speaking Arabic, then Romance, with a courtly tradition.
5. Jewish character generation using the regions, including community courtiers.
6. A faith tenet that discourages leaving the Hebrew cultures and encourages joining one.

## Built

All in `common/scripted_effects/kehillah_jewish_culture_dynamics_effects.txt`, hooked from
`common/on_action/kehillah_jewish_culture_on_actions.txt`.

**Hybridization** (`on_culture_created`). Take a new culture with one Jewish parent and one
non-Jewish parent. The non-Jewish parent's language picks the historical culture:

| Language of the non-Jewish parent | Becomes |
|---|---|
| German, Saxon, Dutch, Frankish, French | Ashkenazi |
| Occitan | Provenci |
| Iberian, Basque | Sephardi |
| Italian, Sardinian, Latin | Italki |
| Greek, Albanian, South Slavic | Romaniote |
| Czech, Polish, East Slavic, Slavonic, Vlach | Canaani, or Ashkenazi once Canaani is absorbed |
| Berber | Ma'aravi |
| Arabic, Aramaic, Egyptian | Mizrahi, or Ma'aravi / Teimani if the founder is in those lands |
| Iranian, Tocharian | Radhanite |
| Marathi | Bene Israel |
| Tamil, Telugu, Kannada | Kochini |
| Ethiopic, Cushitic, Omotic | Beta Israel |

When there is a match, everything of the hybrid moves to the historical culture:

- its counties (`set_county_culture`), which also take it as their native Jewish culture;
- its characters, including the founder;
- the founder's own lands.

The player gets a toast. The emptied hybrid is left behind with no members.

Some hybrids are kept as made:

- one with no match, such as Jewish + Norse;
- a hybrid of two Jewish cultures;
- a Jewish divergence.

For these, the founder's lands take the new culture.

**Counties** (`on_county_culture_change`). A county whose own culture becomes Jewish takes it as
its native culture.

**Rulers** (`on_character_culture_change`). A ruler whose culture becomes Jewish makes it native
in every county they hold directly, and in their domicile's county. A Kehillah leader holds no
county, so the domicile is what covers them.

**Communities** (`kehillah_claim_community_regions_effect`). Each year, and whenever the Jewish
Cultures map is painted, a community whose county has no native Jewish culture makes its leader's
culture native there.

**Sephardi** speaks Arabic. It turns to Romance (`set_culture_pillar = language_iberian`) by
chance from 1212 (Las Navas de Tolosa), and at the latest in 1250. Starts from 1250 on begin with
Romance. Its traditions lose Caravaneers and gain Poetry and Language Scholars, for the Andalusi
grammarians: Hayyuj and Ibn Janah. Spain in 867 stays Sephardi, an Arabic-speaking Sephardi; it
is not Ma'aravi.

**Courtiers.** Every place a community creates one of its own members now takes the local Jewish
culture of the leader's county, falling back to the leader's culture
(`kehillah_save_courtier_culture_effect`). That covers 16 `create_character` sites:

- household heads;
- the seeded Dayyan and notables;
- the fallback rabbi candidate;
- the yeshiva head and travelling students;
- Bet Din litigants.

Settlers from a mother community keep the mother's culture, since they carry it with them.

**Character generation in the pool** has been wired to the regions since 2026-11-08 (the pool
template).

**Historical characters fixed:**

| Figure | Was | Now |
|---|---|---|
| Béziers, Lunel and Narbonne leaders | Sephardi | Provenci |
| Prague's leader | Ashkenazi | Canaani |
| Labrat ibn Sighmar of Mahdia | Sephardi | Ma'aravi |

## Still to do

**1. The rest of the historical characters.** They are in four big files:

| File | Characters |
|---|---|
| `kehillah_historical_families_1066.txt` | 95 |
| `kehillah_sefer_haqabbalah_figures.txt` | 86 |
| `kehillah_sefer_haqabbalah_wives.txt` | 51 |
| `kehillah_world_bookmark_leaders.txt` | 47 |

Most are already right. Geonim and Babylonian sages are Mizrahi. The Spanish sages are Sephardi.
The Rhineland is Ashkenazi.

The likely corrections:

- **Kairouan's sages** (Hushiel, Hananel, Nissim) → Ma'aravi.
- **Provençal figures** (the Kimhis, Abraham ibn Daud's Provençal contemporaries) → Provenci.
- **Byzantine and Italian figures**, checked one by one.

This needs a per-character read of each figure's place, so it is a separate pass.

**2. A faith tenet: "a people that dwells apart".** Proposal:

- **The tenet.** A new tenet, given to Rabbinic Judaism's rites and to the Karaites.
- **Leaving a Hebrew culture.** A character of such a faith who moves to a non-Hebrew culture
  loses piety and gains stress, and Jewish characters think less of them. This hooks
  `on_character_culture_change`, which is already wired.
- **AI conversion.** The AI won't take vanilla's "adopt local culture" if it would leave a
  Hebrew culture. This needs a `kehillah_` override of that decision's `ai_will_do`.
- **Joining a Hebrew culture.** A new decision, "Join the [local Jewish] people", lets a
  non-Hebrew-culture character of such a faith (a convert, a Khazar) adopt the local Jewish
  culture, falling back to the nearest one. It is cheap, and the AI is weighted to take it.

The tenet files are shared with other work, so this waits for a go-ahead and a quiet tree.

**3. Babylonian and Palestinian rites**, as proposed 2026-11-09.

## Live-test checklist

1. **New 1066 game.**
   - `error.log` is clean.
   - Sephardi characters speak Arabic.
   - Béziers, Lunel and Narbonne leaders are Provenci, Prague's is Canaani, and Mahdia's is
     Ma'aravi.
2. **Courtiers.** A new household in a Provence community is Provenci, even under a Sephardi
   leader.
3. **Hybrid.** As a Jewish ruler, or with `create_hybrid_culture` from the console, hybridize
   Italki with German. The character should end up Ashkenazi, the toast should show, and their
   counties should be Ashkenazi on the Jewish Cultures map.
4. **Hybrid with no match.** Jewish + Norse should keep the hybrid, and the founder's lands
   should show it (pink).
5. **A community in an empty county.** Found one in, say, Uppland. After a repaint the county
   takes the leader's culture.
6. **Sephardi's turn.** Run `effect = { kehillah_sephardi_turns_to_romance_effect = yes }`.
   Sephardi's language should become Iberian.
