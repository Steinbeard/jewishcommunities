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

**Corrected 2026-11-14** ([spec](../spec/2026-11-14-adventurers-seats-and-invitations.md)): the stranger
term is now -20 and **only a marriage waives it**. A great rabbi keeps the great-rabbi paragraph but the
stranger paragraph stays; his record pays through the track lines instead. Step 2 below is rewritten for
that. The foreign-region term is now a foreign-**culture** term.

1. Probe .3, which gives the Rabbi trait, piety level 3 and a Talmudics record of 70. It logs
   `great_rabbi=yes`.
2. Weigh Mainz again. **The stranger paragraph stays, and the great-rabbi paragraph is added.** The
   score rises by *A rabbi* and *A record in the Talmud* (+12), not by the stranger term. Probe .1 shows
   the track values and `stranger=yes (-20)`.
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

---

# Added 2026-11-14: adventurers, invitations, visits, founding

Built the same day, not run. See [the spec](../spec/2026-11-14-adventurers-seats-and-invitations.md).
**V13 is the one that can end a game**, so it comes first. Do it on a test save.

## V13. An adventurer wins a seat (the dangerous one)

**Risk:** an adventurer holds a camp and then a community title. The old code would have called
`change_government`, which destroys the camp without making a Quarter and ends in Game Over 15 to 25
days later. The new route is `kehillah_succession.0010`'s scaffold.

1. Boot Worms 1066. Take the **Step Down** decision. You are now a landless adventurer.
2. Probe .8. Expect `adventurer_candidate=yes`, `can_weigh Mainz=yes`, `domicile=yes`.
3. Right-click Mainz's leader: **Weigh Their Seat**. Check the new lines: the stranger term is -20, the
   culture line shows if your culture differs, and there is **no** "leads a community" line. Put your name
   forward. The prestige cost is shown. The tooltip says your camp would give way to the Quarter.
4. Probe .3, so your score can win. Probe .1: `in_pool=yes`.
5. Probe .4 kills Mainz's leader. **Same day:** you hold the Mainz title and are still an adventurer.
   `error.log` has **no** `change_government` or `illegal government` line. This is the line that matters.
6. **Next day**, `debug.log` shows `kehillah_succession.0010` provisioning the Quarter: "created the
   temporary Kehillah scaffold", "destroyed the adventurer's camp title", "PASS successor has Kehillah
   government".
7. **Two days after the death:** the event *Called to Mainz* appears. Probe .5: `primary=` Mainz, one
   `holds community` line, a domicile, no candidacy left.
8. Your domicile panel shows Mainz's buildings. Let a month pass: no Game Over, no error flood.
9. `error.log`: look for `change_government`, `create_adventurer_title`, `destroy_title`, `domicile`.

Result:

## V14. A community sends for you

1. As a player rabbi with the stand-for-seat conditions met, probe .7. Expect the event *A Letter from
   Mainz* and `invited=yes` in `debug.log`.
2. **I will weigh the seat** opens the weigh event. It says they sent for you, and shows *The community
   sent for them* (+15) in the breakdown. The declaration costs half.
3. Run probe .7 again at once: it clears the seat's cooldown and your invitation, so it sends again.
   **Decline, with thanks** removes the invitation and adds a little regard.
4. **Optional:** set a seat's leader old, then advance years. A letter should come now and then, at most
   one per seat per five years.

Result:

## V15. Visit the Jewish Community

1. As an adventurer, travel to a county with a community: Worms, Speyer or Mainz. **Visit the Jewish
   Community** is in the decisions list. It is **absent** in a county with no community, and for a
   non-Jewish or landed character.
2. Choose it. The event shows the quarter's name and the leader, and the leader's culture.
3. **Take a family into my company** costs gold, and a family joins your court: a head, his wife, children.
   Check their culture (the county's local Jewish culture) and rite. The option is greyed with a reason
   when you cannot pay.
4. Run the decision again after six months. The family option is greyed ("no family to spare") for three
   years. **Pray with the congregation** still works.
5. With ten Jewish followers, **Found a Jewish Community** becomes available at your camp.
6. **Speak with the leader about the seat** opens the weigh event, when you may stand.
7. `error.log`: no tooltip floods from the event.

Result:

## V16. Founding for every Jewish faith

1. Make the adventurer Karaite, then Samaritan, then Beta Israel (`faith` console route). **Found a Jewish
   Community** is shown for each. Before this change a Samaritan or Beta Israel adventurer never saw it.
2. Found one for each faith, with ten followers. The community has a Quarter and a library.
3. **Check:** the Samaritan community's library. If it holds the Rabbanite default works, a Samaritan
   tradition value and seed is the fix (spec section 6).
4. `error.log`: no new `kehillah` lines.

Result:

## V17. Ordinary succession with the new terms

A rabbi with a Talmudics record now scores higher in everyone's succession, native or not. Kill an AI
leader with a rabbi in his court and check the breakdown shows the *record in the Talmud* line without any
blank or error. The ordinary-succession checks of V1 still hold.

Result:
