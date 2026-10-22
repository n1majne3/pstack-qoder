---
name: maintain-formal-verification-skill
description: "Bring a project's formal verification back in line with the code after the code changes: find the commits that touched verified code, update the model, harness, or properties to describe the code as it is now, rerun, and say whether each failure is drift in the verification or a bug in the code. Use for /maintain-formal-verification-skill, \"is the model still true to the code\", or after merges and refactors that touched verified code without rechecking it."
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

# Maintain a formal verification skill

A formal check proves a property of what it describes. When the code changes and the verification does not, the check can keep passing while it describes code that no longer exists. That pass is the dangerous case, because it looks like a proof. This skill is the upkeep loop for a verify skill that `/create-formal-verification-skill` generated, or for any project-local skill that runs a model checker, prover, or code-level verifier against named code. The project-local skill handles a change that an agent makes while it uses that skill. This skill handles the changes that skipped it: merges, edits made without the skill, and drift that builds up across many commits.

## Outcomes

Give each check one outcome, and say which:

- **in sync**: no change since the last sync alters what the check describes, and the check passes.
- **updated**: the code changed, the verification now describes the new code, and the check passes.
- **bug**: the verification describes the current code, and the code breaks the property. This is a finding about the code. It is not drift.
- **blocked**: the check could not be brought back in line or could not run. Say exactly why.

A check can be both updated and bug: the update makes the verification describe the code again, and then the property fails on it.

## Edit scope

Edit only the verification: models, harnesses, property files, and the verify skill itself. Never edit product code during a run, unless the user asks you to. When a property fails on the current code, do not weaken the property or the model to make it pass. Report the failure.

## Pass

1. **Find the checks.** A verify skill has no fixed name, so find it by what it does: a project skill that runs a model checker, a prover, or another verifier against named code. Read each one you find, or the one the user named. For each check, collect the property, the code it covers, the bounds and assumptions, the command that runs it, and the commit where it was last confirmed to describe the code. If no verify skill exists, stop and point at `/create-formal-verification-skill`. If the skill does not record a sync commit, use the last commit that changed the verification files, and say that you did.

2. **Run it as it is.** Run each check once before you change anything, and record the result. A pass here does not tell you that the code is correct. It tells you that the old description still holds. A failure here can be drift or a bug. Do not decide which until step 5.

3. **Read every change to covered code.** Diff the covered files from the sync commit to the current commit, and read each commit message. Also look for code that moved: a covered function that is renamed, split, or moved to another file is still covered code. Also look for new code that touches the state that a check guards, such as a new function that writes the same fields. For each change, decide which of these it is:
   - **No effect.** The change does not alter anything the verification describes, such as formatting, comments, or code paths that the verification does not cover. Check this against the model or harness, not against the commit message.
   - **The verification no longer describes the code.** A step that was one indivisible action is now two, a branch was added or removed, a check moved, a new path reaches the guarded state, or a value now has a different range. The model or harness must change.
   - **The promise changed on purpose.** The change alters what the code promises, and evidence in the change says that this is intended: the doc comment, the tests, the changelog, or the commit message. The property must change, and you must cite that evidence.
   - **The promise may be broken.** The code changed, and no evidence says that the promise changed. Treat a failure that follows as a bug candidate.

4. **Update from the code, not from the result.** Change the model or harness so that each changed part again points to code that a reviewer can open, and keep one indivisible step in the code as one step in the verification. Write the update from the code before you rerun, and do not shape it by what makes the check pass. Change a property only for a promise that changed on purpose. Write down the old wording, the new wording, and the evidence. Keep the bounds unless the change makes them wrong. If you must reduce a bound, say so in the report.

5. **Rerun and judge each result.**
   - **Pass:** the check can now pass on a description that has lost the ability to fail. Break the new code the way the property guards against, such as removing a new check or reordering a new step, and confirm that the check catches it. Then drop the break.
   - **Fail:** replay the counterexample against the real code, step by step. If a step cannot happen in the code, the verification is wrong. Fix the verification, and say what was wrong. If every step can happen, it is a bug. Name the commit that introduced it, tell the counterexample as a sequence of steps in the code's own words, and state the harm in one sentence. If a cheap test or reproduction against the real code shows the bug, add it to the report as evidence. Do not commit it to the product code.

6. **Update the verify skill.** Update the code that each check covers, the commands, the bounds, the assumptions, and the sync commit. Set the sync commit to the commit that you checked. Do not move the sync commit for a blocked check, and say so in the report. Then follow the verify skill once as the next agent would, so that you know its steps still run.

## Report

Tell the user, for each check:

- the outcome, and the commits that you read;
- what changed in the verification and why, with a short reason for each change: the code changed shape, or the promise changed on purpose (with the evidence);
- the rerun result, and the break that you used to show the updated check can still fail;
- each bug, in plain words: the counterexample as steps in the code's words, the harm, and the commit that introduced it;
- what the verification still does not cover, including new code that it should cover and does not.

Say outright which failures were drift in the verification and which were bugs in the code. For a check that passed before you updated it and fails after, say that the old pass was on a stale description.

Put the verification updates in a change of their own, separate from any product fix.
