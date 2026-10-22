import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

from sync import ROOT, digest_tree


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def build(root=ROOT):
    upstream = root / "upstream" / "pstack"
    lock = json.loads((root / "upstream-lock.json").read_text())
    if digest_tree(upstream) != lock["sha256"]:
        raise ValueError("Upstream mirror differs from recorded snapshot")
    policy = json.loads((root / "adapter" / "policy.json").read_text())
    stage = root / "build" / "stage"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    for directory in ("skills", "docs", "assets", "agents", "automations"):
        if (upstream / directory).exists():
            destination = stage / directory if directory not in ("agents", "automations") else stage / "reference" / directory
            shutil.copytree(upstream / directory, destination)
    shutil.copy2(upstream / "README.md", stage / "README.md")
    for skill, reason in policy["excludedSkills"].items():
        candidate = stage / "skills" / skill
        if not candidate.is_dir() or candidate.parent != stage / "skills":
            raise ValueError(f"Stale or invalid exclusion: {skill}")
        if not reason.strip():
            raise ValueError(f"Missing exclusion reason: {skill}")
        shutil.rmtree(candidate)
    for directory in ("rules", "agents"):
        shutil.copytree(root / "adapter" / directory, stage / directory)
    rule = (root / "adapter" / "rules" / "qoder.md").read_text(encoding="utf-8")
    rule_body = rule.split("---", 2)[-1].strip() if rule.startswith("---\n") else rule
    for skill in (stage / "skills").glob("*/SKILL.md"):
        raw = skill.read_bytes()
        if not raw.startswith(b"---\n") or b"\n---\n" not in raw[4:]:
            raise ValueError(f"Unsupported skill frontmatter: {skill}")
        end = raw.index(b"\n---\n", 4) + len(b"\n---\n")
        header = b"\n<!-- pstack-qoder adapter: generated -->\n" + rule_body.encode("utf-8") + b"\n<!-- upstream skill body follows -->\n"
        skill.write_bytes(raw[:end] + header + raw[end:])
    for agent in (stage / "agents").glob("*.md"):
        text = agent.read_text(encoding="utf-8")
        agent.write_text(text.replace("{{QODER_ADAPTER}}", rule_body), encoding="utf-8", newline="\n")
    shutil.copy2(upstream / "LICENSE", stage / "LICENSE")
    (stage / "bin").mkdir()
    shutil.copy2(root / "scripts" / "setup.py", stage / "bin" / "setup.py")
    if (root / "README.md").exists():
        shutil.copy2(root / "README.md", stage / "QODER-README.md")
    manifest = {
        "name": "pstack-qoder",
        "version": lock["version"],
        "displayName": "pstack for Qoder",
        "description": "pstack engineering workflows adapted for Qoder; configure role models with setup-pstack.",
        "author": {"name": "pstack Qoder contributors"},
        "homepage": "https://github.com/cursor/plugins/tree/main/pstack",
        "license": "MIT",
        "skills": "./skills",
        "agents": ["./agents/pstack-implement.md", "./agents/pstack-judge.md"],
    }
    write_json(stage / ".qoder-plugin" / "plugin.json", manifest)
    write_json(stage / "compatibility.json", policy)
    write_json(stage / "upstream-lock.json", lock)
    fingerprint = digest_tree(stage)
    release_id = f"v{lock['version']}+{fingerprint[:12]}"
    write_json(stage / "provenance.json", {
        "upstream": lock,
        "payloadSha256": fingerprint,
        "release": release_id,
    })
    destination = root / "plugin"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(stage, destination)
    dist = root / "dist"
    dist.mkdir(exist_ok=True)
    archive = dist / f"pstack-qoder-{release_id[1:]}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as output:
        for path in sorted(destination.rglob("*"), key=lambda path: path.relative_to(destination).as_posix()):
            if path.is_file():
                info = zipfile.ZipInfo(path.relative_to(destination).as_posix(), (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                output.writestr(info, path.read_bytes())
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (dist / "SHA256SUMS").write_text(f"{checksum}  {archive.name}\n", encoding="utf-8", newline="\n")
    notes = f"pstack for Qoder {release_id}\n\nUpstream commit: {lock['commit']}\nUpstream version: {lock['version']}\nPayload SHA-256: {fingerprint}\n\nDownload the ZIP asset, not GitHub's Source code ZIP. Model assignments are stored in user settings and are not included.\n"
    (dist / "release-notes.txt").write_text(notes, encoding="utf-8")
    write_json(dist / "release.json", {"tag": release_id, "archive": archive.name, "sha256": checksum})
    return archive


if __name__ == "__main__":
    argparse.ArgumentParser().parse_args()
    print(build())
