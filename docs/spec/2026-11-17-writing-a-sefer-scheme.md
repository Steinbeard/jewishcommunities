# Writing a sefer as a scholarly project

**Status: BUILT through 2026-11-18; source validation complete, live verification pending.** Supersedes the composition and named-ambition rules in [the 2026-11-08 redesign](2026-11-08-sefer-system-redesign.md) §6.1–6.2 and the separate survey/no-artifact decisions in [the 2026-11-17 build record](../implementation/2026-11-17-writing-sefarim-flow.md). The catalog and per-rite standing ladder remain the authoritative base. See [the implementation record](../implementation/2026-11-17-writing-sefer-scheme.md).

## Player flow

1. **Discipline:** Write a Sefer opens with Parshanut, Talmudics and Machshavah. The tooltip shows a named aptitude and its inputs. Existing poems are a Parshanut form, not a fourth ledger genre. A Karaite Religious Scholar may write Scripture and thought without being given the Rabbanite Rabbi trait.
2. **Project:** choose a form, such as Torah commentary, midrashic exposition, poetry, Talmud commentary, halakhic treatise, responsa, minhag collection, philosophical dialogue, mystical work, or disputation. The relevant language and a source the author has mastered are hard requirements. Near projects remain visible but disabled through CK3's `show_as_unavailable`; their tooltip explains the missing requirements. An unfilled landmark niche is shown as a possible outcome, not selected directly.
3. **Composition:** a self-directed personal scheme takes at least several seasons. Research, objections and revision produce choices and risk. Learning, relevant mastery/rounds, trait experience, language, work form, helpers and event choices determine the visible chance to finish and the accumulated quality. Failure yields notes and some experience, no book.
4. **Result:** an ordinary completed book gives an artifact and news to communities in diplomatic range, but no ledger work, library copy or automatic mastery. An exceptional manuscript can fill an unoccupied historical catalog niche; only then is it registered in the ledger, mastered by its author, placed in the author's library and represented by a matching landmark artifact. Reception by rites remains a separate, longer process.

## Historical landmarks

The ten existing named work IDs remain stable for save compatibility. The catalog also contains 26 fixed works dated after the 867 bookmark, for 36 future niches in total: 36 after 867, 20 after 1066 and twelve after 1178. Every such work has a mapped writing form and scholarly gate. Before its catalog circulation date, a scholar may fill a fixed niche in an alternate history; otherwise the historical version enters circulation on its existing date. A filled niche leaves its project form available for ordinary artifact-only manuscripts. A work written by a player has the actual author, composition year and a dynamic author-aware title and description in the ledger. The historical author's identity can ease some old ambition gates but never reserves a niche. The [2026-11-18 addendum](2026-11-18-commentary-and-landmark-expansion.md) specifies thesis-tenet requirements, the eight added works and commentary links.

**2026-11-18 outcome correction:** The original build erroneously registered every successful book as a ledger work. Daniel chose a stricter distinction: ordinary success is a manuscript and local news; landmark success is the rare route into the historical ledger. The landmark roster now includes all catalog works later than a start date, including prayer books, legal letters, Karaite commentaries, poetry, Beta Israel Sabbath instruction and the Kerala charter tradition. A charter niche represents a scholarly compilation of the remembered document, not the Jewish writer issuing a royal grant.

## Period-sensitive Machshavah — 2026-11-17 addendum

**Status: BUILT; live check pending.** This addendum supersedes the initial Machshavah project gates above where they depended on later source books. An 867 scholar can write a dialogue on Scripture and law after mastering the Torah plus the Mishnah, Philo or *Memar Marqah*; a disputation can draw on those sources; an ethical exhortation can draw on Tanakh and an early ethical source. Mystical writing still draws on *Sefer Yetzirah*, and translation on the earlier Greek or Arabic sources already in the catalog. These generic forms remain open in later periods too.

Systematic philosophical dialogue becomes an additional form from 933, when the catalog dates *Emunot ve-Deot*, and requires mastery of it or *Chovot ha-Levavot*. The latter enables a distinct inward-devotion form from its catalog date of 1080. *Kuzari* and *Moreh Nevukhim* are outcomes of systematic dialogue; *Sefer Hasidim* is an outcome of inward devotion. The Machshavah choice scene and objection scene vary with the era and form. Explicit dates guard the later forms, while source mastery still determines whether a character may select them. Historical landmark qualifications remain separate.

## Study partner

A named chavrusa may assist Study Torah and composition. Their learning and language should influence the visible chance, and events should establish a relationship. Assigning one must not confer mastery or let a character bypass a project's hard language requirement. A partner is optional, so writing and study remain possible without a suitable courtier.

## Implementation limits to verify live

CK3 event options support `show_as_unavailable` in the installed vanilla files. The scheme must prove its save/load, cancellation, progress and chance display in a disposable live save. The artifact must show the same name as the ledger work after save/load. These are not established by xTiger alone; repository policy assigns live checks to Luna.
