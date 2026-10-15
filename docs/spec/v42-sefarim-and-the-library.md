# V42: Sefarim and the Beit Midrash collection

**Status: FIRST UI AND SEEDING SLICE SCRIPTED; FRESH-BOOT SEED VERIFIED, UI NOT LIVE-VERIFIED — 2026-10-14. Broader mechanics below are a proposal.** Requested by Daniel on 2026-10-14. Builds on [V13](v13-domicile-library-panel.md), [V24](v24-rabbi-gameplay-loop.md), [V29](v29-yeshiva.md), and [V32](v32-exceptional-sefarim.md). This document supersedes V13's claim that the green check and "mastered" list can read `kehillah_studied_works`: V24 established that list as *encountered* and `kehillah_mastered_works` as successful mastery. ROADMAP remains authoritative for shipped status.

## The first slice

- The panel has Books and Yeshiva pages. The yeshiva controls and portraits no longer push the collection down the same column. The Books page retains the held-work list, donation buttons, and the player's checklist.
- A work's book icon opens a longer catalog description in the same panel. The row hover also shows that description and a mastery status. The personal mastered list can be expanded when wanted.
- Both the green check and that list now read `kehillah_mastered_works`. A failed first reading remains in `kehillah_studied_works` for discovery and save compatibility, but does not claim mastery on screen.
- Initial seeding uses 1–3 distinct works at tier 1, 3–4 at tier 2, and 4–6 at tier 3. All draws still come from the existing Parshanut and Talmudics pool. No Hashkafa copies appear from this seed. Upgrading a hall later does not create books for free. The seed runs once when a community is registered; no existing-save library is rerolled.

The [fresh isolated CK3 check](../testing/2026-10-14-sefer-seed-live-check.md) saw Worms at tier 3 with six distinct works and Mainz at tier 1 with three. A second fresh boot ran `kehillah_sefer_debug.1`, a read-only probe for a leader's hall tier, held flags, and mastered flags; it logged five distinct works in tier-3 Worms without adding runtime errors. The virtual-display input path could not open the library, so no UI rendering or click assertion passed.

The catalog still uses title-owned work flags. Its longer descriptions are text, not artifact entities. The 2026-09-15 [inventory spike](spike-book-inventory.md) found that vanilla artifacts are character-owned, although `artifact_succession_title` can move them with a title. The installed CK3 1.20.1 `title_on_actions.txt` still contains that succession transfer. A wholesale artifact conversion would require a single source of truth for possession, loss, donations, copying, succession, and DLC absence. A display mirror must never become a second independent inventory.

