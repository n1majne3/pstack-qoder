import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("pstack_setup", Path(__file__).resolve().parents[1] / "scripts" / "setup.py")
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.settings = {
            "providers": {"sample": {"apiKey": "fixture-secret", "baseUrl": "http://127.0.0.1", "models": [
                {"model": "auto/fast", "displayName": "Fast", "capabilities": {"thinking": {"supportedEffortLevels": ["high", "max"]}}},
                {"model": "auto/strong", "capabilities": {"thinking": {"supportedEffortLevels": ["low", "high"]}}},
            ]}},
            "agents": {"overrides": {"unrelated": {"enabled": False}, "pstack-qoder:pstack-judge": {"tools": ["Read"], "modelConfig": {"generateContentConfig": {"temperature": 0.2}}}}},
            "permissions": {"fixture": True},
        }
        self.selections = {
            "pstack-qoder:pstack-implement": {"model": "sample/auto/fast", "effort": "max"},
            "pstack-qoder:pstack-judge": {"model": "sample/auto/strong", "effort": "high"},
        }
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "settings.json"
        self.path.write_text(json.dumps(self.settings))

    def test_catalog_contains_no_credentials(self):
        catalog = setup.catalog(self.settings)
        self.assertEqual(catalog[0]["id"], "sample/auto/fast")
        self.assertNotIn("fixture-secret", json.dumps(catalog))
        self.assertNotIn("127.0.0.1", json.dumps(catalog))

    def test_apply_preserves_other_settings(self):
        digest = setup.preview(self.path, self.selections)["confirmationDigest"]
        setup.apply(self.path, self.selections, digest)
        saved, _ = setup.read_settings(self.path)
        self.assertEqual(saved["providers"], self.settings["providers"])
        self.assertEqual(saved["permissions"], self.settings["permissions"])
        self.assertEqual(saved["agents"]["overrides"]["unrelated"], {"enabled": False})
        judge = saved["agents"]["overrides"]["pstack-qoder:pstack-judge"]
        self.assertEqual(judge["tools"], ["Read"])
        self.assertEqual(judge["modelConfig"]["generateContentConfig"]["temperature"], 0.2)
        self.assertEqual(judge["modelConfig"]["model"], "sample/auto/strong")
        self.assertEqual(judge["modelConfig"]["generateContentConfig"]["thinkingConfig"]["thinkingBudget"], 24576)

    def test_changed_settings_rejected(self):
        digest = setup.preview(self.path, self.selections)["confirmationDigest"]
        changed = copy.deepcopy(self.settings)
        changed["permissions"]["other"] = True
        self.path.write_text(json.dumps(changed))
        before = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, "changed since preview"):
            setup.apply(self.path, self.selections, digest)
        self.assertEqual(self.path.read_bytes(), before)

    def test_confirmation_binds_selected_effort(self):
        digest = setup.preview(self.path, self.selections)["confirmationDigest"]
        self.selections["pstack-qoder:pstack-judge"]["effort"] = "low"
        with self.assertRaisesRegex(ValueError, "selections changed"):
            setup.apply(self.path, self.selections, digest)

    def test_bad_effort_rejected_without_write(self):
        original = self.path.read_bytes()
        self.selections["pstack-qoder:pstack-judge"]["effort"] = "xhigh"
        with self.assertRaisesRegex(ValueError, "not advertised"):
            setup.apply(self.path, self.selections, setup.preview(self.path, self.selections)["confirmationDigest"])
        self.assertEqual(original, self.path.read_bytes())

    def test_unknown_model_rejected(self):
        self.selections["pstack-qoder:pstack-judge"]["model"] = "not-a-provider/model"
        with self.assertRaisesRegex(ValueError, "not in"):
            setup.plan(self.settings, self.selections)

    def test_repeated_apply_is_idempotent(self):
        setup.apply(self.path, self.selections, setup.preview(self.path, self.selections)["confirmationDigest"])
        first = self.path.read_bytes()
        setup.apply(self.path, self.selections, setup.preview(self.path, self.selections)["confirmationDigest"])
        self.assertEqual(first, self.path.read_bytes())


if __name__ == "__main__":
    unittest.main()
