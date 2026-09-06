# Scenario: The Kehillah of Worms, 1066

Status: **draft — for review**. This is the concrete instantiation of the
v1 spec's "generic playable start" (see
[../spec/v1-kehillah-community.md](../spec/v1-kehillah-community.md) §7,
question 3) — it runs the plain Phase 1 baseline mechanic (no regional
overlay, no host dynamics), just with real names and geography instead of
placeholders.

## 1. Setting (verified against the installed 1.19 game files)

- **County/barony:** `c_worms` / `b_worms`, province 2731. Duchy of West
  Franconia, Kingdom of Germany / Holy Roman Empire.
- **Start date:** the vanilla **1066.9.15** bookmark date, not a custom
  date — this scenario overlays a new playable entry onto vanilla's
  existing 1066 history rather than requiring its own timeline.
- **Host liege:** Bishop **Siegfried** of Worms — the actual vanilla title
  holder of `c_worms` at this date (character ID 33134). Not invented.
- **Development level:** 12 (per vanilla's `1066.1.1` checkpoint on
  `c_worms`) — a modestly developed episcopal city, not a backwater.

## 2. Why 1066, specifically

Chosen deliberately, not just because it's a vanilla bookmark year:

- The real historical Worms Synagogue was built in **1034** — 32 years
  before this start date. A modest, already-established community (not
  founded-from-nothing) is the historically accurate starting state, and
  it maps directly onto starting the Synagogue main building at **tier 1**
  rather than empty (§4).
- It lands inside the documented tenure of a real, identifiable communal
  leader (§3) — the alternative bookmark years (867, 1178) don't have that.
- It's roughly 30 years before the 1096 Rhineland massacres during the
  First Crusade, which devastated Worms' Jewish community historically.
  v1 deliberately has no existential-threat mechanics yet (Phase 4), so
  this scenario is *not* framed around that — but it's worth knowing the
  date sits in a real calm-before-the-storm window, useful once Phase 4
  exists.

## 3. Starting character: Isaac ben Eliezer ha-Levi

