---
description: Execute a task with automatic complexity routing and planning. Generates execution plans for complex work, executes simple tasks directly.
---

# Task Execution Protocol

You are executing `/do $ARGUMENTS`.

## Step 1: Load Context

Read `.claude/CLAUDE.md` in full — Prime Directive, build commands, coding standards, and Critical Constraints (git commits, code comments).
If `.claude/SPEC.md` exists, read it for requirements context.
If any `.claude/PLAN*.md` files exist, read them to understand active work.

## Step 2: Complexity Analysis

Score the task:

| Dimension | 0 pts | 1 pt | 2 pts | 3 pts |
|-----------|-------|------|-------|-------|
| Files | 1 | 2-5 | 6-10 | 11+ |
| Domains | 1 | 2 | 3+ | — |
| Est. LOC | <100 | 100-500 | 500-1500 | 1500+ |
| Dependencies | Independent | Sequential | Complex graph | — |

- **SIMPLE (0-1):** Execute directly
- **MODERATE (2-3):** Create `.claude/STATE.md`, track progress
- **COMPLEX (4+):** Create `.claude/PLAN.md`, get approval, then execute

## Step 3: Route

### SIMPLE
1. Execute the task directly
2. Report completion

### MODERATE
1. Create `.claude/STATE.md` with task breakdown
2. Discover agents: `ls .claude/agents/*.md` — match task to specialist descriptions
3. Delegate or execute directly if no specialist matches
4. Update `.claude/STATE.md` at completion

### COMPLEX
1. Check if `.claude/PLAN.md` already exists:
   - **If yes:** Use a feature suffix instead — `.claude/PLAN-{feature}.md` (e.g., `PLAN-auth.md`)
   - **If no:** Use `.claude/PLAN.md`
2. Create the plan file with:
   - Goal and scope (files to create/modify)
   - Phases with deliverables
   - Agent assignments (from dynamic discovery)
   - Dependencies (parallel vs sequential)
3. Present plan to user
4. **WAIT FOR USER APPROVAL** before executing
5. On approval, execute phase-by-phase with matching STATE file (`.claude/STATE.md` or `.claude/STATE-{feature}.md`)

## Step 4: Agent Routing

Discover available agents dynamically:
1. List `.claude/agents/*.md`
2. Read frontmatter `description` from each agent
3. Match task keywords against agent descriptions
4. If match found → delegate to specialist
5. If no match → let Claude handle it natively

## Checkpoint Triggers

Update `.claude/STATE.md` when ANY of these occur:
1. Phase transition
2. Major decision made
3. Error encountered
4. Task completion
5. Context running low

## Output Format

**SIMPLE:**
```
Classification: SIMPLE (X points)
Executing directly...
[results]
```

**MODERATE:**
```
Classification: MODERATE (X points)
[progress updates]
```

**COMPLEX:**
```
Classification: COMPLEX (X points)
Creating PLAN.md for approval...

[PLAN.md contents]

Please review and approve to proceed.
```
