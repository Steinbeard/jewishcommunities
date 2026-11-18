# Writing a Sefer live check — 2026-11-18

**Status: PARTIAL LIVE CHECK; ordinary path and artifact fix verified, landmark/save check unrun.** Daniel explicitly requested a Terra tester for this session, overriding the repository's usual Luna-only rule. The tester used the shared checkout and isolated CK3 profiles. It inspected process ownership before launch and stopped only its own processes.

## First boots

- First fresh boot failed to reach a useful writing test. `error.log` reported missing UTF-8 BOMs for the three new writing localization files and unrecognized writing event/manuscript keys. The files and generated writing outputs now carry BOMs. A second fresh boot reached the menu without those errors.
- In fresh 1066 Rashi, the Write a Sefer decision showed a magenta `NOT_has_variable_trigger` missing-localization error. At 130% UI scale its panel extended below a 1920×1080 screen; 100% scale made the button accessible. The requirement now uses a labeled custom tooltip; the scale behavior still needs review.

## Ordinary Talmud commentary

- L1 showed Parshanut 30, Talmudics 34 and Machshavah 40 aptitude. Talmudics L2 offered a Bavli order commentary, Yerushalmi order and halakhic treatise. Choosing Bavli commentary deducted 75 Piety and began a personal scheme.
- The scheme showed 91% success and “7 months until completion.” A phase finished, then the same timer returned for the next phase, so that native label describes a phase rather than the full multi-phase project. Research, a chavrusa choice, objections and a long revision all rendered. Choosing Yitzhak as chavrusa raised visible success from 91% to 95%.
- Ordinary completion on 26 November 1068 named *Glosses on the Bavli* in the event and later news. The manuscript existed with Rashi as holder and creator, but its inventory title was blank and its description said “An original manuscript of .” The artifact now receives direct form-specific localization at creation instead of an empty artifact-scope custom lookup; a retest must verify it.
- The “Word of Your Book Spreads” option exposed a long list of individual rabbis' XP gains and ran offscreen. Nearby-news effects are now hidden behind a short summary tooltip. The test did not independently verify ledger absence, save/reload, or a landmark outcome.
- No new writing-related post-boot errors appeared in `error.log` during this run. The orphaned console-only debug event warning was present at boot.

## Adjacent event observed

An unrelated *Targum Pseudo-Jonathan* controversy twice showed Rav Isaac of Worms as the second portrait while saying no single critic or scholar had emerged. The event's portrait used a saved scope while its custom text tested that scope from character localization. The event now sets short-lived character markers for the text conditions; this also awaits live retest.

## Targeted retest

In a third fresh isolated boot, the decision requirements displayed readable cooldown and active-project conditions without magenta debug text. The ordinary writing news tooltip was compact and explained nearby sharing without enumerating every recipient. A loaded writing save again reached ordinary success and correctly named *Glosses on the Bavli* in news. The artifact inventory now listed *Glosses on the Bavli*, its description repeated that title, and Rav Shlomo was shown as creator and holder. The retest log had no writing-specific runtime errors. The controversy marker change made its critic sentence fire, but the scoped critic name then rendered as a literal `ERROR` (three related runtime localization errors); the text has been made generic while the portrait still identifies the person. That final wording has not yet been retested. A separate vanilla social event about Rashi and his father also sounded implausible but was unrelated to the mod writing flow.

## Remaining checks

Verify the corrected decision requirement, ordinary manuscript title/description after creation and reload, compact local-news tooltip, actual absence of a new ledger entry, and one landmark route's tenet gate, author, mastery, manuscript and commentary reception. Compare `error.log` with each fresh boot baseline.
