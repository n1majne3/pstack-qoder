import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import io

ROOT = Path(__file__).resolve().parents[1]
REMOTE = "https://github.com/cursor/plugins.git"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def digest_tree(root):
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda path: path.relative_to(root).as_posix()):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not accepted: {path}")
        if path.is_file():
            digest.update(path.relative_to(root).as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def sync(source, root=ROOT):
    if git(source, "status", "--porcelain", "--", "pstack"):
        raise ValueError("Upstream checkout has local changes")
    commit = git(source, "rev-parse", "HEAD")
    tree = git(source, "rev-parse", "HEAD:pstack")
    archive = subprocess.check_output(["git", "-c", "core.autocrlf=false", "-C", str(source), "archive", "HEAD", "pstack"])
    with tempfile.TemporaryDirectory(prefix="pstack-canonical-") as temporary:
        with tarfile.open(fileobj=io.BytesIO(archive)) as snapshot:
            if any(not item.isfile() and not item.isdir() for item in snapshot.getmembers()):
                raise ValueError("Upstream snapshot contains unsupported links or special files")
            snapshot.extractall(temporary, filter="data")
        return sync_snapshot(Path(temporary) / "pstack", commit, tree, root)


def sync_snapshot(incoming, commit, tree, root):
    fingerprint = digest_tree(incoming)
    lock_path = root / "upstream-lock.json"
    if lock_path.exists():
        previous = json.loads(lock_path.read_text())
        if previous["tree"] == tree:
            if digest_tree(root / "upstream" / "pstack") != previous["sha256"]:
                raise ValueError("Local upstream mirror changed; refusing to overwrite")
            if previous["sha256"] == fingerprint:
                return False
    destination = root / "upstream" / "pstack"
    if destination.exists():
        if not lock_path.exists():
            raise ValueError("Existing mirror has no ownership lock")
        previous = json.loads(lock_path.read_text())
        if digest_tree(destination) != previous["sha256"]:
            raise ValueError("Local upstream mirror changed; refusing to overwrite")
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(incoming, destination)
    lock_path.write_text(json.dumps({
        "repository": REMOTE,
        "commit": commit,
        "tree": tree,
        "sha256": fingerprint,
        "version": json.loads((incoming / "plugin.json").read_text())["version"],
    }, indent=2) + "\n", encoding="utf-8", newline="\n")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    if args.source:
        changed = sync(args.source.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix="pstack-upstream-") as temporary:
            repo = Path(temporary) / "plugins"
            subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", REMOTE, str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "sparse-checkout", "set", "pstack"], check=True)
            changed = sync(repo)
    print("Upstream mirror updated" if changed else "Upstream pstack unchanged")


if __name__ == "__main__":
    main()
