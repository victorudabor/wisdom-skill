# Wisdom installation guide

## Interactive quick start

Run this from the root of the project where you want the skill:

```bash
npx wisdom install
```

Choose an AI tool and installation scope. Project scope is recommended because it keeps the skill versioned with the codebase and visible to collaborators.

## CLI options

| Option | Values | Purpose |
|---|---|---|
| `--agent` | `claude`, `codex`, `all` | Select the AI coding tool |
| `--scope` | `project`, `user` | Install locally or globally |
| `--version` | `latest`, `0.2.0` | Select a bundled skill version |
| `--project` | filesystem path | Use a project other than the current directory |
| `--force` | flag | Replace an existing installation |
| `--yes` | flag | Skip interactive questions |
| `--json` | flag | Return machine-readable output |

## Updating

```bash
npx wisdom update --agent claude --scope project --yes
```

## Removing

```bash
npx wisdom uninstall --agent claude --scope project --yes
```

## Diagnosing

```bash
npx wisdom doctor
```

This reports detected agent folders, available skill versions, and existing installations.

## Using the installed skill

After installation, restart or reopen the AI coding tool if it does not immediately discover new skills. Then write a natural request such as:

```text
Use Exact UI Replica in Hybrid mode. Analyse the attached MVP, create the implementation contract and master build prompt, then build the page in this repository and verify it against the reference.
```
