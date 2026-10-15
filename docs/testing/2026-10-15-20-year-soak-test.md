**Status:** soak-test report, 2026-10-15. Findings and recommendations only; nothing was changed in the mod. The soaked build was commit `ab31f90` (tip of `autonomous/shabbat-2026-10`), in a private instrumented copy. The player was Worms, 1066 to Feb 1087 (20.4 game years). A Sonnet subagent played; an Opus orchestrator analysed the logs. Compare the [2026-10-12 soak](2026-10-12-balance-soak-test.md) and the [V33 soak](2026-10-13-v33-pressures-soak.md).

# 20-year soak: how the game feels (2026-10-15)

## Method

- **Isolated game.** CK3 1.20 ran with `-debug_mode -develop` under a separate `-userdir` (`C:\Users\Daniel\ck3soak\profile`). The mod was a `git archive` of `ab31f90` at `C:\Users\Daniel\ck3soak\mod`. Two Codex CK3 instances ran alongside it and were left untouched.
- **Instrumentation (copy only, never the repo).** A script inserted into the `immediate` block of all 544 mod events:
  - `debug_log = "KSOAKP <id>"` plus the date when the root is a player;
  - `KSOAKA <id>` when the root is an AI.

  It also logged `KSOAKMSG <file:line>` before each of the 56 player-scoped `send_interface_message`/`toast` calls. The counts below are therefore real firings, not estimates. ck3-tiger on the instrumented copy matched the clean copy: no new errors, and one `scope = none` event was given a scope-free probe.
