# Messianic Hope, Prophetic Revelation, and Temple Service

**Status:** DRAFT PROPOSAL (2026-11-15), not implemented. Requested by Daniel.
Complements the [current tenet pass](../implementation/2026-11-15-tenet-fixes-and-sacred-homeland.md).
Numbers are starting balance proposals; engine support and historical wording
require verification before implementation. No starting roster is changed.

**2026-11-15 implementation addendum:** Daniel requested implementation with
active messianism, deeper prophetic authority, artwork, and Samaritan sacrifice
at Gerizim through a real pilgrimage intent. The [build record and integration
audit](../implementation/2026-11-15-revival-tenets-and-integration-audit.md)
supersedes the provisional effects below. Those original proposals remain here
as design history; use the build record for shipped source behavior.

## Messianic Hope

**Jewish historical glossary:** Geulah; explain differing accounts of
redemption and the Messiah without requiring an imminent prediction or revolt.
An English heading is followed by a short native glossary link, not an essay.

**Belief description:** "Present humiliation need not be the final condition of
our people. By preserving the covenant and sustaining one another, we prepare
for an age of restoration, justice, and peace."

- Virtues: Patient, Zealous. Vice: Cynical.
- Followers: +10% Stress Loss; faster recovery of faith Fervor after persecution
  or loss of a holy site, implemented as a capped aftermath effect rather than
  a reward for causing losses. No bonus for deaths.
- Personal: +10% Spiritual Fulfillment Gain; a capped Piety/Stress reward for
  helping restore an afflicted community or regain an own-faith holy site.
- Distinctive content: optional messianic claimants who can generate Hope and
  division. Treat any events as new proposed content, not an existing unlock.
  Predictions and militancy are choices within that content, not requirements
  of the tenet. Do not make imminent apocalypse the default belief.
- Starting status: Known for Rabbinic Judaism and Karaism; other traditions
  require individual review. Not an automatic new core.

The subject is future redemption. Sacred Homeland instead concerns present
attachment to sacred places; Temple Service concerns sacrificial institutions.
This tenet supplies no additional generic conquest CB.

## Prophetic Revelation

**Jewish historical glossary:** Nevuah. Explain prophetic calling, visions,
ethical admonition, and disagreement over authentic and false prophets without
equating the Possessed trait with a historical medical diagnosis.

**Belief description:** "The divine word may interrupt the affairs of rulers
and reveal what custom alone cannot teach. Those called to bear it must speak,
even when the powerful would rather not listen."

- Virtues: Possessed, Honest. Vice: Deceitful.
- Followers: +1 Learning; spiritual fulfillment through a proposed prophetic
  vision/interpretation event pool. Possessed is religiously valued rather than
  merely tolerated. The event pool is explicitly new content.
- Personal: +10% Spiritual Fulfillment Gain; a proposed Admonish Ruler
  interaction challenges an actual ruler over an identifiable transgression,
  with opinion and Piety consequences. It is not generic free condemnation.
- Default starts: dormant historical tenet, Known as an inherited teaching but locked for core/personal adoption. A normal
  reform should not casually buy the return of prophecy. A future validated
  revival/claimant chain could unlock a synod or
  personal adoption, with schism/controversy where appropriate.
- A character acquiring Possessed does not itself reactivate prophecy or
  change authority doctrine. Accepting a claimant is a separate decision.

This concerns a claim to divine communication, rather than Scholarly Study's
argument from received sources or Esotericism's interpretation of hidden truth.

## Temple Service

**Jewish historical glossary:** Avodat ha-Mikdash. Explain offerings, priestly
and Levitical roles, sacred calendar, and the institutions sustaining worship.

**Belief description:** "At the sanctuary, the offerings, songs, and appointed
rites give order to the service of the divine. Priests and Levites bear duties
that neither royal favor nor private devotion can replace."

- Virtues: Kohen, Levite, Diligent. Vice: Lazy. Kohen/Levite virtues are a design
  choice about hereditary sacred office; confirm their effects are appropriate
  for each tradition before implementation.
- Followers, when the recognized sanctuary functions: +10% Monthly Piety;
  priestly office and sanctuary maintenance support actual seasonal service.
  Ordinary alms must not be relabeled sacrifices.
- Personal: cheaper or more rewarding participation in the proposed temple
  service activity, plus opinion with its officiants. A non-priest can adopt
  the tenet without becoming eligible for priestly office.
- Default Rabbinic/Karaite starts: dormant historical tenet, Known historically but locked for core/personal adoption.
  Future Temple restoration can unlock it alongside the appropriate sanctuary
  and headship rules. Wanting restoration does not mean sacrifices already occur.
- Samaritan status and revival conditions require separate historical review:
  Gerizim and its continuing sacrificial tradition must not be forced through
  a Jerusalem-only restoration gate. Temple Service is narrower than the mere
  survival of sacrifice and should not erase Samaritan practice in current starts.

Sacred Homeland's holy-site recovery CB can support access to the site, but
conquest alone does not create a sanctuary, ordain priests, or restore service.

Dormant is a design description, not a proposed additional engine status. The
ordinary Known status records historical familiarity; explicit eligibility
triggers would prevent ordinary adoption before revival.

## Implementation constraints for a later approved pass

Provide follower and personal effects in native panels, short glossary links,
distinct icons, clear greyed-out revival requirements, and separate doctrine
gates for priesthood, canon, and authority. Do not copy Rabbinic assumptions to
every Jewish faith. Historical loss, disputed legitimacy, and functioning
institutions are different conditions. Any proposed new interaction/event pool
must be built and tested before its tenet advertises it as available.

## Source lead for the Samaritan distinction

The [Samaritan community's account of Passover](https://www.the-samaritans.net/the-festival-of-passover/)
describes its sacrifice on Mount Gerizim. It establishes why a Jerusalem-only
revival gate cannot stand for all Jewish-group practice. Its present-day account
does not by itself verify every proposed medieval starting condition; those
remain for the separate historical review above.

## Addendum 2026-11-24: Temple Service starts unknown, learned from books

**Status:** IMPLEMENTED 2026-11-24 (Daniel: "Should we adjust the Temple Service
tenet so that maybe it's just not known and you can discover it personally
through studying?" -- "Yes please"). Supersedes the "Known historically" default
start in the Temple Service section above; Messianic Hope and Prophetic
Revelation keep it.

- Outside the Samaritans' Gerizim rite, where it is a core tenet, every Jewish
  faith starts with Temple Service **unknown**
  (`scripts/kehillah_faith_revision_build.py`, regenerated history and
  migrations).
- A reader learns it personally from a book that argues for it, on first
  mastery (Seder Kodashim, or a book written in play): the existing
  `kehillah_sefer_teach_tenet_effect`. The completion event's option tooltips
  now list a newly learned tenet among the reading's rewards.
- Restoring the service in Jerusalem still makes it permitted for the faith;
  adopting it still requires the restored service.
- Existing saves: once, while the service is not restored, a faith holding it
  exactly Known returns it to unknown
  (`common/scripted_effects/kehillah_temple_service_tenet_effects.txt`). CK3 has
  no effect that removes a tenet a character already knows, so readers who knew
  it keep it.
- Not yet checked in game: how 1.21's faith window shows an unknown tenet to a
  character who knows it personally.
