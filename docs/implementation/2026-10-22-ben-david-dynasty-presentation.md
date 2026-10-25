# Ben David dynasty presentation — 2026-10-22

**Status: IMPLEMENTED; source and xTiger checked; live UI verification pending.**

The Baghdad exilarch's dynasty 9000064 displays as **Ben David** instead of
"of the House of David," which CK3's dynasty phrasing localized awkwardly.
The dynasty now has a gold lion on blue and the motto "The scepter shall not
depart from Judah." The lion and line refer to [Genesis 49:9](https://www.sefaria.org/Genesis.49.9)
and [Genesis 49:10](https://www.sefaria.org/Genesis.49.10). These arms are a
modern gameplay emblem, not historically attested heraldry for the family.

The motto uses CK3's dynasty `motto` key, which the installed game's
`common/dynasties/_dynasties.info` says the founding house inherits. The coat
of arms uses a base-game lion emblem. This change affects presentation only;
it does not change any character, lineage trait, title history, or succession
script. A live game still needs to confirm the dynasty screen shows the name,
motto, and arms together.

This is a separate implementation unit from the sourced historical-character
roster in the 2026-10-22 research spike. Other family icons and mottos should
follow the roster's evidence and accuracy-caveat columns as characters are
implemented.

Validation on 2026-10-22: xTiger reported 0 fatal, 15 errors, 100 warnings,
1 untidy, and 38 tips, matching the unchanged branch baseline; it reported no
finding in the edited files. `git diff --check` passed. The delegated live
check could not run because the available tester reported it was not the Luna
model required by this repository. No CK3 process was launched or inspected
for this change. The dynasty-screen check remains pending.
