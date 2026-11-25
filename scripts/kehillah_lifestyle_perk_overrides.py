"""Build the Kehillah lifestyle perk overrides from the installed vanilla files.

Spec: docs/spec/2026-11-24-kehillah-lifestyle-perks.md.

Copies vanilla lifestyle_perks files into common/lifestyle_perks/ under the same
names (so they replace vanilla's), then:
- inserts one `government_character_modifier = { flag = FLAG ... }` block per perk
  listed in KEHILLAH_BLOCKS;
- adds one tooltip line (gated on FLAG) per perk listed in KEHILLAH_TEXT, for
  Kehillah effects that live in the mod's own scripts (has_perk checks);
- hides vanilla tooltip lines that describe vassal-only effects (HIDE_TEXT).
Everything else stays identical to vanilla.

Re-run after every CK3 patch:
    python scripts/kehillah_lifestyle_perk_overrides.py "<CK3 install>/game"
"""
import json
import os
import re
import sys

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(MOD, "common", "lifestyle_perks")

# Set only by kehillah_government. Not government_is_kehillah: the landed
# Kehillah government has that flag too, and keeps vanilla's landed perks.
FLAG = "government_uses_kehillah_lifestyle_perks"

# perk -> modifier lines (indented on insert)
KEHILLAH_BLOCKS = {
    "00_learning_1_medicine_tree_perks.txt": {
        # The landless flag drops vanilla's epidemic resistance; keep it.
        "healthy_perk": ["epidemic_resistance = 5"],
    },
    "00_learning_2_scholarship_tree_perks.txt": {
        # planned_cultivation_perk: no modifier; it slows sefer wear (KEHILLAH_TEXT).
        # The landless flag drops vanilla's fascination bonus; keep it.
        "scientific_perk": ["cultural_head_fascination_mult = 0.2"],
    },
    "00_learning_3_theology_tree_perks.txt": {
        "faithful_perk": ["domicile_monthly_piety_add = 0.25"],
        "church_and_state_perk": ["domicile_monthly_piety_mult = 0.5"],
    },
    "00_stewardship_1_wealth_tree_perks.txt": {
        "heregeld_perk": ["domicile_monthly_gold_add = 0.15"],
        "detailed_ledgers_perk": ["monthly_income_mult = 0.05"],
        "war_profiteer_perk": ["independent_ruler_opinion = 5"],
        "fearful_troops_perk": ["domicile_monthly_gold_mult = 0.1"],
        "it_is_my_domain_perk": ["different_culture_opinion = 5", "different_faith_opinion = 5"],
        # The landless flag drops vanilla's income per stress; keep it.
        "golden_aplomb_perk": ["monthly_income_per_stress_level_mult = 0.1"],
        "at_any_cost_perk": ["monthly_income_mult = 0.05"],
    },
    "00_stewardship_2_domain_tree_perks.txt": {
        "organized_muster_rolls_perk": ["domicile_monthly_gold_add = 0.15", "domicile_build_gold_cost = -0.1"],
        "tax_man_perk": ["monthly_income_mult = 0.05"],
        "defensive_measures_perk": ["enemy_hostile_scheme_success_chance_add = -10"],
        "cutting_corners_perk": ["domicile_build_prestige_cost = -0.1"],
        "professional_workforce_perk": ["domicile_build_speed = -0.2"],
        "centralization_perk": ["domicile_monthly_prestige_add = 0.15"],
        "popular_figurehead_perk": ["general_opinion = 5"],
        "divided_attention_perk": ["domicile_monthly_gold_add = 0.15"],
    },
    "00_stewardship_3_duty_tree_perks.txt": {
        "meritocracy_perk": ["monthly_prestige_gain_per_court_position_add = 0.05"],
        # The landless flag drops vanilla's language-learning speed; keep it.
        "chains_of_loyalty_perk": ["learn_language_scheme_phase_duration_add = major_scheme_phase_duration_bonus_value"],
        "likable_perk": ["same_faith_opinion = 5"],
        "positions_of_power_perk": ["monthly_piety_gain_per_court_position_add = 0.05"],
        "large_levies_perk": ["courtier_opinion = 10"],
        "soon_forgiven_perk": ["stress_loss_mult = 0.1"],
        "toe_the_line_perk": ["councillor_opinion = 10"],
    },
}

