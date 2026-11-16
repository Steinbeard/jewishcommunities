"""Keep vanilla county holy-war resolution, with a narrower holy-site target.

Rebuild after reviewing upstream 00_religious_war.txt on a game update.
No vanilla casus belli is overridden.
"""
from pathlib import Path
from kehillah_holiday_revision_build import block

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"E:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game")


def build():
    source = (GAME / "common/casus_belli_types/00_religious_war.txt").read_text(encoding="utf-8-sig")
    cb = block(source, "minor_religious_war")
    cb = cb.replace("minor_religious_war = {", "kehillah_recover_holy_site = {", 1)
    cb = cb.replace("allowed_for_character = {", """allowed_for_character = {
        is_landed = yes
        NOT = { government_has_flag = government_is_kehillah }
        OR = { rite ?= { rite_has_parameter = kehillah_recover_holy_site } AND = { has_character_flag = kehillah_messianic_mission_active kehillah_has_messianic_hope_trigger = yes } }
""", 1)
    cb = cb.replace("valid_to_start = {", """valid_to_start = {
        scope:attacker.faith = {
            any_holy_site = { holy_site_county = scope:target }
        }
        trigger_if = {
            limit = { scope:attacker = { NOT = { rite ?= { rite_has_parameter = kehillah_recover_holy_site } } } }
            scope:target = title:c_jerusalem
        }
""", 1)
    # The reduced cost applies only to this restricted holy-site war.
    cb = cb.replace("multiply = holy_war_cb_piety_cost_multiplier",
                    "multiply = holy_war_cb_piety_cost_multiplier\n            multiply = 0.5", 1)
    # In invalidation descriptions the war can already have been cleared.
    cb = cb.replace("scope:war = {", "scope:war ?= {")
    cb = cb.replace("pam_notify_holy_war_instigator_effect_win = yes",
                    "scope:attacker = { save_scope_as = puppet_or_actor }\n        pam_notify_holy_war_instigator_effect_win = yes")
    cb = cb.replace('war_name = "RELIGIOUS_WAR_NAME"', 'war_name = "KEHILLAH_RECOVER_HOLY_SITE_WAR_NAME"')
    cb = cb.replace('cb_name = "HOLY_WAR_COUNTY_NAME"', 'cb_name = "KEHILLAH_RECOVER_HOLY_SITE_CB_NAME"')
    target = ROOT / "common/casus_belli_types/kehillah_sacred_homeland.txt"
    target.parent.mkdir(exist_ok=True)
    target.write_text("# GENERATED: CK3 1.20.1.2 county holy war, narrowed to the attacker's holy sites.\n" + cb + "\n",
                      encoding="utf-8-sig", newline="\r\n")


if __name__ == "__main__":
    build()
