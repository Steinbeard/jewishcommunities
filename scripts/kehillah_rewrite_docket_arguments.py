"""Move authored cases 15-114 to argument, citation, feedback, panel stages.

Run after kehillah_generate_docket_batch.py. Existing prose and resolution
effects stay in their case files; only the old judge options are replaced.
"""
from pathlib import Path
import re
from kehillah_docket_batch10_data import EXTRA_CASES
from kehillah_docket_batch20_data import EXTRA_CASES_2
from kehillah_docket_batch30_data import EXTRA_CASES_3
from kehillah_docket_batch40_data import EXTRA_CASES_4
from kehillah_docket_batch50_data import EXTRA_CASES_5
from kehillah_docket_batch60_data import EXTRA_CASES_6
from kehillah_docket_batch70_data import EXTRA_CASES_7

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "events"
FLAGS = {15: "defect", 16: "accounts_gap", 17: "security_gap", 18: "restriction"}
FLAGS.update({c["n"]: c["flag"] for batch in (
    EXTRA_CASES, EXTRA_CASES_2, EXTRA_CASES_3, EXTRA_CASES_4,
    EXTRA_CASES_5, EXTRA_CASES_6, EXTRA_CASES_7,
) for c in batch})
FLAGS.update({19: "ledger_gap", 20: "receipt_found", 21: "opposition", 22: "fund_restricted", 23: "income_hidden", 24: "share_concealed"})


def match_brace(source: str, opening: int) -> int:
    depth = 0
    quote = False
    comment = False
    escape = False
    for index in range(opening, len(source)):
        ch = source[index]
        if comment:
            if ch == "\n":
                comment = False
            continue
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                quote = False
            continue
        if ch == "#":
            comment = True
        elif ch == '"':
            quote = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return index + 1
    raise ValueError("unclosed brace")


def top_blocks(event: str, name: str):
    blocks = []
    for match in re.finditer(r"(?m)^\t" + name + r"\s*=\s*\{", event):
        opening = event.index("{", match.start(), match.end())
        blocks.append((match.start(), match_brace(event, opening)))
    return blocks


def choice_event(event: str, n: int, seat: int) -> str:
    eid = f"0{n}"
    options = top_blocks(event, "option")
    assert len(options) >= 2, (n, seat, len(options))
    afters = top_blocks(event, "after")
    assert len(afters) == 1, (n, seat)
    opts = []
    for letter, position, skill in (("a", 1, "Diplomacy"), ("b", 2, "Learning"), ("c", 3, "Stewardship")):
        check_letter = {"a": "c", "c": "b"}.get(letter, letter) if n == 15 else letter
        stress = "if = { limit = { has_trait = just } add_stress = 5 custom_tooltip = kehillah_din_stress_just_tt }" if position in (1, 3) else "if = { limit = { has_trait = impatient } add_stress = 8 custom_tooltip = kehillah_din_stress_impatient_tt }\n\t\tif = { limit = { has_trait = diligent } add_stress = -4 custom_tooltip = kehillah_din_stress_diligent_tt }"
        opts.append(f"""\toption = {{
\t\tname = kehillah_bet_din.{eid}1.{letter}
\t\tkehillah_din_choose_argument_effect = {{ SEAT = {seat} POSITION = {position} LETTER = {check_letter} }}
\t\t{stress}
\t\tcustom_tooltip = kehillah_din_argument_{check_letter}_factors_tt
\t\tshow_as_tooltip = {{
\t\t\trandom_list = {{
\t\t\t\t0 = {{ modifier = {{ add = kehillah_din_argument_{check_letter}_chance_value }} custom_tooltip = kehillah_din_argument_preview_success }}
\t\t\t\t0 = {{ modifier = {{ add = {{ value = 100 subtract = kehillah_din_argument_{check_letter}_chance_value }} }} custom_tooltip = kehillah_din_argument_preview_failure }}
\t\t\t}}
\t\t}}
\t\tai_chance = {{ base = {35 if position == 2 else 30} }}
\t}}""")
    option_text = "\n".join(opts)
    after_text = f"\tafter = {{ trigger_event = {{ id = kehillah_bet_din.{eid}5 }} }}"
    # Replace from the last span backwards to retain original offsets.
    spans = [(options[0][0], options[-1][1], option_text), (afters[0][0], afters[0][1], after_text)]
    for start, end, value in sorted(spans, reverse=True):
        event = event[:start] + value + event[end:]
    return event


