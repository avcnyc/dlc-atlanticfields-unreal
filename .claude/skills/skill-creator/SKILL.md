---
name: skill-creator
description: Guide for creating effective skills that fit this framework. Use when users want to create a new skill that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

You are the Skill Creator, responsible for helping users design and implement new skills that extend the orchestration framework.

## Purpose

Skills are specialized knowledge modules that Claude can invoke to handle specific domains, workflows, or technical integrations. A well-designed skill provides:

- **Focused Expertise** - Deep knowledge in one area
- **Clear Activation** - Obvious when to invoke the skill
- **Self-Contained** - All necessary context included
- **Actionable Guidance** - Step-by-step instructions, not theory
- **Reference System** - Additional detail available on-demand
- **Auditor Compliance** - Passes skill-auditor validation at 9+/10

The Skill Creator uses auditor rules as generation constraints to ensure new skills are compliant from the start, preventing common issues like missing sections, behavioral content, oversized files, and poor descriptions.

## Quick Start

### Step 1: Understand the Need

Ask the user:
- **What domain or workflow does this skill address?**
- **What problems will this skill solve?**
- **What tools or integrations are required?**
- **What expertise should Claude gain from this skill?**

### Step 2: Plan the Structure

Determine:
- **Skill name** - Single word, lowercase, hyphenated if needed
- **Core content** - What goes in SKILL.md (under 500 lines)
- **Reference content** - What detail belongs in references/ (200-500 lines each)
- **Examples needed** - Real-world usage patterns
- **Integration points** - How it connects to framework

### Step 3: Create the Skill

1. Select template from `references/templates/` (skill-template.md or skill-with-agent-template.md)
2. Create directory: `.claude/skills/{skill-name}/`
3. Write SKILL.md with frontmatter and core guidance
4. Create references/ directory if needed
5. Write reference files with detailed patterns
6. Run skill-auditor to verify quality (target 9+/10)

## Skill Structure

```
.claude/skills/{skill-name}/
├── SKILL.md              # Main skill file (< 500 lines)
└── references/           # Optional detailed references
    ├── workflows.md      # Multi-step processes (200-500 lines)
    ├── patterns.md       # Code/config patterns (200-500 lines)
    └── examples.md       # Complete examples (200-500 lines)
```

## SKILL.md Template

```markdown
---
name: {skill-name}
description: {One sentence describing when to use this skill}
---

# {Skill Title}

You are the {Role Name}, responsible for {primary responsibility}.

## Purpose

{2-3 paragraphs explaining:
- What this skill provides
- Why it's valuable
- What it enables}

## Quick Start

### Step 1: {First Action}
{Instructions}

### Step 2: {Second Action}
{Instructions}

### Step 3: {Third Action}
{Instructions}

## {Core Section 1}

{Essential knowledge or patterns}

## {Core Section 2}

{Essential knowledge or patterns}

## {Core Section 3}

{Essential knowledge or patterns}

## Common Pitfalls

- ❌ **{Mistake}** - {Why it's wrong} → ✅ **{Correct approach}**
- ❌ **{Mistake}** - {Why it's wrong} → ✅ **{Correct approach}**
- ❌ **{Mistake}** - {Why it's wrong} → ✅ **{Correct approach}**

## When to Load References

Load `references/{file}.md` when:
- **{Trigger condition}** - Load {file}.md
- **{Trigger condition}** - Load {file}.md
- **{Trigger condition}** - Load {file}.md

## Examples

### Example 1: {Scenario}
{Working example with context}

### Example 2: {Scenario}
{Working example with context}
```

## Frontmatter Requirements

```yaml
---
name: skill-name              # Lowercase, hyphenated, matches directory
description: {description}    # One clear sentence starting with action verb
---
```

**Name Pattern:**
- Single concept: `react`, `python`, `unreal-engine`
- Combined: `skill-creator`, `api-testing`, `db-migration`
- Max 3 words: `react-component-testing`

**Description Pattern:**
- Start with context: "Guide for...", "Patterns for...", "Workflow for..."
- Include trigger: "Use when..."
- Keep under 200 characters
- Be specific and actionable

## Framework Integration

### Naming Conventions

**DO:**
- `api-testing` - Clear, specific
- `database-migration` - Domain-focused
- `error-handling` - Problem-focused

**DON'T:**
- `api-testing-v2` - No versions
- `new-api-tester` - No temporal references
- `api-testing-helper` - No generic suffixes

### Description Patterns

**Good Descriptions:**
```yaml
description: Guide for creating REST API tests with Jest and Supertest. Use when building API test suites or validating endpoints.

description: Patterns for migrating PostgreSQL databases safely. Use when planning schema changes or data migrations.

description: Workflow for implementing error boundaries in React applications. Use when handling component errors or improving error UX.
```

**Bad Descriptions:**
```yaml
description: Helps with API testing  # Too vague

description: API testing skill for when you need to test APIs  # Redundant

description: Use this when testing  # No context
```

### Reference Structure

**When to Split into References:**
- SKILL.md approaching 500 lines
- Deep technical patterns needed
- Multiple workflow variations
- Large code examples

**Reference File Naming:**
- `workflows.md` - Multi-step processes
- `patterns.md` - Code/config patterns
- `examples.md` - Complete working examples
- `troubleshooting.md` - Common issues and fixes
- `integration.md` - Framework integration details

**Reference File Structure:**
```markdown
# {Reference Topic}

## Overview
{Brief introduction}

## Pattern 1: {Name}

### When to Use
{Trigger conditions}

### Implementation
{Step-by-step or code example}

### Example
{Working example}

## Pattern 2: {Name}
...
```

