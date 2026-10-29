**Status:** proposal dated 2026-10-28, from Daniel's request in conversation. Not built. Depends on
[V12 community map view](v12-community-map-view.md) (the list-building pattern),
[V15](v15-host-charter.md)/[V16](v16-jewish-settlement-policy-and-charters.md) (charter and
settlement policy), [V34](v34-outlook-teachings-and-founding.md)/[V35](v35-player-clarity-outlook-and-invitations.md)
(outlook and teachings), [V40](v40-living-crises-and-councils.md)/[V41](v41-danger-incidents-and-the-pogrom-unfolding.md)
(danger and incidents). Sits after the [community inspector](../implementation/2026-10-25-community-map-inspector.md)
in ROADMAP order. Supersedes nothing.

# Realm view: Jewish communities in a realm

## 1. Why

From a ruler's character window, a player can't see how the Jews of that realm are doing. The
community leaders already appear in the vanilla **Subjects** tab. They're mixed in with every
other vassal there, sorted by military strength, and each row shows "Realm Size: 0" and "Cease
Tribute Chance: None", which mean nothing for a Kehillah. That tab tells you who the leaders are.
It doesn't tell you their situation. This view adds that missing piece, for Jewish and non-Jewish
players alike. A Christian ruler looking at their own Jews is also groundwork for Track B.

## 2. Entry points

1. **Character window, realm block (primary).** Add a menorah chip, "N Jewish communities",
   next to the domicile/building counter under the title row (vanilla
   `window_character.gui`, `realm_info` block). Who gets it, and what it's titled, is settled in
   section 8. A Kehillah leader holds a title but no land. If their window's realm block
   doesn't render, or is laid out differently, the chip goes in the nearest equivalent spot.
   Check this live. When any community is Tense or
   worse, add a small "N in danger" badge. Clicking it opens the window for **that
   character's realm**.
2. **Kehillah Domain tab, host section** (`gui/window_my_realm.gui`, beside
   `KEHILLAH_DOMAIN_HOST`). Add a link, "All communities under [host]", that opens the same
   window scoped to the community's host.
3. **Holding-view community inspector.** Add a small realm link in its header that opens the
   same window.

No fifth tab next to Family/Relationships/Courtiers/Subjects. Those tabs list characters, and
the row would be crowded. The chip costs no space when it's hidden.

## 3. Whose realm

*(Revised 2026-10-28 with Daniel's answer; the first draft scoped a duke's window to the duchy.)*

The window always covers the **whole top realm**: every led community whose
`domicile.domicile_location.county.holder.top_liege` is the viewed character's top liege. Only
the title and the "in your lands" group change with whose window it was opened from (section 8):
a vassal's window opens as "Jewish communities in Champagne"; an emperor's or a Kehillah leader's
as "…in the Holy Roman Empire".

When the viewed character is a vassal, their own communities are pulled out into a short
**"In your lands"** group above the full list (the same rows, filtered to counties the
viewed character holds or their vassals hold). The full realm list follows below it. For the top
liege, that group is the whole list, so it's not shown.

Policy, charter host and outlook always resolve to the **top liege**, the same host V15/V16
use (`kehillah_host_charter_effects.txt` resolves
`domicile.domicile_location.county.holder.top_liege`). When the viewed character is a vassal,
the header says so ("Policy set by Heinrich IV").

