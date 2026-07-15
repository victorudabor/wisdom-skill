---
name: exact-ui-replica
description: Analyze a supplied UI screenshot, MVP image, mockup, or existing page to generate an implementation-ready master coding prompt, build a high-fidelity working frontend, or repair code until it matches the reference. Use for screenshot-to-code, pixel-accurate recreation, exact UI cloning, MVP reverse engineering, visual-difference correction, responsive reconstruction, design-token extraction, and detailed frontend build specifications. Do not use for open-ended redesigns unless the reference must first be replicated.
license: MIT
compatibility: Requires an agent that can inspect images. Build and repair modes also require codebase access. Verification works best with Node.js 20+, Playwright, Python 3.10+, Pillow, and NumPy.
metadata:
  author: Maverp
  version: "0.2.0"
  category: frontend-engineering
  capability: screenshot-to-prompt-and-code
---

# Exact UI Replica

Turn visual UI evidence into an implementation contract, an engineered build prompt, a working frontend, or a verified visual repair. Treat the supplied reference as the primary design authority. Do not beautify, simplify, modernize, or replace visible decisions unless the user explicitly requests modifications.

## Select the operating mode first

Infer the mode from the request and state it in the working artifacts.

### Mode A — Prompt generation

Use when the user asks for a detailed, engineered, master, implementation, Codex, Claude, Cursor, Copilot, or coding prompt based on a visual reference.

Deliver:

1. reference inventory;
2. evidence-based design specification;
3. implementation contract;
4. complete master build prompt using `assets/master-build-prompt-template.md`;
5. assumptions and unresolved asset requirements;
6. acceptance and visual-verification criteria.

Do not write generic advice. The prompt must be detailed enough for another coding agent to begin implementation without reinterpreting the design.

### Mode B — Direct build

Use when the user asks to create, code, implement, or deploy the referenced interface.

Deliver the working implementation, verification artifacts where tooling permits, and a fidelity report.

### Mode C — Visual repair

Use when an implementation already exists and the user asks to fix, align, polish, or make it match a reference.

Capture a baseline, classify mismatches, make scoped changes, compare again, and protect unrelated behavior.

### Mode D — Hybrid

Use when the user requests both the engineered prompt/specification and the implementation. Produce the implementation contract first, then build from it.

## Definition of fidelity

“Exact” means the closest practical reproduction supported by the available evidence:

- same visible information hierarchy and copy;
- matching section order, layout geometry, alignment, sizing, spacing, typography, colors, radii, borders, shadows, imagery, icon treatment, layering, and crop behavior;
- matching supplied responsive states;
- functioning visible controls and states;
- measured comparison when code is rendered;
- transparent assumptions where the reference is incomplete.

A static image cannot reveal every font file, asset, interaction, breakpoint, hidden state, or off-screen section. Never claim mathematical identity without evidence and comparison.

## Non-negotiable principles

1. **Reference over preference.** The visible reference outranks taste and trends except for safety, accessibility, legal constraints, or explicit user changes.
2. **Evidence before invention.** Distinguish observed facts, strong inferences, weak inferences, and substitutions.
3. **No decorative drift.** Do not add glassmorphism, gradients, cards, icons, animation, copy, or sections absent from the reference.
4. **No arbitrary defaults.** Do not default to Inter, Tailwind, blue buttons, Lucide icons, or a fashionable component library without evidence or project justification.
5. **Preserve the stack.** In build or repair mode, reuse the repository framework, package manager, router, styling system, and components unless they block fidelity.
6. **Geometry before decoration.** Fix the canvas, sections, containers, grids, and wrapping before micro-details.
7. **Measure, render, compare, correct.** A first implementation is not completion.
8. **Functionality must survive fidelity.** Visible interactions must work and unrelated behavior must remain intact.
9. **Do not hide uncertainty.** Record missing fonts, assets, states, and unresolved differences.
10. **Do not misidentify libraries.** Visual similarity is not proof that the original design used a particular framework or package.

## Inputs to establish

Use the conversation, attached files, repository, and environment to establish:

- reference image paths, dimensions, and role;
- target route, screen, or component;
- requested operating mode;
- authoritative viewport or device dimensions;
- existing or preferred frontend stack;
- available logos, photos, illustrations, icons, fonts, videos, and 3D assets;
- required interactions, routes, forms, overlays, and states;
- responsive targets;
- browser and deployment constraints;
- whether substitutions or placeholders are permitted.

Do not block on non-critical unknowns. Infer conservatively, label the inference, and continue. If no usable visual reference exists, follow `references/missing-inputs-and-assumptions.md` and do not invent an “exact” design.

## Mandatory workflow

### Stage 0 — Evidence and mode gate

1. Confirm that at least one usable visual reference exists.
2. Select Prompt, Build, Repair, or Hybrid mode.
3. Determine whether the image is a complete page, crop, composite board, device mockup, state, or scroll segment.
4. Separate the actual screen from presentation frames, watermarks, browser chrome, decorative borders, and mockup devices.
5. Create the intake record using `assets/reference-intake-template.md`.

