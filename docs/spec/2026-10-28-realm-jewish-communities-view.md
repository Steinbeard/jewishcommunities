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
   `window_character.gui`, `realm_info` block). Show it when the viewed character is a landed
   ruler and at least one led community sits in their realm. When any community is Tense or
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

The window is scoped to the **viewed character's realm**: every led community whose
`domicile.domicile_location.county.holder` is that character or one of their vassals at any
level. For an emperor, that's the whole empire. For a duke, it's the duchy's sub-realm, titled
"…in the Duchy of Franconia".

Policy, charter host and outlook always resolve to the **top liege**, the same host V15/V16
use (`kehillah_host_charter_effects.txt` resolves
`domicile.domicile_location.county.holder.top_liege`). When the viewed character is a vassal,
the header says so ("Policy set by Heinrich IV"). The vassal's own outlook still appears in the
rows, as the local lord of that vassal's own communities.

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

**Incidents, last 10 years:** a dated list, newest first (see section 6). Below it, one muted
line: "Recent anti-Jewish incidents in the [faith] faith: N" (`kehillah_faith_recent_incidents_value`).

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

## 6. The one new piece of state: an incident log

Today there is no dated, realm-readable incident record. `kehillah_faith_pressure` is a decaying
per-faith counter. `kehillah_incident_outcome` is cleared after the scene. The `kehillah_history_*`
variables only record losses and refoundings. Options:

1. **Latest incident per community** (recommended first slice): when an incident resolves, set
   `kehillah_last_incident_year` and `kehillah_last_incident_kind` (a flag) on the community
   title. The window lists the communities whose year is within 10. Two new variables. The
   limit: only the newest incident per community shows.
2. **A real log:** a global variable list of per-incident record carriers. More complete, but
   CK3 variable lists can't hold structs, so it needs a carrier object per entry and pruning.
   Defer until (1) proves too thin in play.

Wording for each incident kind comes from the existing community-news loc (V30), not new prose.
Per the no-effects-in-loc rule, any odds or effects appear in tooltips, never in the line text.

## 7. Small separate fix: Subjects-tab rows

Where vanilla's subject row allows it, swap "Realm Size / Cease Tribute Chance" for the pillar
bands and danger band on Kehillah-government rows. This needs a check of
`window_character.gui`'s subject item first: if the row isn't per-row overridable without
copying the whole file, drop this.

## 8. Open questions for Daniel

- Should a vassal's chip show their own sub-realm (as proposed) or always the top realm?
- Is option 1's "latest per community" enough for the incident list?
- Should non-Jewish AI rulers' windows show the chip by default, or only when the player is
  Jewish or a host?
