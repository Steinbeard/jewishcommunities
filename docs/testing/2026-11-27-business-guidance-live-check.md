**Status:** SOURCE CHECKS PASS; row/eligibility/Domain hover and both Domain button states PASS; native alert view helper PASS; manual alert-icon click and construction-state checks UNRUN, 2026-11-27. Implements [business guidance and UI](../spec/2026-11-27-business-guidance-and-ui.md), continuing PR #87. This does not rerun or resolve [native market delivery](2026-11-27-family-businesses-live-playtest-log.md).

# Source checks

- 21 focused checks pass: 9 business, 8 household economy, 4 guidance integration checks. Native candidate conditions are tied to all twelve actual vacant court-position types; construction advice checks spare registered heads, household commitments, actual free Craft Row slots, permission, peace, construction, reserve and universal-trade availability. Native costs remain the inspector’s authority.
- xTiger before and after: 0 fatal, 579 errors, 776 warnings, 37 untidy, 152 tips. No new fatal/error/warning signature. These are baseline findings, primarily installed 1.21 versus validator 1.20 gaps, not a zero-error repository.
- Domain tooltips only read values/custom localization. Native action effects recheck availability and use only native interface effects to close My Realm/open the owned domicile. Domain buttons set one-day navigation requests; guarded scripted widgets open/focus the Quarter, select Households/Businesses, then consume the request. No hire, gold payment, family-asset change or construction occurs in advice/navigation.
- Existing generator stays idempotent. The staffing status is a native eligibility query, not a cached roster-size guess. Native Appoint remains accessible even with no candidate so the picker can display its eligibility state.

# Live session

Luna preflight found no CK3 process and did not launch before SOURCE READY. It identified the isolated launcher/profile and existing xTiger processes, which must not be attached to or terminated indiscriminately. Source is frozen for the delegated check. Owned PID **7320**, isolated userdir `C:/Users/Daniel/.codex/ck3-test/festival-observance`, and `mod/jewishcommunities_codex.mod` mount were verified. Fresh playable Worms and a unique console marker were confirmed.

- Read-only `.1`: **staffing AVAILABLE**, **expansion UNAVAILABLE** at fresh start.
- **Quarter panel rendering PASS:** the shorter leading-household exemption fits. The family-card Manage businesses control switches to Businesses. Market and Dyers show “Vacant — operator available,” native Appoint and compact output/income; no obvious overlap/clipping in the inspected game-only capture. This is a rendering pass at the tester’s scale, not every UI scale/name length.
- Captured evidence: `C:/Users/Daniel/AppData/Local/Temp/kehillah-live-businesses-domainroute.png` (game only, downscaled). The filename is not itself proof of the separate Domain button route.
- **Domain Affluence hover PASS:** the full numeric breakdown and the new section render: operating premises 0/4, unassigned eligible households 1, family assets/no duplicate income reward, seasonal growth, and staff-before-expanding advice. Saved game-only capture `C:/Users/Daniel/AppData/Local/Temp/kehillah-live-domain-affluence-hover.png`. The separate Quarter-driver hover remains UNRUN.
- **Domain Manage businesses FAIL on first implementation:** with the Quarter behind My Realm, clicking the new control did not bring it into view. This is a real navigation failure; no button-route pass is claimed for that revision.
- `.3` logged native staffing alert requested, but the actual alert item was not clicked; alert click-through remains UNRUN.
- **No-candidate case PASS:** `.2` then `.1` reports staffing UNAVAILABLE, expansion UNAVAILABLE and unassigned count zero. The roster says “Vacant — no eligible household”; native Dyers Appoint still opens its picker, showing 0 of 0 / “No valid Characters found.” Captures: `kehillah-live-blocked-businesses.png` and `kehillah-live-empty-picker.png` in Temp. An explicit alert request does not prove automatic scan timing.
- Error log stayed at 622,407 bytes after the inspected baseline; no new business/tooltip error appeared. The tester verified ownership, closed PID 7320, then confirmed no CK3 process remained.

## Navigation fix and narrow retest

After process closure, both Domain controls and alerts share a staged request bridge: dismiss My Realm, call vanilla’s `ToggleGameViewData` only while the Quarter is closed, then select the requested tab and consume the request only after the Quarter is actually open. This avoids closing an already-open Quarter or selecting a tab while the view is still switching. Native `IsGameViewOpen` guards each stage. Requests are mutually exclusive and expire after a day. The existing direct Household opener now uses this path too. Twenty-one source checks pass again; the native API/guard regression replaces the earlier assertion that merely checked an Open call existed.

Fresh isolated retest, owned PID **23544**, correct mount/profile and unique marker `KEHILLAH_NAV_BRIDGE_20261127_1640` verified.

