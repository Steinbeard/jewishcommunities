# Jewish map modes as their own category; Community Crises map; hover cards — 2026-11-08

**Status:** Implemented 2026-11-08 at Daniel's request; xTiger-clean on the files touched; not yet
checked live (checklist at the end). Supersedes the "Faith strip" and "Banner" parts of
[the 2026-10-29 map-mode strip note](2026-10-29-map-mode-strip.md) and retires the roster window
of [v12](../spec/v12-community-map-view.md).

*Addendum, later 2026-11-08:* the community card now shows in every Jewish map mode, has a Library
button and a yeshiva line, and a Beit Midrash card joins it; Beit Midrash baronies show on the
Communities map. See [the library cards note](2026-11-08-library-cards.md).

## What Daniel asked for

1. Map modes for community crises, with a hover card about the crisis.
2. Hover cards with information about libraries on the Libraries map.
3. Both modelled on the Jewish Communities map's hover card.
4. No community ledger on the Jewish Communities map.
5. The Jewish map modes in a category of their own, apart from Faith.

"Card" is read as the map's hover description (`barony_description`), the card the Jewish
Communities map already shows over a community's quarter.

## What changed

**A Jewish category.** A small menorah button (`map_mode_jewish_button`, 26 wide against the
row's 32) sits under the large Realms button, left of the bottom-right row (Faiths, Cultures,
Houses, +). Placed in that row, it made five buttons, too wide for vanilla's fixed 170-wide box;
widening the box also looked awkward (both tried 2026-11-08). It paints and opens Jewish Communities. In any
Jewish mode, the strip above the map shows only the five Jewish buttons: Communities, Rites,
Crises, Status of the Jews, Libraries. The three Faith buttons are hidden there, and the Jewish
buttons are hidden in the Faith modes, so neither family's strip carries the other's buttons.

Why the same strip widget: `hud_bottom.gui` places exactly one strip, `faith_mini_map_mode`. A
second strip would mean forking `hud_bottom.gui` as well. Instead the one strip shows one family
at a time; `ignoreinvisible` keeps it centred. The row's `ignoreinvisible` changed from `no` to
`yes`, so the hidden menorah leaves no gap in the multiplayer lobby. All changes are fenced in
`gui/shared/mapmodes.gui`.

**Community Crises map** (`kehillah_community_crises_map`). It paints each community's quarter
as follows, worst state first:

| Colour | State | Read from the community title |
|---|---|---|
| Red | an armed host, or a mob | `kehillah_mob_threat`; `kehillah_crisis_stage` 2, not done |
| Orange | agitation | `kehillah_crisis_intro_pending`; stage 1, not done |
| Purple | a decree, a Talmud trial, an expulsion | `kehillah_decree_situation`, `kehillah_trial_situation`, `kehillah_expulsion_quarters` |
| Blue | aftermath of an attack | stage 3 or 4, not done |
| Yellow | no crisis, tense or worse | holder's `kehillah_incident_yearly_chance_value` >= 8 (KehillahDangerBand's "Tense") |
| Green | no crisis, calm or uneasy | otherwise |

The states are scripted triggers in `common/scripted_triggers/kehillah_map_card_triggers.txt`.
Both the paint (`kehillah_pick_community_crises_map_color_effect`) and the card's status line
(`KehillahCrisisMapStatus`) test them in the same order. They read the same variables as
`kehillah_trouble_crisis_active_trigger`. The paint is in `kehillah_map_view_effects.txt`, with
its scripted_gui in `kehillah_map_view_gui.txt`.

**The crisis card:** the community, its county and its leader. Below that: the crisis status, the
situation's name and phase, the cause (from `KehillahCrisisCause`), and the danger band with the
yearly chance of trouble. The danger line reuses the Domain tab's `KehillahDangerBand` and
`KehillahTroubleStatusLine`.

**The library card** replaces the old three-line hover. It shows the library and its county, its
holder, its kind (sealed, yeshiva seat, Karaite or Rabbanite, in the paint's order), and the
number of works. It also shows the Tanakh parts (of 3), the Bavli orders held (of 6, or "a
complete Shas"), and the Yerushalmi orders (of 4). This covers the spec's "size and whether its
Shas is complete" (Sefer redesign section 2.5).

**Ledger retired.** The roster window and its minimized header are unregistered in
`gui/scripted_widgets/kehillah_scripted_widgets.txt`. Their definitions stay in
`gui/kehillah_community_map_view.gui`, so restoring them takes one line each. The Communities
button is now a plain button, with no open, hide or reopen states. Its tooltip is
`kehillah_communities_map_desc`. The Communities hover card now shows Prosperity, Stability and
Greatness, the columns the ledger had. The map-mode tutorial points at the new menorah button.
The paint still refreshes the mirrored roster: `kehillah_map_view_count` gates that tutorial.

## Not done

- No colour legend for the Crises map; its button tooltip lists the colours, as Rites does. The
  policy map's legend widget is the pattern if one is wanted.
- One crises map, not several. Splitting it by kind (attacks / decrees and trials / danger) is
  possible with the same triggers if the single map reads as too busy.

## Live-test checklist

1. The menorah sits after Houses in the bottom-right row; hovering it shows the category tooltip;
   clicking it opens Jewish Communities and the button glows.
2. In each Jewish mode the strip shows exactly five buttons, centred, and no Faith buttons; in
   Faiths/Holy Orders/Clerical Regions it shows only the three Faith buttons, and the holy-site
   selector still sits above Faiths.
3. No roster window appears on Jewish Communities; hovering a community shows standing and the
   three pillars.
4. Crises map: the "Showing:" banner reads "Community Crises"; quarters are coloured; in a test
   save with a crisis under way (`kehillah_inspector_debug_events` or the crisis debug events),
   the card shows status, situation, phase and cause. A quiet community shows "None" and its
   danger line.
5. Libraries map: the card shows kind, works and the three corpus lines on a Kehillah library and
   on a landed Beit Midrash.
6. `error.log` stays clean after hovering several quarters on both maps (tooltip-only errors).
