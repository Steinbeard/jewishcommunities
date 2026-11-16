"""Generate the dated Karaite roster; see docs/implementation/2026-11-15-karaite-community-seats.md."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOV = "government = kehillah_government succession_laws = { kehillah_appointment_succession_law }"
# key, county, name, start dates, founded (approx), culture, representative names
SEATS = [
    ("nahavand_karaites", "c_nihawand", "Nahavand", (867, 1066), 850, "radhanite", ("Binyamin", "Yosef")),
    ("qumis_karaites", "c_damghan", "Qumis", (867,), 850, "radhanite", ("Shlomo",)),
    ("tustar_karaites", "c_tustar", "Tustar", (1066, 1178), 1000, "radhanite", ("Yitzhak", "Moshe")),
    ("ramla_karaites", "c_jaffa", "Ramla", (1066,), 1000, "mustarab", ("Yosef",)),
    ("gharbiya_karaites", "c_al-gharbiya", "al-Gharbiya", (1066, 1178), 1000, "mustarab", ("Natan", "Aharon")),
    ("talavera_karaites", "c_malagon", "Talavera", (1066,), 1030, "sephardi", ("Yehuda",)),
    ("cyprus_karaites", "c_famagusta", "Cyprus", (1178,), 1100, "romaniote", ("Shlomo",)),
    ("attaleia_karaites", "c_lycia", "Attaleia", (1178,), 1120, "romaniote", ("Eliyahu",)),
    ("ascalon_karaites", "c_ghazza", "Ascalon", (1178,), 1100, "mustarab", ("Avraham",)),
    ("trebizond_karaites", "c_trebizond", "Trebizond", (1178,), 1150, "romaniote", ("Aharon",)),
]


def write(path, contents):
    (ROOT / path).write_text(contents, encoding="utf-8-sig", newline="\n")


def main():
    titles, history, characters, coas = [], [], [], []
    loc = ["l_english:\n"]
    register = ["kehillah_register_karaite_communities_effect = {\n"]
    seed = ["kehillah_history_seed_karaite_roster_effect = {\n"]
    cid = 9001240
    for key, county, place, dates, founded, culture, names in SEATS:
        title = f"d_kehillah_{key}"
        titles.append(f"{title} = {{\n\tlandless = yes\n\tdefinite_form = yes\n\truler_uses_title_name = no\n\tcan_be_named_after_dynasty = no\n\tno_automatic_claims = yes\n\tde_jure_drift_disabled = yes\n\tcapital = {county}\n\tcolor = {{ 102 133 157 }}\n}}\n\n")
        history.append(f"{title} = {{\n\t{founded}.1.1 = {{ effect = {{ set_variable = {{ name = kehillah_founded_year value = {founded} }} }} }}\n")
        for year, name in zip(dates, names):
            birth = year - 40
            death = year + 30
            characters.append(f'{cid} = {{ name = "{name}" rite = "karaism" culture = "{culture}" learning = 10 trait = education_learning_3 {birth}.1.1 = {{ birth = "{birth}.1.1" }} {death}.1.1 = {{ death = "{death}.1.1" }} }} # representative, dates approximate\n')
            history.append(f"\t{year}.{'9.15' if year == 1066 else '1.1'} = {{ liege = 0 holder = {cid} {GOV} }}\n\t{1100 if year == 1066 else 900 if year == 867 else 1210}.1.1 = {{ holder = 0 }}\n")
            cid += 1
        history.append("}\n\n")
        coas.append(f'{title} = {{ pattern = "pattern_solid.dds" color1 = "blue" colored_emblem = {{ texture = "ce_menorah.dds" color1 = "yellow" color2 = "yellow" color3 = "yellow" instance = {{ position = {{ 0.5 0.5 }} scale = {{ 0.72 0.72 }} }} }} }}\n')
        loc.append(f' {title}:0 "Kehillah of {place}"\n {title}_adj:0 "{place} Jewish"\n {title}_desc:0 "A Jewish community of {place}, whose traditions may change with its people."\n')
        register.append(f"\ttitle:{title} ?= {{ kehillah_register_start_community_effect = yes }}\n")
        seed.append(f"\ttitle:{title} = {{ kehillah_history_seed_authored_title_effect = yes }}\n")
    write("common/landed_titles/kehillah_karaite_landed_titles.txt", "".join(titles))
    write("history/titles/kehillah_karaite_titles.txt", "".join(history))
    write("history/characters/kehillah_karaite_leaders.txt", "# Representative leaders; not historical identifications.\n" + "".join(characters))
    write("common/coat_of_arms/coat_of_arms/kehillah_karaite_title_coas.txt", "".join(coas))
    write("localization/english/kehillah_karaite_communities_l_english.yml", "".join(loc))
    write("common/scripted_effects/kehillah_karaite_roster_effects.txt", "".join(register) + "}\n\n" + "".join(seed) + "}\n")


if __name__ == "__main__":
    main()
