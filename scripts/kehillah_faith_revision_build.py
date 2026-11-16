"""Generate faith history and the once-only compatibility migration.

The first twelve book/reform indices retain their numeric positions; Piyyut is appended as 13. Several
retired convictions converge on a surviving teaching; integer save data stays
untouched. This table also documents the deterministic personal-tenet mapping.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = {
    "tenet_talmud_torah": "tenet_kehillah_scholarly_study",
    "tenet_baalei_hamiqra": "tenet_literalism",
    "tenet_kehillah_emunah_temimah": "tenet_unrelenting_faith",
    "tenet_kehillah_pesak": "tenet_religious_legal_pronouncements",
    "tenet_kehillah_pilpul": "tenet_kehillah_scholarly_study",
    "tenet_kehillah_geonut": "tenet_religious_legal_pronouncements",
    "tenet_kehillah_minhag_avoteinu": "tenet_kehillah_covenant_community",
}
ROSTERS = {
    "rabbinism": ("tenet_religious_legal_pronouncements", "tenet_kehillah_scholarly_study", "tenet_kehillah_covenant_community"),
    "minhag_ashkenaz": ("tenet_asceticism", "tenet_kehillah_scholarly_study", "tenet_kehillah_covenant_community"),
    "minhag_sepharad": ("tenet_kehillah_hokhmah", "tenet_religious_legal_pronouncements", "tenet_kehillah_sacred_liturgy"),
    "minhag_yerushalmi": ("tenet_kehillah_avelei_tziyon", "tenet_ritual_celebrations", "tenet_kehillah_covenant_community"),
    "merkabah": ("tenet_esotericism", "tenet_inner_journey", "tenet_kehillah_sacred_liturgy"),
    "karaism": ("tenet_literalism", "tenet_legalism", "tenet_kehillah_covenant_community"),
    "haymanot": ("tenet_kehillah_covenant_community", "tenet_asceticism", "tenet_ritual_celebrations"),
    "malabarism": ("tenet_kehillah_covenant_community", "tenet_adaptive", "tenet_eastern_syncretism"),
    "samaritan": ("tenet_kehillah_covenant_community", "tenet_literalism", "tenet_kehillah_temple_service"),
    "kabarism": ("tenet_adaptive", "tenet_religious_legal_pronouncements", "tenet_legalism"),
}
# Only these exact old default triplets are replaced wholesale. Reformed rites
# retain all their non-retired choices.
OLD_ROSTERS = {
    "rabbinism": ("tenet_legalism", "tenet_kehillah_geonut", "tenet_talmud_torah"),
    "minhag_ashkenaz": ("tenet_legalism", "tenet_asceticism", "tenet_talmud_torah"),
    "minhag_sepharad": ("tenet_legalism", "tenet_religious_legal_pronouncements", "tenet_talmud_torah"),
    "minhag_yerushalmi": ("tenet_legalism", "tenet_ritual_celebrations", "tenet_talmud_torah"),
    "merkabah": ("tenet_esotericism", "tenet_inner_journey", "tenet_talmud_torah"),
    "karaism": ("tenet_communal_identity", "tenet_baalei_hamiqra", "tenet_legalism"),
    "haymanot": ("tenet_communal_identity", "tenet_religious_legal_pronouncements", "tenet_asceticism"),
    "malabarism": ("tenet_communal_identity", "tenet_religious_legal_pronouncements", "tenet_eastern_syncretism"),
    "kabarism": ("tenet_religious_legal_pronouncements", "tenet_legalism", "tenet_communal_identity"),
}
HOMELAND = "tenet_kehillah_avelei_tziyon"
STUDY = "tenet_kehillah_scholarly_study"
LITURGY = "tenet_kehillah_sacred_liturgy"
COVENANT = "tenet_kehillah_covenant_community"
# Concrete ritual prohibitions, not bans on inquiry or interpretation.
PROHIBITED = {faith: ["tenet_human_sacrifice", "tenet_ritual_cannibalism", "tenet_divine_marriage", "tenet_gnosticism"] for faith in ("rabbinic_faith", "karaism", "haymanot", "malabarism", "samaritan", "kabarism")}
KNOWN = {
    "rabbinic_faith": sorted(set(sum((ROSTERS[k] for k in ("rabbinism", "minhag_ashkenaz", "minhag_sepharad", "minhag_yerushalmi", "merkabah")), ())) | {"tenet_aniconism", "tenet_literalism", "tenet_unrelenting_faith"}),
    "karaism": [*ROSTERS["karaism"], "tenet_aniconism", "tenet_kehillah_hokhmah", "tenet_asceticism", HOMELAND, "tenet_ritual_celebrations", LITURGY, "tenet_pursuit_of_knowledge", "tenet_unrelenting_faith"],
    "haymanot": [*ROSTERS["haymanot"], "tenet_aniconism", "tenet_legalism"],
    "malabarism": [*ROSTERS["malabarism"], "tenet_aniconism", "tenet_legalism", "tenet_ritual_celebrations"],
    "samaritan": [*ROSTERS["samaritan"], "tenet_aniconism", "tenet_legalism", HOMELAND],
    "kabarism": [*ROSTERS["kabarism"], "tenet_aniconism", "tenet_ritual_celebrations", "tenet_kehillah_hokhmah"],
}
PERMITTED = {
    "rabbinic_faith": ["tenet_adaptive"],
    "karaism": [STUDY, "tenet_inner_journey", "tenet_esotericism", "tenet_adaptive", "tenet_religious_legal_pronouncements"],
    "haymanot": ["tenet_literalism", "tenet_kehillah_hokhmah", HOMELAND, STUDY, LITURGY, "tenet_religious_legal_pronouncements"],
    "malabarism": ["tenet_kehillah_hokhmah", HOMELAND, STUDY, LITURGY, "tenet_religious_legal_pronouncements"],
    "samaritan": ["tenet_asceticism", STUDY, LITURGY, "tenet_religious_legal_pronouncements"],
    "kabarism": [COVENANT, HOMELAND, STUDY, LITURGY],
}
# Historically familiar teachings need not be active cores or unlocked practices.
for _faith in KNOWN:
    for _tenet in ("tenet_kehillah_messianic_hope", "tenet_kehillah_prophetic_revelation", "tenet_kehillah_temple_service"):
        if _tenet not in KNOWN[_faith] and _tenet not in PERMITTED[_faith] and _tenet not in PROHIBITED[_faith]:
            KNOWN[_faith].append(_tenet)



def write(path, text):
    (ROOT / path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\r\n")


def build():
    history = ["# GENERATED by scripts/kehillah_faith_revision_build.py.",
               "# Shared by all rites of each faith. No runtime startup status changes."]
    migrate = ["# GENERATED: old saves only. Fresh games mark this version after the lobby.",
               "kehillah_faith_revision_migrate_effect = {",
               "    if = {", "        limit = { NOT = { has_global_variable = kehillah_faith_revision_20261114 } }",
               "        set_global_variable = { name = kehillah_faith_revision_20261114 value = yes }"]
    for faith, known in KNOWN.items():
        history += [f"{faith} = {{", "    867.1.1 = {"]
        if faith == "karaism": history += ["        created = yes"]
        if faith == "rabbinic_faith":
            history += ["        rites = { minhag_yerushalmi = { enabled = yes } }"]
        migrate += [f"        faith:{faith} ?= {{", "            kehillah_sefer_quiet_rite_messages_effect = yes"]
        for status, values in (("known", known), ("permitted", PERMITTED[faith]), ("prohibited", PROHIBITED[faith])):
            values = list(dict.fromkeys(values))
            history += [f"        {status} = {{ {' '.join(values)} }}"]
            for tenet in values:
                migrate += [f"            set_tenet_status = {{ tenet = tenet:{tenet} status = {status} }}"]
        history += ["    }"]
        if faith == "rabbinic_faith":
            history += ["    1000.1.1 = {", "        rites = { minhag_ashkenaz = { enabled = yes } minhag_sepharad = { enabled = yes } }", "    }"]
        history += ["}"]
        migrate += ["        }"]
    migrate += ["        religion:judaism_religion = {", "            every_faith = {",
                "                kehillah_sefer_quiet_rite_messages_effect = yes",
                "                if = {", "                    limit = { has_doctrine = special_doctrine_prophecy_of_malachi }",
                "                    remove_doctrine = special_doctrine_prophecy_of_malachi",
                "                    add_doctrine = kehillah_institutional_headship", "                }",
                "                every_faith_rite = {",
                "                    if = {", "                        limit = { rite_has_doctrine = special_doctrine_prophecy_of_malachi }",
                "                        remove_rite_doctrine = special_doctrine_prophecy_of_malachi",
                "                        add_rite_doctrine = kehillah_institutional_headship", "                    }"]
    for rite, old in OLD_ROSTERS.items():
        migrate += ["                    if = {", f"                        limit = {{ this = rite:{rite} {' '.join('rite_has_tenet = '+t for t in old)} }}"]
        migrate += [f"                        remove_rite_tenet = {t}" for t in old]
        migrate += [f"                        add_rite_tenet = {t}" for t in ROSTERS[rite]]
        migrate += ["                    }"]
    for old, new in LEGACY.items():
        migrate += ["                    if = {", f"                        limit = {{ rite_has_tenet = {old} }}",
                    f"                        remove_rite_tenet = {old}",
                    "                        if = {", f"                            limit = {{ NOT = {{ rite_has_tenet = {new} }} }}",
                    f"                            add_rite_tenet = {new}", "                        }"]
        # Converged retired cores still leave three distinct choices. At most
        # one of these fallbacks is added for the one removed legacy core.
        for fallback in ("tenet_communal_identity", "tenet_literalism", STUDY, LITURGY):
            migrate += ["                        else_if = {", f"                            limit = {{ NOT = {{ rite_has_tenet = {fallback} }} }}",
                        f"                            add_rite_tenet = {fallback}", "                        }"]
        migrate += ["                    }"]
    migrate += ["                    kehillah_standing_refresh_ceilings_rite_effect = yes", "                }", "            }", "        }",
                "        every_living_character = {", "            kehillah_faith_revision_personal_effect = yes", "        }", "    }", "}",
                "kehillah_faith_revision_personal_effect = {"]
    for old, new in LEGACY.items():
        migrate += ["    if = {", f"        limit = {{ has_personal_tenet = {old} }}",
                    f"        remove_personal_tenet = {old}", "        if = {",
                    f"            limit = {{ NOT = {{ has_personal_tenet = {new} }} }}",
                    f"            force_set_personal_tenet = {new}", "        }", "    }",
                    "    if = {", f"        limit = {{ has_variable = kehillah_leaning_{old} }}",
                    f"        remove_variable = kehillah_leaning_{old}",
                    f"        set_variable = {{ name = kehillah_leaning_{new} value = yes }}", "    }",
                    "    if = {", f"        limit = {{ is_target_in_variable_list = {{ name = kehillah_book_tenets target = flag:{old} }} }}",
                    f"        remove_list_variable = {{ name = kehillah_book_tenets target = flag:{old} }}",
                    "        if = {", f"            limit = {{ NOT = {{ is_target_in_variable_list = {{ name = kehillah_book_tenets target = flag:{new} }} }} }}",
                    f"            add_to_variable_list = {{ name = kehillah_book_tenets target = flag:{new} }}", "        }", "    }"]
    migrate += ["}"]
    write("history/faiths/kehillah_baalei_hamiqra_faith_history.txt", "\n".join(history))
    write("common/scripted_effects/kehillah_faith_revision_migration_effects.txt", "\n".join(migrate))
    write("common/on_action/kehillah_faith_revision_on_actions.txt", """# Fresh games read history; only existing saves perform a runtime migration.
on_game_start_after_lobby = { on_actions = { kehillah_faith_revision_new_game } }
kehillah_faith_revision_new_game = {
    effect = { set_global_variable = { name = kehillah_faith_revision_20261114 value = yes } }
}
yearly_global_pulse = { on_actions = { kehillah_faith_revision_yearly } }
kehillah_faith_revision_yearly = { effect = { kehillah_faith_revision_migrate_effect = yes } }
""")


if __name__ == "__main__":
    build()
