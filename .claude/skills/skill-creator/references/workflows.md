# Skill Creation Workflows

## Overview

This document provides detailed multi-step workflows for creating, testing, and integrating skills into the orchestration framework.

## Pattern 1: Requirements Gathering Workflow

### When to Use

Use this workflow when starting a new skill from scratch or when the user's requirements are unclear.

### Implementation

**Step 1: Identify the Domain**
- Ask: "What domain or area does this skill cover?"
- Look for: Specific technology, workflow, or problem area
- Examples: "API testing", "Database migrations", "React components"

**Step 2: Define the Problem**
- Ask: "What problems will this skill solve?"
- Look for: Pain points, repetitive tasks, knowledge gaps
- Examples: "Writing consistent API tests", "Safe schema changes", "Type-safe components"

**Step 3: Determine Scope**
- Ask: "What should be included? What should be excluded?"
- Look for: Clear boundaries, related but separate concerns
- Examples:
  - Include: Jest setup, Supertest patterns, async testing
  - Exclude: Unit testing, E2E testing (separate skills)

**Step 4: Identify Prerequisites**
- Ask: "What tools, frameworks, or knowledge are required?"
- Look for: Dependencies, assumed knowledge, tool versions
- Examples: "Node.js, Jest 29+, basic HTTP knowledge"

**Step 5: Sketch Use Cases**
- Ask: "Can you describe 2-3 scenarios where you'd use this skill?"
- Look for: Concrete examples, different complexity levels
- Examples: "Testing GET endpoint", "Testing POST with auth", "Testing error responses"

### Example

**User:** "I need help with Unreal Engine blueprints"

**Workflow:**
1. **Domain:** Unreal Engine visual scripting
2. **Problem:** Creating complex blueprint logic, debugging visual scripts
3. **Scope:**
   - Include: Blueprint creation, node patterns, debugging
   - Exclude: C++ integration (separate skill), UI widgets (separate skill)
4. **Prerequisites:** Unreal Engine 5.x, basic blueprint knowledge
5. **Use Cases:**
   - Creating actor components
   - Implementing gameplay mechanics
   - Debugging blueprint logic

**Result:** Skill named `unreal-blueprints` focused on visual scripting patterns

## Pattern 2: Skill Planning Workflow

### When to Use

After requirements gathering, use this to structure the skill content.

### Implementation

**Step 1: Choose the Name**
- Apply naming conventions:
  - Single word if possible: `react`, `python`
  - Hyphenate for clarity: `api-testing`, `database-migration`
  - Max 3 words: `react-component-testing`
- Avoid: versions, temporal refs, generic suffixes
- Test: Say it out loud - does it clearly describe the domain?

**Step 2: Write the Description**
- Template: "{What} for {Domain}. Use when {Trigger}."
- Examples:
  - "Guide for creating REST API tests with Jest. Use when building test suites."
  - "Patterns for migrating PostgreSQL databases. Use when planning schema changes."
- Keep under 200 characters
- Make trigger explicit

**Step 3: Define Core Content (SKILL.md)**
- Must include:
  - Role statement
  - Purpose (2-3 paragraphs)
  - Quick start (3 steps)
  - 2-4 core sections
  - Common pitfalls (3+)
  - When to load references
  - 2-3 examples
- Target: 300-450 lines (leave room for growth)

**Step 4: Identify Reference Content**
- Split if:
  - Deep technical detail needed
  - Multiple workflow variations exist
  - Large code examples required
  - Troubleshooting needs its own section
- Reference types:
  - `workflows.md` - Multi-step processes
  - `patterns.md` - Code/config patterns
  - `examples.md` - Complete working examples
  - `troubleshooting.md` - Common issues
  - `integration.md` - Framework connections

**Step 5: Create Content Outline**

SKILL.md outline:
```
1. Frontmatter (name, description)
2. Title and role statement
3. Purpose
4. Quick Start (3 steps)
5. Core Section 1 (essential pattern/knowledge)
6. Core Section 2 (essential pattern/knowledge)
7. Core Section 3 (essential pattern/knowledge)
8. Core Section 4 (optional)
9. Common Pitfalls (3-5 items)
10. When to Load References
11. Examples (2-3)
```

References outline (per file):
```
1. Title and overview
2. Pattern 1 (when to use, implementation, example)
3. Pattern 2 (when to use, implementation, example)
4. Pattern 3 (when to use, implementation, example)
5. Pattern 4-6 (if needed)
```

### Example

**Planning `api-testing` skill:**

**Name:** `api-testing` (clear, specific, domain-focused)

**Description:** "Guide for creating REST API tests with Jest and Supertest. Use when building API test suites or validating endpoints."

