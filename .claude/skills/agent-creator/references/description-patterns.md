# Agent Description Patterns

Collection of high-quality agent descriptions that achieve 5/5 auditor scores.

## Anatomy of an Excellent Description

A 5/5 description includes:
1. **WHAT** - What the agent does (clear capability statement)
2. **WHEN** - Trigger terms for invocation
3. **WHY** - Unique value or specialization
4. **EXAMPLES** - 2-3 `<example>` blocks showing usage
5. **PROACTIVE** (optional) - "Use PROACTIVELY" for auto-invocation

## Pattern Templates

### Pattern 1: PROACTIVE with Multiple Examples

```yaml
description: |
  Use PROACTIVELY for {domain} development: {capabilities-list}.
  Specializes in {unique-value}.

  <example>
  user: "{user-request-1}"
  assistant: "{agent-action-1}"
  </example>

  <example>
  user: "{user-request-2}"
  assistant: "{agent-action-2}"
  </example>

  <example>
  user: "{user-request-3}"
  assistant: "{agent-action-3}"
  </example>
```

**When to use**: Agents that should be invoked automatically based on keywords.

**Example** (TouchDesigner Python):
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

  <example>
  user: "Clean up my extension with proper type hints and docstrings"
  assistant: "I'll use the touchdesigner-python-specialist to refactor your
             extension with proper type hints, docstrings, and conventions."
  </example>

  <example>
  user: "Audit my TouchDesigner Python code for issues"
  assistant: "I'll have the touchdesigner-python-specialist review your
             extension for convention violations, missing type hints, and
             potential improvements."
  </example>
```

### Pattern 2: Use When + Specialization

```yaml
description: |
  {Role statement}. Use when {trigger-1}, {trigger-2}, or {trigger-3}.
  Specializes in {unique-capabilities}.

  <example>
  user: "{user-request}"
  assistant: "{agent-action}"
  </example>
```

**When to use**: Agents with clear, specific triggers.

**Example** (API Testing):
```yaml
description: |
  API testing expert with Jest and Supertest. Use when creating REST API
  tests, validating endpoints, or building test suites. Specializes in async
  test patterns and comprehensive coverage.

  <example>
  user: "Write tests for my user registration endpoint"
  assistant: "I'll use the api-testing-specialist to create comprehensive
             tests with request validation, error cases, and authentication."
  </example>

  <example>
  user: "How do I test async API calls?"
  assistant: "I'll use the api-testing-specialist to show you async testing
             patterns with proper setup and teardown."
  </example>
```

### Pattern 3: Domain Expert

```yaml
description: |
  {Domain} expert. {Brief capability statement}. Use for {task-1},
  {task-2}, and {task-3}. Specializes in {framework/technology} with
  {unique-approach}.

  <example>
  user: "{user-request}"
  assistant: "{agent-action}"
  </example>
```

**When to use**: Agents focused on a specific domain or technology.

**Example** (Python FastAPI):
```yaml
description: |
  FastAPI REST API expert. Modern Python 3.10+ async development. Use for
  endpoint creation, dependency injection, and Pydantic validation.
  Specializes in FastAPI best practices with type hints and async patterns.

  <example>
  user: "Create a FastAPI endpoint for user authentication"
  assistant: "I'll use the python-fastapi-specialist to build a secure
             async endpoint with JWT validation and proper error handling."
  </example>

  <example>
  user: "How do I add middleware to my FastAPI app?"
  assistant: "I'll use the python-fastapi-specialist to implement custom
             middleware following FastAPI patterns."
  </example>
```

### Pattern 4: Task-Oriented

```yaml
description: |
  {Task specialist}. {What it does}. Use PROACTIVELY {when-trigger}.
  {Unique-value}.

  <example>
  user: "{user-request}"
  assistant: "{agent-action}"
  </example>
```

**When to use**: Agents focused on specific tasks or workflows.

**Example** (Code Review):
```yaml
description: |
  Code quality reviewer. Analyzes changes for style, security, performance,
  and maintainability. Use PROACTIVELY after code changes to ensure quality
  standards. Provides actionable feedback with examples.

  <example>
  user: "Review this pull request"
  assistant: "I'll have the code-review-specialist analyze the changes for
             quality, security vulnerabilities, and best practices."
  </example>

  <example>
  user: "Check if my code follows best practices"
  assistant: "I'll use the code-review-specialist to audit your code against
             established patterns and conventions."
  </example>
```

### Pattern 5: Framework Specialist

```yaml
description: |
  {Framework} development expert. {Capabilities}. Use when {building/implementing}
  {framework-features}. Specializes in {version} with {patterns}.

  <example>
  user: "{user-request}"
  assistant: "{agent-action}"
  </example>
```

**When to use**: Agents focused on a specific framework or library.

**Example** (React Testing):
```yaml
description: |
  React Testing Library expert. Component testing with modern React patterns.
  Use when writing tests for React components, hooks, or user interactions.
  Specializes in React 18+ with testing-library best practices.

  <example>
  user: "Write tests for my login form component"
  assistant: "I'll use the react-testing-specialist to create comprehensive
             tests covering user interactions, validation, and form submission."
  </example>

  <example>
  user: "How do I test custom hooks?"
  assistant: "I'll use the react-testing-specialist to show you hook testing
             patterns with renderHook and proper cleanup."
  </example>
