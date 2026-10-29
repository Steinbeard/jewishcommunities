**Status:** agreed with Daniel and built 2026-10-28 (first slice; see section 10 for what was
built and how it departs from the sections above). Source and xTiger checked; **not live-tested**.
Depends on
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

*(Revised twice on 2026-10-28 with Daniel's answers. The first draft scoped a duke's window
to the duchy; the second made every window the whole top realm with an "in your lands" group;
this final version gives lower lords their own view.)*

There are **two views**, chosen by whose window the chip is on:

1. **Realm view**: opened from a top liege's window or from any Kehillah leader's window. It
   covers every led community whose `domicile.domicile_location.county.holder.top_liege` is that
   top liege, and is titled "Jewish communities in the Holy Roman Empire". This is the full
   layout in section 4.
2. **Lord's view**: opened from a vassal ruler's window. It covers only the communities in that
   lord's lands: counties they hold, or their own vassals hold, at any depth. (Assumption: a
   duke's lands include his counts' counties. Narrow this to the personal domain only if Daniel
   prefers.) It's titled "Jewish communities in Champagne". It's a smaller window:
   - the same community rows (leader, local lord, charter, pillars, danger);
   - **this lord's** outlook on the Jews, since their own outlook is what moves danger
     locally (`kehillah_danger_lord_value`);
   - one compact line for the rules set from above: "Settlement policy: Allowed · Charter
     host: Heinrich IV". This stays because the overlord's policy and charters still bind these
     communities;
   - the news-feed entries for these communities only, filtered from the realm feed;
   - a link at the bottom, **"View Jewish communities in the Holy Roman Empire"**, which opens
     the realm view.

Policy, charter host and outlook-as-host always resolve to the **top liege**, the same host
V15/V16 use (`kehillah_host_charter_effects.txt` resolves
`domicile.domicile_location.county.holder.top_liege`).

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
- **A vassal's chip opens a separate lord's view** of the Jews in their own lands, with a link
  up to the overlord's realm view (section 3). This replaces the earlier same-day answer, where
  a vassal's chip opened the whole realm with their own communities called out.
- **Charters: top liege only** for now (section 3).
- **News feed, not latest-per-community**: a 10-year scrollable timeline, negative incidents
  first, positive news later (section 6).

