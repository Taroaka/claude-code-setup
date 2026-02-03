---
name: improve-workflow
description: Structured coding workflow for Codex CLI that mirrors the improve_claude_code command pack (plan/tdd/verify/code-review/build-fix/e2e/test-coverage/update-docs). Use when you want Codex to run a tight loop: restate requirements, make a step plan, implement minimal changes, run validations, and summarize results; or when you want Codex to help you run multi-agent tmux sessions with claude/codex.
---

# Improve Workflow

## Default loop (plan → implement → verify)

1) Restate requirements and constraints (what is in/out)
2) If the change is non-trivial, create/update a plan (use `update_plan`)
3) Implement smallest safe change set (avoid unrelated refactors)
4) Validate (prefer fast, local checks before full test suite)
5) Summarize what changed + how to run/verify

## Command-pack equivalents (Codex)

- `plan`: Restate requirements + risks + step plan; WAIT if user wants approval gates
- `tdd`: Write/adjust tests first (if repo has tests), then implement, then re-run
- `verify`: Run the most relevant checks; if none exist, run minimal sanity checks
- `build-fix`: Build/test first, then fix errors iteratively (smallest diff each loop)
- `code-review`: Review changed areas for correctness, security, perf, readability; propose follow-ups
- `refactor-clean`: Do mechanical cleanup only when it reduces risk or enables the requested change
- `update-docs`: Update the smallest canonical doc files (avoid random new docs)

## Validation quick picks (choose what exists)

- Python: `python -m compileall .` then (if present) `pytest`
- Node: `npm test` / `pnpm test` / `yarn test`
- Go: `go test ./...`

Prefer repo-local scripts (`scripts/*`) if they exist.

## Multi-agent tmux (this repo)

If the repo contains `scripts/ai/multiagent.sh`, use it to launch:

- Claude Code: `scripts/ai/multiagent.sh --engine claude`
- Codex CLI: `scripts/ai/multiagent.sh --engine codex`

If `tmux` is missing on macOS: `brew install tmux`.
