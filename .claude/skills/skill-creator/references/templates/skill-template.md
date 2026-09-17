# Skill Template (Standalone)

This template generates skills that pass auditor validation at 9+/10.

## Template

```markdown
---
name: {domain}
description: {Brief description in third person}. Use when {trigger-conditions}. {Additional-context}.
---

# {Title}

You are the {Role Name}, responsible for {primary-responsibility}.

## Purpose

{Paragraph 1: What this skill provides and the problem it solves}

{Paragraph 2: Why it's valuable and what it enables}

{Paragraph 3: How it integrates with the framework or workflow}

## Quick Start

### Step 1: {First Action}
{Clear, actionable instructions for first step}

### Step 2: {Second Action}
{Clear, actionable instructions for second step}

### Step 3: {Third Action}
{Clear, actionable instructions for third step}

## Core Concepts

### {Concept 1}
{Essential knowledge, pattern, or technique}

### {Concept 2}
{Essential knowledge, pattern, or technique}

### {Concept 3}
{Essential knowledge, pattern, or technique}

## Common Pitfalls

- ❌ **{Mistake 1}** - {Why it's wrong} → ✅ **{Correct approach}**
- ❌ **{Mistake 2}** - {Why it's wrong} → ✅ **{Correct approach}**
- ❌ **{Mistake 3}** - {Why it's wrong} → ✅ **{Correct approach}**

## When to Load References

Load `references/{reference-1}.md` when:
- **{Trigger condition}** - {What the reference provides}

Load `references/{reference-2}.md` when:
- **{Trigger condition}** - {What the reference provides}

Load `references/{reference-3}.md` when:
- **{Trigger condition}** - {What the reference provides}

## Examples

### Example 1: {Scenario 1}

**{Context or setup}**:
```{language}
{Working code example with comments}
```

**{Explanation}**: {What this example demonstrates}

### Example 2: {Scenario 2}

**{Context or setup}**:
```{language}
{Working code example with comments}
```

**{Explanation}**: {What this example demonstrates}

### Example 3: {Scenario 3}

**{Context or setup}**:
```{language}
{Working code example with comments}
```

**{Explanation}**: {What this example demonstrates}
```

## Placeholder Guide

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{domain}` | Domain/technology name | `python-fastapi`, `react-testing` |
| `{Title}` | Human-readable title | `Python FastAPI Patterns`, `React Testing Guide` |
| `{Role Name}` | Role descriptor | `FastAPI Expert`, `Testing Guide` |
| `{primary-responsibility}` | What role does | `helping developers build REST APIs` |
| `{trigger-conditions}` | When to use | `building FastAPI applications` |
| `{Concept X}` | Core concept name | `Async Patterns`, `Validation` |
| `{Mistake X}` | Common error | `Using sync functions`, `Missing type hints` |
| `{reference-X}` | Reference file name | `workflows`, `patterns`, `examples` |
| `{Scenario X}` | Example scenario | `Creating an Endpoint`, `Adding Validation` |

## Required Sections (For Auditor Compliance)

Must have these sections in this order:

1. **Role Statement** - "You are the..."
2. **Purpose** - 2-3 paragraphs explaining what, why, value
3. **Quick Start** - Exactly 3 steps
4. **Core Concepts** - 3-5 subsections with essential knowledge
5. **Common Pitfalls** - Minimum 3 items with ❌/✅ format
6. **When to Load References** - Guide for when to load each reference file
7. **Examples** - Minimum 2 concrete examples with code

## Content Guidelines

### Role Statement
- Format: "You are the {Role}, responsible for {responsibility}."
- Be specific about the domain and purpose
- Use third person perspective

Example:
```markdown
You are the FastAPI Development Guide, responsible for helping developers
build modern REST APIs with Python 3.10+ and async patterns.
```

### Purpose Section
- 2-3 paragraphs (not more, not less)
- Paragraph 1: What and problem it solves
- Paragraph 2: Why valuable and what it enables
- Paragraph 3: Integration with framework/workflow
- No bullet lists in Purpose section

### Quick Start
- Exactly 3 steps (numbered as "Step 1:", "Step 2:", "Step 3:")
- Each step is actionable and specific
- Steps should enable user to get started quickly
- No substeps or bullet lists within steps

### Core Concepts
- 3-5 subsections (use `###` headers)
- Each concept is essential knowledge
- Focus on patterns, not exhaustive details
- Keep each concept to 3-5 sentences or a small code block

### Common Pitfalls
- Minimum 3, recommended 5-7
- Format: `❌ **{Mistake}** - {Explanation} → ✅ **{Correct}**`
- Be specific about the mistake and solution
- Include real examples users might encounter

### When to Load References
- Group by reference file
- Format: "Load `references/{file}.md` when:"
- List 1-3 trigger conditions per file
- Be specific about what content is in each file

### Examples
- Minimum 2, recommended 3
- Each example must have:
  - Scenario title (descriptive)
  - Context or setup explanation
  - Working code block
  - Explanation of what it demonstrates
- Examples should be complete and runnable
- Use realistic scenarios

## Description Writing

### Format
```yaml
description: {Brief description}. Use when {triggers}. {Additional context}.
```

