# Medieval Rabbinic Minhagim: first implementation slice

**Status: built 2026-11-12; source and xTiger checked, live scripted test pending.** Implements
the first slice of [the rite design](../spec/2026-11-11-medieval-rabbinic-minhagim-and-karaite-kehillot.md).
This stays on the current Sefarim feature branch because rite-specific canon is implemented in the
existing catalog and library system.

## Result

- The faith remains **Rabbinic Judaism**. Its mainline rite keeps the internal key `rabbinism` and
  is displayed as **Minhag Bavli**. Script compatibility is preserved.
- Adds `minhag_yerushalmi` and `minhag_sepharad` rite types. The rite types share the Rabbinic
  faith and its faith-level doctrines; their localized descriptions identify their regional
  custom.
- At start, Jerusalem's community and county follow Minhag Yerushalmi in all three bookmarks;
  Tiberias follows it in 867. Sephardi characters and counties follow Minhag Sepharad from 1066.
  Rite seeding runs before community libraries are initialized.
- The catalog supports rite-specific canon. Mishnah and the four extant Yerushalmi divisions are
  foundational in Minhag Yerushalmi; the six Bavli divisions are outside its canon. Other
  Rabbinic rites follow the Bavli. A Yerushalmi community library starts with Mishnah and its four
  Talmudic divisions. Complete-corpus checks use the four Yerushalmi divisions for that rite.
- The Gaonate title history seats Amram ben Sheshna in 867, passes it to Nahshon in 872, leaves
  it vacant in 1066, and seats Samuel ben Eli in 1178. Game-start initialization applies the
  regular Gaon style/head refresh to these static historical holders.

## Karaite representation

No bookmark community was changed to Karaism. The sources establish Karaite communities in Fustat
and Constantinople, but not a citywide majority. Toledo and Talavera are named as Karaite centers;
the same evidence says Rabbanites are the majority and records suppression of Karaism. The surviving
Castilian stronghold is unnamed. With one dominant community per place, setting one of these
existing communities to Karaism would overstate the evidence. Future minority congregation support
or a specifically documented Karaite-majority locality would let the mod represent them without
mislabeling the dominant community.

Sources consulted:

- [Medieval Fustat Jewish communities, Library of Congress-hosted study](https://tile.loc.gov/storage-services/master/gdc/gdcebookspublic/20/20/71/54/53/2020715453/2020715453.pdf)
- [Toledo, Jewish Virtual Library](https://jewishvirtuallibrary.org/jsource/judaica/ejud_0002_0020_0_19924.html)
- [Martínez Delgado and Ashur, Karaite presence in al-Andalus](https://revistaseug.ugr.es/index.php/meahhebreo/article/download/22581/22425/)
- [Encyclopaedia Iranica, Daniel al-Qumisi](https://www.iranicaonline.org/articles/danial-b/)
- [Two Talmudim overview](https://daat.ac.il/daat/vl/guide/guide01.pdf)

## Verification

- `py -3 -m py_compile scripts/kehillah_library_catalog.py` — passed.
- `py -3 scripts/kehillah_library_catalog.py` — regenerated 168-work catalog, standing values,
  effects and localization.
- `git diff --check` — passed.
- xTiger 1.6.10 / CK3 1.20.1.2 — 0 fatal and 16 errors overall, matching the recorded baseline;
  no errors in changed files. One existing root-scope warning points at the startup hook in
  `kehillah_on_actions.txt`; the called historical-pillar effect and warning are documented in
  `docs/testing/xtiger-mcp-guide.md`. xTiger also reports 109 warnings overall, including
  pre-existing warnings elsewhere in the mod.
- Live runtime probe — pending. PID 26900 was running CK3 without a Codex ownership marker; no
  control was sent. This session did not have xTiger MCP tools.

## Follow-up probe

In disposable 867, 1066, and 1178 saves, log `rite:rabbinism.head_of_rite`,
`rite:minhag_yerushalmi`, `rite:minhag_sepharad`, the relevant title holders, the Jerusalem/Tiberias
county rites, and each library's `kehillah_library_tradition` and work list. Confirm the 867 Gaon
is Amram; 1066 has no head; 1178's head is Samuel; Yerushalmi has four divisions plus Mishnah and
no Bavli orders; Sepharad is created in 1066 and 1178, not 867. Check `error.log` against a clean
kehillah-tagged baseline. The in-game rename can be checked on the faith and rite panels after
these script assertions pass.
