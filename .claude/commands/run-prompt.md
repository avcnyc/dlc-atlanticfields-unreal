---
description: Execute prompts created by /create-prompt. Delegates to fresh sub-task contexts with parallel or sequential execution.
argument-hint: <prompt-number(s)-or-name> [--parallel|--sequential]
---

# Run Prompt Protocol

You are executing `/run-prompt $ARGUMENTS`.

This is the execution counterpart to `/create-prompt`.

## Step 1: Parse Arguments

Parse `$ARGUMENTS` to extract:
- Prompt numbers/names (normalize commas to spaces, filter out flags)
- Execution strategy flag (--parallel or --sequential, default: --sequential)

**Examples:**
- `005` → Single: 005
- `005 006 007` → Multiple: [005, 006, 007], sequential
- `005,006,007` → Multiple: [005, 006, 007], sequential
- `005,006,007 --parallel` → Multiple: [005, 006, 007], parallel

## Step 2: Resolve Files

For each prompt number/name:
- If empty or "last": Find most recent in `.claude/prompts/`
- If a number: Match zero-padded (e.g., `5` → `005-*.md`)
- If text: Match files containing that string

**Matching rules:**
- Exactly one match → use it
- Multiple matches → list and ask user to choose
- No matches → error with available prompts list

If `.claude/prompts/` doesn't exist or is empty, suggest running `/create-prompt` first.

## Step 3: Execute

### Single Prompt
1. Read the complete prompt file contents
2. Delegate via Agent tool
3. Wait for completion
4. Archive to `.claude/prompts/completed/` (create if needed)
5. Git commit:
   - Stage modified files with `git add [file]` (never `git add .`)
   - Commit: `[type]: [description]`
6. Return results

### Parallel Execution
1. Read all prompt files
2. **Spawn ALL Agent tools in a SINGLE MESSAGE** (critical for parallelism)
3. Wait for ALL to complete
4. Archive all to `.claude/prompts/completed/`
5. Git commit all work
6. Return consolidated results

### Sequential Execution
1. For each prompt in order:
   a. Read prompt file
   b. Delegate via Agent tool
   c. Wait for completion
   d. Archive prompt
   e. If failed, stop and report error
2. Git commit all work
3. Return consolidated results

## Output Format

**Single:**
```
Executed: .claude/prompts/005-implement-feature.md
Archived: .claude/prompts/completed/005-implement-feature.md

Results:
[Summary of what the sub-task accomplished]
```

**Parallel:**
```
Executed in PARALLEL:
- .claude/prompts/005-implement-auth.md
- .claude/prompts/006-implement-api.md
- .claude/prompts/007-implement-ui.md

Archived: .claude/prompts/completed/

Results:
[Consolidated summary]
```

**Sequential:**
```
Executed SEQUENTIALLY:
1. .claude/prompts/005-setup-database.md - Success
2. .claude/prompts/006-create-migrations.md - Success
3. .claude/prompts/007-seed-data.md - Success

Archived: .claude/prompts/completed/

Results:
[Consolidated summary showing progression]
```

## Constraints

- Parallel: ALL Agent calls in single message
- Sequential: Wait for each before starting next
- Archive only after successful completion
- On failure: Stop sequential execution, report error
