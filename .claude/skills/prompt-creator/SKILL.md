---
name: prompt-creator
description: Prompt engineering patterns for Claude Code. Use when creating prompts for coding, analysis, research, or multi-step tasks.
---

# Prompt Creator

You are the Prompt Engineering Expert, providing knowledge and patterns for crafting effective prompts that get results.

## Purpose

Creating effective prompts is the foundation of successful AI-assisted development. A well-crafted prompt leverages Claude's capabilities (extended thinking, parallel tool calling, long-horizon reasoning) while avoiding common pitfalls (vague objectives, missing context, poor examples).

Prompt engineering combines art and science. The 10 prompting principles synthesize Anthropic's official best practices into actionable patterns. XML tags provide structure, examples demonstrate behaviors, and "why" context enables Claude to make informed decisions. Claude 4.x models have been trained for more precise instruction following than previous generations, requiring explicit guidance while offering unprecedented capabilities.

This skill integrates with the prompt-creator-specialist agent, providing the knowledge and patterns that the agent references when generating prompts for users. The agent handles workflow orchestration while this skill provides the fundamental patterns and principles.

## Quick Start

### Step 1: Understand the Goal

Identify what you're building and why:
- **Coding task** - Creating, refactoring, or fixing code
- **Analysis task** - Investigating code, finding bottlenecks, security issues
- **Research task** - Gathering information, exploring patterns
- **Creative task** - Designing systems, UI components, architectures
- **Multi-step task** - Complex workflows requiring sequential prompts

### Step 2: Choose the Right Pattern

Select the appropriate template based on task type:
- **Coding** - Include requirements, constraints, verification
- **Analysis** - Include analysis_focus, data_sources, output_format
- **Research** - Include scope, research_process, deliverables
- **Creative** - Include constraints, creative_direction, examples
- **Multi-step** - Include sequence_context, dependencies, execution_strategy

### Step 3: Apply the Structure

Build your prompt using XML tags:
1. Start with `<objective>` - Clear goal statement with why
2. Add `<context>` - Background, current state, integration points
3. Define `<requirements>` - Specific, actionable specifications
4. Set `<constraints>` - Boundaries that focus creativity
5. Include `<examples>` - Show both correct and incorrect approaches
6. Specify `<output>` - Exact format and deliverables
7. Add `<verification>` - How to validate success

## Core Concepts

### The 10 Prompting Principles (Condensed)

**1. Use XML Tags for Organization**
Claude was trained with XML tags. Benefits: clarity, accuracy, flexibility, parseability.
Common tags: `<objective>`, `<context>`, `<requirements>`, `<constraints>`, `<examples>`, `<verification>`, `<output>`

**2. Be Explicit and Direct**
State clear, action-oriented commands. Include: action verb, quantity, topic, audience, constraints with WHY.

**3. Define Boundaries for Creativity**
Constraints focus creativity rather than limit it. Define: length, format, style, scope.

**4. The Exploratory Draft**
Draft, plan, then act: Analysis → Planning → Review → Execution

**5. Demand Structured Output**
Request specific formats: markdown tables, JSON, numbered lists, code blocks with language tags.

**6. Explain the "Why"**
For every constraint, explain reasoning. Context enables better decisions.

**7. Control Output Verbosity**
Be explicit: "Be concise, use bullet points" or "Think step-by-step, explain reasoning"

**8. Use Examples (Multishot)**
Include 3-5 examples showing both correct and incorrect approaches in `<example>` tags.

**9. The Tone of Collaboration**
Use firm, clear, respectful tone. Not overly polite ("Could you perhaps...") nor aggressive ("Do this NOW").

**10. Divide and Conquer**
Simple task → Single prompt. Complex task → Multi-prompt chain (001, 002, 003...).

### Claude 4.x Specific Guidance

**Extended Thinking Triggers**
Use high-level guidance, not prescriptive steps. Trigger phrases: "thoroughly analyze", "consider multiple approaches", "deeply evaluate", "explore various solutions"

Good: "Thoroughly analyze the codebase to identify refactoring opportunities. Consider multiple approaches."
Bad: "1. List all functions, 2. Check each function, 3. Identify which are over 20 lines..."

**Parallel Tool Calling**
For independent operations, include:
```xml
<parallel_tool_calling>
If you intend to call multiple tools with no dependencies, make all independent calls in parallel.
For example: reading 3 files, checking multiple endpoints, analyzing multiple functions.
However, if calls depend on previous results, call them sequentially.
</parallel_tool_calling>
```

**State Discovery**
For resumable tasks:
```xml
<state_management>
Before starting: Read STATE.md to verify dependencies
After completing: Update STATE.md with progress and resume point
</state_management>
```

### XML Structuring Fundamentals

**Tag Naming:** Use semantic, intuitive names (`<objective>` not `<info>`)

