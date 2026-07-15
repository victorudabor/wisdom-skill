# Visual Forensics

Use this reference during Stage 3. The purpose is to convert visual evidence into an implementable specification without redesigning it.

## 1. Establish the canvas

Record:

- exact reference width and height;
- visible browser or device chrome, if any;
- whether the image is a complete page, cropped page, modal, component, or composite;
- likely device pixel ratio when metadata or sharpness provides evidence;
- whether the screenshot is at the top of the page or mid-scroll;
- global background color, image, gradient, video, texture, and overflow behavior.

Do not treat screenshot pixels as CSS pixels automatically. Use known device dimensions, browser chrome, text size, and project context to infer the CSS viewport.

## 2. Mark alignment anchors

Identify the stable lines that govern the composition:

- left and right container edges;
- header baseline and bottom edge;
- central axis;
- column boundaries;
- repeated card edges;
- image crop boundaries;
- text-block widths;
- button and control baselines;
- section starts and ends.

Major anchors matter more than tiny decoration. A page with accurate colors but incorrect anchors will still look wrong.

## 3. Decompose layers

For each visible region, identify:

- structural layer: page, section, grid, flex row, stack, overlay;
- content layer: headings, body text, metadata, labels, controls;
- asset layer: image, logo, illustration, icon, video, mesh, 3D object;
- effect layer: gradient, shadow, blur, noise, mask, blend mode;
- interaction layer: button, input, tab, carousel, menu, drag target;
- state layer: selected, active, disabled, expanded, loading, empty.

Use normal layout before absolute positioning. Use absolute positioning only where the reference clearly layers or floats elements independently.

## 4. Extract typography

Record every distinct text role:

- family or closest evidence-based category;
- variable/static font behavior;
- weight;
- size;
- line height;
- letter spacing;
- case transformation;
- color and opacity;
- maximum width;
- line count and wrapping;
- alignment;
- text decoration.

Match line wrapping, not just font size. Font family, width, letter spacing, container width, and line-height interact.

When the exact font is unavailable:

1. search supplied assets and project files;
2. inspect existing CSS and package dependencies;
3. identify a legal equivalent with similar metrics;
4. tune width, size, weight, spacing, and line height;
5. disclose the substitution.

## 5. Extract color and depth

Build a table with:

- token name;
- sampled or estimated value;
- opacity;
- role;
- confidence;
- notes about blending or gradients.

Sample from flat central areas, not anti-aliased edges. For gradients, record direction, stops, spread, and transparency. For shadows, estimate x, y, blur, spread, color, and opacity.

## 6. Identify spacing logic

Measure repeated gaps and infer:

- page gutters;
- container padding;
- row and column gaps;
- card padding;
- heading-to-copy gap;
- copy-to-action gap;
- section rhythm;
- control height and internal padding;
- icon-to-label gap.

Do not force all values onto 4px or 8px increments when visible evidence contradicts that pattern.

## 7. Identify imagery and crop behavior

For every image-like region, record:

- source asset candidate;
- displayed aspect ratio;
- `object-fit` behavior;
- focal point or `object-position`;
- clipping mask and radius;
- overlays and blend modes;
- whether it continues off-canvas;
- desktop and mobile crop differences.

Do not replace distinctive photography or branding with generic stock assets and still call the result exact.

## 8. Identify icons

Determine:

- filled, outlined, duotone, hand-drawn, or custom style;
- stroke width;
- corner and cap style;
- optical size;
- container shape;
- icon-to-text alignment;
- candidate installed library.

Prefer, in order:

1. supplied original icon;
2. existing project icon library with the matching glyph;
3. exact legal open-source equivalent;
4. custom SVG traced from authorized reference evidence;
5. transparent documented approximation.

## 9. Infer layout model

Choose the simplest layout system that explains the evidence:

- centered max-width container;
- full-bleed sections with inner container;
- CSS Grid;
- flex rows and stacks;
- sticky header or rail;
- layered absolute composition;
- horizontal scroll or carousel;
- viewport-height hero;
- fixed or floating controls.

Do not reproduce a responsive grid using hundreds of unrelated absolute coordinates.

## 10. Confidence labels

Label specification decisions:

- **Observed:** directly visible or measurable.
- **Strong inference:** supported by repeated geometry or project evidence.
- **Weak inference:** plausible but not confirmed.
- **Substitution:** original source is unavailable.

These labels belong in the design specification and final report.
