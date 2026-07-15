#!/usr/bin/env python3
"""Inspect a UI reference image and emit deterministic JSON metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install with: python3 -m pip install -r scripts/requirements.txt"
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report dimensions, transparency, and dominant colors for a UI reference image."
    )
    parser.add_argument("image", type=Path, help="Path to PNG, JPEG, WEBP, or another Pillow-supported image")
    parser.add_argument(
        "--colors",
        type=int,
        default=12,
        help="Number of dominant colors to return (default: 12)",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    return parser.parse_args()


def inspect_image(path: Path, color_count: int) -> dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(f"Image does not exist: {path}")
    if color_count < 1 or color_count > 64:
        raise ValueError("--colors must be between 1 and 64")

    with Image.open(path) as source:
        source.load()
        original_mode = source.mode
        rgba = source.convert("RGBA")
        width, height = rgba.size
        alpha = rgba.getchannel("A")
        alpha_extrema = alpha.getextrema()
        has_transparency = alpha_extrema[0] < 255

        # Reduce resolution before quantization so large screenshots remain fast.
        sample = rgba.copy()
        sample.thumbnail((512, 512), Image.Resampling.LANCZOS)
        rgb = Image.new("RGB", sample.size, (255, 255, 255))
        rgb.paste(sample, mask=sample.getchannel("A"))
        quantized = rgb.quantize(colors=color_count, method=Image.Quantize.MEDIANCUT)
        palette = quantized.getpalette() or []
        counts = quantized.getcolors(maxcolors=color_count) or []
        total = max(1, sample.width * sample.height)

        dominant = []
        for count, index in sorted(counts, reverse=True):
            base = index * 3
            red, green, blue = palette[base : base + 3]
            dominant.append(
                {
                    "hex": f"#{red:02X}{green:02X}{blue:02X}",
                    "rgb": [red, green, blue],
                    "share": round(count / total, 6),
                }
            )

        return {
            "path": str(path.resolve()),
            "format": source.format,
            "mode": original_mode,
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 6) if height else None,
            "has_transparency": has_transparency,
            "alpha_range": list(alpha_extrema),
            "dominant_colors": dominant,
        }


def main() -> int:
    args = parse_args()
    try:
        result = inspect_image(args.image, args.colors)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2

    payload = json.dumps({"ok": True, "image": result}, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
