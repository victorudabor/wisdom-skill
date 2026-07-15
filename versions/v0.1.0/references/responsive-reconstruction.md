# Responsive Reconstruction

## Evidence hierarchy

Use responsive evidence in this order:

1. supplied references for the exact viewport;
2. existing implementation behavior;
3. supplied design files or specifications;
4. repeated alignment and content-priority clues;
5. conservative standard behavior.

## Multiple supplied viewports

When desktop, tablet, and mobile references exist:

- implement each supplied viewport as an explicit target;
- identify which elements resize, wrap, reorder, collapse, hide, scroll, or change alignment;
- derive breakpoints from actual failure points and observed transitions;
- compare screenshots at every authoritative viewport;
- test intermediate widths for discontinuities.

## One supplied viewport

When only one reference exists:

- make that viewport authoritative;
- retain content priority;
- prefer wrapping and stacking before hiding meaningful content;
- convert dense navigation to an accessible mobile pattern only when necessary;
- preserve image focal points;
- avoid arbitrary breakpoint proliferation;
- label mobile behavior as inferred.

## Common transformation types

Record transformations per component:

- **Scale:** font, image, or spacing changes continuously.
- **Wrap:** content moves to a new line or row.
- **Stack:** columns become vertical.
- **Reorder:** visual order changes while semantic order remains sensible.
- **Collapse:** navigation, filters, or secondary controls move behind a trigger.
- **Scroll:** rails remain horizontal with overflow.
- **Hide:** decorative or genuinely secondary content disappears.
- **Replace:** desktop control becomes a mobile equivalent.
- **Crop:** image focal point or mask changes.

## Breakpoint selection

Do not choose breakpoints solely because a framework provides them. Add a breakpoint where the composition fails or where a supplied reference proves a state change.

## Mobile quality checks

Verify:

- no horizontal page overflow;
- primary text is readable without zoom;
- touch targets are usable;
- fixed controls do not cover content;
- headings do not create isolated words unless the reference does;
- image focal points remain intentional;
- dialogs and menus fit the viewport;
- sticky elements do not consume excessive height;
- keyboard focus remains visible.

## Wide-screen behavior

Determine whether the reference implies:

- a fixed max-width container;
- expanding side gutters;
- full-bleed media;
- fluid columns;
- fixed central composition;
- intentional off-canvas decoration.

Do not stretch a composition that is visibly designed to remain bounded.
