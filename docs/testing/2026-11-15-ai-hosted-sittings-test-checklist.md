**Status:** NOT RUN — written 2026-11-15 for Daniel's interactive live test of [AI-hosted Sittings via a stand-in](../spec/2026-11-15-ai-hosted-sittings-via-stand-in.md). xTiger: 0 new reports.

# AI-hosted Sittings — live test checklist

Every log line starts `KEHILLAH_BD_AI` in `debug.log`. Before starting, note the time, so that new `error.log` lines can be told apart from the startup noise.

## 1. An AI Sitting starts and is handed over

1. Start 1066 (Worms) in debug mode and unpause for a day.
2. Console: `event kehillah_bet_din_ai_debug.1`.
   - Expect an `ATTEMPT via stand-in` line naming the leader and the stand-in, or `ATTEMPT direct` for a landed Kehillah leader.
   - `NO_STAND_IN` or `no AI leader can convene` means try again, or note which gate is failing.
3. Play about 10 days.
   - Expect `HANDOFF PASS` naming the same pair, then an `INTENT ...` line and several `GUEST added` lines.
   - `HANDOFF ABORT` means the leader had left his Quarter or was busy; note it and repeat step 2.
   - No HANDOFF line after 10 days means the stand-in's planner did not create the Sitting. Repeat step 2 up to three times and record the count.
4. Console: `event kehillah_bet_din_ai_debug.2`.
   - Expect a sitting whose host has the Kehillah government and is AI, `via stand-in`, `still gathering`, and attendees.

## 2. The docket opens and the Sitting finishes

5. Play about 60 days.
   - Expect `DOCKET opened with a full bench`, or `GATHERED phase 1 not active yet` followed later by the normal opening.
   - `DOCKET no quorum` is a real failure. Note who attended (from `.2`).
6. Play on until the Sitting ends (about 3 months). Run `.2` again: the sitting should be gone. In `error.log`, look for lines that name `kehillah_bet_din` case events or `kehillah_bet_din.0099` with an AI host.

## 3. The player is invited (the "visit" path)

7. Play a Jewish ruler or Kehillah leader with AI communities of the same rite within diplomatic range, such as Worms. Since 2026-11-15, judges are chosen by rite and range, not minhag region.
   - Also check that a community outside the old regions (for example Baghdad) can now convene.
8. Console: `event kehillah_bet_din_ai_debug.3`, then play about 10 days. Expect an `INVITE player invited` line naming you.
9. **Look:** do you get the normal activity invitation, from the AI leader, for the Sitting of the Bet Din? Accept it.
10. Travel there, and check that you arrive before the docket opens (about 60 days after the handoff). If you are among the best-ranked judges, you should sit as a co-judge and get the case events.
11. **Look:** did any invitation arrive *before* the handoff with a count named as host? That is cosmetic, but record it.

## 4. Synod and Sanhedrin (when available)

12. If a regional leader qualifies for the Synod (open takkanah, quorum, no recent synod, prestige), `.1` and `.3` may produce `INTENT synod`. Expect `GUEST added` lines for delegates, the motion events running for the AI host, and a ruling bound to the region.
13. An AI Nasi with an open takkanah should produce `INTENT sanhedrin`.

## 5. Ordinary play

14. Unpause for 2–3 years at speed 5 with no debug events. Count the `ATTEMPT`, `HANDOFF PASS` and `DOCKET opened` lines. Expect several AI Sittings a year across the map.
15. A player-hosted Sitting must behave exactly as before: no gathering wait, and the Piety cost charged at the start.

## Record

Write a dated live-test log, following the existing convention. Record the counts from steps 3 and 14, any `error.log` lines with `kehillah_bet_din` in them, and the answers to the two **Look** questions.
