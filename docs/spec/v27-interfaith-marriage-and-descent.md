# V27: Interfaith marriage and Jewish descent — 2026-10-02

**Status: scripted for CK3 1.20; live mixed-marriage and birth verification pending.**

Depends on vanilla Judaism and the existing 1.20 Judaism religion override in
`common/religion/religion_types/kehillah_judaism_reserved_names.txt`. This is a
focused addition to the Track A Jewish family loop; it does not change the
community's government, succession law, dynasty, or culture inheritance.

Jewish faiths inherit two new religion-level doctrines. Interfaith Marriage is
**Permitted** by default. When a proposed spouse practices a Jewish rite with
that doctrine, CK3's AI Evil-faith marriage cutoff is raised beyond the maximum
hostility level. The existing acceptance score, diplomatic range, consent, and
other vanilla constraints still apply. A newly created Jewish faith can choose
**Community Endogamy** to retain vanilla AI reluctance. Players were already
able to propose cross-faith marriages under CK3 1.20; this change addresses
the AI-only cutoff and its matching acceptance penalty. It does not make an
interfaith match automatic.

Jewish Descent is **Matrilineal** by default. New Jewish faiths can choose
**Patrilineal** or **Either Parent**. For a child born to one Jewish and one
non-Jewish parent, the chosen doctrine sets the child's public faith and rite
from the qualifying parent at birth. The opposite choice sets the child's faith
and rite from the non-Jewish parent, so vanilla's patrilineal marriage behavior
cannot silently defeat a matrilineal rule. If both parents are Jewish, vanilla
determines which Jewish rite the child receives. An unknown father leaves a
Jewish mother's rite in place when no paternal rite can be determined.
The paternal branch uses CK3's public family father, not a hidden biological
father.

This is a religious belonging rule, not a new genetic trait or a change to
CK3's culture and dynasty inheritance. A child can still convert later through
ordinary gameplay. `events/kehillah_interfaith_debug_events.txt` contains
console-only probes for the doctrine on a selected character and the resulting
faith of a selected mixed-parent child.
