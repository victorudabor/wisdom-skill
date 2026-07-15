# Evaluation Rubric

Score each category from 0 to 3.

## 1. Triggering and scope

- 0: Does not activate for replica tasks or activates for unrelated redesign work.
- 1: Recognizes the task but ignores important boundaries.
- 2: Correctly scopes most cases.
- 3: Correctly distinguishes replica, modification, and missing-reference cases.

## 2. Reference analysis

- 0: Begins coding without inspecting references.
- 1: Gives a superficial visual description.
- 2: Extracts most major design properties.
- 3: Produces an evidence-based specification with observed/inferred distinctions.

## 3. Repository preservation

- 0: Replaces the stack or damages unrelated code.
- 1: Uses the existing stack inconsistently.
- 2: Mostly preserves conventions and scope.
- 3: Audits first, reuses existing systems, and keeps changes tightly scoped.

## 4. Implementation fidelity

- 0: Generic redesign.
- 1: Similar theme but incorrect geometry/content.
- 2: Strong resemblance with some major mismatches.
- 3: High-fidelity geometry, typography, assets, and states at authoritative viewports.

## 5. Responsive behavior

- 0: Broken or ignored.
- 1: Generic stacking only.
- 2: Reasonable inferred behavior.
- 3: Reproduces supplied states and validates intermediate widths.

## 6. Verification

- 0: Makes unsupported pixel-perfect claims.
- 1: Manually checks only.
- 2: Captures and compares at one target.
- 3: Runs iterative visual comparison at all authoritative viewports and reports metrics.

## 7. Functionality and accessibility

- 0: Static or broken implementation.
- 1: Partial interactions.
- 2: Main interactions work with basic accessibility.
- 3: Visible behavior works, keyboard/focus semantics are handled, and no major regressions remain.

## 8. Transparency

- 0: Hides substitutions or limitations.
- 1: Vague caveats.
- 2: Lists important assumptions.
- 3: Clearly reports substitutions, remaining mismatches, evidence, and measured results.

A production candidate should score at least 20/24 with no zero in reference analysis, implementation fidelity, or verification.
