# Native Jewish cultures: one data source, a Jewish Cultures map, rites over cultures — 2026-11-08

**Status:** Implemented 2026-11-08 at Daniel's request; xTiger-clean on the files touched; not yet
checked live (checklist at the end). Adds a sixth view to
[the Jewish map category](2026-11-08-jewish-map-category.md). Switches off the minhag region
*tints* on the map (v12 section 9). The minhag regions themselves stay in gameplay; see
"Minhag regions" below.

## What Daniel asked for

1. A map mode showing where each Jewish culture is native.
2. Stored dynamically, so different start dates can differ and events can make new Jewish cultures
   appear and spread.
3. The same data source used to generate Jewish characters.
4. Cultures: Ashkenazi, Bavli, Romaniote, Italki, Sephardi, Provenci, Yerushalmi, Radhanite,
   Musta'arabi, Juhuri, Kochini, Beta Israel, and Canaani for a small part of eastern Europe.
5. Disable the minhag regions for now, unless they are useful for this.
6. Show the underlying culture on the Community Rites map.
7. On the Community Rites map, clicking a community's quarter opens the Faith view on that
   community's rite.

## The data source

Two variables on every **county** title (`common/scripted_effects/kehillah_jewish_culture_homeland_effects.txt`):

- **`kehillah_native_jewish_culture`** is the stored, authored value. It holds the culture a Jew
  native to the county is raised in, and can be any culture, including one created in play.
- **`kehillah_local_jewish_culture`** is the resolved value, and readers use this one. It is the
  county's own culture when that culture has `heritage_israelite`, and the native one otherwise.
  So a Jewish culture that comes to dominate a county becomes its local Jewish culture without any
  event having to say so. That is how a culture created in play shows up on the map and in the
  pool. `kehillah_resolve_local_jewish_culture_effect` writes it.

The data is per county, not per duchy, so that events can move a single county.

**API for events:**

- `kehillah_set_native_jewish_culture_effect = { CULTURE = culture:x }` sets one county.
- `kehillah_set_duchy_native_jewish_culture_effect = { CULTURE = scope:new_culture }` sets every
  de jure county of a duchy.
- `kehillah_native_jewish_culture_here_is_trigger = { CULTURE = x }` is a province-scope test.

**Seeding** (`kehillah_seed_native_jewish_cultures_effect`, run from `kehillah_on_game_start`
right after `kehillah_tag_minhag_regions_effect`). Later steps override earlier ones:

1. **Broad geography**, by each county's province:

   | Region | Culture |
   |---|---|
   | Iberia | Sephardi |
   | Southern Italy | Italki |
   | Balkans and Asia Minor | Romaniote |
   | Rest of Europe | Ashkenazi |
   | Levant, Arabia and North Africa | Musta'arabi |
   | Mesopotamia, Jazira and Persia | Bavli |
   | Steppe and Central Asia | Radhanite before 1100, then Bavli |
   | India | Radhanite |

2. **The minhag regions' duchy lists:**

   | Minhag region | Culture |
   |---|---|
   | Ashkenaz | Ashkenazi |
   | Provence | Provenci |
   | Italki | Italki |
   | Romaniote | Romaniote |
   | Sepharad | Sephardi |
   | Eretz Yisrael | Yerushalmi |
   | Misraim and Maghreb | Musta'arabi |
   | Bavel and Paras | Bavli |
   | Caucasus | Juhuri |

3. **Named duchies:**

   | Duchies | Culture |
   |---|---|
   | Khazaria, Azov, Alania | Radhanite |
   | Georgia, Abkhazia, Greater Armenia, Vaspurakan | Bavli |
   | Chera Nadu (Kochi) | Kochini |
   | Gondar (Semien, Dembiya) | Beta Israel |
   | Bohemia, Moravia, Lesser Poland, Wielkopolska, Mazovia, Kiev, Volhynia, Chernigov | Canaani, before 1300 (Ashkenazi after) |

The dated rules are why a 1066 start and a 1178 start differ. A save from before this change
is seeded the first time any Jewish map is painted (`kehillah_ensure_native_jewish_cultures_effect`,
gated by the global variable `kehillah_native_jewish_cultures_seeded`).

## Character generation

`pool_repopulate_local_flavor` (`common/scripted_character_templates/kehillah_pool_repopulation_patch.txt`):

- **Existing Jewish entries.** Each existing Jewish `random_culture` entry (Ashkenazi, Sephardi,
  Romaniote, Italki, Radhanite, Kochini, Bavli) now fires on the county's native culture. Its old
  geography is kept only as a fallback for an unseeded county. Ashkenazi keeps its no-pagans check.
