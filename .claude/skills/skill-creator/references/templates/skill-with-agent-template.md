# Skill Template (With Agent)

This template generates skills paired with agents, ensuring proper knowledge-behavior separation.

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

{Paragraph 3: How it integrates with the {domain}-specialist agent}

## Quick Start

### Step 1: {First Action}
{Clear, actionable instructions}

### Step 2: {Second Action}
{Clear, actionable instructions}

### Step 3: {Third Action}
{Clear, actionable instructions}

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

## Examples

### Example 1: {Scenario 1}

**{Context}**:
```{language}
{Working code example}
```

**{Explanation}**: {What this demonstrates}

### Example 2: {Scenario 2}

**{Context}**:
```{language}
{Working code example}
```

**{Explanation}**: {What this demonstrates}
```

## Key Differences from Standalone Template

**Skill with Agent MUST:**
- Focus on knowledge, NOT behavior
- NO "When Invoked" workflow sections
- NO decision trees or orchestration logic
- Reference agent in Purpose paragraph 3
- Keep SKILL.md even more concise (<400 lines recommended)
- Use reference files heavily for patterns and examples

**Skill with Agent MUST NOT:**
- Duplicate agent content
- Include workflow steps (agent's responsibility)
- Define role behaviors (agent's responsibility)
- Include tool usage instructions (agent decides)

## Responsibility Separation

### Agent Responsibilities (Behavioral)
- When Invoked workflow
- Tool selection and usage
- Quality checks before completion
- Response formatting
- Methodology and approach

### Skill Responsibilities (Knowledge)
- Core Concepts and patterns
- Common Pitfalls with solutions
- Reference materials and examples
- Technical details and edge cases
- Best practices and conventions

### No Duplication Zone
- Agent should NOT include code examples (refer to skill)
- Agent should NOT repeat patterns (refer to skill)
- Skill should NOT include workflow steps (keep in agent)
- Skill should NOT include tool usage (keep in agent)
- Skill should NOT define "When Invoked" (keep in agent)

## Content Guidelines

### Purpose Section (Paragraph 3)
Must mention the paired agent:

Example:
```markdown
This skill integrates with the python-fastapi-specialist agent, providing
patterns and conventions that the agent references when implementing FastAPI
solutions.
```

### Quick Start
Keep more concise than standalone skills:
- Focus on key patterns to learn
- Reference where to find detailed workflows (in agent)
- Point to reference files for complete examples

### Core Concepts
Should be the heart of the skill:
- Patterns the agent will reference
- Conventions the agent will follow
- Technical knowledge the agent needs
- Best practices to apply

### When to Load References
More important for paired skills:
- Agent will reference these files
- Guide should be clear for agent invocation
- Include what each reference contains

## Examples by Domain

### TouchDesigner Python Skill (with Agent)

```yaml
---
name: touchdesigner-python
description: "Comprehensive TouchDesigner Python extension development with support for reactive state, lifecycle callbacks, and property decorators. Use when creating TD extensions, implementing callbacks, managing reactive state, or refactoring TD Python code."
---

# TouchDesigner Python Extensions

You are the TouchDesigner Python Guide, responsible for helping developers
create properly structured extensions with reactive state management,
lifecycle callbacks, and modern Python 3.11+ type hints.

## Purpose

TouchDesigner extensions are Python classes that add custom behavior to
components. Well-structured extensions use reactive state (tdu.Dependency)
to automatically update UI and parameter expressions, lifecycle callbacks
(onInitTD, onDestroyTD) for proper initialization and cleanup, and
consistent naming conventions that enable promotion to the component level.

This skill provides patterns for creating extensions that integrate
seamlessly with TouchDesigner's architecture. Extensions follow a
consistent naming convention: PascalCase component names with Ext suffix
(e.g., MyComp component → MyCompExt class). Capitalized members are
automatically promoted to the component level for external access.

This skill integrates with the touchdesigner-python-specialist agent,
providing the conventions, patterns, and examples that the agent
references when implementing TouchDesigner Python solutions.
```

**Note**: Paragraph 3 clearly links to the agent.

### Python FastAPI Skill (with Agent)

```yaml
---
name: python-fastapi
description: "Modern FastAPI development patterns with Python 3.10+ async, Pydantic validation, and dependency injection. Use when building REST APIs, implementing endpoints, or structuring FastAPI applications."
---

# FastAPI Development Patterns

You are the FastAPI Development Guide, responsible for providing patterns
and best practices for building modern REST APIs with FastAPI.

## Purpose

FastAPI is a modern Python framework for building high-performance REST
APIs with automatic OpenAPI documentation, Pydantic validation, and native
async support. Well-structured FastAPI applications use type hints
extensively, implement dependency injection properly, and follow RESTful
conventions.

This skill provides essential patterns for async endpoint design,
request/response validation with Pydantic, middleware implementation, and
database integration. These patterns enable developers to build scalable,
maintainable APIs that leverage FastAPI's automatic documentation and
validation features.

This skill integrates with the python-fastapi-specialist agent, providing
the patterns, conventions, and code examples that the agent references
when implementing FastAPI solutions.
```

## Placeholder Guide

Same as standalone template, plus:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{domain}-specialist` | Paired agent name | `python-fastapi-specialist` |
| `{agent-references}` | What agent uses from skill | `patterns and conventions` |

