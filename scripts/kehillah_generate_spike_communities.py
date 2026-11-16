"""Generate the 2026-11-15 roster additions from the Ibn Daud / Benjamin spike.

Edit the tables here, then run:
    python -I scripts/kehillah_generate_spike_communities.py
It rewrites five files (landed titles, title history, leaders, coats of arms,
English localization) and the wiring effects file. Design and sources:
docs/research/2026-11-14-sefer-haqabbalah-and-benjamin-community-spike.md and
docs/implementation/2026-11-15-spike-roster-communities.md.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# key, county, rgb, coa colour, display name, adjective, founded (approx), description
COMMUNITIES = [
    ("saragossa", "c_zaragoza", (170, 110, 60), "red", "Saragossa", "Saragossan Jewish", 900,
     "The great Jewish community of the Ebro, home of Ibn Gabirol, Ibn Janah and Bahya ibn Paquda."),
    ("seville", "c_sevilla", (190, 140, 60), "yellow", "Seville", "Sevillian Jewish", 900,
     "A wealthy Andalusi community at the court of the Abbadid kings."),
    ("malaga", "c_malaga", (180, 120, 70), "blue", "Malaga", "Malagan Jewish", 900,
     "A port community of the Zirid kingdom, where Samuel ha-Nagid once kept a spice shop and Ibn Gabirol was born."),
    ("denia", "c_denia", (150, 120, 80), "blue_light", "Denia", "Denian Jewish", 1000,
     "A taifa port whose Jewish community later took Isaac ben Reuben al-Bargeloni as its judge."),
    ("barcelona", "c_barcelona", (160, 70, 70), "yellow", "Barcelona", "Barcelonan Jewish", 876,
     "A Catalan community under the counts of Barcelona, its sages known as far as Benjamin of Tudela's travels."),
    ("gerona", "c_girona", (140, 80, 80), "red", "Gerona", "Geronese Jewish", 890,
     "A small Catalan congregation in the shadow of the cathedral."),
    ("tudela", "c_tudela", (150, 100, 70), "green", "Tudela", "Tudelan Jewish", 900,
     "A community on the Ebro frontier, the home of Benjamin of Tudela."),
    ("huesca", "c_huesca", (140, 100, 90), "brown", "Huesca", "Oscan Jewish", 900,
     "A community of the upper Ebro valley, old in the Muslim north and kept by the kings of Aragon."),
    ("calatayud", "c_calatayud", (150, 110, 90), "black", "Calatayud", "Calatayud Jewish", 1000,
     "A community of the Jalon valley in the kingdom of Aragon."),
    ("tarragona", "c_tarragona", (130, 90, 90), "blue_light", "Tarragona", "Tarragonan Jewish", 1130,
     "A small community in the resettled Catalan port."),
    ("leon", "c_leon", (120, 70, 110), "purple", "León", "Leonese Jewish", 905,
     "A community of the royal city of León, traders and tax-farmers to its kings."),
    ("burgos", "c_burgos", (130, 80, 100), "purple", "Burgos", "Burgalese Jewish", 1000,
     "A Castilian community at the head of the road to Santiago."),
    ("otranto", "c_lecce", (90, 110, 160), "blue", "Otranto", "Otrantine Jewish", 900,
     "The Apulian seat of learning: 'from Bari goes forth Torah, and the word of the Lord from Otranto.'"),
    ("thebes", "c_attica", (100, 110, 170), "purple", "Thebes", "Theban Jewish", 900,
     "The largest Jewish community of Byzantine Greece, renowned for its silk and purple dyers."),
    ("salonica", "c_thessalonika", (90, 120, 170), "blue", "Salonica", "Salonican Jewish", 50,
     "An ancient Macedonian community of silk-weavers."),
    ("djerba", "c_djerba", (170, 140, 90), "green", "Djerba", "Djerban Jewish", 500,
     "An island community that by its own tradition dates from the First Temple."),
    ("qala_hammad", "c_satif", (160, 120, 90), "brown", "the Qal'a of the Banu Hammad", "Hammadid Jewish", 1010,
     "The community of the Hammadid capital, where Isaac Alfasi was born."),
    ("tyre", "c_acre", (80, 120, 140), "blue_light", "Tyre", "Tyrian Jewish", 300,
     "A coastal community of glass-makers and shipowners, once the refuge of the Palestinian academy."),
    ("salerno", "c_salerno", (110, 100, 150), "red", "Salerno", "Salernitan Jewish", 900,
     "The largest Jewish community of southern Italy, beside the famous school of medicine."),
    ("marseille", "c_provence", (90, 130, 140), "green", "Marseille", "Massiliot Jewish", 576,
     "A Provencal port with two congregations, an upper house of study and a lower congregation."),
    ("regensburg", "c_regensburg", (120, 100, 140), "black", "Regensburg", "Regensburg Jewish", 1020,
     "A Danube community of long-distance traders, open to the east."),
    ("mosul", "c_mosul", (120, 130, 90), "green", "Mosul", "Mosuli Jewish", 700,
     "A great Mesopotamian community led by a nasi of the House of David."),
    ("aleppo", "c_aleppo", (130, 120, 80), "yellow", "Aleppo", "Aleppine Jewish", 700,
     "A large Syrian community on the caravan road to the Euphrates."),
    ("hamadan", "c_hamadan", (110, 140, 100), "blue_light", "Hamadan", "Hamadani Jewish", 600,
     "A Persian community that keeps the tomb of Mordecai and Esther."),
]

# Bookmark holders. A string ID reuses an existing character; a tuple makes a new leader:
# (id, name, culture, skill, rabbi, birth, death, dynasty, note)
H1066 = {
    "saragossa": "9002097",   # Bahya ibn Paquda
    "seville": "9002099",     # Judah ibn Bal'am
    "barcelona": "9002086",   # Reuben, father of Isaac al-Bargeloni
    "leon": "9002081",        # Joseph ben Joab Escapat
    "burgos": "9002084",      # Isaac ibn Shalbib
    "malaga": (9001200, "Yosef", "sephardi", "stewardship", False, 1020, 1090, None, "representative"),
    "denia": (9001201, "Yaakov", "sephardi", "learning", True, 1022, 1090, None, "representative"),
    "gerona": (9001202, "Avraham", "sephardi", "stewardship", False, 1024, 1095, None, "representative"),
    "tudela": (9001203, "Shlomo", "sephardi", "stewardship", False, 1022, 1090, None, "representative"),
    "huesca": (9001204, "Yitzhak", "sephardi", "stewardship", False, 1025, 1095, None, "representative"),
    "otranto": (9001205, "Menachem", "italki", "learning", True, 1020, 1090, None, "representative"),
    "thebes": (9001206, "Eliyahu", "romaniote", "stewardship", False, 1020, 1090, None, "representative"),
    "djerba": (9001207, "Natan", "maaravi", "learning", True, 1022, 1090, None, "representative"),
    "qala_hammad": (9001208, "Yehuda", "maaravi", "stewardship", False, 1018, 1085, None, "representative"),
}
H1178 = {
    "thebes": (9001220, "Kuti", "romaniote", "learning", True, 1120, 1190, None, "Benjamin's chief rabbi of Thebes"),
    "mosul": (9001221, "Zakkai", "bavlim", "diplomacy", True, 1115, 1185, None, "Benjamin's 'Zakkai the Nasi' of the House of David"),
    "aleppo": (9001222, "Moshe", "mustarab", "learning", True, 1120, 1190, "9000028", "Benjamin's R. Moses el-Constantini"),
    "saragossa": (9001223, "Avraham", "sephardi", "stewardship", False, 1130, 1200, None, "representative"),
    "tudela": (9001224, "Yosef", "sephardi", "stewardship", False, 1130, 1200, None, "representative"),
    "salonica": (9001225, "Shmuel", "romaniote", "learning", True, 1120, 1190, None, "Benjamin's chief rabbi R. Samuel"),
    "tyre": (9001226, "Efraim", "mustarab", "learning", True, 1115, 1185, None, "Benjamin's R. Ephraim the Dayan"),
    "salerno": (9001227, "Yehuda", "italki", "learning", True, 1120, 1190, None, "Benjamin's R. Judah ben Isaac"),
    "marseille": (9001228, "Yitzhak", "provenci", "learning", True, 1122, 1193, None, "R. Isaac ben Abba Mari, author of the Ittur"),
    "barcelona": (9001229, "Sheshet", "sephardi", "diplomacy", False, 1131, 1209, "9000027", "Sheshet Benveniste, physician and statesman"),
    "regensburg": (9001230, "Efraim", "ashkenazi", "stewardship", False, 1125, 1195, None, "representative"),
    "hamadan": (9001231, "Mordechai", "radhanite", "stewardship", False, 1125, 1195, None, "representative"),
    "gerona": (9001232, "Avraham", "sephardi", "stewardship", False, 1130, 1200, None, "representative"),
    "huesca": (9001233, "Shlomo", "sephardi", "stewardship", False, 1130, 1200, None, "representative"),
    "leon": (9001234, "David", "sephardi", "stewardship", False, 1130, 1200, None, "representative"),
    "burgos": (9001235, "Yaakov", "sephardi", "stewardship", False, 1130, 1200, None, "representative"),
    "calatayud": (9001236, "Yitzhak", "sephardi", "stewardship", False, 1130, 1200, None, "representative"),
    "tarragona": (9001237, "Binyamin", "sephardi", "stewardship", False, 1135, 1205, None, "representative"),
    "otranto": (9001238, "Menachem", "italki", "learning", True, 1125, 1195, None, "Benjamin's R. Menachem of Otranto"),
    "djerba": (9001239, "Natan", "maaravi", "learning", True, 1130, 1200, None, "representative"),
}

GOV = "government = kehillah_government succession_laws = { kehillah_appointment_succession_law }"


def holder_id(h):
    return h if isinstance(h, str) else str(h[0])


def write(path, text):
    p = ROOT / path
    p.write_text(text, encoding="utf-8-sig", newline="\r\n")
    print("wrote", path)


def main():
    head = "# GENERATED by scripts/kehillah_generate_spike_communities.py -- edit the tables there.\n"
    lt, th, coa, loc, ch = [head], [head], [head], ["l_english:\n", " # GENERATED by scripts/kehillah_generate_spike_communities.py\n"], [head]
    reg, seed = [], []
    for key, county, rgb, coacol, name, adj, founded, desc in COMMUNITIES:
        t = f"d_kehillah_{key}"
        lt.append(f"""
{t} = {{
	landless = yes
	definite_form = yes
	ruler_uses_title_name = no
	can_be_named_after_dynasty = no
	can_use_nomadic_naming = no
	no_automatic_claims = yes
	de_jure_drift_disabled = yes
	capital = {county}
	color = {{ {rgb[0]} {rgb[1]} {rgb[2]} }}
}}
""")
        lines = [f"\n{t} = {{", f"\t{founded}.1.1 = {{ effect = {{ set_variable = {{ name = kehillah_founded_year value = {founded} }} }} }}"]
        if key in H1066:
            lines.append(f"\t1066.9.15 = {{ liege = 0 holder = {holder_id(H1066[key])} {GOV} }}")
            lines.append("\t1100.1.1 = { holder = 0 }")
        if key in H1178:
            lines.append(f"\t1178.1.1 = {{ liege = 0 holder = {holder_id(H1178[key])} {GOV} }}")
            lines.append("\t1210.1.1 = { holder = 0 }")
        lines.append("}")
        th.append("\n".join(lines) + "\n")
        coa.append(f"""
{t} = {{
	pattern = "pattern_solid.dds"
	color1 = "{coacol}"
	colored_emblem = {{
		texture = "ce_menorah.dds"
		color1 = "{'white' if coacol == 'yellow' else 'yellow'}"
		color2 = "{'white' if coacol == 'yellow' else 'yellow'}"
		color3 = "{'white' if coacol == 'yellow' else 'yellow'}"
		instance = {{ position = {{ 0.5 0.5 }} scale = {{ 0.72 0.72 }} }}
	}}
}}
""")
        cap = name[0].upper() + name[1:]
        loc.append(f' {t}:0 "Kehillah of {name}"\n {t}_adj:0 "{adj}"\n {t}_desc:0 "{desc}"\n')
        _ = cap
        reg.append(f"\ttitle:{t} ?= {{ kehillah_register_start_community_effect = yes }}")
        seed.append(f"\ttitle:{t} = {{ kehillah_history_seed_authored_title_effect = yes }}")

    for book in (H1066, H1178):
        for key, h in book.items():
            if isinstance(h, str):
                continue
            cid, nm, cul, skill, rabbi, b, d, dyn, note = h
            traits = f"trait = education_{skill}_3" + (" trait = kehillah_rabbi_trait" if rabbi else "")
            dyn_s = f" dynasty = {dyn}" if dyn else ""
            ch.append(f'{cid} = {{ name = "{nm}"{dyn_s} rite = "rabbinism" culture = "{cul}" {skill} = 10 {traits} '
                      f'{b}.1.1 = {{ birth = "{b}.1.1" }} {d}.1.1 = {{ death = "{d}.1.1" }} }} # {key}: {note}; dates estimated\n')

    write("common/landed_titles/kehillah_spike_landed_titles.txt", "".join(lt))
    write("history/titles/kehillah_spike_titles.txt", "".join(th))
    write("common/coat_of_arms/coat_of_arms/kehillah_spike_title_coas.txt", "".join(coa))
    write("localization/english/kehillah_spike_communities_l_english.yml", "".join(loc))
    write("history/characters/kehillah_spike_leaders.txt", "".join(ch))
    write("common/scripted_effects/kehillah_spike_roster_effects.txt", head + """
# Called from kehillah_on_actions.txt's registry block, after the older roster.
kehillah_register_spike_communities_effect = {
""" + "\n".join(reg) + """
}

# Called from kehillah_history_seed_authored_roster_effect.
kehillah_history_seed_spike_roster_effect = {
""" + "\n".join(seed) + "\n}\n")


if __name__ == "__main__":
    main()
