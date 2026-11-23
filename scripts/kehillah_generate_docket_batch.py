"""Generate authored Bet Din hearings from the stable case-18 event flow.

Run from the mod root. The prose below is the source for this batch; generated
files are committed so the game does not depend on Python or this script.
"""
from pathlib import Path
from kehillah_docket_batch10_data import EXTRA_CASES
from kehillah_docket_batch20_data import EXTRA_CASES_2

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "events/kehillah_bet_din_stranger_aid_events.txt").read_text(encoding="utf-8-sig")

CASES = [
    dict(n=19, book="BD-021", slug="bakers_capital", flag="ledger_gap", order="nezikin", title="The Baker's Missing Capital",
         scene="[kbd_litigant_a.GetFirstName] says the bakery's grain supplier has not been paid. [kbd_litigant_b.GetFirstName], the other partner, says a season of poor sales consumed the capital. The account book stops before the last delivery. The judges must decide who carries the debt while the supplier waits.",
         a="Pay the supplier from communal reserves and charge the second partner.", a_tt="The supplier is paid at once, but incomplete books may make the accusation unjust. Prosperity bears a large cost.",
         b="Audit the deliveries before dividing the loss.", b_tt="Both partners open their books to an independent accountant. The supplier receives a smaller advance while the court establishes what was taken in.",
         c="Split the loss evenly and close the partnership.", c_tt="The supplier gets a settlement quickly, but an equal split may hide a clear debt in the complete accounts.",
         source="Cite a mastered Nezikin work and audit the partnership.", source_tt="A Nezikin work can guide the court on entrusted property and trade obligations. It cannot supply the missing entries in these bakers' books.",
         combo="Pair a careful scholar with a steward to reconstruct the ledger.", combo_tt="The judges compare deliveries, withdrawals and receipts before allocating the loss.",
         out1="The court pays the supplier from its reserves and charges the second partner. The bakery can keep buying grain, but the books remain incomplete.",
         out2="The court advances part of the debt and orders an independent accounting of deliveries and withdrawals.",
         out3="The partners divide the loss and dissolve their venture. The supplier accepts payment, though neither partner thinks the division was proved.",
         true="The missing pages conceal a withdrawal by the first partner. Charging the second partner alone was unjust.",
         false="The books reconcile with the supplier's receipts. Equal division ignored a traceable obligation.",
         one="The supplier is paid from communal reserves. Prosperity pays the larger cost.", two="An audit and advance cost some Prosperity.", three="The settlement costs less Prosperity but may misallocate the debt.",
         log="[CHARACTER.GetTitledFirstName] ruled on [TARGET_CHARACTER.GetFirstName]'s bakery debt claim."),
    dict(n=20, book="BD-031", slug="tax_between_towns", flag="receipt_found", order="nezikin", title="The Taxpayer Between Two Communities",
         scene="[kbd_litigant_a.GetFirstName] speaks for a town that demands a household levy from a newcomer. [kbd_litigant_b.GetFirstName] says the same levy was paid before leaving another community, but the receipt is in a traveling chest. The town's collector needs funds now. The court must avoid charging twice while keeping the common expenses paid.",
         a="Pay the town's claim from communal reserves now.", a_tt="The collector gets the money at once. If a receipt exists, the community may have paid a claim that was already settled.",
         b="Advance essential costs and send for the receipt.", b_tt="The town is funded while a messenger checks the old community's records. The court pays for the inquiry.",
         c="Settle for a smaller contribution and close the account.", c_tt="The newcomer pays less and the town receives something, but this may underfund a valid levy.",
         source="Cite a mastered Nezikin work and verify the prior payment.", source_tt="A Nezikin source can guide the court on proof of payment and communal obligations. The missing receipt still has to be found.",
         combo="Send a steward and a scholar to compare both towns' records.", combo_tt="The court advances urgent costs while two judges check the old and new accounts.",
         out1="The court pays the town from communal reserves. The collector is satisfied, but the newcomer's claimed payment remains unverified.",
         out2="The court advances essential costs and asks the former town for a copy of its receipt before assigning the levy.",
         out3="The court orders a smaller contribution as a final compromise. Neither town will revisit the account.",
         true="A receipt arrives from the former town. The full claim would have charged the newcomer twice.",
         false="No earlier payment appears in the old town's books. The reduced contribution leaves a real shortfall.",
         one="Communal reserves pay the full claim, at a large Prosperity cost.", two="A messenger and temporary advance cost some Prosperity.", three="The compromise costs less now but may leave a shortfall.",
         log="[CHARACTER.GetTitledFirstName] ruled on [TARGET_CHARACTER.GetFirstName]'s disputed town levy."),
    dict(n=21, book="BD-049", slug="prayer_rite", flag="opposition", order="zeraim", title="The Scholar Who Changed the Prayer Rite",
         scene="[kbd_litigant_a.GetFirstName], a visiting scholar, proposes a new reading for the congregation's prayers. [kbd_litigant_b.GetFirstName] speaks for the regular readers, who fear losing the words they know. Some households welcome the change; others have not been heard. The court must choose how the community will pray together next month.",
         a="Fund new books and adopt the reading at once.", a_tt="The scholar's reading takes hold quickly, but a divided congregation may stop attending. New books are costly.",
         b="Hold trial services and ask each household to be heard.", b_tt="The congregation can test the reading before choosing. Both sides share the work of teaching and listening.",
         c="Keep the inherited reading and end the dispute.", c_tt="Regular readers keep their practice, but a broadly welcomed change may be lost without a fair hearing.",
         source="Cite a mastered Zeraim work and hold a trial reading.", source_tt="A Zeraim work on prayer can inform the discussion. It does not reveal whether this congregation accepts the proposed reading.",
         combo="Have a scholar and steward plan trial services together.", combo_tt="The judges arrange teaching, listen to households, and keep regular services available.",
         out1="The court adopts the scholar's reading and pays for new books. The regular readers must learn it before the next service.",
         out2="The court arranges trial services, records household views, and postpones a permanent change until the congregation has heard both readings.",
         out3="The court keeps the inherited reading. The scholar's supporters are told to let the matter rest.",
         true="The household count shows strong opposition. A sudden change would have split regular worshippers.",
         false="Most households were willing to learn the new reading. Ending the discussion closed a door the community wanted open.",
         one="Books and teaching cost the community substantial Prosperity.", two="Trial services and instruction cost some Prosperity.", three="Keeping the old reading costs little, but may leave a dispute unresolved.",
         log="[CHARACTER.GetTitledFirstName] ruled on [TARGET_CHARACTER.GetFirstName]'s proposed prayer reading."),
    dict(n=22, book="BD-032", slug="synagogue_roof", flag="fund_restricted", order="moed", title="The Synagogue Roof and the Sacred Fund",
         scene="[kbd_litigant_a.GetFirstName] speaks for worshippers who want the leaking synagogue roof repaired before the rains. [kbd_litigant_b.GetFirstName] keeps a charitable fund whose donor may have reserved it for the poor. The deed is stored elsewhere. A dry room matters, but so does the promise under which the money was given.",
         a="Repair the roof from the sacred fund now.", a_tt="Work begins at once. If the donor reserved the money for relief, the court spends it against that purpose.",
         b="Patch the roof and inspect the donor's deed.", b_tt="A temporary covering protects services while the court learns which funds may pay for permanent work.",
         c="Leave the fund untouched and seek new subscriptions.", c_tt="The donor's money is safe, but the roof keeps leaking while the community raises another fund.",
         source="Cite a mastered Moed work and examine the fund's purpose.", source_tt="Mishnah Megillah discusses communal property and its proceeds. It cannot reveal this donor's terms; the court must read the deed.",
         combo="Ask a scholar and steward to inspect the deed and roof together.", combo_tt="The judges protect services with a temporary patch while checking the gift's permitted uses.",
         out1="The court releases money for a permanent roof. Workers arrive quickly, while the treasurer waits for the missing deed.",
         out2="The court orders a temporary covering and sends for the deed before committing the charitable fund.",
         out3="The court leaves the fund closed and asks households to subscribe for the repair. Rain still enters the synagogue.",
         true="The deed reserves the fund for poor relief. Spending it on the roof would break the donor's direction.",
         false="The deed permits repairs. The long subscription drive delayed work the fund could have paid for.",
         one="The fund pays for construction at a high Prosperity cost.", two="A temporary patch and deed search cost some Prosperity.", three="Subscriptions cost less now, while the roof continues to leak.",
         log="[CHARACTER.GetTitledFirstName] ruled on [TARGET_CHARACTER.GetFirstName]'s synagogue roof petition."),
    dict(n=23, book="BD-058", slug="child_maintenance", flag="income_hidden", order="nashim", title="The Child's Maintenance After Divorce",
         scene="[kbd_litigant_a.GetFirstName] represents a father who offers a small weekly payment after his divorce. [kbd_litigant_b.GetFirstName] speaks for the child's household, where food and rent now cost more. The father says his trade has slowed; the household says he has kept some earnings out of view. The court must provide for the child without setting a payment the father cannot meet.",
         a="Accept the father's smaller weekly payment.", a_tt="The agreement is quick and affordable, but hidden income would leave the child short of needed support.",
         b="Pay interim support and examine the trade accounts.", b_tt="The child receives help now. The court sets the continuing amount after inspecting receipts and expenses.",
         c="Order the larger payment requested by the household.", c_tt="The child's needs are met on paper, but an honest low income could make the order impossible to sustain.",
         source="Cite a mastered Nashim work and examine the support agreement.", source_tt="A Nashim source helps frame family obligations. The court must still establish this parent's means and the child's needs.",
         combo="Have a scholar and steward review the accounts and child's needs.", combo_tt="The judges fund interim support and compare the household budget with the father's trade receipts.",
         out1="The court accepts a smaller weekly payment. The father agrees, while the child's household must stretch each coin.",
         out2="The court orders interim support and examines the trade records before setting a continuing payment.",
         out3="The court orders the larger weekly payment. The child's household welcomes the ruling, but collection may prove difficult.",
         true="The father's books omit earnings from a second route. The smaller payment understated his means.",
         false="The books show a genuine decline in earnings. The larger payment would be hard to collect.",
         one="Communal support fills the immediate gap at a large Prosperity cost.", two="Interim support and accounting cost some Prosperity.", three="The court subsidizes collection at a smaller Prosperity cost.",
         log="[CHARACTER.GetTitledFirstName] ruled on [TARGET_CHARACTER.GetFirstName]'s child support claim."),
    dict(n=24, book="BD-023", slug="empty_caravan", flag="share_concealed", order="nezikin", title="The Caravan That Returned Empty",
         scene="[kbd_litigant_a.GetFirstName] returned from a long caravan journey with little to show its investors. [kbd_litigant_b.GetFirstName] says a share of the sales was concealed before the caravan reached home. The surviving tally names goods loaded, but not every sale. The court must weigh an expensive search against the risk of accusing a partner without proof.",
         a="Release the agent and cover the investors' loss.", a_tt="The dispute ends quickly at communal expense. A concealed share would make the release unjust.",
         b="Trace the caravan's sales and pay an interim share.", b_tt="The court checks merchants and cargo records while investors receive part of what is owed.",
         c="Order the agent to repay the full claimed share.", c_tt="Investors are protected, but a genuine loss could ruin an innocent trader.",
         source="Cite a mastered Nezikin work and trace the caravan's accounts.", source_tt="A Nezikin work can frame entrusted goods and proof. It cannot tell the court what this caravan actually sold.",
         combo="Pair a scholar with a trader to follow the cargo trail.", combo_tt="The panel compares departure lists, buyer receipts and the agent's return account.",
         out1="The court releases the agent and covers the investors' loss from communal reserves. No further account is demanded.",
         out2="The court advances part of the disputed share and sends for records from the caravan's ports.",
         out3="The court orders full repayment from the agent. Investors welcome the decision; the trader says the caravan truly returned empty.",
         true="A buyer's receipt reveals a share kept off the return account. Releasing the agent would have rewarded concealment.",
         false="The surviving receipts support a real loss. Full repayment would punish a trader for an empty journey.",
         one="Communal reserves cover the claim at a large Prosperity cost.", two="Tracing the cargo and paying an advance cost some Prosperity.", three="Enforcement costs less but may punish an honest loss.",
         log="[CHARACTER.GetTitledFirstName] ruled on [TARGET_CHARACTER.GetFirstName]'s caravan accounting claim."),
]
CASES.extend(EXTRA_CASES)
CASES.extend(EXTRA_CASES_2)

