"""Build the small synod agenda, preserving unrelated events and closing fixes.

Doctrine pairs are deliberate policy boundaries, not a tenet catalogue.
Rerunnable; see docs/spec/2026-11-26-synod-consolidation.md.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# group, first doctrine, alternative, controversy of moving to each
PRACTICE = [
    ('marriage', 'doctrine_monogamy', 'doctrine_polygamy', 10, 35),
    ('conversion', 'kehillah_proselytism_discouraged', 'kehillah_proselytism_encouraged', 5, 20),
    ('clergy', 'doctrine_clerical_gender_male_only', 'doctrine_clerical_gender_either', 15, 35),
]


def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')


def write(path, body):
    body = re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', body.replace('\r\n', '\n'))
    (ROOT / path).write_bytes(('\ufeff' + body.replace('\n', '\r\n')).encode('utf-8'))


def replace_block(text, key, body):
    pattern = r'(?ms)^' + re.escape(key) + r' = \{.*?^\}'
    replacement = key + ' = {\n' + body.strip('\n') + '\n}'
    if re.search(pattern, text):
        return re.sub(pattern, lambda _: replacement, text, count=1)
    return text.rstrip() + '\n\n' + replacement + '\n'


def build():
    path = 'events/kehillah_synod_events.txt'
    text = read(path)
    text = replace_block(text, 'kehillah_synod.0100', r'''
    type = character_event
    title = kehillah_synod.0100.t
    desc = kehillah_synod.0100.desc
    theme = faith
    left_portrait = { character = root animation = thinking }
    trigger = { exists = involved_activity }
    option = {
        name = kehillah_synod_option_tenet_reform
        trigger = { kehillah_reform_any_motion_trigger = yes }
        custom_tooltip = kehillah_synod_option_tenet_reform_desc
        hidden_effect = { kehillah_reform_clear_choice_effect = yes }
        trigger_event = kehillah_reform.0001
        ai_chance = { base = 40 modifier = { add = 100 rite ?= { has_variable = kehillah_reform_pending_tenet } } }
    }
    option = {
        name = kehillah_synod_kind_law
        trigger = { kehillah_synod_has_law_motion_trigger = yes }
        custom_tooltip = kehillah_synod_practice_category_tt
        trigger_event = kehillah_synod.0109
        ai_chance = { base = 5 }
    }
    option = {
        name = kehillah_synod_authority
        trigger = { OR = { kehillah_synod_can_propose_head_trigger = yes kehillah_synod_can_propose_herem_person_trigger = yes } }
        custom_tooltip = kehillah_synod_authority_tt
        trigger_event = kehillah_synod.0110
        ai_chance = { base = 50 }
    }
    option = {
        name = kehillah_synod_kind_none
        custom_tooltip = kehillah_synod_kind_none_tt
        ai_chance = { base = 0 modifier = { add = 100 NOT = { kehillah_reform_any_motion_trigger = yes } NOT = { kehillah_synod_has_law_motion_trigger = yes } NOT = { kehillah_synod_can_propose_head_trigger = yes } NOT = { kehillah_synod_can_propose_herem_person_trigger = yes } } }
    }
''')
    # Retain old IDs as safe exits for event windows queued before the rework.
    for number in (105, 106, 107):
        text = replace_block(text, f'kehillah_synod.{number:04}', r'''
    type = character_event
    hidden = yes
    immediate = { trigger_event = kehillah_synod.0100 }
''')
    text = replace_block(text, 'kehillah_synod.0110', r'''
    type = character_event
    title = kehillah_synod.0110.t
    desc = kehillah_synod.0110.desc
    theme = learning
    trigger = { exists = involved_activity }
    immediate = {
        ordered_in_global_list = {
            variable = kehillah_cherem_tracked
            limit = { kehillah_synod_herem_target_trigger = { HOST = root } }
            order_by = "has_trait_xp(kehillah_cherem_trait)"
            position = 0
            check_range_bounds = no
            save_scope_as = kehillah_synod_herem_target
        }
    }
    option = {
        name = kehillah_synod_kind_headship
        trigger = { kehillah_synod_can_propose_head_trigger = yes }
        custom_tooltip = kehillah_synod_headship_choice_tt
        trigger_event = kehillah_synod.0108
        ai_chance = { base = 50 }
    }
    option = {
        name = kehillah_synod_sanction_named
        trigger = { exists = scope:kehillah_synod_herem_target kehillah_synod_can_propose_herem_person_trigger = yes }
        custom_tooltip = kehillah_synod_sanction_tt
        hidden_effect = { involved_activity = { set_variable = { name = kehillah_synod_herem_target value = scope:kehillah_synod_herem_target } } }
        kehillah_synod_put_motion_effect = { MOTION = flag:herem_person }
        ai_chance = { base = 30 modifier = { add = 30 has_trait = zealous } }
    }
    option = { name = kehillah_synod_kind_back trigger_event = kehillah_synod.0100 ai_chance = { base = 0 } }
''')
    body = r'''
    type = character_event
    title = kehillah_synod.0108.t
    desc = kehillah_synod.0108.desc
    theme = learning
    trigger = { exists = involved_activity }
    immediate = {
        remove_variable = kehillah_synod_candidate_1
        remove_variable = kehillah_synod_candidate_2
        remove_variable = kehillah_synod_candidate_3
        involved_activity = {
            ordered_attending_character = {
                limit = { kehillah_synod_head_candidate_trigger = { HOST = root } }
                order_by = { value = 0 primary_title = { add = kehillah_head_of_rite_title_score_value } }
                max = 3
                check_range_bounds = no
                if = { limit = { NOT = { exists = root.var:kehillah_synod_candidate_1 } } root = { set_variable = { name = kehillah_synod_candidate_1 value = prev } } }
                else_if = { limit = { NOT = { exists = root.var:kehillah_synod_candidate_2 } } root = { set_variable = { name = kehillah_synod_candidate_2 value = prev } } }
                else = { root = { set_variable = { name = kehillah_synod_candidate_3 value = prev } } }
            }
        }
        var:kehillah_synod_candidate_1 ?= { save_scope_as = kehillah_synod_candidate_1 }
        var:kehillah_synod_candidate_2 ?= { save_scope_as = kehillah_synod_candidate_2 }
        var:kehillah_synod_candidate_3 ?= { save_scope_as = kehillah_synod_candidate_3 }
    }
'''
    for i in range(1, 4):
        body += f'''
    option = {{
        name = kehillah_synod_nominate_{i}
        trigger = {{ exists = var:kehillah_synod_candidate_{i} kehillah_synod_rite_headship_open_trigger = yes }}
        custom_tooltip = kehillah_synod_nominate_tt
        involved_activity = {{ set_variable = {{ name = kehillah_synod_nominee value = root.var:kehillah_synod_candidate_{i} }} }}
        kehillah_synod_put_motion_effect = {{ MOTION = flag:head_of_rite }}
        ai_chance = {{ base = {50 if i == 1 else 10} }}
    }}
'''
    body += '    option = { name = kehillah_synod_kind_back trigger_event = kehillah_synod.0110 ai_chance = { base = 0 } }\n'
    text = replace_block(text, 'kehillah_synod.0108', body)
    body = r'''
    type = character_event
    title = kehillah_synod.0109.t
    desc = kehillah_synod.0109.desc
    theme = faith
    trigger = { exists = involved_activity }
    immediate = {
'''
    for i, (_, first, second, cost_a, cost_b) in enumerate(PRACTICE, 1):
        body += f'''
        remove_variable = kehillah_synod_practice_{i}
        if = {{
            limit = {{ rite = {{ rite_has_doctrine = {first} rite_can_choose_doctrine = {second} }} }}
            set_variable = {{ name = kehillah_synod_practice_{i} value = doctrine:{second} }}
            set_variable = {{ name = kehillah_synod_practice_old_{i} value = doctrine:{first} }}
            kehillah_synod_score_doctrine_effect = {{ DOCTRINE = {second} STEP = {cost_b} VAR = kehillah_synod_practice_cost_{i} }}
        }}
        else_if = {{
            limit = {{ rite = {{ rite_has_doctrine = {second} rite_can_choose_doctrine = {first} }} }}
            set_variable = {{ name = kehillah_synod_practice_{i} value = doctrine:{first} }}
            set_variable = {{ name = kehillah_synod_practice_old_{i} value = doctrine:{second} }}
            kehillah_synod_score_doctrine_effect = {{ DOCTRINE = {first} STEP = {cost_a} VAR = kehillah_synod_practice_cost_{i} }}
        }}
        var:kehillah_synod_practice_{i} ?= {{ save_scope_as = kehillah_synod_practice_{i} }}
        var:kehillah_synod_practice_old_{i} ?= {{ save_scope_as = kehillah_synod_practice_old_{i} }}
'''
    body += '    }\n'
    for i in range(1, 4):
        body += f'''
    option = {{
        name = kehillah_synod_practice_option_{i}
        trigger = {{ exists = var:kehillah_synod_practice_{i} }}
        custom_tooltip = kehillah_synod_practice_option_{i}_tt
        kehillah_synod_controversy_tt_effect = {{ VAR = kehillah_synod_practice_cost_{i} }}
        hidden_effect = {{
            involved_activity = {{
                set_variable = {{ name = kehillah_synod_proposed_doctrine value = root.var:kehillah_synod_practice_{i} }}
                set_variable = {{ name = kehillah_synod_previous_doctrine value = root.var:kehillah_synod_practice_old_{i} }}
                set_variable = {{ name = kehillah_synod_proposal_rite value = root.rite }}
                set_variable = {{ name = kehillah_synod_controversy value = root.var:kehillah_synod_practice_cost_{i} }}
            }}
        }}
        kehillah_synod_put_motion_effect = {{ MOTION = flag:rite_doctrine }}
        ai_chance = {{ base = 2 }}
    }}
'''
    body += '    option = { name = kehillah_synod_kind_back trigger_event = kehillah_synod.0100 ai_chance = { base = 0 } }\n'
    text = replace_block(text, 'kehillah_synod.0109', body)
    # Saved objects make names work for both host and delegates, including after completion.
    load = '''
        involved_activity.var:kehillah_reform_topic ?= { save_scope_as = kehillah_reform_topic }
        involved_activity.var:kehillah_reform_replacement ?= { save_scope_as = kehillah_reform_replacement }
        involved_activity.var:kehillah_synod_previous_doctrine ?= { save_scope_as = kehillah_synod_previous_doctrine }
'''
    for number in (101, 102):
        pattern = r'(?ms)(^kehillah_synod\.' + str(number).zfill(4) + r' = \{.*?\n\s*immediate = \{)'
        # Remove only our previous generated payload loads before regenerating.
        section = re.search(r'(?ms)^kehillah_synod\.' + str(number).zfill(4) + r' = \{.*?^\}', text)[0]
        clean = re.sub(r'(?m)^        involved_activity(?:\.activity_host)?\.var:kehillah_reform_(?:topic|replacement) \?= .*\n', '', section)
        clean = re.sub(r'(?m)^        involved_activity\.var:kehillah_synod_previous_doctrine \?= .*\n', '', clean)
        clean = re.sub(r'(\n\s*immediate = \{)', lambda m: m[1] + load, clean, count=1)
        text = text.replace(section, clean, 1)
    # A carried vote which lapses during revalidation must not announce enactment.
    ruling = re.search(r'(?ms)^kehillah_synod\.0103 = \{.*?^\}', text)[0]
    ruling_new = ruling.replace('after = {\n\t\tif = {\n\t\t\tlimit = { scope:kehillah_synod_outcome = flag:passed }',
                               'after = {\n\t\tif = {\n\t\t\tlimit = { scope:kehillah_synod_outcome = flag:passed scope:kehillah_synod_applied ?= yes }')
    text = text.replace(ruling, ruling_new, 1)
    write(path, text)

    path = 'common/scripted_triggers/kehillah_synod_triggers.txt'
    text = read(path)
    text = replace_block(text, 'kehillah_synod_has_open_takkanah_trigger', r'''
    exists = primary_title
    OR = {
        kehillah_synod_can_propose_herem_person_trigger = yes
        kehillah_synod_rite_headship_open_trigger = yes
        AND = { kehillah_reform_any_motion_trigger = yes OR = { is_ai = no rite ?= { has_variable = kehillah_reform_pending_tenet } } }
        AND = { is_ai = no kehillah_synod_has_law_motion_trigger = yes }
    }
''')
    law = '    kehillah_synod_law_rite_trigger = yes\n    OR = {\n'
    for _, first, second, _, _ in PRACTICE:
        law += f'        rite = {{ OR = {{ AND = {{ rite_has_doctrine = {first} rite_can_choose_doctrine = {second} }} AND = {{ rite_has_doctrine = {second} rite_can_choose_doctrine = {first} }} }} }}\n'
    text = replace_block(text, 'kehillah_synod_has_law_motion_trigger', law + '    }')
    # Retired menus must not open a sitting through other old callers.
    for name in ('kehillah_synod_has_marriage_motion_trigger', 'kehillah_synod_has_communal_motion_trigger', 'kehillah_synod_has_undertaking_motion_trigger'):
        text = replace_block(text, name, '    always = no # Retired in the 2026-11-26 consolidation.')
    write(path, text)

    path = 'common/scripted_effects/kehillah_synod_effects.txt'
    text = read(path)
    # Award reform Greatness only after revalidation and actual enactment.
    text = text.replace('kehillah_reform_enact_effect = yes\n\t\tkehillah_change_pillar_effect = { PILLAR = greatness AMOUNT = kehillah_synod_passed_greatness }', 'kehillah_reform_enact_effect = yes')
    # Keep legacy enact branches to finish already-stored old motions.
    old_marker = '\t# 2026-11-25 law and custom: a doctrine'
    new_marker = '    # Practice proposals revalidate the exact rite'
    start = text.index(old_marker) if old_marker in text else text.index(new_marker)
    end = text.index('\t# 2026-11-25 dynamic agenda: the gathering names', start)
    text = text[:start] + r'''
    # Practice proposals revalidate the exact rite and its previous doctrine.
    else_if = {
        limit = { scope:kehillah_synod_takkanah = flag:rite_doctrine }
        if = {
            limit = {
                exists = scope:kehillah_synod_proposal_rite
                exists = scope:kehillah_synod_previous_doctrine
                rite = scope:kehillah_synod_proposal_rite
                rite = {
                    rite_has_doctrine = scope:kehillah_synod_previous_doctrine
                    NOT = { rite_has_doctrine = scope:kehillah_synod_proposed_doctrine }
                    rite_can_choose_doctrine = scope:kehillah_synod_proposed_doctrine
                }
            }
            rite = { change_rite_doctrine = scope:kehillah_synod_proposed_doctrine }
            save_scope_value_as = { name = kehillah_synod_applied value = yes }
            custom_tooltip = kehillah_synod_rite_doctrine_tt
            kehillah_change_pillar_effect = { PILLAR = greatness AMOUNT = kehillah_synod_passed_greatness }
            if = {
                limit = { exists = scope:kehillah_synod_controversy scope:kehillah_synod_controversy >= kehillah_synod_controversy_moderate }
                kehillah_change_pillar_effect = { PILLAR = stability AMOUNT = kehillah_synod_controversy_stability_value }
            }
        }
        else = { custom_tooltip = kehillah_reform_lapsed_tt }
    }
''' + text[end:]
    # Integrate with the concurrently-built completion snapshot, never restore the old involved_activity dependency.
    marker = 'kehillah_synod_prepare_closing_ruling_effect = {\n'
    load = '''\tsave_scope_value_as = { name = kehillah_synod_applied value = no }
\tscope:activity.var:kehillah_reform_topic ?= { save_scope_as = kehillah_reform_topic }
\tscope:activity.var:kehillah_reform_replacement ?= { save_scope_as = kehillah_reform_replacement }
\tif = {
\t\tlimit = { scope:activity.var:kehillah_synod_takkanah ?= flag:tenet_reform exists = scope:activity.var:kehillah_reform_topic }
\t\tset_variable = { name = kehillah_reform_topic value = scope:activity.var:kehillah_reform_topic }
\t\tset_variable = { name = kehillah_reform_rite value = scope:activity.var:kehillah_reform_rite }
\t\tset_variable = { name = kehillah_reform_action value = scope:activity.var:kehillah_reform_action }
\t\tremove_variable = kehillah_reform_replacement
\t\tif = { limit = { exists = scope:activity.var:kehillah_reform_replacement } set_variable = { name = kehillah_reform_replacement value = scope:activity.var:kehillah_reform_replacement } }
\t}
\tscope:activity.var:kehillah_synod_proposal_rite ?= { save_scope_as = kehillah_synod_proposal_rite }
\tscope:activity.var:kehillah_synod_previous_doctrine ?= { save_scope_as = kehillah_synod_previous_doctrine }
'''
    old_load = '''\tvar:kehillah_reform_topic ?= { save_scope_as = kehillah_reform_topic }
\tvar:kehillah_reform_replacement ?= { save_scope_as = kehillah_reform_replacement }
\tscope:activity.var:kehillah_synod_proposal_rite ?= { save_scope_as = kehillah_synod_proposal_rite }
\tscope:activity.var:kehillah_synod_previous_doctrine ?= { save_scope_as = kehillah_synod_previous_doctrine }
'''
    if marker in text:
        text = re.sub(re.escape(marker) + r'.*?(?=\tsave_scope_value_as = \{\n\t\tname = kehillah_synod_takkanah)', lambda _: marker + load, text, count=1, flags=re.S)
    text = text.replace('custom_tooltip = kehillah_synod_head_named_tt\n\t\t\t\thidden_effect',
                        'custom_tooltip = kehillah_synod_head_named_tt\n\t\t\t\tsave_scope_value_as = { name = kehillah_synod_applied value = yes }\n\t\t\t\thidden_effect')
    # Sanctions recheck the named leader instead of applying a stale selection.
    sanction_old = '\t# 2026-11-11 cherem track: the synod places'
    sanction_start = text.index(sanction_old) if sanction_old in text else text.index('    # A personal sanction is revalidated')
    sanction_end = text.index('\telse_if = {\n\t\tlimit = { scope:kehillah_synod_takkanah = flag:ketubbah_clause }', sanction_start)
    text = text[:sanction_start] + r'''
    # A personal sanction is revalidated when acknowledged.
    else_if = {
        limit = { scope:kehillah_synod_takkanah = flag:herem_person }
        if = {
            limit = { scope:kehillah_synod_herem_target ?= { is_alive = yes kehillah_synod_herem_target_trigger = { HOST = root } } }
            save_scope_value_as = { name = kehillah_synod_applied value = yes }
            scope:kehillah_synod_herem_target = {
                custom_tooltip = kehillah_synod_herem_person_tt
                hidden_effect = {
                    save_scope_value_as = { name = kehillah_cherem_pronounced_by value = flag:synod }
                    kehillah_cherem_pronounce_effect = yes
                }
            }
            kehillah_change_pillar_effect = { PILLAR = greatness AMOUNT = kehillah_synod_passed_greatness }
        }
        else = { custom_tooltip = kehillah_reform_lapsed_tt }
    }
''' + text[sanction_end:]
    text = text.replace('limit = { scope:kehillah_synod_level ?= flag:sanhedrin }\n\t\tkehillah_change_pillar_effect = { PILLAR = greatness AMOUNT = kehillah_sanhedrin_passed_greatness }',
                        'limit = { scope:kehillah_synod_level ?= flag:sanhedrin scope:kehillah_synod_applied ?= yes }\n\t\tkehillah_change_pillar_effect = { PILLAR = greatness AMOUNT = kehillah_sanhedrin_passed_greatness }')
    write(path, text)

    loc = {
        'kehillah_synod.0100.t': 'The Synod’s Proposal',
        'kehillah_synod.0100.desc': 'The ordinary cases are concluded. The delegates may now vote on one proposal: a tenet, a change to our rite’s practice, or the exercise of communal authority.\\n\\nChoose a matter with a concrete consequence. You may also close the sitting without a proposal.',
        'kehillah_synod_kind_law': 'Rite practice',
        'kehillah_synod_practice_category_tt': 'Change a doctrine of your rite: marriage, conversion policy, or clergy eligibility. Only alternatives allowed by the game are offered.',
        'kehillah_synod_authority': 'Leadership and discipline',
        'kehillah_synod_authority_tt': 'Nominate an eligible academy head, or put a named leader already in Niddui before the delegates for Herem.',
        'kehillah_synod.0110.t': 'Leadership and Discipline',
        'kehillah_synod.0110.desc': 'The gathering may recognise a head for a headless rite, or pronounce Herem on a leader already in Niddui. Only matters with an eligible candidate or target appear.',
        'kehillah_synod_sanction_named': 'Pronounce Herem on [kehillah_synod_herem_target.GetName].',
        'kehillah_synod_sanction_tt': 'If passed and still valid, applies the existing Herem system to this named leader. This is a personal sanction, not a new doctrine.',
        'kehillah_synod_headship_choice_tt': 'Choose among up to three eligible attending academy heads, ranked by the existing headship merit score.',
        'kehillah_synod.0108.t': 'Nominate a Head of Our Rite',
        'kehillah_synod.0108.desc': 'These attending academy heads qualify for the vacant headship. The delegates will vote on the person you nominate.\\n\\nThis uses the existing Gaonate office. A headship cannot be created here while that shared office is occupied.',
        'kehillah_synod_nominate_tt': 'If the vote passes and the nominee still qualifies, grants the existing head-of-rite office. No new succession law is created.',
        'kehillah_synod.0109.t': 'Change Our Rite’s Practice',
        'kehillah_synod.0109.desc': 'Each proposal replaces a doctrine of our rite. Hover the doctrine names to read their game effects. The ruling affects this rite, including at a Sanhedrin.\\n\\nThe proposals below cover marriage, conversion policy, and clergy eligibility. Received custom already in force does not need to be renewed.',
        'kehillah_synod_kind_none': 'Conclude without a proposal.',
        'kehillah_synod_kind_none_tt': 'No proposal is put to a vote and no proposal prestige is spent.',
        'kehillah_synod_kind_back': 'Return to the agenda.',
        'kehillah_synod_motion_rite_doctrine': 'The proposal is to replace [kehillah_synod_previous_doctrine.GetName( GetPlayer.GetFaith )] with [kehillah_synod_proposed_doctrine.GetName( GetPlayer.GetFaith )] in the host’s rite.',
        'kehillah_synod_rite_doctrine_tt': 'This rite adopts [kehillah_synod_proposed_doctrine.GetName( GetPlayer.GetFaith )].',
        'kehillah_synod_requires_open_takkanah_tt': 'A valid tenet, rite-practice, headship, or personal-sanction proposal is available.',
    }
    for i in range(1, 4):
        loc[f'kehillah_synod_nominate_{i}'] = f'Nominate [kehillah_synod_candidate_{i}.GetName].'
        loc[f'kehillah_synod_practice_option_{i}'] = f'[kehillah_synod_practice_{i}.GetGroup.GetName( ROOT.Char.GetFaith )]: [kehillah_synod_practice_{i}.GetName( ROOT.Char.GetFaith )]'
        loc[f'kehillah_synod_practice_option_{i}_tt'] = f'Current: [kehillah_synod_practice_old_{i}.GetName( ROOT.Char.GetFaith )]\\nProposed: [kehillah_synod_practice_{i}.GetName( ROOT.Char.GetFaith )]\\nApplies to your rite. The doctrine tooltip describes its game effects.'
    path = 'localization/english/kehillah_synod_l_english.yml'
    text = read(path)
    for key, value in loc.items():
        line = f' {key}:0 "{value}"'
        pattern = r'(?m)^ ' + re.escape(key) + r':.*$'
        if re.search(pattern, text):
            text = re.sub(pattern, lambda _: line, text)
        else:
            text += line + '\n'
    write(path, text)
    # Keep the closing result and vote receipts intact on every agenda rebuild.
    from kehillah_synod_vote_build import build as build_vote_feedback
    build_vote_feedback()


if __name__ == '__main__':
    build()
