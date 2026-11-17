# Sefarim ledger: ranks and comparisons

**Status:** Built 2026-11-15 at Daniel's request; source/xTiger checked; live checks unrun.
Extends the ledger in [the shelf and ledger record](2026-11-08-library-shelf-and-ledger.md).

The ledger adds Rank beside Date and Name. It sorts highest first in the selected rite,
preserving date order within each rank. Changing rites rebuilds that order. Sort button
selection now reads the actual character state, avoiding disagreement with old GUI flags.

The selected work separates its current rank from **Highest attainable rank**, replacing
the ambiguous Ceiling field. Hover shows the tradition's baseline, the actual status of
each supported/opposed historical tenet, and its effect on the limit. Canonical corpora
instead explain doctrinal acceptance, including rejected corpora. The numeric reception
evidence and existing next-rank requirements remain. Works composed during play retain a
general explanation directing the reader to Work details for their chosen arguments.

**Other traditions** expands a bounded comparison panel for the selected work, showing
living Jewish rites and their faiths. It reads existing standings directly; it invents no
independent faith-wide consensus or new historical stance. The summary mapping is:

| Existing ranks | Summary |
|---|---|
| Anathema, Banned, Rejected (0–2) | Rejected |
| Contested (3) | Ambivalent |
| Obscure (4) | Unknown |
| Popular through Authoritative (5–8) | Important |
| Foundational through Divine (9–11) | Holy |

Unknown here means an unestablished reception, not an undiscovered or uncirculated book.
The comparison hover explains this distinction. The existing rite selector supplies exact
ranks and explanations for another tradition.

## Cost and generation

`scripts/kehillah_generate_ledger_assessment.py` generates only the ledger's rank effects,
assessment values and per-work assessment localization. Run it after changing the catalog.
It does not regenerate or alter other agents' catalog outputs.

Sorting checks catalog membership and evaluates each included book's rank once, partitions
flags into twelve temporary lists, then concatenates those lists in descending order.
Temporary lists are cleared. It runs on an explicit ledger rebuild (open/sort/rite selection),
with no daily/yearly hook or character/library scan added. Comparison reads rank values for
one selected work per listed rite, rather than every book against every rite.

## Validation and remaining checks

xTiger baseline: 0 fatal, 27 errors, 89 warnings, 37 untidy, 135 tips. First post-change
pass matched the baseline exactly. A later shared-tree pass reported 25 errors and 96
warnings while unrelated work changed concurrently; none of its semantic reports named
the ledger changes. The new debug file's BOM warning was corrected before the final pass.
Source checks verify all 173 catalog flags have rank buckets, assessment keys and canon-safe
limit helpers. Existing baseline issues are outside these changes.

Luna could not inspect Windows CIM process ownership in this environment, so it did not
launch or control CK3. Runtime ordering and visual layout remain unverified.

Manual checks:

1. Open the ledger in Worms or Granada; choose Rank. Torah should lead, rejected works
   should follow ordinary works. Switch Date/Name/Rank and change rites; selection and
   order must agree. Repeat without losing or duplicating entries.
2. Select a diwan: hover its rank/limit. Confirm Sacred Liturgy's actual rite status and
   its rank limit; compare a prohibited-tenet work and a canonical corpus.
3. Open Other traditions; verify rite and faith names, bounded scrolling, and the five
   summaries. Compare a Bavli order in Rabbinic/Karaite/Haymanot rites. Check long names,
   the ledger's bottom edge, and error.log for tooltip-only errors.
4. Console `event kehillah_ledger_debug.1` logs dated/ranked counts and ordered flags.
   Check equal counts, complete distinct rows, and descending ranks against the rite.

Shared checkout retained with unrelated changes preserved. Staging the exact ledger files failed with `.git/index.lock: Permission denied`. No branch
was switched and no unrelated changes were staged. Commit, push and PR delivery are blocked.