- **New entries.** Provenci, Yerushalmi, Musta'arabi, Juhuri, Beta Israel and Canaani have
  native-culture-only entries.
- **`after_creation`.** A character with `heritage_israelite` is moved to the county's resolved
  local Jewish culture, using `set_culture`. This covers cultures created in play, which no entry
  can name. Its first name still comes from the picked culture's list.

The mod's own `create_character` calls take the leader's or county's culture and are unchanged.
Moving them onto this source is a possible follow-up.

## New cultures

All six are in `common/culture/cultures/kehillah_israelite_cultures_patch.txt` and use the Israelite
heritage. Their names are in `localization/english/kehillah_jewish_cultures_l_english.yml`.

| Culture | Language | Name list (reused for now) |
|---|---|---|
| provenci | Occitano-Romance | Sephardi |
| yerushalmi | Arabic | Bavli |
| mustarab | Arabic | Bavli |
| juhuri | Iranian | Bavli |
| beta_israel | Ethiopic | Ethiopian |
| canaani | Czech-Slovak | Ashkenazi |

Dedicated name lists are a follow-up. Traditions and ethnicities are judgement calls, noted in the
file's header.

## The maps

- **Jewish Cultures** (`kehillah_jewish_cultures_map`). It is the sixth button in the Jewish
  strip, with a culture icon. Every barony takes its county's local Jewish culture colour (titles
  `d_kehillah_mapcolor_jculture_*`). A Jewish culture with no colour of its own gets pink, and a
  county with no Jewish culture gets the neutral base. The hover card names the county and its
  Jewish culture.
- **Community Rites.** Every barony that is not a community's quarter now takes a *dimmed* tint
  of its culture (`d_kehillah_mapcolor_jculture_pale_*`, 55% of the way to the old rite base), so
  the bright rite colours stand out. The hover card on those baronies names the Jewish culture.
- **Click-through.** A zero-size widget in `gui/window_county_view.gui`
  (`kehillah_rites_map_click_to_faith`) is shown only on the Rites map and only when the clicked
  barony is a tagged quarter. On `_show` it runs `OpenGameViewData( 'faith', <leader>.GetRite )`,
  the same call vanilla's rite buttons use. Other baronies still open the county view.
- **Jewish Communities.** The minhag tints are gone, and every county takes the neutral base. The
  "Customary region" line is removed from both of its hover cards.

## Minhag regions

The minhag regions are useful here: their duchy lists are step 2 of the seeding. They also drive
gameplay, which is still on:

- Bet Din regional peers and the convene and overdue triggers;
- synods;
- the Sanhedrin election;
- the Gaonate;
- invite rules.

Turning that off would be a redesign of those systems. Another session was editing the Bet Din
files at the time, so only the map tint is switched off. `kehillah_pick_region_tint_effect` and
its colour titles are kept, unused. Whether the gameplay should move onto the culture layer
instead is open, and listed below.

## Not done / open

- Dedicated name lists for the six new cultures.
- Events that spread or found a culture. The API is ready; no event calls it yet.
- The mod's own `create_character` sites still read the leader's or county's culture.
- Whether Bet Din, synod and Sanhedrin regions should move from minhag regions to native cultures.
- The click-through fires on `_show`. If the Faith view does not close the county view, a second
  click on another quarter while it is still open may not fire. Check this live.

## Live-test checklist

1. **New game, 1066 Worms.**
   - `error.log` has no errors naming the new cultures, the template or the homeland effects.
   - The Jewish strip shows six buttons, centred.
2. **Jewish Cultures map.**
   - Each culture appears where the table above puts it: Provence lavender, Bohemia, Poland and
     Kiev pale blue, Malabar green, Gondar red, Derbent olive, Jerusalem gold.
   - Hovering shows the culture name, not a raw key.
3. **Start-date differences.** In a 1178 or later start, Central Asia is Bavli. In a start after
   1300, Bohemia is Ashkenazi.
4. **Community Rites map.**
   - The underlay is dim and the quarters are bright.
   - Hovering a non-quarter barony shows its Jewish culture.
   - Clicking Worms's quarter opens the Faith view on its rite, and a second quarter clicked
     afterwards does the same.
   - Clicking another barony opens the county view.
5. **Jewish Communities map.** The background is neutral, and the hover card has no "Customary
   region" line.
6. **Pool generation.** Run the debug pool or wait for physicians and guests in Provence or Fustat.
   New Jewish characters should be Provenci or Musta'arabi.
7. **Dynamic cultures.** Console-set a county's culture to a hybrid Jewish culture, then repaint.
   The county should show pink and its card should name the hybrid.
8. **`error.log`** stays clean after hovering both maps.
