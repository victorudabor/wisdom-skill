# Exact UI Replica Skill

A portable Agent Skill for reconstructing supplied UI screenshots, MVP images, mockups, and visual references as high-fidelity working frontends.

## What it does

The skill gives an AI coding agent a disciplined screenshot-to-code workflow:

1. inventory and inspect reference images;
2. audit the existing repository and preserve its stack;
3. extract layout, typography, color, spacing, effects, icons, and assets;
4. create a component and implementation plan;
5. build the interface in fidelity-first order;
6. reconstruct responsive behavior;
7. capture the implementation at exact viewports;
8. calculate visual-difference metrics;
9. correct mismatches iteratively;
10. produce a transparent fidelity report.

## Package structure

```text
exact-ui-replica/
├── SKILL.md
├── skill.json
├── README.md
├── LICENSE
├── references/
├── scripts/
├── assets/
└── evals/
```

## Installation

Install the entire `exact-ui-replica` directory in the skill directory supported by your AI coding agent. For repository-scoped Codex use, place it under:

```text
.agents/skills/exact-ui-replica/
```

For user-scoped Codex use, place it under:

```text
~/.agents/skills/exact-ui-replica/
```

Other skills-compatible agents may use a different discovery directory. Keep the internal package structure unchanged.

## Optional verification dependencies

### Python tools

```bash
python3 -m pip install -r scripts/requirements.txt
```

### Browser capture

```bash
cd scripts
npm install
npx playwright install chromium
```

## Example invocation

```text
Use the exact-ui-replica skill to rebuild the supplied 1440 × 1024 MVP screenshot in this existing React project. Preserve the current stack, create the page at /discover, and verify it against the reference at 1440 × 1024 and 390 × 844.
```

## Important limitation

A static screenshot does not expose all source assets, font files, interactions, states, breakpoints, or off-screen content. This skill therefore targets measured high fidelity and requires unresolved assumptions to be reported instead of claiming unsupported perfection.

## Version

`0.1.0` — foundation package.
