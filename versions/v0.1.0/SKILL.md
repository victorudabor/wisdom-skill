---
name: exact-ui-replica
description: Reconstructs a supplied UI screenshot, MVP image, mockup, or visual reference as a high-fidelity working frontend. Use when the user asks to clone, recreate, reproduce, reverse-engineer, or build an exact or pixel-perfect interface, including its layout, spacing, typography, colors, icons, assets, responsive behavior, interactions, styles, and libraries. Do not use for open-ended redesigns unless a reference must first be replicated.
license: MIT
compatibility: Requires an agent that can inspect images and edit a codebase. Visual verification works best with Node.js 20+, Playwright, Python 3.10+, Pillow, and NumPy.
metadata:
  author: Maverp
  version: "0.1.0"
  category: frontend-engineering
  capability: screenshot-to-code
---

# Exact UI Replica

Reconstruct a supplied visual interface as a functioning frontend with measured visual fidelity. Treat the reference as the primary source of truth. Do not beautify, reinterpret, simplify, modernize, or replace visible design decisions unless the user explicitly requests a redesign.

## Core objective

Produce the closest practical implementation of the reference at the reference viewport and preserve its design language across inferred responsive states.

“Exact” means:

- identical information hierarchy and visible content structure;
- matching section order, dimensions, alignment, spacing, colors, typography, radii, borders, shadows, imagery, icons, and layering;
- matching responsive behavior when multiple viewport references exist;
- working interactions for visible controls and states;
- evidence-based visual verification rather than subjective claims.

A single static image cannot reveal every hidden state, font file, asset, interaction, or breakpoint. Never claim mathematical identity when the evidence is incomplete. Report assumptions and measured differences.

## Activation boundaries

Use this skill when the user provides or points to at least one of the following:

- UI screenshot;
- MVP image;
- Figma export or mockup;
- landing-page reference;
- dashboard or mobile-app reference;
- an existing implementation plus a reference it must match.

Do not silently proceed as though a missing visual reference exists. When no usable reference is available, state that the reference is required and provide a structured intake checklist. Do not invent the design and call it an exact replica.

## Required operating principles

1. **Reference over preference.** The visible reference outranks personal design taste and generic best practices, except for safety, accessibility, or explicit project constraints.
2. **Inspect before editing.** Examine every supplied image and audit the existing repository before selecting libraries or changing files.
3. **Preserve the stack.** Reuse the project’s framework, conventions, package manager, styling system, and components unless they make faithful reconstruction impractical.
4. **No decorative drift.** Do not add gradients, glassmorphism, animations, cards, icons, effects, copy, or sections that are absent from the reference.
5. **No arbitrary defaults.** Avoid defaulting to common fonts, blue buttons, Lucide icons, Tailwind spacing, or fashionable patterns merely because they are convenient.
6. **Measure, implement, compare, correct.** A first render is not completion.
7. **Functionality must survive fidelity.** Visible controls should work, semantic structure should be sensible, and the page should remain maintainable.
8. **Do not damage unrelated code.** Keep changes scoped and preserve existing behavior.

## Inputs to establish

Collect these from the user message, attached files, repository, or environment:

- reference image paths and their pixel dimensions;
- target route or screen;
- target viewport or device size;
- existing or preferred framework;
- available logos, photos, icons, fonts, videos, and 3D assets;
- required interactions and navigation;
- responsive targets;
- deployment constraints;
- whether placeholder content is permitted.

Do not block unnecessarily. If non-critical details are unavailable, infer conservatively, record the assumption, and continue.

## Mandatory workflow

### Stage 1 — Reference inventory

1. Identify every visual reference and record its dimensions.
2. Determine whether references represent different pages, breakpoints, states, scroll positions, or concepts.
3. Rank references by authority when they conflict.
4. Inspect supplied assets separately from screenshots.
5. Run `scripts/inspect_image.py` when local image paths are available.

Create or update a design specification using `assets/design-spec-template.md`.

### Stage 2 — Repository audit

Before installing anything:

1. Inspect the file tree and package manifests.
2. Identify the framework, router, build tool, package manager, styling approach, icon libraries, fonts, test tools, and screenshot tooling.
3. Locate the target route and reusable components.
4. Detect project instructions such as `AGENTS.md`, contributor guides, lint rules, and deployment requirements.
5. Record constraints that affect the reconstruction.

Do not replace a functioning stack merely to match a preferred boilerplate.

### Stage 3 — Visual forensics

Read `references/visual-forensics.md` and decompose the reference into:

- canvas and viewport;
- global background and overflow behavior;
- header, navigation, hero, sections, rails, footer, overlays, and floating elements;
- grid, columns, alignment anchors, containers, gutters, and section rhythm;
- typography hierarchy and line wrapping;
- color and opacity tokens;
- borders, radii, shadows, blur, texture, and depth;
- icons, illustrations, photos, videos, logos, and masks;
- visible states, controls, and motion cues;
- probable responsive rules.

Separate direct observations from inferred decisions.

### Stage 4 — Design-token extraction

Build a compact token set before styling individual components:

- canvas and surface colors;
- text and muted-text colors;
- accent and status colors;
- font families, sizes, weights, line heights, and letter spacing;
- spacing scale derived from repeated measurements;
- container widths and gutters;
- radii, border widths, and shadow recipes;
- icon sizes and stroke style;
- z-index and overlay levels;
- animation durations and easing when visible.

Use CSS custom properties, theme tokens, or the project’s existing token system. Do not force a mathematically neat scale when the reference visibly uses irregular values.

