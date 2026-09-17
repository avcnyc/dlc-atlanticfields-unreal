# Agent Generation Guide

Complete guide to customizing agent templates and ensuring auditor compliance.

## Template Customization Process

### Step 1: Choose Template

**Use `agent-template.md` when:**
- Agent has no extensive knowledge requirements
- Tasks are straightforward and well-defined
- No need for reference materials or code examples
- System prompt will be under 100 lines

**Use `agent-with-skill-template.md` when:**
- Agent needs access to patterns, conventions, examples
- Domain has extensive knowledge base
- Multiple reference files would be helpful
- Want to keep agent concise by delegating knowledge to skill

### Step 2: Fill Frontmatter

#### Name Field
```yaml
name: {domain}-specialist
```

**Pattern**: `{domain}-specialist` or `{domain}-{specialization}-specialist`

**Examples**:
- `python-fastapi-specialist`
- `react-testing-specialist`
- `database-migration-specialist`
- `api-security-specialist`

**Rules**:
- Lowercase only
- Hyphens for separation
- Ends with `-specialist`
- No underscores
- No version numbers (v1, v2)
- No reserved words (anthropic, claude)
- 1-64 characters total

#### Description Field
```yaml
description: |
  {what-agent-does}. Use {when-trigger} for {primary-tasks}.
  Specializes in {unique-capabilities}.

  <example>
  user: "{user-request}"
  assistant: "{assistant-response}"
  </example>
```

**Components**:
1. **First line** - What the agent does (one sentence)
2. **Use trigger** - When to invoke ("Use when...", "Use PROACTIVELY...")
3. **Specialization** - What makes it unique
4. **Examples** - 2-3 `<example>` blocks showing invocation

**Quality Criteria** (for 5/5 score):
- Includes WHAT the agent does
- Includes WHEN to use it (trigger terms)
- Includes WHY it's valuable (specialization)
- Has 2-3 concrete examples
- Under 1024 characters
- No XML tags in content (except `<example>`)

See `description-patterns.md` for more examples.

#### Tools Field
```yaml
tools: Read, Write, Edit, Bash, Skill
```

**Options**:
- **Omit field** - Agent inherits all tools (recommended)
- **Minimal list** - Only list essential tools if restricting

**Common tool combinations**:
- Code editing: `Read, Write, Edit, Grep, Glob`
- Script execution: `Read, Bash`
- With skill: Include `Skill` in list
- Analysis only: `Read, Grep, Glob`

#### Skills Field (only for agent-with-skill template)
```yaml
skills: {skill-name}
```

**Pattern**: Comma-separated skill names (usually just one)

**Examples**:
- `skills: python-fastapi`
- `skills: touchdesigner-python`
- `skills: react-testing, api-testing` (multiple, rare)

**Rules**:
- Must match skill directory name
- Skill must exist at `.claude/skills/{skill-name}/SKILL.md`
- If skills field present, must include `Skill` in tools (or omit tools)

#### Model Field
```yaml
model: sonnet
```

**Options**:
- `sonnet` - Fast, cost-effective (recommended default)
- `opus` - Complex reasoning, high quality
- `haiku` - Very fast, simple tasks
- `inherit` - Use parent context model
- Omit field to use system default

### Step 3: Customize System Prompt

#### Role Statement (Line 1)
```
You are an expert {domain} developer specializing in {areas}.
```

**Examples**:
- "You are an expert Python developer specializing in FastAPI, async patterns, and type hints."
- "You are an expert TouchDesigner Python developer specializing in extensions and reactive state."
- "You are a code quality reviewer specializing in security, performance, and maintainability."

#### When Invoked Section

**Pattern** (standalone):
```markdown
## When Invoked

1. **{Step Title}** - {What to do}
2. **{Step Title}** - {What to do}
3. **{Step Title}** - {What to do}
4. **{Step Title}** - {What to do}
5. **{Step Title}** - {What to do}
6. **{Step Title}** - {What to do}
```

**Pattern** (with skill):
```markdown
## When Invoked

1. **{Step Title}** - {What to do}
2. **{Step Title}** - {What to do}
3. **Load the {skill-name} skill** - Reference it for {what-skill-provides}
4. **{Step Title}** - {What to do}
5. **{Step Title}** - {What to do}
6. **{Step Title}** - {What to do}
```

**Key**: Step 3 should always reference skill loading if agent has skill.

#### When NOT to Invoke Section

