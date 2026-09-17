# XML Patterns for Prompt Engineering

## Table of Contents

1. [Overview](#overview)
2. [Core Tags](#core-tags)
3. [Tag Naming Conventions](#tag-naming-conventions)
4. [Nesting Patterns](#nesting-patterns)
5. [Task-Specific Tag Sets](#task-specific-tag-sets)
6. [Complete Examples](#complete-examples)

## Overview

### Why XML Tags Matter

Claude was trained with XML tags in the training data, making them the optimal structuring mechanism. Benefits:

- **Clarity** - Separate different parts cleanly
- **Accuracy** - Reduce misinterpretation through explicit boundaries
- **Flexibility** - Easily modify sections without affecting others
- **Parseability** - Extract structured outputs

XML tags act as semantic containers telling Claude "this section contains X type of information." Unlike markdown headers which are visual, XML tags have semantic meaning Claude recognizes during instruction following.

## Core Tags

### Essential Tags for All Prompts

**`<objective>`** - Clear statement of what to build and why
```xml
<objective>
Create user authentication system with JWT tokens.
Include registration, login, and password reset.
WHY: Secure user access and protect sensitive data.
</objective>
```

**`<context>`** - Background, motivation, dependencies
```xml
<context>
Current state:
- Express.js API with no authentication
- PostgreSQL database configured
- Need to secure 12 existing endpoints

WHY: 60% of endpoints expose sensitive user data.
</context>
```

**`<requirements>`** - Specific, explicit requirements
```xml
<requirements>
<requirement name="backend">
  <file path="src/routes/auth.js">
    <purpose>Authentication route handlers</purpose>
    <specifications>
      - POST /api/auth/register
      - POST /api/auth/login
      - Input validation with Joi
    </specifications>
  </file>
</requirement>
</requirements>
```

**`<constraints>`** - Boundaries with WHY explanations
```xml
<constraints>
- Under 500 lines

  WHY: Keeps implementation focused and auditable.

- No plaintext passwords

  WHY: Security requirement, must use bcrypt hashing.
</constraints>
```

**`<examples>`** - Correct and incorrect demonstrations
```xml
<examples>
<example name="correct">
  <scenario>When to use this pattern</scenario>
  <implementation>
  ```javascript
  // Code example
  ```
  </implementation>
  <quality_markers>
    - Why this is good
  </quality_markers>
</example>

<example name="avoid">
  <scenario>Anti-pattern to AVOID</scenario>
  <why_avoid>Why this fails</why_avoid>
</example>
</examples>
```

**`<output>`** - Exact format specification
```xml
<output>
Create files using relative paths:
- ./src/auth/routes.js - Authentication endpoints
- ./src/auth/controllers.js - Business logic

Format: Markdown with code blocks
WHY: Readable in terminal and can be saved to docs
</output>
```

**`<verification>`** - How to validate success
```xml
<verification>
Structural:
- [ ] All files created at specified paths
- [ ] No syntax errors

Functional:
- [ ] Registration creates user with hashed password
- [ ] Login returns valid JWT token

Testing:
- [ ] Run npm test - all tests pass
</verification>
```

## Tag Naming Conventions

### Good Tag Names (Semantic)
- `<objective>` - Clear purpose
- `<context>` - Background info
- `<requirements>` - Specifications
- `<constraints>` - Boundaries
- `<examples>` - Demonstrations
- `<verification>` - Validation
- `<output>` - Deliverables

### Avoid (Too Generic)
- `<info>` - What kind?
- `<data>` - What data?
- `<stuff>` - Unclear
- `<section>` - Non-specific

## Nesting Patterns

### Hierarchical Requirements

```xml
<requirements>
  <requirement name="backend">
    <file path="src/routes/auth.js">
      <purpose>Authentication endpoints</purpose>
      <specifications>
        - POST /api/auth/register
        - POST /api/auth/login
      </specifications>
    </file>
  </requirement>

  <requirement name="tests">
    <file path="tests/auth.test.js">
      <purpose>Test suite</purpose>
      <specifications>
        - Unit tests for controllers
        - Integration tests for endpoints
      </specifications>
    </file>
  </requirement>
</requirements>
```

### Multi-Level Context

```xml
<context>
  <current_state>
    <backend>
      - Express.js 4.18 server
      - PostgreSQL 14 database
    </backend>
    <frontend>
      - React 18 with TypeScript
      - Redux for state
    </frontend>
  </current_state>

  <problem>
    <description>No authentication exists</description>
    <impact>Security vulnerability</impact>
  </problem>
</context>
```

## Task-Specific Tag Sets

### Coding Task Tags
```xml
<objective>What to build</objective>
<context>Current state, why needed</context>
<requirements>File-by-file specs</requirements>
<constraints>Boundaries and limits</constraints>
<examples>Code demonstrations</examples>
<parallel_tool_calling>Tool optimization</parallel_tool_calling>
<output>Deliverables</output>
<verification>Validation</verification>
```

### Analysis Task Tags
```xml
<objective>What to analyze</objective>
<analysis_focus>High-level guidance (extended thinking)</analysis_focus>
<data_sources>Files, commands to examine</data_sources>
<parallel_tool_calling>Read files simultaneously</parallel_tool_calling>
<output_format>Structure for findings</output_format>
<verification>Completeness checks</verification>
```

### Research Task Tags
```xml
<research_objective>What to research</research_objective>
<scope>Focus areas and boundaries</scope>
<research_process>Discovery, gathering, synthesis</research_process>
<deliverables>Output files and structure</deliverables>
<verification>Coverage and quality</verification>
```

### Multi-Step Task Tags
```xml
<objective>Overall goal (step N of M)</objective>
<sequence_context>Previous, current, next</sequence_context>
<dependencies>What required and produced</dependencies>
<execution_strategy>PARALLEL or SEQUENTIAL</execution_strategy>
<state_management>Before/after tracking</state_management>
```

## Complete Examples

### Coding Task with XML

```xml
<objective>
Implement JWT authentication for Express.js API.
Include registration, login, and protected route middleware.
</objective>

<context>
Current state:
- Express.js API with 12 public endpoints
- PostgreSQL database with User model
- No authentication or authorization

WHY: 8 of 12 endpoints expose sensitive data requiring authentication.
</context>

<requirements>
<requirement name="authentication">
  <file path="src/routes/auth.js">
    <purpose>Authentication endpoints</purpose>
    <specifications>
      - POST /api/auth/register
      - POST /api/auth/login
      - POST /api/auth/refresh
    </specifications>
  </file>

  <file path="src/middleware/authenticateToken.js">
    <purpose>Protect routes requiring authentication</purpose>
    <specifications>
      - Verify JWT from Authorization header
      - Attach user to req.user
      - Return 401 if invalid
    </specifications>
  </file>
</requirement>
</requirements>

<constraints>
- Under 400 lines

  WHY: Authentication should be focused and auditable.

- No plaintext passwords

  WHY: Security requirement. Must use bcrypt.

- JWT secret in environment variable

  WHY: Never hardcode secrets.
</constraints>

<parallel_tool_calling>
Read existing files simultaneously to understand integration points.
</parallel_tool_calling>

<output>
Create:
- ./src/routes/auth.js
- ./src/middleware/authenticateToken.js
- ./tests/auth.test.js

Provide:
- Summary of implementation
- Usage example (how to protect routes)
</output>

<verification>
Structural:
- [ ] All files created at correct paths
- [ ] No syntax errors

Functional:
- [ ] Registration creates user with hashed password
- [ ] Login returns valid JWT
- [ ] Protected routes reject invalid tokens

Testing:
- [ ] npm test passes
- [ ] Manual flow: Register → Login → Access protected route
</verification>
```

### Analysis Task with XML

```xml
<objective>
Analyze dashboard codebase to identify performance bottlenecks.
Target <500ms initial render.
</objective>

<analysis_focus>
Thoroughly analyze from multiple angles:
- Database queries and indexes
- Frontend rendering and bundle size
- Network requests and caching

Explore various optimization approaches before concluding.
</analysis_focus>

<data_sources>
Examine:
@src/pages/Dashboard.tsx
@src/api/analytics.ts
@backend/routes/dashboard.js

Commands:
!npm run build -- --analyze
!npm run lighthouse
</data_sources>

<parallel_tool_calling>
Read all source files simultaneously, then analyze together.
</parallel_tool_calling>

<output_format>
Save to: ./analyses/dashboard-performance.md

Structure:
## Executive Summary
[2-3 sentences]

## Findings
| File | Line | Issue | Severity | Impact |
|------|------|-------|----------|--------|

## Recommendations
1. [Priority 1 with expected improvement]
2. [Priority 2 with expected improvement]
</output_format>
```

### XML + Multishot + Chain of Thought

```xml
<analysis_task>
  <objective>Identify performance bottlenecks</objective>

  <examples>
    <example>
      <scenario>Analyzing slow query</scenario>
      <thinking>
        Examining query execution plan.
        Nested loop scanning 10k rows - bottleneck.
        Index on user_id would optimize to index seek.
      </thinking>
      <recommendation>
        CREATE INDEX idx_orders_user_id ON orders(user_id);
        Expected: 2000ms → 50ms
      </recommendation>
    </example>
  </examples>

  <output_format>
    For each bottleneck:
    1. File and line
    2. Analysis in `<thinking>` tags
    3. Recommendation
    4. Impact
  </output_format>
</analysis_task>
```

## Tag Combinations

### Parallel Tool Calling

```xml
<data_gathering>
  <parallel_tool_calling>
    Read simultaneously:
    - src/auth/routes.js
    - src/auth/controller.js
    - src/middleware/jwt.js

    All reads are independent and can run in parallel.
  </parallel_tool_calling>

  <analysis_focus>
    After gathering, analyze for security vulnerabilities.
  </analysis_focus>
</data_gathering>
```

### State Management for Multi-Step

```xml
<state_management>
Before starting:
- Read STATE.md to verify dependencies met
- Confirm expected files exist

After completing:
- Update STATE.md with progress
- Mark this prompt complete
- Set resume point for next prompt
</state_management>
```
