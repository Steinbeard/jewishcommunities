**Status:** BUILT 2026-11-23; source/xTiger checked, live check pending. Extends [citation strength and risk](../spec/2026-11-23-bet-din-citation-strength-and-risk.md) and the [cherem design](../spec/2026-11-11-reviews-and-cherem.md).

# Forbidden sources at a Bet Din

Daniel asked for consequences and clear warning when a judge cites a book the host rite forbids. Each proposed work is assessed in the rite of the convening community's current leader, not the citing judge. Its real standing is used, not the special reduced Mishnah rank used to pick a source. A warning symbol appears on each banned or anathematized choice and the option tooltip gives the consequence.

Naming a source gives the citing judge 5 cherem XP if Banned, 15 if Anathema, using the same values as reading. The citation is public even if the argument fails its reliability roll. The existing cherem helper limits XP to living Jewish characters outside full Cherem; the cause is recorded for teshuvah. One award occurs when the source is selected, not again when the ruling closes. No host or no assessed rank means no penalty. Generated dispatch is maintained by `scripts/kehillah_library_catalog.py`.

Console-only `event kehillah_din_cherem_debug.1` logs the citing judge and each offered source's host standing while the citation event is open. Live checks remain: compare identical citations under different host and judge rites, test both forbidden ranks and a safe rank, failed and successful arguments, another judge citing, full Cherem, each option and its tooltip. Verify XP once and check error.log; rendering and engine behavior are unverified.
