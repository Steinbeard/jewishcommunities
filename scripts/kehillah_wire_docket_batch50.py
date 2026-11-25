"""Idempotently wire cases 85-114 into the Bet Din draw and citation systems."""
from pathlib import Path
from kehillah_docket_batch50_data import EXTRA_CASES_5
from kehillah_docket_batch60_data import EXTRA_CASES_6
from kehillah_docket_batch70_data import EXTRA_CASES_7
EXTRA_CASES = EXTRA_CASES_5 + EXTRA_CASES_6 + EXTRA_CASES_7

ROOT = Path(__file__).resolve().parents[1]
EFFECTS = ROOT / "common/scripted_effects/kehillah_bet_din_scripted_effects.txt"
CITE = ROOT / "common/scripted_effects/kehillah_din_citation_effects.txt"
TRIGGERS = ROOT / "common/scripted_triggers/kehillah_din_citation_triggers.txt"
PARTIES = ROOT / "common/scripted_effects/kehillah_bet_din_sources_effects.txt"
DEBUG = ROOT / "events/kehillah_bet_din_expansion_debug_events.txt"

DATES = {
    85:(867,1453),86:(900,1350),87:(950,1350),88:(950,1453),89:(1100,1453),
    90:(950,1350),91:(867,1453),92:(900,1350),93:(867,1453),94:(867,1453),
    95:(1100,1453),96:(900,1350),97:(867,1453),98:(867,1453),99:(867,1453),
    100:(950,1350),101:(867,1453),102:(950,1453),103:(867,1453),104:(1100,1453),
    105:(867,1453),106:(900,1350),107:(867,1453),108:(867,1453),109:(950,1453),
    110:(867,1453),111:(867,1453),112:(900,1350),113:(867,1453),114:(900,1350),
}
REGIONS = {
    86: "OR = { geographical_region = world_middle_east geographical_region = world_africa_north_east }",
    87: "geographical_region = world_africa_north_east",
    89: "geographical_region = world_europe_west_iberia",
    90: "geographical_region = world_africa_north_east",
    92: "OR = { geographical_region = world_middle_east geographical_region = world_africa_north_east }",
    95: "geographical_region = world_europe_west_iberia",
    96: "OR = { geographical_region = world_middle_east geographical_region = world_africa_north_east }",
    100: "geographical_region = world_africa_north_east",
    102: "OR = { geographical_region = world_middle_east geographical_region = world_africa_north_east }",
    104: "geographical_region = world_europe_west_iberia",
    106: "OR = { geographical_region = world_middle_east geographical_region = world_africa_north_east }",
    109: "OR = { geographical_region = world_middle_east geographical_region = world_africa_north_east }",
    112: "OR = { geographical_region = world_middle_east geographical_region = world_africa_north_east }",
    114: "OR = { geographical_region = world_middle_east geographical_region = world_africa_north_east }",
}
CULTURES = {88: "ashkenazi"}

def read(path):
    return path.read_text(encoding="utf-8-sig")

def write(path, value):
    path.write_text(value, encoding="utf-8-sig")

def insert(path, anchor, addition, sentinel):
    value = read(path)
    if sentinel in value:
        return
    if anchor not in value:
        raise ValueError(f"anchor missing in {path}: {anchor[:80]}")
    write(path, value.replace(anchor, anchor + addition))

draw = ""
for c in EXTRA_CASES:
    n, flag = c["n"], c["flag"]
    lo, hi = DATES[n]
    geo = f"\n\t\t\t\tdomicile.domicile_location ?= {{ {REGIONS[n]} }}" if n in REGIONS else ""
    if n in CULTURES:
        geo += f"\n\t\t\t\tculture = culture:{CULTURES[n]}"
    draw += f"""
        # CASE {n} -- {c['title']} ({c['book']}).
        10 = {{
            trigger = {{
                kehillah_has_dispute_candidates_trigger = yes{geo}
                current_date >= {lo}.1.1
                current_date < {hi + 1}.1.1
                NOT = {{ scope:activity = {{ is_target_in_variable_list = {{ name = kehillah_bet_din_cases_heard target = flag:kehillah_din_case{n} }} }} }}
            }}
            scope:activity = {{
                add_to_variable_list = {{ name = kehillah_bet_din_cases_heard target = flag:kehillah_din_case{n} }}
                kehillah_din_reset_case_effect = yes
                set_variable = {{ name = kehillah_din_case value = {n} }}
                set_variable = {{ name = kehillah_bet_din_case_drawn value = 1 }}
                random_list = {{
                    50 = {{ set_variable = {{ name = kehillah_din_case{n}_{flag} value = 1 }} }}
                    50 = {{ set_variable = {{ name = kehillah_din_case{n}_{flag} value = 0 }} }}
                }}
            }}
            trigger_event = kehillah_bet_din.0{n}1
        }}"""
