# Exact UI Replica Skill

A portable Agent Skill that turns UI screenshots, MVP images, mockups, and existing pages into:

- an implementation-ready master coding prompt;
- a measured UI design and implementation contract;
- a high-fidelity working frontend;
- or a scoped visual repair with screenshot-difference evidence.

## Operating modes

| Mode | Use it when | Main deliverable |
|---|---|---|
| Prompt | You need a detailed prompt for Codex, Claude Code, Cursor-like agents, Copilot, or another coding AI | Master build prompt + implementation contract |
| Build | You want the agent to code the interface | Working page + verification artifacts |
| Repair | Existing code is close but visually wrong | Baseline, scoped fixes, before/after comparison |
| Hybrid | You need the contract/prompt and the implementation | Both prompt and verified build |

## Why it is different

The skill does not stop at “make it pixel-perfect.” It enforces a repeatable sequence:

1. isolate the correct screen or concept;
2. inventory reference dimensions and states;
3. audit the repository and preserve its stack;
4. extract layout, typography, tokens, assets, states, and responsive rules;
5. create an implementation contract;
6. generate the master prompt or implement directly;
7. capture at exact viewports;
8. compare reference and render;
9. correct high-impact mismatches;
10. report evidence, assumptions, substitutions, and remaining differences.

## Package structure

```text
exact-ui-replica/
├── SKILL.md
├── skill.json
├── VERSION
├── CHANGELOG.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── adapters/
│   ├── codex.md
│   ├── claude-code.md
│   └── generic-agent-skills.md
├── references/
├── assets/
├── scripts/
├── examples/
└── evals/
```

## Install

### Codex — repository scope

```bash
python3 scripts/install_skill.py --target codex-project --project /path/to/repository
```

### Codex — user scope

```bash
python3 scripts/install_skill.py --target codex-user
```

### Claude Code — project scope

```bash
python3 scripts/install_skill.py --target claude-project --project /path/to/repository
```

### Claude Code — personal scope

```bash
python3 scripts/install_skill.py --target claude-user
```

### Other Agent Skills-compatible clients

```bash
python3 scripts/install_skill.py --target generic --destination /path/to/client/skills
```

The skill follows the open Agent Skills folder format. Tool permissions and discovery locations still vary by client, so “portable” means compatible with clients that implement the standard or can load a `SKILL.md` bundle.

## Validate the package

```bash
python3 scripts/validate_skill.py .
```

## Optional verification dependencies

### Python

```bash
python3 -m pip install -r scripts/requirements.txt
```

### Browser capture

```bash
cd scripts
npm install
npx playwright install chromium
```

## Example: generate the master prompt

```text
Use exact-ui-replica in Prompt mode. Analyse the attached Lazercroft desktop MVP, isolate the hero and collection rail, and generate a complete implementation prompt for an existing Vite project. Include measured geometry, fonts, colors, icons, responsive transformations, interactions, libraries, file structure, visual verification commands, and objective acceptance criteria. Do not redesign it.
```

## Example: build directly

```text
Use exact-ui-replica in Build mode. Recreate the supplied 1440 × 1024 dashboard at /dashboard in the existing Next.js project. Preserve CSS Modules, implement all visible controls, and verify at 1440 × 1024 and 390 × 844.
```

## Example: repair existing code

```text
Use exact-ui-replica in Repair mode. The current /discover page is close to the attached reference. Capture a baseline, fix only visual differences, preserve API behavior, compare again, and report before/after metrics.
```

## Included tools

| Script | Purpose |
|---|---|
| `inspect_image.py` | Dimensions, transparency, and dominant colors |
| `audit_project.py` | Framework, package manager, styling, icons, fonts, tests, and likely routes |
| `capture_page.mjs` | Deterministic exact-viewport screenshot |
| `visual_diff.py` | Metrics, overlay, heatmap, mask, mismatch bounds, and regional diagnostics |
| `run_verification.py` | One-command capture and compare |
| `validate_skill.py` | Frontmatter, version, references, manifests, and eval validation |
| `install_skill.py` | Local Codex, Claude Code, or generic installation |

## Important limitation

A screenshot cannot expose every hidden state, original source asset, exact font file, breakpoint, backend behavior, or off-screen section. The skill therefore requires evidence labels and prevents unsupported “no difference” claims.

## Version

`0.2.0` — prompt-generation, direct-build, repair, portability, and deterministic verification release.
