# Sefer acquisition live test — 2026-10-20

**Status: SOURCE AND METHOD UI PASS; ACTIVE PROFILE LOG CLEAN; EXTENDED ROUTE/COMPLETION MATRIX PENDING.** Tested on CK3 1.20.1.1 from `codex/sefarim-acquisition` after merging `origin/master` at `97fa062`.

## Static checks

- `scripts/kehillah_library_catalog.py` ran twice with an unchanged second run and generated 23 work actions.
- `git diff --check` passed apart from Git's existing LF-to-CRLF notice for `kehillah_library_acquire_gui.txt`.
- `ck3-tiger` reported `fatal: 0, error: 1091, warning: 151, untidy: 1, tips: 24` after the master merge. No reported fatal, error or warning named an acquisition file changed by V48. Tiger still targets CK3 1.19.0 while the installed game is 1.20.1.1.

## Live checks

All automated launches used separate explicit `-userdir` profiles and exact PID ownership. Luna controlled only its named isolated process. A final passive Luna pass performed no input or screen control.

- An earlier isolated 1066 Worms probe enumerated 17 released missing works, included `work_emunot_vedeot`, and logged PASS for hiding both *Chovot HaLevavot* (1080) and *Kuzari* (1140). It added no error-log lines.
- The earlier single-route build successfully selected Bereshit Rabbah from a named source, charged gold, displayed the named pending row and forced delivery through `kehillah_sefer_debug.5`. That run exposed the saved-scope custom-localization defect; V48 replaced it with the guarded `kehillah_commission_work_loc` character variable before the final method UI test.
- A fresh v3 run loaded the 1066 Worms start and visibly confirmed the tier-1 Sofer's Workshop. Its post-load delta contained no acquisition/library, unset-target, invalid-comparison, custom-localization or GUI/data-context match.
- Daniel's final v4 screenshots confirmed the two-stage UI on *Talmud Bavli: Moed*: Narbonne and Jerusalem appeared as source communities. Choosing Narbonne opened **How Shall We Acquire It?** with **Buy a surplus manuscript** and **Borrow the exemplar and have our scribe copy it**. The source-Scriptorium option was absent because that source lacked the tier-2 facility. The local-copy tooltip showed the tier-1 route's 15-gold cost and eighteen-month time, plus the nine-month Scriptorium improvement.
- The active v4 profile (`C:\Users\Daniel\.codex\ck3-test\sefarim-acquisition-v4`, PID 34796 at inspection) had 2,926 error-log lines and zero matches for acquisition/library, `kehillah_commission_work_loc`, invalid comparison, or GUI/data-context failures. Its four unset-target matches were the two pre-existing `kehillah_mob_*` warnings repeated twice.

An older inactive `sefarim-acquisition` profile contained historical acquisition errors from hot-loading the work before event `.0005` and its localization existed. Those are not attributed to the final v4 build; they are retained in that profile's log rather than silently conflated with the clean v4 result.

## Still worth exercising

The first playable slice is stable enough to review, but a later live matrix should explicitly start and finish all four routes (purchase, external Scriptorium, tier-1 local, tier-2 local/distant), repeat delivery after succession, and confirm each route-specific pending description. The title-scoped completion mechanism itself was unchanged from the earlier successful forced-delivery check.
