# Pre-alpha screenshots and test pass

**Status:** 2026-11-16. Replaces this file's first version from the same day. A screenshot list
that doubles as the live check for features built in the last four weeks and marked "not
live-tested" in their docs. Each shot is taken on a screen that one of those features changed,
so check the **Check** column while you're there. Tick both columns as you go.

The 12 shots in `docs/images/` are from 2026-10-18. Keep `quarter-map`, `council`, `decisions`,
`event-accusation`, `holiday-rosh-hashanah`, `bet-din-sitting` and `charter-renewed`. Everything
below is new or a re-shoot.

**How to capture:** full window, 16:9, JPG at about 85 quality, into `docs/images/`. Move tooltips
you don't want out of frame first. Pick moments with real names and numbers, not empty states.
Before each session, note how many `kehillah` lines `error.log` has, and check it again after
the UI steps, because tooltip-only error floods only show up there.

**★ = Steam gallery pick.** Steam shows the first one as the main preview, so take ★1 last, once
you know which shot is strongest.

---

## A. Main menu: the start screens

| ✓shot | ✓test | File | Screen | Check |
|---|---|---|---|---|
| | | ★ `start-1066.jpg` | Age of the Rishonim with Joseph or David selected | Granada roster has no duplicate characters ([doc](../implementation/2026-11-10-granada-duplicate-roster.md)) |
| | | `start-867.jpg` | Age of the Geonim with Manasseh selected | Portraits and text for all seven characters |
| | | `start-1178.jpg` | The Paths of Torah with the Rambam selected | As above |

## B. Worms 1066, as Isaac (the main session)

Before unpausing:

| ✓shot | ✓test | File | Screen | Check |
|---|---|---|---|---|
| | | ★ `domain-overview.jpg` | Domain: pillars, Quarter, the three leadership-style buttons | Buttons, effects text, and the "no style chosen" reminder ([doc](../implementation/2026-11-15-community-leadership-styles.md)) |
| | | `leadership-style-chosen.jpg` | The same screen after choosing Scholarly, with the mandate status showing | The selected styling and the ten-year mandate text |
| | | `succession-candidates.jpg` | The succession candidates panel | Candidates' scores reflect the style you chose ([doc](../implementation/2026-11-15-succession-candidates-and-continuity.md)) |
| | | `faith-rite.jpg` | Faith screen for Worms's rite: tenets and doctrines | Rite icon and name, tenet statuses, no raw keys ([revision](../implementation/2026-11-14-faith-rite-tenet-holiday-revision.md), [icons](../implementation/2026-11-12-jewish-rite-icons-and-names.md)) |
| | | `tenet-decision.jpg` | Decisions list showing Pursue Sacred Study or Compose Sacred Verse | Take one and check its result ([doc](../implementation/2026-11-15-tenet-fixes-and-sacred-homeland.md)) |
| | | ★ `library-shelf.jpg` | Library: the shelf and book cards | Starting books fit the rite, including *Sefer Yetzirah*, with no blank cards ([seeding](../implementation/2026-11-15-rite-weighted-library-seeding.md), [cards](../implementation/2026-11-08-library-cards.md)) |
| | | ★ `sefarim-ledger.jpg` | Sefarim Ledger sorted by rank, with the "Other traditions" comparison showing | Rank order, highest attainable rank, and later works offered through the scholarly network ([doc](../implementation/2026-11-15-sefarim-ledger-assessment.md)) |
| | | `study-next-book.jpg` | The study choice, or the study scheme's tooltip | Timing and tooltips ([doc](../implementation/2026-11-11-study-sefer-timing-and-tooltips.md)) |
| | | ★ `jewish-map-mode.jpg` | Jewish map mode with a community card open | Library button, yeshiva line, Beit Midrash card ([doc](../implementation/2026-11-08-jewish-map-category.md)) |
| | | `jewish-cultures-map.jpg` | The Jewish cultures map mode | Culture colours and names ([doc](../implementation/2026-11-08-jewish-cultures-map.md)) |
| | | `realm-communities.jpg` | Realm view of the HRE's Jewish communities | "Capital community" label, tiers |
| | | `community-safety.jpg` | The Community Safety panel | Risk score and planning tasks ([risk](../implementation/2026-11-05-community-safety-risk.md), [planning](../spec/2026-11-08-community-safety-planning.md)) |

Then play a year or two, with no shots needed unless something looks good:

- [ ] **Court size** feels right, not empty or bloated ([doc](../implementation/2026-11-15-court-size-by-prosperity.md)).
- [ ] **Quarter costs**: completing every line should cost about 3,885 gold in total.
- [ ] **Convene a Bet Din:** shoot `bet-din-docket.jpg` mid-case with a source citation showing ([bench sources](../implementation/2026-11-13-bet-din-bench-sources.md)).
- [ ] **Write a sefer** and see it reviewed: shoot `sefer-review.jpg` ([reviews and cherem](../spec/2026-11-11-reviews-and-cherem.md)).
- [ ] **Cherem:** `event kehillah_cherem_debug.3` has your rite's head ban you. Shoot `cherem.jpg`, then check teshuvah with `.5`. **Use a disposable save.**
- [ ] **Succession:** kill Isaac. Check the Continue-as screen and that the style mandate carries over. Re-shoot `succession.jpg` if the new screen looks better.

## C. Granada 1066, as Joseph (crisis and the Nagid)