- **Yearly snapshots.** Console run files logged the player and all 19 seeded communities' S/P/G, fame, gold, leader age and danger. Communities founded during play (Konstanz, Ingolstadt) are not in the snapshots.
- **Play.** The agent played as an engaged player and journaled all 55 popups: text, options, choice, and flags. Every 4-5 years, and after each succession, it took a look-around pass through the decisions, the Quarter, the council and the court.
- **Raw data** is outside the repo, in `C:\Users\Daniel\ck3soak\out\`:
  - `journal.md`;
  - `logs\run1_debug.log` (12.8 MB, below the ~18 MB log cap);
  - `logs\run1_error.log`, `logs\error_baseline.log`;
  - the save `Rav_Yossi_of_Kehillah_of_Worms_1087_02_17.ck3` in the profile.

## Run summary

- **No crashes.**
- **Two successions, both clean:**
  - Isaac (died 1079, aged 79) to Akiva, his Shtadlan and heir;
  - Akiva (died 1086, aged 58) to Yossi.

  Each showed the mod's death-screen paragraph, and play continued without the `play` console command.
- **Player actions:**
  - Send Out Settlers twice, founding Konstanz (1071) and Ingolstadt (1079);
  - Write a Sefer once;
  - Learn Torah;
  - Set the Community's Goal twice;
  - a Hekdesh upgrade to level 2 (220 gold);
  - filling the empty Ne'eman and Shtadlan council seats.

## Frequency: what actually fired

**Player-rooted mod events: 60 firings of 25 distinct events in 20 years, about 3 a year.**

| Event | Times | Comment |
|---|---|---|
| `kehillah_yeshiva.0320` The Graduating Class | 14 | Yearly from 1075 on. Same text each time; only the name and the count change. |
| `kehillah_invitation.0001` An Invitation to Settle | 9 | Single option. Senders: Poland, the Papacy, Toledo, Croatia, Pisa, Kairouan, Barcelona, Granada. |
| `kehillah_study_torah.*` (Course of Study / Companion) | 7 | The same two texts verbatim. |
| `kehillah_settlement_conditions.*` / `kehillah_settlers.*` / `kehillah_goals.0001` | 15 | Decision chains; these feel good. |
| `kehillah_book.0001-0006` (Sefer chain) | 6 | One chain, a strong payoff. |
| `kehillah_accusation.*`, `kehillah_incident.0001/.0010/.0090` | 5 | The best content in the run. |

**Never fired in 20 years, for anyone, AI included:**
- **All 26 `jewish_holidays` events and `jewish_holiday_feast`.** This is a bug; see below.
- **All Bet Din content:**
  - `kehillah_bet_din` (42 events), `kehillah_din_sources` (78), `kehillah_bet_din_travel`, `kehillah_bet_din_semicha`, `kehillah_responsa`;
  - the Bet Din conference activity was never held, by the player or any AI.
- **Other systems with no firings:**
  - conversion and anusim;
  - expulsion, refugees and exiles;
  - pogrom and aftermath;
  - the mob spike, children, loan challenge, and the Jewish pope.

Some of these are rare by design, and nobody in 1066-1087 hit a crusade or expulsion. But Bet Din and holidays are meant to be everyday content.

**Side-feed messages to the player: 238 in 20 years, about 12 a year.**
- `kehillah_community_news_effects.txt:25`: 75;
- yeshiva notices (`kehillah_yeshiva_effects.txt` 1236/1259/878/907): 113;
- book news: 15;
- household: 13.

They arrive in clusters of 3-5. This is down from the 2026-10-12 soak but is still the largest non-actionable stream.

**AI-rooted mod events: 665.** The top source is `kehillah_yeshiva.0102` (111). The other busy ones are settlement-conditions, study, goals, task contracts and books.

**Vanilla popups: about 14.** From 1074 on, the ageing leader's vanilla decline chain dominates: Where Am I, Dim Vision, Prisoner in My Own Body, Lessons Unlearned, Close to the End, Aching Bones.

**Quiet stretches.** Aug 1071 to Feb 1073 had no popups at all. Sep 1080 to Mar 1082 had nothing but the yearly Graduating Class.

## Pillars and economy (snapshots)

| Date | Communities | Avg S / P / G | Avg danger | Stability bands | Prosperity bands |
|---|---|---|---|---|---|
| Oct 1066 | 19 | 648 / 378 / 363 | 20 | 18 Healthy, 1 Flourishing | 12 Strained, 7 Healthy |
| Feb 1076 | 19 | 724 / 411 / 451 | 25 | 11 Flourishing, 8 Healthy | 10 Strained, 9 Healthy |
| Apr 1084 | 19 | 747 / 437 / 483 | 34 | 11 Flourishing, 7 Healthy, 1 Legendary | 12 Healthy, 7 Strained |
| Jan 1087 | 19 | 726 / 427 / 499 | 39 | 9 Flourishing, 9 Healthy, 1 Legendary | 9 Healthy, 10 Strained |

- **Worms (player), 1087:** S 994, P 565, G 1056, fame 176, danger 57, gold 477.
  - Stability and Greatness reached Legendary by about 1079 and stayed there.
  - The Realm panel showed "falling" on pillars that never visibly moved.
- **The 2026-10-12 complaint (everything flat around 200) is fixed.** The swing has gone the other way, though. No community was in Crisis or even Strained Stability at any point. The player sits at Legendary with no effort, so the pillars stopped telling a story after about 1072.
- **AI economics.** Three AI communities ended with negative gold (Córdoba -68, Mahdia -28, Narbonne -19), while the player banked about +2.5 a month. Danger rises steadily (20 to 39 on average, Worms 57), which is the only slowly worsening number.
- **Gold has no pull.** The player's only real sink, a Quarter building upgrade, was found by the agent's own exploration after 13 years. No event or notice points at it.

## Bugs (confirmed against source)

1. **Holiday events never fire: a regression from `aeba30e` (2026-10-13).** [jewish_holiday_on_actions.txt](../../common/on_action/jewish_holiday_on_actions.txt) replaced the weight `300 = 0` with `chance_of_no_event = { value = 300 ... }`. `chance_of_no_event` is a percentage: vanilla's `_on_actions.info` example uses 10, and vanilla `yearly_on_actions.txt` uses 30-95. So 300, or 150 with Ritual Celebrations, always means no event. To keep the rates that commit's comment intends (11.6%, or 15.9% with the tenet, under `chance_to_happen = 25`), use `value = 54` and `value = 36` with the tenet, instead of `multiply = 0.5`. The 2026-10-12 soak still saw Purim, Hanukkah and Rosh Hashanah events, so they used to work.
2. **Raw `GetFirstName` in the "Artifact Gained!" toast.** In [kehillah_book_news_l_english.yml](../../localization/english/kehillah_book_news_l_english.yml), artifact names such as `kehillah_book_artifact_name_talm_damages` use `[creator.GetFirstNameNoTooltip]`, and no `creator` scope exists where the artifact name is built. Seen live after Akiva's death, with matching error.log lines.
3. **"1 of the yeshiva's students have received semicha"** (`kehillah_yeshiva.0320.desc`). A singular variant is needed for a class size of 1. It happened 3 times.
4. **The Sefer chain's final-revision event (Jul 1071) showed an empty title bar.** From the journal; the exact event id was not pinned down.
5. **Book-effect tooltip errors.**
   - [kehillah_book_effects.txt](../../common/scripted_effects/kehillah_book_effects.txt) lines 209/213/274/281: "Script system error while building tooltip".
   - `kehillah_book_tier` is read unset in `kehillah_book.0005`'s immediate block (12 times).
   - The library-ownership triggers (`kehillah_scripted_triggers.txt` around lines 1047-1113) each erred once.
   - The 2026-10-12 soak's `kehillah_book_genre` error is gone.
6. **Missing loc keys `kehillah_succession_text` and `kehillah_vanilla_succession_text`** (the KehillahSuccessionText custom loc) are reported at startup. The death screen still showed the right paragraph, so this may be a dead fallback; it needs checking.
7. **Likely raw keys in Quarter building tooltips (ck3-tiger, not seen live).** 11 `domicile_building_parameter_kehillah_*` keys have no localization, for example `unlocks_treasurer`, `has_mikvah`, `prominent_quarter` and `has_yeshiva`. Only `kehillah_holds_library` has text.
8. **The Hekdesh tooltip says "Camp gains additional moderate resistance to Plagues".** That is vanilla domicile wording.

Static "variable used but never set" warnings are worth a pass, since each one may be a dead branch: `kehillah_mob_asked_men`, `kehillah_mob_tried_defence`, `kehillah_case7_pending_responsum`, `kehillah_case7_correspondent`, `kehillah_case7_asking_title`, `kehillah_kohen_gadol_portrait`. Otherwise mod runtime errors are few; most of the 12k error.log lines are vanilla or static checks.

## Does it feel alive and realistic?

**Where it works.** The incidents are the best thing in the mod:
- *An Accusation* (1077): a blood libel, four real options with vanilla odds, and a follow-up.
- *The Talmud on Trial* and *What Came of It* (1085): an apostate with a list of passages, a Learning challenge, and books that come home with pages missing.
- *The Badge* (1080).

These read like history and the prose is restrained. The Sefer chain and Send Out Settlers both end in something concrete: a legacy payoff, and a real new community on the map. The first Graduating Class choice (keep him, send him where there is no rabbi, or recommend him to the Kaiser) is the right kind of decision.

**Where it doesn't.**
1. **The weekly life of the community is absent.**
   - No festivals ever fired (bug 1).
   - No Bet Din case ever came before the leader.
   - Nobody in the community asks the leader for anything.

   Between incidents, the community exists only as numbers and side-feed notices. The mod's most characteristic content — holidays, the court, petitions — is exactly what never appeared.
2. **The same few things repeat.** Graduating Class 14 times, Invitation 9 times, Course of Study 4 times and A Charter Is Sealed 3 times. All are single-option or near-identical, and they make up about half of the mod popups. A player learns to click through them.
3. **The pillars stop meaning anything.** Legendary by about 1079, with nothing to lose; the "falling" labels never visibly move.
4. **The incidents are early.** The badge (Christian hosts, Lateran IV 1215) and the Talmud trial (Paris 1240) both fired in the 1080s. The director adds weight after 1215/1230 but allows both from 1066 at base weight. A protective (62) Kaiser decreeing a badge in 1080 also strains belief.
5. **Vanilla text intrudes on the leader's life.**
   - The obituary calls the scholar-leader "conniving ... pettiness and spite" and says he died "rarely leaving his castle".
   - Gibbering Fool, a pronunciation joke about "gibbet".
   - Two copies of "Someone Else" six years apart, on the same date.

   This is vanilla behaviour, but it is what the player sees most of from about age 70.

## Where the loop is shallow or broken

- **No recurring choice with real stakes.** Decisions are one-click: Tzedakah, the goal, Learn Torah. The Write a Sefer decision's first event, "What to Write", offers a single option.
- **Gold accumulates and nothing asks for it.** The Quarter upgrade is the sink, but it is never surfaced.
- **The Bet Din conference is invisible.** The agent never found it in 20 years of looking around decisions, council and court. The AI never hosts one either, so 120+ events are dark.
- **Invitation to Settle is all noise and no choice.** See the proposal below.
- **Succession is now smooth**, but each one replays an identical *A Charter Is Sealed* and repeats the "New Dayyan" toast for an unchanged Dayyan.
- **UI notes:**
  - Hyperlinks inside option text swallow clicks.
  - In a 2048x1152 window the decision panel's "Take decision" button sits below the window edge; the agent used Enter.

## Proposal: invitations, rarer and more historical (discussed with Daniel 2026-10-15)

Today [kehillah_open_door_candidate_trigger](../../common/scripted_triggers/kehillah_invitation_triggers.txt) admits any AI independent Christian or Muslim duke or greater with no community whose capital is within `squared_distance_large` (650 px, "one France") of any community. Each such ruler gets a flat 5% yearly review (`kehillah_invitation_review_chance`). Every Kehillah player in diplomatic range with any reachable county then gets the full letter. In this run that meant 11 invitations worldwide by 1081, 9 popups for Worms, and every one a single option.

Proposed (not yet built):
1. **Distance: medium, measured from the realm, not the capital.** Require some county in the ruler's realm within `squared_distance_medium` (250 px, "one Ireland") of a community's quarter. A capital check at 250 px would wrongly exclude large realms whose Jewish frontier is far from the capital.
2. **Stricter gates, all required:**
   - no community of their own;
   - outlook Well-disposed or better;
   - at least one concrete motive:
     - a stewardship wealth or domain lifestyle focus;
     - short of cash (in debt, or gold below a few months' income);
     - stewardship 14+ with diligent, ambitious or greedy;
     - recent devastation (occupied or raided counties).
3. **Theocracies may invite** (Daniel: "seems historical, e.g. Avignon"; compare the papal Comtat Venaissin's "Juifs du Pape"). Lift the independent duke-or-greater limit far enough to allow bishops and counts whose liege does not ban Jews. Bishop Rüdiger of Speyer's 1084 charter is the in-period example.
4. **Weighted chance, not a flat 5%:** about 2% a year plus 2-3% per motive. Target roughly one invitation every 3-5 years worldwide.
5. **An expulsion nearby triggers reviews** (Daniel). When a ruler expels Jews, eligible rulers within medium distance of the expelling realm get an immediate review with a bonus. This is the historical pattern of refugees welcomed next door: Provence and the Comtat after 1306, the Ottomans after 1492. It ties into the existing refugee and exiles systems.
6. **An open invitation attracts Jewish adventurers** (Daniel). While an invitation is open, Jewish landless adventurers and wanderers are drawn to the realm. The natural-founding and settlers-gate logic should weight invited counties highly, so the invitation produces communities even without a player.
7. **Player-facing:**
   - the full popup only for invitations from a realm the community could realistically answer, at most about once a decade, with everything else as a side-feed notice;
   - real options in the letter: send families now (into Send Out Settlers with this lord's county), send the Shtadlan to negotiate terms (the existing Seek an Invitation task), or decline;
   - drop the "(10)" outlook number from the prose (no numbers in loc) and show it through the vanilla tooltip.

Knock-on: settlers and exiles depend on open invitations, so rarer invitations mean fewer new communities. Items 5 and 6 and the Shtadlan's task should keep the map growing.

## Top recommendations, in order

1. **Fix the holiday `chance_of_no_event` regression** (bug 1). It is one line and restores the most flavourful everyday content.
2. **Find out why no Bet Din conference was held in 20 years.** The AI side is already at its maximum: `ai_will_do = 100`, re-checked every 6 months (`kehillah_bet_din_conference.txt` around line 624). Zero conferences across 19 communities therefore points to a failing gate, not to AI reluctance. The candidates are:
   - `kehillah_region_can_field_bet_din_panel_trigger`;
   - `kehillah_has_community_rabbi_trigger`;
   - the 1.20 activity cost or validity.

   A debug probe evaluating those per community would settle it. Separately, put the Bet Din in front of the player: a nudge event when cases are pending, or a case arriving as a popup with "convene the court" as an option. Startup also logs duplicate default invite rules for this activity (4 lines).
3. **Cut repetition:**
   - make the Graduating Class choice an event only when it matters (an exceptional student, or a community lacking a rabbi), with a quiet feed line otherwise;
   - give A Charter Is Sealed a short "renewed" variant for successions;
   - add variant texts for Course of Study.
4. **Invitations, per the proposal above.**
5. **Tension on the pillars.** Make Legendary harder to keep: a higher upkeep, decay toward Healthy, or danger biting into Stability. The player should feel at least one dip in 20 years.
6. **Date-gate the anachronistic incidents for Christian hosts:** the badge before 1215 and the Talmud trial before 1230, either banned or at a very small weight. Make the badge rare under a protective lord.
7. **A gold sink with a prompt.** A notice or event when the treasury passes a threshold ("the elders ask about the Hekdesh roof"), pointing at the Quarter upgrades.
8. **Text fixes:** the GetFirstName artifact names, the plural "students have", the empty Sefer revision title, the Hekdesh "Camp" wording, and the missing building-parameter loc.

## Not covered by this run

- **Probe gaps.** The player probe's age/piety/prestige fields printed 0, a probe problem, so player piety and prestige were not tracked. The founded communities (Konstanz, Ingolstadt) are missing from the snapshots.
- **Systems that never triggered in 1066-1087** — crusade, expulsion, conversion, mob and pogrom (except as feed notices in Jan 1084) — are untested here.
- **Popup texts were read from screenshots.** Only one crop was saved, so the journal's wording is the record. The UI items (empty title, raw toast text) were not re-verified by a second screenshot.
- **The other CK3 instance interfered.** One Codex CK3 window (PID 11076) sat TOPMOST on the primary monitor for much of the run. Two of the agent's screenshots captured that window instead, but no input went to it.

## Addendum, 2026-10-15 afternoon: fixes and a partial verification run

Daniel reviewed this report the same day. The fixes and new mechanics are recorded in [V44](../spec/v44-persistent-pressure.md). A second Sonnet agent played a fresh Worms 1066 game on an instrumented copy of the fixes. It ran from 11:41 until the session usage limit stopped it at about 1078 (12 game years); its journal is `C:\Users\Daniel\ck3soak\out2\journal.md`. That copy predated the invitation redesign, the Bet Din decision and suggestion, the treasury suggestion, the activity rename and the player holiday rate, so those are tiger-clean only.

**Verified live:**
- **Holidays fire again:** 61 holiday events for AI characters by 1078, after zero in the whole soak. None reached the player in 12 years, though. The old design rate (about 12% a year) was too low to be seen, so the player's rate is now about 60% a year (75% with Ritual Celebrations). This retune is not yet verified.
- **Graduating Class:** a popup in Feb 1069 and Feb 1076 (7 years apart), otherwise notices. Yeshiva notices fell to about 2.7 a year (32 in 12 years).
- **The Charter Renewed:** shown after Isaac's death in Nov 1077, with the clerk scene and the four terms.
- **The Servants' Decree:** fired Nov 1076 under Heinrich IV. The petition succeeded, and "What Came of It" read correctly.
- **Text fixes:**
  - the Learn Torah requirements show "You are not incapable" and the new library line, with no BUG text;
  - the Hekdesh tooltip reads "Residents gain ..." and no longer says "Camp";
  - the Stability footing shows +400;
  - "One More Pass" has its title.
- **Bet Din:**
  - The player hosted a full sitting from the Activities list (F9): three cases, rulings and "The Docket Is Closed". The soak agent had simply never found it there.
  - **AI hosting is still unconfirmed.** The four AI-rooted Bet Din events by 1078 were all steps inside the player's own sitting (cases `.0042`/`.0062`/`.0082` and an invited judge's travel), interleaved with it in the log. No AI community hosted. Whether the invite-rule fix alone was enough is unknown. The yearly `ai_attempt_to_host_activity` nudge (V44 section 5) is the fix under test.
- **New bug found:** a ruling tooltip showed the raw key `kehillah_bet_din_dismissed_mysticism_opinion`. That modifier and four other opinion modifiers had no loc; all five now do.

**Not yet verified live:**
- the invitation redesign;
- Convene the Bet Din and Cases Await the Bet Din;
- AI Bet Din hosting with the yearly nudge;
- The Treasury Is Full;
- the "Sitting of the Bet Din" rename;
- the new pressure terms in an actual decline;
- artifact names with the author's name (the run's book was an unnamed work type).
