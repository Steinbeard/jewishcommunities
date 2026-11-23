# Bet Din docket research integration

**Status: first playable case scripted 2026-11-23; source and xTiger checked; live hearing pending. The remaining workbook cases are research, not implemented.**

The [Mishnah-audited workbook](../research/bet-din-docket/CK3_Bet_Din_Docket_250_Cases_Mishnah_Audited.xlsx) is the exact file Daniel shared from his ChatGPT Library. Its SHA-256 is `BB099DF4FE3AFE3F5F688F0F69DDBA3220144D3FCB16FE16AA36456BD8C6A1F4`. It contains 250 proposed cases, 1,250 option prototypes, and cross-references to the Mishnah. The workbook's own **Ruling Options** sheet labels every choice `DESIGN PROTOTYPE / NOT HALAKHICALLY APPROVED`; **Research Audit** leaves case-specific medieval application and editorial sign-off open. It is a research source, not executable Paradox script.

## First case: BD-170, The Failing Mikveh

This case fills the Tahorot gap identified in [the rulings and gates spec](../spec/2026-11-11-rulings-sermons-and-gates.md). It is drawn only after 1100 in Christian-ruled Iberia, when the community has a mikvah and two suitable litigants. The donor alleges a defect in the bath's water channel; a hidden fact says whether the join is defective. The court may close and rebuild, inspect and repair if needed, or leave the bath open. Skilled judges can cite a mastered Tahorot work or conduct a joint inspection. An actual defect sharply lowers the quality of a leave-open ruling; closing a sound bath imposes a smaller quality cost. The final event reveals the channel's condition, changes the community's pillars, records the ruling, and advances the existing docket.

The workbook's primary link is [Mishnah Mikvaot 6:1](https://www.sefaria.org/Mishnah_Mikvaot.6.1), concerning water joined to a mikvah. The short quotation in the source tooltip identifies the subject. It does not by itself determine whether this fictional channel is valid; the game makes that a separate fact. This hearing adapts the workbook's premise and facts to the existing three-judge sequence. It does not copy the workbook's five generic options or its 0–100 scoring suggestion, because neither is a verified ruling and the mod's current docket uses a different tally.

The mod tracks mastery by whole work and Mishnah order, not by individual tractate. Case 15 therefore accepts a mastered Tahorot work; it does not claim to implement the workbook's proposed `mastery_mishnah_mikvaot` flag. The bench's Tahorot list and citation system use the existing order-wide code. This is an explicit departure from the workbook's proposed tractate bonuses.

## Verification and follow-up

- The isolated branch started from `origin/master`; the shared human-testing checkout and its unrelated edits were left intact.
- xTiger's pre-change baseline on CK3 1.21.0.3 was 0 fatal, 216 errors, 829 warnings. The 1.20-targeted validator reports known version-mismatch findings. The final run matched the baseline exactly, with no findings in the changed script. An event-file encoding warning and a domicile-scope warning were corrected during the pass.
- The diagnostic console event `kehillah_bet_din_expansion_debug.1` now reports case 15 and the hidden channel fact.
- A Luna live-game check remains pending: draw case 15 in a qualifying community, confirm the two co-judges and resolution fire once, check both hidden-fact outcomes and all three directions, inspect the source tooltip and activity log, and compare error.log to its boot baseline. No other model should substitute for Luna under AGENTS.md.

The next implementation unit should add a Zeraim case from a researched, region-specific premise and then review tractate-level mastery as a separate system decision. The workbook's BD-221 is broadly themed but its **Research Audit** calls the region a placeholder and says to select and research a real province before release. It is not a ready-made cross-regional event. The 249 remaining proposed cases need case-by-case legal and mechanical review, not bulk generation.
