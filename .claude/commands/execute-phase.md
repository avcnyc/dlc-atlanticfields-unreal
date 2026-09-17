---
description: Execute the next phase from PLAN.md. Reads plan and state, gathers context, implements deliverables, verifies build, and updates progress.
argument-hint: [phase number] or [feature-name phase-number]
---

# Execute Phase Protocol

You are executing `/execute-phase $ARGUMENTS`.

## Strict Workflow — Execute In Order

### STEP 1: READ THE PLAN
Determine which plan to execute:
- If `$ARGUMENTS` includes a feature name (e.g., `auth 3`), read `.claude/PLAN-{feature}.md`
- If `$ARGUMENTS` is a number only (e.g., `3`), read `.claude/PLAN.md`
- If `$ARGUMENTS` is empty, read `.claude/PLAN.md`
- If `.claude/PLAN.md` doesn't exist, check for any `PLAN-*.md` files and ask which one

Read the plan in full. Target the specified phase, or determine the next incomplete phase.
Extract: goal, files to create/modify, deliverables, dependencies.

### STEP 2: READ STATE
Read the matching STATE file (`.claude/STATE.md` or `.claude/STATE-{feature}.md`) to confirm prior phases are complete.
If a prior phase is NOT marked complete, **STOP** and report the dependency gap.

### STEP 3: READ PROJECT CONTEXT
Read `.claude/CLAUDE.md` in full for:
- **Prime Directive** — the rules that govern ALL implementation
- **Build & Verify commands** — what to run after implementation
- **Coding Standards** — naming, style, conventions to follow
- **Critical Constraints** — git commit rules, code comment style
- **Canonical References** — source of truth docs to cross-reference

If `.claude/SPEC.md` exists, read it for requirements context.
If `.claude/CLAUDE.md` references files in `.claude/reference/`, read those too.

### STEP 4: READ EXISTING CODE
Read all files that this phase will modify or depend on.
Understand what exists before writing new code.

**Parallel reads:** Read all independent files simultaneously — do NOT read sequentially when parallel is possible.

### STEP 5: IMPLEMENT
Write the code for this phase EXACTLY as specified in the plan:
- Every file listed in the phase's scope
- Every deliverable mapped to this phase
- Follow the Prime Directive and coding standards from CLAUDE.md

**One phase only:**
- Do NOT reach ahead into future phases
- Do NOT add "while we're here" improvements
- Do NOT refactor prior phase code unless this phase explicitly calls for it
- If you notice issues in prior code, document in STATE.md but do not fix unless blocking

### STEP 6: BUILD & VERIFY
Run the build/test/lint commands from `.claude/CLAUDE.md`:
```
[build command from CLAUDE.md]
[test command from CLAUDE.md]
[lint command from CLAUDE.md]
```
Fix ALL errors. Do not proceed until verification passes.
If a fix requires changing logic, re-read the spec/reference to confirm correctness.

### STEP 7: UPDATE STATE
Update the matching STATE file (`.claude/STATE.md` or `.claude/STATE-{feature}.md`) with:
- Phase marked complete with date
- List of files created/modified
- Any deviations from plan documented
- Resume point set to next phase or "All phases complete"

---

## Output Format

```
### Phase [N] Complete: [Phase Name]

**Files Created:**
- `path/to/file` — [one-line description]

**Files Modified:**
- `path/to/file` — [what changed]

**Verification:**
- Build: PASS/FAIL
- Tests: PASS/FAIL
- Lint: PASS/FAIL

**Verification Checklist:**
- [ ] [Specific things to manually check]
- [ ] [Routes, UI elements, behaviors to verify]
- [ ] [Commands to run]

**Known Limitations:**
- [Anything using placeholder data or needing real credentials]

**Next Phase:** Phase [N+1]: [Name] — [key deliverables]
**Blockers:** [Any dependencies to resolve before next phase]
```

---

## Constraints

**FOLLOW THE PRIME DIRECTIVE** — read it from `.claude/CLAUDE.md` before writing any code.

- Build must pass before phase is marked complete
- One phase at a time — no reaching ahead
- All file reads in parallel when independent
- Deviations from plan must be documented and justified
- Resume point must be specific and executable
