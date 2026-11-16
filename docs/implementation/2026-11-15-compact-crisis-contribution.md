**Status:** Built 2026-11-15; source/xTiger checked; visual check pending.

# Compact crisis contribution control

Daniel requested a numeric contributed total beside a `+[n]` button, where n is the Gold price for one more point. This supersedes the funding row's previous verbose labels and separate points tally.

The Armed Host situation window now places the Gold total and purchase button immediately together, with the expanding spacer after both. Hovering the total explains it and shows funded points; hovering the button explains +1 Quarter Held, escalating prices, the bargain discount, and the 25-point cap. The display expressions explicitly use GetPlayer, matching the existing scripted GUI execution scope rather than relying on event ROOT localization.

The existing marginal-cost value, eligibility checks, and guarded payment effect remain authoritative. Source review confirms each payment increments paid points by one and applies one catalyst point; the label and payment use the same rounded marginal price.

Validation: git diff --check passed for the two changed UI/localization files. xTiger before and after: 0 fatal, 34 errors, 117 warnings, 37 untidy, 135 tips. No live game was controlled; rendering remains unverified.

Manual check: during Armed Host, open the situation window. Confirm a numeric Gold total immediately beside a +cost Gold button. Hover each, then buy a point: treasury falls by the displayed cost, total rises by that cost, funded points rise by one, and the next price updates. Check the disabled state without sufficient Gold and at 25 funded points.

Delivery: changes are in the shared main worktree on its existing branch, preserving concurrent work. Git staging failed creating .git/index.lock (Permission denied), preventing commit, push, and PR creation. No branch switch was attempted in the heavily modified shared checkout.

## Follow-up: total remains zero after payment

Daniel's live screenshot confirms the compact row renders, but shows zero after repeated contribution catalysts. Both numeric labels now use direct GUI data expressions so their values are evaluated by the widget rather than through a static localization-key label. The payment effect also captures the marginal price in the paying character scope once, then uses that same saved value for the treasury deduction and title ledger increment. This removes the ledger's dependency on event ROOT and guarantees the recorded amount matches the charge. Source alone cannot distinguish a stale label from a bad ledger value in Daniel's running save; the fix addresses both paths.

Follow-up manual check: reload the updated scripts/UI or restart with the existing save, contribute once with the window open, and verify total and next price update without reopening. Repeat after reopening and saving/loading. Previously unrecorded payments cannot be reconstructed accurately from funded points alone, since income and discounts may have changed; no speculative backfill is applied. Live verification remains pending. Git staging is still blocked by index.lock permission denial.
