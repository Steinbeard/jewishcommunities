**Status:** Built on 2026-10-23; source and xTiger checked. The live UI check is pending because another CK3 process was already running, and was left untouched.

# Community rites and realm Jewish-policy map modes

This addition to the V12 map view gives the player two more views, reachable from the existing
map-mode controls:

- **Community Rites** paints only each registered Kehillah's occupied barony by its leader's
  current rite. Rabbinism, Minhag Ashkenaz, Karaism, Samaritanism and Kabarism have distinct
  colors; other Jewish rites use a shared fallback. Unoccupied baronies stay neutral so regional
  minhag geography is not mistaken for a community's actual rite.
- **Jewish Settlement Policy** paints each county's baronies according to its de facto top liege's
  primary-title policy: banned, discouraged, allowed or encouraged. A missing value is Allowed,
  matching the V16 policy triggers. Unheld counties stay neutral.

Both views use CK3's existing `baronies` color mode and the color-carrier titles from V12. Painting
recolors baronies in save state, as the original community map does. Colors refresh when the player
chooses a view; a subsequent rite or policy change is reflected the next time that view is opened.
The existing Community map, its roster, and its regional tint meaning remain unchanged.

The realm policy shown is the top liege primary title's policy, which is the value consumed by the
settlement-policy triggers. It describes the realm-wide stance and does not replace a community's
individual Host Charter.

## Addendum, 2026-10-28: the policy map in play

Daniel opened the policy map from the realm view and found it confusing ("a weird map view").
Four causes, all fixed:

1. **Its widgets were never created.** The rite and policy banners and the row of buttons
   between the three Jewish maps were defined in `gui/kehillah_community_map_view.gui` but never
   listed in `gui/scripted_widgets/kehillah_scripted_widgets.txt`. The banner read "Showing:"
   with no name, and nothing led back to the other maps. All three are now registered.
2. **No legend.** A colour key (Encouraged, Allowed, Discouraged, Banned, No policy) now sits
   above the map-mode buttons.
3. **No hover.** The map mode has a `barony_description`: county, realm, ruler, and policy.
4. **Everything was green.** In 1066 nearly every realm is Allowed, so this is mostly correct.
   But a ruler who can't set a policy (a Jewish or communal ruler) was painted Allowed too. They
   now get the grey "No policy" colour, and the hover says why.

Since 2026-10-28 the policy is a realm law ([note](2026-10-28-jewish-settlement-law.md)). The
map reads it through the same band triggers.
