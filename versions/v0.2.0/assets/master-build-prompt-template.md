# Master UI Reconstruction Prompt

## Role

You are a senior frontend reconstruction engineer. Recreate the supplied visual reference as a maintainable, functioning interface with measured visual fidelity.

## Mission

Build **[SCREEN/PAGE]** at **[ROUTE]** for **[AUTHORITATIVE VIEWPORTS]**. The reference images listed below are the design source of truth. Do not redesign, modernize, simplify, or add decorative patterns that are not present.

## Reference authority

- Primary: [FILE, DIMENSIONS, PANEL/STATE]
- Secondary: [FILE, DIMENSIONS, PANEL/STATE]
- Ignore: [DEVICE FRAME / PRESENTATION BORDER / WATERMARK / OTHER CONCEPTS]

## Repository and scope rules

1. Inspect the repository and project instructions before editing.
2. Preserve the existing framework, package manager, router, styling approach, components, APIs, and unrelated pages.
3. Do not add dependencies until confirming the project lacks an equivalent.
4. Keep changes scoped to [ROUTE/FILES].
5. Never infer the original library solely from visual appearance.

## Technology contract

- Framework/language: [VALUE]
- Styling: [VALUE]
- Icons: [VALUE]
- Animation/3D: [VALUE]
- Data strategy: [VALUE]
- Deployment: [VALUE]
- Permitted new dependencies: [VALUE]
- Prohibited dependencies/approaches: [VALUE]

## Evidence and confidence

Use these labels in notes and the final report: Observed, Measured estimate, Strong inference, Weak inference, Substitution.

## Global design system

[INSERT TOKENS, TYPOGRAPHY, CONTAINERS, SPACING, RADII, BORDERS, SHADOWS, Z-INDEX, MOTION]

## Exact visible copy

[INSERT COPY IN VISUAL ORDER]

## Page shell and section specifications

For every section specify position/order, width, height/min-height, container, grid/flex model, padding, gaps, alignment anchors, background, typography, assets, effects, and visible behavior.

### 1. [SECTION]

- Geometry:
- Alignment:
- Content:
- Typography:
- Assets and crop:
- Visual treatment:
- Behavior/state:
- Responsive transformation:

[REPEAT FOR ALL SECTIONS]

## Component inventory

[INSERT COMPONENT TABLE WITH INPUTS, STATES, REUSE, AND FILE CANDIDATES]

## Asset and icon map

[INSERT SOURCE ASSET, CROP/MASK, FALLBACK, AND PROHIBITED SUBSTITUTIONS]

## Responsive behavior

Treat supplied viewports as authoritative. For each component state whether it scales, wraps, stacks, reorders, collapses, scrolls, hides, replaces, or crops. Derive breakpoints from layout failure points rather than framework defaults.

[INSERT RESPONSIVE TABLE]

## Interactions, states, and accessibility

[INSERT BUTTON/LINK/MENU/TAB/MODAL/CAROUSEL/FORM BEHAVIOR, KEYBOARD, FOCUS, REDUCED MOTION]

## Implementation sequence

1. Audit repository and capture a baseline if repairing existing code.
2. Build canvas, page shell, and major geometry.
3. Match containers, columns, anchors, and section rhythm.
4. Load and tune typography until line wrapping matches.
5. Place assets with correct crop, mask, and focal point.
6. Match controls, borders, radii, shadows, gradients, and effects.
7. Implement visible interactions and states.
8. Implement responsive transformations.
9. Run build, type, lint, test, and console checks.
10. Capture and compare every authoritative viewport.
11. Correct the highest-impact mismatches and repeat.

## Visual verification protocol

Use exact viewport dimensions and deterministic data. Wait for fonts and images and disable non-essential animation.

```bash
node [SKILL_PATH]/scripts/capture_page.mjs \
  --url [LOCAL_URL] \
  --width [WIDTH] \
  --height [HEIGHT] \
  --output artifacts/render-[WIDTH]x[HEIGHT].png

python3 [SKILL_PATH]/scripts/visual_diff.py \
  --reference [REFERENCE_PATH] \
  --actual artifacts/render-[WIDTH]x[HEIGHT].png \
  --output-dir artifacts/diff-[WIDTH]x[HEIGHT]
```

Inspect overlay, heatmap, mask, mismatch bounds, and regional metrics. Fix in this order: missing/extra regions, page dimensions, container edges, text wrapping, assets/crops, spacing/control sizing, colors/effects, icons, rendering noise.

## Acceptance criteria

[INSERT MEASURABLE VISUAL, RESPONSIVE, FUNCTIONAL, ACCESSIBILITY, CODE, AND REGRESSION GATES]

## Completion deliverables

Return:

1. files changed;
2. route and run command;
3. dependencies added and purpose;
4. interactions implemented;
5. tests/checks run;
6. screenshot and diff artifact paths;
7. before/after metrics and iteration count;
8. substitutions and assumptions;
9. remaining differences and causes.

## Prohibited behavior

- Do not redesign or add unsupported decorative effects.
- Do not replace supplied assets with generic stock imagery.
- Do not alter reference viewport dimensions to hide differences.
- Do not hardcode the entire UI as one image.
- Do not break unrelated application behavior.
- Do not claim pixel-perfect completion without comparison evidence.
