#!/usr/bin/env python3
"""Compare reference and rendered UI screenshots and create visual diagnostics."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image, ImageChops, ImageEnhance
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow and NumPy are required. Install with: "
        "python3 -m pip install -r scripts/requirements.txt"
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two screenshots and write metrics, overlay, heatmap, and absolute diff files."
    )
    parser.add_argument("--reference", required=True, type=Path, help="Reference screenshot")
    parser.add_argument("--actual", required=True, type=Path, help="Rendered screenshot")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for comparison artifacts")
    parser.add_argument(
        "--threshold",
        type=int,
        default=16,
        help="Per-channel absolute-difference threshold used for differing-pixel percentage (0-255, default: 16)",
    )
    parser.add_argument(
        "--resize-actual",
        action="store_true",
        help="Resize actual to the reference dimensions before comparison; use only for diagnostics",
    )
    return parser.parse_args()


def load_rgb(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(f"Image does not exist: {path}")
    with Image.open(path) as image:
        image.load()
        return image.convert("RGB")


def global_ssim(reference: np.ndarray, actual: np.ndarray) -> float:
    """Compute a simple global SSIM approximation over all RGB samples."""
    ref = reference.astype(np.float64)
    act = actual.astype(np.float64)
    mu_x = ref.mean()
    mu_y = act.mean()
    sigma_x = ref.var()
    sigma_y = act.var()
    covariance = ((ref - mu_x) * (act - mu_y)).mean()
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2
    numerator = (2 * mu_x * mu_y + c1) * (2 * covariance + c2)
    denominator = (mu_x**2 + mu_y**2 + c1) * (sigma_x + sigma_y + c2)
    return float(numerator / denominator) if denominator else 1.0


def make_heatmap(diff_array: np.ndarray) -> Image.Image:
    magnitude = diff_array.max(axis=2).astype(np.uint8)
    red = magnitude
    green = np.clip(magnitude.astype(np.int16) * 0.35, 0, 255).astype(np.uint8)
    blue = np.zeros_like(magnitude)
    alpha = np.where(magnitude > 0, np.clip(magnitude.astype(np.int16) * 2, 32, 255), 0).astype(np.uint8)
    rgba = np.dstack([red, green, blue, alpha])
    return Image.fromarray(rgba, mode="RGBA")


def compare(args: argparse.Namespace) -> dict[str, object]:
    if not 0 <= args.threshold <= 255:
        raise ValueError("--threshold must be between 0 and 255")

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

    mae = float(diff_array.mean())
    rmse = float(math.sqrt(np.mean(np.square(diff_array.astype(np.float64)))))
    max_channel_diff = int(diff_array.max())
    per_pixel_max = diff_array.max(axis=2)
    differing_pixel_share = float(np.mean(per_pixel_max > args.threshold))
    exact_pixel_share = float(np.mean(per_pixel_max == 0))
    similarity = global_ssim(ref_array, act_array)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    absolute_diff = ImageChops.difference(reference, actual)
    enhanced_diff = ImageEnhance.Contrast(absolute_diff).enhance(2.0)
    overlay = Image.blend(reference, actual, alpha=0.5)
    heatmap = make_heatmap(diff_array)

    absolute_diff.save(args.output_dir / "absolute-diff.png")
    enhanced_diff.save(args.output_dir / "enhanced-diff.png")
    overlay.save(args.output_dir / "overlay.png")
    heatmap.save(args.output_dir / "heatmap.png")

    metrics = {
        "reference": str(args.reference.resolve()),
        "actual": str(args.actual.resolve()),
        "reference_size": list(reference.size),
        "original_actual_size": list(original_actual_size),
        "comparison_size": list(actual.size),
        "resized_actual": original_actual_size != actual.size,
        "threshold": args.threshold,
        "mean_absolute_error": round(mae, 6),
        "root_mean_square_error": round(rmse, 6),
        "max_channel_difference": max_channel_diff,
        "differing_pixel_share": round(differing_pixel_share, 8),
        "differing_pixel_percent": round(differing_pixel_share * 100, 4),
        "exact_pixel_share": round(exact_pixel_share, 8),
        "global_ssim_approximation": round(similarity, 8),
        "notes": [
            "Metrics are affected by font rendering, browser engine, anti-aliasing, compression, and device scale.",
            "Use overlay and heatmap files to classify mismatches before changing code.",
        ],
    }
    (args.output_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )
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
