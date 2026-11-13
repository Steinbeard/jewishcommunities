# Nearby communities in a crisis; the situation map pin — 2026-11-11

**Status:** Implemented 2026-11-11 at Daniel's request. xTiger reports nothing new. Not yet
checked live; the checklist is at the end.

## What Daniel asked for

A crisis in another community (screenshot: "Danger to the Kehillah of Granada", listed under
*Other Situations*) didn't show on the main map. He asked for:

1. a vanilla situation map pin (`situation_map_pin_widget`) that Jewish characters see;
2. nearby Jewish communities added to the crisis as a participant group, with "nearby" meaning
   "within a distance" (his choice over "same minhag region").

## Nearby communities (built)

A fourth participant group, `kehillah_crisis_neighbour` ("Nearby communities"), is added in
`common/situation/situations/kehillah_crisis_situation.txt`. It is listed last, so nobody who
fits an earlier group lands in it.

**Who counts.** The holder of every other title in the global list
`kehillah_registered_communities` whose quarter (`holder.domicile.domicile_location`) is within
vanilla's `squared_distance_medium` of the threatened quarter. The community-founding decisions
use the same distance for "nearby".

**How it is kept current.** `kehillah_crisis_situation_sync_inner_effect` already rebuilds every
manual participant on each sync: at the start of the crisis, on each event that moves it, and
quarterly through `kehillah_crisis_situation_reconcile`. Each sync now does two things:

- removes the characters in the situation's variable list `kehillah_crisis_neighbours`;
- recomputes the neighbours and re-adds them.

The group's `is_character_valid` reads the same list. A successor, or a community that moves
away, is picked up at the next sync.

**No mechanical effect yet.** Every phase's `modifier_sets` entry is keyed to
`kehillah_crisis_community`, so neighbours get no modifiers. Every crisis decision still checks
that the viewer leads the threatened community. For now the group only makes the crisis visible
to neighbours: it shows under their *Your Situations*, and in the window's participant list.
Natural follow-ups, not built: send aid, take in refugees, a Bet Din appeal.

## The map pin (findings, nothing built)

- The pin is drawn by the engine. `gui/map_icon_layer.gui` only lays out its contents
  (`situation_map_pin_widget`, a `SituationMapIcon` data context). The data-types dump gives
  `SituationMapIcon` one function, `GetSituation`, and no script trigger decides which situations
  get a pin.
- The only scripted input is `set_situation_center_province`. The effects documentation says it
  is "useful for displaying pins". The crisis already calls it, on the leader's domicile province,
  and so do the decree and the talmud trial.
- The pin still didn't appear for Daniel, who was not a participant. The most likely reason is
  that the engine shows pins only for situations the player takes part in. If so, the neighbour
  group gives nearby Jewish leaders the pin with no GUI change, and that is also exactly the
  "Jewish characters" audience Daniel wanted. This is the first thing to check live.
- If pins turn out to show for everyone instead, restricting them to Jewish characters means
  overriding vanilla's whole `gui/map_icon_layer.gui` (about 6,000 lines) to add a `visible` to
  the pin. That is brittle across patches. It should be a separate decision.

### Live result and next experiments (later 2026-11-11)

Daniel joined a crisis with the probe `run\kehillah_crisis_join.txt`, and **still saw no pin**.
So participation alone is not the rule.

A Discord thread Daniel shared (KeizerHarm) gives vanilla's natural disasters as the working
example: their pin is the epicentre, and it is moved with an effect. Compared with
`tgp_natural_disaster.txt` and `spawn_earthquake_in_county_effect`, the crisis does the same
things: `start_situation`, then `set_situation_center_province` on the new situation. The crisis
has done this since it was built (`032b9d7`, 2026-10-31). Two differences remain:

- **Where the centre is.** The earthquake centres on a county's capital province
  (`title_province`). The crisis centres on the community's quarter barony
  (`domicile_location`).
