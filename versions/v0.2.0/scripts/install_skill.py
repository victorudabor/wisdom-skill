#!/usr/bin/env python3
"""Install this skill into common Agent Skills discovery directories."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SKILL_NAME = "exact-ui-replica"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install Exact UI Replica into a supported local skill directory.")
    parser.add_argument(
        "--target",
        required=True,
        choices=["codex-user", "codex-project", "claude-user", "claude-project", "generic"],
    )
    parser.add_argument("--project", type=Path, help="Project root for project-scoped targets")
    parser.add_argument("--destination", type=Path, help="Skills parent directory for the generic target")
    parser.add_argument("--force", action="store_true", help="Replace an existing installation")
    parser.add_argument("--dry-run", action="store_true", help="Print destination without copying")
    return parser.parse_args()


def destination(args: argparse.Namespace) -> Path:
    home = Path.home()
    if args.target == "codex-user":
        return home / ".agents" / "skills" / SKILL_NAME
    if args.target == "claude-user":
        return home / ".claude" / "skills" / SKILL_NAME
    if args.target == "codex-project":
        if not args.project:
            raise ValueError("--project is required for codex-project")
        return args.project.expanduser().resolve() / ".agents" / "skills" / SKILL_NAME
    if args.target == "claude-project":
        if not args.project:
            raise ValueError("--project is required for claude-project")
        return args.project.expanduser().resolve() / ".claude" / "skills" / SKILL_NAME
    if not args.destination:
        raise ValueError("--destination is required for generic")
    return args.destination.expanduser().resolve() / SKILL_NAME


def ignore(_directory: str, names: list[str]) -> set[str]:
    blocked = {"__pycache__", ".DS_Store", ".git", ".pytest_cache"}
    return {name for name in names if name in blocked or name.endswith(".pyc")}


def main() -> int:
    args = parse_args()
    source = Path(__file__).resolve().parents[1]
    try:
        target = destination(args)
        if source == target or source in target.parents:
            raise ValueError("Refusing to install the skill inside itself")
        if args.dry_run:
            print(json.dumps({"ok": True, "dry_run": True, "source": str(source), "destination": str(target)}, indent=2))
            return 0
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if not args.force:
                raise FileExistsError(f"Destination already exists: {target}. Use --force to replace it.")
            shutil.rmtree(target)
        shutil.copytree(source, target, ignore=ignore)
        print(json.dumps({"ok": True, "source": str(source), "destination": str(target), "target": args.target}, indent=2))
        return 0
    except (ValueError, FileExistsError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
