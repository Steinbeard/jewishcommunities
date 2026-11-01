**Status:** Implemented in the main worktree, 2026-10-29; source audit and
xTiger checked. No live test performed. Completes missing adult personalities in
the fixed roster described in
[the family implementation](2026-10-23-historical-families-and-seeding.md) and
[the Granada revision](2026-10-29-granada-chain-rewrite.md).

# Fixed adult personalities

Daniel asked whether every character should have three personality traits and
requested missing traits be filled. Three is the normal adult target, not a
hard engine requirement. The installed 1.20.1.2 `game/common/defines/00_defines.txt`
sets `RANDOM_PERSONALITY_TRAITS_BASE = 3`, `RANDOM_PERSONALITY_TRAITS_SPAN = 0`,
`HISTORY_CHILD_PERSONALITY_TRAITS = { 9 11 13 }`, and
`INTENDED_MAX_PERSONALITY_TRAITS = 6`. Thus children with fewer traits are normal,
and six is an error threshold, not a target. Education, Rabbi, poet, intellect,
lineage and other non-personality traits do not count toward the usual three.

The audit reads the installed trait definitions (`category = personality`) and
counts only those traits. Of the 201 custom history entries, 109 definitions with
`disallow_random_traits = yes` had fewer than three personalities. Eleven are
children at their authored start and remain untouched; the remaining **98 adult
definitions receive 259 traits**, bringing each to exactly three. All existing
personality and non-personality traits are preserved. Adults already dead at a
bookmark are included when their fixed historical profile was incomplete.

These additions are **editorial gameplay characterization**, not newly attested
biographical facts. Existing roles and personality traits guided the choices;
they are not universally positive scholar/merchant profiles. Examples: Yoseph
retains Ambitious and Arrogant and gains Diligent; Samuel gains Brave; Abu Ishaq
retains Zealous and gains Wrathful and Stubborn. No personality is inferred from
faith, culture or ancestry alone.

The other 92 definitions retain their existing policy: one already has three
fixed personality traits; 91 do not disable random traits. In particular,
[V51](../spec/v51-bookmark-rosters.md)'s deliberate decision to leave named
bookmark personalities unspecified remains in force, as do the representative
world roster and library-author credits. This pass does not claim that all 201
characters have three explicitly written traits or that an existing save changes.
History changes apply to new campaigns. The eleven children are left to normal
childhood progression rather than being assigned adult personalities now.

## Source and validator checks

- All 98 changed entries have three distinct personality traits recognized by the
  installed game; none contains an opposite pair.
- All 103 other character definitions are unchanged. Removing just the added
  personality assignments reproduces the original character tokens, confirming
  preserved names, dates, kinship, faith, culture, education and court placement.
- Whitespace checks pass. xTiger reports the same 0 fatal, 15 errors, 103 warnings,
  1 untidy and 43 tips as the baseline; no new finding.
- This is a static roster pass, with no government, succession or title changes.
  Live rendering remains unrun for the separate poem scene.

## Authored additions

The table records additions only; the existing traits remain in each history file.

