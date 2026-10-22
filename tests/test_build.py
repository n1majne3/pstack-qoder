import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import build
from sync import digest_tree


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        upstream = self.root / "upstream" / "pstack"
        for name in ("keep", "cursor-only"):
            folder = upstream / "skills" / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_bytes(b"---\nname: example\n---\nOriginal upstream text\n")
        (upstream / "LICENSE").write_text("MIT fixture")
        (upstream / "README.md").write_text("Upstream help fixture")
        (upstream / "plugin.json").write_text('{"version": "1.2.3"}')
        for directory in ("rules", "agents"):
            folder = self.root / "adapter" / directory
            folder.mkdir(parents=True)
            (folder / "example.md").write_text("Adapter fixture")
        (self.root / "adapter" / "rules" / "qoder.md").write_text("Fixture rule")
        (self.root / "adapter" / "policy.json").write_text(json.dumps({"excludedSkills": {"cursor-only": "No Qoder equivalent"}}))
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "setup.py").write_text("pass\n")
        (self.root / "upstream-lock.json").write_text(json.dumps({"version": "1.2.3", "commit": "a" * 40, "sha256": digest_tree(upstream)}))

    def test_package_and_mirror(self):
        archive = build.build(self.root)
        original = self.root / "upstream" / "pstack" / "skills"
        self.assertTrue((original / "cursor-only" / "SKILL.md").exists())
        with zipfile.ZipFile(archive) as payload:
            names = payload.namelist()
            self.assertIn(".qoder-plugin/plugin.json", names)
            self.assertIn("skills/keep/SKILL.md", names)
            self.assertNotIn("skills/cursor-only/SKILL.md", names)
            emitted = payload.read("skills/keep/SKILL.md")
            self.assertIn(b"Fixture rule", emitted)
            self.assertTrue(emitted.endswith(b"Original upstream text\n"))
            self.assertEqual((original / "keep" / "SKILL.md").read_bytes(), b"---\nname: example\n---\nOriginal upstream text\n")
            self.assertFalse(any(name.startswith((".github/", "upstream/")) for name in names))

    def test_reproducible(self):
        archive = build.build(self.root)
        first = archive.read_bytes()
        self.assertEqual(build.build(self.root).read_bytes(), first)

    def test_sidecar_changes_release_identity(self):
        first = build.build(self.root)
        (self.root / "adapter" / "rules" / "example.md").write_text("Changed adapter")
        second = build.build(self.root)
        self.assertNotEqual(first.name, second.name)

    def test_mirror_edit_rejected(self):
        (self.root / "upstream" / "pstack" / "LICENSE").write_text("Edited")
        with self.assertRaisesRegex(ValueError, "mirror differs"):
            build.build(self.root)

    def test_full_validator_rejects_missing_nonrequired_skill(self):
        from validate import validate
        for name in ("pstack-implement", "pstack-judge"):
            (self.root / "adapter" / "agents" / f"{name}.md").write_text(f"---\nname: {name}\nmodel: inherit\n---\n")
        policy = self.root / "adapter" / "policy.json"
        value = json.loads(policy.read_text())
        value["requiredSkills"] = []
        policy.write_text(json.dumps(value))
        build.build(self.root)
        validate(self.root)
        shutil.rmtree(self.root / "plugin" / "skills" / "keep")
        with self.assertRaisesRegex(ValueError, "Incomplete skill payload"):
            validate(self.root)

    def test_stale_exclusion_rejected(self):
        (self.root / "adapter" / "policy.json").write_text('{"excludedSkills": {"missing": "reason"}}')
        with self.assertRaisesRegex(ValueError, "Stale"):
            build.build(self.root)


if __name__ == "__main__":
    unittest.main()
