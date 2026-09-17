---
description: Create effective prompts for Claude Code tasks using expert prompt engineering
argument-hint: [task description]
---

<context>
Before proceeding, use the Glob tool to check `.claude/prompts/*.md` to:
1. Verify if the prompts directory exists
2. Find the highest numbered prompt to determine next sequence number

Pass this information to the agent workflow.
</context>

<objective>
Create well-structured, effective prompts using the prompt-creator-specialist agent and skill.

User's task description: $ARGUMENTS
</objective>

<invocation>
Invoke the **prompt-creator-specialist agent** to handle the complete workflow.

The agent will:
1. **Intake** - Gather requirements if $ARGUMENTS is empty/vague
2. **Analyze** - Determine task type, complexity, and structure
3. **Question** - Ask clarifying questions via AskUserQuestion
4. **Generate** - Create prompt(s) using patterns from prompt-creator skill
5. **Present** - Show decision tree for execution options

The agent references the **prompt-creator skill** for:
- XML structure patterns
- Task-specific templates
- Worked examples
- Anti-patterns to avoid
</invocation>

<execution>
After the agent generates prompt(s), it will present options:

**Single prompt:** Run now, review first, or save for later
**Multiple parallel:** Run all in parallel, run sequentially, or review first
**Multiple sequential:** Run all sequentially, run first only, or review first

The user's choice determines the next action via /run-prompt command.
</execution>
