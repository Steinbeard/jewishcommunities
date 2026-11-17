"""County-library preservation contracts; runtime behavior needs the live probe."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")

def block(text, name):
    start = text.index(name + " = {")
    opening = text.index("{", start)
    depth = 1
    for i in range(opening + 1, len(text)):
        depth += (text[i] == "{") - (text[i] == "}")
        if depth == 0:
            return text[start:i + 1]
    raise AssertionError("unclosed block")

class CountyLibrary(unittest.TestCase):
    def test_relocation_never_changes_collections_or_registries(self):
        source = read("common/scripted_effects/kehillah_library_county_effects.txt")
        code = re.sub(r"#.*", "", source)
        self.assertNotRegex(code, r"kehillah_library_works|seed_|register_library|clear_variable|change_title_holder")
        self.assertNotIn("add_to_global_variable_list", code)

    def test_grant_and_old_save_refresh_share_relocation(self):
        grant = block(read("common/scripted_effects/kehillah_sanhedrin_effects.txt"), "kehillah_grant_community_county_effect")
        self.assertLess(grant.index("resolve_title_and_vassal_change"), grant.index("kehillah_lib_refresh_seat_effect"))
        self.assertIn("scope:kehillah_land_community = {\n\t\tkehillah_lib_refresh_seat_effect", grant)
        yearly = block(read("common/scripted_effects/kehillah_sefer_effects.txt"), "kehillah_lib_yearly_library_effect")
        self.assertIn("kehillah_lib_refresh_seat_effect = yes", yearly)

    def test_temple_precedes_domicile_fallback(self):
        seat = block(read("common/scripted_effects/kehillah_sefer_effects.txt"), "kehillah_lib_refresh_seat_effect")
        self.assertLess(seat.index("kehillah_lib_reconcile_county_temple_effect"), seat.index("tier = tier_barony"))
        self.assertLess(seat.index("exists = var:kehillah_library_temple_seat"), seat.index("holder ?= { exists = domicile }"))

    def test_seat_is_local_jewish_temple_and_persistent(self):
        source = read("common/scripted_effects/kehillah_library_county_effects.txt")
        self.assertIn("title_capital_county.holder ?= holder", source)
        self.assertEqual(source.count("has_holding_type = church_holding"), 2)
        self.assertEqual(source.count("barony.holder ?= { faith.religion = religion:judaism_religion }"), 2)
        self.assertIn("limit = { NOT = { has_variable = kehillah_library_temple_seat } }", source)
        self.assertIn("remove_variable = kehillah_library_temple_seat", source)

    def test_county_card_reads_physical_seat(self):
        link = block(read("common/scripted_effects/kehillah_library_card_effects.txt"), "kehillah_lib_link_card_county_effect")
        self.assertIn("var:kehillah_library_seat.county ?=", link)
        self.assertIn("exists = var:kehillah_library_temple_seat", link)

if __name__ == "__main__":
    unittest.main()