## Content Guidelines

### Core Content (SKILL.md)

**Include:**
- Role statement and purpose
- Quick start steps
- Essential patterns and knowledge
- Common pitfalls with solutions
- When to load references
- 2-3 working examples

**Exclude:**
- Deep implementation details (use references/)
- Large code blocks (use references/examples.md)
- Multiple workflow variations (use references/workflows.md)
- Exhaustive troubleshooting (use references/troubleshooting.md)

### Reference Content

**Include:**
- Detailed step-by-step workflows
- Complete code examples
- Pattern variations
- Edge cases and troubleshooting
- Integration details

**Structure:**
- 200-500 lines per file
- Clear section headers
- Working examples for each pattern
- Cross-references to other files

## Common Pitfalls

- ❌ **Too Broad** - Skill covers multiple unrelated domains → ✅ **Split into focused skills**
- ❌ **Too Long** - SKILL.md exceeds 500 lines → ✅ **Move detail to references/**
- ❌ **No Examples** - Pure theory without working code → ✅ **Include 2-3 real examples**
- ❌ **Vague Description** - "Helps with testing" → ✅ **"Guide for creating API tests with Jest"**
- ❌ **Generic Name** - "helper", "utils", "tools" → ✅ **Domain-specific name**
- ❌ **No Trigger** - Unclear when to invoke → ✅ **Explicit "Use when..." in description**
- ❌ **Implementation Detail** - "Uses Express" in name → ✅ **"API testing" (tool-agnostic)**
- ❌ **Temporal Reference** - "New", "Legacy", "V2" → ✅ **Timeless naming**

## When to Load References

Load `references/workflows.md` when:
- **Multi-step process needed** - User needs complete workflow guidance
- **Planning new skill** - Understanding skill creation process
- **Complex integration** - Skill interacts with multiple framework components

Load `references/output-patterns.md` when:
- **Writing SKILL.md** - Need quality standards and templates
- **Creating reference files** - Need structure and formatting guidance
- **Quality review** - Verifying skill completeness

Load `references/templates/skill-template.md` when:
- **Creating standalone skill** - Skill with no paired agent
- **Need base scaffold** - Starting point for any skill

Load `references/templates/skill-with-agent-template.md` when:
- **Creating skill for agent** - Skill paired with agent for harmonization
- **Ensuring agent-skill consistency** - Following harmonization patterns

## Workflow

### Initial Conversation

1. **Understand the need:**
   - "What problem are you solving?"
   - "What domain expertise should this provide?"
   - "What tools or integrations are involved?"

2. **Plan the skill:**
   - Name the skill
   - Define scope (what's in, what's out)
   - Identify core vs. reference content
   - Sketch example use cases

3. **Create the structure:**
   - Generate SKILL.md with frontmatter
   - Write core sections
   - Identify reference needs
   - Create reference files if needed

### Verification

Before completing, check:

- [ ] **Name** - Lowercase, hyphenated, descriptive
- [ ] **Description** - Clear trigger, under 1024 chars, third person
- [ ] **SKILL.md** - Under 500 lines
- [ ] **Role statement** - Clear responsibility
- [ ] **Quick start** - 3 actionable steps
- [ ] **Core sections** - Essential knowledge only
- [ ] **Common pitfalls** - At least 3 with solutions
- [ ] **References section** - Clear triggers for loading
- [ ] **Examples** - 2-3 working examples
- [ ] **Reference files** - 200-500 lines each if present
- [ ] **No behavioral content** - No "When Invoked" workflow steps
- [ ] **Run skill-auditor** - Verify score is 9+/10

## Examples

### Example 1: Creating an API Testing Skill

**User Request:** "I need help creating API tests with Jest and Supertest"

**Process:**
1. **Name:** `api-testing`
2. **Description:** "Guide for creating REST API tests with Jest and Supertest. Use when building API test suites or validating endpoints."
3. **Core Content:**
   - Quick start: Setup, write first test, run suite
   - Essential patterns: Request testing, response validation, error handling
   - Common pitfalls: Async issues, database state, authentication
4. **Reference Content:**
   - `workflows.md` - Complete test suite creation process
   - `patterns.md` - Advanced testing patterns (mocking, fixtures, etc.)
   - `examples.md` - Full test files for different API types

### Example 2: Creating a Database Migration Skill

**User Request:** "I want a skill for PostgreSQL schema migrations"

**Process:**
1. **Name:** `database-migration`
2. **Description:** "Patterns for migrating PostgreSQL databases safely. Use when planning schema changes or data migrations."
3. **Core Content:**
   - Quick start: Plan migration, write script, test rollback
   - Essential patterns: Schema changes, data transformations, zero-downtime
   - Common pitfalls: Foreign keys, data loss, rollback failures
4. **Reference Content:**
   - `workflows.md` - Complete migration process from planning to deployment
   - `patterns.md` - Migration script patterns for different scenarios
   - `troubleshooting.md` - Common migration issues and fixes

### Example 3: Creating a React Component Skill

**User Request:** "Need guidance for building React components with TypeScript"

**Process:**
1. **Name:** `react-typescript`
2. **Description:** "Guide for building type-safe React components with TypeScript. Use when creating React components or implementing TypeScript patterns."
3. **Core Content:**
   - Quick start: Create component, add types, implement logic
   - Essential patterns: Props typing, event handlers, hooks
   - Common pitfalls: Type assertions, any types, generic components
4. **Reference Content:**
   - `patterns.md` - Advanced TypeScript patterns for React
   - `examples.md` - Complete component examples (forms, lists, async)
   - `integration.md` - Integrating with state management, routing, etc.
