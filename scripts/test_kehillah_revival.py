"""Checks for real integration boundaries: native pilgrimage, book saves,
revival locks, and pledge/ritual rewards. Engine/runtime tests remain separate.
"""
import unittest
from pathlib import Path
from PIL import Image
from test_kehillah_tenet_polish import ROOT, source, block, parse, child
from kehillah_revival_build import TENETS, GAME
from kehillah_library_catalog import TENET_INDEX
from kehillah_faith_revision_build import ROSTERS, KNOWN


class Revival(unittest.TestCase):
    def test_all_three_have_distinct_follower_and_personal_effects(self):
        text = source('common/religion/tenet_types/kehillah_revival_tenets.txt')
        for key in TENETS:
            data = child(parse(block(text, key)), key)
            self.assertTrue(child(data, 'character_modifier'))
            self.assertTrue(child(data, 'personal_tenet_modifier'))
            self.assertTrue(child(data, 'parameters'))
            self.assertTrue(child(data, 'personal_tenet_parameters'))
            with Image.open(ROOT / 'gfx/interface/icons/faith_tenets' / (key.removeprefix('tenet_') + '.dds')) as image:
                self.assertEqual(image.size, (260, 400))
                self.assertEqual(image.getchannel('A').getextrema(), (0, 255))

    def test_native_pilgrimage_preserved_except_host_intent_and_live_completion_hook(self):
        original = (GAME / 'common/activities/activity_types/pilgrimage.txt').read_text(encoding='utf-8-sig')
        result = source('common/activities/activity_types/pilgrimage.txt')
        self.assertEqual(result.count('kehillah_complete_sacrifice_intent_effect = yes'), 1)
        result = result.replace(' kehillah_offer_sacrifice_intent', '').replace('        kehillah_complete_sacrifice_intent_effect = yes\n', '')
        self.assertEqual(result, original)

    def test_gerizim_and_jerusalem_are_distinguished_by_barony_not_shared_county(self):
        text = source('common/scripted_triggers/kehillah_revival_triggers.txt')
        data = child(parse(block(text, 'kehillah_sacrifice_destination_trigger')), 'kehillah_sacrifice_destination_trigger')
        alternatives = child(data, 'OR')
        self.assertEqual(len(alternatives), 2)
        self.assertIn('activity_location.barony = title:b_nablus', text)
        self.assertIn('activity_location.barony = title:b_jerusalem', text)
        service = block(text, 'kehillah_temple_service_available_trigger')
        self.assertIn('has_variable = kehillah_temple_service_restored', service)
        self.assertIn('has_building_or_higher = dome_of_the_rock_01', service)
        self.assertIn('has_trait = kohen', service)

    def test_samaritans_start_with_service_and_others_need_an_institution(self):
        self.assertIn(TENETS[2], ROSTERS['samaritan'])
        self.assertNotIn('tenet_ritual_celebrations', ROSTERS['samaritan'])
        for key in TENETS[:2]:
            self.assertIn(key, KNOWN['rabbinic_faith'])
        # 2026-11-24: Temple Service starts unknown outside the Samaritans; it is
        # learned from the books that argue for it.
        for faith in ('rabbinic_faith', 'karaism', 'haymanot', 'malabarism', 'kabarism'):
            self.assertNotIn(TENETS[2], KNOWN[faith])
        self.assertIn(TENETS[2], KNOWN['samaritan'])
        self.assertNotIn(TENETS[1], ROSTERS['rabbinism'])
        temple = block(source('common/religion/tenet_types/kehillah_revival_tenets.txt'), TENETS[2])
        self.assertIn('can_pick_as_personal_tenet = { kehillah_temple_service_available_trigger = yes }', temple)
        upgrade = source('common/scripted_effects/kehillah_tenet_polish_effects.txt')
        # A save with the original Communal Identity core must first receive
        # Covenant Community, then match the old default requiring replacement.
        self.assertLess(upgrade.index('remove_rite_tenet = tenet_communal_identity'),
                        upgrade.index('remove_rite_tenet = tenet_ritual_celebrations'))
        self.assertIn('has_global_variable = kehillah_tenet_polish_20261115_study', upgrade)

    def test_sacrifice_reward_has_one_payment_cap_and_personal_increment(self):
        effect = block(source('common/scripted_effects/kehillah_revival_effects.txt'), 'kehillah_complete_sacrifice_intent_effect')
        self.assertEqual(effect.count('add_gold ='), 1)
        self.assertIn('gold >= minor_gold_value', effect)
        self.assertIn('kehillah_sacrifice_destination_trigger = yes', effect)
        self.assertIn('NOT = { var:kehillah_sacrifice_reward_year ?= current_year }', effect)
        self.assertIn('current_month = 4', effect)
        self.assertIn('has_personal_tenet = tenet_kehillah_temple_service', effect)
        self.assertIn('add_piety = 200', effect)
        self.assertIn('add_piety = 100', effect)
        self.assertIn('complete_activity_intent = yes', effect)

    def test_append_only_book_reform_and_handwritten_dispatch(self):
        self.assertEqual(tuple(TENET_INDEX[14:17]), TENETS)
        bridge = source('common/scripted_effects/kehillah_reform_effects.txt')
        for i, key in enumerate(TENETS, 15):
            self.assertIn(f'var:kehillah_reform_pending_tenet ?= {i}', bridge)
            self.assertIn(f'value = tenet:{key}', bridge)
        for file in ('common/scripted_effects/kehillah_minds_effects.txt', 'common/scripted_triggers/kehillah_minds_triggers.txt',
                     'common/scripted_effects/kehillah_sefer_effects.txt', 'events/kehillah_sefer_events.txt'):
            text = source(file)
            for key in TENETS:
                self.assertIn(key, text)
        reform = source('common/scripted_triggers/kehillah_reform_triggers.txt')
        self.assertIn('kehillah_temple_service_available_trigger = yes', reform)
        self.assertIn('has_character_flag = kehillah_prophetic_calling', reform)
        self.assertIn('kehillah_reform_choice_valid_trigger = yes', bridge)

    def test_mission_pledge_and_reckoning_are_not_passive_piety(self):
        events = source('events/kehillah_revival_events.txt')
        pledge = block(events, 'kehillah_revival.0002')
        self.assertIn('value = scope:kehillah_messianic_pledge multiply = -1', pledge)
        self.assertIn('add_gold = scope:kehillah_messianic_pledge', pledge)
        self.assertIn('kehillah_messianic_mission_active', pledge)
        reckoning = block(events, 'kehillah_revival.0005')
        self.assertIn('kehillah_messianic_promised_faith', reckoning)
        self.assertIn('kehillah_messianic_disillusion_modifier', reckoning)
        self.assertIn('remove_variable = kehillah_messianic_patron', reckoning)
        cb = source('common/casus_belli_types/kehillah_sacred_homeland.txt')
        self.assertIn('has_character_flag = kehillah_messianic_mission_active', cb)
        self.assertIn('scope:target = title:c_jerusalem', cb)

    def test_prophetic_admonition_preserves_target_choice_and_revival_lock(self):
        text = source('common/character_interactions/kehillah_revival_interactions.txt')
        self.assertIn('has_trait = arbitrary has_trait = callous has_trait = deceitful', text)
        self.assertIn('scope:recipient = { trigger_event = kehillah_revival.0021 }', text)
        event = block(source('events/kehillah_revival_events.txt'), 'kehillah_revival.0021')
        self.assertIn('kehillah_revival.0021.heed', event)
        self.assertIn('kehillah_revival.0021.reject', event)
        self.assertIn('kehillah_prophetic_revival_recognized', event)
        self.assertNotIn('imprison', event)
        gate = block(source('common/scripted_triggers/kehillah_revival_triggers.txt'), 'kehillah_revival_adoption_allowed_trigger')
        self.assertIn('kehillah_prophetic_calling', gate)
        self.assertIn('kehillah_temple_service_available_trigger', gate)


if __name__ == '__main__':
    unittest.main()
