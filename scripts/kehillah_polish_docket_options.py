"""Refresh authored Bet Din event choices after the argument-flow update.

The base prose generator still starts from the original docket template;
kehillah_rewrite_docket_arguments.py creates the current flow for new output.
This migration updates an already rewritten checkout without regenerating
unrelated case prose.
"""
from pathlib import Path
import re

from kehillah_rewrite_docket_arguments import (
    EVENTS, choice_event, citation_and_feedback, match_brace,
)


def event_span(source: str, eid: str):
    match = re.search(rf"(?m)^kehillah_bet_din\.{eid} = \{{", source)
    assert match, eid
    opening = source.index("{", match.start(), match.end())
    return match.start(), match_brace(source, opening)


def apply():
    updated = set()
    for path in EVENTS.glob("kehillah_bet_din*_events.txt"):
        source = path.read_text(encoding="utf-8-sig")
        cases = {int(n) for n in re.findall(r"(?m)^kehillah_bet_din\.0(\d+)5 = \{", source)}
        for n in sorted(cases):
            if not 15 <= n <= 114:
                continue
            eid = f"0{n}"
            for seat in range(1, 4):
                start, end = event_span(source, f"{eid}{seat}")
                source = source[:start] + choice_event(source[start:end], n, seat) + source[end:]
            start, end = event_span(source, f"{eid}5")
            source = source[:start] + citation_and_feedback(n).strip() + source[end:]
            start, end = event_span(source, f"{eid}4")
            panel = source[start:end]
            panel, removed = re.subn(rf"(?m)^\s*desc = kehillah_bet_din\.{eid}4\.desc\s*\n", "\n", panel, count=1)
            source = source[:start] + panel + source[end:]
            if re.search(rf"(?m)^kehillah_bet_din\.{eid}6 = \{{", source):
                start, end = event_span(source, f"{eid}6")
                source = source[:start] + source[end:]
            updated.add(n)
        if cases:
            path.write_text(source, encoding="utf-8-sig", newline="\r\n")
    assert updated == set(range(15, 115)), f"Missing cases: {set(range(15, 115)) - updated}"
    return len(updated)


if __name__ == "__main__":
    print(f"Polished {apply()} cases")
