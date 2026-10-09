# Appointment and clerical succession live tests — 2026-10-09

**Status: appointment succession FIXED and verified. Clerical continuation verified for rabbinic leaders (3 of 4 runs; 1 unexplained Game Over). Lay (Parnas) leaders still Game Over: open.**

Fresh boots, CK3 1.20.0.4, 1066 Kehillah of Worms, Isaac ben Eliezer ha-Levi, `kill 29176`. All runs
were by subagents.

## 1. Appointment succession was inert since the 1.20 port

Before the fix, the community's "View Succession" window showed "No valid Characters found (0 of 0)",
and Isaac's eldest daughter inherited. That ignores both the male-only lock and the merit scoring.
The 2026-10-01 port test saw a daughter succeed too and recorded it as a pass.

**Cause:** CK3 1.20 only runs appointment succession at or above the government's
`min_appointment_tier` ("Title tier that enables appointment succession mechanics",
`_governments.info`). Every vanilla appointment government sets it; `kehillah_government` didn't.
**Fix:** `min_appointment_tier = county`, as the theocratic governments use.

**After the fix:**
- The window lists 13–14 candidates: council members, sons and grandsons.
- Every female candidate sits near −100,000 under the male-only lock.
- The title passed by `appointment_succession` to the top scorer, Dayyan Gad Ben Ari (score 113).
- No crash at Play or on death, and no succession errors.

**New problem:** the player got Game Over ("no Player Heir"), because the appointee is from
another dynasty.

## 2. Clerical continuation (Daniel's design, modelled on vanilla 1.20)

- A trait with `clergy = yes` makes its holder clergy, and clergy "automatically join faith
  organization" (`_traits.info`).
- For an organization member, "your Heir will be the next person to receive your Primary Title"
  (`ECCLESIASTICAL_RULER_SUCCESSION_DESCRIPTION`).

**Run A, with a temporary leader trait (later removed):**
- The death screen offered "Continue as Rav Mishael" (the appointee, house Epstein) and "Choose a
  New Destiny...".
- Choose a New Destiny listed Isaac's house members, including two adventurers, so "your heir as
  an adventurer" is reachable there when one exists.
- Continuing as Mishael worked: he held Worms, the government and quarter were intact, and there
  were no errors.

**Run B, after the Rabbi trait got `clergy = yes` and lay leaders got `join_organization`:**
- **Rabbi path:** 3 of 4 runs passed ("Continue as Rav Dov Ber" / "Rav Shimon" plus Choose a New
  Destiny). One run ended in Game Over. That run fired `kehillah_debug.104` and
  `kehillah_household_debug.6` first, and Isaac's membership wasn't probed before the kill, so the
  cause is not isolated.
- **Lay path: FAIL in 2 of 2 runs.**
  - `join_organization = faith.organization` does make a lay leader a member. Probe `.7` showed
    "faith HAS an organization" and "PASS lay leader is a member".
  - He still has no player heir, and his death is Game Over. Script-joined membership does not
    produce the clergy-style heir.
  - Separately, the join in `kehillah_update_leader_flavor_effect` was not in effect right after
    an appointment succession: all three lay appointees were non-members.

## 3. Household standing in succession (slice 2)

- The standing term didn't appear in candidate breakdowns because most council seats were held by
  lowborn courtiers, who have no house.
- Probe `.6` passed for the one housed councillor (House Luria, registered with standing).
- The term is correct; it simply rarely applies while seats go to lowborn.

## 4. Portraits

No turban on Jewish clergy. Isaac and the Dayyan were both bearded.

## Pre-existing errors seen

- `kehillah_restore_quarter_effect` / `kehillah_restore_track_2/3_effect` "Failed to fetch variable
  for 'kq_countinghouse' / 'kq_workshops' / 'kq_market_stalls'" from `kehillah_on_title_gain`.
  These showed in one run's log only.
- The `kehillah_community_map_view.gui` layout warnings and mapcolor coat-of-arms noise, as before.

## Boot stall

Direct launches stall "Not Responding" until the CK3 window is clicked. See the shim guide's section
of the same name.