The new order descriptions were checked against [Sefaria's Talmud catalog](https://www.sefaria.org/texts/Talmud?lang=en); the shorter existing entries remain the source of each work's title and attribution. These are short game descriptions, not claims that every medieval community owned a complete printed edition of an order.

## The collection to build toward

| Layer | Holder | Meaning |
| --- | --- | --- |
| Work identity | Stable work ID | The text's subject, author or attribution, era, and faith availability. |
| Copy | Community title | The community can offer this work for study and use it to attract scholars. The current `kehillah_library_works` list remains the authoritative copy record until an artifact prototype proves a replacement. |
| Encounter | Character | The character has seen or attempted the work. Existing `kehillah_studied_works` means this. |
| Mastery | Character | Successful deep study, stored in `kehillah_mastered_works`; this gates citations and stronger writing rewards. |
| Manuscript artifact | Character, following a title when appropriate | A visible object for a distinguished copy or exceptional authored sefer, with provenance and optional artifact interactions. This needs an EP1-off route for the underlying work. |

Do a **one-work artifact prototype** before converting the catalog: make one named copy, bind it to the community title, change leaders, donate or copy it, save and reload, then inspect how vanilla inventory actually displays it. Test the title-succession variable on the new owner after a transfer; an old title value can reclaim a donated artifact at the next succession. The title list must continue to drive study until the artifact route proves every consumer and save migration. Ordinary books written in the existing chain remain distinct from new enduring world works, per V32.

## Acquisition and scholarly demand

1. **Find a source.** A scholar selects a field or a named work worth pursuing. Show known nearby libraries and a reason for the choice: an unmastered source for semicha, a source cited in a Bet Din case, a yeshiva's teaching focus, or a prerequisite for a writing ambition. The scholar should not choose randomly from already mastered works while an accessible new source fits the intent.
2. **Get a copy.** Commissioning should identify a source library, a scribe, travel or correspondence time, and the cost. A sofer's workshop lowers the time or cost; a higher hall supports a larger active collection. Preserve the existing random acquisition as a fallback until the named route is proved, then retire or narrow it so two systems do not grant the same copy twice.
3. **Circulate deliberately.** News of an ordinary book is not a library copy. An exceptional author's origin library gets the first copy. Other communities gain a copy only through an explicit copy, purchase, or donation effect. The player can see both the source and destination before confirming a transfer.
4. **Capacity without deletion.** A hall tier can limit *displayed active study slots* or copying throughput. Do not silently destroy a saved work when a building is damaged or a tier falls. Decide overflow handling from a live test of the actual collection UI before adding a hard capacity.

## Rewards and uses

| State | Proposed effect | Guard against farming |
| --- | --- | --- |
| Community owns a work | Small Greatness and yeshiva attraction weighted by field diversity and a few exceptional works, not a linear bonus for every duplicate. The relevant work can be consulted locally. | Count stable work IDs once; cap the broad collection bonus. A loss removes its ownership benefit. |
| Character first masters it | Current Rabbi track XP and Talmud Torah rewards remain; add a modest field-specific Learning lifestyle XP or progress toward a relevant perk, not a free perk for each title. | Once per character and work; encounters do not qualify. |
| Character cites it | A relevant Bet Din, responsum, or disputation option becomes available, with argument text particular to the source. The library's possession alone does not give a judge personal mastery. | Gate on the actor's mastery and the case's source tag; no universal "books give +X" court modifier. |
| Character writes from it | A relevant mastered source, actual rulings or teaching, field depth, and writing quality advance a named exceptional ambition. | V32's once-per-world work guard and failed-bid ordinary outcome; do not mint enduring works solely from high Learning. |

Tune numbers only after measuring how often communities acquire books and how often scholars reach mastery in a long observe run. A strong hall ought to draw readers because it offers **sources they lack**, not because it grants an unbounded passive stat bonus.

## Canon and faith access, later slice

Store eligibility on the *work*, never inferred from its owner. The first pass should distinguish scriptural texts shared across traditions from rabbinic oral-law works and Karaite-specific works. A Tanakh entry could be available to Jewish faiths and be a relevant biblical source for Christians, while Jewish and Christian interpretive traditions would still differ. `Talmud Torah` and the separate Ba'alei ha-Miqra route already enforce distinct curricula; do not merge their mastery rewards simply because both can read a biblical text. Model eligibility as a positive list of faith families or rites with a reason shown in the book detail, and verify CK3 1.20's rite/faith scope syntax in the installed game before scripting it. Cross-faith ownership, access, and canon are separate questions: a Christian holder owning a Hebrew text does not by itself make it canon to that faith.

Start with one shared scriptural work and one Rabbinic-only work. Prove access, study, citation, and UI wording for Rabbinism, Karaism, and a Christian rite. Historical catalog expansion follows that proof.

## Composition, corpora, and living standing — 2026-10-14 addendum

**Status: PROPOSAL, NOT IMPLEMENTED.** Daniel proposed historical dates, prestige tiers, grouping the Mishnah and Talmuds differently, and letting scholarly use change a work's standing. This refines the work-identity and reward sections above; it does not change the current save format or starting seed.

Give each work three separate kinds of information:

1. **History:** an approximate composition or redaction period, an earliest plausible circulation date for game logic, and a confidence label where dating or authorship is disputed. Show the historical period in the catalog; enforce the availability date at *creation or acquisition*, never by deleting an old saved copy. An enduring work authored during play uses its actual completion date. The current catalog already gates *Emunot ve-Deot* at 933, *Chovot HaLevavot* at 1080, and *Kuzari* at 1140 in acquisition. Put those dates in one audited catalog before adding more; V32's proposed dynamic *Kuzari* authorship will need to replace its fixed 1140 gate, not coexist with it.
2. **Kind and corpus:** Torah has a scriptural role of its own. The Mishnah is a distinct source that the Talmuds discuss, so preserve its identity and its separate Bet Din citations even if the UI nests it alongside Talmudic study. Display Bavli and Yerushalmi as corpora whose study units are tractates or meaningful sections. A community might own particular volumes; one shelf entry must not imply that every tractate is present. Existing seder flags and character mastery need an explicit migration before changing their granularity.
3. **Reception:** fixed doctrinal role and an evolving reputation are different. A foundational text does not lose its canonical role when no one cites it for a decade. A responsum or commentary can become influential through copies, independent scholars who master it, teaching, and citations in actual rulings. Neglect can reduce that *influence*, within bounded bands. Award credit once per distinct scholar, case, or community over a time window, so rereading and repeated low-stakes cases cannot inflate a work indefinitely.

For the first dynamic slice, use four reception bands—little known, discussed, established, influential—on one later commentary or responsum. Recalculate slowly, perhaps once every five years, from saved adoption records. Influence can improve copying interest, a yeshiva's attraction, or the weight of a named citation; it must not auto-grant mastery or override the case's reasoning. A corpus can have a fixed foundational role while its specific tractates have different local demand. Only after that slice works should reception be tracked separately for Rabbinic and Karaite readers, with new faiths inheriting an initial baseline from their parent and then diverging through play. That lets shared texts have different standings without forcing a single universal prestige ladder.

As a concrete later text, use *Iggeret Rav Sherira Gaon* rather than a generic "Responsa of Sherira Gaon" collection. It is a long Geonic response written in 986/987 about the history of rabbinic teaching and texts; it can start as a respected but not foundational source in a 1066 campaign. Its historical date is supported by [Robert Brody's British Academy chapter](https://academic.oup.com/british-academy-scholarship-online/book/16046/chapter-abstract/171031593). The distinction between Mishnah and Talmud as text and commentary is described in [Sefaria's Talmud catalog](https://www.sefaria.org/texts/Talmud/Bavli?set-language-cookie=).

## Verification gates

The first slice needs a fresh isolated CK3 boot, a library with and without a yeshiva, a click on a held work, expansion of the personal checklist, and a failed-then-successful reading to prove the check changes only on mastery. A console probe should inspect tier-1/2/3 seed counts and distinctness on fresh titles; a live UI check should confirm the longer text stays inside the panel. Record the session in `docs/testing/`. The artifact prototype requires a succession and transfer test, plus an EP1-off study path, before it can replace the flag list.
