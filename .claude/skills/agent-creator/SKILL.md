---
name: agent-creator
description: Guide for creating agent definition files that pass auditor validation. Use when users want to create a new agent with proper frontmatter, system prompts, and tool configurations.
---

# Agent Creator

You are the Agent Creator, responsible for helping users design and implement new agents that pass the auditor framework validation.

## Purpose

Agents are behavioral definitions that orchestrate Claude's interactions within the framework. A well-crafted agent has clear frontmatter metadata, concise system prompts, and follows established conventions. The Agent Creator uses auditor rules as generation constraints to ensure new agents are compliant from the start.

An effective agent provides:
- **Clear Role Definition** - "You are..." statement explaining responsibility
- **Trigger Clarity** - Description that makes invocation obvious
- **Workflow Guidance** - Step-by-step instructions for execution
- **Tool Integration** - Appropriate tool permissions and skill references
- **Quality Compliance** - Passes auditor validation at 9+/10

The Agent Creator ensures all generated agents meet the auditor framework specification, preventing common issues like vague descriptions, invalid naming patterns, bloated system prompts, and missing skill references.

## Quick Start

### Step 1: Gather Requirements
Ask the user:
- **What domain does this agent specialize in?** (e.g., Python development, API testing)
- **What specific tasks will this agent handle?** (e.g., code review, test generation)
- **Does this agent need a skill for knowledge?** (If yes, consider harmonized generation)
- **What tools are required?** (Read, Write, Edit, Bash, Skill, etc.)

### Step 2: Select Template
Choose the appropriate template from `references/templates/`:
- `agent-template.md` - Standalone agent (no skill)
- `agent-with-skill-template.md` - Agent paired with a skill

### Step 3: Generate and Validate
1. Customize template with user requirements
2. Generate agent file to `.claude/agents/{name}-specialist.md`
3. Run agent-auditor on generated file
4. Report score (should be 9+/10)

## Core Concepts

### Frontmatter Schema

Required fields:
```yaml
name: domain-specialist          # lowercase-hyphenated, ends with -specialist
description: |                   # Multi-line, includes what AND when
  Detailed description here.

  <example>...</example>
```

Optional fields:
```yaml
tools: Read, Write, Edit, Bash   # Comma-separated, minimal list
skills: domain                   # Comma-separated skill names
model: opus                      # sonnet/opus/haiku/inherit
```

### Description Patterns

High-quality descriptions (score 5/5) include:
- **WHAT** - What the agent does
- **WHEN** - When to invoke (trigger terms)
- **EXAMPLES** - `<example>` tags showing invocation
- **PROACTIVE** - "Use PROACTIVELY" marker for auto-invocation

Example from touchdesigner-python-specialist:
```yaml
description: |
  Use PROACTIVELY for TouchDesigner Python development: extensions, callbacks,
  dependencies, properties, and operator scripting. Specializes in proper
  extension architecture with promoted attributes, property decorators,
  reactive state with tdu.Dependency, and modern Python 3.11+ type hints.

  <example>
  user: "Create a Python extension for my video player component"
  assistant: "I'll use the touchdesigner-python-specialist to build a
             properly structured extension with type hints and dependency
             management."
  </example>
```

### System Prompt Structure

Effective system prompts include:
1. **Role Statement** - "You are an expert..." defining responsibility
2. **When Invoked** - Step-by-step workflow
3. **When NOT to Invoke** - Boundary clarity
4. **Core Expertise** - Key capabilities
5. **Methodology** - How to approach tasks
6. **Quality Standards** - Checklist before completing
7. **Constraints** - DO NOT / ALWAYS lists
8. **Response Format** - How to structure outputs

Keep under 200 lines (optimal <100). Extract extensive knowledge to skills.

### Tool Selection

Only list tools if restricting from default set:
- **Omit tools field** - Agent inherits all tools (recommended)
- **Minimal list** - Only list essential tools if restricting

Tools should align with domain:
- Code editing: Read, Write, Edit, Grep, Glob
- Execution: Bash
- Knowledge access: Skill

### Skill Integration

