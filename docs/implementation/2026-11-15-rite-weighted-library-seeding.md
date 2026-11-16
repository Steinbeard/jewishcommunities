# Rite-Weighted Library Seeding

**Status: BUILT; source checks and xTiger baseline pass, fresh-start check pending — 2026-11-15.** Implements Daniel's direction that starting libraries reflect their rite's intellectual tenets, while keeping Machshavah materially present but rarer than Parshanut and Talmudics.

## What changes

The Shas-first seed remains intact. The extra one to three non-Bavli books now retain the old ordinary draw and receive additional weighted buckets when the holder's rite carries a relevant tenet:

| Rite emphasis | Tenet | Favoured seed material |
| --- | --- | --- |
| Peshuto shel Miqra | `tenet_literalism` | Targum Onkelos, Mekhilta, Genesis Rabbah |
| Iyyun ha-Talmud | `tenet_kehillah_scholarly_study` | Mishnah, Tosefta, Yerushalmi Moed, Halakhot Gedolot, and Geonic sources |
| Pesak Halakha | `tenet_religious_legal_pronouncements` | Halakhot Gedolot and the Geonic legal sources |
| Reasoned Theology | `tenet_kehillah_hokhmah` | Arabic *Theology of Aristotle*, Galen's *On the Usefulness of the Parts*, or *Mekor Hayyim* |
| Esoteric traditions | `tenet_esotericism` | *Sefer ha-Razim*, *Hekhalot Rabbati*, or *Shiur Qomah* |
| Sacred Liturgy | `tenet_kehillah_sacred_liturgy` | One available Andalusi Hebrew poetry collection |

Every Rabbinic library still receives *Sefer Yetzirah*. Since 933, *Emunot ve-Deot* is now seeded only when the rite has Reasoned Theology, rather than universally.

Machshavah is capped at one optional extra work during a library's initial seed. The cap applies across the Reasoned Theology and Esotericism routes and is cleared after creation. It keeps the extra shelf's genre probabilities below the Parshanut and Talmudics buckets, even where a rite strongly favors intellectual or mystical study.

## Hokhmah and poetry additions

Reasoned Theology explicitly values philosophy, medicine, and the study of nature. It may now select one of three date-gated Arabic works through the same one-extra-Machshavah cap: the *Theology of Aristotle* (840), an Arabic *On the Usefulness of the Parts* of Galen (850), or Ibn Gabirol's *Mekor Hayyim* (1050). The first is deliberately labelled an Arabic adaptation of Plotinus **attributed** to Aristotle, rather than silently treating that attribution as fact. These are shared-tradition, non-canonical works recorded in the existing Machshavah display genre; their titles and prose make their Hokhmah/medical character visible.

Sacred Liturgy now gives a Rabbinic library exactly one additional, available Hebrew poetry collection: Poems of Dunash ben Labrat from 990, Samuel ha-Nagid's *Diwan* from 1056, or Solomon ibn Gabirol's *Diwan* from 1058. They are Parshanut works with the `poetry` sermon kind, so the existing sermon system can preach from them. The dates are circulation gates, not claims that a single authorial edition was completed in that exact year; each entry states the relevant uncertainty where it matters.

The special liturgy draw is deliberately not folded into the ordinary Parshanut random list. A Sacred-Liturgy rite will visibly retain a poetic/liturgical shelf once such material exists, while other rites do not begin to overproduce poetry. It is not counted toward the optional-Machshavah cap.

Historical research and the choice of representative circulation dates are recorded in [the catalog research note](../research/2026-11-15-hokhmah-andalusi-diwan-catalog.md).

## Checks

- Focused source assertions confirm the Hokhmah and Sacred-Liturgy gates, all date-gated catalog IDs, the optional-Machshavah cap, and the rational/mystical helper effects.
- The current shared-worktree xTiger audit reports `fatal: 0, error: 34, warning: 117, untidy: 37, tips: 135`; no report names these new works or `kehillah_library_effects.txt`. The aggregate is a moving repository baseline because other work is concurrent.
- Manual fresh-start check remains: compare a Literalist, an Iyyun, a Hokhmah, an Esoteric, and a Sacred-Liturgy Rabbinic community; verify Shas size remains determined by hall/eminence, Hokhmah receives only one optional supplement, and Sacred Liturgy receives exactly one date-valid poetry collection.
