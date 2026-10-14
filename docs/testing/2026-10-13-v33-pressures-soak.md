**Status:** soak-test report for V33 pressures ([spec](../spec/v33-pressures.md)), 2026-10-12/13: Worms 1066 to 1117, 51 game years. Findings only; no tuning decided yet. Raw data is in the session scratchpad, not the repo. Compare with the [first soak](2026-10-12-balance-soak-test.md).

# V33 pressures soak report (2026-10-12/13)

## Run summary
- ck3.exe -debug_mode -develop, Worms 1066 bookmark, Isaac (9000002), tree at 270093e + uncommitted working-tree edits (traits/icons, not pressure code). No mod files edited by me.
- Observed 15 Sep 1066 -> 1117-03 (51 game years): probes every ~3-4 yrs, 17 usable snapshots (dates: 1070-01 ... 1117-03). **Gap: 1097-03 -> 1099-01 not observed** (debug.log hit its ~18.1 MB cap at ~1097; I noticed late, killed, relaunched from the autosave of 1 Jan 1099; run 1 logs kept as v33_debug_run1.log). 1066-1070 was not probed after the first (init) probe (stability/prosperity/greatness vars read 0 at 1066-09, as in the previous soak: they are lazily initialised).
- Player play: first/default option for every event (template clicker), no decisions at all (no Distribute Tzedakah this run - pure low-effort play). Successions: Isaac -> Chananya Landsberg (1079) -> Menashe Nehardai (1103); all clean.
- Crashes: none. ck3 alive and responsive at the end; I killed only my own process (22496). No hot-reload incidents seen.
- Registered communities: 19 at start, 23 from 1070 (four dynamic "x_d_laamp_779..782" communities appear and are registered; see Findings).

## Band distribution per snapshot (23 communities; S=Strained 150-399, H=Healthy 400-699, F=Flourishing 700-949; C=Crisis <150 incl. uninitialised new ones)
| Date | Stability | Prosperity | Greatness | avg S / P / G | courtiers over cap | avg courtiers / cap |
|---|---|---|---|---|---|---|
| 1070-01 | H19 C4 | S14 C9 | F1 H6 S12 C4 | 482/171/328 | 7 | 26.7/28.3 |
| 1075-01 | H19 C4 | S12 C11 | F1 H6 S12 C4 | 501/169/347 | 14 | 28.5/28.0 |
| 1082-08 | F1 H18 C4 | S15 C8 | F1 H8 S10 C4 | 495/186/372 | 17 | 32.2/28.8 |
| 1090-01 | H19 F1 C3 | S17 C5 H1 | L0 F2 H8 S10 C3 | 540/209/397 | 15 | 33.8/29.9 |
| 1097-03 (First Crusade on) | H19 S3 C1 | S19 C3 H1 | L1 F2 H10 S8 C2 | 500/217/447 | 11 | 32.8/30.7 |
| 1099-01 (crusade on) | H17 S4 F1 C1 | S18 C4 H1 | F2 H11 S9 C1 | 489/221/462 | 10 | 32.9/30.7 |
| 1102-05 (crusade over) | H22 C1 | S20 C2 H1 | L1 F2 H11 S8 C1 | 545/227/476 | 14 | 33.4/31.4 |
| 1107-02 | H21 F1 C1 | S21 C1 H1 | L1 F2 H12 S7 C1 | 594/226/484 | 10 | 29.6/31.3 |
| 1114-01 | H18 F4 S1 | S18 C4 H1 | L1 F3 H12 S7 | 601/225/503 | 7 | 29.0/32.1 |
| 1117-03 | H21 F2 | S18 C3 H2 | L2 F2 H13 S6 | 600/230/529 | 7 | 29.0/33.0 |
(Full 17-row series are in soak33_table.txt / snaps33b.json in the scratch dir; the "C" in Stability up to ~1099 are the 3-4 new x_d_laamp communities, not real Crisis.)

