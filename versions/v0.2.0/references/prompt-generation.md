# Prompt Generation Mode

Use this reference when the requested output is an engineered coding prompt rather than immediate code.

## Purpose

The generated prompt is a build contract for another coding agent. It must reduce interpretation, prevent redesign drift, and make verification unavoidable.

## Required preparation

Before writing the master prompt:

1. isolate the exact page, panel, state, and viewport;
2. inventory visible content and assets;
3. extract the design system and component structure;
4. identify the existing or requested stack;
5. separate observed values from estimates;
6. identify unresolved assets and behavior;
7. decide what the target agent may change.

## Prompt architecture

Use this order:

1. **Role and outcome** — define the agent as a senior frontend reconstruction engineer and state the exact deliverable.
2. **Reference authority** — declare the images and viewports as the source of truth.
3. **Repository rules** — inspect before editing, preserve stack, do not damage unrelated code.
4. **Evidence ledger** — list reference dimensions, target route, panels, states, assets, and confidence.
5. **Technology contract** — framework, language, styling, icon, animation, 3D, data, and deployment constraints.
6. **Global design system** — tokens, fonts, containers, spacing, radii, borders, shadows, z-index, motion.
7. **Page anatomy** — every visible section in order.
8. **Component specifications** — purpose, content, geometry, visual treatment, behavior, responsive transformation.
9. **Asset map** — original assets, project assets, generated-safe primitives, and prohibited substitutions.
10. **Responsive rules** — authoritative viewports and changes by component.
11. **Interaction states** — hover, focus, active, selected, open, loading, empty, error, and motion.
12. **Implementation sequence** — geometry first, then typography/assets, then effects/behavior, then responsive and QA.
13. **Verification protocol** — exact screenshot commands, comparison, mismatch classification, and iteration.
14. **Acceptance criteria** — measurable visual, functional, responsive, accessibility, and code-quality gates.
15. **Completion format** — changed files, commands, metrics, assumptions, and unresolved differences.

## Specificity rules

- Use direct imperatives: “Set,” “Preserve,” “Measure,” “Capture,” and “Compare.”
- Include exact values only when observed or measured.
- Label estimates with a tolerance or confidence.
- Include visible copy verbatim when legible.
- State image crop, object position, alignment anchors, and line wrapping.
- Describe icon style and size, not merely icon meaning.
- Name libraries only when installed, requested, or justified by the visual requirement.
- For 3D or cinematic references, specify rendering responsibilities, fallback behavior, performance budgets, and reduced-motion handling.
- Tell the agent which changes are prohibited.

## Weak prompt patterns to avoid

Avoid:

- “Make it modern and beautiful.”
- “Use the best libraries.”
- “Make it pixel-perfect” without verification steps.
- “Use Tailwind and Lucide” without repository or visual evidence.
- long lists of trendy effects not visible in the reference;
- declaring exact font names from visual guesswork;
- mixing desktop and mobile layouts into one unclear specification;
- asking for every possible feature when only the visible MVP is in scope.

## Handling unreadable or hidden information

Use placeholders only when needed to preserve geometry. Mark them clearly. Do not invent business metrics, legal claims, testimonials, prices, or backend behavior from a screenshot.

## Final self-check

The target coding agent should be able to answer these from the prompt alone:

- What route and viewport am I building?
- Which reference is authoritative?
- What must remain unchanged?
- What are the page sections and components?
- What are the key dimensions and tokens?
- Which assets and libraries should I use?
- How does each component respond?
- Which interactions must work?
- How do I prove visual fidelity?
- What exactly must I report when complete?