- **How participants join.** Earthquake participants are landed rulers added automatically
  (`auto_add_rulers`, `require_realm_in_sub_region`). Every crisis participant is added by hand.

Two probes in the CK3 `run` folder test this:

- `kehillah_pin_capital.txt` moves one crisis's centre to its county's capital.
- `kehillah_pin_control_earthquake.txt` starts a real earthquake in that county, as a control.
  Test saves only.

If the earthquake shows a pin and the moved crisis doesn't, the difference is in the situation
definition or in how participants join. If neither shows a pin, it's the map mode, the zoom, or
an interface setting.

**Result (Daniel, later 2026-11-11):** the earthquake showed a pin over Garnatah. The crisis did
not, even with its centre moved to the same county capital. Daniel isn't a participant in the
earthquake, so the engine's rule is neither participation nor location. It is in the situation
**definition**. Compared with the earthquake, the crisis:

- is in group `minor` (the earthquake is in `natural_disasters`);
- sets `window`, `gui_window_name`, a triggered `icon` and an `illustration`, none of which the
  earthquake sets.

Debug-only test types A, B and C (`common/situation/situations/kehillah_pin_test_situations.txt`)
separate those two differences. The probe `run\kehillah_pin_test.txt` starts all three around
the player. A copies the earthquake's shape; B is A in group `minor`; C is A with the crisis's
window, icon and illustration. A restart is needed first. Delete the test types once the answer
is in.

**Result:** A (Troyes), B (Langres) and C (Sens) all started cleanly, and **none showed a pin**,
not even the earthquake-shaped A. So neither the group type nor the window and icon settings is
the cause. A still differs from the earthquake in two ways:

- **Participants.** A has none; the earthquake auto-adds the landed rulers of the area.
- **Icons.** Every vanilla situation type has an icon file named after its key in
  `gfx/interface/icons/situation_types/`. No type in this mod has one, the crisis included.

Two more tests check these. **D** auto-adds rulers and starts in Paris. **E** gets a copy of the
earthquake's icon as its type icon file, plus sub-region and phase icons, and starts in Reims. The
probe is `run\kehillah_pin_test2.txt`. If E shows a pin, the fix for the crisis is just a
`kehillah_community_crisis.dds` in that folder.

**Correction (Daniel, later 2026-11-11):** the first probe's pins *were* there; Daniel had been
looking in the wrong place. **A (Troyes) and C (Sens) showed a pin; B (Langres) did not.** C's pin
carried the crisis's torch-and-pitchfork icon; A's was blank, having no icon. So the window,
custom GUI, icon and illustration are fine, participants are not needed, and no type icon file is
needed. **The only thing that hides the pin is `situation_group_type = minor`.** Vanilla's
`00_situation_group_types.txt` marks `minor` as "referred to in code", and its only vanilla user,
the Silk Road, has no pin either. `natural_disasters` is not referred to in code and has only a
`sort_order`. Tests D and E are therefore unnecessary.

**Fix (applied later 2026-11-11, at Daniel's request with CK3 open; xTiger reports nothing new):** a mod group type, `kehillah_communal` (`sort_order = 50`, between `minor` and
`struggles`), in `common/situation/situation_group_types/kehillah_situation_group_types.txt`,
with `situation_group_type_kehillah_communal` loc, and the crisis moved to it. A mod group rather
than `natural_disasters`, so a pogrom isn't filed under natural disasters in the Situations list.
The decree and trial situations are also `minor`; whether they get pins is a separate choice. To
be confirmed after a restart: a group type change is unlikely to take effect on hot reload.

**Result after a restart:** Granada's crisis, now in `kehillah_communal`, still showed no pin,
including after its centre was moved to the county capital (probe `run\kehillah_pin_capital.txt`).
Daniel leads Granada, so he takes part in the crisis, and test C had no participants. The next
probe, `run\kehillah_pin_leave.txt`, removes the player, to test whether the engine hides the pin
of a situation the player is in. **Result: still no pin.** One difference remains: test C was
started fresh, while Granada's crisis was started before the group change, and the engine may
decide on a pin only when a situation starts. `run\kehillah_pin_fresh.txt` starts a new crisis in
an AI community beyond medium distance from the player, so the player is not a participant.
**Result: no pin on the fresh crisis either.**

