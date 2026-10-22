# pstack for Qoder

An unofficial Qoder port of [pstack by Lauren Tan](https://github.com/cursor/plugins/tree/main/pstack), licensed MIT. The source snapshot is kept byte-for-byte; a deterministic build adds the Qoder execution contract and removes wholly unsupported skills.

## Install

Download the ZIP asset from this repository's Releases and import it through Qoder's plugin ZIP installation UI. Do not use GitHub's generated Source code ZIP: the installable manifest must be at the archive root.

For a local CLI installation:

```sh
qodercli plugins validate ./plugin
qodercli plugins install ./plugin
```

Restart the session or use `/plugins reload`. Invoke the plugin's `setup-pstack` skill from the slash-command picker, then `poteto-mode`. The exact displayed slash name depends on the client. The two registered agents are `pstack-qoder:pstack-implement` and `pstack-qoder:pstack-judge`.

A marketplace catalog is provided at `.qoder-plugin/marketplace.json`, with a root `marketplace.json` copy for clients that use that location. On a CLI supporting custom marketplace management, add this repository using the documented `plugins marketplace add` command. CLI 1.0.28 has no marketplace-management/update subcommands; use the local installation path or upgrade separately. This project never changes or upgrades your Qoder installation automatically.

## Model setup

Both agent definitions ship with `model: inherit`. Setup enumerates every configured provider's models, asks you to select the implementation/judgment models and their advertised effort, previews existing and proposed values, and saves only the corresponding model overrides in user-level Qoder settings. Provider IDs are resolved locally, not hardcoded in this repository. The helper does not expose API keys or endpoints.

The settings keys are qualified agent names. Effort is persisted through Qoder's actual `modelConfig.generateContentConfig.thinkingConfig.thinkingBudget` contract; supported labels map to the runtime's numeric budgets. Reload/start a new session before using the assignment. Override precedence and actual provider acceptance must be verified on the target client; static schema checks alone do not prove a model call used the assignment.

Manual helper workflow (normally driven by the setup skill):

```sh
python plugin/bin/setup.py models
python plugin/bin/setup.py preview --implement-model PROVIDER/MODEL --implement-effort high --judge-model PROVIDER/MODEL --judge-effort high
```

After approving the preview, repeat the selected arguments with `apply --confirm-digest DIGEST_FROM_PREVIEW`. The helper refuses changed settings, unknown models and unadvertised effort. It preserves unrelated settings and never writes credentials into the plugin. Models available only in a native account catalog, not the configured-provider catalog, currently require verified client-native configuration rather than invented identifiers.

## Compatibility

The current snapshot contains 57 skills. The package includes 56; `make-bot-ui` is excluded because Cursor routines, sender-key UI and wake webhooks are its essential workflow. Benny is not registered. Raw Cursor agents and automations are retained under `reference/` only to document the original package; the Qoder manifest explicitly loads only the two Qoder agents.

Mixed skills remain available. Cursor Bugbot controls, Custom Modes/shortcuts, `/loop` and cloud lifecycle steps are explicitly skipped, with evidence gaps disclosed. Ordinary repository work and meaningful independent reviews remain. A panel using the same selected model is not multi-model diversity.

Upstream scripts are bundled as reference and are never executed by sync, build, installation or setup. Some need Bun, Java/TLC, renderer packages or macOS-specific utilities; executing them is a separate, permission-governed task. Runtime checks that cannot run are not reported as passes.

**Why the adapter is compiled into skills:** the inspected CLI 1.0.28 and Desktop 0.4.8 worker do not load a plugin's `rules/` as automatic context, despite broader online plugin documentation listing rules. The build inserts the independent Qoder contract after each skill's frontmatter and in each role-agent prompt. Upstream files and bodies remain unchanged in `upstream/`. No extra adapter-file read or globally installed rule is necessary; the injected text still costs context tokens when a skill is loaded. An isolated CLI 1.0.28 installation discovered all 56 packaged skills and both qualified agents; user-level model overrides changed the displayed role models as expected. Desktop UI, real provider calls and end-to-end agent compliance with the embedded contract remain unverified.

Upstream help retains references to excluded functions and Cursor setup. The embedded Qoder contract governs execution and explicitly marks these references unavailable. The source Claude Code adapter is reference only, not Qoder guidance.

## Repository ownership

- `upstream/pstack/`: complete immutable snapshot of the upstream subtree, including docs, assets, agents and automations.
- `upstream-lock.json`: source commit/tree and canonical content fingerprint.
- `adapter/`: maintained Qoder contract, role-agent templates and exclusion policy; sync never touches it.
- `scripts/setup.py`: credential-safe local setup helper.
- `plugin/`: generated installable plugin, shared by ZIP and marketplace delivery; never edit it manually.
- `.github/workflows/sync-release.yml`: daily upstream sync, validation and content-addressed Release.

## Build and test

Python 3.12+ and Git are required; the tooling uses the standard library only.

```sh
python scripts/sync.py
python -m unittest discover -s tests -v
python scripts/build.py
python scripts/validate.py
```

To use an already-fetched upstream checkout: `python scripts/sync.py --source PATH`. Snapshot bytes come from Git objects, not Windows checkout line endings. A modified mirror is rejected rather than silently overwritten. ZIP entries have fixed timestamps, stable ordering and a SHA-256 checksum.

## Daily releases

The workflow runs daily at 03:23 UTC, on default-branch pushes and manually. Pull requests only test/build. Upstream code is copied as data, never run. A write-enabled job commits changed mirror/generated payload and publishes the ZIP and SHA256SUMS in the same workflow, so GITHUB_TOKEN push-trigger suppression does not break publication.

The manifest version follows upstream. Tags are `v<upstream-version>+<payload-hash>`, so adapter-only changes get their own release and retries produce the same identity. A repeated manifest version may not be detected by clients that compare only semantic versions; use the release identity/checksum and manual reinstallation if needed. `+...` build metadata does not increase SemVer precedence. Installed ZIPs do not self-update.

Publication requires the repository's Actions token to have contents-write permission. No personal access token or provider secret is needed. Forks should review automatic upstream publishing before enabling the scheduled workflow.

## Attribution

Original skills and supporting material: Lauren Tan and the cursor/plugins contributors, MIT. Qoder adaptation: this repository's contributors. This is not an official Cursor or Qoder plugin.
