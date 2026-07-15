# Implementation Rules

Use this reference during planning and implementation.

## Preserve the existing project

Before adding dependencies or creating parallel systems:

- read `package.json`, lockfiles, configuration, routes, and entry points;
- use the current package manager;
- reuse the existing CSS strategy;
- follow current naming, file organization, formatting, and testing conventions;
- inspect existing design tokens and components for exact matches;
- avoid rewriting unrelated modules.

## Greenfield fallback

When no stack exists and the user has not specified one, select the smallest production-sensible stack that supports the interface. A reasonable web default is TypeScript, a modern component framework, semantic HTML, CSS custom properties, and a lightweight test/build setup. Record the choice and avoid dependency bloat.

## Geometry before decoration

Implement in this order:

1. root sizing and page background;
2. section boundaries;
3. major columns and alignment anchors;
4. content widths and text wrapping;
5. images and visual focal points;
6. typography;
7. component padding and gaps;
8. borders, radii, shadows, gradients, and blur;
9. icons and tiny details;
10. motion.

## Component boundaries

Create a component when one or more apply:

- it repeats;
- it has its own interaction or state;
- it has a coherent semantic role;
- it is likely to be reused;
- separating it makes visual tuning safer.

Do not fragment every text line into a component. Do not put the entire page in one giant component.

## CSS and sizing

- Use CSS variables or the project theme for repeated tokens.
- Use fixed values where the reference requires fixed geometry.
- Use fluid sizing where evidence shows scaling.
- Use `clamp()` only when it reproduces observed interpolation.
- Match `box-sizing`, line-height, and font rendering assumptions.
- Avoid excessive `!important` and specificity wars.
- Avoid unexplained magic numbers; comment values that compensate for a known visual constraint.
- Prefer logical properties when they do not make the code harder to compare with the reference.

## Content fidelity

- Preserve exact visible copy, capitalization, punctuation, number formatting, and ordering.
- Do not replace content with lorem ipsum unless the reference text is unreadable and no source exists.
- Match visible truncation and line clamps.
- Use data arrays for repeated cards or navigation items rather than duplicating markup.

## Assets

- Map every visible asset to a source file or documented substitution.
- Compress or optimize only when visual quality is preserved.
- Preserve transparency, masks, and focal points.
- Do not hotlink unstable third-party URLs in a production implementation.
- Do not remove watermarks or ownership marks.

## Icons

- Match the icon family and stroke treatment.
- Normalize SVG view boxes and optical alignment without changing the visible glyph.
- Apply `aria-hidden="true"` to decorative icons and accessible names to icon-only controls.

## Interactions

Implement interactions shown or strongly implied by the reference. For an ambiguous control, choose the least surprising standard behavior and record the assumption.

Examples:

- active nav item changes route or section;
- carousel arrows move the rail;
- tabs change the visible panel;
- menu icon opens navigation;
- form control accepts input and validates;
- modal trigger opens a dismissible dialog;
- hover cues receive corresponding hover behavior.

## Motion

Do not add animation as decoration. When motion is required:

- match the visible direction and distance;
- use restrained durations and easing;
- preserve layout stability;
- respect `prefers-reduced-motion`;
- avoid blocking input during long transitions.

## Libraries

Before adding a library, answer:

1. Is equivalent functionality already installed?
2. Does the library improve visual fidelity or reliability?
3. Is the cost proportionate to the feature?
4. Can it be tree-shaken or imported narrowly?
5. Is its license suitable?
6. Can the project deploy it in the target environment?

Record each added dependency and its purpose in the completion report.

## Maintainability

An exact implementation should still be editable. Prefer reusable tokens, clear component boundaries, and direct readable CSS over generated noise or one-off coordinate dumps.
