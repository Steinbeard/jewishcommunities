**Status:** Built 2026-11-15; source checked; live visual check pending.

# Yeshiva indication in the community card

Daniel requested moving the Yeshiva Seat indication into the Library button rather than adding height to the card or length to its heading. This supersedes the inline heading treatment for the community card only.

The existing 66-by-56 footer button now uses the Rosh Yeshiva icon and a green Yeshiva label when `kehillah_card_has_yeshiva` is shown. Otherwise it retains Library. The hover describes the seat, its standing (including dormant status), and its head using the existing title-scoped localization. Clicking keeps the existing library-opening behavior and access checks. The heading returns to the community name alone. No additional row, spacing, or height is introduced.

Manual check: compare Lucena with a community without a yeshiva; confirm matching footer/header alignment, hover standing/head, and that both footer variants open the correct library. Check a dormant seat as well. No live game was controlled in this session.

Validation: xTiger baseline was 0 fatal, 28 errors, 111 warnings, 37 untidy, 122 tips; post-change comparison recorded below. The shared checkout contains substantial unrelated edits; these were preserved. Git metadata is read-only under the session permissions, preventing branch/commit/push delivery.
Post-change xTiger: 0 fatal, 28 errors, 111 warnings, 37 untidy, 122 tips, identical to baseline. No new findings. Diff whitespace check passed. Git staging was attempted and denied when creating .git/index.lock; changes remain uncommitted.

## Student count, teaching focus, and icon correction (2026-11-15)

**Status:** Built; source checked; live icon/tooltip verification pending.

Daniel's screenshot confirms the new label and original tooltip render, but the icon is blank. Replace the conditional texture expression with two static texture icons, using mutually exclusive visibility conditions. They occupy the same 22-by-22 space above the label. The Yeshiva tooltip now shows the enrolled student count and teaching focus, reusing `kehillah_yeshiva_student_count_value` and `KehillahYeshivaSpecialization` on the community title holder, exactly as the existing yeshiva panel does. Zero students displays as 0; an unset specialization follows the existing Talmud default. This count is the enrolled student roll, not estimated population.

Manual verification: hover Lucena and check Students and Teaching focus against its yeshiva panel; confirm the Rosh Yeshiva icon appears. Hover another community with no yeshiva and confirm its Library icon remains. Footer dimensions and click behavior are unchanged. No live-game control performed. Git metadata remains read-only in this session.
Validation of the addendum: xTiger totals unchanged (0 fatal, 28 errors, 111 warnings, 37 untidy, 122 tips); diff whitespace check passed. Git staging again failed creating .git/index.lock (permission denied).
