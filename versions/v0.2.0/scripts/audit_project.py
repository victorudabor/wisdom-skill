#!/usr/bin/env python3
"""Audit a local codebase and emit a concise, deterministic JSON stack report."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

IGNORED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", ".next", "dist", "build",
    "coverage", ".cache", ".turbo", ".venv", "venv", "__pycache__", "storage",
}

MANIFESTS = [
    "package.json", "composer.json", "pyproject.toml", "requirements.txt", "Pipfile",
    "Gemfile", "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "build.gradle.kts",
]

LOCKFILES = {
    "pnpm-lock.yaml": "pnpm",
    "yarn.lock": "yarn",
    "package-lock.json": "npm",
    "bun.lock": "bun",
    "bun.lockb": "bun",
    "composer.lock": "composer",
    "poetry.lock": "poetry",
    "Pipfile.lock": "pipenv",
    "uv.lock": "uv",
}

FRAMEWORK_HINTS = {
    "next": "Next.js",
    "react": "React",
    "vue": "Vue",
    "nuxt": "Nuxt",
    "svelte": "Svelte",
    "@sveltejs/kit": "SvelteKit",
    "astro": "Astro",
    "vite": "Vite",
    "angular": "Angular",
    "@angular/core": "Angular",
    "laravel": "Laravel",
}

STYLE_HINTS = {
    "tailwindcss": "Tailwind CSS",
    "sass": "Sass",
    "less": "Less",
    "styled-components": "styled-components",
    "@emotion/react": "Emotion",
    "@mui/material": "Material UI",
    "@chakra-ui/react": "Chakra UI",
    "antd": "Ant Design",
    "bootstrap": "Bootstrap",
}

ICON_HINTS = {
    "lucide-react": "Lucide",
    "react-icons": "React Icons",
    "@heroicons/react": "Heroicons",
    "@fortawesome/fontawesome-free": "Font Awesome",
    "@fortawesome/react-fontawesome": "Font Awesome React",
    "phosphor-react": "Phosphor",
    "@phosphor-icons/react": "Phosphor",
}

TEST_HINTS = {
    "vitest": "Vitest",
    "jest": "Jest",
    "@playwright/test": "Playwright Test",
    "cypress": "Cypress",
    "@testing-library/react": "Testing Library",
    "phpunit/phpunit": "PHPUnit",
}

SCREENSHOT_HINTS = {
    "playwright": "Playwright",
    "@playwright/test": "Playwright Test",
    "puppeteer": "Puppeteer",
    "cypress": "Cypress",
    "loki": "Loki",
    "@storybook/test-runner": "Storybook Test Runner",
}

INSTRUCTION_FILES = [
    "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "README.md", ".cursorrules",
    ".github/copilot-instructions.md",
]

ROUTE_DIRS = ["app", "pages", "src/app", "src/pages", "routes", "src/routes"]
ENTRY_CANDIDATES = [
    "src/main.tsx", "src/main.jsx", "src/main.ts", "src/main.js", "src/App.tsx",
    "src/App.jsx", "app/page.tsx", "app/page.jsx", "pages/index.tsx", "pages/index.jsx",
    "index.html", "public/index.html", "artisan", "manage.py",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect a repository and report its likely stack and constraints.")
    parser.add_argument("project", type=Path, nargs="?", default=Path.cwd(), help="Project directory")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to inspect (default: 5000)")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def walk_files(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".pytest_cache"))
        for name in sorted(names):
            files.append(Path(current) / name)
            if len(files) >= max_files:
                return files
    return files


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def package_data(root: Path) -> tuple[dict[str, Any], dict[str, str]]:
    package = read_json(root / "package.json")
    dependencies: dict[str, str] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = package.get(key, {})
        if isinstance(value, dict):
            dependencies.update({str(k): str(v) for k, v in value.items()})
    return package, dependencies


def matches(dependencies: dict[str, str], hints: dict[str, str]) -> list[str]:
    found = []
    keys = set(dependencies)
    for package_name, label in hints.items():
        if package_name in keys and label not in found:
            found.append(label)
    return found


def detect_css(files: list[Path], root: Path) -> dict[str, Any]:
    extensions = {".css": 0, ".scss": 0, ".sass": 0, ".less": 0, ".styl": 0}
    modules = 0
    token_files: list[str] = []
    for path in files:
        suffix = path.suffix.lower()
        if suffix in extensions:
            extensions[suffix] += 1
        lower = path.name.lower()
        if ".module." in lower:
            modules += 1
        if any(term in lower for term in ("token", "theme", "variables", "design-system")) and suffix in extensions:
            token_files.append(rel(root, path))
    return {
        "file_counts": extensions,
        "css_modules_files": modules,
        "likely_token_files": token_files[:25],
    }


def detect_fonts(files: list[Path], root: Path) -> dict[str, Any]:
    font_files = [rel(root, p) for p in files if p.suffix.lower() in {".woff", ".woff2", ".ttf", ".otf"}]
    declarations: list[str] = []
    pattern = re.compile(r"font-family\s*:\s*([^;}{]+)", re.IGNORECASE)
    for path in files:
        if path.suffix.lower() not in {".css", ".scss", ".sass", ".less", ".html", ".tsx", ".jsx"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")[:250_000]
        except OSError:
            continue
        for match in pattern.findall(text):
            value = " ".join(match.split()).strip(" '\"")
            if value and value not in declarations:
                declarations.append(value)
            if len(declarations) >= 30:
                break
        if len(declarations) >= 30:
            break
    return {"local_files": font_files[:50], "declared_families": declarations}


def detect_composer(root: Path) -> tuple[dict[str, Any], dict[str, str]]:
    composer = read_json(root / "composer.json")
    dependencies: dict[str, str] = {}
    for key in ("require", "require-dev"):
        value = composer.get(key, {})
        if isinstance(value, dict):
            dependencies.update({str(k): str(v) for k, v in value.items()})
    return composer, dependencies


def audit(root: Path, max_files: int) -> dict[str, Any]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {root}")

    files = walk_files(root, max_files)
    package, node_deps = package_data(root)
    composer, php_deps = detect_composer(root)

    package_managers = [manager for filename, manager in LOCKFILES.items() if (root / filename).exists()]
    if (root / "package.json").exists() and not any(pm in package_managers for pm in ("npm", "yarn", "pnpm", "bun")):
        package_managers.append("npm-or-compatible")

    frameworks = matches(node_deps, FRAMEWORK_HINTS)
    if "laravel/framework" in php_deps:
        frameworks.append("Laravel")
    if (root / "artisan").exists() and "Laravel" not in frameworks:
        frameworks.append("Laravel")

    manifests = [name for name in MANIFESTS if (root / name).exists()]
    instructions = [name for name in INSTRUCTION_FILES if (root / name).exists()]
    route_dirs = [name for name in ROUTE_DIRS if (root / name).is_dir()]
    entries = [name for name in ENTRY_CANDIDATES if (root / name).exists()]

    scripts = package.get("scripts", {}) if isinstance(package.get("scripts", {}), dict) else {}
    likely_commands = {
        key: value for key, value in scripts.items()
        if any(term in key.lower() for term in ("dev", "start", "build", "test", "lint", "type", "preview", "storybook"))
    }

    return {
        "ok": True,
        "project": str(root),
        "files_scanned": len(files),
        "scan_truncated": len(files) >= max_files,
        "manifests": manifests,
        "package_managers": package_managers,
        "frameworks_and_build_tools": frameworks,
        "styling": matches(node_deps, STYLE_HINTS),
        "icons": matches(node_deps, ICON_HINTS),
        "tests": sorted(set(matches(node_deps, TEST_HINTS) + matches(php_deps, TEST_HINTS))),
        "screenshot_and_browser_tools": matches(node_deps, SCREENSHOT_HINTS),
        "instructions": instructions,
        "route_directories": route_dirs,
        "entry_candidates": entries,
        "package_scripts": likely_commands,
        "css": detect_css(files, root),
        "fonts": detect_fonts(files, root),
        "notable_config": [
            rel(root, p) for p in files
            if p.name in {
                "vite.config.ts", "vite.config.js", "next.config.js", "next.config.mjs",
                "tailwind.config.js", "tailwind.config.ts", "tsconfig.json", "eslint.config.js",
                "playwright.config.ts", "playwright.config.js", "vercel.json", "netlify.toml",
            }
        ][:50],
        "dependency_counts": {"node": len(node_deps), "php": len(php_deps)},
        "notes": [
            "This is a heuristic audit. Confirm findings by reading the relevant manifests and project instructions.",
            "Do not install or replace libraries solely because they appear in this report.",
        ],
    }


def main() -> int:
    args = parse_args()
    try:
        result = audit(args.project, args.max_files)
    except (ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    payload = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
