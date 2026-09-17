# Agent-Skill Harmonization Rules

Complete reference for generating consistent agent+skill pairs that pass harmonization audits.

**Version**: 1.0
**Based On**: C:\Users\CHOY\Documents\GitHub\TemporalTD\specs\auditor-framework-spec.md (Section 5)
**Purpose**: Ensure agent-skill pairs work together correctly with no duplication

---

## Table of Contents

1. [Overview](#overview)
2. [Naming Conventions](#naming-conventions)
3. [Responsibility Separation](#responsibility-separation)
4. [Integration Requirements](#integration-requirements)
5. [Duplication Prevention](#duplication-prevention)
6. [Generation Workflow](#generation-workflow)
7. [Harmonization Checklist](#harmonization-checklist)
8. [Common Violations](#common-violations)

---

## Overview

### Purpose of Harmonization

Harmonization ensures that when an agent references a skill:
- **Naming is consistent** - Agent and skill names align
- **Integration is correct** - Agent properly references skill in frontmatter
- **No duplication exists** - Content isn't repeated between files
- **Responsibilities are clear** - Behavior in agent, knowledge in skill
- **Token budget is met** - Combined size under 7000 tokens

### When Harmonization Applies

Run harmonization checks when:
- Generating agent+skill pair together
- Agent references skill in `skills:` field
- User requests "create agent and skill for X"
- Validating existing agent-skill pairs

### Harmonization Rules (From Spec)

Based on Section 5 of auditor-framework-spec.md:

**Integration Checks** (H-IN-*):
- H-IN-001: Agent references skill in frontmatter
- H-IN-002: Naming consistency
- H-IN-003: Agent has Skill tool permission
- H-IN-004: Description alignment

**Duplication Detection** (H-DUP-*):
- H-DUP-001: No content duplication
- H-DUP-002: Agent defers to skill for knowledge
- H-DUP-003: Skill doesn't define behavior

**Efficiency Checks** (H-EF-*):
- H-EF-001: Combined token budget <7000
- H-EF-002: Skill reference efficiency

**Consistency Checks** (H-CS-*):
- H-CS-001: Tool requirements compatible
- H-CS-002: Model compatibility
- H-CS-003: Terminology consistency

---

## Naming Conventions

### Pattern Rules

**Agent Naming**:
```
Format: {domain}-specialist
Examples:
  - python-fastapi-specialist
  - touchdesigner-python-specialist
  - api-testing-specialist
  - database-migration-specialist
```

**Skill Naming**:
```
Format: {domain}
Examples:
  - python-fastapi
  - touchdesigner-python
  - api-testing
  - database-migration
```

**Consistency Requirement**:
- Agent `{domain}` must match skill `{domain}`
- If agent is `python-fastapi-specialist`, skill MUST be `python-fastapi`
- No variations: `fastapi` vs `python-fastapi` is inconsistent

### File Paths

**Agent**:
```
.claude/agents/{domain}-specialist.md
```

**Skill**:
```
.claude/skills/{domain}/SKILL.md
.claude/skills/{domain}/references/*.md
```

**Example**:
```
.claude/agents/python-fastapi-specialist.md
.claude/skills/python-fastapi/SKILL.md
.claude/skills/python-fastapi/references/patterns.md
```

### Validation

**H-IN-002 Check**:
```python
agent_name = "python-fastapi-specialist"
skill_name = "python-fastapi"

# Extract domain from agent name
agent_domain = agent_name.replace("-specialist", "")  # "python-fastapi"

# Check consistency
if agent_domain != skill_name:
    raise_warning("H-IN-002: Naming inconsistency")
```

---

## Responsibility Separation

### Agent Responsibilities (Behavioral)

**What agents contain**:
- Role definition ("You are an expert...")
- When Invoked workflow (step-by-step)
- When NOT to Invoke (boundaries)
- Methodology (how to approach tasks)
- Quality Standards (checklist before completion)
- Constraints (DO NOT / ALWAYS lists)
- Response Format (how to structure output)
- Tool selection and usage
- Integration with other framework components

**Example from agent**:
```markdown
## When Invoked

1. **Analyze the request** - Understand what functionality is needed
2. **Check existing code** - Read relevant files if they exist
3. **Load the python-fastapi skill** - Reference it for patterns and conventions
4. **Implement solution** - Write code following all conventions from the skill
5. **Verify quality** - Check type hints, tests, documentation
```

### Skill Responsibilities (Knowledge)

**What skills contain**:
- Role statement and purpose
- Quick Start (getting started steps)
- Core Concepts (patterns, techniques, conventions)
- Common Pitfalls (mistakes to avoid)
- When to Load References (guide to reference files)
- Examples (working code demonstrations)
- Reference files (detailed patterns, workflows, examples)

**Example from skill**:
```markdown
## Core Concepts

### Async Patterns
FastAPI endpoints should use async/await for I/O operations:
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await db.fetch_user(user_id)
    return user
```

### Validation
Use Pydantic models for request/response validation...
```

### Clear Boundaries

| Content Type | Agent | Skill |
|--------------|-------|-------|
| Workflows | ✓ | ✗ |
| Tool usage | ✓ | ✗ |
| Decision trees | ✓ | ✗ |
| Quality checks | ✓ | ✗ |
| Code patterns | ✗ | ✓ |
| Conventions | ✗ | ✓ |
| Examples | ✗ | ✓ |
| Technical details | ✗ | ✓ |
| Best practices | ✗ | ✓ |

### Violation Examples

**H-DUP-003 Violation** (Skill defines behavior):
```markdown
# In SKILL.md (WRONG)

## When Invoked

1. First analyze the codebase
2. Then implement the pattern
3. Finally verify the results
```
→ This belongs in agent, not skill.

**H-DUP-002 Violation** (Agent duplicates knowledge):
```markdown
# In Agent (WRONG)

FastAPI endpoints use async/await:
```python
@app.get("/users")
async def list_users():
    return await db.fetch_all()
```

# In Skill (DUPLICATE)

FastAPI endpoints use async/await:
```python
@app.get("/users")
async def list_users():
    return await db.fetch_all()
```
```
→ Remove from agent, reference skill instead.

---

## Integration Requirements

### Frontmatter Integration

**Agent frontmatter MUST include**:
```yaml
---
name: {domain}-specialist
description: ...
tools: ..., Skill
skills: {domain}
---
```

**Required fields**:
- `skills:` field listing the skill name
- `Skill` in tools list (or omit tools to inherit)

**H-IN-001 Violation**:
```yaml
# Agent has skill reference but no skills field
---
name: python-fastapi-specialist
tools: Read, Write, Edit, Bash, Skill
# Missing: skills: python-fastapi
---
```

**H-IN-003 Violation**:
```yaml
# Agent has skills field but no Skill tool
---
name: python-fastapi-specialist
tools: Read, Write, Edit, Bash
skills: python-fastapi
# Missing: Skill in tools list
---
```

### System Prompt Integration

**Agent MUST reference skill in "When Invoked"**:
```markdown
## When Invoked

1. **{Step 1}** - {Description}
2. **{Step 2}** - {Description}
3. **Load the {skill-name} skill** - Reference it for {what-skill-provides}
4. **{Step 4}** - {Description}
5. **{Step 5}** - {Description}
```

**Example**:
```markdown
## When Invoked

1. **Analyze the request** - Understand what API functionality is needed
2. **Check existing code** - Read relevant endpoint files if they exist
3. **Load the python-fastapi skill** - Reference it for patterns, conventions, and examples
4. **Implement solution** - Write code following all conventions from the skill
5. **Provide guidance** - Show how to test the endpoint
```

**Agent MUST mention skill in "Core Expertise"**:
```markdown
## Core Expertise

You have deep knowledge of:

- **{Area 1}**: {capabilities}
- **{Area 2}**: {capabilities}
- **{Area 3}**: {capabilities}

**For detailed patterns, conventions, and code examples, reference the {skill-name} skill.**
```

### Skill Integration

**Skill MUST mention agent in Purpose**:
```markdown
## Purpose

{Paragraph 1: What and problem}

{Paragraph 2: Why and value}

This skill integrates with the {domain}-specialist agent, providing
the patterns and conventions that the agent references when implementing
{domain} solutions.
```

**Example**:
```markdown
This skill integrates with the python-fastapi-specialist agent, providing
the patterns, conventions, and code examples that the agent references
when implementing FastAPI REST API solutions.
```

### Description Alignment (H-IN-004)

Agent and skill descriptions should complement, not contradict:

**Agent description**:
```yaml
description: |
  FastAPI REST API expert. Use PROACTIVELY when building FastAPI
  applications, async endpoints, or API validation.
```

**Skill description**:
```yaml
description: Modern FastAPI development patterns with Python 3.10+ async,
  Pydantic validation, and dependency injection. Use when building REST APIs,
  implementing endpoints, or structuring FastAPI applications.
```

**Alignment check**:
- Both mention FastAPI
- Both reference async patterns
- Both include API development
- No contradictions

---

## Duplication Prevention

### Detection Method (H-DUP-001)

**Line-level comparison**:
```python
def detect_duplication(agent_content: str, skill_content: str) -> DuplicationReport:
    """
    Find duplicated content between agent and skill.

    Flags if:
    - More than 30 consecutive lines match
    - Significant code blocks are identical
    - Pattern descriptions are repeated
    """
    # Implementation per spec section 5.2
```

### Common Duplication Patterns

**Pattern 1: Code Examples**

❌ **Duplicated**:
```markdown
# In Agent
FastAPI endpoint example:
```python
@app.get("/users")
async def list_users():
    return await db.fetch_all()
```

# In Skill
FastAPI endpoint example:
```python
@app.get("/users")
async def list_users():
    return await db.fetch_all()
```
```

✅ **Fixed**:
```markdown
# In Agent
## When Invoked

3. **Load the python-fastapi skill** - Reference it for endpoint patterns

# In Skill
## Examples

### Example 1: List Endpoint
```python
@app.get("/users")
async def list_users():
    return await db.fetch_all()
```
```

**Pattern 2: Pattern Descriptions**

❌ **Duplicated**:
```markdown
# In Agent and Skill (both have)
Async patterns in FastAPI use async/await for I/O operations.
This enables non-blocking request handling for better performance.
```

✅ **Fixed**:
```markdown
# In Agent
Load the python-fastapi skill for async patterns

# In Skill (only place with detail)
## Core Concepts

### Async Patterns
FastAPI endpoints should use async/await for I/O operations.
This enables non-blocking request handling for better performance.
```

**Pattern 3: Convention Lists**

❌ **Duplicated**:
```markdown
# In Agent
**Constraints:**
- Use type hints on all parameters
- Implement Pydantic models for validation
- Use async/await for database calls

# In Skill
## Core Concepts

### Type Hints
Use type hints on all parameters...

### Validation
Implement Pydantic models for validation...

### Async Database Access
Use async/await for database calls...
```

✅ **Fixed**:
```markdown
# In Agent
**ALWAYS:**
- Follow conventions from python-fastapi skill

# In Skill (detailed conventions)
## Core Concepts
{Detailed pattern descriptions}
```

### Prevention Strategy

When generating agent+skill pairs:

1. **Generate skill first** - Establish knowledge base
2. **Reference in agent** - Agent points to skill, doesn't duplicate
3. **Verify separation** - Run duplication check
4. **Fix violations** - Remove duplicates, prefer skill for knowledge

---

## Generation Workflow

### Step-by-Step Process

#### Phase 1: Requirements Gathering

1. **Identify domain**: What technology/workflow?
2. **Determine scope**: What capabilities needed?
3. **Check existing**: Any related agents/skills?
4. **Plan split**: What's behavior vs knowledge?

#### Phase 2: Skill Generation

1. **Create skill directory**: `.claude/skills/{domain}/`
2. **Use template**: `skill-with-agent-template.md`
3. **Fill placeholders**:
   - name: `{domain}`
   - description: third person, triggers
   - Role statement: "You are the {Role}..."
   - Purpose: 3 paragraphs (3rd mentions agent)
   - Core Concepts: Patterns agent will use
   - Common Pitfalls: Min 3 items
   - Examples: Min 2 working examples
4. **Create references**: Move detailed content to references/
5. **Validate**: Run skill-auditor, target 9+/10

#### Phase 3: Agent Generation

1. **Create agent file**: `.claude/agents/{domain}-specialist.md`
2. **Use template**: `agent-with-skill-template.md`
3. **Fill placeholders**:
   - name: `{domain}-specialist`
   - description: Include examples, "Use PROACTIVELY"
   - skills: `{domain}`
   - tools: Include `Skill`
   - When Invoked: Step 3 loads skill
   - Core Expertise: Reference skill
4. **Avoid duplication**: Don't repeat skill content
5. **Validate**: Run agent-auditor, target 9+/10

#### Phase 4: Harmonization Validation

1. **Run both auditors** simultaneously
2. **Check integration**:
   - H-IN-001: skills field present
   - H-IN-002: naming consistent
   - H-IN-003: Skill tool present
   - H-IN-004: descriptions align
3. **Check duplication**:
   - H-DUP-001: No >30 line overlap
   - H-DUP-002: Agent defers to skill
   - H-DUP-003: Skill has no behavior
4. **Check efficiency**:
   - H-EF-001: Combined <7000 tokens
   - H-EF-002: Agent guides reference loading
5. **Check consistency**:
   - H-CS-001: Tools compatible
   - H-CS-002: Models compatible
   - H-CS-003: Terminology aligned

#### Phase 5: Fix Issues

For each violation:
1. **Identify root cause**
2. **Apply fix**:
   - Duplication → Remove from agent, keep in skill
   - Missing integration → Add reference in agent
   - Naming mismatch → Rename to match
3. **Re-run audits**
4. **Repeat until both score 9+/10**

---

## Harmonization Checklist

### Pre-Generation

- [ ] Domain identified and clear
- [ ] Scope defined (what's in, what's out)
- [ ] Behavior vs knowledge split planned
- [ ] Template selected (skill-with-agent, agent-with-skill)

### During Skill Generation

- [ ] Name is `{domain}` (lowercase, hyphenated)
- [ ] Description in third person with triggers
- [ ] Purpose paragraph 3 mentions agent
- [ ] No "When Invoked" workflow sections
- [ ] No behavioral content (decision trees, tool usage)
- [ ] Core Concepts has essential patterns
- [ ] Common Pitfalls has min 3 items
- [ ] Examples has min 2 working examples
- [ ] SKILL.md under 500 lines (ideally <400)
- [ ] References created for detailed content

### During Agent Generation

- [ ] Name is `{domain}-specialist`
- [ ] Description has examples with "Use PROACTIVELY"
- [ ] Frontmatter includes `skills: {domain}`
- [ ] Frontmatter includes `Skill` in tools (or omits tools)
- [ ] Step 3 of "When Invoked" loads skill
- [ ] "Core Expertise" section references skill
- [ ] No code examples (refer to skill instead)
- [ ] No pattern duplication from skill
- [ ] System prompt under 200 lines

### Post-Generation Validation

- [ ] Agent-auditor score 9+/10
- [ ] Skill-auditor score 9+/10
- [ ] H-IN-001: Agent references skill in frontmatter ✓
- [ ] H-IN-002: Naming consistent ✓
- [ ] H-IN-003: Agent has Skill tool ✓
- [ ] H-IN-004: Descriptions align ✓
- [ ] H-DUP-001: No >30 line duplication ✓
- [ ] H-DUP-002: Agent defers to skill ✓
- [ ] H-DUP-003: Skill has no behavior ✓
- [ ] H-EF-001: Combined <7000 tokens ✓
- [ ] H-EF-002: Agent guides reference loading ✓
- [ ] H-CS-001: Tools compatible ✓
- [ ] H-CS-002: Models compatible ✓
- [ ] H-CS-003: Terminology consistent ✓

---

## Common Violations

### Violation 1: Missing Skill Reference in Agent

**Issue**: H-IN-001 failure
```yaml
# Agent frontmatter missing skills field
---
name: python-fastapi-specialist
tools: Read, Write, Edit, Bash, Skill
# Missing: skills: python-fastapi
---
```

**Fix**:
```yaml
---
name: python-fastapi-specialist
tools: Read, Write, Edit, Bash, Skill
skills: python-fastapi
---
```

### Violation 2: Naming Inconsistency

**Issue**: H-IN-002 failure
```
Agent: python-fastapi-specialist
Skill: fastapi  # Mismatch!
```

**Fix**:
```
Agent: python-fastapi-specialist
Skill: python-fastapi  # Consistent domain
```

### Violation 3: No Skill Tool

**Issue**: H-IN-003 failure
```yaml
# Agent has skills but no Skill tool
---
name: python-fastapi-specialist
tools: Read, Write, Edit, Bash
skills: python-fastapi
---
```

**Fix**:
```yaml
---
name: python-fastapi-specialist
tools: Read, Write, Edit, Bash, Skill
skills: python-fastapi
---
```

### Violation 4: Content Duplication

**Issue**: H-DUP-001 failure (52 lines duplicated)

**Agent and Skill both have**:
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await db.fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**Fix**: Remove from agent, keep in skill
```markdown
# In Agent
3. **Load the python-fastapi skill** - Reference examples/endpoints.md

# In Skill
## Examples
### Example 1: User Retrieval Endpoint
{code example here}
```

### Violation 5: Skill Contains Workflow

**Issue**: H-DUP-003 failure

**Skill has** (WRONG):
```markdown
## When Invoked

1. Analyze the request
2. Load appropriate patterns
3. Implement solution
```

**Fix**: Remove from skill (workflows belong in agent)

### Violation 6: Token Budget Exceeded

**Issue**: H-EF-001 failure
```
Agent: 3200 tokens
Skill SKILL.md: 4100 tokens
Total: 7300 tokens (exceeds 7000)
```

**Fix**: Extract content from skill to references/
```
Agent: 3200 tokens
Skill SKILL.md: 2800 tokens
Skill references/: 2500 tokens (not counted in budget)
Total: 6000 tokens ✓
```

### Violation 7: Agent Not Guiding References

**Issue**: H-EF-002 failure

**Agent doesn't specify which references** (WRONG):
```markdown
3. **Load the skill** - Reference it for patterns
```

**Fix**: Be specific about references
```markdown
2. **Check Skill References**: Load appropriate reference file:
   - `conventions.md` for code style patterns
   - `patterns.md` for endpoint implementations
   - `examples.md` for complete working code
```

---

## Quick Reference

### Harmonized Pair Structure

**Agent** (`.claude/agents/{domain}-specialist.md`):
```yaml
---
name: {domain}-specialist
description: |
  {One-liner}. Use PROACTIVELY {when}. Specializes in {capabilities}.
  <example>...</example>
tools: ..., Skill
skills: {domain}
---

You are an expert {domain} developer...

## When Invoked
1. Analyze request
2. Check existing code
3. **Load the {domain} skill** - Reference for patterns
4. Implement solution
5. Verify quality
```

**Skill** (`.claude/skills/{domain}/SKILL.md`):
```yaml
---
name: {domain}
description: {Third-person}. Use when {triggers}. {Context}.
---

You are the {Role}, responsible for...

## Purpose
Para 1: What/problem
Para 2: Why/value
Para 3: Integration with {domain}-specialist agent

## Quick Start
3 steps

## Core Concepts
3-5 patterns

## Common Pitfalls
Min 3 items (❌/✅)

## When to Load References
Reference file triggers

## Examples
Min 2 working examples
```

### Target Metrics

- Agent auditor: 9+/10
- Skill auditor: 9+/10
- No H-* violations
- Combined: <7000 tokens
- No duplication: <30 lines overlap
- Clear separation: Behavior in agent, knowledge in skill