## Harmonization Notes

When generating skill for existing agent:

### Check Agent First
1. Read agent file to understand domain
2. Identify what knowledge agent needs
3. Extract patterns/examples agent references
4. Ensure no duplication

### Content Extraction
If agent has:
- Code examples → Move to skill `references/examples.md`
- Pattern lists → Move to skill `Core Concepts`
- Conventions → Move to skill `references/conventions.md`
- Detailed workflows → Keep in agent (agent responsibility)

### Agent Updates Required
After generating skill, update agent to:
- Add `skills: {skill-name}` to frontmatter
- Add `Skill` to tools list (or omit tools)
- Reference skill in "When Invoked" step 3
- Remove duplicated content
- Add skill reference in "Core Expertise" section

## Validation Checklist

After generating, verify all items from standalone template, plus:

### Harmonization Specific
- [ ] Purpose paragraph 3 mentions paired agent
- [ ] No "When Invoked" workflow sections
- [ ] No behavioral content (decision trees, orchestration)
- [ ] Agent name follows `{domain}-specialist` pattern
- [ ] Skill name matches agent's `skills:` field
- [ ] No content duplication (run harmonization audit)
- [ ] Agent references skill correctly
- [ ] Combined agent+skill under 7000 tokens

### Content Separation
- [ ] Skill has knowledge (patterns, examples, conventions)
- [ ] Agent has behavior (workflows, tool usage, quality checks)
- [ ] No overlap between skill Core Concepts and agent When Invoked
- [ ] Reference files contain detail, not workflow steps

## Post-Generation Steps

### Step 1: Generate Skill
1. Use this template
2. Fill in all placeholders
3. Create SKILL.md and references/

### Step 2: Validate Skill
```
Load skill-auditor skill
Audit .claude/skills/{name}/
Target score: 9+/10
```

### Step 3: Check Agent Reference
```
Read .claude/agents/{domain}-specialist.md
Verify skills: field includes {name}
Verify Skill in tools list
Verify step 3 references skill loading
```

### Step 4: Run Harmonization Audit
```
Load both agent-auditor and skill-auditor
Run harmonization checks
Verify no duplication detected
Check combined token budget < 7000
```

### Step 5: Fix Issues
If harmonization issues found:
1. Identify duplicated content
2. Keep in skill if knowledge-based
3. Keep in agent if behavior-based
4. Re-run audits until both pass

## Common Mistakes

### Mistake 1: Including Workflows in Skill
❌ **Bad**:
```markdown
## When Invoked

1. Analyze the request
2. Check existing code
3. Implement solution
```

✅ **Good**: Remove workflows. This belongs in agent.

### Mistake 2: Not Mentioning Agent
❌ **Bad**: Purpose section doesn't reference agent

✅ **Good**: Paragraph 3 explicitly mentions the paired agent

### Mistake 3: Duplicating Agent Content
❌ **Bad**: Skill repeats same patterns as agent

✅ **Good**: Agent references skill, skill has unique knowledge

### Mistake 4: Behavioral Instructions
❌ **Bad**: "You should first check...", "Then implement..."

✅ **Good**: "Pattern for...", "Convention is...", "Example shows..."

### Mistake 5: Tool Usage Guidance
❌ **Bad**: "Use the Read tool to...", "Execute with Bash..."

✅ **Good**: "Code example shows...", "Pattern demonstrates..."

## Integration with Agent Creator

### Generation Order
1. **Agent first**: Defines behavior and workflow
2. **Skill second**: Provides knowledge base
3. **Validate both**: Run both auditors
4. **Harmonize**: Run harmonization audit

### Naming Convention
- Agent: `{domain}-specialist.md`
- Skill: `{domain}/SKILL.md`
- Consistency: Both use same `{domain}` prefix

### Cross-References
Agent should reference skill:
```markdown
3. **Load the {domain} skill** - Reference it for {what-skill-provides}
```

Skill should mention agent:
```markdown
This skill integrates with the {domain}-specialist agent, providing
{what-agent-uses} that the agent references when implementing solutions.
```

## Quick Reference

### Skill with Agent Structure
```markdown
---
name: {domain}
description: {third-person}. Use when {triggers}. {context}.
---

# {Title}

You are the {Role}, responsible for {primary-responsibility}.

## Purpose
Para 1: What/problem
Para 2: Why/value
Para 3: Integration with {domain}-specialist agent

## Quick Start
3 steps (concise, pattern-focused)

## Core Concepts
3-5 subsections (patterns agent will use)

## Common Pitfalls
Min 3 items (❌/✅ format)

## When to Load References
Clear triggers for agent to load files

## Examples
Min 2 examples (working code)
```

### Target Metrics
- SKILL.md: <400 lines (even more concise than standalone)
- Purpose: Exactly 3 paragraphs (3rd mentions agent)
- Core Concepts: 3-5 patterns (essential knowledge)
- References: Heavy use for detailed content
- Auditor score: 9+/10
- Harmonization: No duplication, <7000 tokens combined
