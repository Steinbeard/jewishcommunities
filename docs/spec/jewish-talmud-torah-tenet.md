# Talmud Torah tenet — 2026-10-13

**Status: Implemented in the separate development branch; source checked, live gameplay pending.** This is the first new Jewish tenet proposed in [v25's tenet mapping](v25-by-god-alone-adaptation-proposals.md). It changes the starting `rabbinism` rite and the existing Learn Torah loop; it does not create another activity or use the vanilla Scholar trait as its reward.

## Historical idea

Talmud Torah means Torah study as an ongoing religious duty of ordinary life, including the transmission of learning in a household. Maimonides' *Mishneh Torah*, Laws of Torah Study 1:1 and 1:8, describes teaching children and setting aside regular study even while poor, ill, or supporting a family ([1:1](https://www.sefaria.org/Mishneh_Torah%2C_Torah_Study.1.1), [1:8](https://www.sefaria.org/Mishneh_Torah%2C_Torah_Study.1.8)). The mod expresses a rite's communal emphasis on that ideal. Its broad player access is a gameplay choice; it does not claim identical medieval rules for every person's formal education or ordination.

## Implemented rules

- Replaces Rabbinism's third starting tenet, vanilla `tenet_pursuit_of_knowledge`, with `tenet_talmud_torah`. Legalism and Religious Legal Pronouncements remain in their vanilla slots. Any Jewish rite may select the new tenet on reform; non-Jewish rites may not.
- Grants +10% Scholar lifestyle XP to followers through a tenet character modifier. Diligent is a virtue and Lazy a sin. The tenet grants no Scholar trait or Rabbi trait.
- Extends the existing Learn Torah scheme to adult lay Jewish rulers and landless adventurers of a rite with the tenet, subject to its existing accessible-library, capacity, imprisonment, and scheme checks. The established rabbi and ordination-candidate route still works without the tenet. The scheme's descriptions no longer call every reader a rabbi; semicha tooltips appear only for actual ordination candidates.
- Mastering a new library work awards an additional 25 Piety and 50 Learning lifestyle XP. Rereading an already mastered work awards 10 Piety and 25 XP. An unmastered reading retains its baseline reward and gets no tenet bonus. The shared study effect covers both the continuous scheme and its journey variant; Rabbi trait XP remains separately guarded by possession of that trait.

The tenet hooks into the mod's library rather than generic Learning actions: the player must spend time on an actual work. Its passive lifestyle modifier also touches a vanilla system. This first pass does not yet reward childhood teaching or book donations, which would need their own balanced actions rather than a second reward for the same study completion.

## Compatibility and verification

The `rabbinism` rite override copies the installed CK3 1.20.1 definition except for the tenet swap, and therefore needs review after a game update. The tenet uses a vanilla icon and its own English text. `ck3-tiger` 1.19.0 reports `unknown token rite` through the touched gates and shared effect; CK3 1.20.1 uses `rite = { rite_has_tenet = ... }` in vanilla character triggers. No other touched-file findings remain. The console-only probes are `kehillah_talmud_torah_debug.1` (eligibility) and `.2` (Mishnah mastery in a disposable save). Live boot, tenet display, scheme availability, and reward resolution are still to be checked.

## Rabbi and semicha synergy — 2026-10-13 addendum

**Status: Implemented in script; source checked, live gameplay pending.** Daniel asked the tenet to help established rabbis grow and candidates study for semicha. Successful new-work study now adds 5 Rabbi trait XP in the work's own track to the existing 15; successful repeat study adds 2 to the existing 5. The added XP is still guarded by actual possession of `kehillah_rabbi_trait`. A lay reader or candidate without that trait receives none, and failed readings get no added trait XP.

The usual mastery check requires Learning 10 or a one-course intervention. A follower of Talmud Torah may instead master a work at Learning 8, the [v21 candidate-entry floor](v21-rabbi-ordination-paths.md#31-admission-to-study). This lets a Learning-8 or Learning-9 candidate earn the two real mastered works and distinct study fields needed for semicha. It leaves the two-work/two-field curriculum, Learning-8 readiness, faith and leadership eligibility, and study-hall institution untouched. The lower mastery floor applies to the shared library study effect used by the continuous Learn Torah scheme and the journey variant. Script values hold the 8, 5, and 2 tuning numbers.

`kehillah_talmud_torah_debug.1` now reports whether the lower mastery floor is met. `.3` resolves a natural Mishnah course on an unstudied Learning-8/9 test character; `.2` remains the forced-success reward probe. Run these in a disposable save because study alters the character's records and rewards.

## Rabbi as a virtue — 2026-10-13 addendum

**Status: Implemented in script; ck3-tiger checked, live display pending.** At Daniel's suggestion, Talmud Torah also names `kehillah_rabbi_trait` as a virtue, with weight 15. This supersedes the first rule above only as to the tenet's virtue list: Diligent remains a virtue and Lazy remains a sin. Semicha still requires its existing curriculum and institution; the tenet does not grant the Rabbi trait. The virtue expresses esteem for a recognized teacher, while Diligent keeps a virtue available to every lay learner. The Rabbi trait already grants base monthly Piety and same-faith opinion, so this virtue is an additional reward to review in the live tenet and character tooltips.

The first isolated boot of this addendum also exposed a pre-existing scheme-description error: the game expected `kehillah_study_torah_desc_general`, while the scheme and localization used a key with an extra `_scheme_`. Both now use the expected key. This is a presentation fix for the same Learn Torah scheme, not a change to its study rules.

## Live tooltip correction — 2026-10-15 addendum

**Status: Corrected and live tooltip verified.** This supersedes the passive modifier named in the first implemented rule. A Worms 1066 live tooltip showed that `lifestyle_scholar_xp_gain_mult` presents as **Religious Scholar Trait Experience Gain +10%** in CK3 1.20.1. It was the wrong modifier for our intended passive Learning lifestyle bonus. The tenet now uses `monthly_learning_lifestyle_xp_gain_mult = 0.10`, the key used by vanilla Learning traits. A fresh live tooltip displayed **Monthly Learning Lifestyle Experience +10%** and the existing work-mastery Piety, Learning XP, Rabbi XP, and Learning-8 rules. The tenet does not award a Religious Scholar trait.
