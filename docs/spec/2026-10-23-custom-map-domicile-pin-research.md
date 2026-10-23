# Domicile pins and custom map modes

**Status:** Research, 2026-10-23. No working custom-mode overlay demonstrated. A native-mode recolouring prototype passed static validation; its live rendering check was blocked before campaign entry. No runtime changes ship with this note.

Updates the feasibility discussion in [the September spike](spike-domicile-map-visibility.md) and [the October navigation note](2026-10-13-faith-map-navigation-and-nusach.md). Does not approve replacing vanilla Landless Rulers. Requested by Daniel ahead of the unrelated Near-term TODO queue.

## Established evidence

- Daniel's October 23 comparison showed Kehillah portrait pins in vanilla Landless Rulers at distant zoom, and no pins in Jewish Communities even at close zoom. Research commit `240c0a3` records this in `docs/testing/2026-10-23-domicile-pins-live-playtest-log.md`. The September claim that Kehillah domiciles do not qualify no longer describes the current game.
- Adding custom-mode visibility to `landless_rulers_map_widget` did not work. Vanilla's widget already lacks a GUI map-mode gate. Visibility cannot establish that the engine creates the parent and supplies its data.
- A province-icon prototype appeared in Details view but not the custom map's tested paper-map views. See [the October 14 live check](../testing/2026-10-14-map-visibility-live-test.md). Repeating it is not a new solution.
- Installed CK3 1.20.1.2 defines `landless_rulers` at `game/gfx/map/map_modes/map_modes.txt:4560`, using `color_mode = selected_character_realms`. Our custom key uses `color_mode = baronies`. Mode identity and colouring algorithm are separate fields.
- `game/gui/map_icon_layer.gui:944` defines the native pin widget. Its normal-play branch uses `LandlessRulersMapIcon.GetValidDomicilesCount`, `GetFirstValidDomicileIndex`, `GetFirstValidDomicile`, and `GetDomiciles`. No configurable pin-source field was found in installed map-mode definitions. That search does not exclude undocumented hooks.

These results suggest a native mode-specific decision controls pins. They do not isolate the mode key from colouring or selection behavior, or prove every custom GUI approach impossible.

## Next experiment: native identity, community colours

Keep the key `landless_rulers`, replace its definition with the body of `kehillah_communities_map`, and have the Communities button paint the baronies before selecting `landless_rulers`. This tests whether the known pin-producing mode retains pins with our regional colours.

The isolated prototype used `origin/master` at `a454bd7`:

1. Copy installed `game/gfx/map/map_modes/map_modes.txt` into the same mod-relative path. Replace only its complete `landless_rulers` block with the existing custom map block, renamed to `landless_rulers`. Keep the original custom-mode file.
2. In `gui/kehillah_community_map_view.gui`, change the eight quoted map-key uses from `'kehillah_communities_map'` to `'landless_rulers'`. Keep the paint action, roster variable and localization key. This is diagnostic navigation: the native banner may overlap the custom header.
3. Enter isolated Worms 1066, open Communities from Faiths, and verify BOTH community colours and multiple Kehillah pins at strategic and close zoom. Hover/click a pin and compare runtime errors against the pre-interaction baseline.

No `map_icon_layer.gui` override is needed. Vanilla's debug GUI documents console command `Dockables.Create GameMapModeSelector` at `gui/debug/debug_menus.gui:368`; this provides a fallback to guessing button coordinates, but the existing paint effect must still run first.

The prototype was removed after the blocked test. Recoverable local copies are at `C:/Users/Daniel/.codex/ck3-test/native-community-pins/prototype/`.

### Tradeoffs if it works

This repurposes vanilla Landless Rulers globally. Its normal button would open the recoloured definition too, potentially without first painting the communities. Its native population also includes unrelated adventurers. Production adoption needs a decision about that replacement, navigation/labels, refresh behavior and compatibility with other map-mode mods. It is not a transparent overlay on our independent custom key.

If preserving the native map is essential, a further discriminating experiment is the reverse: retain the custom key but copy vanilla's colour/selection definition. A pass would show the key alone is not the restriction; a failure would strengthen, not prove, the native-key hypothesis. Neither outcome alone delivers community colours plus pins under the custom key.

## Validation

xTiger baseline: **0 fatal, 8 errors, 77 warnings**. Prototype: **0 fatal, 8 errors, 79 warnings**. Added warnings are `duplicate-field` findings in the copied vanilla court-language tooltip and copied community tooltip. The eight errors are unchanged. `git diff --check` passed.

The Luna delegate launched its isolated profile and confirmed mod mounting, but another CK3 test occupied the only available display. No campaign or map was inspected. See [the actual attempt](../testing/2026-10-23-native-community-pins-live-test.md). Static validation and mod mounting do not confirm pin/colour coexistence.

Installed-source SHA-256:

- `gfx/map/map_modes/map_modes.txt`: `FEB28BBD29604CDA4AEAE2AC31E99F44FA4092B2DE163F765B219A8E7775B115`
- `gui/map_icon_layer.gui`: `29BF7A31B79614D154DC55B71FA998470220DE7FD0FE54CE95C7C061AE6769D8`
