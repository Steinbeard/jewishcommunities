# Jewish rite icons and names

**Status: built 2026-11-12; source and xTiger checked, live UI check pending.**
Follows the medieval minhag build and Daniel's twelve-symbol art direction.

## Names and descriptions

- The faith stays Rabbinic Judaism. Its mainline rite, internal key `rabbinism`, displays as
  **Minhag Bavel**. It now has a rite description centered on Sura, Pumbedita, the Bavli and
  Geonic teaching.
- Minhag Yerushalmi and Minhag Sepharad each have their own description. The Yerushalmi text
  covers the Palestinian-rooted practice represented in 867 Italy and Byzantium as well as the
  Land of Israel.
- The `merkabah` rite displays as **Yordei Merkavah**, with a description of its mystical path.
- The prior `kehillah_minhagim_l_english.yml` began with literal `\xef\xbb\xbf` characters,
  and the Bavli replacement file had no actual BOM. Both now start with a real UTF-8 BOM, as
  CK3 localization files require. This addresses the raw keys visible in Daniel's screenshot.

## Icon set

All new files are transparent 100×100 RGBA DDS files under `gfx/interface/icons/faith/`.
The built-in image generator used vanilla CK3 Jewish faith icons as a style reference: isolated,
centered silhouettes with a restrained metal or wood palette, small bevels, no border or words.
The icons were downsampled and centered within 82×82 pixels for readability in rite lists.

![The twelve requested emblems at in-game size](assets/kehillah-jewish-faith-icons-preview.png)

| Rite or faith | Icon | Assignment |
| --- | --- | --- |
| Minhag Bavel | Lectern / shtender | Mainline rite |
| Minhag Yerushalmi | Vanilla seven-branched menorah (`rabbinism.dds`) | Rite |
| Minhag Ashkenaz | Torah scroll | Rite |
| Minhag Sepharad | Ornate geometric star | Rite |
| Yordei Merkavah | Chariot wheel | Rite |
| Karaism | Open book with qof | Faith and rite |
| Haymanot | Ark of the Covenant | Faith and rite |
| Samaritanism | Stone tablets | Faith and rite |
| Khazar Judaism / Kabarism | Horse with Jewish medallion | Faith and rite |
| Malabarism | Ship with menorah sail | Faith and rite |
| Italki | Arch-of-Titus-inspired menorah | Asset ready; Italki is a culture, not a separate rite |
| Romaniote | Purple oil lamp with star | Asset ready; Romaniote is a culture, not a separate rite |

The shared image prompt specified a single CK3 faith emblem, compact hand-painted metal or wood,
one main color, a transparent square background and readability at 32 pixels. Each requested
symbol in the table supplied the subject prompt. The Yerushalmi icon uses the installed vanilla
asset itself, preserving Paradox's exact menorah silhouette. This keeps the faith-level Rabbinic
star distinct from the mainline rite's lectern.

Haymanot and Malabarism faith definitions and their mainline rites are copied from installed
CK3 1.20.1.2, changing only the icon fields; refresh them if vanilla changes. Existing Karaite,
Samaritan and Khazar overrides received matching icon references. The 867 Italian and Byzantine
communities continue using Minhag Yerushalmi, so the Italki/Romaniote art is deliberately unused
until those communities gain separate rites.

## Verification

- xTiger 1.6.10: 0 fatal, 16 baseline errors, 107 warnings; no new changed-file errors.
- Source audit: all icon names resolve to a 100×100 RGBA DDS, except `rabbinism`, which resolves
  to the installed vanilla icon. Thumbnail atlas inspected at native size.
- Live UI check pending under the repository's Luna-only game-control rule. Verify names,
  descriptions and silhouettes on the Rites screen after a fresh CK3 restart; inspect
  `error.log` against the boot baseline.
