import json
from pathlib import Path
import re
import zipfile

from sync import ROOT, digest_tree


def validate(root=ROOT):
    plugin = root / "plugin"
    manifest = json.loads((plugin / ".qoder-plugin" / "plugin.json").read_text())
    if manifest["name"] != "pstack-qoder" or not re.fullmatch(r"\d+\.\d+\.\d+(?:-[\w.]+)?(?:\+[\w.]+)?", manifest["version"]):
        raise ValueError("Invalid plugin identity")
    for resource in (manifest["skills"], *manifest["agents"]):
        if not resource.startswith("./") or ".." in Path(resource).parts or not (plugin / resource).exists():
            raise ValueError(f"Missing or invalid manifest resource: {resource}")
    policy = json.loads((root / "adapter" / "policy.json").read_text())
    for name in policy["excludedSkills"]:
        if (plugin / "skills" / name).exists():
            raise ValueError(f"Excluded skill remains: {name}")
    for name in policy["requiredSkills"]:
        if not (plugin / "skills" / name / "SKILL.md").exists():
            raise ValueError(f"Required skill missing: {name}")
    mirror = root / "upstream" / "pstack"
    expected_files = {path.relative_to(mirror / "skills").as_posix() for path in (mirror / "skills").rglob("*") if path.is_file() and path.relative_to(mirror / "skills").parts[0] not in policy["excludedSkills"]}
    actual_files = {path.relative_to(plugin / "skills").as_posix() for path in (plugin / "skills").rglob("*") if path.is_file()}
    if actual_files != expected_files:
        raise ValueError(f"Incomplete skill payload: missing={sorted(expected_files - actual_files)}, extra={sorted(actual_files - expected_files)}")
    for path in (plugin / "skills").rglob("*"):
        if path.is_file():
            data = path.read_bytes()
            if path.name == "SKILL.md" and path.parent.parent == plugin / "skills":
                start = data.index(b"\n<!-- pstack-qoder adapter: generated -->\n")
                end_marker = b"<!-- upstream skill body follows -->\n"
                end = data.index(end_marker, start) + len(end_marker)
                data = data[:start] + data[end:]
            if data != (mirror / "skills" / path.relative_to(plugin / "skills")).read_bytes():
                raise ValueError(f"Upstream body differs: {path}")
    for name in ("pstack-implement", "pstack-judge"):
        body = (plugin / "agents" / f"{name}.md").read_text()
        if "model: inherit" not in body or "name: " + name not in body:
            raise ValueError(f"Invalid role agent: {name}")
    provenance = json.loads((plugin / "provenance.json").read_text())
    if provenance["upstream"]["sha256"] != digest_tree(mirror):
        raise ValueError("Provenance mismatch")
    release = json.loads((root / "dist" / "release.json").read_text())
    with zipfile.ZipFile(root / "dist" / release["archive"]) as archive:
        if ".qoder-plugin/plugin.json" not in archive.namelist() or archive.testzip():
            raise ValueError("Invalid ZIP")
        files = {path.relative_to(plugin).as_posix(): path for path in plugin.rglob("*") if path.is_file()}
        if len(archive.namelist()) != len(files) or set(archive.namelist()) != set(files):
            raise ValueError("ZIP and marketplace payload file sets differ")
        for name in archive.namelist():
            if archive.read(name) != files[name].read_bytes():
                raise ValueError(f"ZIP payload differs: {name}")
            if name.startswith("/") or ".." in Path(name).parts:
                raise ValueError(f"Unsafe archive entry: {name}")
    print(f"Validated {len(list((plugin / 'skills').glob('*/SKILL.md')))} skills and ZIP structure")


if __name__ == "__main__":
    validate()
