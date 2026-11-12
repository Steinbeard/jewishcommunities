# Crisis political consequences

Status: **implemented and source-checked 2026-11-12; live test pending.** This addendum records the invitation and backlash rules added after the Granada crisis review.

## Invitation suspension

An active `kehillah_community_crisis` now prevents its host ruler from issuing a new invitation to Jewish settlers. The gate applies to the visible ruler decision, the AI's automatic invitation when it raises the settlement policy, and the candidates for open-door and Shtadlan-sought invitations. It lasts until the situation is closed, including its recovery phase. Existing open invitations are not retroactively cancelled: the immediate concern is preventing the contradictory new proclamation while an established community is in danger.

## Hostile-faction victory

When the crisis resolves as **Quarter Struck** (outcome 4), the anti-Jewish faction wins a political concession before the sovereign's later judgement event:

- the host ruler receives a persistent `-15` personal outlook shift toward Jews;
- the realm's Jewish Settlement Policy is lowered by one rung if it is currently Favored or Tolerated; and
- the struck community's charter is worsened by one available term, prioritising security, then construction, jurisdiction, and its faith-specific final term.

The automatic policy consequence stops at Discouraged. A local faction victory does not itself impose a realm-wide ban and expulsion; the ruler's subsequent judgement can still order the existing targeted expulsion, while broader bans remain a deliberate policy decision. Charter revision is marked so the existing charter refresh can report it to the community.

For a disposable-save verification, `event kehillah_crisis_political_debug.1` reports whether the current community's host is blocked from invitations, and `.2` applies the Quarter Struck political backlash to the current community.