for case in CASES:
    n = case["n"]
    s = TEMPLATE.replace("0181", f"0{n}1").replace("0182", f"0{n}2").replace("0183", f"0{n}3").replace("0184", f"0{n}4")
    s = s.replace("case18", f"case{n}").replace("CASE = 18", f"CASE = {n}").replace("= 18", f"= {n}").replace("_18", f"_{n}")
    s = s.replace("restriction", case["flag"])
    s = s.replace("kehillah_var_prosperity", f"kehillah_var_{case.get('pillar', 'prosperity')}")
    s = s.replace(".restricted", ".fact_true").replace(".unrestricted", ".fact_false")
    s = s.replace("# The traveler needs food regardless of whether this particular fund\n\t\t# is restricted. An unrestricted meal is the safe middle course.",
                  "# The hidden fact changes the risk of the first and third rulings.\n\t\t# The investigation remains the dependable, costlier middle course.")
    lines = s.splitlines()
    lines[:3] = [f"# Workbook {case['book']}: {case['title']}.", "# A playable fictional dispute using the common three-judge docket flow."]
    s = "\n".join(lines) + "\n"
    (ROOT / f"events/kehillah_bet_din_{case['slug']}_events.txt").write_text(s, encoding="utf-8-sig")

    p = f"kehillah_bet_din.0{n}"
    labels = {
        f"{p}1.t": case["title"], f"{p}1.desc": case["scene"],
        f"{p}1.a": case["a"], f"{p}1.a.tt": case["a_tt"],
        f"{p}1.b": case["b"], f"{p}1.b.tt": case["b_tt"],
        f"{p}1.c": case["c"], f"{p}1.c.tt": case["c_tt"],
        f"kehillah_din_source_{n}": case["source"], f"kehillah_din_source_{n}_tt": case["source_tt"],
        f"kehillah_din_combo_{n}": case["combo"], f"kehillah_din_combo_{n}_tt": case["combo_tt"],
        f"{p}4.t": "The Court Records Its Ruling", f"{p}4.desc": case.get("decision_desc", "The parties return to hear the court's ruling."),
        f"{p}4.outcome_1": case["out1"], f"{p}4.outcome_2": case["out2"], f"{p}4.outcome_3": case["out3"],
        f"{p}4.fact_true": case["true"], f"{p}4.fact_false": case["false"],
        f"{p}4.quality_great": "$kehillah_bet_din.0083.quality_great$",
        f"{p}4.quality_good": "$kehillah_bet_din.0083.quality_good$",
        f"{p}4.quality_poor": "$kehillah_bet_din.0083.quality_poor$",
        f"kehillah_din_case{n}_one_tt": case["one"],
        f"kehillah_din_case{n}_two_tt": case["two"],
        f"kehillah_din_case{n}_three_tt": case["three"],
    }
    for tier, adjective in (("great", "well-supported"), ("good", "workable"), ("poor", "disputed")):
        labels[f"kehillah_bet_din_case{n}_{tier}_log_title"] = f"{case['title']}: a {adjective} ruling"
        labels[f"kehillah_bet_din_case{n}_{tier}_log"] = case["log"]
    loc = "l_english:\n" + "\n".join(f' {key}:0 "{value}"' for key, value in labels.items()) + "\n"
    (ROOT / f"localization/english/kehillah_bet_din_{case['slug']}_l_english.yml").write_text(loc, encoding="utf-8-sig")