- **Domain Manage businesses PASS with Quarter closed:** My Realm closes, the Quarter opens and Businesses is selected. Capture `kehillah-nav-domain-closed-result.png` in Temp.
- **Already-open Quarter PASS:** F2 opened My Realm over the Quarter. Manage businesses closed My Realm and kept the Quarter open on Businesses. Capture `kehillah-nav-domain-open-quarter-result.png`.
- `.1`: staffing AVAILABLE / expansion UNAVAILABLE; `.3` requested the staffing action. The tester inspected the native action/tips dropdown and could not identify a business item, so actual alert click remained UNRUN. The source audit below establishes why that was not the correct place to verify an `alert` icon.
- No post-startup tooltip/business error was observed. Owned PID 23544 was closed and a subsequent inventory found no CK3.

## Native alert interface audit

Installed `common/important_actions/_important_actions.info` says `alert` has a separate icon, while `action` is in the Current Situation dropdown, and click effects allow interface effects only. The alert click implementation was corrected to a shared native `close_view` / domicile-scoped `open_view_data` helper with explicit player. It opens the Quarter, then the existing utilization control selects Businesses. It sets no character variable. The now-unused construction request/widget was removed; Domain’s already-tested tab-selection bridge remains. `.4` probes the exact native alert view helper; its output is not a manual-icon-click pass. Twenty-one source checks pass again, including absence of gameplay writes in alert actions. Final alert-only run, owned PID **4312**, correct isolated profile/mod mount and unique marker `KEHILLAH_ALERT_FINAL_20261127_1651` verified:

- **Native alert view helper PASS:** `.4` requested the exact shared interface helper; the Quarter main view opened from the map. Game-only capture `C:/Users/Daniel/AppData/Local/Temp/kehillah-alert-helper-quarter.png`. This validates the native domicile scope/view call, not an icon click.
- `.1`: staffing AVAILABLE / expansion UNAVAILABLE. `.3`: native staffing alert requested.
- **Manual alert icon visibility/click UNRUN:** one likely separate top-bar icon was inspected; it was the existing A Sefer to Study action. The tester stopped without a broader icon search. No staffing-icon click is claimed. The engine’s automatic scan timing also remains unverified.
- No new business-advice/GUI/tooltip error was observed after source-loaded startup diagnostics. The early-boot error-log size grew from 3,569 to 621,570 bytes as known startup unused-variable/event-target messages completed; that growth is not a clean pre-UI baseline. Actual post-startup business-error filters were clean.
- Verified PID 4312 was closed; subsequent inventory showed no CK3. No other game/process or global configuration was changed.

Construction-advice setup and its native alert remain UNRUN. The shared native view helper is verified; construction eligibility gates are source-checked, not a completed gameplay scenario. Both Domain buttons retain their guarded native opener; removing the unused construction-request branch does not alter their tested states.

## Screenshot gallery update

The [published gallery](https://steinbeard.github.io/jewishcommunities-playtests/) now includes the polished Businesses panel and Domain Affluence hover, with honest revision/provenance notes. All six PNGs and live HTML return HTTP 200 and match source SHA-256 hashes. This gallery update uses saved game-only captures and makes no additional runtime claim.

# Manual validation guide

1. Fresh isolated Worms: record owned PID, userdir, mount, version, log baseline and a unique console marker. Use `event kehillah_business_debug.2` if a producer is needed; confirm its actual setup result.
2. Quarter > Businesses: fixed portrait size, wrapped household/status, compact terms and output/income fit. Hover terms/Appoint. Click both sub-tabs; only the selected body should take space. Check long family names. Vacancies say operator available only when the exact native picker has an eligible Ba’al Bayit.
3. My Realm > Domain: hover Affluence, then its Quarter driver. Both explain household assets and seasonal staffing effects, show utilization/available heads and a next action. No undefined localization or data-function error. Manage businesses opens Businesses, including when the Quarter was already open.
4. `event kehillah_business_advice_debug.1` reports native guidance availability and unassigned count without a refresh/payment. `.3` requests the native staffing alert through the real predicate for click testing. Locate its separate alert icon (not the Current Situation dropdown), click it and confirm the Quarter, then choose Businesses operating and native Appoint. If needed, `.4` probes the exact native view helper; this is not evidence that the icon was visible or clicked. This explicit request is not proof of the engine’s automatic important-action scan timing.
5. On a disposable paused state, `.2` applies a two-day commitment to currently free households. `.1` must now report staffing unavailable and count zero; vacancy status explains no eligible household. No actionable staffing recommendation should be generated by `.3`. Let the two days expire or reload before further staffing tests. An already-created native alert may await normal engine invalidation; clicking it must recheck and do nothing if stale.
6. Expansion: all existing businesses staffed, another eligible registered head free, one universal first-tier craft unbuilt, actual free Craft Row internal slot, at peace, charter permission, no ongoing construction and reserve. The lower-priority alert opens the Quarter for Craft Row inspection. Repeat with one unmet condition at a time, including one vacant existing business. Its wording must not promise a final native price or auto-start a build.
7. Compare error offsets, save game-only downscaled captures where rendering is the question, recheck ownership and close only the tester PID. Record unavailable setup or blocked tools as UNRUN, never PASS.
