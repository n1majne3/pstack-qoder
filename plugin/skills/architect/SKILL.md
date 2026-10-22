---
name: architect
description: "Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape."
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

# Architect

Sketch types, function signatures, class shapes, and module boundaries with `not implemented` bodies and pseudocode. Synthesize across multiple model perspectives, then fill in code against the chosen sketch.

## Start

Open a todolist with one entry per phase before starting.

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

## Phase A: Ground the problem

Build a real mental model of every system the new code touches. Run the **how** skill over the relevant subsystems. Naming a file isn't grounding. Produce the architectural explanation `how` prescribes. If the design redefines ownership or layering, also run the **why** skill on the existing shape so the rationale becomes a constraint, not a guess.

Skip Phase A only when the work is genuinely greenfield with no surrounding system to integrate.

## Phase B: Sketch

Run the **arena** skill with the design-sketch task and the Phase A grounding artifacts. Pass `references/runner-prompt.md` as each runner's prompt.

Take the runners from the `architect runners` line in the `pstack-models.mdc` rule, in place of the `arena runners` line. If the rule or that line is missing, use `claude-opus-5-5-xhigh` and `grok-4.7-xhigh-fast`. Alias and rejected entries follow the runner rules in the **arena** skill's Phase A.

Design it twice. Require at least two structurally distinct candidates before synthesis, even when the first looks sufficient. This is the **exhaust-the-design-space** principle skill made concrete. Whole-shape alternatives, not point fixes inside one shape.

Screen every candidate against [`references/design-red-flags.md`](references/design-red-flags.md) before synthesis. Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Prefer the design where a change that looks right from one file is right for the whole repo.

Compare viable candidates on interface depth. Prefer the design that hides more complexity behind a smaller, simpler public surface. A rich interface can keep call chains short by concentrating capability instead of scattering it across layers.

Arena returns one synthesized design package. Its synthesis decision fills the rationale's "Synthesis decision" section.

## Phase C: Agree (opt-in)

Default: proceed directly to implementation with the synthesized design. No human checkpoint.

Opt in to a checkpoint when the invoker explicitly asks: "/architect with checkpoint," "stop and show me before implementing," or similar. Then surface the synthesized design and pause for sign-off.

The synthesis can ship as its own commit either way, as the "scaffold first" mode of the **foundational-thinking** principle skill. Planned and scoped breakage during fill-in is fine, per the **outcome-oriented-execution** principle skill. For adversarial pressure on the design before implementing, run the **interrogate** skill on the synthesized sketch.

If the human pushes back on the shape (in a checkpoint or after the fact), treat that as Phase A evidence. Re-ground and re-run Phase B before writing more code.

## Phase D: Implement against the sketch

Replace `not implemented` bodies with code, pseudocode with logic. The synthesized sketch is the contract. Deviations from it are signal to surface, not friction to absorb silently. If a function needs a parameter the sketch didn't anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching.

## Phase E: Scrap when the architecture is wrong

If implementation keeps producing friction the sketch can't absorb, throw the sketch out. Don't bolt fixes onto a wrong design, per the **redesign-from-first-principles** and **fix-root-causes** principle skills.

The signal is a *pattern*, not single instances. Tells:

- The same shape of workaround appearing repeatedly across unrelated code.
- Multiple unrelated edge cases that all need special-case branches.
- Types that need escape hatches (`any`, casts, optional fields always set in practice) to compile.
- The "we need a lock" reflex when the sketch said the state wasn't shared.
- Callers having to know the abstraction's internal rules to use it.
- Two or more independent Phase D deviations of the same shape across the implementation.

Use judgment. A few edge cases don't condemn an architecture. Some problems are legitimately complex. Complexity in the data is not complexity in the design.

When you scrap:

1. Re-run the **how** skill over what's been built.
2. Redesign as if the new constraints had been day-one assumptions, per redesign-from-first-principles.
3. Subtract before adding, per the **subtract-before-you-add** principle skill. The new sketch should be smaller than the old one before it grows.
4. Return to Phase B and re-run arena.

## Outputs

The caller's usage is written first and the type sketch derived from it. One file with new types and signatures for small changes. Module map plus type definitions for larger work. The rationale ships alongside, shaped per `references/rationale-template.md`, including the usage sketch and the synthesis decision.
