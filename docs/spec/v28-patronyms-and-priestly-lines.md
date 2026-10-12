# V28: Patronyms and priestly lines — 2026-10-11

**Status: scripted for CK3 1.20 and ck3-tiger-checked; nothing here is live-tested yet. See "Unverified" below.**

Depends on [v27](v27-interfaith-marriage-and-descent.md) for the birth on_action that this extends. It
does not change any government, succession, or dynasty rule.

## What shipped

- **"ben"/"bat" patronyms.** All seven Israelite name lists (ashkenazi, sephardi, radhanite, bavlim,
  kochinim, romaniote, italki) in `common/culture/name_lists/kehillah_israelite_names.txt` set
  `patronym_prefix_male = "dynnpat_pre_ben"`, `patronym_prefix_female = "dynnpat_pre_bat"` and
  `always_use_patronym = yes`. Prefix text is in `localization/english/names/kehillah_patronyms_l_english.yml`.
  The patronym is taken from the character's father at runtime, so a character without a defined father
  shows none. Only two history files define parents (`granada_1066.txt`, `yitzhaki_anglia_anchor.txt`);
  1066 start characters will show no patronym until dead-father stubs are added.
- **Kohen and Levite seeded.** `kohen` and `levite` already passed father to son. They now carry
  `genetic = yes` (ck3-tiger and vanilla agree `random_creation` needs it), `random_creation = 0.05` / `0.04`
  (about the traditional share of the population), and `potential = { faith.religion = religion:judaism_religion }`.
  `kehillah_apply_jewish_descent_on_birth` strips both traits from a child who ends up outside Judaism.
- **Probe.** `events/kehillah_patronym_debug_events.txt`, `event kehillah_patronym_debug.1` on a selected
  character.

## Decisions

- **"Ben X" for everyone, not only the lowborn.** Restricting patronyms to lowborn characters would mean
  overriding vanilla's name-format strings globally, which also changes Norse, Arabic and Gaelic
  cultures. Not worth it. A house member's short name still uses the house, and full names show both.
- **No shared ha-Kohen / ha-Levi house.** It would make every Kohen kin to every other, misfire the mod's
  dynasty-based ties (ROADMAP ~1102, ~1824), and break the lowborn logic (ROADMAP ~372). Houses remain for
  notable families only. The trait itself marks ordinary lowborn Kohanim and Levites.
- **No nicknames for ha-Kohen / ha-Levi.** Nicknames print in the wrong position, in quotes, and some name
  formats drop the patronym; there is also only one nickname slot.
- **26 `dynn_Ben_*` pool entries removed** from the random dynasty-name pools (Ben_Aharon, Ben_Ari,
  Ben_Jeremias, Ben_Leonhard, Ben_Michael, Ben_Reuben, Ben_Sol, Ben_Shlomo, Ben_Shimon, Ben_Yitzhak,
  Ben_Yankev, Ben_Yosef, Ben_David, each in both the dynasty and cadet lists). None were defined dynasties.
  With patronyms on, they would print as "X ben Y ben Y". Bare patronymic-style names remain (`dynn_Binyamin`,
  `Mose`, `Ya_akov`, `Yeshayahu`, Radhanite `Yitzhak`/`Yaakov`/`Efraim`); they are less likely to double up
  and were left alone.

## Replacement dynasty names — 2026-10-11

61 historically flavoured family and toponymic names were added to the random pools (both dynasty and
cadet lists) in place of the removed `dynn_Ben_*` entries: 14 Ashkenazi, 10 Sephardi, 10 Radhanite, 8 Bavlim,
3 Kochini, 5 Romaniote, 11 Italki. Eight reuse vanilla's own localization (Landau, Trier, Balkhi, Basri,
Qazwini, Khorasani, Baghdadi, Mala); the other 53 are in
`localization/english/dynasties/kehillah_dynasty_pool_l_english.yml`. Some are later than 1066 (Ashkenazi
surnames especially; the existing pool already had Horowitz and Epstein), and the Kochini ones are place
names rather than attested families. Both are judgment calls, easy to prune.

## The Exilarch and "Ben David"

"Ben David" for an Exilarch is a claim of Davidic descent, not a father's name. As a random dynasty it would
duplicate the patronym of any Exilarch whose father was called David, and it would be handed to unrelated
characters. So it is gone from the pool. For the Babylonia content (ROADMAP Phase 2):

1. Individual Exilarchs get their patronym automatically ("David ben Zakkai"), provided the father character
   exists.
2. The line itself should be a **defined dynasty with an ID** in `common/dynasties/ha_levi.txt`'s range
   (next free after 9000060), named for the line rather than "Ben David" (for example a Bustanai house; the
   exact name is a historical call to confirm before writing it).
3. The Davidic claim should be a trait, flag or government feature on that line, not part of a name.

Update: the V29 work has since defined `dynn_BenDavid` ("of the House of David") as a real dynasty in
`ha_levi.txt`, which is the approach recommended above.

## Unverified (needs a live check)

- How the engine combines patronym and house for house members, and for nicknamed characters.
- Whether `random_creation` honours `potential`, and the real hit-rate of 5% / 4%.
- Whether underscore given names (`Dov_Ber`, `Shem_Tov`) render properly inside a patronym.
- That `faith.religion` is accepted inside a trait `potential` on 1.20.
- ck3-tiger (built for 1.19) reports the pre-existing `rite` and `set_character_rite` hits in the on_action
  file, none on the new block.

## Not built

A "Discouraged" intermarriage tier (a penalty rather than the v27 hard block) is still only a proposal. It
would need a custom `on_marriage` handler, since vanilla has no interfaith marriage penalty outside struggles.