**Core Content (SKILL.md):**
- Role: "You are the API Testing Guide"
- Purpose: Why API testing matters, what this skill provides
- Quick Start: Setup Jest/Supertest, write first test, run suite
- Core Sections:
  1. Test structure (describe/it, setup/teardown)
  2. Request patterns (GET, POST, PUT, DELETE)
  3. Response validation (status, body, headers)
  4. Error handling (4xx, 5xx responses)
- Common Pitfalls: Async issues, database state, authentication
- Examples: Basic GET test, POST with validation, authenticated request

**Reference Content:**
- `workflows.md`: Complete test suite creation process
- `patterns.md`: Advanced patterns (mocking, fixtures, parallel tests)
- `examples.md`: Full test files for different scenarios

## Pattern 3: Testing and Validation Workflow

### When to Use

After creating skill files, use this to verify quality and completeness.

### Implementation

**Step 1: Structural Validation**

Check SKILL.md:
- [ ] Frontmatter present with name and description
- [ ] Name matches directory name
- [ ] Description under 200 characters
- [ ] Role statement present
- [ ] Purpose section 2-3 paragraphs
- [ ] Quick Start has 3 steps
- [ ] 2-4 core sections present
- [ ] Common Pitfalls has 3+ items
- [ ] When to Load References section present
- [ ] 2-3 examples present
- [ ] Total under 500 lines

Check references/:
- [ ] Each file 200-500 lines
- [ ] Clear section structure
- [ ] Working examples for each pattern
- [ ] Cross-references where needed

**Step 2: Content Validation**

SKILL.md quality:
- [ ] Role is clear and specific
- [ ] Purpose explains value, not just description
- [ ] Quick Start is actionable (not just reading)
- [ ] Core sections teach essential knowledge
- [ ] Pitfalls show wrong vs. right approach
- [ ] Examples are complete and working
- [ ] References have clear triggers

Reference quality:
- [ ] Each pattern has "When to Use"
- [ ] Implementation steps are clear
- [ ] Examples are complete and realistic
- [ ] Code is correctly formatted
- [ ] Cross-references are accurate

**Step 3: Integration Validation**

Framework fit:
- [ ] Skill name follows conventions
- [ ] Description follows pattern
- [ ] No version numbers or temporal refs
- [ ] No implementation details in name
- [ ] Trigger is explicit in description
- [ ] References use standard naming

**Step 4: Example Testing**

Test each example:
- [ ] Example has clear context
- [ ] Code is syntactically correct
- [ ] Example demonstrates core concept
- [ ] Example is self-contained
- [ ] Example matches framework patterns

**Step 5: User Testing**

Simulate invocation:
- [ ] Read description - is trigger clear?
- [ ] Read Quick Start - can I start immediately?
- [ ] Read Core Section - do I understand the pattern?
- [ ] Read Example - can I adapt to my use case?
- [ ] Check References - do I know when to load them?

### Example

**Validating `database-migration` skill:**

**Structural:**
- ✅ Frontmatter: name=database-migration, description under 200 chars
- ✅ Role: "You are the Database Migration Guide"
- ✅ Purpose: 3 paragraphs on safe migrations
- ✅ Quick Start: Plan migration, write script, test rollback
- ✅ Core: Schema patterns, data transforms, zero-downtime, rollback
- ✅ Pitfalls: Foreign keys, data loss, rollback failures (4 items)
- ✅ Examples: Add column, rename table, data migration
- ✅ Total: 387 lines

**Content:**
- ✅ Quick Start is actionable steps
- ✅ Core sections teach patterns, not theory
- ✅ Pitfalls show specific errors and fixes
- ✅ Examples include SQL and rollback scripts

**Integration:**
- ✅ Name: No version, no temporal refs
- ✅ Description: Clear trigger ("when planning schema changes")
- ✅ References: workflows.md, patterns.md, troubleshooting.md

**Result:** Skill is ready for use

## Pattern 4: Integration Workflow

### When to Use

After validation, use this to integrate the skill into the framework.

### Implementation

**Step 1: File Placement**

Create structure:
```bash
.claude/skills/{skill-name}/
├── SKILL.md
└── references/
    ├── workflows.md       # If needed
    ├── patterns.md        # If needed
    ├── examples.md        # If needed
    └── troubleshooting.md # If needed
```

**Step 2: Documentation Updates**

Update relevant docs:
- Add skill to skills registry (if exists)
- Update README if skill is framework-critical
- Add to examples in DOCUMENTATION.md (if applicable)

**Step 3: Cross-Reference Updates**

Update related skills:
- Add references in related skills
- Update command files that might invoke this skill
- Add to agent definitions that should use this skill

**Step 4: Testing Integration**

