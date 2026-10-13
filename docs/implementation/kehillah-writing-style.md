# Player-facing writing

**Status:** Editorial guidance adopted for the 2026-10-09 writing pass, following
Daniel's request to remove fluffy and unnatural prose. Gameplay and historical
design remain governed by [ROADMAP.md](../../ROADMAP.md) and the relevant specs.

## Bet Din and responsa direction — 2026-10-09

Daniel extended this guidance to court cases and correspondence. Give each
litigant a concrete concern and distinguish a persuasive argument from a just
outcome. A learned judge should have more ways to reason, not a universal
button that makes every dispute disappear. Personality and complementary
skills on the bench should matter alongside personal book mastery.

Use the books as the library already represents them. A choice can require
Bavli Nashim while its hover text cites Gittin 45a. Short transliterated Hebrew
or Aramaic quotations use vanilla's `Glossary()` markup, with a translation,
precise citation and any qualification needed to avoid presenting a disputed
interpretation as settled law. Quotations must support the actual argument.

A responsum is a named scholar's advice on a specific question. The recipient
needs an interesting choice about the answer and the work it demands; the
asking court retains responsibility for adopting or rejecting it. Historical
sources inspire fictional cases, which must not be presented as transcripts
of documented medieval proceedings.

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

## Follow-up editorial pass — 2026-10-12

Revised 227 English entries across the main Kehillah, community goal,
responsa, bookmark and Norman settlement files. The heaviest edits replace
generic verdicts and repeated claims of importance with the question heard,
the choice made and the result. The ten translation offers and endings now
name the requested work without repeating the same dramatic refrain.

The dowry dispute's two named options previously described rulings for the
opposite families from the opinion effects in the event script. Their wording
now matches the favored party. The compromise also no longer claims the
community chest pays toward the dowry; its script changes Stability only.

The five files retain their keys and UTF-8 BOMs, and their edited entries
have balanced bracket references and formatting. `git diff --check` passed.
`ck3-tiger` reports no findings in the edited localization files. Its
whole-mod output remains noisy (668 errors and 126 warnings), with a version
warning because the installed validator targets CK3 1.19.0 and the installed
game is 1.20.0.4. No live rendering test was performed for this text pass.
