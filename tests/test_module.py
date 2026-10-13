import unittest
import json
from pathlib import Path

from embervault_sdk import ModuleContext
from src.module import plan_setting_change


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


if __name__ == "__main__":
    unittest.main()
