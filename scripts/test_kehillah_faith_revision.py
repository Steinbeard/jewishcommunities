"""Source-executed regression checks for canon, festival selection, and saves.

These evaluate the actual capability expressions. They cannot establish engine
serialization, event rendering, or initialization order; the live checklist does.
"""
from pathlib import Path
import re
import unittest

from kehillah_holiday_revision_build import block
from kehillah_library_catalog import TENET_INDEX, dynamic_tenet_branches

ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def parse(text):
    tokens = re.findall(r'#[^\n]*|"(?:\\.|[^"\\])*"|\?=|>=|<=|[{}=<>]|[^\s{}=<>]+', text)
    tokens = [t for t in tokens if not t.startswith("#")]
    i = 0

    def body():
        nonlocal i
        out = []
        while i < len(tokens) and tokens[i] != "}":
            if i + 1 >= len(tokens) or tokens[i + 1] not in ("=", "?=", ">=", "<=", ">", "<"):
                out.append((tokens[i], "", None)); i += 1
                continue
            key = tokens[i]; op = tokens[i+1]; i += 2
            if tokens[i] == "{":
                i += 1; value = body(); i += 1
            else:
                value = tokens[i]; i += 1
            out.append((key, op, value))
        return out
    return body()


def child(tree, name):
    return next(value for key, _, value in tree if key == name)


TRIGGERS = {}
for path in ("common/scripted_triggers/jewish_holiday_scripted_triggers.txt",
             "common/scripted_triggers/kehillah_holiday_capability_triggers.txt",
             "common/scripted_triggers/kehillah_rite_tradition_triggers.txt"):
    TRIGGERS.update({key: value for key, _, value in parse(source(path))})


def evaluate(tree, state):
    result = []
    branch = False
    for key, op, value in tree:
        if key in ("trigger_if", "if"):
            branch = evaluate(child(value, "limit"), state)
            result.append(not branch or evaluate([x for x in value if x[0] != "limit"], state))
        elif key in ("trigger_else", "else"):
            if not branch: result.append(evaluate(value, state))
        elif key == "AND": result.append(evaluate(value, state))
        elif key in ("OR", "NOR"):
            yes = any(evaluate([x], state) for x in value)
            result.append(yes if key == "OR" else not yes)
        elif key == "NOT": result.append(not evaluate(value, state))
        elif key in TRIGGERS:
            result.append(evaluate(TRIGGERS[key], state) == (value == "yes"))
        elif key in ("rite", "rite_faith") and isinstance(value, list):
            result.append(evaluate(value, state))
        elif key in ("rite_has_doctrine", "has_doctrine"):
            doctrines = state["rite_doctrines"] if key == "rite_has_doctrine" else state["faith_doctrines"]
            result.append(value in doctrines)
        elif key == "faith.religion": result.append(value == state["religion"])
        elif key == "rite_faith": result.append(value == "faith:" + state["faith"])
        elif key == "this": result.append(value == "rite:" + state["rite"])
        elif key == "rite_has_tenet": result.append(value in state["cores"])
        elif key == "has_personal_tenet": result.append(value in state["personal"])
        elif key == "has_character_flag": result.append(value in state["flags"])
        elif key in ("any_child", "any_courtier"):
            people = state["children"] if key == "any_child" else state["courtiers"]
            result.append(any(evaluate(value, person) for person in people))
        elif key == "current_month": result.append(int(value) == state["month"])
        elif key == "always": result.append(value == "yes")
        elif key in ("is_alive", "is_adult", "is_imprisoned", "is_ai"):
            result.append(state[key] == (value == "yes"))
        else: raise AssertionError(f"Unsupported expression: {key} {op} {value}")
    return all(result)


def state(faith, authority, rite=None, local=()):
    person = dict(religion="religion:judaism_religion", is_adult=True, is_imprisoned=False)
    return dict(faith=faith, rite=rite or faith, religion="religion:judaism_religion",
                faith_doctrines={authority}, rite_doctrines=set(local), cores=set(), personal=set(),
                flags=set(), month=1, is_alive=True, is_adult=True, is_imprisoned=False, is_ai=False,
                children=[dict(person, is_adult=False)], courtiers=[person])