## Per-community time series (Stability), selected columns
Dates:  70-01 79-04 90-01 93-08 97-03 99-01 02-05 07-02 14-01 17-03
- worms     641 744 690 647 429 388 487 543 541 541
- speyer    523 602 597 575 461 434 509 551 608 656
- mainz     622 649 668 662 558 552 555 642 537 560
- troyes    538 575 645 630 559 525 631 615 536 550
- paris     603 477 520 562 527 410 524 651 566 442
- cologne   556 554 576 571 399 392 502 529 628 646
- praha     589 584 536 560 530 452 516 600 703 710
- narbonne  617 585 652 608 491 492 616 667 574 590
- lunel     635 537 662 612 462 442 583 631 628 530
- toledo    604 624 657 686 620 619 622 700 638 690
- granada   574 651 586 620 676 716 677 746 711 725
- baghdad   470 563 608 605 614 588 576 601 540 563
- lucena    595 629 656 633 637 640 641 683 759 696
- jerusalem 576 587 618 550 552 554 552 571 603 616
- mahdia    542 525 575 559 572 544 487 544 536 563
- sura      592 640 727 661 614 633 646 655 576 554
- x779      0 0 0 0 0 0 -25 -25 391 518      (new community; see findings)
- x780      0 0 226 576 527 497 629 685 541 554
- x781      0 0 0 201 347 368 528 662 704 699
- x782      0 0 0 -25 200 338 478 546 645 634
Prosperity (same dates): worms 316 314 353 344 319 326 334 317 312 319 | speyer 194 196 220 236 232 239 243 225 202 196 | mainz 169 229 247 266 277 304 343 359 319 326 | troyes 115 117 124 105 95 92 97 119 116 116 | paris 187 173 206 204 206 133 170 178 185 84 | cologne 198 184 178 212 243 266 322 357 392 409 | toledo 250 311 414 417 445 455 428 425 405 413 | beziers 144 146 175 169 168 183 182 211 286 302 | lunel 145 119 246 243 221 218 219 239 297 323 | mahdia 158 143 240 225 197 200 174 196 174 214 | jerusalem 208 227 245 226 233 236 240 233 212 212 | baghdad 177 226 274 269 264 260 220 221 224 212.
Greatness: worms 708 -> 861 -> 915 -> 956 (1097) -> 987 (1114); baghdad 480 -> 986 (1117, Legendary); narbonne 589 -> 836; others 270-580, yeshiva-driven as before.

## Did the pillars move? Yes.
- Stability: now mostly Healthy (avg ~480-600, per-community ranges typically 400-300 wide, e.g. Worms 388-744, Granada 546-746, Cologne 392-646, Lunel 442-662). Previous soak: flat ~200 for 60 years. Stability now reacts to the world and recovers.
- Prosperity: moves much less. Most communities live in a ~100-wide band for 50 years; 21/23 stay Strained or Crisis the whole game. Only Toledo ever reaches Healthy (414-455). Growth is slow drift of the baseline (e.g. Cologne 198 -> 409, Mainz 169 -> 359, Lunel 145 -> 323, Beziers 144 -> 302) driven by the county-economy term/ buildings, not by pressures.
- Pillars track baselines closely (S within ~20-80 of baseline, P within ~15), so the 15%/5% convergence is fast: a pressure is fully "felt" within about a year.

