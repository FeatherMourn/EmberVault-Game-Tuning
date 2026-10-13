import unittest
import json
from pathlib import Path

from embervault_sdk import ModuleContext
from src.module import compare_setting_plans, plan_setting_change


class GameTuningTests(unittest.TestCase):
    def test_manifest_matches_staged_only_boundary(self):
        manifest = json.loads((Path(__file__).parents[1] / "module.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["safety"]["read_only"])
    def test_setting_change_is_staged_only(self):
        result = plan_setting_change(ModuleContext("embervault.game-tuning", "research", "EV-OP-1"),
                                     "resource_yield_multiplier", 2.0, "research")
        self.assertEqual(result.status, "ready")
        self.assertEqual(result.data["application_state"], "staged-only")
        self.assertFalse(result.data["mutates_live_game"])

    def test_setting_change_rejects_wrong_profile(self):
        result = plan_setting_change(ModuleContext("embervault.game-tuning", "default", "EV-OP-2"),
                                     "resource_yield_multiplier", 2.0, "research")
        self.assertEqual(result.status, "blocked")

    def test_setting_plan_comparison_is_read_only_and_profile_scoped(self):
        result = compare_setting_plans([
            {"key": "z", "value": 2, "profile_id": "research", "application_state": "staged-only"},
            {"key": "a", "value": 1, "profile_id": "default", "application_state": "staged-only"},
        ], profile_id="research")
        self.assertEqual([item["key"] for item in result["changes"]], ["z"])
        self.assertTrue(result["read_only"])
        self.assertFalse(result["mutates_live_game"])


if __name__ == "__main__":
    unittest.main()
