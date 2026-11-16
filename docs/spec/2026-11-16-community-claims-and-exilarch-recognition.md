**Status: Built 2026-11-16; xTiger baseline unchanged; live claim storage, gates and both effects passed; UI activations and claim inheritance unverified.**

# Community claims and Exilarch recognition

This supersedes the one-character Baghdad petition in
`docs/implementation/2026-11-16-david-and-the-exilarchate.md`. David's
1066 history, family, and Baghdad claim remain an instance of these rules.

## Two distinct claims

**A community seat is a title.** CK3 refused manual pressed claims on the
tested landless community and vanilla landless titles, so this mod records
claim titles in a character's `kehillah_community_claims` variable list.
Any Jewish landless adventurer with such a claim on an existing Kehillah
title may press it through that title's
current leader. This is a character interaction, so the target is whichever
community the player selects, including dynamically founded communities.
The claimant must be adult, free, at peace, present in the seat's county,
and able to pay 100 gold and 150 prestige. The incumbent's opinion must be
at least -10 and the host ruler's at least -25. The title transfer uses the
incumbent as its government base, sets the seat primary, destroys the old
adventurer camp, and preserves the claimant's camp Dayyan as a community
Dayyan if that courtier is still available. The claim is consumed on a
successful transfer and the displaced incumbent receives a recorded
return claim. A claimant's recorded claims are scripted to pass to their primary heir at
death. David starts with a recorded claim on Baghdad; this is authored
character history, not a gate in the interaction.

**The Exilarchate is a lineage office.** A Jewish Kehillah leader with the
inheritable Ben David trait may seek recognition while the titular office
is vacant. The leader must be adult, free, at peace, present at their own
community seat, have host opinion at least -25, and pay 100 gold and 150
prestige. The office is a lifetime dignity and lapses at succession; a
qualified successor petitions again. It can coexist with any community
seat and does not transfer or create one. A Ben David adventurer first
needs to gain a community seat through a claim or another normal route.
The office is not a Jewish religious head title and confers no Gaonate.
The grant effect repeats the Ben David and Jewish-leader guards, so a
different caller cannot award the title to an ineligible character.
The dated historical exilarchal line is marked with Ben David as well.

## Nagid and court offices

The Nagid is a host realm's appointment to the leader of its capital
community, with a service at the host's court. Exilarchal recognition is a
separate title; a person may hold both but receives neither from the other.
If a pressed community claim displaces an incumbent Nagid, the existing
Nagid office is vacated and the host must confirm a new holder through its
normal rules. The claimant is not automatically appointed Nagid. Other
court posts belong to their employers. The claimant's own camp Dayyan is
the one office explicitly carried into a community council; the prior
leader's officers remain with the prior leader unless reassigned through
ordinary community play.

## Relationship to Weigh Their Seat

Weigh Their Seat is merit appointment and requires the player to already
lead a community. Press Claim is a living-to-living transfer for a Jewish
adventurer with a recorded community claim. It does not change appointment scoring
or succession laws, whose crash history is recorded in
`docs/implementation/v1-kehillah-implementation.md` sections 6 and 8.
Community leaders with a claim still use the existing candidacy path to
change seats; a direct transfer between two community leaders requires
its own verified Quarter and court handover before it can be enabled.

The current interaction and recognition decision are player-initiated.
AI use and a direct claim route for an existing community leader are
separate extensions; no character or community ID gates either action.
