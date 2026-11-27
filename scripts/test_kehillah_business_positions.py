"""Integration checks for native staffing and reversible, shared-site production."""
import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

from test_kehillah_household_economy import ROOT, block, read

CAT = json.loads(read("scripts/kehillah_business_catalog.json"))
BUSINESSES = CAT["businesses"]
GENERATED = [
    "common/court_positions/types/kehillah_business_positions.txt",
    "common/scripted_triggers/kehillah_business_triggers.txt",
    "common/script_values/kehillah_business_values.txt",
    "common/scripted_effects/kehillah_business_effects.txt",
    "common/modifiers/kehillah_business_modifiers.txt",
    "common/customizable_localization/kehillah_business_custom_loc.txt",
    "gui/kehillah_businesses.gui",
    "localization/english/kehillah_business_l_english.yml",
    "common/scripted_guis/kehillah_business_generated_gui.txt",
]


class BusinessPositionsTest(unittest.TestCase):
    def test_every_business_has_one_unpaid_native_position_and_complete_callbacks(self):
        positions = read(GENERATED[0])
        self.assertEqual(len(BUSINESSES), 12)
        for business in BUSINESSES:
            body = block(positions, f"kehillah_business_{business['key']}_position")
            self.assertIn("max_available_positions = 1", body)
            self.assertIn("salary = { gold = 0 }", body)
            self.assertIn("received_salary = { gold = 0 }", body)
            self.assertIn("kehillah_business_worker_trigger = yes", body)
            self.assertIn("house.var:kehillah_household_of = scope:liege.primary_title", body)
            for hook in ["received", "revoked", "invalidated", "vacated"]:
                self.assertIn("trigger_event = kehillah_business.1", block(body, "on_court_position_" + hook))
            self.assertIn("any_house_member", body)
            self.assertIn("kehillah_household_assignment_cooldown", body)

    def test_buildings_no_longer_pay_or_produce_unconditionally(self):
        buildings = read("common/domiciles/buildings/kehillah_domicile_buildings.txt")
        for business in BUSINESSES:
            for row in business["track"] + business["extra"]:
                body = block(buildings, row["building"])
                self.assertNotRegex(body, r"(?m)^\s*domicile_monthly_gold_add\s*=")
                self.assertNotRegex(body, r"trade_good_\w+_production_add\s*=")
                self.assertIn(f"kehillah_business_{business['key']} = yes", body)

    def test_tier_income_preserves_original_inheritance_and_annexes(self):
        modifiers = read(GENERATED[4])
        catalog = {b["key"]: b for b in BUSINESSES}
        self.assertEqual([r["income"] for r in catalog["dyers"]["track"]], [0.1, 0.25])
        self.assertEqual([r["income"] for r in catalog["bankers"]["track"]], [0.3, 0.7, 1.2])
        self.assertEqual(sum(r["goods"].get("books_paper", 0) for r in catalog["copyists"]["track"] + catalog["copyists"]["extra"]), 2)
        for b in BUSINESSES:
            for n, row in enumerate(b["track"] + b["extra"]):
                actual = float(re.search(r"domicile_monthly_gold_add\s*=\s*([\d.]+)", block(modifiers, f"kehillah_business_{b['key']}_income_{n}"))[1])
                self.assertAlmostEqual(actual, row["income"])

    def test_native_staffing_is_required_for_each_business_output(self):
        values = read(GENERATED[2])
        for b in BUSINESSES:
            for kind in ["income", "output"]:
                body = block(values, f"kehillah_business_{b['key']}_{kind}_value")
                self.assertIn("value = 0", body)
                self.assertIn(f"kehillah_business_{b['key']}_staffed_trigger = yes", body)
        self.assertIn("kehillah_business_bankers_staffed_trigger = yes", block(read("common/script_values/kehillah_banking_values.txt"), "kehillah_lending_table_tier_value"))

    def test_production_modifiers_encode_totals_for_multiple_communities(self):
        mods, effects = read(GENERATED[4]), read(GENERATED[3])
        goods = {g for b in BUSINESSES for row in b["track"] + b["extra"] for g in row["goods"]}
        for good in goods:
            amounts = {}
            for bit in CAT["production_bits"]:
                mid = f"kehillah_business_supply_{good}_{bit}"
                amounts[bit] = int(re.search(r"production_add\s*=\s*(\d+)", block(mods, mid))[1])
                self.assertIn(f"has_province_modifier = {mid}", effects)
                self.assertIn(f"remove_province_modifier = {mid}", effects)
            for total in range(1024):
                self.assertEqual(sum(amount for bit, amount in amounts.items() if total & bit), total)
        aggregate = block(effects, "kehillah_business_rebuild_site_effect")
        self.assertIn("every_in_global_list", aggregate)
        self.assertIn("holder.domicile.domicile_location = scope:kh_business_site", aggregate)
        self.assertIn("kh_business_excluded_leader", aggregate)
        self.assertIn("days = 120", aggregate)

    def test_business_jobs_do_not_anchor_migration_or_block_council_recruitment(self):
        families = read("common/scripted_effects/kehillah_household_effects.txt")
        self.assertIn("kehillah_has_civic_court_position_trigger = yes", families)
        self.assertNotIn("has_any_court_position =", families)
        self.assertIn("kehillah_business_revoke_all_effect = yes", families)
        civic = block(read(GENERATED[1]), "kehillah_has_civic_court_position_trigger")
        self.assertIn("any_court_position_type", civic)
        self.assertIn("has_court_position = scope:kh_business_civic_type", civic)
        for b in BUSINESSES:
            self.assertIn(f"this = court_position_type:kehillah_business_{b['key']}_position", civic)

    def test_departure_relocation_and_building_completion_reconcile_outputs(self):
        cleanup = block(read("common/scripted_effects/kehillah_quarter_effects.txt"), "kehillah_quarter_district_remove_effect")
        self.assertIn("kehillah_business_rebuild_site_effect = yes", cleanup)
        self.assertIn("kh_business_excluded_leader", cleanup)
        refresh = block(read(GENERATED[3]), "kehillah_business_refresh_effect")
        self.assertIn("var:kehillah_business_last_site", refresh)
        self.assertIn("domicile.domicile_location", refresh)
        self.assertIn("kehillah_business_clear_income_effect = yes", refresh)
        self.assertIn("kehillah_business_positions_migrated", refresh)
        self.assertIn("NOT = { any_house_member = { kehillah_has_business_position_trigger = yes } }", refresh)
        self.assertIn("on_domicile_moved", read("common/on_action/kehillah_business_on_actions.txt"))

    def test_ui_uses_native_appointment_and_specific_business_inspectors(self):
        gui, domicile = read(GENERATED[6]), read("gui/window_domicile.gui")
        self.assertIn(".OpenAppointWindow(DomicileWindow.GetCharacter.Self)", gui)
        self.assertNotIn("CanHirePosition", gui)
        self.assertIn("CourtPosition.OpenReplaceWindow", gui)
        self.assertIn("CourtPosition.OpenRevokeConfirmation", gui)
        self.assertNotIn("Scope.GetFlagName", gui)
        self.assertNotIn("Localize(Concatenate", gui)
        for b in BUSINESSES:
            self.assertIn(f"GetCourtPositionType('kehillah_business_{b['key']}_position').OpenAppointWindow(DomicileWindow.GetCharacter.Self)", gui)
            self.assertIn(f"kehillah_business_inspector_{b['key']} = {{}}", domicile)
            self.assertIn(f"kehillah_business_pin_{b['key']} = {{}}", domicile)
        self.assertIn("kehillah_businesses_summary", domicile)
        self.assertNotIn("kehillah_economy_assign_workshop", read("gui/kehillah_household_economy.gui"))

    def test_every_native_role_resolves_existing_profession_art(self):
        gui = read(GENERATED[6])
        for business in BUSINESSES:
            source = ROOT / business["icon_source"]
            relative = "gfx/interface/icons/court_position_types/kehillah_business_" + business["key"] + "_position.dds"
            target = ROOT / relative
            self.assertTrue(target.is_file(), relative)
            self.assertEqual(target.read_bytes()[:4], b"DDS ")
            self.assertEqual(source.read_bytes(), target.read_bytes())
            self.assertIn(relative, gui)

    def test_all_custom_court_positions_have_role_textures(self):
        roles = set()
        for path in (ROOT / "common/court_positions/types").glob("*.txt"):
            roles.update(re.findall(r"^([a-z0-9_]+)\s*=\s*\{", path.read_text(encoding="utf-8-sig"), re.M))
        for key in roles:
            texture = ROOT / "gfx/interface/icons/court_position_types" / (key + ".dds")
            self.assertTrue(texture.is_file(), key)
            self.assertEqual(texture.read_bytes()[:4], b"DDS ")
        for key, source in CAT["other_position_icons"].items():
            target = ROOT / "gfx/interface/icons/court_position_types" / (key + ".dds")
            self.assertEqual(target.read_bytes(), (ROOT / source).read_bytes())

    def test_generator_is_idempotent(self):
        generated = GENERATED + ["gfx/interface/icons/court_position_types/kehillah_business_" + b["key"] + "_position.dds" for b in BUSINESSES]
        generated += ["gfx/interface/icons/court_position_types/" + key + ".dds" for key in CAT["other_position_icons"]]
        before = {p: hashlib.sha256((ROOT / p).read_bytes()).digest() for p in generated}
        subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "scripts/kehillah_business_positions.py")], check=True)
        self.assertEqual(before, {p: hashlib.sha256((ROOT / p).read_bytes()).digest() for p in generated})


if __name__ == "__main__":
    unittest.main()
