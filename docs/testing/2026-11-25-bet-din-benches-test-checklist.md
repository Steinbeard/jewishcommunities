**Status: checklist, 2026-11-25. Built and xTiger-checked, not live-tested.** For Daniel's live pass on the Bet Din
"bench and benches" rework. The design record is the header of
`common/scripted_triggers/kehillah_bet_din_benches_triggers.txt` (Daniel: "build everything with comments as the spec").

# Bet Din: the bench and the benches — test checklist

## What changed

- **Who judges.** The convener always argues seat 1 and is now also recorded as Av Beit Din. A convener without
  qualification sits "by his kavod and learning" at **-10** argument chance. Co-judges must be **qualified by
  rite**: ordained (Rabbanite), Learning 12 (Karaite), the `kohen` trait (Samaritan), Learning 12 (any other rite,
  groundwork). The community's own Dayyan is seated first, then fellow leaders, then a qualified player, then by
  judicial Learning.
- **Short bench.** If too few qualified judges come, the court looks in this order: qualified household members at
  the Quarter (summoned, no travel), then learned laymen among the attendees, then learned laymen of the household,
  all laymen at -10. If no court of three can be seated, the session ends with "No Court of Three", which refunds
  the Piety. **The cooldown is not lifted**: CK3 has no effect for that.
- **Semicha by judging is retired**; semicha is now sought from the benches.
- **Guests choose an intent:** Follow the Docket (default), Study in the Library, Make Friends, Seek Semicha
  (Rabbanites without the Rabbi trait), Bring a Complaint.
- **Role clarity:** the guest description says either "You may be seated as a judge" (with how seats are filled) or
  "You will sit on the benches". At the opening, each player guest gets "The Court Is Seated", which says where
  they sit.

## Before you start

- Note the `kehillah`-tagged lines in `error.log` after boot, as a baseline.
- Probe at any point during a sitting: `event kehillah_bet_din_benches_debug.1`, then read `debug.log` for
  `KBD_BENCHES`.

## Checks

1. **Planner text.** Open the Bet Din planner as a non-rabbi leader whose Dayyan is ordained. The "requires a
   rabbi" line reads "The community has a rabbi of its own…" and passes.
2. **Parnas presiding.** Convene as that non-rabbi leader. At the opening, "A Seat by Kavod" fires. On the first
   argument screen, the option tooltip shows "Seated without ordination: -10 chance", and the displayed
   percentages are 10 lower than an ordained leader's would be.
3. **Dayyan seated.** In the same sitting, the Dayyan holds a co-judge seat (the probe shows JUDGE2 or JUDGE3), even
   if visiting leaders came.
4. **Credit.** After a good ruling, the XP and citation credit go to the convener (seat 1), not to the Dayyan.
5. **Ordination required.** An unordained visiting leader who attends sits on the benches and gets "The Court Is
   Seated" with the benches text (play as a guest, or read the probe).
6. **Lay fallback.** Make the only qualified candidates unavailable (console: remove the Rabbi trait from nearby
   leaders' Dayyanim, or convene with only learned unordained courtiers). The court seats laymen; the probe shows
   `JUDGE2 is LAY`. A lay co-judge's argument chance is 10 lower.
7. **No court.** Make even laymen unavailable. "No Court of Three" fires, the Piety comes back, and no case
   is drawn.
8. **Guest description.** As a guest (accept an AI community's invitation), look at the activity's guest text
   before travelling. A qualified rabbi sees "You may be seated as a judge…"; an unordained character sees "You will
   sit on the benches…". **Also check whether this text appears on the invitation itself or only in the activity
   window**; the engine docs don't say.
9. **Follow the Docket (player guest).** On each case, "From the Benches" offers that case's positions by name. Pick
   one: a success or failure toast follows. On the court's ruling screen, a line "The benches leaned toward …"
   appears when any voice carried. Answering after the court has ruled shows "So be it" only.
10. **Study.** A guest with Study gets "In the Host's Library" at the opening, naming a real work from the host's
    shelves. Mastery shows up in the character's mastered works.
11. **Make Friends.** At the close, a success toast makes a friend (relation reason "Met on the benches of a Bet
    Din"); a failure gives mutual opinion.
12. **Seek Semicha.** An unordained Rabbanite guest, with an ordained judge on the bench, is examined at the close:
    success grants the Rabbi trait as ordained, failure gives Learning experience. With no ordained judge on the
    bench, "No One to Examine Me" appears.
13. **Bring a Complaint.** At the opening, "A Grievance of My Own" lists up to three people (rivals first). Choose
    one, then a claim; each claim's tooltip shows its odds. At the close a toast gives the ruling. Check:
    - cherem: the defendant's ban deepens one level. A community leader never reaches the full ban this way.
    - restitution: gold moves, never more than the defendant holds.
    - honor: Prestige moves.
    - a player defendant gets a letter "From the Bet Din,".
14. **error.log after each UI step.** Look especially for `Custom` / data errors from the option names
    `[GetPlayer.Custom('KehillahDinBenchPosition1')]` (benches.0010) and from `KehillahDinRowsLine` on the ruling
    screen.

## Known limits

- The activity cooldown stays after "No Court of Three"; only the Piety is refunded.
- AI followers on the benches pick a position at random. Their weight (4 per voice, capped at 10 per position)
  can tip a close panel but never outweighs a judge's successful argument (20).
- Complaints are offered against rivals, people with grounds for a ban, and bitter enemies (opinion -30 or worse)
  of the same faith within diplomatic range. Ma'arufia, broken betrothals and seat disputes were not built.
- Rites other than Rabbanite, Karaite and Samaritan use a Learning-12 placeholder rule.
