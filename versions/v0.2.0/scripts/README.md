# Script Reference

All tools return JSON and use non-zero exit codes for failures.

## Inspect an image

```bash
python3 scripts/inspect_image.py reference.png --colors 16
```

## Audit a repository

```bash
python3 scripts/audit_project.py /path/to/project --output artifacts/project-audit.json
```

## Capture a page

```bash
node scripts/capture_page.mjs \
  --url http://127.0.0.1:3000/target \
  --width 1440 \
  --height 1024 \
  --output artifacts/render.png \
  --metadata artifacts/capture.json
```

## Compare screenshots

```bash
python3 scripts/visual_diff.py \
  --reference reference.png \
  --actual artifacts/render.png \
  --output-dir artifacts/diff
```

## Capture and compare

```bash
python3 scripts/run_verification.py \
  --url http://127.0.0.1:3000/target \
  --reference reference.png \
  --width 1440 \
  --height 1024 \
  --output-dir artifacts/verification
```

## Validate the skill

```bash
python3 scripts/validate_skill.py .
```

## Install locally

```bash
python3 scripts/install_skill.py --target codex-user
```
