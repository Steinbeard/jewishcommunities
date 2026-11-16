# Rashi and Western Jewish men's hair

**Status: Built 2026-11-15; source validated, live portrait check blocked by process access.**

Rashi's 1066 character DNA and Troyes bookmark portrait now use the
vanilla `mena_hairstyles_straight` template at value 150. That template's
third option is `male_hair_western_07`, a longer side part. The previous
`western_hairstyles_straight` value 79 selected `male_hair_western_01`,
the blunt bowl cut visible in the reported portrait.

A game-only portrait modifier at priority 1 gives Jewish men with Western
clothing and straight hair the same MENA straight pool, whose options
exclude `male_hair_western_01`. It retains short and long alternatives,
including the Western side part; other religions, female portraits,
and other hair types retain their ordinary selection. Religious and
situational hair rules have later priority and can still take precedence.
Barbershop customization and explicitly saved portrait changes are not
restricted. This is a visual preference for this mod, not a historical
claim that medieval Jewish men never wore a similar cut.

The installed CK3 1.20.1.2 gene definitions and portrait priority rules
were checked. xTiger before and after: 0 fatal, 25 errors, 109 warnings;
no new diagnostic. The game must be restarted to load portrait definitions,
and existing saves may retain DNA or barbershop choices already stored.
The delegated live check could not inspect CK3 process ownership because
the Windows CIM query was denied, so it did not control a game instance.
Git staging likewise failed because `.git/index.lock` could not be created
(permission denied); these files remain uncommitted in the shared worktree.