**Nesting Patterns:**
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
</requirements>
```

**Combining Techniques:**
XML + Multishot + Chain of Thought for complex analysis tasks

## Common Pitfalls

### 1. Vague Objectives
❌ **Wrong:** "Make the app better"
✅ **Right:** "Improve dashboard load time from 3s to <500ms by implementing query optimization, caching, and lazy loading. WHY: 40% of users abandon at >2s load time."

### 2. Missing "Why" Context
❌ **Wrong:** "Don't use loops"
✅ **Right:** "Use array methods instead of loops. WHY: Functional patterns improve testability and reduce mutable state bugs in this codebase."

### 3. Infinite Scope (No Boundaries)
❌ **Wrong:** "Create a dashboard with any useful features"
✅ **Right:** "Create dashboard with exactly 4 widgets: activity feed, stats card, action buttons, profile summary. Mobile-first, dark mode, <300 LOC. WHY: Mobile users are 60% of traffic."

### 4. Examples Show Bad Behavior
❌ **Wrong:** Example shows `console.log` debugging with no error handling
✅ **Right:** Example shows structured logging with try/catch, labeled as "correct approach" with quality markers

### 5. No Verification Criteria
❌ **Wrong:** No verification section
✅ **Right:** Verification checklist with structural (files created, no syntax errors), functional (features work), and testing (tests pass) criteria

### 6. Overly Prescriptive for Complex Tasks
❌ **Wrong:** "1. List files, 2. Open first file, 3. Read line 1, 4. Check if line has function..."
✅ **Right:** "Thoroughly analyze codebase to identify all exported functions. Consider multiple approaches for discovering functions efficiently."

### 7. Telling Claude What NOT to Do
❌ **Wrong:** "Do not use markdown. Do not include code blocks. Do not use bullet points."
✅ **Right:** "Use smoothly flowing prose paragraphs with complete sentences. WHY: Response will be read by TTS engine."

### 8. Wrong Tone (Too Polite or Aggressive)
❌ **Wrong:** "Could you perhaps consider creating..."
❌ **Wrong:** "Build this component NOW or else"
✅ **Right:** "Create a login component with email/password validation."

## When to Load References

Load `references/xml-patterns.md` when:
- Need detailed tag hierarchy and nesting examples
- Want task-specific tag structures (coding vs analysis vs research)
- Building complex nested requirements
- Combining XML with multishot and chain of thought

Load `references/prompt-templates.md` when:
- Generating prompts for specific task type
- Need complete template structure with all sections
- Want pattern variations (single prompt vs multi-step)
- Building sequential prompt chains

Load `references/examples.md` when:
- Task is ambiguous or complex
- Need to show good vs bad patterns clearly
- Want worked examples across all task types
- User requests pattern demonstrations

Load `references/anti-patterns.md` when:
- Reviewing generated prompts for issues
- User asks about common mistakes
- Need fix suggestions for specific violations
- Validating prompt quality before execution

## Examples

### Example 1: Simple Coding Task

```xml
<objective>
Create a React login component with email/password validation.
Include real-time validation feedback and error handling.
</objective>

<context>
Current state: React 18 app with TypeScript, authentication API at /api/auth/login
Need: Component for login page
WHY: Users need secure login flow with clear feedback
</context>

<requirements>
<file path="src/components/LoginForm.tsx">
  <purpose>Login form component</purpose>
  <specifications>
    - Email and password input fields
    - Real-time validation (email format, password length)
    - Submit button disabled until valid
    - Error message display
    - Loading state during submission
  </specifications>
</file>
</requirements>

<constraints>
- Under 150 lines (WHY: Components should be focused and composable)
- Use controlled inputs (WHY: Required for real-time validation)
- No inline styles (WHY: Using Tailwind CSS)
</constraints>

<verification>
- [ ] Component renders without errors
- [ ] Validation works for email and password
- [ ] Submit disabled when invalid
- [ ] Error messages display correctly
</verification>
```

### Example 2: Analysis Task with Extended Thinking

```xml
<objective>
Analyze dashboard codebase to identify performance bottlenecks causing slow load times.
</objective>

<analysis_focus>
Thoroughly analyze and consider multiple perspectives:
- Database query patterns and indexes
- Frontend rendering and bundle size
- Network request sequencing and caching

Explore various optimization approaches before concluding.
</analysis_focus>

<parallel_tool_calling>
When reading multiple files or running commands, invoke tools simultaneously rather than sequentially.
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

### Example 3: Multi-Step Task with State Management

```xml
<objective>
Build user authentication system (Prompt 2 of 4: API Implementation)
</objective>

<sequence_context>
Previous: Prompt 001 completed database schema
This prompt: Create authentication API endpoints
Next: Prompt 003 will build UI components
</sequence_context>

<dependencies>
Requires: User table from Prompt 001
Produces: API endpoints for Prompt 003 to consume
</dependencies>

<execution_strategy>
Strategy: SEQUENTIAL
Reason: API must exist before UI can call endpoints
</execution_strategy>

<state_management>
Before starting: Read STATE.md to confirm database schema completed
After completing: Update STATE.md marking API complete, set resume point for UI
</state_management>
```