### Biggest swings and the term responsible
1. **First Crusade, kehillah_bd_holy_war_value -150**: appears 1096-97 on 16 of 23 communities (all Christian-host ones + the x_ ones), gone by 1102. 1093-08 -> 1097-03: Worms -218 (647 -> 429; baseline 479 -> 369 with host -60, holy war -150), Cologne -172, Lunel -150, Beziers -124, Vienna -123, Narbonne -117, Speyer -113. Worms bottoms at 388 (1099-01). 1099 -> 1102-05 recovery: Lunel +141, x780 +132, x781 +159, x782 +140, Worms +99 (388 -> 487), then 552 by 1103. No community stuck in Crisis; every one recovered within 4-5 years of the crusade's end. Stability average 489 -> 545 -> 594.
2. **Host attitude (kehillah_bd_host_attitude_value)**: the most important permanent term. Typical value -20..-60 (mean about -40..-60 across snapshots); extremes -130/-180 for Baghdad, Sura, Mahdia (Muslim/zealous hosts), +20/+30 for friendly hosts. Worms host +20 (1082-90, S 714-720) -> -60 (1093 onward, baseline 479-519): a ~200 swing on a host change, cited at Worms 1090-01 -> 1093-08 (S 690 -> 647, baseline 714 -> 479).
3. **War (kehillah_bd_war_stability_value -40, host at war)** is the commonest term: 8-20 of 23 communities at any snapshot, mostly the flat -40; a single -160 (occupation+raid) hit Paris 1114-01 -> 1117-03 (S 566 -> 442, P 185 -> 84; Prosperity -101: war_prosperity -125 + econ -50). Paris is the best example of a localised war: both pillars fell in one snapshot, and it will probably recover later (not observed - run ended). Mahdia 1070 -> 1075: war prosperity -125/+150 swung P 158 -> 103 -> 54 -> 126.
4. **Policy (kehillah_bd_policy_stability_value)**: only +40 (Encouraged) appears (4-7 communities); no Discouraged/Banned host observed in 51 years, so the -100/-250 branches are unobserved.
5. **Teaching (kehillah_bd_host_teaching_stability_value)** was +30 for every community at every snapshot (22/23 at 1107; "protective"), and **religious tension** was -30 for every community at every snapshot. These two are uniform and cancel exactly (net 0): they add no differentiation and no movement. The strict (-80) and exclusionary (-200) teaching branches were never observed.
6. Stability baseline floor 500 + structural buildings gives sb of 340-715; combined with host/war terms the bulk lands 400-700.

## Stuck / pinned communities
- No community pinned in Stability Crisis long-term. Stability never got near the Legendary cap; max 759 (Lucena 1114), a few reach Flourishing late (4 at 1114-01).
- Prosperity: Troyes is stuck in Crisis for 51 years (77-124, baseline 89-139); Paris 84-206, Mahdia 54-240 touch Crisis. Prosperity pinned in a Strained band for 18-21 of 23 communities for the whole run. Worms P is nearly constant (303-353) regardless of Crusade/war: wars through the county hit Worms hardly at all (its county is rarely occupied).
- Greatness: Worms reaches 956-987 (Legendary from 1097), Baghdad 986 at 1117; no pillar sits at the cap otherwise.
- **x_d_laamp communities (dynamic, 779-782)**: Stability var reads 0 (uninitialised) for 20-40 years: x779 had S=0 AND P frozen at exactly 220 and G=15 from start to 1107 (no pillar tick at all), then S -25 (!), 82, 391, 518; x782 S -25 at 1093; x781 0 until 1093; x780 0 until ~1086. Negative Stability (-25) shows the value is not clamped at 0 at creation. These communities look un-ticked until something triggers their first quarterly pulse; P frozen at 220 for 40 years suggests x779's holder may not have been receiving the quarterly pulse. Treat as a likely bug or at least an init gap (outside V33 itself, but visible because V33 baselines never get applied until the first tick).

## Comparison with previous soak (flat ~200/~190)
- Stability: 200 -> 480-600 average, with range and recoveries. Prosperity: 190 -> 170-230 average, ~unchanged distribution (Strained), but with real divergence between communities (54-455 vs 66-333 before). Greatness unchanged in shape (yeshiva fame driven).
- New: crusade-driven dip of ~100-220 and a ~4-year recovery; war and host swings; Paris occupation-like hit.

## Courtier count vs capacity
- Capacity 22-54 (avg 28 -> 33 as buildings are added), counts avg 27 -> 34 (peak around 1090) -> 29 by 1117. Over capacity: 7/23 (1070) rising to 17/23 (1082) and 15/23 (1090), down to 7/23 at 1114-1117. Extremes: Paris 42/24, Praha 51/24 (1090), Baghdad 42/34, Troyes 25/24, Mainz 52/30 (1090). Worms 50-54 against cap 54 (touches 54/54 at 1086, 1102, 1103), i.e. Worms essentially lives at the cap.
- Since overcrowding no longer drains Stability, being over cap has no visible consequence in this data; it mostly just reads as a soft number. The cap is "sensible" as a long-run average (matches counts +/-10%), but the Prosperity-poor communities (Troyes, Paris, Praha: cap 24) sit permanently 20-100% over because capacity is dominated by buildings/prosperity bonus that those never build/earn. I did not observe what overcapacity actually does (no per-community effect probe).

