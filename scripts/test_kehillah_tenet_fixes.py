"""Regression coverage for the rendering/data faults reported in Daniel's UI."""
import re
import unittest
from PIL import Image
from test_kehillah_tenet_polish import ROOT, source, block, parse, child
from kehillah_tenet_icons import NAMES


class TenetFixes(unittest.TestCase):
    def test_ashkenaz_study_default_and_conservative_save_upgrade(self):
        from kehillah_faith_revision_build import ROSTERS
        expected = {'tenet_asceticism', 'tenet_kehillah_scholarly_study', 'tenet_kehillah_covenant_community'}
        self.assertEqual(set(ROSTERS['minhag_ashkenaz']), expected)
        data = child(parse(source('common/religion/rite_types/kehillah_minhag_ashkenaz_rites.txt')), 'minhag_ashkenaz')
        self.assertEqual({x[0] for x in child(data, 'tenets')}, expected)
        upgrade = source('common/scripted_effects/kehillah_tenet_polish_effects.txt')
        self.assertIn('this = rite:minhag_ashkenaz', upgrade)
        self.assertIn('rite_has_tenet = tenet_asceticism', upgrade)
        self.assertIn('rite_has_tenet = tenet_legalism', upgrade)
        self.assertIn('rite_has_tenet = tenet_kehillah_covenant_community', upgrade)
        self.assertIn('remove_rite_tenet = tenet_legalism', upgrade)

    def test_retired_geonut_pilpul_and_minhag_have_no_effects(self):
        text = source('common/religion/tenet_types/kehillah_sefer_tenets.txt')
        for key in ('tenet_kehillah_geonut', 'tenet_kehillah_pilpul', 'tenet_kehillah_minhag_avoteinu'):
            data = child(parse(block(text, key)), key)
            fields = {x[0] for x in data}
            self.assertFalse(fields & {'traits', 'parameters', 'personal_tenet_parameters', 'character_modifier', 'personal_tenet_modifier'})
            self.assertIn(('visible', '=', 'no'), data)
            self.assertIn(('always', '=', 'no'), child(data, 'is_shown'))
            self.assertIn(('always', '=', 'no'), child(data, 'can_pick'))
        witness = child(parse(source('common/religion/tenet_types/kehillah_tenet_types.txt')), 'tenet_kehillah_kiddush_hashem')
        traits = child(witness, 'traits')
        self.assertEqual({x[0] for x in child(traits, 'virtues')}, {'brave', 'zealous'})
        self.assertEqual({x[0] for x in child(traits, 'sins')}, {'craven'})

    def test_study_virtues_and_existing_actions(self):
        text = block(source('common/religion/tenet_types/kehillah_study_and_liturgy_tenets.txt'), 'tenet_kehillah_scholarly_study')
        data = child(parse(text), 'tenet_kehillah_scholarly_study')
        virtues = child(child(data, 'traits'), 'virtues')
        self.assertEqual({x[0] for x in virtues}, {'kehillah_rabbi_trait', 'lifestyle_scholar', 'diligent'})
        self.assertIn('kehillah_scholarly_reading', text)
        self.assertNotIn('kehillah_sacred_study ', text)
        self.assertNotIn('kehillah_sacred_study_decision = {', source('common/decisions/kehillah_faith_practice_decisions.txt'))
        law = source('common/religion/tenet_types/kehillah_legal_pronouncements_override.txt')
        self.assertIn('kehillah_rabbi_trait = { weight = 15', law)

    def test_historical_context_is_a_short_glossary_link(self):
        referenced = set()
        for path in (ROOT / 'common/religion/tenet_types').glob('kehillah*.txt'):
            referenced.update(re.findall(r'desc = (\w*(?:historical_glossary|general_glossary))', path.read_text(encoding='utf-8-sig')))
        found = {}
        for path in (ROOT / 'localization/english').glob('*.yml'):
            for key, body in re.findall(r'^ (\w+):\d* "(.*)"$', path.read_text(encoding='utf-8-sig'), re.M):
                if key in referenced and key.startswith(('kehillah_', 'tenet_kehillah_')):
                    found[key] = body
        self.assertGreaterEqual(len(found), 15)
        for key, body in found.items():
            self.assertRegex(body, r"^\[Glossary\('[^']{1,65}','[a-z_0-9]+'\)\]$", key)
            self.assertNotIn(r'\n', body)

    def test_homeland_targets_own_sites_with_normal_religious_war_rules(self):
        text = block(source('common/religion/tenet_types/kehillah_sefer_tenets.txt'), 'tenet_kehillah_avelei_tziyon')
        for flag in ('tenet_pentarchy_holy_site_prosperity', 'tenet_pentarchy_pilgrim_circuit',
                     'tenet_pentarchy_pilgrim_circuit_companions', 'kehillah_recover_holy_site'):
            self.assertIn(flag, text)
        self.assertIn('fervor_per_holy_site = 0.05', text)
        cb = source('common/casus_belli_types/kehillah_sacred_homeland.txt')
        for condition in ('any_holy_site = { holy_site_county = scope:target }',
                          'rite_has_parameter = kehillah_recover_holy_site',
                          'is_valid_religious_war_target_trigger', 'tier = tier_county',
                          'holy_wars_forbidden', 'multiply = 0.5', 'on_victory ='):
            self.assertIn(condition, cb)
        self.assertNotIn('great_holy_wars_active', text)

    def test_icon_assets_match_native_canvas_and_keep_transparency(self):
        for name in NAMES:
            with Image.open(ROOT / 'gfx/interface/icons/faith_tenets' / (name + '.dds')) as image:
                self.assertEqual(image.size, (260, 400))
                self.assertEqual(image.mode, 'RGBA')
                self.assertEqual(image.getchannel('A').getextrema(), (0, 255))

    def test_retired_identity_tenets_are_hidden_and_unselectable(self):
        for path, key in (('kehillah_baalei_hamiqra_tenets.txt', 'tenet_baalei_hamiqra'),
                          ('kehillah_talmud_torah_tenets.txt', 'tenet_talmud_torah')):
            data = child(parse(block(source('common/religion/tenet_types/' + path), key)), key)
            self.assertIn(('visible', '=', 'no'), data)
            self.assertIn(('always', '=', 'no'), child(data, 'is_shown'))
            self.assertIn(('always', '=', 'no'), child(data, 'can_pick'))


if __name__ == '__main__':
    unittest.main()