Define boundaries (3-5 items):
```markdown
## When NOT to Invoke

- {Out of scope item 1}
- {Out of scope item 2}
- {Out of scope item 3}
```

**Examples**:
- "Non-Python questions"
- "Frontend development (no API involved)"
- "Pure network/operator wiring (no Python)"
- "Performance profiling"

#### Core Expertise Section

List 4-5 capability areas:
```markdown
## Core Expertise

You have deep knowledge of:

- **{Area 1}**: {capabilities}
- **{Area 2}**: {capabilities}
- **{Area 3}**: {capabilities}
- **{Area 4}**: {capabilities}
```

**For agents with skills**, add reference note:
```markdown
**For detailed patterns, conventions, and code examples, reference the {skill-name} skill.**
```

#### Methodology Section

Step-by-step approach (5-7 steps):
```markdown
## Methodology

1. **{Step Title}**: {Description}
2. **{Step Title}**: {Description}
3. **{Step Title}**: {Description}
```

**For agents with skills**, include skill reference step:
```markdown
2. **Check Skill References**: Load appropriate reference file from the skill:
   - `{reference-1}.md` for {use-case-1}
   - `{reference-2}.md` for {use-case-2}
```

#### Quality Standards Section

Checklist before completion (6-10 items):
```markdown
## Quality Standards

Before completing, verify:

- [ ] {Check 1}
- [ ] {Check 2}
- [ ] {Check 3}
```

**For agents with skills**, add:
```markdown
- [ ] Patterns from {skill-name} skill correctly applied
```

#### Constraints Section

DO NOT and ALWAYS lists:
```markdown
## Constraints

**DO NOT:**
- {Constraint 1}
- {Constraint 2}
- {Constraint 3}

**ALWAYS:**
- {Requirement 1}
- {Requirement 2}
- {Requirement 3}
```

**For agents with skills**, add:
```markdown
**DO NOT:**
- Duplicate content from {skill-name} skill - reference it instead

**ALWAYS:**
- Reference the {skill-name} skill for patterns and examples
```

#### Response Format Section

How to structure output:
```markdown
## Response Format

When providing solutions:

1. **{Section}**: {What to include}
2. **{Section}**: {What to include}
3. **{Section}**: {What to include}
```

**For agents with skills**, add:
```markdown
3. **Note which skill references were used**: (e.g., "Following Pattern X from {reference}.md")
```

### Step 4: Verify Line Count

**Target**: Under 200 lines (excluding frontmatter)
**Optimal**: Under 100 lines

**If too long**:
- Remove code examples (move to skill)
- Consolidate sections
- Use bullet points instead of paragraphs
- Extract detailed guidance to skill references

**Line count breakdown**:
- Role statement: 1-2 lines
- When Invoked: 10-15 lines
- When NOT: 5-8 lines
- Core Expertise: 8-12 lines
- Methodology: 10-15 lines
- Quality Standards: 10-15 lines
- Constraints: 10-15 lines
- Response Format: 8-12 lines
- **Total**: ~70-100 lines (optimal)

## Auditor Compliance Checklist

Before finalizing, verify against auditor rules:

### Frontmatter (A-FM-*)
- [ ] `name` field present
- [ ] `name` matches `^[a-z0-9-]+$` pattern
- [ ] `name` is 1-64 characters
- [ ] `name` has no reserved words (anthropic, claude)
- [ ] `description` field present
- [ ] `description` is 1-1024 characters
- [ ] `description` has no XML tags (except `<example>`)
- [ ] `tools` field is valid CSV (if present)
- [ ] `model` field is valid value (if present)
- [ ] `skills` field is valid CSV (if present)

### Content (A-CT-*)
- [ ] Frontmatter is valid YAML
- [ ] Frontmatter has `---` delimiters
- [ ] System prompt is present (non-empty body)
- [ ] System prompt is under 200 lines
- [ ] No Windows paths (backslashes)
- [ ] File is UTF-8 encoded

### Quality (A-QL-*)
- [ ] Description includes WHAT and WHEN
- [ ] Description has trigger terms
- [ ] Description has examples (bonus)
- [ ] System prompt has role definition ("You are...")
- [ ] System prompt has workflow ("When Invoked:")
- [ ] System prompt has examples (bonus)
- [ ] System prompt specifies output format (bonus)
- [ ] Agent has single responsibility
- [ ] Minimal code examples in prompt
- [ ] Tools list minimized (or omitted)

