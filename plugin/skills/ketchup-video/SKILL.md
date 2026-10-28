---
name: ketchup-video
description: "Catch the user up like /ketchup, with a short subtitled video of slides for what happened and the waiting calls as text under it. Use for /ketchup-video."
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

# Ketchup video

Follow [`/ketchup`](../ketchup/SKILL.md), but show what happened in a short subtitled video instead of its summary and visuals. Its window starts at the last message the user wrote before `/ketchup-video`, not before any earlier `/ketchup`. Writing and rendering the video, outside the repo, is the one exception to its read-only rule. The reply is ketchup's opening sentence, the embedded video, one line naming any work left that you can do yourself, and the action items. When the video shows a call's options, call each option by the name the video gives it. If the render fails, say so in one line and give only the calls.

## Slides

Use the screenshots, recordings, diffs, and data the work produced, not the chat's prose about them. Before you draw, write the one sentence the user should leave with and one line per slide. Drop each slide that does not change what the user knows. Use at most 10 slides, and fewer is better. Neither note goes in the reply.

Each slide makes one point. Build the slides on one picture and change it from slide to slide, rather than cut to an unrelated one. A color or shape means the same thing on every slide. Show the work in pictures, such as how a system works, a PR stack with each PR's state, a before and after of a fix, or options side by side. Point at what changed with arrows, highlights, and motion. A slide is never a bullet list, a status list, a table, or boxes with nothing connecting them.

Keep text to the minimum. Put each label on the thing it names, in plain words a person would say, not tags like "Tests: pass". Never caption what a picture shows, and never give a fact twice, across slides or in the text under them.

Show what came of each thing the user asked for, and whether it is done, still running, failed, or not checked. Never show something done that still waits on the user. Show any bug found and fixed on the way. If a visible change has no screenshot, say so on its slide and name what changed on screen. Draw only from facts you have. Never invent a number, and never draw a screen you did not capture.

## Subtitles

Give each slide one short subtitle line, about ten words, that says its point the way you would tell the user, from only what that slide shows. Say what the picture means rather than read out its labels. Put the subtitle in a strip below the slide, the same height on every slide and empty except for the subtitle, so it never covers the slide. Set it small, but readable when the video plays at chat size.

## Render

Render one silent landscape video, such as an mp4, with motion between slides. Every frame is the slide itself, edge to edge, above its subtitle strip. Make the frames from the slides, never by recording a screen, and burn each subtitle into its slide's frames so it stays on screen for the slide's whole hold. The hold is the time a slide is fully on screen, not counting the motion into or out of it. Hold each slide long enough to read the words it adds, at least one second for each three words. A slide adds its subtitle and each word that was not on the slide before it, including a label it changes. The first slide adds all its words. Words inside a screenshot do not count.

Before you embed the video, check the rendered file. Look at one frame from each slide at chat size, and check that its subtitle is readable and covers nothing. Measure each hold by matching the file's frames to the slide, not with a still-frame detector, which counts the faint ends of a fade as still. Count the words each slide adds against its measured hold. Fix any slide you cannot read in that time, render again, and check again.
