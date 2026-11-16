**Status: General seat interaction and Dayyan handover live-verified 2026-11-16; Exilarch grant effect passed but its UI confirmation remains unrun.**

# General community claims and Exilarch recognition

## Source and static checks

The code on the `codex/exilarch-baghdad-claim-20261116` branch removes the
David-only decision and separates a targetable community claim interaction
from Exilarch recognition. xTiger against this worktree's absolute
`descriptor.mod` still reports the origin/master baseline: 0 fatal, 17
errors, 124 warnings, 38 untidy, 44 tips. No changed feature file has a
new diagnostic. `git diff --check` passes.

## Isolated Luna session and engine finding

Luna owned isolated CK3 PID 15604, using
`C:/Users/Daniel/.codex/ck3-test/festival-observance`. In a fresh 1066
campaign it identified David ben Hezekiah as history ID 9001102, internal
ID 34176, and switched to him. A script probe showed the first attempt to
use CK3's ordinary `has_claim_on` trigger for Baghdad failed, despite an
authored `add_pressed_claim`. In a disposable campaign, the same command
gave a working claim on `k_england` but did not give one on
`d_kehillah_baghdad`, vanilla `d_samaritan`, or a vanilla landless
adventurer title. The tested landless titles all have
`no_automatic_claims = yes`, so the probe does not isolate that flag from
the landless property. It does establish that ordinary CK3 claims do not
work for the community titles as currently defined.

The tester then added `title:d_kehillah_baghdad` to David's
`kehillah_community_claims` character variable list in the disposable
game. `is_target_in_variable_list` returned true. The implementation was
revised to use that list for any target community; David's initial entry
is now authored as a 1066 character-history effect. The current build was
not loaded in this test process and that history effect remains untested.

Using the console-only direct transfer probe with the earlier script
version, CK3 logged `KEHILLAH_SEAT_CLAIM: claimant gained community; old
camp removed` at 13:51:42. As Baghdad's leader, David passed the separate
Exilarch decision's observed adult, freedom, peace, Ben David, community
leadership, vacant-office, location, host-opinion, 100-gold, and
150-prestige gates. The decision was visible in the UI. A console-only
office probe logged `KEHILLAH_EXILARCH: vacant office recognized for a Ben
David community leader` at 13:59:09 and recorded David with Baghdad as
his primary title. This does not prove the UI activation or full
post-office state in the current build.

Luna hit its usage limit before the fresh-boot end-to-end test. Root
identified the single remaining isolated PID 15604 by its `-userdir`,
stopped that PID, and confirmed no CK3 process remained. Root did not
control the game UI or capture a screen.

## Fresh claim-list build

A later Luna fresh boot of the current build confirmed David's
history-authored `kehillah_community_claims` list contains Baghdad.
With David at Baghdad, a run-file probe found every generic interaction
condition true: Ezra was the target community leader, David was a Jewish
adventurer with the recorded claim, adult, free and at peace, with the
required resources, location, caretaker opinion and host opinion.
The tester invoked the exact scripted effect called by the interaction's
`on_auto_accept`; it logged a successful community transfer without a
claim-effect error. Post-state probes confirmed David held Baghdad as
primary, had Kehillah government and a Quarter, no longer held the camp,
kept Isaac as Dayyan, and was not Nagid. David's used custom claim was
consumed and the displaced caretaker received a custom return claim.
The graphical character interaction itself was not clicked in that pass.

The separate console-only office probe then granted the Exilarchate to
David. Post-state confirmed he held the office with Baghdad still primary
and Kehillah government intact; he was still not Nagid. The recognition
decision's UI activation was not clicked in the fresh build.

The tester rechecked and stopped only isolated PID 27912 and confirmed no
CK3 processes remained. The fresh error log had no new claim, interaction,
Exilarch, or Dynasty_house errors. It did contain 7,074 repeated
`title_province` context errors from the existing culture-homeland
game-start actions, plus test-run-file encoding and console-debug warnings;
these were not caused by the claim and office effects.

## Third session: actual seat interaction

Luna booted a fresh isolated game as PID 8552, confirmed David's history
claim again, moved him to Baghdad, and checked the interaction gates.
Using the character finder, it opened Parnas Ezra's right-click menu,
then Diplomacy and **more...**, where **Press Claim to Community Seat**
appeared. The tester confirmed it in the UI. Gold fell from 756 to 656
and prestige from 1400 to 1250. CK3 logged the generic transfer effect.
David held Baghdad as primary with Kehillah government and a Quarter;
his camp was gone, his used claim was consumed, the caretaker gained the
custom return claim, and David did not become Nagid.

The UI route exposed a difference from the direct event probe: Isaac was
not appointed Baghdad Dayyan. The interaction's debug scopes showed
`kehillah_claim_camp_dayyan` correctly captured Isaac, but `root` was
empty. The effect had checked `is_courtier_of = root`, so that condition
failed under a character interaction. Source now checks
`is_courtier_of = scope:kehillah_claimant`; this fix requires a fresh
boot and UI rerun. No other transfer scope error appeared.

## Fourth session: corrected Dayyan handover

Luna booted a fresh isolated 1066 game as PID 31268. David's history
claim was present and the Baghdad interaction gates passed. Before the
transfer the character finder showed Yitzhak ibn Sakri as **Your Dayyan**.
Luna took the seat through Ezra's actual character interaction; the
100-gold/150-prestige cost was charged. A post-transfer probe confirmed
Baghdad primary, Kehillah government, Quarter present, old camp gone,
David not Nagid, and Isaac `9003160` both David's courtier and his
community council Dayyan. The new effect checks the saved claimant scope
and moves the former camp Dayyan into that court before appointing him.
No unset-root or null-courtier error appeared in the fresh error log.

The shortened Exilarch decision detail opened with its requirements
checked. Its confirmation control remained below the isolated window's
visible panel; scrolling and Enter did not activate it. The grant effect
and post-state remain proven by the earlier direct probe, while this UI
activation is unrun. Luna stopped only PID 31268 and confirmed no CK3
process remained.

## Remaining live checks

Activate the separate Exilarch decision through its UI confirmation and
verify the office holder, unchanged community primary title, and cost.
The confirm control was clipped in the isolated test window, so this is
a UI access check rather than an untested grant effect. Save/reload of
the revised two-step route and the claim-inheritance on-death hook remain
unrun. A second target or claimant would confirm generality beyond the
ID-free source audit.