### Skill Reference (A-SK-*)
- [ ] Referenced skills exist (if `skills:` field present)
- [ ] `Skill` tool available (if `skills:` field present)
- [ ] No content duplication with skill

## Common Generation Mistakes

### Mistake 1: Vague Description
❌ **Bad**:
```yaml
description: Helps with Python development
```

✅ **Good**:
```yaml
description: |
  Python expert. Use PROACTIVELY for FastAPI development, type hints,
  and async patterns. Specializes in modern Python 3.10+ with Pydantic
  validation.

  <example>
  user: "Create a FastAPI endpoint"
  assistant: "I'll use the python-fastapi-specialist to build a
             properly structured async endpoint."
  </example>
```

### Mistake 2: No Examples in Description
❌ **Bad**:
```yaml
description: API testing specialist. Use when testing APIs.
```

✅ **Good**:
```yaml
description: |
  API testing expert. Use when creating REST API tests or validating
  endpoints. Specializes in Jest, Supertest, and async patterns.

  <example>
  user: "Write tests for my user endpoint"
  assistant: "I'll use the api-testing-specialist to create
             comprehensive tests with validation."
  </example>
```

### Mistake 3: Invalid Name Pattern
❌ **Bad**:
```yaml
name: Python_Helper
name: fastapi-v2
name: my_agent
```

✅ **Good**:
```yaml
name: python-fastapi-specialist
name: api-testing-specialist
name: code-review-specialist
```

### Mistake 4: Bloated System Prompt
❌ **Bad**: 300 lines with extensive code examples

✅ **Good**: Extract examples to skill, keep prompt under 200 lines

### Mistake 5: No Workflow
❌ **Bad**:
```markdown
You are a Python expert. Help with Python code.
```

✅ **Good**:
```markdown
## When Invoked

1. **Analyze the request** - Understand what functionality is needed
2. **Check existing code** - Read relevant files
3. **Load the python skill** - Reference patterns and conventions
4. **Implement solution** - Write code following best practices
5. **Verify quality** - Check type hints, tests, documentation
```

### Mistake 6: Duplicating Skill Content
❌ **Bad**: Agent includes same code examples as skill

✅ **Good**: Agent references skill, doesn't duplicate

### Mistake 7: Missing Skill Tool
❌ **Bad**:
```yaml
skills: python-fastapi
tools: Read, Write, Edit  # Missing Skill tool!
```

✅ **Good**:
```yaml
skills: python-fastapi
tools: Read, Write, Edit, Skill
```

Or omit tools entirely to inherit all.

## Post-Generation Validation

### Step 1: Run Agent Auditor
```
Load agent-auditor skill
Audit .claude/agents/{name}-specialist.md
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

### Step 4: Test Invocation
Create a test scenario:
```
User request: "{example-from-description}"
Expected: Agent should be invoked
Verify: Check that trigger terms match
```

## Integration with Skill Creator

When generating agent+skill pairs:

### Generation Order
1. **Generate skill first** (knowledge base)
2. **Generate agent second** (references skill)

### Consistency Checks
- Agent name: `{domain}-specialist`
- Skill name: `{domain}`
- Agent `skills:` field includes skill name
- Agent step 3 references skill loading
- No content duplication between agent and skill

### Harmonization Audit
After generating both:
```
Load agent-auditor and skill-auditor
Run harmonization audit on pair
Verify both score 9+/10
Check no duplication detected
```

## Quick Reference

### Frontmatter Quick Fill
```yaml
---
name: {domain}-specialist
description: |
  {One-liner}. Use {when} for {tasks}. Specializes in {capabilities}.

  <example>
  user: "{request}"
  assistant: "{response}"
  </example>
tools: {omit or minimal list}
skills: {skill-name}  # if using skill
model: sonnet  # or opus, haiku
---
```

### System Prompt Structure
```markdown
You are an expert {domain} developer...

## When Invoked
1-6 steps

## When NOT to Invoke
3-5 boundaries

## Core Expertise
4-5 areas

## Methodology
5-7 steps

## Quality Standards
6-10 checklist items

## Constraints
DO NOT / ALWAYS lists

## Response Format
3-4 sections
```

### Target Metrics
- Description: 200-500 chars with examples
- System prompt: <100 lines (optimal), <200 lines (max)
- When Invoked: 5-6 steps
- Core Expertise: 4-5 areas
- Quality checklist: 6-10 items
- Auditor score: 9+/10
