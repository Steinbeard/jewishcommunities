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