draw = draw.replace("        # CASE", "\t\t# CASE").replace("        10 =", "\t\t10 =")
anchor = "\n\t}\n\n\t# NO CASE WAS ELIGIBLE."
value = read(EFFECTS)
if "flag:kehillah_din_case85" not in value:
    if anchor not in value:
        raise ValueError("draw-list anchor missing")
    value = value.replace(anchor, draw + anchor, 1)
    write(EFFECTS, value)

cleanup_anchor = "if = { limit = { exists = scope:activity.var:kehillah_din_case84_seal_required } scope:activity = { remove_variable = kehillah_din_case84_seal_required } }"
cleanup_anchor2 = "if = { limit = { exists = involved_activity.var:kehillah_din_case84_seal_required } involved_activity = { remove_variable = kehillah_din_case84_seal_required } }"
for anchor, scope in ((cleanup_anchor, "scope:activity"), (cleanup_anchor2, "involved_activity")):
    addition = "".join(
        f"\n\t\tif = {{ limit = {{ exists = {scope}.var:kehillah_bet_din_case{c['n']}_direction }} {scope} = {{ remove_variable = kehillah_bet_din_case{c['n']}_direction }} }}"
        f"\n\t\tif = {{ limit = {{ exists = {scope}.var:kehillah_din_case{c['n']}_{c['flag']} }} {scope} = {{ remove_variable = kehillah_din_case{c['n']}_{c['flag']} }} }}"
        for c in EXTRA_CASES
    )
    insert(EFFECTS, anchor, addition, "kehillah_din_case85_interest_hidden } " + scope)

pick = "".join(f"\nkehillah_din_case_{c['n']}_pick_effect = {{ kehillah_din_pick_citations_{c['order']}_effect = yes }}" for c in EXTRA_CASES)
bench = "".join(f"\nkehillah_din_case_{c['n']}_bench_effect = {{ kehillah_din_bench_order_effect = {{ SEDER = {c['order']} }} }}" for c in EXTRA_CASES)
covered = "".join(f"\nkehillah_din_case_{c['n']}_covered_trigger = {{ kehillah_din_covers_{c['order']}_trigger = yes }}" for c in EXTRA_CASES)
insert(CITE, "kehillah_din_case_84_pick_effect = { kehillah_din_pick_citations_nezikin_effect = yes }", pick, "kehillah_din_case_85_pick_effect")
insert(CITE, "kehillah_din_case_84_bench_effect = { kehillah_din_bench_order_effect = { SEDER = nezikin } }", bench, "kehillah_din_case_85_bench_effect")
insert(TRIGGERS, "kehillah_din_case_84_covered_trigger = { kehillah_din_covers_nezikin_trigger = yes }", covered, "kehillah_din_case_85_covered_trigger")

value = read(PARTIES)
if "involved_activity.var:kehillah_din_case = 85" not in value:
    target = "involved_activity.var:kehillah_din_case = 84 } }"
    if target not in value:
        raise ValueError("party response anchor missing")
    extra = "".join(f" involved_activity.var:kehillah_din_case = {c['n']}" for c in EXTRA_CASES)
    write(PARTIES, value.replace(target, "involved_activity.var:kehillah_din_case = 84" + extra + " } }", 1))

addition = "".join(
    f"\n\t\t\tif = {{ limit = {{ exists = involved_activity.var:kehillah_din_case involved_activity.var:kehillah_din_case = {c['n']} }} debug_log = \"kehillah_bet_din_expansion_debug: case {c['n']} active\" }}"
    f"\n\t\t\tif = {{ limit = {{ exists = involved_activity.var:kehillah_din_case{c['n']}_{c['flag']} }} debug_log = \"kehillah_bet_din_expansion_debug: case {c['n']} fact set\" }}"
    for c in EXTRA_CASES
)
insert(DEBUG, 'debug_log = "kehillah_bet_din_expansion_debug: case 84 fact set" }', addition, "case 85 active")