| ID | Name in history | Added personality traits |
|---|---|---|
| 9000201 | Shlomo | humble |
| 9000216 | Joseph | diligent |
| 9000219 | Isaac | stubborn |
| 9000221 | Labrat | generous |
| 9000230 | Samuel | brave |
| 9000231 | Elyasaf | humble, shy |
| 9000232 | Nissim | diligent |
| 9000233 | Hannah | brave |
| 9000235 | Abu_Ishaq | wrathful, stubborn |
| 9002000 | Yitzhak | honest, temperate |
| 9002001 | Sarah | generous, gregarious |
| 9002002 | Yitzhak | calm, content, honest |
| 9002003 | Simeon | gregarious, generous, fickle |
| 9002004 | Rivka | shy, forgiving |
| 9002008 | Samuel | humble, diligent, stubborn |
| 9002009 | Meir | ambitious, temperate |
| 9002010 | Judah | shy, honest, stubborn |
| 9002011 | Nathan | calm, just, content |
| 9002012 | Jacob | ambitious, generous |
| 9002013 | Esther | compassionate, trusting |
| 9002014 | Isaac | diligent, greedy, patient |
| 9002015 | Joseph | gregarious, honest, ambitious |
| 9002018 | Baruch | temperate, just, stubborn |
| 9002019 | Isaac | patient, humble |
| 9002020 | Moses | patient, diligent, brave |
| 9002021 | Enoch | zealous, diligent, stubborn |
| 9002023 | Isaac | just, stubborn |
| 9002024 | Moses | calm, honest, content |
| 9002025 | Jacob | shy, temperate, diligent |
| 9002026 | Yehuda | compassionate, humble |
| 9002027 | Yaakov | gregarious, diligent |
| 9002028 | Hushiel | diligent, generous, zealous |
| 9002029 | Hananel | patient, just, stubborn |
| 9002030 | Miriam | gregarious, compassionate |
| 9002032 | Elhanan | calm, content, generous |
| 9002033 | Shemariah | diligent, zealous, patient |
| 9002034 | Jacob | shy, honest, humble |
| 9002035 | Moses | just, temperate, stubborn |
| 9002036 | Levi | calm, diligent, content |
| 9002037 | Judah | ambitious, impatient, honest |
| 9002038 | Jehiel | patient, generous, humble |
| 9002039 | Daniel | shy, diligent, stubborn |
| 9002040 | Nathan | generous, gregarious |
| 9002041 | Abraham | ambitious, gregarious, fickle |
| 9002042 | Shabbethai | honest, patient, content |
| 9002043 | Kalonymus | gregarious, generous, eccentric |
| 9002044 | Moses | zealous, just, calm |
| 9002045 | Tobiah | diligent, humble, stubborn |
| 9002046 | Eliezer | patient, compassionate, temperate |
| 9002047 | Nahray | honest, patient |
| 9002048 | Arus | gregarious, ambitious, temperate |
| 9002049 | Ali | generous, stubborn |
| 9002050 | Yaqub | diligent, greedy, calm |
| 9002051 | Daniel | just, temperate, stubborn |
| 9002053 | Hezekiah | ambitious, just, brave |
| 9002054 | David | gregarious, ambitious, brave |
| 9002055 | Yitzhak | patient, diligent, shy |
| 9002056 | Yehuda | ambitious, diligent, gregarious |
| 9002057 | Daniel | patient, generous, content |
| 9002059 | Faraj | gregarious, greedy, patient |
| 9002060 | Rivka | honest, impatient, generous |
| 9002061 | Saadia | temperate, just, stubborn |
| 9002062 | Miriam | calm, content, compassionate |
| 9002063 | Bundar | diligent, gregarious, ambitious |
| 9002064 | Yefet | impatient, honest, ambitious |
| 9002065 | Avraham | shy, diligent, stubborn |
| 9002067 | Nathan | gregarious, patient, honest |
| 9002070 | Bodo_Eleazar | stubborn |
| 9002071 | Hugo | calm, honest, brave |
| 9002072 | Bertha | content, generous, trusting |
| 9002073 | Alvaro | diligent, stubborn |
| 9002074 | Ahimaaz | gregarious, generous, eccentric |
| 9002075 | Paltiel | patient, diligent, ambitious |
| 9002076 | Solomon | generous, shy, stubborn |
| 9002077 | Hasdai | ambitious, gregarious, diligent |
| 9002078 | Isaac | calm, patient, temperate |
| 9002079 | Joseph | zealous, humble, stubborn |
| 9002080 | Mazliah | just, patient, temperate |
| 9002081 | Joseph | diligent, ambitious, calm |
| 9002082 | Joab | content, generous, honest |
| 9002083 | Amram | gregarious, ambitious, impatient |
| 9002084 | Isaac | patient, greedy, diligent |
| 9002085 | Isaac | shy, honest, zealous |
| 9002086 | Reuben | content, calm, trusting |
| 9002087 | Yaqqar | zealous, generous, stubborn |
| 9002088 | Samuel | honest, calm, content |
| 9002089 | Natan | honest, humble |
| 9002090 | Hanukkah | diligent, ambitious, patient |
| 9002091 | Yaakov | content, gregarious, generous |
| 9002092 | Hanukkah | patient, temperate, stubborn |
| 9002093 | Joseph | diligent, honest, ambitious |
| 9002094 | Yahya | gregarious, impatient, generous |
| 9002095 | Judah | patient, greedy, diligent |
| 9002096 | Abraham | content, calm, honest |
| 9002097 | Bahya | humble, temperate |
| 9002098 | Joseph | just, patient, stubborn |
| 9002099 | Judah | zealous, humble, diligent |
| 9002100 | Samuel | calm, honest, content |
