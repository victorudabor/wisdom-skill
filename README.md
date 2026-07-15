# Wisdom

**Portable skills for AI coding agents.**

Wisdom installs expert workflows into Claude Code, Codex, and compatible AI coding tools. The first bundled skill is **Exact UI Replica**, an advanced screenshot-to-prompt, screenshot-to-code, and visual-repair skill.

## Quick start

From your project root, run:

```bash
npx wisdom-skills install
```

Wisdom will ask which AI coding tool to target and install the skill into the current project.

Then, inside your AI coding tool, say:

> Use Exact UI Replica to recreate this MVP exactly.

That is all.

## Non-interactive installation

Claude Code, current project:

```bash
npx wisdom-skills install --agent claude --scope project --yes
```

Codex, current project:

```bash
npx wisdom-skills install --agent codex --scope project --yes
```

All supported tools:

```bash
npx wisdom-skills install --agent all --scope project --yes
```

Global installation for every project:

```bash
npx wisdom-skills install --agent claude --scope user --yes
```

## Commands

```bash
npx wisdom-skills install
npx wisdom-skills update
npx wisdom-skills uninstall
npx wisdom-skills doctor
npx wisdom-skills list
```

## What gets installed

For Claude Code project scope:

```text
.claude/skills/exact-ui-replica/
```

For Codex project scope:

```text
.agents/skills/exact-ui-replica/
```

Global installation uses the equivalent folders in your home directory.

## Exact UI Replica

The bundled skill can:

- generate an implementation-ready master coding prompt from an MVP image;
- extract layout, spacing, typography, colors, icons, assets, and responsive rules;
- build a high-fidelity frontend in an existing project;
- repair an implementation against a visual reference;
- capture screenshots and calculate visual differences;
- produce a transparent fidelity report.

## Requirements

- Node.js 18 or newer
- Claude Code, Codex, or another compatible Agent Skills client

Visual verification may additionally use Python, Pillow, NumPy, Playwright, and Chromium.

## Full documentation

- [Installation and CLI guide](./docs/installation.md)
- [Exact UI Replica skill](./versions/v0.2.0/README.md)
- [Repository](https://github.com/victorudabor/wisdom-skill)

## Current release

- Wisdom CLI: `0.4.0`
- Exact UI Replica: `0.2.0`

## License

MIT © Maverp
