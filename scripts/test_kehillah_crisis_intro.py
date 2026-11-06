"""Source contracts for crisis entry ordering; runtime checks live in kehillah_crisis_intro_debug.

Run: python scripts/test_kehillah_crisis_intro.py
These tests do not claim to emulate CK3 or verify that its alert renders.
"""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
OPENINGS = [
    ("granada", "kehillah_granada.0018", 3),
    ("accusation", "kehillah_accusation.0001", 4),
    ("talmud_trial", "kehillah_talmud_trial.0001", 4),
    ("decree", "kehillah_decree.0001", 6),
    ("mob", "kehillah_mob.0004", 1),
    ("crisis_race", "kehillah_crisis_race.0300", 1),
    ("crisis_race", "kehillah_crisis_race.0310", 1),
    ("expulsion", "kehillah_expulsion.0001", 4),
]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def block(text, key):
    match = re.search(r"(?m)^\s*(?:scripted_effect\s+)?" + re.escape(key) + r"\s*=\s*\{", text)
    if not match:
        raise AssertionError(f"Missing block {key}")
    start = text.index("{", match.start())
    depth = 0
    quoted = comment = False
    for index in range(start, len(text)):
        char = text[index]
        if char == "\n":
            comment = False
        if comment:
            continue
        if char == '"' and text[index - 1] != "\\":
            quoted = not quoted
        if quoted:
            continue
        if char == "#":
            comment = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:index]
    raise AssertionError(f"Unclosed block {key}")


