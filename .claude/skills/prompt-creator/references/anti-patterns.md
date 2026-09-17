# Anti-Patterns in Prompt Engineering

## Table of Contents

1. [Overview](#overview)
2. [Critical Anti-Patterns](#critical-anti-patterns)
   - [Vague Objectives](#1-vague-objectives)
   - [Missing Context](#2-missing-context)
   - [No Boundaries](#3-no-boundaries)
   - [Missing Verification](#4-missing-verification)
   - [Missing "Why" Explanations](#5-missing-why-explanations)
   - [Generic Specifications](#6-generic-specifications)
   - [Bad Examples](#7-bad-examples)
   - [Overly Prescriptive](#8-overly-prescriptive)
3. [Summary](#summary)

## Overview

Anti-patterns are common mistakes that lead to poor results from Claude. Each shows:
- **Bad** - Common mistake
- **Why it fails** - Root cause
- **Good** - What Claude needs

## Critical Anti-Patterns

### 1. Vague Objectives

**Bad:**
```xml
<objective>Make the app better</objective>
```

**Why it fails:** No specific action, no measurable outcome, infinite interpretation space.

**Good:**
```xml
<objective>
Improve dashboard load time from 3 seconds to under 500ms.
Implement query optimization, frontend caching, and lazy loading.

WHY: 40% of users abandon when load time exceeds 2 seconds.
</objective>
```

**Fix:**
- Use specific action verbs (Improve, Create, Implement)
- Quantify the goal (from X to Y)
- List specific approaches
- Always explain WHY

---

### 2. Missing Context

**Bad:**
```xml
<objective>Create a login component</objective>
<requirements>
- Email field
- Password field
</requirements>
```

**Why it fails:** Claude doesn't know current state, tech stack, integration points, or motivation.

**Good:**
```xml
<context>
Current state:
- React 18 app with TypeScript
- Using Tailwind CSS for styling
- Authentication API exists at /api/auth/login
- Other forms use React Hook Form library

Integration:
- Lives in src/components/LoginForm.tsx
- Called from pages/login.tsx

WHY: Current login has no validation, causing user confusion.
</context>
```

**Fix:**
- Describe current state (what exists, tech stack)
- Show how solution integrates
- List dependencies
- Always include WHY

---

### 3. No Boundaries

**Bad:**
```xml
<objective>Create a user dashboard with useful features</objective>
```

**Why it fails:** Infinite possibilities lead to generic, unfocused, over-engineered output.

**Good:**
```xml
<constraints>
Features (exactly these 4):
1. Recent activity feed (last 10 items)
2. Quick stats card (3 key metrics)
3. Action buttons (2 primary actions)
4. Profile summary (avatar + name + role)

Technical boundaries:
- Mobile-first responsive design
  WHY: 60% of users access from mobile

- Must load in under 1 second
  WHY: Performance budget requirement

- Maximum 300 lines of code
  WHY: Enforces component composition

WHY these features: User research showed these provide 80% of value while keeping dashboard focused.
</constraints>
```

**Fix:**
- Define exact features or deliverables
- Set quantitative limits
- Specify format/style boundaries
- Explain WHY each constraint exists
- Remember: constraints focus creativity

---

### 4. Missing Verification

**Bad:**
```xml
<objective>Build authentication system</objective>
<requirements>[Requirements listed]</requirements>
```

**Why it fails:** No definition of "done", Claude can't validate work, missing edge cases.

**Good:**
```xml
<verification>
Structural:
- [ ] All files created at specified paths
- [ ] No syntax errors (run linter)
- [ ] All functions have JSDoc comments
- [ ] No TODO or placeholder content

Functional:
- [ ] Registration creates user with hashed password
- [ ] Login returns valid JWT token
- [ ] Protected routes reject invalid tokens

Testing:
- [ ] Run npm test - all tests pass
- [ ] Manual test: Register → Login → Access protected route
- [ ] Error cases: Invalid email, duplicate user, wrong password

Integration:
- [ ] Works with existing Express middleware
- [ ] No breaking changes
</verification>
```

**Fix:**
- Include verification section with checklists
- Group checks by category (Structural, Functional, Testing, Integration)
- Specify commands to run
- List edge cases
- Define measurable success criteria

---

### 5. Missing "Why" Explanations

**Bad:**
```xml
<constraints>
- Under 500 lines
- No placeholders
- Use TypeScript
</constraints>
```

**Why it fails:** Claude doesn't understand reasoning, may work around constraints inappropriately.

**Good:**
```xml
<constraints>
- Under 500 lines
  WHY: Skills need to fit in a single reading. Longer content should be split.

- No placeholders or TODOs
  WHY: Prompts execute in isolated contexts. Placeholders cause execution failures.

- Use TypeScript with strict mode
  WHY: Type safety catches errors at compile time. Project standard for all new code.
</constraints>
```

**Fix:**
- Add "WHY:" explanation after every constraint
- Explain business reason or technical reason
- Help Claude understand intent, not just rules

---

### 6. Generic Specifications

**Bad:**
```xml
<requirements>
<file path="src/api/users.js">
  <specifications>
    - Create some API endpoints
    - Handle errors
  </specifications>
</file>
</requirements>
```

**Why it fails:** Too vague to implement, no specific endpoints, no error strategy.

**Good:**
```xml
<requirements>
<file path="src/api/users.js">
  <purpose>User CRUD API endpoints</purpose>
  <specifications>
    - GET /api/users - List users (paginated, 20 per page)
    - GET /api/users/:id - Get user by ID
    - POST /api/users - Create user
      - Input: { email, firstName, lastName }
      - Validation: Email format, required fields
      - Returns: 201 with created user

    Error handling:
    - 400 for validation errors
    - 404 for user not found
    - 500 for server errors

    Database:
    - Use Sequelize User model
    - All operations async/await
  </specifications>
</file>
</requirements>
```

**Fix:**
- List specific endpoints with HTTP methods
- Include input/output formats
- Specify validation rules
- Define error codes and handling
- Name exact libraries or functions

---

### 7. Bad Examples

**Bad:**
```xml
<examples>
<example>
app.get('/users', (req, res) => {
  const users = db.users;
  console.log('Fetched users');
  res.json(users);
});
</example>
</examples>
```

**Why it fails:** Example shows anti-patterns (console.log, synchronous, no error handling). Claude may mimic them.

**Good:**
```xml
<examples>
<example name="correct-api-pattern">
  <scenario>Fetching users with proper error handling</scenario>
  <implementation>
  ```javascript
  app.get('/api/users', async (req, res) => {
    try {
      const users = await db.users.findAll();
      logger.info(`Retrieved ${users.length} users`);
      res.json({ success: true, data: users });
    } catch (error) {
      logger.error('Failed to fetch users:', error);
      res.status(500).json({ success: false, error: 'Failed to retrieve users' });
    }
  });
  ```
  </implementation>
  <quality_markers>
    - Async/await for database operations
    - Try/catch error handling
    - Structured logging (not console.log)
    - Consistent response format
  </quality_markers>
</example>

<example name="avoid-this-antipattern">
  <scenario>Anti-pattern to AVOID</scenario>
  <bad_implementation>
  ```javascript
  app.get('/users', (req, res) => {
    const users = db.users;
    console.log('Fetched');
    res.json(users);
  });
  ```
  </bad_implementation>
  <why_avoid>
    - Synchronous database access (blocks event loop)
    - No error handling
    - console.log instead of structured logging
  </why_avoid>
</example>
</examples>
```

**Fix:**
- Always label examples clearly (correct vs incorrect)
- Show BOTH good and bad for contrast
- Explain why good examples are good
- Explain why bad examples fail
- Provide complete, working code (no placeholders or "...")

---

### 8. Overly Prescriptive

**Bad:**
```xml
<analysis_process>
Follow these exact steps:
1. List all files
2. Open the first file
3. Read line 1
4. Check if line 1 contains a function
5. If yes, record the function name
6. Move to line 2
[...50 more micro-steps]
</analysis_process>
```

**Why it fails:** Too prescriptive prevents extended thinking, micromanagement reduces quality. Claude 4.x excels at high-level guidance.

**Good:**
```xml
<analysis_objective>
Thoroughly analyze the codebase to identify all exported functions and their purposes.

Consider multiple approaches for discovering functions efficiently.
Evaluate tradeoffs between grep-based searching vs file-by-file analysis.
Explore how functions relate to each other and identify architectural patterns.
</analysis_objective>
```

**Fix:**
- Use high-level guidance, not step-by-step
- Trigger extended thinking with:
  - "Thoroughly analyze"
  - "Consider multiple approaches"
  - "Evaluate tradeoffs"
  - "Explore various solutions"
- Focus on goals, not methods
- Trust Claude's reasoning capabilities

---

## Summary

**Most anti-patterns stem from:**
1. **Lack of specificity** - Vague instead of concrete
2. **Missing context** - No "why" or background
3. **Assumed knowledge** - Expecting Claude knows your patterns
4. **No verification** - Can't validate results
5. **Bad examples** - Showing anti-patterns without labels
6. **Micromanagement** - Overly prescriptive for complex tasks

**Golden rules to avoid anti-patterns:**
- Be specific and explicit
- Always explain "WHY"
- Use XML structure for organization
- Include verification criteria
- Show both good and bad examples (labeled)
- Use firm, clear, respectful tone
- High-level guidance for complex tasks
- Make success criteria measurable
- Provide complete examples (no placeholders)
- Define exact boundaries and constraints
