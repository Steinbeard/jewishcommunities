# Rachel Imenu and the Cave of Machpelah

**Status: Built 2026-11-15 in the shared checkout; source checked; live registry/travel/save checks pending.**

Daniel requested Rachel as a Tzaddeket and Kever Rachel, and/or Avraham's
Ma'arat HaMachpelah. This implements both using the installed game's native
`saint` trait and faith registry, plus two named travel points of interest.
The installed trait already calls Jewish women Tzadeket and Jewish men Tzadik.
No new trait, holy-site slot, tenet, building or government is introduced.
This is the requested narrow exception to v25's proposed deferral of tomb content.

Rachel and Avraham are obscured deceased characters in
`history/characters/kehillah_biblical_ancestors.txt`. Their dates are schematic
ordering dates, not historical dating claims. Hebrew culture and Rabbinism
provide engine affiliations, not claims about Bronze Age culture or rites.
Recognition is seeded only in Rabbinic Judaism; other Jewish faiths are not
automatically assigned Rabbinic shrine practices. The native registry supplies
inheritance on later faith splits.

Kever Rachel uses province 5965 (Jerusalem), representing the traditional
Bethlehem-road site: the installed map has no Bethlehem barony. Machpelah uses
5966 (Hebron). Both belong to c_jerusalem, already a Jewish holy site; this does
not claim the two tombs occupy the same place. The Biblical associations are
Genesis 35:19-20 (https://www.sefaria.org/Genesis.35.19-20) and Genesis 23 and
49:29-31 (https://www.sefaria.org/Genesis.49.29-31). Machpelah's description
includes the patriarchs and matriarchs, rather than presenting it as Avraham's
grave alone.

The travel sites award the native miniscule Piety reward to Jewish visitors and
miniscule Learning experience to other visitors, once under the native first-visit
rules. They use their own descriptions and toasts, avoiding the generic relic
extraction event chain. Initialization also consumes all native relic charges
for both ancestors, preventing the generic extraction decision from offering
their remains. Existing Jerusalem/Mary content is not removed or hidden.

Start and after-lobby hooks are idempotent. Use a fresh campaign: pre-existing
saves may lack the new history characters; load hooks and PoI builders guard
against missing characters rather than claiming a verified migration.

## Verification

- xTiger before: 0 fatal, 18 errors, 81 warnings, 37 untidy, 121 tips.
- Initial check caught two wrong-scope relic-charge calls; corrected to character scope,
  matching installed `history/characters/saints.txt`.
- Final xTiger: 0 fatal, 18 errors, 81 warnings, 37 untidy, 121 tips;
  unchanged baseline, with no new reports for this feature.
- Console probe: `event kehillah_ancestral_tombs_debug.1`. Run twice; both must
  log PASS for recognition, zero relic charges and both travel sites.
- Live checks unrun: xTiger game tools are unavailable in this session. Verify
  867/1066/1178 fresh starts, Rabbinic faith's ancestor list, female trait label,
  both travel names/toasts, generic relic-decision exclusion, and save/reload.
- Git staging failed with `.git/index.lock: Permission denied`. No branch switch,
  commit, push or PR; unrelated edits and the current branch were preserved.