class CrisisIntroductionContracts(unittest.TestCase):
    def test_all_existing_openings_acknowledge_in_after_and_preserve_choices(self):
        for family, key, choices in OPENINGS:
            with self.subTest(event=key):
                event = block(source(f"events/kehillah_{family}_events.txt"), key)
                after = block(event, "after")
                self.assertIn("kehillah_crisis_acknowledge_effect", after)
                self.assertIn("has_variable = kehillah_crisis_intro_accepted", after)
                self.assertEqual(len(re.findall(r"(?m)^\s*option\s*=", event)), choices)
                options = event[:event.index("\n\tafter")]
                immediate = block(event, "immediate")
                self.assertIn("kehillah_crisis_start_with_popup_effect", immediate)
                options = options.replace(immediate, "")
                for forbidden in ("start_situation =", "start_war =", "kehillah_crisis_acknowledge_effect ="):
                    self.assertNotIn(forbidden, options)
                previews = re.findall(r"show_as_tooltip = \{ (kehillah_intro_\w+_response_effect) = yes", options)
                for effect in previews:
                    self.assertEqual(after.count(effect + " = yes"), 1)

    def test_granada_poem_reserves_before_it_starts(self):
        event = block(source("events/kehillah_granada_events.txt"), "kehillah_granada.0018")
        immediate = block(event, "immediate")
        self.assertLess(immediate.index("kehillah_crisis_reserve_intro_effect"), immediate.index("kehillah_crisis_start_with_popup_effect"))

    def test_host_popup_starts_and_keeps_its_rising_text_after_activation(self):
        event = block(source("events/kehillah_crisis_intro_events.txt"), "kehillah_crisis_intro.0001")
        immediate = block(event, "immediate")
        self.assertIn("kehillah_crisis_start_with_popup_effect = { FAMILY = retarget }", immediate)
        self.assertIn("kehillah_crisis_start_with_popup_effect = { FAMILY = host }", immediate)
        self.assertIn("var:kehillah_crisis_opening ?= flag:rising", event)

    def test_accusation_cannot_fire_twice_once_its_crisis_starts(self):
        begin = block(source("common/scripted_effects/kehillah_accusation_effects.txt"), "kehillah_accusation_begin_effect")
        self.assertIn("else_if = {", begin[:begin.index("trigger_event = kehillah_accusation.0001")])

    def test_no_event_still_promises_that_answering_starts_a_crisis(self):
        for path in (ROOT / "events").glob("*.txt"):
            self.assertNotIn("kehillah_crisis_acknowledge_tt", path.read_text(encoding="utf-8-sig"), path.name)

    def test_staging_does_not_create_active_situations_or_start_wars(self):
        for filename, key in [
            ("trial", "kehillah_trial_begin_effect"),
            ("decree", "kehillah_decree_begin_effect"),
            ("expulsion", "kehillah_expulsion_start_effect"),
            ("crusade", "kehillah_mob_preaching_mark_target_effect"),
            ("crusade", "kehillah_mob_retarget_effect"),
        ]:
            with self.subTest(effect=key):
                effect = block(source(f"common/scripted_effects/kehillah_{filename}_effects.txt"), key)
                self.assertNotIn("start_situation =", effect)
                self.assertNotIn("start_war =", effect)
                self.assertNotIn("kehillah_crisis_begin_effect =", effect)
                self.assertNotIn("send_interface_message =", effect)

    def test_pending_stories_and_reconciliation_cannot_advance(self):
        preach = block(source("common/scripted_effects/kehillah_crusade_effects.txt"), "kehillah_mob_preaching_tick_effect")
        self.assertLess(preach.index("flag:attack"), preach.index("change_variable ="))
        march = block(source("common/scripted_effects/kehillah_mob_effects.txt"), "kehillah_mob_tick_effect")
        self.assertIn("NOT = { var:kehillah_mob_target_title ?= { var:kehillah_crisis_intro_pending ?= flag:retarget } }", march)
        sync = block(source("common/scripted_effects/kehillah_crisis_situation_effects.txt"), "kehillah_crisis_situation_sync_inner_effect")
        self.assertLess(sync.index("NOT = { has_variable = kehillah_crisis_intro_pending }"), sync.index("start_situation"))
        expulsion = block(source("common/scripted_effects/kehillah_expulsion_effects.txt"), "kehillah_expulsion_quarterly_effect")
        self.assertLess(expulsion.index("NOT = { has_variable = kehillah_crisis_intro_pending }"), expulsion.index("name = kehillah_expulsion_quarters add"))

    def test_cast_and_terms_are_copied_without_rerolling(self):
        for family in ("trial", "decree"):
            text = source(f"common/scripted_effects/kehillah_{family}_effects.txt")
            rolled = block(text, f"kehillah_{family}_roll_effect")
            fields = set(re.findall(r"set_variable\s*=\s*\{\s*name\s*=\s*(kehillah_\w+)", rolled))
            activate = block(text, f"kehillah_{family}_activate_effect")
            self.assertNotIn(f"kehillah_{family}_roll_effect =", activate)
            for field in fields:
                self.assertIn(f".var:{field}", activate)

    def test_stale_events_require_same_title_family_epoch_county_and_host(self):
        ack = block(source("common/scripted_effects/kehillah_crisis_intro_effects.txt"), "kehillah_crisis_acknowledge_effect")
        for guard in (
            "primary_title ?= scope:kehillah_crisis_intro_title",
            "var:kehillah_crisis_intro_pending ?= flag:$FAMILY$",
            "var:kehillah_crisis_intro_epoch = scope:kehillah_crisis_intro_epoch",
            "domicile.domicile_location.county ?= primary_title.var:kehillah_crisis_intro_county",
            "domicile.domicile_location.county.holder.top_liege ?= primary_title.var:kehillah_crisis_intro_host",
        ):
            self.assertIn(guard, ack)
        reserve = block(source("common/scripted_effects/kehillah_crisis_intro_effects.txt"), "kehillah_crisis_reserve_intro_effect")
        self.assertIn("name = kehillah_crisis_intro_epoch add = 1", reserve)

    def test_granada_followups_are_scheduled_from_acknowledgment(self):
        schedule = block(source("common/scripted_effects/kehillah_granada_effects.txt"), "kehillah_granada_schedule_effect")
        self.assertNotIn("id = kehillah_granada.0002", schedule)
        self.assertNotIn("id = kehillah_granada.0003", schedule)
        ack = block(source("common/scripted_effects/kehillah_crisis_intro_effects.txt"), "kehillah_crisis_acknowledge_effect")
        self.assertIn("id = kehillah_granada.0002 days = 35", ack)
        self.assertIn("id = kehillah_granada.0003 days = 76", ack)

    def test_new_crisis_admission_reserves_all_families(self):
        gate = block(source("common/scripted_triggers/kehillah_crisis_intro_triggers.txt"), "kehillah_crisis_can_offer_intro_trigger")
        for name in ("kehillah_crisis_intro_pending", "kehillah_mob_threat", "kehillah_trial_situation", "kehillah_decree_situation", "kehillah_expulsion_quarters"):
            self.assertIn(name, gate)

    def test_fresh_opening_replaces_old_colour_without_changing_granada_epoch(self):
        marker = block(source("common/scripted_effects/kehillah_crusade_effects.txt"), "kehillah_mob_preaching_mark_target_effect")
        self.assertLess(marker.index("remove_variable = kehillah_crisis_opening"), marker.index("kehillah_crisis_set_opening_effect = yes"))
        self.assertIn("var:kehillah_crisis_intro_pending ?= flag:granada", marker)
        self.assertIn("name = kehillah_crisis_intro_pending value = flag:attack", marker)
        self.assertIn("trigger_event = kehillah_accusation.0001", marker)

    def test_sudden_hosts_and_retargets_keep_wars_out_of_staging(self):
        host = block(source("common/scripted_effects/kehillah_mob_effects.txt"), "kehillah_mob_raise_effect")
        self.assertIn("kehillah_crisis_can_offer_intro_trigger = yes", host)
        self.assertIn("FAMILY = host", host)
        self.assertIn("trigger_event = kehillah_crisis_intro.0001", host)
        self.assertNotIn("start_war =", host)
        retarget = block(source("common/scripted_effects/kehillah_crusade_effects.txt"), "kehillah_mob_retarget_acknowledged_effect")
        self.assertIn("start_war =", retarget)
        self.assertIn("name = kehillah_crisis_stage value = 2", retarget)

    def test_alert_is_persistent_and_opens_situation_only_after_intro(self):
        alert = block(source("common/important_actions/kehillah_crisis_actions.txt"), "action_kehillah_active_crisis")
        self.assertIn("type = alert", alert)
        self.assertIn("NOT = { has_variable = kehillah_crisis_intro_pending }", alert)
        self.assertIn("open_view_data = situation", alert)
        announce = block(source("common/scripted_effects/kehillah_crisis_effects.txt"), "kehillah_crisis_announce_once_effect")
        self.assertNotIn("kehillah_crisis_announce_effect = yes", announce)


if __name__ == "__main__":
    unittest.main(verbosity=2)
