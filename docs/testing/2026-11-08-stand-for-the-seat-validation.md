**Status:** CHECKLIST, 2026-11-08. Written with the first implementation pass of
[Stand for the Seat](../spec/2026-11-08-stand-for-the-seat.md) (section 13). Nothing below has been
run. Daniel runs these by hand; record each result in place (PASS / FAIL and a line on what you saw)
or in a dated live-test log.

# Stand for the Seat: what to validate

**Setup for every test:**
- **Bookmark:** `bm_1066_kehillah_worms`, playing Worms (`d_kehillah_worms`).
- **Test seat:** Mainz, unless you choose another. Speyer works too. All three Sh'um communities share
  a customary region.
- **Before you start:** note the `kehillah` lines already in `error.log`, so new ones stand out.
- **Probes:** console `event kehillah_candidacy_debug.N`. They write `KEHILLAH_CAND_PROBE` lines, and
  the feature itself writes `KEHILLAH_CAND` lines, to `debug.log`:

  ```
  findstr KEHILLAH_CAND "%USERPROFILE%\Documents\Paradox Interactive\Crusader Kings III\logs\debug.log"
  ```

  | Probe | Does |
  |---|---|
  | .1 | Status: preview score, in the pool, invested, engine score, the gates |
  | .2 | Declare for the test seat, free |
  | .3 | Make the player a great rabbi |
  | .4 | Kill the test seat's leader |
  | .5 | After a win: titles held, the Quarter record, courtiers |
  | .6 | Clear all candidacy state |

Run them in order. **V1 and V3 decide whether the design stands.** If either fails, stop and report
it: section 7.1–7.4 of the spec is the fallback.

---

## V1. The game loads, and ordinary succession still works

**Risk:** four new keys in `kehillah_leadership`. A rejected key drops the whole succession type,
and the game crashes on load ("unhandled succession order [invalid]").

1. Boot to the bookmark. The game reaches it with no crash.
2. `error.log` has no new line naming `kehillah_leadership` or `succession_appointment`.
3. Open the Worms leader's succession view. The line still lists his family and officers. Their
   breakdowns may now show the new lines, *A rabbi* or *How the board regards them*, and nothing
   reads blank.
4. Kill the leader of an AI community nobody has declared for, such as Speyer's
   (`kill <id>`). His heir takes the seat, the Quarter is rebuilt as before, and no new errors appear.
5. **Optional:** let a month pass. Successions anywhere in the world behave sensibly. The new
   terms changed who wins a little; they shouldn't change it wildly.

Result:

## V2. Weigh Their Seat

1. Right-click Mainz's leader. **Weigh Their Seat** is in the menu.
2. It is **not** offered on your own courtiers, on a leader of another faith, or on anyone who leads
   no community.
3. Choose it. The event *The Seat of Mainz* opens and shows:
   - your score as a real number, not blank;
   - your place "N of M", and the front-runner's name and score;
   - the stranger paragraph, since Worms's leader is not yet a great rabbi or married in;
   - under **The seat**: the Sh'um line and the Standing line. Add capital, yeshiva, economy,
     Nagid or crisis lines only where they are true.
4. **Put my name forward** shows its prestige cost and is available. Choose **Not now**.
5. `error.log`: no new lines from opening the event, and no tooltip error floods.

Result:

## V3. A declaration puts you in the seat's own line

**This is the central question:** does `change_appointment_investment` put an outsider into
`kehillah_leadership`'s pool?

1. Weigh Mainz again and choose **Put my name forward**. Or run probe .2, which is free.
2. Let **one day** pass, since the line is recalculated on the tick.
3. Probe .1. Expect:
   - `declared=yes`;
   - `invested=yes`;
   - `in_pool=yes`;
   - `engine_score=` the same number as `preview_score=`. A small difference means the two formulas
     have drifted; note both numbers.
4. Open Mainz's leader's succession view. **You are in the line**, and your breakdown shows:
   - the engine's invested line;
   - *Leads a community of standing*;
   - *From another community*;
   - *A stranger to the congregation*;
   - and **not** *Already leads another community* or *Not of this community's household*. Those are the old
     −500 terms, which must be waived for a declared candidate.