class FaithRevision(unittest.TestCase):
    def test_holiday_matrix_in_every_government_and_personal_tenet_combination(self):
        rows = [
            ("rabbinic_faith", "rabbinic", set(range(1, 14))),
            ("karaism", "toric", set(range(1, 14)) - {5, 6}),
            ("haymanot", "kohanim", set(range(1, 14)) - {5, 6, 7, 8}),
            ("samaritan", "samaritan_torah", set(range(1, 14)) - {5, 6, 7, 8}),
            ("malabarism", "toric", set(range(1, 14)) - {5, 6}),
            ("kabarism", "rabbinic", set(range(1, 14))),
        ]
        for faith, authority, expected in rows:
            for government in ("courtier", "feudal", "kehillah", "adventurer"):
                for personal in (set(), {"tenet_ritual_celebrations", "tenet_kehillah_sacred_liturgy"}):
                    s = state(faith, f"temple_authority_{authority}_doctrine")
                    s.update(government=government, personal=personal)
                    actual = {n for n in range(1, 14) if evaluate(TRIGGERS[f"jewish_holiday_scene_{n:04d}_eligible_trigger"], s)}
                    self.assertEqual(actual, expected, (faith, government, personal))

    def test_local_authority_supersedes_parent_faith(self):
        s = state("rabbinic_faith", "temple_authority_rabbinic_doctrine", local={"temple_authority_toric_doctrine"})
        self.assertFalse(evaluate(TRIGGERS["is_rabbinic_authority_jewish_trigger"], s))
        self.assertTrue(evaluate(TRIGGERS["jewish_holiday_accepts_esther_trigger"], s))

    def test_secondary_rabbinic_rites_inherit_authority(self):
        for rite in ("minhag_ashkenaz", "minhag_sepharad", "minhag_yerushalmi", "merkabah"):
            s = state("rabbinic_faith", "temple_authority_rabbinic_doctrine", rite=rite)
            self.assertTrue(evaluate(TRIGGERS["is_rabbinic_authority_jewish_trigger"], s))

    def test_conversion_and_imprisonment_invalidate_the_existing_queue(self):
        for n in range(1, 14):
            s = state("rabbinic_faith", "temple_authority_rabbinic_doctrine")
            s["flags"].add(f"jewish_holiday_{n:04d}_pending")
            self.assertFalse(evaluate(TRIGGERS["jewish_holiday_no_pending_trigger"], s))
            s["religion"] = "religion:christianity_religion"
            self.assertFalse(evaluate(TRIGGERS[f"jewish_holiday_scene_{n:04d}_eligible_trigger"], s))
            s["religion"] = "religion:judaism_religion"; s["is_imprisoned"] = True
            self.assertFalse(evaluate(TRIGGERS[f"jewish_holiday_scene_{n:04d}_eligible_trigger"], s))
        calendar = block(source("common/on_action/jewish_holiday_on_actions.txt"), "jewish_holiday_calendar_pulse")
        for n in range(1, 14):
            remove = calendar.index(f"remove_character_flag = jewish_holiday_{n:04d}_pending")
            display = calendar.index(f"trigger_event = jewish_holidays.{n:04d}")
            self.assertLess(remove, display)

    def test_one_engine_pulse_and_eligibility_before_draw(self):
        actions = parse(source("common/on_action/jewish_holiday_on_actions.txt"))
        self.assertEqual(sum(k == "random_yearly_everyone_pulse" for k, _, _ in actions), 1)
        self.assertNotIn("random_yearly_playable_pulse", [x[0] for x in actions])
        yearly = child(actions, "jewish_holiday_yearly_pulse")
        choices = child(child(child(yearly, "effect"), "random"), "random_list")
        self.assertEqual(len(choices), 13)
        for _, _, choice in choices: self.assertIsInstance(child(choice, "trigger"), list)

    def test_scenes_requiring_people_are_filtered_before_draw(self):
        s = state("rabbinic_faith", "temple_authority_rabbinic_doctrine")
        s["children"] = []; s["courtiers"] = []
        for n in (3, 9, 12):
            self.assertFalse(evaluate(TRIGGERS[f"jewish_holiday_scene_{n:04d}_eligible_trigger"], s))
        self.assertTrue(evaluate(TRIGGERS["jewish_holiday_scene_0004_eligible_trigger"], s))
        variants = parse(source("events/kehillah_holiday_variant_events.txt"))
        self.assertIn("any_child", [x[0] for x in child(child(variants, "jewish_holidays.0203"), "trigger")])

    def test_preserved_player_and_ai_cadence(self):
        actions = parse(source("common/on_action/jewish_holiday_on_actions.txt"))
        chance = child(child(child(child(actions, "jewish_holiday_yearly_pulse"), "effect"), "random"), "chance")

        def number(tree, s):
            value = 0
            for key, _, item in tree:
                if key == "value": value = int(item)
                elif key == "if" and evaluate(child(item, "limit"), s):
                    value = number([x for x in item if x[0] != "limit"], s)
            return value

        for ai, ordinary, festive in ((False, 60, 75), (True, 12, 16)):
            s = state("karaism", "temple_authority_toric_doctrine"); s["is_ai"] = ai
            self.assertEqual(number(chance, s), ordinary)
            s["cores"].add("tenet_ritual_celebrations"); self.assertEqual(number(chance, s), festive)
            s["personal"].add("tenet_ritual_celebrations"); self.assertEqual(number(chance, s), festive)
            s["cores"].clear(); self.assertEqual(number(chance, s), festive)

    def test_stable_numeric_slots_and_no_double_argument(self):
        self.assertEqual(TENET_INDEX, [
            "tenet_kehillah_scholarly_study", "tenet_literalism", "tenet_kehillah_hokhmah",
            "tenet_unrelenting_faith", "tenet_religious_legal_pronouncements", "tenet_kehillah_scholarly_study",
            "tenet_religious_legal_pronouncements", "tenet_communal_identity", "tenet_kehillah_avelei_tziyon",
            "tenet_esotericism", "tenet_asceticism", "tenet_kehillah_kiddush_hashem", "tenet_kehillah_sacred_liturgy",
            "tenet_kehillah_covenant_community", "tenet_kehillah_messianic_hope", "tenet_kehillah_prophetic_revelation", "tenet_kehillah_temple_service"])
        branches = dynamic_tenet_branches("sample", lambda cond, tenet: [(cond, tenet)])
        aliases = [cond for cond, tenet in branches if "_tenet_b ?= 6" in cond]
        self.assertEqual(len(aliases), 1)
        self.assertIn("_tenet_a ?= 1", aliases[0]); self.assertIn("_tenet_a ?= 6", aliases[0])
        reform = source("events/kehillah_reform_events.txt")
        self.assertIn("ordered_rite_tenet", reform)
        self.assertIn("value = var:kehillah_reform_drop_1", reform)

    def test_no_dlc_dependency_and_poet_virtue(self):
        text = source("common/religion/tenet_types/kehillah_study_and_liturgy_tenets.txt")
        self.assertNotIn("requires_dlc_flag", text)
        self.assertIn("virtues = { lifestyle_poet =", block(text, "tenet_kehillah_sacred_liturgy"))

    def test_personal_study_never_changes_acceptance_of_oral_torah(self):
        text = source("common/script_values/kehillah_library_standing_values.txt")
        standing = child(parse(block(text, "kehillah_lib_standing_work_mishnah")), "kehillah_lib_standing_work_mishnah")
        for faith, doctrine, expected in (("rabbinic_faith", "rabbinic", 9), ("karaism", "toric", 2),
                                          ("haymanot", "kohanim", 4), ("samaritan", "samaritan_torah", 4)):
            s = state(faith, f"temple_authority_{doctrine}_doctrine")
            for personal in (set(), {"tenet_kehillah_scholarly_study", "tenet_kehillah_hokhmah", "tenet_literalism"}):
                s["personal"] = personal
                value = int(child(standing, "value"))
                for key, _, clause in standing:
                    if key in ("if", "else_if") and evaluate(child(clause, "limit"), s):
                        value = int(child(clause, "value")); break
                self.assertEqual(value, expected, (faith, personal))

    def test_fresh_game_never_changes_tenet_status(self):
        text = source("common/on_action/kehillah_faith_revision_on_actions.txt")
        self.assertNotIn("set_tenet_status", block(text, "kehillah_faith_revision_new_game"))
        history = source("history/faiths/kehillah_baalei_hamiqra_faith_history.txt")
        self.assertNotIn("tenet_kehillah_kiddush_hashem", history)
        # Authority still belongs to doctrine; the wider review adds explicit
        # ritual prohibitions, never a blanket ban on scholarship or judgments.
        from kehillah_faith_revision_build import PROHIBITED
        for values in PROHIBITED.values():
            self.assertEqual(set(values), {"tenet_human_sacrifice", "tenet_ritual_cannibalism", "tenet_divine_marriage", "tenet_gnosticism"})

    def test_deaths_never_grant_greatness_or_a_tenet_death_bonus(self):
        mob = source("common/scripted_effects/kehillah_mob_effects.txt")
        self.assertNotIn("kehillah_kiddush_hashem_rite", block(mob, "kehillah_pogrom_effect"))
        self.assertNotIn("kehillah_pogrom_martyr_greatness", mob)
        remembrance = block(source("common/scripted_effects/kehillah_faith_practice_effects.txt"), "kehillah_witness_after_persecution_effect")
        self.assertIn("var:kehillah_witness_attack_grade >= 3", remembrance)
        self.assertIn("scope:kehillah_pogrom_original_faith = {", remembrance)
        self.assertIn("AMOUNT = 5", remembrance)


if __name__ == "__main__":
    unittest.main()
