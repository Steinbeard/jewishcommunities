# Kohen and Levite: random_creation removed, game-start assignment instead

**Status:** BUILT 2026-11-15, xTiger clean on the touched files; **not live-tested.** Amends the
`random_creation` lines of [2026-10-18-jewish-lineage-traits.md](2026-10-18-jewish-lineage-traits.md)
and [v28-patronyms-and-priestly-lines.md](../spec/v28-patronyms-and-priestly-lines.md). Priestly
status still passes by descent and survives conversion (decision 2026-10-29).

## The bug

A woman met as an adventurer in a Granada tavern (Maliki, Andalusian) carried the Levite trait.
`levite` and `kohen` had `random_creation` (5 and 4) and a `potential = { faith.religion = ... }`
meant to keep them Jewish. `potential` does not hold: the CK3 Mod Co-op server reports (2025-11-16)
that after game start `potential` "doesnt block character from receiving traits at all", and no
vanilla trait uses `potential`. The one-time game-start sweep cannot reach characters generated later.

## The change

- `random_creation` removed from `kohen` and `levite` (`common/traits/kehillah_traits.txt`). With no
  random roll, nothing can hand the trait to the wrong person.
- New `kehillah_assign_priestly_traits_at_start_effect`
  (`common/scripted_effects/kehillah_priestly_trait_effects.txt`), called from the existing
  game-start sweep in `kehillah_apostasy_on_actions.txt` after the strip. It rolls 5% Kohen, 4% Levite
  for a living Jewish adult man who has neither trait, has **no recorded father**, and is **not authored
  in this mod's history files**.
- New generated trigger `kehillah_is_history_file_character_trigger`
  (`common/scripted_triggers/kehillah_history_character_triggers.txt`), built by
  `scripts/kehillah_generate_history_character_trigger.py` from every key in `history/characters/`.
  **Re-run the script after adding a history character**, or the new character can be rolled at start.

## Why "no recorded father"

The traits inherit down the male line at birth only. A start character with a father would otherwise
roll independently of the line he descends from. Generated start characters normally have no parents,
so they are the ones this reaches. Their already-born sons are not covered, since the sons have no
father either, and each rolls separately.

## Known gaps

1. **Characters generated after game start get neither trait.** Adventurers, travelling guests,
   courtier refills. Consequence: Jewish generated guests are never Kohen or Levite. Wanted: a hook
   that fires when a Jewish character is generated. No such on_action exists to my knowledge; the
   mod's own `create_character` calls could use a shared effect. Recorded in ROADMAP.
2. Vanilla's own history characters are not in the exclusion trigger, so a Jewish vanilla one without
   a father can be rolled.
3. Not live-tested. Suggested check: start the Worms 1066 bookmark, then run a probe that counts
   `kohen` and `levite` among living Jewish men, confirms no non-Jew has either (outside conversos), and
   confirms no character from `history/characters/` was changed.
