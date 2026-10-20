**Status: Implemented, source-checked, and live-verified on 2026-10-18; statistical generated-character frequency and paternal inheritance still require a dedicated probe.**

# Jewish lineage traits

Daniel requested a Davidic lineage marker modeled on vanilla's Sayyid trait, a succession benefit for that lineage, and an audit of generated Kohanim and Levites.

## Ben David

`ben_david` follows the mechanical shape of vanilla `sayyid`: it is a fame-category trait inherited with certainty through the publicly acknowledged father by sons and daughters. Its female display name is *Bat David*. It gives +5 Jewish opinion and vanilla's initial-legitimacy boost, and costs 25 points in the Ruler Designer. It is not randomly generated and is not removed by conversion; it records a lineage claim rather than current religious observance. Its dedicated `ben_david.dds` asset reuses vanilla's Sayyid artwork under the trait-key filename CK3 expects.

Representative David of Baghdad (`9000222`) starts with the trait. Kehillah appointment scoring gives a Ben/Bat David candidate +15. That is enough to matter, but less than communal office (+25), endorsement (+30), or a substantial Learning and Stewardship advantage, so Davidic descent does not make the Kehillah hereditary.

The historical-roster source-map branch should give the trait to reviewed Davidic/exilarchal characters when those characters receive defensible dates and move into live history. The trait does not by itself assert that a conjectural link is historical fact.

## Kohen and Levite generation

CK3 1.20's generated `_traits.info` defines `random_creation` as a percentage from 0 to 100. The previous values `0.05` and `0.04` therefore meant 0.05% and 0.04%, despite their comments describing 5% and 4%. They are now `5` and `4`. The existing Jewish-faith potential and paternal inheritance remain unchanged. Elijah ha-Kohen now explicitly carries `kohen`; Isaac HaLevi already carried `levite`.

The name-list format cannot make a dynasty-name draw conditional on a character trait. Random `HaLevi`, `Segal`, `Cohen`, and `Cohen Tzedek` dynasty names were therefore removed from the Israelite random and cadet pools. Historically authored families retain those names and their matching traits. Generated Kohanim and Levites may belong to ordinary family names, which is preferable to generating an explicit priestly name on a character without the corresponding lineage.

## Verification

A corrected fresh isolated boot reached the 1066 selector. David of Baghdad displayed the Ben David icon and localized tooltip, Elijah ha-Kohen displayed Kohen, and the focused error-log checks found no errors attributable to the lineage traits, their icons, the adjusted name lists, or the appointment score. See `docs/testing/2026-10-18-jewish-lineage-traits-live-test.md`.

### Still needed

A fresh-game probe should create a large sample of Jewish generated characters, count Kohen and Levite traits, verify that non-Jewish generated characters do not receive them, and test paternal inheritance of all three lineage traits. The exact observed proportions will vary because independently successful inheritable-trait rolls are resolved to one resulting trait.