If `in_pool=NO` after a few days, the investment route doesn't work. Stop here.

Result:

## V4. The gates

1. Probe .3, which gives the Rabbi trait and piety level 3. It logs `great_rabbi=yes`.
2. Weigh Mainz again. The stranger paragraph is gone; the great-rabbi one shows instead. The score
   rises by the stranger term plus *A rabbi*.
3. **Married in:** marry the player, or one of his children, to an adult child of a Mainz board
   member, using whatever console route you prefer. Weigh again:
   - **the player married in:** the married-in paragraph shows, and the stranger term is gone;
   - **a child married in:** *A child married into a local family* shows, and the stranger term
     stays.

Result:

## V5. Ask to Be Named Successor

1. While declared for Mainz, right-click Mainz's leader. **Ask to Be Named Successor** is there. It
   is not offered to any other leader.
2. The AI answer shows its reasons (opinion, great rabbi, married in, same region, his own grown
   kin).
3. If he accepts, Mainz's succession view gives you the existing *Endorsed by the present leader* line.

Result:

## V6. Winning: the seat, the old community, the Quarter

**Setup:** be first in Mainz's line. Probe .3 usually does it; if not, add endorsement or learning.
Then:

1. **Before:** note both Quarters. Open your domicile panel (Worms's buildings) and Mainz's.
2. Probe .4 kills Mainz's leader. Its log line names the engine's heir, which should be you.
3. **On the same day:** you hold Mainz as well as Worms. That is expected for one day.
4. **Next day:**
   - the event *Called to Mainz* appears, naming who now leads Worms;
   - probe .5 shows:
     - `primary=` Mainz;
     - exactly **one** `holds community` line;
     - a domicile;
     - no candidacy left, and a cooldown set.
5. **Your domicile panel shows Mainz's buildings**: Mainz's levels, and none left over from Worms.
6. **Worms's new leader's domicile shows Worms's buildings**, as noted in step 1.
7. Probe .5's record line for Mainz matches what the panel shows.
   - **If Worms's or Mainz's record is wrong**, the building-completed on_action did corrupt a
     record, and the backup didn't restore it. Note which buildings are wrong.
8. `error.log`: no new lines. Look especially for `change_government`, `get_title`, `domicile`
   and `illegal government`.

Result:

## V7. Winning: the people

After V6:
1. **Mainz's people:** its board members, officers and householders are at **your** court now. Check
   whether they still hold their seats and offices.
   - The spec expects not. Report which, if any, survive.
2. **Worms's people:** its board, officers and householders went to Worms's new leader.
3. **Your household:** your spouse and children stayed with you.
4. **The old leader's household:** Mainz's dead leader's widow and children are at your court.

Result:

## V8. Losing

1. Probe .6 to reset, then declare for a seat where you stand far down the line, such as Speyer.
2. Probe .4 kills its leader. Its heir takes the seat.
3. The event *Another Was Chosen* appears.
4. Probe .1:
   - `declared=no`;
   - `invested=no`;
   - `in_pool=NO`;
   - `cooldown=yes`.

Result:

## V9. A winner whose old community has no heir

This is rare: the old seat's line is empty. Expected: the log line `the winner keeps it`, and the
player holds both seats. **Report what actually happens.** The fix is a design decision, not built
yet.

Result:

## V10. Withdrawing

1. Declare, then weigh the same seat again. **Withdraw my name** is there.
2. Choose it. Probe .1 shows:
   - `declared=no`;
   - `invested=no`;
   - `cooldown=yes`.
3. **Put my name forward** on any seat is now greyed, with its reason.

Result:

## V11. Your own death is unchanged

With no candidacy, kill the player. The death screen offers continuation exactly as before:
"Continue as" your community's heir.

Result:

## V12. Final error.log pass

After all of the above, list every new `kehillah` line in `error.log`. Look especially for:
- `appointment_candidate_score`;
- `local_var`;
- `title_heir`;
- `succession_appointment_score_invested`;
- `kehillah_cand_`;
- tooltip floods from the weigh event.

Result:
