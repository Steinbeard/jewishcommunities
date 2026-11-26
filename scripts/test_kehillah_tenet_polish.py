"""Regression checks for historical status setup and cross-rite solidarity."""
from pathlib import Path
import re
import unittest

from kehillah_holiday_revision_build import block
from kehillah_faith_revision_build import KNOWN, PERMITTED, PROHIBITED, ROSTERS, COVENANT
from kehillah_library_catalog import TENET_INDEX
from test_kehillah_faith_revision import parse, child

ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


class TenetPolish(unittest.TestCase):
    def test_starting_status_date_covers_the_earliest_bookmark(self):
        data = parse(source("history/faiths/kehillah_baalei_hamiqra_faith_history.txt"))
        for faith in KNOWN:
            dates = child(data, faith)
            self.assertIn("867.1.1", [x[0] for x in dates])
            self.assertNotIn("867.1.2", [x[0] for x in dates])
            first = child(dates, "867.1.1")
            for status in ("known", "permitted", "prohibited"):
                self.assertTrue(child(first, status))

    def test_historical_rites_precede_runtime_assignment(self):
        data = parse(source("history/faiths/kehillah_baalei_hamiqra_faith_history.txt"))
        rabbinic = child(data, "rabbinic_faith")
        self.assertEqual([x[0] for x in child(child(rabbinic, "867.1.1"), "rites")], ["minhag_yerushalmi"])
        self.assertEqual({x[0] for x in child(child(rabbinic, "1000.1.1"), "rites")}, {"minhag_ashkenaz", "minhag_sepharad"})
        setup = source("common/scripted_effects/kehillah_synod_effects.txt")
        for rite in ("ashkenaz", "yerushalmi", "sepharad"):
            text = block(setup, f"kehillah_seed_minhag_{rite}_effect")
            self.assertIn(f"NOT = {{ exists = rite:minhag_{rite} }}", text)
        for key in ("kehillah_seed_minhag_ashkenaz_effect", "kehillah_set_community_minhag_yerushalmi_effect", "kehillah_seed_minhag_sepharad_effect"):
            text = block(setup, key)
            self.assertNotIn("set_character_rite =", text)
            self.assertIn("set_character_rite_history =", text)

    def test_no_runtime_status_changes_in_fresh_game_or_familiarity(self):
        hooks = source("common/on_action/kehillah_tenet_polish_on_actions.txt")
        new_game = block(hooks, "kehillah_tenet_polish_new_game")
        self.assertNotIn("set_tenet_status", new_game)
        self.assertNotIn("kehillah_tenet_polish_migrate_effect", new_game)
        text = block(source("common/scripted_effects/kehillah_tenet_polish_effects.txt"), "kehillah_tenet_starting_familiarity_effect")
        self.assertNotIn("set_tenet_status", text)
        self.assertIn("NOT = { knows_tenet", text)
        self.assertIn("status = unknown", text)
        self.assertIn("is_playable_character = yes", text)
        self.assertIn("var:kehillah_tenet_familiarity_faith ?= faith", text)

    def test_old_save_repair_preserves_explicit_council_statuses(self):
        text = source("common/scripted_effects/kehillah_tenet_polish_effects.txt")
        repair = block(text, "kehillah_tenet_polish_migrate_effect")
        self.assertIn("NOT = { has_global_variable = kehillah_tenet_polish_20261115_revival }", repair)
        self.assertIn("kehillah_sefer_quiet_rite_messages_effect", repair)
        # Each status assignment is protected by an exact unknown-state test.
        for parent in re.findall(r"if = \{\s*limit = \{ main_rite = \{ has_tenet_status = \{ tenet = (\w+) status = unknown \} \} \}\s*set_tenet_status = \{ tenet = tenet:(\w+) status = (\w+) \}", repair):
            self.assertEqual(parent[0], parent[1])
        self.assertEqual(repair.count("set_tenet_status ="), repair.count("limit = { main_rite = { has_tenet_status =") + 2)

    def test_default_covenant_replaces_the_rite_penalty_not_vanilla_users(self):
        for rite in ("rabbinism", "minhag_ashkenaz", "minhag_yerushalmi", "karaism", "haymanot", "malabarism", "samaritan"):
            self.assertIn(COVENANT, ROSTERS[rite])
            self.assertNotIn("tenet_communal_identity", ROSTERS[rite])
        text = source("common/religion/tenet_types/kehillah_covenant_community_tenet.txt")
        self.assertIn("same_faith_opinion = 10", text)
        self.assertIn("opinion_of_same_faith = 5", text)
        for field in ("same_faith_different_rite_opinion", "same_faith_different_rite_county_opinion_add", "other_culture_conversion_penalty_active"):
            self.assertNotIn(field, text)
        for path in (ROOT / "common/religion/tenet_types").glob("*.txt"):
            self.assertNotRegex(path.read_text(encoding="utf-8-sig"), r"(?m)^tenet_communal_identity\s*=\s*\{")

    def test_covenant_uses_native_hooks_and_no_new_aid_action(self):
        text = source("common/religion/tenet_types/kehillah_covenant_community_tenet.txt")
        for parameter in ("same_culture_conversion_bonus_active", "same_faith_promote_culture_bonus_active",
                          "sanctify_artifacts_communal", "tenet_communal_identity_free_council_sway",
                          "tenet_communal_identity_language_reward"):
            self.assertIn(parameter, text)
        self.assertIn("prosperity_growth_factor = 0.1", text)
        self.assertNotIn("kehillah_covenant_aid", text)
        action = block(source("common/character_interactions/kehillah_covenant_aid_interactions.txt"), "kehillah_covenant_aid_interaction")
        self.assertIn(("always", "=", "no"), child(child(parse(action), "kehillah_covenant_aid_interaction"), "is_shown"))
        self.assertNotIn("kehillah_covenant_service_reward_effect", source("events/kehillah_crisis_network_events.txt"))

    def test_reviewed_status_corrections_are_explicit(self):
        for faith in KNOWN:
            self.assertNotIn("tenet_communal_identity", KNOWN[faith] + PERMITTED[faith] + PROHIBITED[faith])
            self.assertIn("tenet_gnosticism", PROHIBITED[faith])
            self.assertNotIn("tenet_gnosticism", KNOWN[faith] + PERMITTED[faith])
        repair = source("common/scripted_effects/kehillah_tenet_polish_effects.txt")
        self.assertIn("tenet = tenet:tenet_communal_identity status = unknown", repair)
        self.assertIn("tenet = tenet:tenet_gnosticism status = prohibited", repair)

    def test_physician_and_religious_inquiry_are_compatible(self):
        tenet = block(source("common/religion/tenet_types/kehillah_sefer_tenets.txt"), "tenet_kehillah_hokhmah")
        traits = child(child(parse(tenet), "tenet_kehillah_hokhmah"), "traits")
        self.assertIn("lifestyle_physician", [x[0] for x in child(traits, "virtues")])
        self.assertIn("patient", [x[0] for x in child(traits, "virtues")])
        self.assertNotIn("zealous", [x[0] for x in child(traits, "sins")])
        self.assertNotIn("kehillah_sefer_hokhmah", tenet)
        self.assertNotIn("kehillah_tenet_hokhmah_shtadlan", source("common/script_values/kehillah_track_values.txt"))

    def test_custom_tenets_use_english_labels_and_native_historical_glossaries(self):
        for path, key in (("kehillah_sefer_tenets.txt", "tenet_kehillah_hokhmah"),
                          ("kehillah_study_and_liturgy_tenets.txt", "tenet_kehillah_scholarly_study"),
                          ("kehillah_study_and_liturgy_tenets.txt", "tenet_kehillah_sacred_liturgy"),
                          ("kehillah_sefer_tenets.txt", "tenet_kehillah_avelei_tziyon"),
                          ("kehillah_tenet_types.txt", "tenet_kehillah_kiddush_hashem")):
            text = block(source("common/religion/tenet_types/" + path), key)
            self.assertIn("historical_glossary =", text)
            self.assertNotIn("kehillah_sefer_", text)
        glossary = source("localization/english/kehillah_tenet_polish_l_english.yml")
        self.assertIn("Am Kadosh", glossary)
        self.assertIn("medicine", glossary)
        self.assertNotIn('name:0 "Chosen People"', glossary)

    def test_new_book_and_reform_indices_are_appended(self):
        self.assertEqual(TENET_INDEX[7], "tenet_communal_identity")
        self.assertEqual(TENET_INDEX[12], "tenet_kehillah_sacred_liturgy")
        self.assertEqual(TENET_INDEX[13], COVENANT)
        # Book ordinals remain stable; synod replacement choices are now actual core objects.
        reform = source("events/kehillah_reform_events.txt")
        self.assertIn("ordered_rite_tenet", reform)
        self.assertNotIn("kehillah_reform_replace value =", reform)

    def test_all_starting_cores_have_a_reviewed_status(self):
        for faith, rites in (("rabbinic_faith", ["rabbinism", "minhag_ashkenaz", "minhag_sepharad", "minhag_yerushalmi", "merkabah"]),
                             *[(key, [key]) for key in ("karaism", "haymanot", "malabarism", "samaritan", "kabarism")]):
            known = set(KNOWN[faith]); permitted = set(PERMITTED[faith]); prohibited = set(PROHIBITED[faith])
            self.assertFalse(known & permitted)
            self.assertFalse((known | permitted) & prohibited)
            for rite in rites:
                self.assertTrue(set(ROSTERS[rite]) <= known | permitted)


if __name__ == "__main__":
    unittest.main()
