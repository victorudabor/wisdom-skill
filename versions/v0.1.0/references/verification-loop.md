# Visual Verification Loop

Visual fidelity requires a repeatable render-and-compare process.

## Prepare deterministic conditions

Before capturing:

- use the exact viewport dimensions;
- set a consistent device scale factor where possible;
- wait for web fonts and images;
- disable or freeze non-essential animation;
- use deterministic data;
- set the expected route and scroll position;
- dismiss development overlays;
- avoid browser extensions or UI chrome in the capture.

## Capture

Use the project’s existing visual-regression tooling when available. Otherwise use:

```bash
node scripts/capture_page.mjs \
  --url http://127.0.0.1:3000/target \
  --width 1440 \
  --height 1024 \
  --output artifacts/render-1440x1024.png
```

## Compare

```bash
python3 scripts/visual_diff.py \
  --reference references/mvp-1440x1024.png \
  --actual artifacts/render-1440x1024.png \
  --output-dir artifacts/diff-1440x1024
```

The script creates:

- `metrics.json`;
- `overlay.png`;
- `heatmap.png`;
- `absolute-diff.png`.

Metrics are diagnostic, not proof of perceptual equivalence. Anti-aliasing, font rendering, browser engines, image compression, and device scale can produce pixel differences even when the layout is visually close.

## Correct mismatches in impact order

1. missing or extra regions;
2. wrong page or section dimensions;
3. wrong container edges and alignment;
4. wrong text wrapping or font metrics;
5. wrong image crop or asset;
6. wrong spacing and control sizing;
7. wrong colors, borders, shadows, and effects;
8. icon and micro-detail differences;
9. anti-aliasing-only differences.

## Classify before changing

For each major diff region, classify it:

- geometry;
- typography;
- content;
- asset;
- color;
- surface/effect;
- state;
- timing/animation;
- rendering-environment noise.

Avoid random CSS tweaking. Change the rule that explains the mismatch.

## Overlay inspection

A 50/50 overlay reveals doubled edges and text. Use it to find:

- vertical or horizontal offset;
- incorrect scale;
- container-width mismatch;
- line-height mismatch;
- wrong image focal point;
- missing elements.

## Suggested stopping criteria

Stop when:

- all visible elements are present;
- major anchors align within the documented tolerance;
- primary text wraps correctly;
- remaining differences are low-impact or caused by unavailable source assets/rendering differences;
- all remaining differences are documented.

Do not endlessly optimize imperceptible anti-aliasing differences while functional issues remain.
