import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sync import digest_tree, sync


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name)
        self.source = base / "source"
        self.source.mkdir()
        self.root = base / "destination"
        self.root.mkdir()
        self.git("init", "-q")
        pstack = self.source / "pstack"
        (pstack / "skills" / "example").mkdir(parents=True)
        (pstack / "skills" / "example" / "SKILL.md").write_text("Original\n")
        (pstack / "plugin.json").write_text('{"version":"1.2.3"}')
        self.commit()

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.source), *args], check=True, capture_output=True)

    def commit(self):
        self.git("add", "pstack")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")

    def test_sync_is_idempotent(self):
        self.assertTrue(sync(self.source, self.root))
        lock = (self.root / "upstream-lock.json").read_bytes()
        self.assertFalse(sync(self.source, self.root))
        self.assertEqual(lock, (self.root / "upstream-lock.json").read_bytes())
        canonical = subprocess.check_output(["git", "-C", str(self.source), "show", "HEAD:pstack/skills/example/SKILL.md"])
        self.assertEqual(canonical, (self.root / "upstream" / "pstack" / "skills" / "example" / "SKILL.md").read_bytes())

    def test_sidecar_preserved_and_upstream_deletion_mirrored(self):
        sync(self.source, self.root)
        sidecar = self.root / "adapter"
        sidecar.mkdir()
        (sidecar / "fixture").write_text("Owned adapter")
        (self.source / "pstack" / "skills" / "example" / "SKILL.md").unlink()
        self.commit()
        self.assertTrue(sync(self.source, self.root))
        self.assertFalse((self.root / "upstream" / "pstack" / "skills" / "example" / "SKILL.md").exists())
        self.assertEqual((sidecar / "fixture").read_text(), "Owned adapter")

    def test_manual_mirror_edits_rejected(self):
        sync(self.source, self.root)
        (self.root / "upstream" / "pstack" / "plugin.json").write_text("Modified")
        with self.assertRaisesRegex(ValueError, "Local upstream mirror changed"):
            sync(self.source, self.root)

    def test_digest_sorting_is_platform_independent(self):
        import hashlib
        folder = self.root / "hash-fixture"
        folder.mkdir()
        for name in ("a", "Z", "LICENSE", "zeta"):
            (folder / name).write_bytes(name.encode())
        expected = hashlib.sha256()
        for name in ("LICENSE", "Z", "a", "zeta"):
            expected.update(name.encode() + b"\0" + name.encode() + b"\0")
        self.assertEqual(digest_tree(folder), expected.hexdigest())

    def test_dirty_upstream_rejected(self):
        (self.source / "pstack" / "plugin.json").write_text("Modified")
        with self.assertRaisesRegex(ValueError, "local changes"):
            sync(self.source, self.root)


if __name__ == "__main__":
    unittest.main()