For a composite concept board, identify the exact concept and panel to reconstruct. Do not accidentally combine multiple concepts into one interface.

### Stage 1 — Reference inventory

1. Record every reference filename and pixel dimensions.
2. Determine whether each reference represents a page, component, breakpoint, state, concept, or scroll position.
3. Rank references by authority when they conflict.
4. Inspect source assets separately from screenshots.
5. Run `scripts/inspect_image.py` when local paths are available.
6. Record whether screenshot pixels plausibly equal CSS pixels.

Create or update the design specification using `assets/design-spec-template.md`.

### Stage 2 — Repository audit

Required for Build and Repair modes. Optional but useful in Prompt mode when a repository is provided.

Before installing or changing anything:

1. inspect the file tree, manifests, lockfiles, routes, and entry points;
2. identify framework, language, build tool, package manager, CSS approach, component system, icon packages, fonts, tests, and screenshot tooling;
3. locate the target route and reusable components;
4. read `AGENTS.md`, `CLAUDE.md`, contributor guides, lint rules, and deployment notes;
5. run `scripts/audit_project.py` when Python and a local repository are available;
6. document constraints that affect fidelity.

Do not replace a functioning stack merely to use a preferred boilerplate.

### Stage 3 — Visual forensics

Read `references/visual-forensics.md` and decompose the reference into:

- canvas, viewport, background, and overflow;
- header, navigation, hero, sections, sidebars, rails, footer, overlays, and floating elements;
- container edges, columns, alignment anchors, grids, gutters, and section rhythm;
- typography roles, line lengths, line breaks, weights, tracking, and case;
- colors, opacity, gradients, borders, radii, shadows, blur, masks, and texture;
- photography, illustration, video, logo, icon, and crop behavior;
- visible controls, states, motion cues, and likely interactions;
- responsive transformations.

Measure high-impact anchors first. Exact-looking colors cannot compensate for incorrect geometry.

### Stage 4 — Implementation contract

Create an implementation contract using `assets/implementation-contract-template.md`.

The contract must contain:

- authority and confidence labels;
- target route and viewports;
- stack and dependency decisions;
- design tokens;
- complete visible copy;
- component inventory;
- section-by-section geometry;
- asset map and substitutions;
- responsive transformation table;
- interaction/state table;
- accessibility requirements;
- verification commands;
- acceptance criteria;
- explicit non-goals.

Values must be tagged as **Observed**, **Measured estimate**, **Strong inference**, **Weak inference**, or **Substitution**.

### Stage 5A — Generate the master build prompt

Required in Prompt and Hybrid modes. Read `references/prompt-generation.md`.

Create a self-contained prompt using `assets/master-build-prompt-template.md`. It must include:

1. specialist role and mission;
2. source-of-truth and no-redesign rules;
3. supplied inputs and reference dimensions;
4. repository/stack constraints;
5. permitted and prohibited libraries;
6. route and file-structure requirements;
7. design tokens and typography;
8. page shell and section specifications;
9. component inventory and data structures;
10. asset and icon mapping;
11. responsive behavior by component;
12. interactions, states, motion, and accessibility;
13. implementation order;
14. visual verification loop and commands;
15. completion deliverables;
16. objective acceptance criteria;
17. assumptions and questions that must not silently alter the design.

The prompt must say what to build, how to inspect the repository, how to verify it, and what counts as done. Do not pad it with motivational filler.

### Stage 5B — Component and build plan

Required in Build and Repair modes. Read `references/implementation-rules.md` and use `assets/build-plan-template.md`.

Identify:

- page shell and route;
- component boundaries;
- repeated data models;
- asset mapping;
- build order;
- responsive strategy;
- interaction requirements;
- verification viewports;
- risk areas and fallbacks.

### Stage 6 — Implementation

Implement in this priority order:

1. root dimensions, page background, and overflow;
2. major sections and stacking context;
3. containers, columns, grids, anchors, and gutters;
4. text blocks, font loading, line wrapping, and vertical rhythm;
5. images, illustrations, logos, icons, masks, and crops;
6. controls, surfaces, borders, radii, and shadows;
7. states and interactions;
8. motion and micro-details;
9. responsive behavior;
10. accessibility, tests, and cleanup.

Use real supplied assets whenever possible. Follow `references/missing-inputs-and-assumptions.md` for unavailable assets. Do not make a whole interface a single image or canvas unless the user explicitly requests a static non-interactive visual.

### Stage 7 — Responsive reconstruction

Read `references/responsive-reconstruction.md`.

When multiple breakpoints exist, treat each supplied viewport as authoritative and interpolate between them. When only one exists:

- preserve it precisely at that viewport;
- infer changes from content priority and layout failure points;
- avoid inventing an unrelated mobile design;
- test narrow, reference, intermediate, and wide widths;
- label inferred behavior.

### Stage 8 — Functional verification

Verify applicable behavior:

- links, navigation, buttons, forms, tabs, drawers, menus, modals, accordions, carousels, filters, and search;
- hover, focus, active, selected, disabled, loading, empty, expanded, and error states represented by evidence;
- keyboard access and focus management;
- route integrity, image loading, console output, type checks, linting, and tests;
- no changes to unrelated APIs or pages in Repair mode.