Test skill invocation:
1. Invoke skill with typical scenario
2. Verify guidance is clear and actionable
3. Test reference loading
4. Verify examples work
5. Check integration with existing patterns

**Step 5: Documentation**

Document in STATE.md or CLAUDE.md:
- Skill created: name and purpose
- Integration points: what it connects to
- Usage examples: when to invoke
- Future enhancements: what's missing

### Example

**Integrating `api-testing` skill:**

**File Placement:**
```
.claude/skills/api-testing/
├── SKILL.md (412 lines)
└── references/
    ├── workflows.md (287 lines)
    ├── patterns.md (356 lines)
    └── examples.md (423 lines)
```

**Documentation:**
- Added to CLAUDE.md under skill references
- Referenced in `testing-strategy` skill
- Added example invocation to README

**Cross-References:**
- `react-typescript` skill references for component testing
- `/test` command updated to suggest api-testing skill
- `backend-agent` configured to use api-testing

**Testing:**
- Invoked with "I need to test a REST API"
- Verified Quick Start is actionable
- Loaded workflows.md for complete process
- Tested example code - all working

**Result:** Skill is fully integrated

## Complete Skill Creation Process

### End-to-End Example: Creating `unreal-engine` Skill

**Phase 1: Requirements (Pattern 1)**

User: "I need help with Unreal Engine development"

Questions:
1. "What aspects of Unreal Engine?" → "Blueprints, C++, packaging"
2. "What problems?" → "Setting up projects, managing assets, debugging"
3. "What's in scope?" → "Project setup, blueprint patterns, C++ integration"
4. "Prerequisites?" → "UE 5.3+, basic C++ knowledge"
5. "Use cases?" → "Creating gameplay systems, optimizing performance, packaging builds"

**Phase 2: Planning (Pattern 2)**

Name: `unreal-engine`
Description: "Guide for Unreal Engine 5 development with Blueprints and C++. Use when creating gameplay systems, optimizing projects, or debugging UE applications."

Core Content:
- Role: "You are the Unreal Engine Development Guide"
- Purpose: Accelerating UE5 development, avoiding common pitfalls
- Quick Start: Create project, set up version control, create first blueprint
- Core Sections:
  1. Project structure (folders, naming, organization)
  2. Blueprint patterns (components, interfaces, communication)
  3. C++ integration (exposing to blueprints, hot reload)
  4. Debugging (blueprint debugging, C++ debugging, profiling)
- Pitfalls: Blueprint spaghetti, memory leaks, packaging errors
- Examples: Actor component, gameplay system, C++ blueprint function

Reference Content:
- `workflows.md`: Project setup, build pipeline, packaging
- `patterns.md`: Blueprint best practices, C++ patterns, optimization
- `troubleshooting.md`: Common errors and fixes

**Phase 3: Creation**

Write SKILL.md (428 lines):
- Frontmatter with name and description
- Role and purpose sections
- Quick Start: 3 actionable steps
- 4 core sections with essential knowledge
- 5 common pitfalls with solutions
- When to load references
- 3 examples: Blueprint component, C++ function, gameplay system

Write references/workflows.md (312 lines):
- Project setup workflow
- Build pipeline workflow
- Packaging workflow
- Each with step-by-step instructions and examples

Write references/patterns.md (389 lines):
- Blueprint communication patterns
- C++ blueprint integration patterns
- Performance optimization patterns
- Each with when to use, implementation, and example

Write references/troubleshooting.md (267 lines):
- Blueprint compilation errors
- C++ hot reload failures
- Packaging errors
- Runtime crashes
- Each with diagnosis and solution

**Phase 4: Validation (Pattern 3)**

Structural:
- ✅ SKILL.md: 428 lines (under 500)
- ✅ References: 312, 389, 267 lines (all in range)
- ✅ Frontmatter correct
- ✅ All sections present

Content:
- ✅ Quick Start is actionable
- ✅ Examples are complete and working
- ✅ Pitfalls show wrong vs. right
- ✅ References have clear triggers

Integration:
- ✅ Name follows conventions
- ✅ Description has clear trigger
- ✅ No temporal references

**Phase 5: Integration (Pattern 4)**

File Placement:
```
.claude/skills/unreal-engine/
├── SKILL.md
└── references/
    ├── workflows.md
    ├── patterns.md
    └── troubleshooting.md
```

Cross-References:
- Added to `cpp-development` skill
- Referenced in `game-development` agent
- Added example to DOCUMENTATION.md

Testing:
- Invoked with "I'm creating an Unreal Engine game"
- Verified guidance is clear
- Tested example blueprint code
- All working

**Result:** Complete, validated, integrated skill ready for use