**Charters stay top-liege only.** Historically some communities held charters from a local lord
rather than the sovereign. That would give interesting gameplay (a bishop's charter versus the
emperor's) but isn't in scope here. It's recorded as a future idea in section 9.

## 4. Layout

**Header tiles (realm-wide):**

| Tile | Source |
|---|---|
| Settlement policy | top liege's primary title `var:kehillah_jewish_settlement_policy` via the four `kehillah_jewish_settlement_policy_*_trigger`s; loc `kehillah_settlement_policy_*` |
| Faith's teaching on the Jews | top liege's faith doctrine (`kehillah_teaching_*_name`: Witness, Separation and Mission, Exclusion, Dhimma, …), with its protective/strict/exclusionary band |
| Ruler's outlook | `kehillah_outlook_band_value` → `kehillah_outlook_band_*` loc, plus stance (Protector / Pragmatist / Predator / Convinced). The breakdown tooltip reuses the existing outlook breakdown. |
| Danger | **worst** community's band, named ("Mainz: Dangerous"), plus "N of M Tense or worse". Never an average, which would hide one community in trouble among quiet ones. |

**Community rows**, sorted worst danger first:

| Column | Source |
|---|---|
| Community | title name; click opens the leader (vanilla character click) |
| Leader | `holder` |
| Local lord | county holder (feeds `kehillah_danger_lord_value`) |
| Charter | cached terms, one line (the term that matters most: security), from the `kehillah_cached_charter_*` triggers; "Pending" when uncached; full terms in the tooltip |
| Pillars | three band words or icons (existing pillar-band custom loc), not raw numbers |
| Danger | `KehillahDangerBand` (Calm / Uneasy / Tense / Dangerous / Perilous); tooltip = the existing danger breakdown |

**Realm news:** a scrollable timeline, newest first, of what has happened to the realm's Jews
in the last 10 years. It covers violence and accusations now, and later debates and major good
news (see section 6). Below it, one muted line: "Recent anti-Jewish incidents in the [faith]
faith: N" (`kehillah_faith_recent_incidents_value`).

A mockup was shown in the conversation of 2026-10-28. This table is the authoritative version.

## 5. Mechanics

- **Building the list:** reuse `kehillah_refresh_map_view_effect`'s pattern
  (`common/scripted_effects/kehillah_map_view_effects.txt`). A scripted_gui runs on open with the
  viewed character as target. It counts the matches first, then runs `ordered_in_global_list` over
  `kehillah_registered_communities` with `order_by = kehillah_danger_value` and
  `max = <that count>`. The exact count matters: the gotcha recorded in that file is that a max
  larger than the list floods the error log. The result goes into a variable list on the
  player, which the window reads with `GetPlayer.MakeScope.GetList(...)`. Never iterate the
  registry per frame from the GUI.
- **Chip visibility:** a cheap `is_shown` on the scripted_gui (`any_in_global_list` with a
  realm limit). It's evaluated only while the character window is open, over a roster of
  dozens.
- **Chip count / "in danger" badge:** computed in the same pass, or the chip just reads
  "Jewish communities" without a number if a live count proves too costly. Decide while building.

## 6. The one new piece of state: the realm news feed

*(Revised 2026-10-28 with Daniel's answer. The first draft recommended keeping only the latest
incident per community. Daniel wants a feed instead: "a scrollable timeline of violence,
debates, but also anything major that was positive". Positive news is scoped later; the first
slice uses the existing negative-incident system only.)*

Today there is no dated, realm-readable incident record. `kehillah_faith_pressure` is a decaying
per-faith counter. `kehillah_incident_outcome` is cleared after the scene. The `kehillah_history_*`
variables only record losses and refoundings. The V30 community news goes to vanilla feed messages,
which script can't read back.

**Storage: a fixed-slot ring buffer on the top liege's primary title.** CK3 variable lists are sets
(adding the same year or kind twice is a no-op), so parallel lists can't hold records. Instead,
use N numbered slots (start with N = 20), each a small group of variables:

| Variable | Holds |
|---|---|
| `kehillah_feed_<n>_date` | the day the entry happened (`current_date`); also drives the 10-year cutoff |
| `kehillah_feed_<n>_kind` | a flag: `flag:riot`, `flag:accusation`, `flag:pogrom`, `flag:forced_baptism`, … |
| `kehillah_feed_<n>_community` | the community title |
| `kehillah_feed_<n>_actor` | optional character (the accuser, the lord who stood aside) |

`kehillah_realm_feed_push_effect = { KIND = … }`, run from the community leader's scope, resolves
the top liege's primary title and shifts slots n-1 down to n (dropping the oldest). It then
writes slot 1. A yearly pulse clears slots older than 10 years. The window shows slots 1..N in a
scrollarea, each visible only when its variables are set. Each line's text is a custom-loc
switch on `kind`, reusing V30 community-news wording where it exists. Because the feed belongs to
the realm, a community that later changes realm leaves its past entries with the old realm. That
matches "news from the realm".

**Hook points (first slice, negative incidents):** every place that already calls
`kehillah_faith_pressure_add_effect` with a positive amount is an incident the faith noticed, so
the feed push goes beside each one. That's about a dozen call sites in
`events/kehillah_incident_events.txt` (5), `kehillah_mob_effects.txt` (2),
`kehillah_accusation_effects.txt`, `kehillah_anusim_effects.txt` (2),
`kehillah_popular_rising_effects.txt` and `events/kehillah_mission_events.txt`. Host arrest and
expulsion should be checked too, since they may not touch faith pressure.

**To verify before building:** that a GUI line can read a title variable's flag through a
custom-loc switch with the title as root (`[Title.Custom('KehillahFeedLine1')]`, or an
equivalent), and that 20 slots × 4 variables per realm is cheap enough. 20 slots is far below
anything that should matter.

**Later slices:** debates and disputations, and major positive news (a charter granted or
improved, a protector's intervention, a great yeshiva or scholar, a new community founded).
Each later kind is just another `KIND` flag and loc line, with no new storage.

Per the no-effects-in-loc rule, any odds or effects appear in tooltips, never in the line text.

## 7. Small separate fix: Subjects-tab rows

Where vanilla's subject row allows it, swap "Realm Size / Cease Tribute Chance" for the pillar
bands and danger band on Kehillah-government rows. This needs a check of
`window_character.gui`'s subject item first: if the row isn't per-row overridable without
copying the whole file, drop this.

## 8. Decisions and open questions

Answered by Daniel, 2026-10-28:
- **A vassal's chip opens the whole top realm**, with their own communities called out
  (section 3).
- **Charters: top liege only** for now (section 3).
- **News feed, not latest-per-community**: a 10-year scrollable timeline, negative incidents
  first, positive news later (section 6).

- **Who gets the chip** (Daniel, 2026-10-28): it's clickable on any character window, whoever
  is viewing, for two kinds of character:
  - **A ruler with at least one led community in their own lands** (their domain or their
    vassals'). The chip and the window title name that ruler's realm: "Jewish communities in
    Champagne". That ruler's communities lead the window. When the ruler is a vassal, the rest of
    the top realm follows below, so policy and the other realm-level facts still make sense.
  - **A Kehillah leader.** The chip names their host's top realm: "Jewish communities in the Holy
    Roman Empire". This is the same window the Domain-tab link opens.

  No chip on rulers whose lands hold no community, even if another part of their top realm does.

## 9. Future ideas, not scoped

- **Local vs. sovereign charters.** Some communities historically held charters from a local
  lord (a bishop, a count) rather than the sovereign, and the two could conflict. That's good
  gameplay, but it touches V15/V16's single-host assumption everywhere.
- **Positive and debate news** for the feed (section 6, later slices).