Verified via web search, not asserted from memory alone:
- Became head of the Worms yeshiva and **chief rabbi of Worms in 1064**,
  succeeding Yaakov ben Yakar (Rashi's teacher, who died that year) — one
  of Rashi's own subsequent teachers there.
- Per Abraham Zacuto, died **c. 1070** (Zunz gives a wider range,
  1070–1096) — squarely documented as active chief rabbi through our
  1066.9.15 start date.
- Sources: [Yaakov ben Yakar (Wikipedia)](https://en.wikipedia.org/wiki/Yaakov_ben_Yakar),
  [Isaac ben Eleazar ha-Levi (Jewish Encyclopedia)](https://www.jewishencyclopedia.com/articles/8195-isaac-ha-levi-of-worms),
  [Isaac ben Eliezer (Encyclopedia.com)](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/isaac-ben-eliezer)
- Name variant: some sources transliterate "Eleazar" instead of "Eliezer"
  for the patronymic — same person. Using "Eliezer" as primary since it's
  the more common spelling across sources; note the variant in localization
  so it isn't treated as an error later.

**What's documented vs. what's estimated for game purposes:**
- Documented: chief rabbi of Worms from 1064; death c. 1070; a teacher of
  Rashi; based in Worms.
- **Estimated, not attested** — flagged explicitly rather than presented
  as fact: exact birth year and death day/month. No source gives these.
  Per this session's design discussion, we deliberately pick an **older**
  estimated birth year (proposal: c. 1000, making him mid-60s in 1066) so
  that the real ~1070 death reads as the natural end of an elder sage's
  life rather than an abruptly short reign — same real death date, more
  graceful framing. Exact death day/month within 1070: placeholder
  `1070.1.1` pending no more specific source; treat as approximate the way
  vanilla already does for many historical figures with only a known year.
- Dynasty name: **HaLevi**, taken directly from his own documented
  epithet/lineage marker (Levite descent), not invented.

**Consistency note:** this treatment — fix the documented facts (name,
role, dates, faith), let CK3's normal trait-roll systems generate the
rest — is exactly how vanilla already handles real historical religious
figures (real Popes, real Caliphs, Bishop Siegfried himself). Not a new or
special risk particular to this mod.

## 4. Starting Kehillah state

- **Title:** a new landless title, "Kehillah of Worms" (tag TBD in
  technical design), following the v1 baseline's structural pattern (§6 of
  the v1 spec).
- **Synagogue (main building):** tier 1, not empty — reflects the real
  1034 founding predating this start by three decades.
- **Internal buildings (Beit Midrash, Countinghouse, Shtadlan's Chambers,
  Communal Watch, Mikvah, Communal Hall):** none built yet. Consistent
  with a modest, single-tier community — growth is the player's job, not
  a pre-built showcase.
- **Officers (Chief Rabbi, Treasurer, Shtadlan):** none appointed at
  start, since all gate on buildings that don't exist yet (v1 spec §3c).
  Isaac ben Eliezer ha-Levi is the community's leader by virtue of holding
  the Kehillah title itself, independent of the (not-yet-existing) Chief
  Rabbi office slot — worth flagging as a naming collision to resolve in
  technical design (the title-holder is *also* historically "the rabbi" in
  the loose sense, even before the mechanical Chief Rabbi office exists).

## 5. Faith and culture — correction to an earlier draft of this file

An earlier draft flagged "no Judaism faith/culture exists yet in this
project" as a blocking prerequisite. **That was wrong.** Checked directly
against the installed 1.19 files: vanilla already ships a full
`judaism_religion` (`common/religion/religions/00_judaism.txt`) with four
faiths — **rabbinism**, karaism, haymanot, malabarism — and a
`heritage_israelite` culture family (`common/culture/cultures/00_israelite.txt`)
with five cultures — ashkenazi, sephardi, radhanite, kochinim, bavlim. This
isn't a stub; it's detailed (holy sites, doctrines, name lists, traits,
graphics assignments).

**Isaac ben Eliezer ha-Levi's faith/culture, concretely:**
- **Faith: `rabbinism`.** Notably decentralized by design —
  `doctrine_no_head`, with the doctrine's own comment reading "Rabbinism
  is highly decentralised, leaving all decisions down to the individual
  Rabbis. A religious head is very antithetical to their doctrine." That's
  a strong, native validation of Track A's whole premise: many independent
  Kehillot, no single top-down authority to appoint or depose them —
  matches real Rabbinic Judaism's actual structure, not just this mod's
  convenience.
- **Culture: `ashkenazi`.** `ethos = ethos_communal`,
  `heritage = heritage_israelite`, and its traditions include
  `tradition_diasporic` and `tradition_faith_bound` — again, real vanilla
  content already pointed at exactly this mod's premise, not generic
  filler.

**What this doesn't change:** vanilla's religion/culture data is a
population/flavor layer (used for character generation, minority
populations in various counties) — it does not include a dedicated
playable non-landed government for it. Phase 1's actual work (Kehillah
government type, Synagogue-quarter buildings, meritocratic appointment
succession) is fully necessary regardless; we just don't need to build
the faith/culture layer underneath it, which is a meaningful scope cut.

**Bonus find for later phases:** `bavlim` (Babylonian Jews) and `sephardi`
map directly onto Phase 2 (Babylonia) and Phase 3 (Sepharad) — logged to
ROADMAP.md.

## Backlog note

**Rashi at Troyes, c. 1070+, as a separate future scenario.** Checked and
ruled out for *this* scenario: Rashi (b. 1040) studied in Worms as a young
man but returned to Troyes around 1065 — a year before this start date —
and hadn't yet founded his own yeshiva (1067–1070) or built his later
reputation. Wrong city and too early to be "the leader" here. But he's a
strong candidate for a *different* scenario (Troyes, ~1070+) once this
mod supports more than one starting Kehillah — logged to ROADMAP.md.
Source: [Rashi — New World Encyclopedia](https://www.newworldencyclopedia.org/entry/Rashi).
