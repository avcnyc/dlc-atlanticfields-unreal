---
description: Resume work from saved state. Loads context from STATE.md, PLAN.md, and SPEC.md to pick up where you left off.
---

# Resume Protocol

You are executing `/continue`.

Execute three-stage resume: Environment → State → Action

## Stage 1: Environment Verification

```bash
pwd
ls .claude/STATE*.md .claude/PLAN*.md .claude/SPEC.md 2>/dev/null
git status --short
git branch --show-current
```

**Decision Points:**
- Uncommitted changes → Ask: "Commit, stash, or continue?"
- No STATE files found → "No Active Work" output
- Multiple STATE files found → List them and ask which to resume
- Otherwise → Stage 2

## Stage 2: State Reconstruction

If multiple STATE files exist (e.g., `STATE.md` + `STATE-auth.md`), ask user which work stream to resume.

Read in cascade:
1. `.claude/STATE.md` (or `STATE-{feature}.md`) — current progress
2. Matching `.claude/PLAN.md` (or `PLAN-{feature}.md`) — execution plan
3. `.claude/SPEC.md` — requirements context (if exists)
4. `.claude/CLAUDE.md` — Prime Directive and build commands

Determine status from STATE file:
1. **blocked**: Blockers section has content (not "None") → blocked
2. **active**: Resume Point has Next Action OR has In Progress tasks → active
3. **completed**: All tasks completed, none pending → completed
4. **idle**: No active work → idle

## Stage 3: Output by Status

### active
```
Resuming Work

Last Updated: [timestamp]
Context: [phase] - [status]

Progress:
[completed] [in progress] [pending]

Resume Point: [Next Action]
Context: [if present]

Proceed? (y/n)
```
On confirm → Execute Next Action, update STATE file timestamp.

### blocked
```
Work Blocked

Blocker: [description]

Options: 1. Address now  2. Workaround  3. Wait  4. Abandon
```

### completed
```
Work Complete

Completed: [tasks]

Next: 1. Archive & new task  2. Next phase  3. Review
```

### idle / No STATE files
```
No Active Work

Options: 1. /do [task]  2. Check PLAN.md  3. Start fresh
```
If a PLAN file exists with approved status → Offer to start next phase.

### Invalid State
```
Invalid STATE file

Options: 1. Delete & start fresh  2. Check git history  3. Manual fix
```

## Staleness (>24h)
```
State is [X] old. Verify files exist and codebase unchanged. Proceed? (y/n)
```