### Stage 5 — Component and build plan

Read `references/implementation-rules.md` and create a build plan using `assets/build-plan-template.md`.

The plan must identify:

- page shell;
- component boundaries;
- asset mapping;
- data model for repeated content;
- exact implementation order;
- responsive strategy;
- interaction requirements;
- verification viewports;
- uncertain areas and fallback decisions.

Build in visual order, usually from the outer canvas inward and from large geometry to small decoration.

### Stage 6 — Implementation

Implement using these priority rules:

1. page dimensions, background, and overflow;
2. major section geometry;
3. containers, grid, alignment, and spacing;
4. typography and line wrapping;
5. visible assets and iconography;
6. surfaces, borders, radii, shadows, and effects;
7. controls and interaction states;
8. animation and micro-details;
9. responsive behavior;
10. accessibility and code cleanup.

Use real supplied assets whenever available. When an asset is missing, follow `references/missing-inputs-and-assumptions.md` and visibly document the substitution.

### Stage 7 — Responsive reconstruction

Read `references/responsive-reconstruction.md`.

When multiple breakpoints are supplied, reproduce each one directly and interpolate between them. When only one screenshot exists:

- preserve the reference exactly at its viewport;
- infer responsive changes from content priority and layout constraints;
- avoid inventing entirely new mobile patterns without evidence;
- test at narrow, reference, and wide widths;
- prevent overflow, overlap, clipped copy, and unusable controls.

### Stage 8 — Functional verification

Verify:

- navigation and visible calls to action;
- hover, focus, active, selected, expanded, modal, tab, carousel, menu, and form behavior where represented;
- keyboard operability for interactive controls;
- loading and error handling when the implementation connects to data;
- route integrity and absence of broken assets;
- console, type, lint, and test errors.

Do not implement a non-functional image when the user asked for a working interface.

### Stage 9 — Visual verification loop

Read `references/verification-loop.md`.

For each authoritative viewport:

1. run the application;
2. capture a screenshot with `scripts/capture_page.mjs` or existing project tooling;
3. compare it against the reference with `scripts/visual_diff.py`;
4. inspect the generated overlay and heatmap;
5. classify mismatches as geometry, typography, color, asset, effect, state, or content;
6. correct the highest-impact mismatches first;
7. repeat until the remaining differences are understood and documented.

Never call the result pixel-perfect without a comparison pass.

### Stage 10 — Completion report

Use `assets/fidelity-report-template.md` and report:

- files added or changed;
- route and run command;
- reference viewport(s);
- visual-difference measurements when available;
- implemented interactions;
- tests performed;
- substitutions and assumptions;
- remaining mismatches and why they remain.

## Fidelity priorities

When trade-offs are unavoidable, prioritize in this order:

1. layout geometry and alignment;
2. content hierarchy and text wrapping;
3. typography;
4. image and icon fidelity;
5. colors and surfaces;
6. spacing and sizing details;
7. effects and micro-interactions;
8. invisible implementation details.

## Quality gates

The work is incomplete until all applicable gates pass:

- the reference was inspected at full available resolution;
- the existing repository was audited;
- visible sections and elements are represented;
- no unsupported redesign decisions were introduced;
- the authoritative viewport was rendered and compared;
- major geometry mismatches were corrected;
- visible controls work;
- no obvious console, build, type, or lint failures remain;
- substitutions and unresolved differences are disclosed.

Suggested targets, not universal guarantees:

- major alignment anchors within 2–4 CSS pixels at the authoritative viewport;
- no unintended text-wrap differences in primary headings and calls to action;
- no missing visible elements;
- structural similarity score of at least 0.95 when the comparison pipeline and reference quality support it;
- pixel-difference percentage reduced across iterations, with remaining differences explained.

## Library-selection rules

- Reuse installed libraries when they can reproduce the reference faithfully.
- Add a dependency only when it materially improves fidelity, function, or maintainability.
- Match the visible icon family when identifiable.
- Prefer CSS for simple effects; use SVG or canvas when the shape cannot be reproduced faithfully with CSS.
- Use an animation library only for motion that is visible or explicitly required.
- Do not introduce a large UI component library merely to recreate a small custom interface.
- Pin newly added dependency versions and document why each was added.

## Prohibited behavior

Do not:

- claim to have seen an image that is not available;
- redesign while describing the result as a replica;
- replace visible copy with generic marketing copy without permission;
- use arbitrary placeholders when supplied assets exist;
- hide mismatches with cropped screenshots;
- optimize only for desktop when mobile references were supplied;
- hardcode the entire page as one unmaintainable image or canvas unless the user explicitly requests a static visual;
- remove existing functionality unrelated to the target screen;
- expose secrets or use production credentials during verification.

## Available scripts

- `scripts/inspect_image.py` — Reports image dimensions, mode, alpha usage, and dominant colors as JSON.
- `scripts/capture_page.mjs` — Captures a webpage at an exact viewport using Playwright.
- `scripts/visual_diff.py` — Compares reference and rendered screenshots and creates metrics, overlay, and heatmap files.

Run each script with `--help` before first use.

## Reference files

Load only the files relevant to the current stage:

- `references/visual-forensics.md`
- `references/implementation-rules.md`
- `references/responsive-reconstruction.md`
- `references/verification-loop.md`
- `references/missing-inputs-and-assumptions.md`
- `references/accessibility-and-behavior.md`

## Response style

During implementation, communicate concrete findings rather than generic reassurance. Mention important mismatches as soon as they are discovered. At completion, distinguish verified facts from assumptions and do not overstate fidelity.
