# Jewish map modes in the Faith strip — 2026-10-29

**Status:** Implemented 2026-10-29 at Daniel's request; xTiger-checked; live visual check pending.
Supersedes the "No vanilla GUI file is copied into the mod" line of
[the faith map navigation note](../spec/2026-10-13-faith-map-navigation-and-nusach.md) and
[v12](../spec/v12-community-map-view.md)'s "do not fork `gui/shared/mapmodes.gui`" advice, for
the map-mode buttons and banner name only. The rite and policy map modes themselves are
[the 2026-10-23 note](../spec/2026-10-23-community-rite-and-realm-policy-maps.md)'s.

## What Daniel saw

- The banner's "Showing:" line had no map-mode name under it in our modes. Our separate text
  widget sat on top of "Showing:" and outside its background, unlike every vanilla mode.
- The Community Rites and Jewish Settlement Policy buttons only appeared after clicking the
  Jewish Communities button, and each click moved the buttons around: the selected mode's
  button was hidden, so the row closed up and shifted.
- The rites map had no map hover text, and the two new button tooltips were one line each.

## What changed

The mod now carries a full copy of vanilla `gui/shared/mapmodes.gui` (1.20.1.2). The vanilla
copy is its own commit, so the next commit's diff is exactly the mod's change. Every change is
fenced by `JEWISH COMMUNITIES MOD` comments:

- **Faith strip.** `faith_mini_map_mode` stays visible in the mod's three modes as well as the
  three vanilla ones. After Faiths, Holy Orders and Clerical Regions it has a fixed group of three
  Jewish buttons: Jewish Communities (menorah), Community Rites (book and candle,
  `known_faiths.dds`) and Jewish Settlement Policy (charter and quill, `feudal_contract.dds`).
  All three are always shown, in the same place. The selected mode glows and stays pressed, as
  vanilla's do. The Jewish Communities button keeps its three states: open, hide the ledger, and
  reopen the ledger.
- **Why a separate group.** The group hangs off a zero-width widget, so the three vanilla buttons
  stay centred where `hud_bottom.gui` puts the holy-site/religious-head selector above Faiths.
  It has the strip's own background, so it reads as a second, Jewish section of the Faith family.
  The group is hidden when no community is mirrored onto the player, for example in a game with
  no Kehillah or in the multiplayer lobby.
- **Banner.** `flowcontainer_map_mode_header` has the three mod names, so they sit under
  "Showing:" on vanilla's background.
- **Removed** from `gui/kehillah_community_map_view.gui` and its scripted-widget registrations:
  the old toggle, the second copy of the Faith strip, the three overlay names and the extra button
  row. The roster, its minimized header and the policy legend stay there.

Hover text: the rites map now has a `barony_description`, which names the community, its county,
its leader and the leader's rite. To support it, `kehillah_paint_community_rites_map_effect` tags
each host barony with `kehillah_map_community`, as the communities paint does. The policy hover
uses the same layout, with a fallback for a county with no holder. The two `_desc` keys are the
buttons' tooltips, as for vanilla modes, and now list every colour.

## Addendum: shown to every player (2026-10-29)

The Jewish group was gated on `kehillah_map_view_count > 0`, which a non-Jewish player only gets
after the first quarterly pulse (and only if communities exist), so the buttons looked missing.
Daniel asked for them for everyone, since the strip is hard to find anyway. The group is now
visible for any player in a game (`IsInGame`, `GetPlayer.IsValid`). The Jewish Communities
button's paint scripted_gui also runs `kehillah_refresh_map_view_effect`, so the ledger is fresh
on first click. The "hidden when no community is mirrored" line above is superseded. Not yet
checked live.

## Cost of the copy

After a game patch, recopy vanilla `mapmodes.gui` and re-apply the fenced blocks. Another mod that
replaces `mapmodes.gui` will conflict with this one, and whichever loads last wins. That is the
same kind of risk as the mod's existing copies of `window_character.gui`,
`window_county_view.gui`, `window_my_realm.gui` and `window_domicile.gui`.

## Still to check live

- The Jewish group is clickable even though it sits outside its zero-width parent's bounds.
- The holy-site selector still sits above Faiths.
- The names sit under "Showing:".
- The two new hovers show real text.
- `error.log` stays clean after hovering.