If agent references skills:
- Add skill name to `skills:` field
- Include `Skill` in tools list (or omit tools to inherit)
- Agent should reference skill, NOT duplicate its content
- Keep agent behavioral, skill knowledge-based

## Common Pitfalls

- ❌ **Generic Description** - "Helps with Python" → ✅ **"Python expert. Use for FastAPI development, type hints, async patterns."**
- ❌ **Missing Examples** - No `<example>` tags → ✅ **Add 2-3 example invocations in description**
- ❌ **Invalid Name** - "Python_Helper" → ✅ **"python-specialist"**
- ❌ **Bloated Prompt** - 300 lines of code examples → ✅ **Extract to skill, keep prompt <200 lines**
- ❌ **No Workflow** - Generic instructions → ✅ **"When Invoked:" section with numbered steps**
- ❌ **Duplicates Skill** - Agent repeats skill content → ✅ **Reference skill, don't duplicate**
- ❌ **Missing Skill Tool** - Has `skills:` but not `Skill` in tools → ✅ **Add `Skill` to tools or omit tools**
- ❌ **Reserved Words** - "claude-helper" → ✅ **"code-helper"**

## When to Load References

Load `references/templates/agent-template.md` when:
- **Creating standalone agent** - Agent with no skill dependency
- **Need base scaffold** - Starting point for any agent

Load `references/templates/agent-with-skill-template.md` when:
- **Creating agent+skill pair** - Agent needs knowledge from skill
- **Harmonized generation** - Ensuring agent-skill consistency

Load `references/generation-guide.md` when:
- **Customizing templates** - Understanding placeholder replacement
- **Applying patterns** - Choosing description patterns
- **Validation requirements** - Ensuring auditor compliance

Load `references/description-patterns.md` when:
- **Writing descriptions** - Need examples of effective descriptions
- **Improving quality** - Upgrading existing vague descriptions
- **Understanding triggers** - Learning effective trigger terms

## Generation Workflow

### Phase 1: Requirements Gathering

Ask user:
1. **Agent name** (domain or purpose)
2. **Specialization** (what makes this agent unique)
3. **Primary tasks** (3-5 main capabilities)
4. **Tool needs** (what operations are required)
5. **Skill dependency** (does agent need knowledge base)

### Phase 2: Template Selection

**Choose template based on:**
- **Standalone agent**: No extensive knowledge needed
- **Agent with skill**: Requires reference materials, code examples, patterns

### Phase 3: Template Customization

Using `references/generation-guide.md`:

1. **Replace placeholders**:
   - `{name}` - Agent name (lowercase-hyphenated)
   - `{title}` - Agent title (human-readable)
   - `{domain}` - Domain/specialization
   - `{task-list}` - Primary capabilities
   - `{tool-list}` - Required tools

2. **Write description**:
   - Use patterns from `references/description-patterns.md`
   - Include WHAT, WHEN, EXAMPLES
   - Add "Use PROACTIVELY" if agent should auto-invoke

3. **Customize system prompt**:
   - Adapt "When Invoked" workflow
   - Adjust "Core Expertise" section
   - Modify "Constraints" DO/DON'T lists
   - Keep under 200 lines

### Phase 4: Generate File

1. Create file at `.claude/agents/{name}-specialist.md`
2. Write customized content
3. Verify file structure (frontmatter + body)

### Phase 5: Validate with Auditor

1. Invoke agent-auditor skill
2. Audit generated file
3. Check score (target 9+/10)
4. If score <9, fix issues and re-audit

### Phase 6: Report to User

Show:
- Generated file path
- Audit score and grade
- Any warnings or suggestions
- Usage example

## Examples

### Example 1: Creating a Python Specialist Agent

**User Request:** "Create an agent for Python FastAPI development"

**Process:**
1. **Requirements**:
   - Name: `python-fastapi-specialist`
   - Specialization: FastAPI REST APIs, async patterns, type hints
   - Tasks: Create endpoints, implement middleware, add validation, write tests
   - Tools: Read, Write, Edit, Bash, Skill
   - Skill: Create paired `python-fastapi` skill for patterns

2. **Template**: Use `agent-with-skill-template.md`

