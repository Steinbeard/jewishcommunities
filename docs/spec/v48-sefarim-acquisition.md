# V48: Acquiring sefarim through the Library

**Status: FIRST NAMED-COMMISSION SLICE SCRIPTED, NOT YET LIVE-VERIFIED — 2026-10-19.** Requested and approved by Daniel on 2026-10-19. Builds on [V42](v42-sefarim-and-the-library.md), especially its acquisition-and-demand section, and supersedes the random player-facing acquisition flow in `kehillah_acquire_torah_work_decision`. ROADMAP remains authoritative for shipped status.

## Decision

The Library is the place where the player finds, examines, acquires, studies and donates sefarim. **A work that has not yet entered circulation does not appear in the acquisition catalog at all.** It is not shown disabled, named in a locked row or teased by a future date. Once its catalog circulation date arrives, reopening the acquisition page makes it eligible to appear.

The community's existing `kehillah_library_works` title list remains the sole authority for completed copies. Acquisition candidates and pending commissions are supporting title-owned lists, never a second ownership record.

## Player flow

1. The leader opens the Books page and selects **Acquire more sefarim**.
2. The panel replaces the owned shelf with works that are both already in circulation and missing from this community. Rows reuse the catalog's name, genre, standing, attribution and description.
3. Selecting a row opens the ordinary work detail with **Commission this work** in place of study, donation and reader actions.
4. Confirmation names the work and offers up to two registered communities known to own it. After choosing a source, the leader chooses an acquisition method:
   - buy a surplus manuscript, which needs no local workshop;
   - commission the source community's tier-2 Scriptorium;
   - or borrow its exemplar and copy it locally, which requires a tier-1 Sofer's Workshop and is faster when upgraded to a Scriptorium.
5. When no registered community owns the work, a slower search through distant scholarly networks is offered instead. Payment starts one title-owned acquisition. The normal Books page shows the named work and chosen route under **Copyists at Work** until completion.
6. Completion adds the work to `kehillah_library_works`; the current title holder receives the delivery event. Study, donation, citations and all existing consumers then see the copy normally.

The first slice does not rank known sources by distance. It presents up to two valid holders so source choice and provenance can be tested before path-distance logic is added. A later pass may prefer nearby communities or make distance affect copying time.

## Rules and balance

- The catalog itself has no workshop gate. Facilities unlock methods rather than hiding knowledge of available books.
- Buying a surplus manuscript costs `major_gold_value` and delivers after about one month. The source keeps its abstract ownership because the collection tracks whether a work is represented, not the number of physical copies.
- Commissioning the source costs `medium_gold_value`, requires that source to have a tier-2 Scriptorium and completes after about one year. Part of the payment reaches the source holder.
- Local copying costs `minor_gold_value`, requires the destination's tier-1 Sofer's Workshop and uses a borrowed exemplar. It takes about eighteen months at tier 1 or nine months with a tier-2 Scriptorium.
- The distant-network fallback costs `major_gold_value` and completes after about two years.
- Only one work can be commissioned per community at a time. Copying time replaces the old two-year decision cooldown.
- The result is deterministic after confirmation. There is no random failure after paying for a named work.
- The source never loses its exemplar. Donation remains a transfer of the actual held copy; commissioning creates another copy.
- If the leader changes, the commission remains on the title and completes for the successor.
- Losing the Scriptorium or source copy after the order begins does not destroy paid work; access was secured at confirmation.
- No hard collection capacity is introduced. V42's rule against deleting or concealing overflow remains in force.

The initial catalog uses `circulation_year` when supplied and otherwise its existing representative composition year. This is now the generator's one acquisition gate. Future historical work should audit distinct composition and circulation dates in the catalog rather than duplicating date conditions in events.

## AI and retirement of the old route

The old decision becomes AI-only. It refreshes the same eligible candidate list, chooses a named missing work, pays in the same confirmation event and creates the same delayed title commission. Players no longer receive a second decision-menu route, and AI communities no longer gain an instant random copy.

## Save and failure handling

The pending work is a one-item `kehillah_library_commission_work` list on the community title. Its source and route markers are also stored on that title. The delayed completion event is fired on the landed-title scope, not the commissioning character, so death and succession do not cancel or redirect delivery. Completion checks that the work is not already owned before adding it, then clears all pending state.

The derived `kehillah_library_acquisition_candidates` list is rebuilt whenever the player or AI opens the route. Stale candidates therefore cannot reveal a newly authored future work early, and ownership acquired by another route is rechecked both in the work action and the confirmation event.

## Verification gate

Before this slice is called live-verified:

1. Run the catalog generator twice and confirm a clean second run.
2. Run `ck3-tiger` against the feature checkout and compare it with the pre-edit baseline.
3. In a fresh 1066 save, open the acquisition catalog and confirm *Chovot HaLevavot* and *Kuzari* are absent, not locked.
4. Select a named available work and confirm that known source communities are named when any hold it.
5. Verify the method event: purchase is always available when affordable; source commission requires its Scriptorium; local copying requires our Sofer's Workshop and distinguishes tier-1 from tier-2 timing.
6. Pay through one route and verify that no copy appears immediately and the pending named row identifies that route while blocking a second acquisition.
7. Complete the acquisition through the debug probe, confirm the work enters the shelf, and verify study and donation actions become available.
8. Start another acquisition, change the community leader, and confirm delivery reaches the same community under the successor.
9. Record the run in `docs/testing/` and check the isolated `error.log` for new `kehillah_library`, scripted-GUI or data-context errors.