### Requirements
- **Third person** - No "I", "you", "we"
- **Under 1024 characters** - Keep concise
- **Specific triggers** - Include concrete use cases
- **No XML tags** - Plain text only

### Good Examples

```yaml
description: Guide for creating REST API tests with Jest and Supertest. Use when building API test suites or validating endpoints. Covers async patterns, mocking, and integration testing.
```

```yaml
description: Patterns for migrating PostgreSQL databases safely. Use when planning schema changes or data migrations. Includes zero-downtime techniques and rollback strategies.
```

```yaml
description: Comprehensive TouchDesigner Python extension development with support for reactive state, lifecycle callbacks, and property decorators. Use when creating TD extensions, implementing callbacks, managing reactive state, or refactoring TD Python code.
```

### Bad Examples

❌ "I help you with API testing"
→ First person, vague

❌ "API testing skill"
→ No triggers, no context

❌ "Use this when you need to test"
→ Too vague, no specific triggers

## Line Count Guidelines

**SKILL.md Body** (excluding frontmatter):
- Target: 200-400 lines
- Maximum: 500 lines (hard limit per auditor)
- If approaching 500, extract content to reference files

**Reference Files**:
- Target: 200-400 lines each
- Acceptable: Up to 500 lines
- If over 500, split into multiple focused files

## Validation Checklist

After generating, verify:

### Frontmatter
- [ ] `name` field present and lowercase-hyphenated
- [ ] `description` field present and under 1024 chars
- [ ] Description in third person (no "I", "you", "we")
- [ ] Description includes "Use when..." trigger
- [ ] No XML tags in description

### Structure
- [ ] Skill is a directory (not single file)
- [ ] SKILL.md exists in directory root
- [ ] Directory name matches `name` field
- [ ] References are one level deep (no nesting)

### Sections
- [ ] Role statement present ("You are...")
- [ ] Purpose section has 2-3 paragraphs
- [ ] Quick Start has exactly 3 steps
- [ ] Core Concepts has 3-5 subsections
- [ ] Common Pitfalls has minimum 3 items with ❌/✅ format
- [ ] When to Load References section present
- [ ] Examples section has minimum 2 examples

### Content Quality
- [ ] SKILL.md body under 500 lines
- [ ] No behavioral instructions ("When invoked:", decision trees)
- [ ] No Windows paths (use forward slashes)
- [ ] Reference files 200-500 lines each
- [ ] Examples are complete and working
- [ ] Consistent terminology throughout

### Auditor Target
- [ ] Run skill-auditor on generated skill
- [ ] Score should be 9+/10
- [ ] No ERRORS
- [ ] Fix any WARNINGS

## Common Generation Mistakes

### Mistake 1: First Person Description
❌ **Bad**:
```yaml
description: I help you build FastAPI applications
```

✅ **Good**:
```yaml
description: Guide for building FastAPI REST APIs. Use when creating endpoints or implementing async patterns.
```

### Mistake 2: Missing Required Sections
❌ **Bad**: No "Common Pitfalls" section

✅ **Good**: Include all 7 required sections

### Mistake 3: Behavioral Content in Skill
❌ **Bad**:
```markdown
## When Invoked

1. Analyze the request
2. Check existing code
3. Implement solution
```

✅ **Good**: Keep workflows in agents, not skills. Skills provide knowledge.

### Mistake 4: Too Few Common Pitfalls
❌ **Bad**: Only 1-2 pitfalls

✅ **Good**: Minimum 3 pitfalls with ❌/✅ format

### Mistake 5: Oversized SKILL.md
❌ **Bad**: 632 lines in SKILL.md

✅ **Good**: Move detailed content to references/, keep SKILL.md under 500

### Mistake 6: No Examples
❌ **Bad**: Pure theory, no code examples

✅ **Good**: Minimum 2 concrete, working examples

### Mistake 7: Vague Triggers
❌ **Bad**: "Use when needed"

✅ **Good**: "Use when building FastAPI endpoints, implementing validation, or adding middleware"

## Post-Generation Validation

### Step 1: Run Skill Auditor
```
Load skill-auditor skill
Audit .claude/skills/{name}/
```

### Step 2: Check Score
- **Target**: 9.0+/10 (Grade A or better)
- **Acceptable**: 7.0+/10 (Grade C or better)
- **Failing**: <7.0/10 (needs fixes)

### Step 3: Fix Issues
For each ERROR or WARNING:
1. Locate the issue in generated file
2. Apply suggested fix from auditor
3. Re-run auditor
4. Repeat until score is 9+/10

## Integration with Agent Creator

When generating skill as part of agent+skill pair:

### Generate After Agent
1. Agent created first (defines behavior)
2. Skill created second (provides knowledge)

### Avoid Duplication
- Agent has workflows, skill has patterns
- Agent has "When Invoked", skill has "Core Concepts"
- No overlapping content (run harmonization audit)

### Naming Consistency
- Agent: `{domain}-specialist`
- Skill: `{domain}`
- Example: `python-fastapi-specialist` + `python-fastapi`

See agent-creator skill for harmonized generation patterns.
