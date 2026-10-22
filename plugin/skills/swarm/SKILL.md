---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
---

<!-- pstack-qoder adapter: generated -->
# pstack on Qoder

Scope: pstack skills, their playbooks and delegated work only. Apply this Qoder contract when their harness-specific instructions differ. Keep the upstream engineering workflow and the active host permission policy.

## Dispatch

Use the available Qoder tool schemas. Cursor `Task` means `Agent`; task tracking uses the available TaskCreate/TaskUpdate tools. Translate `generalPurpose` to `general-purpose`. Pass only declared parameters, with no per-call model override or invented Cursor agent type.

Route a requested `poteto-agent` by job: coding, refactoring, bugs, performance, hillclimb, exploration, investigation, reflect tooling and swarm workers use `pstack-qoder:pstack-implement`; judgment, prose, hardest tasks, explanation and synthesis use `pstack-qoder:pstack-judge`. Arena, architect and interrogate panels use one fresh instance of each role; preserve additional seat counts with independent instances. Unmapped roles use implement and disclose that choice. A same-model panel is independent review, not model diversity. Both role agents have normal host tools; honor each task's explicit read-only scope.

Pass the absolute installed `skills/poteto-mode/SKILL.md` path and task scope in every delegate brief. Ground each delegate in that file and applicable principle leaves. For `comment-sicko`, use judge with the no-comments rubric and the authorized editing scope; there is no separate Cursor agent to spawn. If a role agent is not discovered, stop that delegation and report the loading problem rather than silently using a different model.

Use supported background/worktree parameters only. A local worktree is not a cloud machine. When resume is unavailable, start a fresh agent with the earlier result. Flatten unsupported nested delegation into the parent while preserving independent checks. Discover MCP tools and schemas with the actual host tools, not a Cursor `mcps/` directory.

## Qoder setup replaces Cursor setup

For setup-pstack, use this complete setup sequence instead of the upstream model enumeration, slug rewriting and Cursor rule writes. The two installed agents stay `model: inherit`; assignments belong only to Qoder user settings. Setup chooses models at runtime; the public plugin contains no provider endpoint, credentials or chosen model IDs.

1. Resolve this plugin root from the loaded skill path. Run `python "<plugin-root>/bin/setup.py" models`. This exposes configured provider/model IDs, labels, advertised effort levels and existing role assignments, never provider credentials. Include all configured providers. If the host has a separate native model catalog, use its verified identifiers only; the helper currently validates configured-provider models plus inherit.
2. Ask the user to choose each role's model and a supported effort. Preserve the full provider-qualified identifier returned by the helper. With no advertised effort, leave effort unset. Use inherit explicitly if requested; never guess a model or substitute another provider.
3. Run the helper's `preview` action with `--implement-model`, optional `--implement-effort`, `--judge-model`, optional `--judge-effort`. Show current and proposed assignments and obtain confirmation, including on repeat setup.
4. Run the same arguments with `apply --confirm-digest <preview-confirmationDigest>` only after confirmation. The helper merges only the two role model configurations into user-level `agents.overrides`, preserves other settings and refuses concurrent edits. Respect any host approval prompt for configuration changes. Credentials and settings files stay local.
5. Report the saved assignments and reload/new-session requirement. Verify effective agent configuration after reload before claiming the models are active. An unsupported runtime field is a compatibility error, not successful setup.

Setup runs only the local setup helper. It installs no runtime dependencies, modifies no plugin files and writes no Cursor configuration.

## Paths and evidence

Create user skills under `~/.qoder/skills/` and project skills under `.qoder/skills/`. Use the host's skill-authoring guidance. Upstream README, guides and Claude adapter are reference material; this Qoder contract governs execution. Raw Cursor agent and automation sources under `reference/` are inert reference material, not registered components.

For recall, reflect, eval and session pickup, use available Qoder conversation tools or verified transcript locations. When transcripts or required evidence are unavailable, report the gap or use the upstream documented digest alternative; a skipped check never counts as a pass.

## Unavailable capabilities

The published bundle excludes make-bot-ui. Help or playbook references to it mean unavailable, not an instruction to fetch it. Cursor routines/Benny, Bugbot-specific controls, Custom Modes/shortcuts, /loop and Cursor cloud-dashboard lifecycle are unsupported: state the skipped step briefly and continue remaining meaningful work. If the skipped step is the requested result itself, report that result unavailable. Retain ordinary git/forge operations supported by the host.

External cursor-team-kit skills and Cursor built-ins are not bundled. Use an actually available equivalent or report the missing prerequisite. Never promise execution after the current session stops. Bundled upstream scripts are inert at sync/build/setup; invoke them for an authorized task only after checking runtime requirements and effects. Do not bootstrap Bun packages, install renderers or use the Cursor/macOS worktree audit as a Qoder deletion-safety gate automatically.
<!-- upstream skill body follows -->

# Swarm

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
4. Pick the worker model from the `swarm workers` line in `~/.cursor/rules/pstack-models.mdc`. If the rule or that line is missing, use `grok-4.7-xhigh-fast`. For `auto` or `inherit-parent`, omit `model` so the workers run on the parent model. If the Task tool rejects a slug, use the default and say so. If it rejects the default, use the closest valid slug of the same family from its error message. For a model race, name each arm's model up front. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.
5. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Spawn all N workers in one message with `subagent_type: generalPurpose`, `environment: "cloud"`, `run_in_background: true`, and the step 4 model, left unset for `auto` or `inherit-parent`. Use `environment: "local"` only when the worker needs access to something on the user's computer.

When a worker must start from a non-default pushed branch, pass `cloud_base_branch`.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
