# V14: One Title Tier for Every Kehillah

Status: **built in script on 2026-09-20; manual live regression pending.** This
supersedes the county-tier choice for pre-authored communities in
[v1 §6](v1-kehillah-community.md) and [v7 §1](v7-minhag-geographic-tagging.md).
Their geographic and flat-title decisions remain in force. See
[ROADMAP.md](../../ROADMAP.md) for the current verification status.

## Decision

Every Kehillah is a flat, landless **duchy-tier** title. The fifteen 1066
communities use `d_kehillah_<place>`; Found a Jewish Community keeps the
duchy-tier runtime title produced by `create_adventurer_title`. The title's
capital points to its real host county, which remains in its vanilla
holder's hands. Rav/Parnas flavorization continues to mask the generic
"Duke" rank.

This implements the user's 2026-09-20 request for a consistent rank between
game-start and formed communities. CK3's `create_adventurer_title` has no
tier parameter, while `create_dynamic_title` rejects `tier = county`
(ck3-tiger and a live console probe with a duchy positive control). A
finite pool of pre-authored county slots was prototyped, then discarded
when the user chose duchy rank for all communities instead.

## Implementation and compatibility

The fifteen title IDs changed from `c_kehillah_*` to `d_kehillah_*` across
landed titles, title history, the Worms bookmark, localization, and all
script references. The existing founding effect is unchanged. The
government's `can_get_government` remains tier-agnostic and requires a
landless title; reintroducing a duchy-only gate caused a documented Game
Over in the 2026-09-20 playtest correction. The shared title definitions
remain flat rather than nested under regional duchies, so minhag lookup
continues to use the real host county's geography.

The changed IDs are a save compatibility break for campaigns started with
the old `c_kehillah_*` titles. Start a new campaign with this build.

## Portraits

The higher title rank should not make a communal leader look like a duke.
`gfx/portraits/portrait_modifiers/kehillah_clothing.txt` gives characters
with Kehillah government plain commoner clothing, no crown, and no cloak.
It selects Western, Northern, Byzantine, or MENA commoner clothing from
the character's clothing style, with a Western fallback. Its priority is
above ordinary rank attire but below religious and situational outfits.
Isaac's placeholder bookmark DNA also uses plain clothing so the start
screen does not show the borrowed royal costume. The user's manual
playtest will verify the bookmark and in-game portraits.
