# Accessibility and Behavior

Visual fidelity and accessibility should coexist.

## Semantics

- Use landmarks such as `header`, `nav`, `main`, `section`, and `footer` where appropriate.
- Preserve a logical heading hierarchy.
- Use buttons for actions and links for navigation.
- Associate labels with form controls.
- Use lists for repeated navigation or collection structures where appropriate.

## Keyboard and focus

- Ensure all interactive controls are keyboard reachable.
- Provide visible focus treatment. Match the reference when it includes focus styling; otherwise use a minimally intrusive accessible treatment.
- Trap and restore focus for modal dialogs.
- Support Escape for dismissible overlays.

## Images and icons

- Write meaningful alt text for informative images.
- Use empty alt text for decorative images.
- Hide decorative SVG icons from assistive technology.
- Give icon-only buttons accessible names.

## Motion

Respect `prefers-reduced-motion`. A reduced-motion mode may simplify animation while preserving the static visual state.

## Contrast

Do not silently recolor the entire design. When visible colors create a serious contrast problem, preserve the reference by default, mention the issue, and propose an optional accessible variant unless the user explicitly prioritizes compliance over exactness.

## Responsive interaction

Maintain usable target sizes and avoid interactions that depend only on hover on touch devices.

## Behavior fidelity

When the reference demonstrates behavior, match it. When it does not, choose standard accessible behavior and label the inference.