## Errors
- No error.log lines mentioning kehillah_pressure or capacity in either run. Run 2 has 36 lines for kehillah_bd_urban_opportunity_stability_value ("Could not fetch title or province from scope 'county'", kehillah_breakdown_values.txt:375/379) all at 00:23:41, which is a tooltip build (GUI), likely triggered while a tooltip was open on a Worms pillar panel; not from the probe. Check once manually (probably a domicile_location.county unset in some scope) - not a pressure_term file.
- Run 1: 36 x "Failed to fetch variable 'kehillah_var_stability/greatness/prosperity' due to not being set": caused by my probe reading var: on not-yet-initialised communities (probe artifact, not game bug; but confirms 3-4 communities had unset vars). 71x "Event kehillah_debug.N is orphaned" and 126x kehillah_host_arrest_triggers.txt errors (kehillah_quarter_under_imprisoner_trigger) are pre-existing/unrelated to V33 (not investigated).
- Other errors are vanilla (laamp triggers, ep3 interactions, activity_hunt, court position duplicate).

## Recommendations (numbers)
1. **Give Prosperity a floor like Stability**: kehillah_prosperity_baseline_floor_value = 250 (or 150 + development_level*8) so no community is stuck at 54-130 (Troyes 77-124 for 50 years, Paris/Mahdia). At present 18-21/23 sit at 150-400 and 22/23 never reach Healthy; floor 250 + the existing positive terms (stewardship, buildings) would put active communities at 400-500, and wars/hosts (-25..-150) then matter. Alternatively scale the local-economy term: development*4 -> development*8 (typical dev 10-25 gives 80-200 instead of 40-100).
2. **Make the permanent terms discriminate**: teaching +30 and tension -30 were identical on all 23 communities for 51 years and cancel. Either make teaching real per-host (observe strict/exclusionary at all; e.g. none seen in 51 years) or drop tension to 0 for communities whose host is Jewish-tolerant (+15 net). Meanwhile, host attitude -40..-60 (mean) is already the swing term; keep as is.
3. **Crusade dip is right-sized but short**: -150 produces -100..-220 and ~4 years to recover (Worms 388 -> 487 -> 552). If you want the First Crusade to be a threat to Stability bands rather than a dip inside Healthy, raise to -250 for hosts in the crusade's target faith's realm or add a one-off event; leave -150 elsewhere. Alternatively leave as is; no tuning needed for functional pressure.
4. **Initialise new/dynamic communities** (x_d_laamp_779-782: S=0, -25, frozen P=220 for 40 years): run kehillah_quarterly_pillars_effect once and clamp S/P/G at >= 0 on community creation; otherwise these show S=0 for 20-40 years.
5. **Courtier capacity**: raise the Crisis base 20 -> 24 or add +2 per 10 development so small communities (Troyes/Paris/Praha cap 24) are not 20-100% over; or decide overcrowding should have a visible consequence (a small -10 to -20 Stability, not -8 flat) since otherwise being over the cap is meaningless. Keep per-tier +2.
6. Not observed (cannot validate): Encouraged vs Discouraged/Banned policy -100/-250, strict/exclusionary teaching -80/-200, occupied -200, raided -120, crusade in non-Christian realm (jihad), host change effects other than Worms 1090-93. Suggest a targeted debug-event run to confirm numbers rather than waiting for them to occur.

## Not observed / caveats
- No data for 1097-03 -> 1099-01 and 1066-1070 (init). Debug.log cap again cost the 1097-1099 window.
- Player decisions were not exercised (no Tzedakah, no Set the Goal), so player-action influences on pillars were not tested. Worms may be somewhat lower than a played game.
- Snapshot cadence 3-4 yrs hides sub-snapshot events (e.g. raids, occupations lasting <1 year).
- Probe read at arbitrary intra-year moments; pillars update quarterly per leader pulse, so values are pre/post-tick noise (+/-15).
