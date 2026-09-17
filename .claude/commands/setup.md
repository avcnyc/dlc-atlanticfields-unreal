---
description: Configure CLAUDE.md for your project. Sets Prime Directive, build/test/lint commands, and coding standards. Run once when adopting the framework, or again to update. Does NOT create plans, specs, or code.
---

# Project Setup

You are executing `/setup`.

**Scope:** Configure the Project Configuration section of `.claude/CLAUDE.md` only. This command does NOT create SPEC.md, PLAN.md, scaffold code, or make architectural decisions.

## Step 1: Read Current State

Read `.claude/CLAUDE.md` to check if Project Configuration is already filled in.

- **If already configured:** Show current config and ask "Update or keep?"
- **If default/empty:** Proceed to Step 2

## Step 2: Gather Configuration

Ask the user these questions using AskUserQuestion. Keep it focused — 5 questions max.

### Question 1: Prime Directive
"What's your project's #1 rule? The hard-won lesson that guides all work."

Examples to offer:
1. "Correctness first — get it working before optimizing"
2. "Never break backwards compatibility"
3. "Test coverage must not decrease"
4. "Faithful to the spec/reference — no creative deviations"
5. Custom (let them type)

### Question 2: Build Command
"What command builds your project?"

Detect from repo if possible:
- `package.json` → suggest `npm run build` or `yarn build`
- `Cargo.toml` → suggest `cargo build`
- `pyproject.toml` → suggest `python -m build`
- `CMakeLists.txt` → suggest `cmake --build build`
- Other → ask directly

### Question 3: Test Command
"What command runs your tests?"

Auto-detect similarly:
- `package.json` with test script → `npm test`
- `Cargo.toml` → `cargo test`
- `pytest.ini` / `pyproject.toml` → `pytest`
- Other → ask

### Question 4: Lint Command
"What command lints/checks your code?"

Auto-detect:
- `.eslintrc` / `package.json` → `npm run lint`
- `Cargo.toml` → `cargo clippy`
- `pyproject.toml` with ruff/flake8 → `ruff check .`
- Other → ask

### Question 5: Coding Standards
"Any specific coding conventions? (e.g., naming, file size limits, style rules)"

Optional — skip if none.

## Step 3: Write Configuration

Update ONLY the Project Configuration section of `.claude/CLAUDE.md`.
Preserve all other sections (Quick Start, Commands, Directory Structure, etc.) exactly as-is.

Replace the commented-out placeholders with actual values:

```markdown
### Prime Directive
[User's answer — formatted as numbered rules if multiple]

### Build & Verify
- **Build:** `[build command]`
- **Test:** `[test command]`
- **Lint:** `[lint command]`

### Coding Standards
[User's conventions, or remove section if none]

### Canonical References
<!-- Add reference material to .claude/reference/ as needed -->
```

## Step 4: Confirm

Show the updated Project Configuration section and ask: "Look good?"

If yes → save. If no → ask what to change.

## Output

```
Project configured!

Prime Directive: [summary]
Build: [command]
Test: [command]
Lint: [command]

Your framework is ready. Start with /do [task] or describe what you want to build.
```

## Constraints

**DO NOT:**
- Create SPEC.md, PLAN.md, or STATE.md
- Scaffold project code or directories
- Make technology or architecture decisions
- Modify anything outside the Project Configuration section of CLAUDE.md

**DO:**
- Auto-detect build tools from repo files when possible
- Keep questions focused and fast (under 2 minutes total)
- Accept "skip" or "none" for optional questions