```

## Quality Scoring

### 5/5 - Exceptional
- Includes WHAT, WHEN, WHY
- Has 2-3 concrete examples
- Trigger terms are specific and actionable
- Specialization is clear and unique
- Often includes "Use PROACTIVELY"
- Under 500 characters

**Example**:
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

### 4/5 - Very Good
- Includes WHAT and WHEN clearly
- Has 1-2 examples
- Trigger terms present but could be more specific
- Specialization mentioned

**Example**:
```yaml
description: |
  Python FastAPI developer. Use when building REST APIs or async endpoints.
  Specializes in modern Python 3.10+ with type hints.

  <example>
  user: "Create an API endpoint"
  assistant: "I'll use the python-fastapi-specialist to build the endpoint."
  </example>
```

### 3/5 - Acceptable
- Includes WHAT and basic WHEN
- May have 1 example
- Trigger terms are vague
- Specialization not clear

**Example**:
```yaml
description: |
  Helps with Python development. Use when working on Python code.

  <example>
  user: "Help with Python"
  assistant: "I'll use the python-specialist."
  </example>
```

### 2/5 - Poor
- WHAT only, no clear WHEN
- No examples
- Vague trigger terms

**Example**:
```yaml
description: Python development specialist with modern patterns.
```

### 1/5 - Very Poor
- Generic, no clear WHAT or WHEN
- No examples

**Example**:
```yaml
description: Helps with tasks
```

## Trigger Term Examples

### Effective Triggers (Specific, Actionable)

**Technology-Specific**:
- "TouchDesigner Python development"
- "FastAPI REST APIs"
- "React component testing"
- "PostgreSQL migrations"

**Task-Specific**:
- "creating extensions"
- "writing tests"
- "building endpoints"
- "refactoring code"

**Pattern-Specific**:
- "async patterns"
- "type hints"
- "dependency injection"
- "reactive state"

**Action-Specific**:
- "review code"
- "audit for issues"
- "clean up"
- "implement"

### Ineffective Triggers (Vague)

**Too Generic**:
- "helps with code"
- "assists development"
- "supports tasks"

**Too Broad**:
- "Python"
- "testing"
- "development"

**Too Vague**:
- "when needed"
- "for assistance"
- "use this"

## Example Composition

### Good Example Structure

```yaml
<example>
user: "{specific-request-showing-trigger-term}"
assistant: "{action-statement-showing-agent-invocation-and-value}"
</example>
```

**Elements**:
1. **User request** - Natural language, includes trigger term
2. **Assistant response** - States agent invocation explicitly
3. **Value statement** - What the agent will do specifically

**Quality markers**:
- User request is realistic and specific
- Assistant explicitly mentions agent name
- Action is clear and concrete
- Shows unique value of agent

### Example Variations

**Creation Task**:
```yaml
<example>
user: "Create a Python extension for my video player component"
assistant: "I'll use the touchdesigner-python-specialist to build a
           properly structured extension with type hints and dependency
           management."
</example>
```

**Review Task**:
```yaml
<example>
user: "Audit my TouchDesigner Python code for issues"
assistant: "I'll have the touchdesigner-python-specialist review your
           extension for convention violations, missing type hints, and
           potential improvements."
</example>
```

**Guidance Task**:
```yaml
<example>
user: "How do I test async API calls?"
assistant: "I'll use the api-testing-specialist to show you async testing
           patterns with proper setup and teardown."
</example>
```

**Refactoring Task**:
```yaml
<example>
user: "Clean up my extension with proper type hints and docstrings"
assistant: "I'll use the touchdesigner-python-specialist to refactor your
           extension with proper type hints, docstrings, and conventions."
</example>
```

## Description Length Guidelines

**Optimal**: 200-400 characters
- Fits in one screen view
- Easy to scan quickly
- Includes all essential elements

**Acceptable**: 400-800 characters
- May need scrolling
- Still readable
- All elements present

**Maximum**: 1024 characters (hard limit)
- Approaching limit
- Consider condensing
- Prioritize essential information

## Common Description Mistakes

### Mistake 1: No Examples
❌ **Bad**:
```yaml
description: Python expert for FastAPI development with type hints.
```

✅ **Good**: Add 2-3 `<example>` blocks.

### Mistake 2: Vague Triggers
❌ **Bad**:
```yaml
description: Use when coding or development tasks.
```

✅ **Good**: Use specific trigger terms like "FastAPI endpoint creation" or "async pattern implementation".

### Mistake 3: No Specialization
❌ **Bad**:
```yaml
description: Helps with Python development.
```

✅ **Good**: Add "Specializes in FastAPI REST APIs with modern Python 3.10+ type hints."

### Mistake 4: Too Technical in Examples
❌ **Bad**:
```yaml
<example>
user: "Implement BaseModel with Field validators using pydantic.validator"
assistant: "Executing schema generation with validation composition."
</example>
```

✅ **Good**: Use natural language that real users would type.

### Mistake 5: First Person in Description
❌ **Bad**:
```yaml
description: I help you with Python development.
```

✅ **Good**: Use third person or action-oriented language: "Python expert. Use for..."

## Testing Your Description

### Checklist
- [ ] WHAT - Clearly states what agent does
- [ ] WHEN - Includes 3+ specific trigger terms
- [ ] WHY - Mentions unique value or specialization
- [ ] EXAMPLES - Has 2-3 `<example>` blocks
- [ ] LENGTH - Under 800 characters (optimal: 200-400)
- [ ] NATURAL - Examples sound like real user requests
- [ ] SPECIFIC - Avoids vague language like "helps with"
- [ ] ACTION - Uses action verbs (create, build, analyze, review)

### Test Invocation
Create a test scenario:
1. Write user request using trigger terms from description
2. Verify agent would be invoked
3. Check that example matches real use case

### Auditor Test
Run agent-auditor on generated agent:
- Description quality should score 4/5 or 5/5
- No errors on description length or format
- Examples should trigger bonus points