- **Who gets the chip** (Daniel, 2026-10-28): it's clickable on any character window, whoever
  is viewing, for two kinds of character:
  - **A ruler with at least one led community in their own lands** (their domain or their
    vassals'). A top liege's chip opens the realm view. A vassal's chip opens the lord's view
    ("Jewish communities in Champagne"), which links up to the realm view (section 3).
  - **A Kehillah leader.** The chip names their host's top realm: "Jewish communities in the Holy
    Roman Empire". This is the same window the Domain-tab link opens.

  No chip on rulers whose lands hold no community, even if another part of their top realm does.

## 9. Future ideas, not scoped

- **Local vs. sovereign charters.** Some communities historically held charters from a local
  lord (a bishop, a count) rather than the sovereign, and the two could conflict. That's good
  gameplay, but it touches V15/V16's single-host assumption everywhere.
- **Positive and debate news** for the feed (section 6, later slices).

## 10. Build record (2026-10-28)

Built on branch `realm-view`. xTiger shows no reports in any new or changed file; the mod's
existing 15 errors are unchanged. **Not live-tested**: Daniel's own CK3 was running, so no test
game was started.

**Files**
- `common/scripted_triggers/kehillah_realm_view_triggers.txt`: whose lands a community is in,
  Tense-or-worse, and who gets the chip.
- `common/script_values/kehillah_realm_view_values.txt`: the danger ordering, the chip's two
  counts, and the ten-year cutoff.
- `common/scripted_effects/kehillah_realm_view_effects.txt`: the news ring buffer (add, shift)
  and the view build.
- `common/scripted_guis/kehillah_realm_view_gui.txt`: `kehillah_realm_view_chip` (is_shown,
  root = viewed character) and `kehillah_realm_view_open` (root = player, `scope:target`).
- `common/customizable_localization/kehillah_realm_view_custom_loc.txt`: the teaching name,
  teaching tone and outlook stance.
- `gui/kehillah_realm_view.gui`, registered in `gui/scripted_widgets/kehillah_scripted_widgets.txt`.
- `gui/window_character.gui`: **new override of vanilla 1.20's file.** Its only change is the
  chip block, inserted after the Treasury badge. On a game update, re-copy vanilla's file and
  re-insert that block. The file header says the same.
- `localization/english/kehillah_realm_view_l_english.yml`
- `events/kehillah_realm_view_debug_events.txt`: `.1` seeds one entry of each news kind,
  `.2` builds the view onto the event's character and logs it, `.3` clears the realm's feed.
- News hooks: `kehillah_realm_news_add_effect = { KIND = … }` sits beside the ten positive
  `kehillah_faith_pressure_add_effect` calls made in a Kehillah leader's scope:

  | Kind | Where |
  |---|---|
  | Talmud trial, badge, Holy Week, bonds, servants' decree | `events/kehillah_incident_events.txt` |
  | Mob preaching, pogrom | `kehillah_mob_effects.txt` |
  | Accusation riot | `kehillah_accusation_effects.txt` |
  | Anusim discovered | `kehillah_anusim_effects.txt` |
  | Popular rising | `kehillah_popular_rising_effects.txt` |

  Not hooked:
  - the overlord-scope anusim call, which has no community;
  - the mission (disputation) calls, which belong to the later "debates" slice;
  - host arrest and expulsion, which don't touch faith pressure. They're still unchecked
    (section 6).

**Departures from the sections above**
- The feed stores the **year** only, not the full date. That's enough for a ten-year window
  and for "newest first".
- The header tiles read the **lord**, the ruler whose lands the view covers, in both modes.
  In the realm view that's the top liege, so nothing changes there. In the lord's view, the
  teaching and outlook tiles show the vassal's own, which is what moves local danger. Policy
  still reads the top liege's realm title, with "Set by …" under it.
- In the realm view, rows don't have a separate "in your lands" group; the lord's view
  replaced it (section 3). The player's own community is highlighted, as in the map ledger.
- No Subjects-tab change (section 7). It's still unexamined.

**Live checks still owed**
1. The chip renders beside Treasury, and also in a Kehillah leader's window, where the realm
   block may be laid out differently.
2. The chip's `IsShown` and its two script values don't cause a frame-time hitch in a large
   realm.
3. The window opens and closes, and the rows, tiles and tooltips show real text. In
   particular, `Localize( Concatenate( 'kehillah_news_kind_', …GetFlagName ) )` must resolve
   for a title variable.
4. The lord's view lists only the lord's lands, and its link opens the realm view.
5. `error.log` stays clean while hovering every tooltip.

### Second pass, after Daniel's live look (2026-10-28)

- **Fixed:** the window frame, column alignment, the lord's-view subheader, and realm names
  without rank. Also restored the 11 breakdown strings that a389fff deleted (the five
  danger-band words among them).
- **Tiles are buttons:**
  - Policy opens the Jewish Settlement Policy map mode. Daniel asked for the laws, but the
    policy is a title variable changed by decision, not a realm law.
  - Teaching opens the faith.
  - Outlook opens that ruler's character window.
  - Danger moves the map to the most endangered community.
  - Each tooltip ends with what a click does.
- **Charter column is a button that opens the Charter itself**, which is a tributary
  contract:
  - the host gets `suzerain_modify_tributary_contract_interaction` on the leader;
  - the leader, on their own row, gets `subject_modify_tributary_contract_interaction` on the
    host;
  - anyone else sees the full terms on hover, with the button disabled.
- **"Known As" replaces the Standing number.** It shows the inspector's 125 pillar-combination
  descriptions (`KehillahInspectorCommunityDescription`). **Dependency:** that custom loc lives
  in the inspector work (`kehillah_inspector_descriptions.txt`), which is uncommitted as of
  this pass. The realm view needs it merged first or alongside.
- **Quarter button** on each row opens the community's domicile, as the map ledger does.

## 11. Audience layout (2026-10-28, third pass)

Daniel found the table "more cluttered and confusing" and suggested "all the kehilla leaders in
a room petitioning their lord". The window now reads top to bottom as an audience:

1. **The ruler:** portrait, name, a one-line summary ("Hears 6 communities, 1 of them Tense or
   worse"), and three fact buttons: policy, teaching and outlook. The danger tile is gone; the
   summary line and the gallery carry danger now.
2. **The petitioners:** a gallery of portrait cards, six to a row and most endangered first.
   Each card has only the county name, the description, and the danger band, plus a red strip
   when Tense or worse. Clicking a card selects it (`kehillah_realm_view_select`, the player
   variable `kehillah_rv_selected`). The view opens on the player's own community if it's
   listed, otherwise on the most endangered.
3. **The detail card** for the selected community: name, leader and place, description,
   danger; then local lord and outlook, the three pillar tiers, and the full Charter terms;
   then buttons for Open Leader, Jewish Quarter, Charter and Show on Map.
4. **Realm news:** collapsed to a header with its count, opened with a click.

**Rejected alternatives:**
- A free-form room, because a GUI datamodel lays out only in rows or grids, and placing
  portraits by hand breaks past about 15 communities.
- Per-card accordions, because each card would need its own open state, and several open at
  once brings the clutter back.

**Spacing fixes** (the France window):
- Every scrolling area now has a fixed height chosen by count. A scrollarea capped below its
  content's height left the window reserving the full height as a gap.
- The fact buttons are taller (three lines fit).
- No `text_label_center` for labels, since it draws its own dark band.

**Policy click and laws:**
- Daniel expected the settlement policy to be a realm law. It isn't: V16 made it a title
  variable changed by two decisions. A real law in `common/laws/` would appear in vanilla's
  laws tab with no GUI work.
- For now, `gui/window_my_realm.gui` shows a "Jewish Settlement Policy" panel at the top of
  the laws tab. It shows the top liege's policy, plus buttons to the raise and lower
  decisions for an independent ruler. The policy fact opens that tab for a landed player
  inside the realm.
- The old click target, the Jewish Settlement Policy map mode (2026-10-23), painted
  incorrectly in Daniel's game. It's no longer linked from here, and it's still unfixed.
- Converting the policy into a real law is recorded as an open design question.
- **Later the same day:** Daniel chose the law. The settlement policy is now the realm law
  group `kehillah_jewish_settlement` ([its note](2026-10-28-jewish-settlement-law.md)), listed
  by vanilla's laws tab. The stopgap panel was removed, and `window_my_realm.gui` is back to
  its earlier state.
