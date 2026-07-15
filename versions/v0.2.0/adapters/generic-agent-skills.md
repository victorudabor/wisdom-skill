# Generic Agent Skills Installation

For an Agent Skills-compatible client, copy the complete directory into the client’s documented skills discovery directory. Keep `SKILL.md`, `references/`, `assets/`, and `scripts/` together.

```bash
python3 scripts/install_skill.py --target generic --destination /path/to/client/skills
```

Clients may differ in tool permissions, image access, shell execution, and automatic invocation. The instruction-only Prompt mode remains usable even when browser capture or code execution is unavailable.
