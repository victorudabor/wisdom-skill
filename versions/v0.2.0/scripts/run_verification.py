#!/usr/bin/env python3
"""Capture a local webpage and compare it with a reference screenshot."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run browser capture and visual comparison in one command.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--width", required=True, type=int)
    parser.add_argument("--height", required=True, type=int)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--selector")
    parser.add_argument("--wait-ms", type=int, default=500)
    parser.add_argument("--threshold", type=int, default=16)
    parser.add_argument("--full-page", action="store_true")
    parser.add_argument("--device-scale", type=float, default=1.0)
    parser.add_argument("--color-scheme", choices=["light", "dark", "no-preference"], default="no-preference")
    return parser.parse_args()


def run(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def main() -> int:
    args = parse_args()
    if args.width < 1 or args.height < 1:
        print(json.dumps({"ok": False, "error": "width and height must be positive"}, indent=2), file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parent
    args.output_dir.mkdir(parents=True, exist_ok=True)
    actual = args.output_dir / f"render-{args.width}x{args.height}.png"
    diff_dir = args.output_dir / f"diff-{args.width}x{args.height}"

    capture = [
        "node", str(root / "capture_page.mjs"), "--url", args.url,
        "--width", str(args.width), "--height", str(args.height),
        "--output", str(actual), "--wait-ms", str(args.wait_ms),
        "--device-scale", str(args.device_scale), "--color-scheme", args.color_scheme,
    ]
    if args.selector:
        capture += ["--selector", args.selector]
    if args.full_page:
        capture.append("--full-page")

    capture_result = run(capture)
    if capture_result["returncode"] != 0:
        summary = {"ok": False, "stage": "capture", "capture": capture_result}
        (args.output_dir / "verification-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2), file=sys.stderr)
        return 1

    compare = [
        sys.executable, str(root / "visual_diff.py"),
        "--reference", str(args.reference), "--actual", str(actual),
        "--output-dir", str(diff_dir), "--threshold", str(args.threshold),
    ]
    compare_result = run(compare)
    ok = compare_result["returncode"] == 0
    summary = {
        "ok": ok,
        "reference": str(args.reference.resolve()),
        "actual": str(actual.resolve()),
        "diff_dir": str(diff_dir.resolve()),
        "viewport": [args.width, args.height],
        "capture": capture_result,
        "compare": compare_result,
    }
    (args.output_dir / "verification-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2), file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
