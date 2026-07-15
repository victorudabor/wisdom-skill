# UI Implementation Contract

## 1. Authority

- Primary reference:
- Secondary references:
- Target route:
- Authoritative viewport(s):
- Operating mode:

## 2. Evidence ledger

| Decision | Value | Confidence | Evidence/notes |
|---|---|---|---|
| Canvas width |  | Observed / Measured estimate / Inference |  |

## 3. Technology contract

- Framework/language:
- Styling system:
- Existing component system:
- Icon strategy:
- Animation/3D strategy:
- New dependencies permitted:
- Deployment constraints:

## 4. Global design tokens

```css
:root {
  --canvas: ;
  --surface: ;
  --text: ;
  --muted: ;
  --accent: ;
  --container-max: ;
  --gutter: ;
  --radius-sm: ;
  --radius-lg: ;
  --shadow-primary: ;
}
```

## 5. Typography

| Role | Family | Weight | Size | Line height | Tracking | Width/wrap | Confidence |
|---|---|---:|---:|---:|---:|---|---|

## 6. Visible copy

Record all readable text in visual order. Mark unreadable text and geometry-preserving placeholders.

## 7. Page anatomy

| Order | Section/component | Geometry | Alignment | Visual treatment | Behavior | Confidence |
|---:|---|---|---|---|---|---|

## 8. Component inventory

| Component | Repeats | Inputs/data | States | Responsive transformation | File candidate |
|---|---:|---|---|---|---|

## 9. Asset map

| Visual region | Required asset | Available source | Crop/mask | Fallback | Status |
|---|---|---|---|---|---|

## 10. Responsive transformation table

| Component | Wide | Desktop | Tablet | Mobile | Evidence |
|---|---|---|---|---|---|

## 11. Interaction and state table

| Control | Trigger | Result | States | Keyboard/focus | Evidence |
|---|---|---|---|---|---|

## 12. Implementation order

1. Canvas and page shell
2. Major geometry
3. Typography and wrapping
4. Assets and icons
5. Surfaces/effects
6. Interactions
7. Responsive behavior
8. Verification and correction

## 13. Verification contract

- Run command:
- URL:
- Screenshot viewports:
- Deterministic data/setup:
- Capture command:
- Diff command:
- Required iterations:

## 14. Acceptance criteria

- [ ] All visible regions exist.
- [ ] Major anchors align within documented tolerance.
- [ ] Primary copy and wrapping match.
- [ ] Assets/crops match or substitutions are disclosed.
- [ ] Supplied responsive states match.
- [ ] Visible interactions work.
- [ ] No unrelated regressions.
- [ ] Screenshot comparisons and report are produced.

## 15. Non-goals and prohibited changes

- 

## 16. Unresolved assumptions

- 
