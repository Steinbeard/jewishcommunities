# Rite-Weighted Library Seeding

**Status: BUILT; source checks and xTiger baseline pass, fresh-start check pending — 2026-11-15.** Implements Daniel's direction that starting libraries reflect their rite's intellectual tenets, while keeping Machshavah materially present but rarer than Parshanut and Talmudics.

## What changes

The Shas-first seed remains intact. The extra one to three non-Bavli books now retain the old ordinary draw and receive additional weighted buckets when the holder's rite carries a relevant tenet:

| Rite emphasis | Tenet | Favoured seed material |
| --- | --- | --- |
| Peshuto shel Miqra | `tenet_literalism` | Targum Onkelos, Mekhilta, Genesis Rabbah |
| Iyyun ha-Talmud | `tenet_kehillah_scholarly_study` | Mishnah, Tosefta, Yerushalmi Moed, Halakhot Gedolot, and Geonic sources |
| Pesak Halakha | `tenet_religious_legal_pronouncements` | Halakhot Gedolot and the Geonic legal sources |
| Reasoned Theology | `tenet_kehillah_hokhmah` | *Mekor Hayyim* once available |
| Esoteric traditions | `tenet_esotericism` | *Sefer ha-Razim*, *Hekhalot Rabbati*, or *Shiur Qomah* |

Every Rabbinic library still receives *Sefer Yetzirah*. Since 933, *Emunot ve-Deot* is now seeded only when the rite has Reasoned Theology, rather than universally.

Machshavah is capped at one optional extra work during a library's initial seed. The cap applies across the Reasoned Theology and Esotericism routes and is cleared after creation. It keeps the extra shelf's genre probabilities below the Parshanut and Talmudics buckets, even where a rite strongly favors intellectual or mystical study.

## Secular Arabic and Greek learning

Reasoned Theology explicitly values philosophy, medicine, and the study of nature; Arabic scholarship is an appropriate medieval transmission route for Greek learning. No secular scientific works are added in this change, because the current catalog has only Parshanut, Talmudics, and Machshavah display genres. Calling a scientific treatise a Machshavah work without a visible distinction would obscure what the player has found.

The next catalogue slice should add a clearly presented Hokhmah/natural-philosophy subcorpus, with curated rather than procedurally invented works. Reasoned Theology should make those works eligible for the same single optional intellectual supplement, retaining the Machshavah/science rarity cap. Candidate material includes Arabic transmission of Euclid, Ptolemy, Galen, and Aristotle, but individual entries need a historical-circulation and language audit before they enter the catalog.

Sacred Liturgy should likewise receive a seed weight once the historical catalog contains Piyyutim; no such fixed work exists in the present catalog, so it receives no empty mechanic.

## Checks

- Focused source assertions confirm all five active tenet gates, the optional-Machshavah cap, and the rational/mystical helper effects.
- xTiger baseline after the change remains `fatal: 0, error: 66, warning: 112, untidy: 37, tips: 132`, with no report in `kehillah_library_effects.txt`.
- Manual fresh-start check remains: compare a Literalist, an Iyyun, a Hokhmah, and an Esoteric Rabbinic community; verify Shas size remains determined by hall/eminence and no library receives more than one optional Machshavah work.
