# Player-facing writing

**Status:** Editorial guidance adopted for the 2026-10-09 writing pass, following
Daniel's request to remove fluffy and unnatural prose. Gameplay and historical
design remain governed by [ROADMAP.md](../../ROADMAP.md) and the relevant specs.

Describe what people do, what they want, and what the player can choose. Keep
Jewish terminology and concrete details of communal life; explain unfamiliar
roles through their duties.

- Give an event a specific situation. A candle gutters; a bailiff demands a
  payment; a pupil asks a question. Avoid listing several possible scenes as
  though they all occurred.
- Let the situation carry its importance. Cut closing aphorisms, vague claims
  about lasting significance, and repeated qualifiers such as "real", "own",
  "genuine", and "not a small thing".
- Keep warmth, humour and tension where the scene supports them. Avoid a
  narrator who continually judges the player's choices or explains how to feel.
- State choices as actions and describe their consequences plainly. Do not
  imply extra rewards, follow-up events, or library unlocks that the script
  does not provide.
- Describe buildings by their use and visible features. Keep requirements and
  gameplay information distinct from atmosphere.
- Preserve localization keys, valid scopes, formatting and Hebrew terms.
  Prefer removing an unnecessary historical assertion to adding an unverified one.

The initial pass revised 130 entries in the main Kehillah and holiday English
localization files. It covers buildings, officers, selected decisions and event
chains, and all eight holiday events. This is an editorial pass through those
areas, not a historical audit or a claim that all localization has been revised.

Validation on 2026-10-09: all 130 replacements preserve the existing keys,
encoding and valid reference expressions; markup is balanced. A snapshot
comparison confirms unrelated working edits were preserved. `ck3-tiger` reports
no findings in either edited localization file. Whole-mod results were
0 fatal / 581 errors before and after, with warnings reduced from 119 to 103;
the installed validator targets 1.19.0 and warns about the installed 1.20.0.3
game. This does not establish a clean whole-mod build. No live rendering test
was performed for this text-only pass.