def citation_and_feedback(n: int) -> str:
    eid = f"0{n}"
    return f"""
kehillah_bet_din.{eid}5 = {{
\ttype = character_event
\ttitle = kehillah_din_argument_citation_title
\tdesc = {{
\t\tfirst_valid = {{
\t\t\ttriggered_desc = {{ trigger = {{ NOT = {{ exists = involved_activity.var:kehillah_din_cite_grounded exists = involved_activity.var:kehillah_din_cite_innovative }} }} desc = kehillah_din_argument_citation_no_books_desc }}
\t\t\tdesc = kehillah_din_argument_citation_desc
\t\t}}
\t}}
\ttheme = learning
\tleft_portrait = {{ character = root animation = thinking }}
\ttrigger = {{ exists = involved_activity involved_activity.var:kehillah_din_case = {n} }}
\timmediate = {{ kehillah_din_prepare_argument_citations_effect = {{ CASE = {n} }} }}
\toption = {{
\t\tname = kehillah_din_argument_no_citation
\t\tshow_as_tooltip = {{ involved_activity = {{
\t\t\trandom_list = {{
\t\t\t\t0 = {{ modifier = {{ add = var:kehillah_din_argument_chance }} custom_tooltip = kehillah_din_argument_preview_success }}
\t\t\t\t0 = {{ modifier = {{ add = {{ value = 100 subtract = var:kehillah_din_argument_chance }} }} custom_tooltip = kehillah_din_argument_preview_failure }}
\t\t\t}}
\t\t}} }}
\t\tai_chance = {{ base = 25 }}
\t}}
\toption = {{
\t\tname = kehillah_din_argument_grounded_citation
\t\ttrigger = {{ custom_description = {{ text = kehillah_din_no_source_tt exists = involved_activity.var:kehillah_din_cite_grounded }} }}
\t\tkehillah_din_choose_argument_citation_effect = {{ SLOT = grounded }}
\t\tshow_as_tooltip = {{ involved_activity = {{
\t\t\trandom_list = {{
\t\t\t\t0 = {{ modifier = {{ add = var:kehillah_din_argument_grounded_chance }} custom_tooltip = kehillah_din_argument_preview_success }}
\t\t\t\t0 = {{ modifier = {{ add = {{ value = 100 subtract = var:kehillah_din_argument_grounded_chance }} }} custom_tooltip = kehillah_din_argument_preview_failure }}
\t\t\t}}
\t\t}} }}
\t\tai_chance = {{ base = 50 }}
\t}}
\toption = {{
\t\tname = kehillah_din_argument_innovative_citation
\t\ttrigger = {{ custom_description = {{ text = kehillah_din_no_source_tt exists = involved_activity.var:kehillah_din_cite_innovative NOT = {{ involved_activity.var:kehillah_din_cite_innovative = involved_activity.var:kehillah_din_cite_grounded }} }} }}
\t\tkehillah_din_choose_argument_citation_effect = {{ SLOT = innovative }}
\t\tshow_as_tooltip = {{ involved_activity = {{
\t\t\trandom_list = {{
\t\t\t\t0 = {{ modifier = {{ add = var:kehillah_din_argument_innovative_chance }} custom_tooltip = kehillah_din_argument_preview_success }}
\t\t\t\t0 = {{ modifier = {{ add = {{ value = 100 subtract = var:kehillah_din_argument_innovative_chance }} }} custom_tooltip = kehillah_din_argument_preview_failure }}
\t\t\t}}
\t\t}} }}
\t\tai_chance = {{ base = 25 }}
\t}}
\tafter = {{
\t\tkehillah_din_roll_argument_effect = yes
\t\tif = {{ limit = {{ involved_activity.var:kehillah_din_argument_seat = 1 }} involved_activity.var:kehillah_bet_din_judge2 ?= {{ trigger_event = {{ id = kehillah_bet_din.{eid}2 }} }} }}
\t\telse_if = {{ limit = {{ involved_activity.var:kehillah_din_argument_seat = 2 }} involved_activity.var:kehillah_bet_din_judge3 ?= {{ trigger_event = {{ id = kehillah_bet_din.{eid}3 }} }} }}
\t\telse = {{ involved_activity.var:kehillah_bet_din_convening_title.holder ?= {{ trigger_event = {{ id = kehillah_bet_din.{eid}4 }} }} }}
\t}}
}}
"""


def rewrite_file(path: Path, n: int) -> bool:
    source = path.read_text(encoding="utf-8-sig")
    eid = f"0{n}"
    if f"kehillah_bet_din.{eid}5 = {{" in source:
        return False
    found = []
    for stage in range(1, 5):
        marker = f"kehillah_bet_din.{eid}{stage} = {{"
        start = source.find(marker)
        assert start >= 0, (path, marker)
        opening = source.index("{", start + len(marker) - 1)
        end = match_brace(source, opening)
        found.append((start, end, source[start:end]))
    replacements = []
    for seat in range(1, 4):
        start, end, event = found[seat - 1]
        replacements.append((start, end, choice_event(event, n, seat)))
    start, end, panel = found[3]
    marker = "\timmediate = {"
    assert marker in panel, (path, "panel immediate")
    panel = panel.replace(marker, f"\timmediate = {{\n\t\tkehillah_din_count_argument_panel_effect = {{ CASE = {n} FACT = {FLAGS[n]} }}", 1)
    desc = "\tdesc = {"
    assert desc in panel, (path, "panel desc")
    panel = panel.replace(desc, "\tdesc = {\n\t\tdesc = kehillah_din_argument_panel_desc", 1)
    panel = re.sub(rf"(?m)^\s*desc = kehillah_bet_din\.{eid}4\.desc\s*\n", "\n", panel, count=1)
    panel = panel.replace("kehillah_bet_din_advance_docket_effect = yes", "kehillah_din_clear_argument_case_effect = yes kehillah_bet_din_advance_docket_effect = yes")
    replacements.append((start, end, panel))
    for start, end, value in sorted(replacements, reverse=True):
        source = source[:start] + value + source[end:]
    source += "\n" + citation_and_feedback(n)
    path.write_text(source, encoding="utf-8-sig", newline="\r\n")
    return True


def apply():
    changed = []
    for path in EVENTS.glob("kehillah_bet_din*_events.txt"):
        text = path.read_text(encoding="utf-8-sig")
        for match in re.finditer(r"(?m)^kehillah_bet_din\.0(\d+)1 = \{", text):
            n = int(match.group(1))
            if 15 <= n <= 114 and rewrite_file(path, n):
                changed.append(n)
            if 15 <= n <= 114:
                text = path.read_text(encoding="utf-8-sig")
    assert all(
        any(f"kehillah_bet_din.0{n}5 = {{" in p.read_text(encoding="utf-8-sig")
            for p in EVENTS.glob("kehillah_bet_din*_events.txt"))
        for n in range(15, 115)
    ), "a case is missing its citation screen"
    return changed


if __name__ == "__main__":
    print(f"Rewrote {len(apply())} cases")
