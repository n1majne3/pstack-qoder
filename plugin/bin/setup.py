import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile

ROLES = ("pstack-qoder:pstack-implement", "pstack-qoder:pstack-judge")
EFFORT_BUDGETS = {"none": 0, "low": 1024, "medium": 8192, "high": 24576, "xhigh": 49152, "max": 65536}


def read_settings(path):
    raw = path.read_bytes() if path.exists() else b"{}"
    return json.loads(raw.decode("utf-8-sig")), hashlib.sha256(raw).hexdigest()


def catalog(settings):
    result = []
    for provider_id, provider in settings.get("providers", {}).items():
        for item in provider.get("models", []):
            model = item.get("model")
            if not isinstance(model, str) or not model:
                continue
            thinking = item.get("capabilities", {}).get("thinking", {})
            result.append({
                "id": f"{provider_id}/{model}",
                "provider": provider_id,
                "label": item.get("displayName", model),
                "efforts": thinking.get("supportedEffortLevels", []),
            })
    return result


def current_assignments(settings):
    overrides = settings.get("agents", {}).get("overrides", {})
    return {role: overrides.get(role, {}).get("modelConfig", {}) for role in ROLES}


def plan(settings, selections):
    known = {item["id"]: item for item in catalog(settings)}
    planned = {}
    for role in ROLES:
        selected = selections[role]
        model, effort = selected["model"], selected.get("effort")
        if model != "inherit" and model not in known:
            raise ValueError(f"Model is not in the configured provider catalog: {model}")
        if effort and (effort not in EFFORT_BUDGETS or model == "inherit" or effort not in known[model]["efforts"]):
            raise ValueError(f"Effort is not advertised by the selected model: {role}")
        planned[role] = {"model": model, "effort": effort}
    return planned


def confirmation_digest(settings_digest, planned):
    payload = json.dumps({"settings": settings_digest, "proposed": planned}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def preview(path, selections):
    settings, digest = read_settings(path)
    planned = plan(settings, selections)
    return {"current": current_assignments(settings), "proposed": planned, "confirmationDigest": confirmation_digest(digest, planned)}


def apply(path, selections, expected_digest):
    settings, observed = read_settings(path)
    planned = plan(settings, selections)
    if confirmation_digest(observed, planned) != expected_digest:
        raise ValueError("Settings or selections changed since preview; generate a new preview before confirming")
    overrides = settings.setdefault("agents", {}).setdefault("overrides", {})
    for role, selected in planned.items():
        config = overrides.setdefault(role, {}).setdefault("modelConfig", {})
        config["model"] = selected["model"]
        content = config.setdefault("generateContentConfig", {})
        thinking = content.setdefault("thinkingConfig", {})
        if selected["effort"]:
            thinking["thinkingBudget"] = EFFORT_BUDGETS[selected["effort"]]
        else:
            thinking.pop("thinkingBudget", None)
        if not thinking:
            content.pop("thinkingConfig", None)
        if not content:
            config.pop("generateContentConfig", None)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".pstack-setup-", dir=path.parent)
    try:
        os.chmod(temporary, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as output:
            json.dump(settings, output, indent=2, ensure_ascii=False)
            output.write("\n")
        if read_settings(path)[1] != observed:
            raise ValueError("Settings changed while saving; no configuration was replaced")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return planned


def main():
    parser = argparse.ArgumentParser(description="Preview or confirm Qoder role-model overrides; never prints provider credentials")
    parser.add_argument("action", choices=("models", "preview", "apply"))
    parser.add_argument("--settings", type=Path, default=Path.home() / ".qoder" / "settings.json")
    parser.add_argument("--implement-model")
    parser.add_argument("--implement-effort")
    parser.add_argument("--judge-model")
    parser.add_argument("--judge-effort")
    parser.add_argument("--confirm-digest")
    args = parser.parse_args()
    settings, digest = read_settings(args.settings)
    if args.action == "models":
        result = {"models": catalog(settings), "current": current_assignments(settings), "settingsDigest": digest}
    else:
        if not args.implement_model or not args.judge_model:
            parser.error("Select both role models")
        selections = {
            ROLES[0]: {"model": args.implement_model, "effort": args.implement_effort},
            ROLES[1]: {"model": args.judge_model, "effort": args.judge_effort},
        }
        planned = plan(settings, selections)
        if args.action == "preview":
            result = preview(args.settings, selections)
        else:
            if not args.confirm_digest:
                parser.error("Use the digest from the confirmed preview")
            result = {"saved": apply(args.settings, selections, args.confirm_digest), "reloadRequired": True}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