# Kehillah-only effects that are not character modifiers. Each perk gets one
# tooltip line (an effect_localization key) at the top of its effect block;
# the effect lives in the mod's scripts, which test has_perk
# (common/script_values/kehillah_lifestyle_perk_values.txt). These perks do
# nothing else for a Kehillah leader: their vanilla effects are vassal, claim
# or county mechanics.
KEHILLAH_TEXT = {
    "00_diplomacy_1_foreign_affairs_tree_perks.txt": {
        "defensive_negotiations_perk": "kehillah_perk_stability_actions_effect",
    },
    "00_martial_2_authority_tree_perks.txt": {
        "absolute_control_perk": "kehillah_perk_stability_actions_effect",
    },
    "00_stewardship_1_wealth_tree_perks.txt": {
        "at_any_cost_perk": "kehillah_perk_prosperity_actions_effect",
    },
    "00_stewardship_2_domain_tree_perks.txt": {
        "centralization_perk": "kehillah_perk_prosperity_actions_effect",
    },
    "00_learning_2_scholarship_tree_perks.txt": {
        "sanctioned_loopholes_perk": "kehillah_perk_greatness_actions_effect",
        "planned_cultivation_perk": "kehillah_perk_sefer_care_effect",
    },
    "00_learning_3_theology_tree_perks.txt": {
        "clerical_justifications_perk": "kehillah_perk_greatness_actions_effect",
    },
}

# Vanilla tooltip lines about vassals that a Kehillah leader would otherwise see.
HIDE_TEXT = {
    "00_stewardship_3_duty_tree_perks.txt": ["toe_the_line_perk_effect", "removes_directive_refusal_perk_effect"],
}

HEADER = (
    "# KEHILLAH OVERRIDE of vanilla {name} (CK3 {ver}).\n"
    "# Generated by scripts/kehillah_lifestyle_perk_overrides.py -- do not hand-edit;\n"
    "# change the script and re-run it after each CK3 patch. Only the blocks marked\n"
    "# KEHILLAH differ from vanilla. Spec: docs/spec/2026-11-24-kehillah-lifestyle-perks.md\n"
)

NL = "\n"
T = "\t"


def block_span(text, start_pat, pos=0, end=None):
    """(start, end of opening match, index of closing brace) of the first matching block."""
    m = re.compile(start_pat, re.M).search(text, pos, len(text) if end is None else end)
    if not m:
        return None
    depth = 0
    i = m.end() - 1
    while True:
        c = text[i]
        if c == "#":
            i = text.index(NL, i)
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return m.start(), m.end(), i
        i += 1


def perk_span(text, name):
    span = block_span(text, r"^" + re.escape(name) + r"\s*=\s*\{")
    if not span:
        raise SystemExit(f"perk {name} not found")
    return span


def text_line(key):
    return (NL + T * 2 + "# KEHILLAH: what this perk does for a community leader." + NL
            + T * 2 + "if = {" + NL
            + T * 3 + "limit = { government_has_flag = " + FLAG + " }" + NL
            + T * 3 + "custom_description_no_bullet = { text = " + key + " }" + NL
            + T * 2 + "}")


def modifier_block(mods):
    return (NL + T + "# KEHILLAH: replaces the landed bonus the landless flag removes." + NL
            + T + "government_character_modifier = {" + NL
            + T * 2 + "flag = " + FLAG + NL
            + "".join(T * 2 + m + NL for m in mods)
            + T + "}" + NL)


def main(game):
    ver = "unknown"
    try:
        settings = os.path.join(os.path.dirname(game), "launcher", "launcher-settings.json")
        ver = json.load(open(settings, encoding="utf-8-sig"))["rawVersion"]
    except Exception:
        pass
    os.makedirs(OUT, exist_ok=True)
    files = list(dict.fromkeys(list(KEHILLAH_BLOCKS) + list(KEHILLAH_TEXT)))
    for fn in files:
        raw = open(os.path.join(game, "common", "lifestyle_perks", fn), "rb").read()
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig").replace("\r\n", NL)
        for perk, key in KEHILLAH_TEXT.get(fn, {}).items():
            start, _, close = perk_span(text, perk)
            eff = block_span(text, r"^\teffect\s*=\s*\{", start, close)
            if eff:
                text = text[:eff[1]] + text_line(key) + text[eff[1]:]
            else:
                text = text[:close] + NL + T + "effect = {" + text_line(key) + NL + T + "}" + NL + text[close:]
        for perk, mods in KEHILLAH_BLOCKS.get(fn, {}).items():
            _, _, close = perk_span(text, perk)
            text = text[:close] + modifier_block(mods) + text[close:]
        for key in HIDE_TEXT.get(fn, []):
            pat = re.compile(r"custom_description_no_bullet = \{\s*text = " + re.escape(key) + r"\s*\}")
            found = pat.findall(text)
            if not found:
                raise SystemExit(f"{key} not found in {fn}")
            text = pat.sub(lambda m: ("if = { # KEHILLAH: vassal-only effect" + NL
                                      + T * 4 + "limit = { NOT = { government_has_flag = " + FLAG + " } }" + NL
                                      + T * 4 + m.group(0) + NL + T * 3 + "}"), text)
        data = (HEADER.format(name=fn, ver=ver) + text).replace(NL, "\r\n").encode("utf-8")
        if bom:
            data = b"\xef\xbb\xbf" + data
        open(os.path.join(OUT, fn), "wb").write(data)
        print("wrote", fn)


if __name__ == "__main__":
    main(sys.argv[1])
