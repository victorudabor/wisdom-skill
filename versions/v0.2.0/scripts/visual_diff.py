#!/usr/bin/env python3
"""Compare UI screenshots and create visual and regional diagnostics."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image, ImageChops, ImageDraw, ImageEnhance
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow and NumPy are required. Install with: python3 -m pip install -r scripts/requirements.txt"
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two screenshots and write visual diagnostics and JSON metrics.")
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--actual", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--threshold", type=int, default=16, help="Per-channel threshold for changed pixels (default: 16)")
    parser.add_argument("--resize-actual", action="store_true", help="Resize actual for diagnostics only")
    parser.add_argument("--grid", type=int, default=4, help="Regional metric grid size from 1 to 12 (default: 4)")
    parser.add_argument("--ignore-border", type=int, default=0, help="Ignore this many pixels around all edges")
    return parser.parse_args()


def load_rgb(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(f"Image does not exist: {path}")
    with Image.open(path) as image:
        image.load()
        return image.convert("RGB")


def global_ssim(reference: np.ndarray, actual: np.ndarray) -> float:
    ref = reference.astype(np.float64)
    act = actual.astype(np.float64)
    mu_x, mu_y = ref.mean(), act.mean()
    sigma_x, sigma_y = ref.var(), act.var()
    covariance = ((ref - mu_x) * (act - mu_y)).mean()
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    denominator = (mu_x**2 + mu_y**2 + c1) * (sigma_x + sigma_y + c2)
    return float(((2 * mu_x * mu_y + c1) * (2 * covariance + c2)) / denominator) if denominator else 1.0


def make_heatmap(diff_array: np.ndarray) -> Image.Image:
    magnitude = diff_array.max(axis=2).astype(np.uint8)
    red = magnitude
    green = np.clip(magnitude.astype(np.int16) * 0.35, 0, 255).astype(np.uint8)
    blue = np.zeros_like(magnitude)
    alpha = np.where(magnitude > 0, np.clip(magnitude.astype(np.int16) * 2, 32, 255), 0).astype(np.uint8)
    return Image.fromarray(np.dstack([red, green, blue, alpha]).astype(np.uint8), mode="RGBA")


def mismatch_bounds(mask: np.ndarray) -> list[int] | None:
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def regional_metrics(diff: np.ndarray, mask: np.ndarray, grid: int) -> list[dict[str, object]]:
    height, width = mask.shape
    regions: list[dict[str, object]] = []
    for row in range(grid):
        y0 = round(row * height / grid)
        y1 = round((row + 1) * height / grid)
        for col in range(grid):
            x0 = round(col * width / grid)
            x1 = round((col + 1) * width / grid)
            region_diff = diff[y0:y1, x0:x1]
            region_mask = mask[y0:y1, x0:x1]
            if region_mask.size == 0:
                continue
            regions.append({
                "row": row,
                "column": col,
                "bounds": [x0, y0, x1, y1],
                "mean_absolute_error": round(float(region_diff.mean()), 6),
                "differing_pixel_percent": round(float(region_mask.mean()) * 100, 4),
            })
    return sorted(regions, key=lambda item: (item["differing_pixel_percent"], item["mean_absolute_error"]), reverse=True)


def compare(args: argparse.Namespace) -> dict[str, object]:
    if not 0 <= args.threshold <= 255:
        raise ValueError("--threshold must be between 0 and 255")
    if not 1 <= args.grid <= 12:
        raise ValueError("--grid must be between 1 and 12")
    if args.ignore_border < 0:
        raise ValueError("--ignore-border must be zero or greater")

    reference = load_rgb(args.reference)
    actual = load_rgb(args.actual)
    original_actual_size = actual.size
    if actual.size != reference.size:
        if not args.resize_actual:
            raise ValueError(
                f"Image sizes differ: reference={reference.size}, actual={actual.size}. "
                "Capture the correct viewport or pass --resize-actual for diagnostics."
            )
        actual = actual.resize(reference.size, Image.Resampling.LANCZOS)

    ref_array = np.asarray(reference, dtype=np.int16)
    act_array = np.asarray(actual, dtype=np.int16)
    diff_array = np.abs(ref_array - act_array)
    per_pixel_max = diff_array.max(axis=2)
    mask = per_pixel_max > args.threshold

    if args.ignore_border:
        border = args.ignore_border
        if border * 2 >= min(mask.shape):
            raise ValueError("--ignore-border is too large for the image")
        mask[:border, :] = False
        mask[-border:, :] = False
        mask[:, :border] = False
        mask[:, -border:] = False
        diff_array[:border, :, :] = 0
        diff_array[-border:, :, :] = 0
        diff_array[:, :border, :] = 0
        diff_array[:, -border:, :] = 0
        per_pixel_max = diff_array.max(axis=2)

    mae = float(diff_array.mean())
    rmse = float(math.sqrt(np.mean(np.square(diff_array.astype(np.float64)))))
    exact_pixel_share = float(np.mean(per_pixel_max == 0))
    differing_pixel_share = float(np.mean(mask))
    similarity = global_ssim(ref_array, act_array)
    bounds = mismatch_bounds(mask)

    row_scores = mask.mean(axis=1)
    col_scores = mask.mean(axis=0)
    top_rows = np.argsort(row_scores)[::-1][:10]
    top_cols = np.argsort(col_scores)[::-1][:10]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    absolute_diff = ImageChops.difference(reference, actual)
    enhanced_diff = ImageEnhance.Contrast(absolute_diff).enhance(2.0)
    overlay = Image.blend(reference, actual, alpha=0.5)
    heatmap = make_heatmap(diff_array)
    mask_image = Image.fromarray((mask.astype(np.uint8) * 255), mode="L")

    annotated = actual.copy()
    draw = ImageDraw.Draw(annotated)
    if bounds:
        draw.rectangle(bounds, outline=(255, 0, 0), width=max(2, reference.width // 500))

    absolute_diff.save(args.output_dir / "absolute-diff.png")
    enhanced_diff.save(args.output_dir / "enhanced-diff.png")
    overlay.save(args.output_dir / "overlay.png")
    heatmap.save(args.output_dir / "heatmap.png")
    mask_image.save(args.output_dir / "diff-mask.png")
    annotated.save(args.output_dir / "annotated-mismatch.png")

    regions = regional_metrics(diff_array, mask, args.grid)
    metrics = {
        "reference": str(args.reference.resolve()),
        "actual": str(args.actual.resolve()),
        "reference_size": list(reference.size),
        "original_actual_size": list(original_actual_size),
        "comparison_size": list(actual.size),
        "resized_actual": original_actual_size != actual.size,
        "threshold": args.threshold,
        "ignore_border": args.ignore_border,
        "mean_absolute_error": round(mae, 6),
        "root_mean_square_error": round(rmse, 6),
        "max_channel_difference": int(diff_array.max()),
        "differing_pixel_share": round(differing_pixel_share, 8),
        "differing_pixel_percent": round(differing_pixel_share * 100, 4),
        "exact_pixel_share": round(exact_pixel_share, 8),
        "global_ssim_approximation": round(similarity, 8),
        "mismatch_bounds": bounds,
        "top_mismatch_rows": [{"y": int(y), "share": round(float(row_scores[y]), 6)} for y in top_rows if row_scores[y] > 0],
        "top_mismatch_columns": [{"x": int(x), "share": round(float(col_scores[x]), 6)} for x in top_cols if col_scores[x] > 0],
        "regional_grid": args.grid,
        "highest_mismatch_regions": regions[: min(12, len(regions))],
        "artifacts": [
            "metrics.json", "overlay.png", "heatmap.png", "absolute-diff.png",
            "enhanced-diff.png", "diff-mask.png", "annotated-mismatch.png",
        ],
        "notes": [
            "Metrics are affected by font rendering, browser engine, anti-aliasing, compression, and device scale.",
            "Use mismatch bounds and regional diagnostics to locate high-impact differences before changing code.",
            "Global SSIM is an approximation, not a standards-compliant local-window SSIM implementation.",
        ],
    }
    (args.output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics


def main() -> int:
    args = parse_args()
    try:
        metrics = compare(args)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, "metrics": metrics}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