**Conclusion (supersedes the `minor` reading above):** the engine draws situation pins only for
the vanilla group `natural_disasters`. Every situation that showed one was in that group (the
earthquake, tests A and C). Every one that didn't was in another: B in `minor`, and the crisis in
`minor` and then in `kehillah_communal`. Vanilla's zoom setting for the pins is even named
`NATURAL_DISASTERS_VISIBLE_ZOOM_STEPS` (`{ 0 19 }` in `00_graphics.txt`). So the crisis is now in
`natural_disasters`, and the `kehillah_communal` group and its loc are removed. The cost is that
the crisis is listed under vanilla's "Natural Disaster" heading in the Situations panel. Overriding
the loc `situation_group_type_natural_disasters` to a broader label would fix that, but it would
also rename vanilla's heading; that's left as Daniel's call. Vanilla's natural-disaster tutorial
checks situation *types*, so it isn't triggered by the crisis.

**Verified live (Daniel, later 2026-11-11):** after a restart, a fresh crisis in Rouen showed its
torch-and-pitchfork pin over Rouen, with the sub-region outlined in red. Daniel was not a
participant. The probes `kehillah_pin_capital` and `kehillah_pin_leave` are deleted;
`kehillah_pin_fresh` (start a new crisis far away) and `kehillah_crisis_join` are kept.

**Decree and trial (later 2026-11-11, at Daniel's request):** `kehillah_decree_situation` and
`kehillah_trial_situation` moved from `minor` to `natural_disasters` too. Both already set an icon
and a centre province (the new leader's quarter), so their pins should appear for any decree or
trial started after a restart. Not yet checked live.

**Pin lost on hot reload (later 2026-11-11):** that edit (23:07) hot-reloaded the crisis file in
Daniel's open game, and Rouen's pin disappeared. The group change itself hot-reloaded at 23:03,
before the Rouen crisis started. Open question, which matters for real play: does a pin come back
after a save is loaded? Tests: `run\kehillah_pin_recenter.txt` re-sets every crisis centre; then
save, reload and look again. If loading drops pins and re-setting the centre restores them, the fix
is to re-set the centre in the crisis's load-time or quarterly sync.

**Cleanup (later 2026-11-11):** the test types A–E, their loc, the copied icon and the probes
`kehillah_pin_capital`, `kehillah_pin_control_earthquake`, `kehillah_pin_test` and
`kehillah_pin_test2` are deleted. The probe `run\kehillah_crisis_join.txt` is kept.

## Change 1 (explained, not built)

`map_mode = sub_regions` would colour the crisis county red in vanilla's *situation* map mode.
The crisis now uses the default, `participant_groups`, and its groups have no colours. That mode
is reached from a situation window, and our crisis window has no button for it yet. It wouldn't
change the ordinary map. The Jewish strip's Community Crises map already covers that.

## Live-test checklist

1. Start a crisis in a community that has another Kehillah within medium distance. Use the crisis
   debug event, or play Granada with Córdoba or Lucena nearby.
2. As the neighbouring community's leader, open Situations. The crisis should be under *Your
   Situations*, and the participant list should show you under "Nearby communities".
3. **The pin:** does a situation pin appear over the threatened quarter on the ordinary map? Note
   whether it appears for the neighbour, for the threatened leader, and for an uninvolved
   character.
4. A distant community's leader should still see it under *Other Situations*.
5. After a quarter passes, a new leader of the neighbouring community should be listed in place
   of the old one.
6. `error.log` has nothing naming `kehillah_crisis_neighbour` or `kehillah_crisis_neighbours`.