| ✓shot | ✓test | File | Screen | Check |
|---|---|---|---|---|
| | | `nagid.jpg` | The Nagid office, or the realm view showing "Nagid's seat" | `event kehillah_nagid_debug.1` logs the office state ([doc](../implementation/2026-10-30-nagid-build.md)) |
| | | ★ `crisis-race.jpg` | Crisis window, both bars partly filled, named sources visible | Threat grade, cause line, suggested responses ([grade](../implementation/2026-11-10-crisis-threat-grade-ui.md), [responses](../implementation/2026-11-05-crisis-suggested-responses.md)) |
| | | `crisis-contribution.jpg` | The Armed Host funding row after buying two or three points | **The gold total updates and doesn't stay at 0** (your bug; [doc](../implementation/2026-11-15-compact-crisis-contribution.md)) |
| | | `crisis-toast.jpg` | A catalyst toast with its points | Names and values make sense |
| | | `crisis-neighbours.jpg` | A nearby community's aid, or the map pin | ([doc](../spec/2026-11-12-neighbouring-community-crisis-aid.md)) |
| | | `crisis-held.jpg` or `crisis-struck.jpg` | The outcome event | The accounting scene and street damage ([held](../implementation/2026-11-15-quarter-held-polish.md), [struck](../implementation/2026-11-07-struck-reckoning-and-opener.md)) |

After the outcome, with no shots needed:

- [ ] The ten-year outlook memory shows (-15 for a breach, -5 for unanswered incitement), and the charter term or settlement policy gets worse ([doc](../implementation/2026-11-15-crisis-settlement-outlook.md)).
- [ ] The host issues no new invitations while the crisis is open ([doc](../implementation/2026-11-12-crisis-political-consequences.md)).
- [ ] The recovery cooldown stops a second crisis from opening straight away.
- If Granada doesn't open a crisis when you need it, `event kehillah_crisis_debug.1` opens a warning on your own community.

## D. Granada 1066, as David ben Hezekiah (adventurers)

| ✓shot | ✓test | File | Screen | Check |
|---|---|---|---|---|
| | | `adventurer-camp.jpg` | David's camp with his Dayyan and his brother | Authored family and friends ([doc](../implementation/2026-11-16-david-and-the-exilarchate.md)) |
| | | `settlement-visit.jpg` | Visit Local Settlement in a county with a community: the "call on the community" choice | **The vanilla options and the Leave button still work** ([doc](../implementation/2026-11-15-adventurer-settlement-visit-bridge.md)) |
| | | `community-claim.jpg` | The claim interaction on the Baghdad seat | Both steps of the transfer |
| | | `exilarch.jpg` | Exilarch recognition, using `event kehillah_exilarch_debug.3` if needed | Title and lifetime office |

- [ ] **Found a community** next to an existing one, or under a host without set terms ([doc](../implementation/2026-11-15-adjacent-founding-and-generic-hosts.md)). Shoot `founding-arms.jpg` if the new arms look good.

## E. Troyes 1066, as Rashi

- [ ] Starts with a small library that isn't empty and a poor economy. Missing books cost Greatness only if the rite treats them as foundational ([doc](../implementation/2026-11-15-rite-foundational-library-penalties.md)).
- [ ] Portrait shows the new hairstyle. Shoot `rashi.jpg` if it looks good.

## F. 867: Manasseh, then Shefatiah of Oria

| ✓shot | ✓test | File | Screen | Check |
|---|---|---|---|---|
| | | `khazar-khagan.jpg` | Manasseh's realm, with a Jewish map mode | Landed Jewish ruler, realm communities |
| | | `karaite-community.jpg` | A Karaite community's card | "Kehillah of [place]" name and Karaite rite icon ([doc](../implementation/2026-11-15-karaite-community-seats.md)) |
| | | `minhag-italy.jpg` | The faith screen for Oria or Lucca's rite | Italian/Byzantine minhag ([doc](../implementation/2026-11-12-medieval-rabbinic-minhagim.md)) |

- [ ] 2 Karaite seats exist, and the Sefer ha-Qabbalah families are present ([doc](../implementation/2026-11-08-sefer-haqabbalah-roster.md)).

## G. 1178: the Rambam, then a quick look at Baghdad

| ✓shot | ✓test | File | Screen | Check |
|---|---|---|---|---|
| | | `rambam-library.jpg` | Fustat library or ledger | Rite-weighted seeding for a different rite |
| | | `yeshiva-card.jpg` | Baghdad on the map: the yeshiva card | Green Yeshiva footer with the Rosh Yeshiva icon ([doc](../implementation/2026-11-15-yeshiva-card-footer.md)) |

- [ ] 6 Karaite seats exist.

## H. Optional: late-game states through the console (no gallery shots)

Use a disposable save. Testers are unlikely to get here, so these can ship as "lightly tested".

- [ ] Revolt and Jewish-majority realms: `kehillah_revolt_debug.1` through `.5` ([doc](../spec/2026-11-15-fallen-realms-revolts-and-jewish-majorities.md))
- [ ] Ancestral tombs: `kehillah_ancestral_tombs_debug.1` ([doc](../implementation/2026-11-15-ancestral-tombs.md))
- [ ] A library moving to a county temple ([doc](../implementation/2026-11-15-county-library-preservation.md))
- [ ] Sittings hosted by AI communities through a stand-in ([doc](../spec/2026-11-15-ai-hosted-sittings-via-stand-in.md))

## Not for this release

- **Yeshiva study planner**: still being built in another session as of 2026-11-16.

## Afterwards

- Point the README image links at the new shots, and replace `realm-pillars.jpg` and `library.jpg`.
- Regenerate `docs/release/thumbnail.png` (640×640, under 1 MB, title band at the bottom) from
  the best new image if it beats Troyes.
- Update the screenshots on `tester-guide.html` and republish it to the same link.
- Write a dated `docs/testing/` log of what passed and failed, and mark each doc's Status line.