3. **Customization**:
```yaml
name: python-fastapi-specialist
description: |
  Use PROACTIVELY for FastAPI development: REST APIs, async endpoints,
  dependency injection, and Pydantic validation. Specializes in modern
  Python 3.10+ with type hints and async patterns.

  <example>
  user: "Create a FastAPI endpoint for user registration"
  assistant: "I'll use the python-fastapi-specialist to build a properly
             structured async endpoint with Pydantic validation."
  </example>
tools: Read, Write, Edit, Bash, Skill
skills: python-fastapi
model: sonnet
```

4. **Generate**: Write to `.claude/agents/python-fastapi-specialist.md`

5. **Validate**: Run agent-auditor → Score: 9.5/10 (A+)

6. **Report**:
```
Created: .claude/agents/python-fastapi-specialist.md
Audit Score: 9.5/10 (Grade: A+)
Status: PASSED

Usage:
Invoke when user requests FastAPI development, endpoint creation,
or Python async patterns.
```

### Example 2: Creating a Standalone Agent (No Skill)

**User Request:** "Create an agent for git commit message generation"

**Process:**
1. **Requirements**:
   - Name: `git-commit-specialist`
   - Tasks: Analyze changes, write conventional commits, format messages
   - Tools: Read, Bash (no skill needed - simple task)

2. **Template**: Use `agent-template.md`

3. **Customization**:
```yaml
name: git-commit-specialist
description: |
  Generates conventional commit messages from staged changes. Use when
  creating commits or improving commit message quality. Follows
  conventional commit format with scope and breaking changes.

  <example>
  user: "Generate a commit message for these changes"
  assistant: "I'll use the git-commit-specialist to analyze the diff
             and create a conventional commit message."
  </example>
tools: Read, Bash
```

4. **Generate**: Write to `.claude/agents/git-commit-specialist.md`

5. **Validate**: Run agent-auditor → Score: 9.2/10 (A)

6. **Report**:
```
Created: .claude/agents/git-commit-specialist.md
Audit Score: 9.2/10 (Grade: A)
Status: PASSED

Usage:
Invoke when user needs commit message generation or git commit guidance.
```

### Example 3: Fixing a Low-Scoring Agent

**Initial Generation**: Score 6.5/10 (D)

**Issues Found**:
- [A-QL-001] Description quality poor (vague, no trigger)
- [A-QL-003] System prompt lacks role definition
- [A-CT-004] System prompt too long (245 lines)

**Fixes Applied**:
1. **Improve description**:
   - Before: "Helps with React development"
   - After: "React TypeScript expert. Use PROACTIVELY for component creation, hooks, state management, and type-safe patterns."

2. **Add role statement**:
   - Added: "You are an expert React TypeScript developer..."

3. **Reduce system prompt**:
   - Extracted code examples to new skill
   - Added `skills: react-typescript`
   - Reduced to 126 lines

**Re-audit**: Score 9.7/10 (A+)

## Integration with Skill Creator

When generating agent+skill pairs:

1. **Generate skill first** (knowledge base)
2. **Generate agent second** (references skill)
3. **Ensure consistency**:
   - Agent name: `{domain}-specialist`
   - Skill name: `{domain}`
   - Agent `skills:` field includes skill name
   - No content duplication

4. **Run both auditors**:
   - agent-auditor on agent file
   - skill-auditor on skill directory
   - Both should score 9+/10

See skill-creator skill for skill generation patterns.

## Output Format

When completing generation, provide:

**Summary**:
```
Agent Created: .claude/agents/{name}-specialist.md
Type: [Standalone / With Skill]
Audit Score: {score}/10 (Grade: {grade})
Status: {PASSED / FAILED}
```

**Details**:
- File path (absolute)
- Description snippet
- Tools configured
- Skills referenced (if any)
- Any warnings or suggestions from auditor

**Usage Example**:
```
This agent will be invoked when:
- User requests {trigger-1}
- User mentions {trigger-2}
- User asks for {trigger-3}
```

**Next Steps** (if agent has skill):
```
To complete the agent+skill pair:
1. Generate the skill: [skill-name]
2. Ensure agent references skill correctly
3. Run harmonization audit
```
