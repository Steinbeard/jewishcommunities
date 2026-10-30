**Status:** source research and implementation proposal, 2026-10-30; no situation code or live test yet. Depends on the uncommitted [Community Safety build](../spec/2026-10-30-community-safety-and-crisis.md) in the main checkout. This note does not supersede its mechanics.

# Community crises as CK3 situations

## Finding

CK3 1.20.1.2 can create multiple instances of one situation type at runtime. The installed `natural_disaster_earthquake` is the relevant example: `is_unique = no`, `start_situation = { type = natural_disaster_earthquake save_scope_as = situation }`, `set_situation_center_province`, and `situation_sub_region:disaster_area = { add_dejure_title_to_sub_region = scope:epicenter_county }`. Its sub-region starts empty and receives counties after creation. A Kehillah crisis could use one instance centered on its domicile county. This is an installed-source inference, not a demonstrated Kehillah runtime result.

Situations have native phases, participant groups, a Situations-list entry, a map pin and a window. Their type chooses `gui_window_name`; `window = situation` supplies the generic situation GUI functions. Phase transitions can use durations or catalyst points. `end_situation = yes` deletes an instance from situation scope. The generic window displays phase progress, prospective phases and participants; it does not know the existing Community Safety preparation controls.

## Fit with the current build

| Current crisis feature | Situation fit | Consequence |
| --- | --- | --- |
| One warning for one community title | One non-unique instance with one dynamic county sub-region | Save the situation reference on the title and the title reference on the situation; do not look it up by type, since multiple crises can run. |
| Warning, armed, judgment, recovery stages | Native phases are possible | The current title variables, preacher story and delayed relays already drive transitions. Making phases authoritative now would create two clocks. Initially mirror title state and advance phases only through a tested bridge. |
| Preparations, petitions, agitation and outbreak roll | Existing title variables and scripted GUI | Keep the Military dashboard as the action surface. A native situation window would need a custom `gui_window_name` or a navigation link to expose these controls. |
| Host, leader and agitator | Participant groups | Automatic participation depends on realm/domicile and can change after succession or movement. Test explicit eligibility; an agitator may need manual participation. |
| Map and HUD presence | Built-in situation pin/list/HUD | These are player-visible additions, not just an internal state container. Test whether simultaneous nearby crises clutter the map or Situations list. |

The situation should *not* replace `story_kehillah_preacher` or `story_kehillah_mob` in the first slice. Those stories currently schedule weekly agitation and four-day march/siege ticks, including early death and arrival paths. The 76-day Granada warning and shortened warnings also make a single fixed situation duration unsuitable. Keep the title-owned incident epoch and cleanup guards while testing the new object. An old save without a situation must continue through the existing title/story route; migration can add a mirror instance at a quarterly check only after its creation and cleanup behavior is proven.

## Small implementation spike

1. After the active Military build is on a feature branch, add `common/situation/situations/kehillah_crisis_situation.txt` with `is_unique = no`, one empty sub-region and minimal warning/armed/judgment/recovery phases. Use a dedicated situation group and a temporary generic window; leave the existing Military tab intact.
2. Add console-only debug events to start a situation for a selected community's domicile county, save reciprocal references, log instance identity and center, and end exactly that instance. Start two different communities, including one in the same realm. Repeat after save/reload. Check whether separate instances and their title references survive and whether ending one leaves the other intact.
3. Test participant membership for the non-landed leader, the actual host sovereign and the agitator; test title succession and host change. Test the map pin, Situations list and HUD with two active crises. A generic window is acceptable for this spike only.
4. If the object behaves, wire creation to the existing warning/armed entry effects and deletion to the existing final cleanup, guarded by the incident epoch. Then test every early resolution, Granada checkpoint, strike, recovery, succession and old-save path against the current crisis test matrix. Only then consider moving phase timing or UI into the situation system.

Use xTiger before the live probe and compare against the checkout's baseline. A Luna tester must perform all CK3 interaction under the repository's process-ownership rules. Source review alone cannot establish that dynamic sub-regions, participation, save identity or the native UI work for a Kehillah.

## Source anchors

- Installed game: `game/common/situation/situations/_situations.info` (region, participant, phase and GUI schema).
- Installed game: `game/common/situation/situations/tgp_natural_disaster.txt` and `game/common/scripted_effects/10_dlc_tgp_natural_disaster_scripted_effects.txt` (non-unique instance and dynamic county region).
- Installed game: `game/events/situation_events/tgp_natural_disaster_events.txt` (`end_situation`).
- Installed game: `game/gui/window_situation_list.gui`, `game/gui/map_icon_layer.gui`, `game/gui/hud.gui` (native presentation).
- Mod working copy: `common/story_cycles/kehillah_mob_story_cycle.txt`, `common/scripted_effects/kehillah_crisis_effects.txt`, `gui/kehillah_crisis_military.gui` (existing scheduling, state and action surface).
