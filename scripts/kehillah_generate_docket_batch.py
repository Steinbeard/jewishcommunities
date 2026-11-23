"""Generate three authored Bet Din hearings from the stable case-18 event flow.

Run from the mod root. The prose below is the source for this batch; generated
files are committed so the game does not depend on Python or this script.
"""
from pathlib import Path

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
]

for case in CASES:
    n = case["n"]
    s = TEMPLATE.replace("0181", f"0{n}1").replace("0182", f"0{n}2").replace("0183", f"0{n}3").replace("0184", f"0{n}4")
    s = s.replace("case18", f"case{n}").replace("CASE = 18", f"CASE = {n}").replace("= 18", f"= {n}").replace("_18", f"_{n}")
    s = s.replace("restriction", case["flag"])
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
        f"{p}4.t": "The Court Records Its Ruling", f"{p}4.desc": case["scene"],
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
