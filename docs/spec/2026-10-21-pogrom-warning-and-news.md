**Status:** implementation built on 2026-10-21; source and `ck3-tiger` checked; live playtest pending. This dated addendum amends the timing and news of [V39](v39-pogroms-and-the-popular-crusade.md), the preacher buildup in [V41](v41-danger-incidents-and-the-pogrom-unfolding.md), and the crisis hub of [V42](v42-the-crisis-as-a-place.md). It leaves the historical Granada onset immediate.

# Warning before the pogrom

Daniel's first playthrough found the crisis compelling but too abrupt. This pass takes “3–6 before” to mean **months**; that choice can be shortened without changing the event architecture. A crusade preacher now spends 90–180 days gathering followers. When an accusation produces a prospective local mob, a named agitator begins preaching for the same span before declaring war. The existing elders' hub provides requests to lords, religious authorities, the agitator and the watch during that interval. A lord or overlord can pledge troops during the warning, then joins and raises them if war begins. Successful persuasion can redirect or weaken the threat. The local buildup uses its own text; it does not describe a crusade or crosses.

On declaration, the host musters for three four-day ticks, then begins moving on the fourth. Its siege therefore cannot begin before day 16, even if its army spawned in the target town. An undefended quarter then takes 14 further days to fall; castle refuge retains its longer countdown. A host turning toward a second community musters again. This is a pacing rule in the scripted march, not an engine siege modifier.

# What neighbours hear

The message at host formation and the message at the gates are replaced with a notice when violence begins and a second report when it ends. The latter states deaths, forced conversions and captives. The earlier preaching news remains a warning, not an attack notification. If a community dissolves within two years of the pogrom, nearby Kehillah players receive a distinct dissolution notice before its title is destroyed. A forced-conversion dissolution already has its own specific notice, so it is excluded from the additional one.

# Rites

Mob leaders and the leaders of popular risings against Jewish communities join one fixed Christian rite teaching Exclusion or one fixed Muslim rite teaching Abolition. The Christian rite is styled around militant supersessionism, the Muslim one around abolition of the Pact's protections. Both are unavailable for normal rite creation. This replaces newly generated rites and prevents repeated short-lived entries in the religion window. The fixed rites use the broad Christian and Sunni faiths respectively; a live pass must check how this displays for a host whose source county belongs to another Christian or Muslim faith.

# Scope and verification

Granada's scripted overnight eruption and a popular rising that is already at war still begin directly. The latter gets the minimum mustering interval after its war declaration. `ck3-tiger` 1.19 reports `set_character_rite` as unknown, including existing uses elsewhere in this 1.20 mod; xTiger 1.20 reports no findings in the changed script or localization files. The isolated boot loaded the mob events after encoding and localization fixes; [the test note](../testing/2026-10-21-pogrom-warning-live-test.md) records the pending gameplay checks. A live pass should verify the local warning, interruption or diversion, rite display, day of first siege tick, and both neighbouring notifications, including dissolution.

## 2026-10-21 naming and Almohadi addendum

Daniel's follow-up supersedes the fixed-rite names and Muslim rite choice in “Rites” above. The Christian fixed rite is **Chrysostomianism**: its followers invoke deicide and perfidy accusations and reject the witness teaching in favor of expelling Jewish communities. The description attributes its name and polemical influence to John Chrysostom; the expulsion program belongs to this fictional movement, not a claim that he personally organized pogroms.

Muslim mob and popular-rising leaders now join vanilla's **Masmudi (Almohadi)** rite rather than a new Muslim rite. The existing `kehillah_assign_teachings_effect` assigns `kehillah_teaching_abolition` to `rite:masmudi` at game start, before the general Muslim Dhimma assignment. This is a deliberate game abstraction: a Muslim mob can display the Almohadi rite before the historical Almohad movement appears in vanilla's 12th-century story. No vanilla rite file is overridden. The rite display and teaching remain pending a live check.

## 2026-10-21 rite reuse addendum

Daniel's subsequent review supersedes the fixed-rite approach and the naming/Almohadi addendum above. A mob preacher or popular-rising leader now stays within their existing faith. If their own rite already teaches Exclusion (Christian) or Abolition (Muslim), they keep it. Otherwise they join an existing rite of **that faith** with the required teaching, if one exists; only the first such leader in a faith creates a dynamic rite. This means Orthodox and Catholic, or Sunni and Shia, do not automatically become one another. The formerly hard-coded Christian rite and its localization are removed; vanilla Masmudi retains its separate Abolition teaching and can be reused naturally by a Masmudi leader. The generated rite's displayed name and the reuse path require a live check.
