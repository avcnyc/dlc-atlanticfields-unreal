---
description: Audit a completed phase for correctness, standards compliance, and code quality. Analysis and fixes only — no new features. Run after /execute-phase, before committing.
argument-hint: [phase number] or [feature-name phase-number]
---

# Audit Phase Protocol

You are executing `/audit-phase $ARGUMENTS`.

**Mode: Analysis + Fixes ONLY — No new features, no scope expansion.**

## Strict Workflow — Execute In Order

### STEP 1: IDENTIFY THE PHASE
Determine which plan/state to audit:
- If `$ARGUMENTS` includes a feature name (e.g., `auth 3`), use `.claude/PLAN-{feature}.md` and `.claude/STATE-{feature}.md`
- If `$ARGUMENTS` is a number only, use `.claude/PLAN.md` and `.claude/STATE.md`
- If empty, use `.claude/STATE.md` (or check for `STATE-*.md` files)

Audit the specified phase, or the most recently completed phase from the STATE file.
If no STATE file exists, ask the user which phase to audit.

### STEP 2: PARALLEL INGESTION
Read ALL of the following in parallel — do NOT read sequentially:

**Phase deliverables:**
- All files created or modified in this phase (from STATE.md or PLAN.md)

**Context:**
- `.claude/CLAUDE.md` — Prime Directive, coding standards, build commands
- Matching PLAN file (`.claude/PLAN.md` or `.claude/PLAN-{feature}.md`) — phase deliverables, scope
- `.claude/SPEC.md` — Acceptance criteria (if exists)

**References:**
- Any canonical source files referenced in CLAUDE.md or PLAN.md
- Any files in `.claude/reference/` relevant to this phase

### STEP 3: GENERATE AUDIT CHECKLIST
Based on what this phase did, generate a phase-specific audit checklist covering:

#### Correctness
- [ ] Every deliverable in PLAN.md for this phase is implemented
- [ ] Implementation matches spec/reference (if canonical sources exist)
- [ ] No logic errors, off-by-one bugs, or incorrect formulas
- [ ] Edge cases handled (empty input, boundary values, error paths)

#### Prime Directive Compliance
- [ ] No premature optimizations added
- [ ] No "while we're here" changes outside phase scope
- [ ] Code follows the project's #1 rule from CLAUDE.md

#### Code Quality
- [ ] No dead code, commented-out blocks, or unused variables
- [ ] No code from prior phases modified (unless this phase's plan explicitly requires it)
- [ ] Functions are focused and reasonably sized
- [ ] Error handling covers failure paths

#### Standards Compliance
- [ ] Naming follows coding standards from CLAUDE.md
- [ ] File organization follows project conventions
- [ ] No hardcoded values that should be configurable

#### Build Verification
- [ ] Build command passes with zero errors
- [ ] Test command passes
- [ ] Lint command passes
- [ ] No new warnings introduced

#### Phase-Specific Checks
Generate additional checklist items based on the nature of the phase:

- **Data/API phase:** Schema correctness, migration safety, endpoint contracts
- **UI phase:** Accessibility, responsive behavior, state management
- **Integration phase:** Connection handling, error recovery, fallback behavior
- **Optimization phase:** Output must remain identical to pre-optimization
- **Refactor phase:** No behavioral changes, all tests still pass

### STEP 4: EXECUTE AUDIT
Work through every checklist item. For each:
- **PASS:** Verified correct
- **FAIL:** Issue found — fix it immediately
- **N/A:** Not applicable to this phase

**Fix rules:**
- Fix only issues within this phase's files
- Do NOT modify files from other phases unless fixing a blocking correctness issue
- Build must succeed after every fix
- If a fix changes behavior, document EXACTLY what changed and why

### STEP 5: RUN BUILD VERIFICATION
After all fixes applied:
```
[build command from CLAUDE.md]
[test command from CLAUDE.md]
[lint command from CLAUDE.md]
```
All must pass. If not, fix and re-run.

### STEP 6: OPTIMIZATIONS & MICRO-OPTIMIZATION NOTES

**Significant optimizations** — Fix them NOW during the audit:
- Blatant performance issues (O(n^2) when O(n) is trivial, missing indexes, unnecessary re-renders)
- Obvious architectural improvements that prevent future problems
- Clear refactoring wins that simplify the code substantially

**Micro-optimizations** — Document but do NOT implement:
- Minor performance tuning (cache hints, intrinsics, loop unrolling)
- Speculative improvements without profiling data
- "Nice to have" refactors that don't affect correctness

Document micro-optimization notes in STATE.md under a "Micro-Optimization Notes" section for future phases.

### STEP 7: UPDATE STATE
Update the matching STATE file (`.claude/STATE.md` or `.claude/STATE-{feature}.md`):
- Mark phase as "AUDITED" (not just complete)
- Record issues found and fixed
- Update resume point

---

## Output Format

```
### Phase [N] Audit: [Phase Name]

**Checklist Results:**
- Correctness: [X/Y passed]
- Prime Directive: [PASS/FAIL]
- Code Quality: [X/Y passed]
- Standards: [PASS/FAIL]
- Build: [PASS/FAIL]

**Issues Found & Fixed:**
- [Issue description] → [Fix applied]
- [Issue description] → [Fix applied]
- (or "None")

**Issues Found & NOT Fixed (out of scope):**
- [Issue in prior phase code — documented for future fix]
- (or "None")

**Significant Optimizations Applied:**
- [Optimization applied during audit]
- (or "None")

**Micro-Optimization Notes (do NOT implement):**
- [Opportunity for future improvement]

**Build Verification:** PASS
**Phase Status:** AUDITED — ready to commit
```

---

## Constraints

- **Analysis + fixes only** — do NOT add new features (audit scope)
- **Phase isolation** — do NOT modify files from other phases unless blocking correctness
- **Build must succeed** after any fixes — never leave codebase broken
- **Zero tolerance for Prime Directive violations** — if the phase broke the #1 rule, fix it
- **Document everything** — every fix gets an explanation of what changed and why
