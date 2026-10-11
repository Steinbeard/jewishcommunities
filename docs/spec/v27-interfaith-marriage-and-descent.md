# V27: Interfaith marriage and Jewish descent — 2026-10-02

**Status: corrected 2026-10-02; default doctrines and the marriage eligibility gate verified live 2026-10-11 on CK3 1.20.0.4. Rite-creation choices are visible in the UI; completed creation and mixed-parent births still need live verification.**

Depends on vanilla Judaism and the existing 1.20 Judaism religion override in
`common/religion/religion_types/kehillah_judaism_reserved_names.txt`. This is a
focused addition to the Track A Jewish family loop; it does not change the
community's government, succession law, dynasty, or culture inheritance.

Jewish faiths inherit two new default doctrines from the religion definition.
The doctrine groups use CK3 1.20's religion lock, which preserves their
inheritance when a Rite branches within Judaism. **Marriage Outside
Judaism: Forbidden** is the default for every existing Jewish faith. The
marriage eligibility trigger rejects a Jewish/non-Jewish pair on either the
player or AI path. A newly created Jewish faith may choose **Permitted**;
this lifts the new gate and CK3's AI Evil-faith marriage cutoff, but normal
acceptance, diplomatic range, consent, and other constraints still apply.
Different faiths within `judaism_religion` remain marriageable. Conversion
to a Jewish faith also makes a prospective spouse eligible.

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

## 2026-10-02 correction

This supersedes the first version of this document and commit `fddcfae` on
interfaith marriage. That version defaulted to Permitted and its Restricted
choice only left the vanilla AI reluctance in place; players could still
propose a mixed-religion marriage. Daniel specified the historical default
should prohibit such marriages for the Jewish faiths, so the default and the
actual eligibility gate were both corrected. This applies to marriages
outside Judaism; it does not prohibit Karaite/Rabbinite marriages within
Judaism. The latter distinction follows the account of medieval Karaite
marriages between Karaites and Rabbanites in
[this Karaite marriage discussion](https://www.myjewishlearning.com/article/who-could-karaites-marry/).
The default prohibition follows the traditional Jewish-law account summarized
in [this intermarriage discussion](https://www.myjewishlearning.com/article/is-intermarriage-against-jewish-law/).

## 2026-10-11 verification

A read-only live probe on eligible unmarried characters found that a Jewish/Jewish
pair passed `can_marry_character_trigger`, while a Jewish/Christian pair that
passed vanilla's `could_marry_character_trigger` failed the modded eligibility
trigger. The earlier live doctrine probe reported Forbidden and Matrilineal for
Rabbinism. See [the 2026-10-11 test log](../testing/2026-10-11-interfaith-marriage-live-test-log.md).

The paused game's rite-creation UI showed both custom doctrine groups, with
Forbidden/Permitted and Matrilineal/Patrilineal/Either Parent available in the
draft. Selecting Permitted changed the draft summary. No rite was actually
created. The original `doctrine_lock = religion` remains: Paradox's
[1.20 update notes](https://steamcommunity.com/app/1158310/?curator_clanid=4777282)
explain that the lock controls whether a doctrine survives moving or creating
a Rite across faith or religion boundaries, rather than whether a choice is
selectable in the creation screen.