Read `references/accessibility-and-behavior.md` when implementing controls or motion.

### Stage 9 — Visual verification loop

Required when a runnable implementation and reference are available. Read `references/verification-loop.md`.

For each authoritative viewport:

1. run the app with deterministic data;
2. capture the exact route with `scripts/capture_page.mjs` or existing tooling;
3. compare with `scripts/visual_diff.py`;
4. inspect overlay, heatmap, mask, mismatch bounds, and regional metrics;
5. classify differences as geometry, typography, content, asset, color, effect, state, timing, or rendering noise;
6. fix the highest-impact cause rather than randomly tweaking CSS;
7. repeat and record before/after metrics.

Use `scripts/run_verification.py` to orchestrate capture and comparison when its assumptions fit the project.

Never call a result pixel-perfect without at least one comparison pass.

### Stage 10 — Completion report

Use `assets/fidelity-report-template.md` and report:

- mode used;
- files added or changed;
- target route and run command;
- reference and verification viewports;
- implemented sections and interactions;
- dependencies added and why;
- tests and checks run;
- visual-difference metrics and iteration count;
- asset/font substitutions;
- remaining mismatches and causes;
- location of generated prompt, contract, screenshots, and diff artifacts.

## Prompt quality gates

A generated master prompt is incomplete unless it:

- is tied to the actual reference rather than generic design language;
- contains the complete visible page structure and copy available from evidence;
- states exact or estimated dimensions with confidence labels;
- specifies the stack or tells the coding agent to preserve the detected stack;
- prohibits unsupported redesign and library guessing;
- defines responsive transformations and visible behavior;
- includes repository audit and implementation order;
- includes screenshot capture, visual comparison, correction, and reporting;
- distinguishes missing assets from approved substitutions;
- contains objective completion criteria.

## Build quality gates

The implementation is incomplete until all applicable gates pass:

- references were inspected at full available resolution;
- the correct panel/concept was isolated;
- the repository was audited;
- all visible regions are represented;
- no unsupported redesign was introduced;
- authoritative viewports were rendered and compared;
- major geometry and wrapping mismatches were corrected;
- visible controls function;
- no obvious build, type, lint, test, or console failures remain;
- substitutions and unresolved differences are disclosed.

Suggested targets, not universal guarantees:

- major alignment anchors within 2–4 CSS pixels at authoritative viewports;
- no unintended primary-heading or CTA wrapping differences;
- no missing visible elements;
- structural-similarity approximation of at least 0.95 when rendering conditions make it meaningful;
- a decreasing differing-pixel percentage across iterations.

## Dependency rules

- Reuse installed packages when they can reproduce the reference faithfully.
- Add a dependency only when it materially improves fidelity, behavior, or maintainability.
- Prefer CSS for simple effects and SVG for vector shapes.
- Use canvas/WebGL/3D libraries only when the reference genuinely requires them.
- Use animation libraries only for visible or explicitly required motion.
- Do not introduce a large UI kit to reproduce a small custom interface.
- Pin new versions and document each addition.
- Never claim the reference used a library without source evidence.

## Prohibited behavior

Do not:

- claim to have inspected an unavailable image;
- merge different concepts from a collage without instruction;
- redesign while calling the output an exact replica;
- invent unreadable copy as factual product content;
- replace supplied assets with generic substitutes;
- hide differences with crops or altered viewport dimensions;
- verify only desktop when mobile references are supplied;
- break APIs, routes, data flows, or unrelated pages;
- expose secrets or use production credentials;
- download or reproduce protected assets without permission;
- remove ownership marks or watermarks;
- generate a verbose prompt that lacks measurable specifications.

## Included deterministic tools

- `scripts/inspect_image.py` — image dimensions, mode, transparency, and palette.
- `scripts/audit_project.py` — repository stack, manifests, scripts, styling, tests, fonts, and likely entry points.
- `scripts/capture_page.mjs` — deterministic browser screenshot at an exact viewport.
- `scripts/visual_diff.py` — pixel metrics, structural approximation, overlay, heatmap, mask, mismatch bounds, and regional diagnostics.
- `scripts/run_verification.py` — capture-and-compare orchestration.
- `scripts/validate_skill.py` — package and metadata validation.
- `scripts/install_skill.py` — local installation helper for supported skill directories.

Run scripts with `--help` before first use.

## Load-on-demand references

- Read `references/prompt-generation.md` for Prompt or Hybrid mode.
- Read `references/visual-forensics.md` before producing the design contract.
- Read `references/implementation-rules.md` before Build or Repair implementation.
- Read `references/responsive-reconstruction.md` when more than one viewport exists or responsive behavior must be inferred.
- Read `references/verification-loop.md` before screenshot comparison.
- Read `references/missing-inputs-and-assumptions.md` when evidence or assets are incomplete.
- Read `references/accessibility-and-behavior.md` when implementing interactions, motion, or forms.

## Communication style

Report concrete observations and mismatches, not generic reassurance. Surface important uncertainty early. At completion, distinguish verified facts from estimates and never overstate fidelity.
