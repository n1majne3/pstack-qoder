---
name: statechart
description: "Draw how any system moves between states, such as a product flow, a protocol, or a service, as a Mermaid statechart from a TLA+ model. Each bug is a numbered path with blue borders to a state that breaks a rule. Use for /statechart, to show a bug as a path through states, or to turn an agreed chart into a TLA+ skeleton."
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

# Statechart

The chart shows how a system moves between states, in the words of the person who reads it. The scripts call that person the reader, as in `readerActions` and reader steps. The reader decides whether the behavior is right. The reader can be a PM who reads a product flow, an engineer who reads a protocol or a service, or a reviewer who reads a design. Label each state with what the reader can observe or cares about, such as "Paying" in an app or "Lease held, write pending" in a lock service. Label each step with the event that moves the system, such as "tap Pay" in an app, "the request reads the count" in a service, or "the lease expires" in a lock service. Keep variable and action names out of labels.

Run `node <skill dir>/scripts/statechart.mjs --help` for the commands and for how to read a chart. Work in a scratch folder outside the repo. The command writes its files next to its input. The first run installs TLC and Java with mise, which downloads about 305 MB and needs the network. The help's TLC section tells how to use a TLC and Java that you have.

## Pick the direction

Use `from-spec` when a TLA+ model exists, or when the code or design is concrete enough to model. Use `from-chart` when there is no model, and the people who own the behavior should agree on it before anyone builds or changes it.

If the code already has a TLA+ spec, start from a copy of that spec. Add the variables that the labels and rules need, and keep the spec's existing invariants. To audit the code against that spec, make the copy model what the code does, and pass the spec unchanged as `--against`. Check it with the config that its authors say it passes, and pass that config as `--against-config` unless it has the spec's file name. One mapping labels both models, so label states and steps from variables that both have. A label that reads a variable that only the copy has must test `"name" in v` first, and label the spec's states another way. When a model describes code, tie every variable and action to code that a reviewer can open, and take its name from that code. Make each action one indivisible step in the code. Put the file and line of the code that checks each condition of an action in a comment on that condition, as in `\* pay.ts:120`.

## Spec to chart

1. Choose the chart's states. When the reader cares about something that a label would hide, put it in the label, such as "Paying, charged twice" when the screen still says "Paying" after a second charge. Start with few states. Split a state when the split separates two bugs, or when the reader must see a step that leaves the label the same, such as a request that reads a count, because the chart does not draw such a step.
2. Write each rule that the reader agrees to as one invariant, with the reader's sentence as its comment. A rule can be about any state in the model: what a screen shows, what a request returns, a stored value, or a message between parts. When the model describes code, the rule also names the code that can change that state. If the model has no variable for what a rule is about, add the variable. Do not drop the rule. For a rule that applies once everything settles, define `Settled == ~ENABLED System`, where `System` is the disjunction of the actions that happen without the reader. For a rule that applies at a narrower point, such as after each request finishes, write a predicate for that point and make the rule hold where it is true. For a goal that the system must be able to reach, write a rule that says the goal never happens, and pass that rule with `--expect-broken`. The path that breaks it is then a way to the goal. The chart still draws the goal as a state that breaks a rule, and `stories.md` tells it as a bug, so name each goal rule in the hand-off. Report each other broken rule as a bug. Never weaken a rule to make the chart pass.
3. Run `from-spec`, then fill in the mapping file it writes. Put the labels in `state` and `step`. When the chart must separate what the reader does from what happens around the reader, list the reader's actions in `readerActions` by action name. Leave the list empty when every action counts the same. When the overview is too large to read, add `--cover`. The overview then keeps only the shortest path to each settled state, plus every bug path, and the command lists what it leaves out. When two bugs end in the same state for different reasons, add `cause` and make it name each reason. To color the states by what the reader cares about, such as "Order shipped", return that group from `group`. The legend names the groups, and in the PNG a state that breaks a rule is red in place of its group color.
4. If there is a proposed fix, model it and pass that model as `--fixed`.
5. Render each chart with `--png` and look at every PNG. Check that each numbered path reads in order. If a label reads like code, fix `state` or `step` and run the command again.
6. When the model describes code, replay each bug's story against the real code, as a test or a live repro, one step per model action. Drive only entry points that a user, a client, or another part of the system reaches, and assert only what they can observe. A test that asserts a flag that it sets, or that searches the source text, proves nothing. When a run proves part of the story and reading the code proves the rest, say which part each proves. When the test copies code that it cannot import, give the commit and line range of the copy, and list what the copy leaves out. If a bug does not reproduce, assume the model is wrong until you show otherwise. Fix the model, not the rule. For a design with no code yet, the TLC trace is the evidence, and the hand-off must say so.

## Chart to spec

1. Draw the chart that the reader agrees to. Use one region for each part that changes independently, such as a device's connection and the job that the device runs. Add one `%% never` line per rule, with the reader's sentence. Draw an event that stops or restarts a part, such as "the app closes" or "the process restarts", as an edge to the state that comes next. Run `render CHART.mmd` to get a PNG of the chart for the reader.
2. Run `from-chart`. If a rule breaks, the agreed chart has a design bug. Take the bug to the people who agreed to the chart.
3. Add the real code's guards and variables to the spec that `from-chart` wrote, and run `from-chart` again. For each difference it prints, ask the reader whether the code is wrong or the chart needs a correction.

## Hand off

Give the PNG and the Mermaid source of each chart to the person who must decide. Add one line per bug with the rule it breaks, its steps as the chart numbers them, whether it reproduced, and whether the proposed fix fixes it. A broken PROPERTY has no path on the chart, so give the TLC counterexample that `stories.md` names for it. With `--against`, also say whether the spec already lists it: in the configs that `stories.md` names, in the spec's notes on what the model leaves out, or not at all. When the model describes code, do not report that a rule holds while the command lists conditions with no file and line. Take every count you quote from `summary.json`. Attach `stories.md` and the command that regenerates everything. Say what the model leaves out.
