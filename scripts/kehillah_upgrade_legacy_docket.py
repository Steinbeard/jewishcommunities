"""Move the fourteen bespoke cases onto the shared three-judge hearing flow.

The original ruling events and their case-specific effects are retained. Only
the choice, citation and panel scaffolding is changed.
"""
from pathlib import Path
import re

from kehillah_rewrite_docket_arguments import (
    EVENTS, choice_event, citation_and_feedback, match_brace, strip_quality_desc,
)


def event_span(source: str, eid: str):
    match = re.search(rf"(?m)^kehillah_bet_din\.{eid} = \{{", source)
    assert match, eid
    opening = source.index("{", match.start(), match.end())
    return match.start(), match_brace(source, opening)


def panel_prelude(n: int):
    lines = [
        f"\t\tinvolved_activity = {{ set_variable = {{ name = kehillah_din_case{n}_legacy value = 2 }} }}",
        f"\t\tkehillah_din_count_argument_panel_effect = {{ CASE = {n} FACT = legacy }}",
        f"\t\tinvolved_activity = {{ remove_variable = kehillah_din_case{n}_legacy }}",
    ]
    if n in (2, 3):
        lines.append(f"\t\tif = {{ limit = {{ involved_activity.var:kehillah_din_panel_winner = 2 }} involved_activity = {{ set_variable = {{ name = kehillah_bet_din_case{n}_direction value = 0 }} }} }}")
    if n == 5:
        lines.extend([
            "\t\tif = { limit = { involved_activity.var:kehillah_din_panel_winner = 1 } involved_activity = { set_variable = { name = kehillah_bet_din_case5_direction value = var:kehillah_bet_din_case5_truth } } }",
            "\t\telse_if = { limit = { involved_activity.var:kehillah_din_panel_winner = 2 } involved_activity = { set_variable = { name = kehillah_bet_din_case5_direction value = 0 } }",
            "\t\t\tif = { limit = { OR = { has_trait = zealous has_trait = paranoid } } add_stress = minor_stress_gain }",
            "\t\t\tevery_courtier = { limit = { OR = { has_trait = zealous has_trait = paranoid } } reverse_add_opinion = { target = root modifier = kehillah_bet_din_dismissed_mysticism_opinion } }",
            "\t\t}",
            "\t\telse = {",
            "\t\t\tif = { limit = { exists = involved_activity.var:kehillah_bet_din_litigant_b involved_activity.var:kehillah_bet_din_litigant_b = { num_sinful_traits >= 1 } } involved_activity = { set_variable = { name = kehillah_bet_din_case5_direction value = 1 } } }",
            "\t\t\telse = { involved_activity = { set_variable = { name = kehillah_bet_din_case5_direction value = 0 } } }",
            "\t\t}",
        ])
    return "\n".join(lines)


def upgrade(path: Path, n: int, eid: str):
    source = path.read_text(encoding="utf-8-sig")
    spans = [event_span(source, eid + str(i)) for i in (1, 2, 3)]
    first, second, panel = (source[a:b] for a, b in spans)
    first = choice_event(first, n, 1, eid)
    second_judge = choice_event(second, n, 2, eid)
    third = second.replace(f"kehillah_bet_din.{eid}2 =", f"kehillah_bet_din.{eid}3 =", 1)
    third = third.replace("kehillah_bet_din_judge2", "kehillah_bet_din_judge3")
    third = choice_event(third, n, 3, eid)
    panel = panel.replace(f"kehillah_bet_din.{eid}3 =", f"kehillah_bet_din.{eid}4 =", 1)
    panel = panel.replace("\timmediate = {", "\timmediate = {\n" + panel_prelude(n), 1)
    panel = panel.replace("\tdesc = {", "\tdesc = {\n\t\tdesc = kehillah_din_argument_panel_desc", 1)
    panel = re.sub(rf"(?m)^\s*desc = kehillah_bet_din\.{eid}3\.desc\s*\n", "\n", panel, count=1)
    panel = strip_quality_desc(panel)
    assert "kehillah_bet_din_advance_docket_effect = yes" in panel, eid
    panel = panel.replace("kehillah_bet_din_advance_docket_effect = yes", "kehillah_din_clear_argument_case_effect = yes kehillah_bet_din_advance_docket_effect = yes")
    replacements = [first, second_judge, third + "\n\n" + panel + "\n\n" + citation_and_feedback(n, eid).strip()]
    for (start, end), replacement in reversed(list(zip(spans, replacements))):
        source = source[:start] + replacement + source[end:]
    path.write_text(source.rstrip() + "\n", encoding="utf-8-sig", newline="\r\n")


def apply():
    done = []
    for n in range(1, 15):
        eid = f"{n-1:03d}" if n <= 9 else f"0{n}"
        matches = [p for p in EVENTS.glob("kehillah_bet_din*_events.txt") if re.search(rf"(?m)^kehillah_bet_din\.{eid}1 = \{{", p.read_text(encoding="utf-8-sig"))]
        assert len(matches) == 1, (n, matches)
        upgrade(matches[0], n, eid)
        done.append(n)
    return done


if __name__ == "__main__":
    print("Upgraded cases", apply())
