#!/usr/bin/env python3
"""Validate the local skill package without third-party YAML dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"`((?:assets|references|scripts|agents|adapters|evals)/[^`]+)`")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an Agent Skills package and Exact UI Replica metadata.")
    parser.add_argument("skill", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    return parser.parse_args()


def parse_frontmatter(text: str) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, ["SKILL.md frontmatter is not closed"]
    block = text[4:end]
    data: dict[str, Any] = {}
    current_map: dict[str, Any] | None = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  ") and current_map is not None and ":" in raw:
            key, value = raw.strip().split(":", 1)
            current_map[key.strip()] = value.strip().strip('"\'')
            continue
        if ":" not in raw:
            errors.append(f"Unparsed frontmatter line: {raw}")
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            data[key] = {}
            current_map = data[key]
        else:
            data[key] = value.strip('"\'')
            current_map = None
    return data, errors


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing required file: {path.name}")
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path.name}: {exc}")
    return {}


def validate(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        errors.append("Missing SKILL.md")
        text = ""
        frontmatter = {}
    else:
        text = skill_path.read_text(encoding="utf-8")
        frontmatter, fm_errors = parse_frontmatter(text)
        errors.extend(fm_errors)

    name = str(frontmatter.get("name", ""))
    description = str(frontmatter.get("description", ""))
    if not name:
        errors.append("Frontmatter name is required")
    elif len(name) > 64 or not NAME_RE.fullmatch(name):
        errors.append("Frontmatter name must be <=64 chars and use lowercase letters, numbers, and hyphens")
    if not description:
        errors.append("Frontmatter description is required")
    elif len(description) > 1024:
        errors.append("Frontmatter description exceeds 1024 characters")

    compatibility = str(frontmatter.get("compatibility", ""))
    if len(compatibility) > 500:
        errors.append("Frontmatter compatibility exceeds 500 characters")

    line_count = len(text.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md has {line_count} lines; consider keeping it under 500")

    manifest = load_json(root / "skill.json", errors)
    evals = load_json(root / "evals" / "evals.json", errors)

    version_file = root / "VERSION"
    version = version_file.read_text(encoding="utf-8").strip() if version_file.exists() else ""
    fm_version = ""
    metadata = frontmatter.get("metadata")
    if isinstance(metadata, dict):
        fm_version = str(metadata.get("version", ""))
    versions = {
        "VERSION": version,
        "SKILL.md": fm_version,
        "skill.json": str(manifest.get("version", "")),
    }
    present_versions = {value for value in versions.values() if value}
    if len(present_versions) > 1:
        errors.append(f"Version mismatch: {versions}")
    if not version:
        warnings.append("VERSION file is missing or empty")

    required_dirs = ["assets", "references", "scripts", "evals"]
    for directory in required_dirs:
        if not (root / directory).is_dir():
            errors.append(f"Missing directory: {directory}/")

    referenced = sorted(set(LINK_RE.findall(text)))
    for item in referenced:
        clean = item.split()[0].rstrip(".,;:")
        if not (root / clean).exists():
            errors.append(f"SKILL.md references missing path: {clean}")

    eval_items = evals.get("evals", []) if isinstance(evals, dict) else []
    if not isinstance(eval_items, list) or not eval_items:
        warnings.append("No evaluation cases found")
    else:
        ids: set[Any] = set()
        for index, case in enumerate(eval_items, start=1):
            if not isinstance(case, dict):
                errors.append(f"Eval #{index} is not an object")
                continue
            case_id = case.get("id")
            if case_id in ids:
                errors.append(f"Duplicate eval id: {case_id}")
            ids.add(case_id)
            for field in ("prompt", "expected_output"):
                if not case.get(field):
                    errors.append(f"Eval {case_id} missing {field}")
            for filename in case.get("files", []) or []:
                if not (root / filename).exists():
                    errors.append(f"Eval {case_id} references missing file: {filename}")

    scripts = sorted(p.name for p in (root / "scripts").glob("*.*") if p.is_file()) if (root / "scripts").exists() else []
    return {
        "ok": not errors,
        "root": str(root),
        "name": name,
        "version": version or fm_version or manifest.get("version"),
        "skill_lines": line_count,
        "referenced_paths_checked": len(referenced),
        "eval_count": len(eval_items) if isinstance(eval_items, list) else 0,
        "scripts": scripts,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    args = parse_args()
    result = validate(args.skill)
    payload = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    stream = sys.stdout if result["ok"] else sys.stderr
    print(payload, file=stream)
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
