# Prompt Templates

## Table of Contents

1. [Overview](#overview)
2. [Coding Task Templates](#coding-task-templates)
3. [Analysis Task Templates](#analysis-task-templates)
4. [Research Task Templates](#research-task-templates)
5. [Creative Task Templates](#creative-task-templates)
6. [Multi-Step Task Templates](#multi-step-task-templates)

## Overview

Complete templates for different task types. Replace bracketed placeholders `[like this]` with specific content.

### Template Selection Guide

| Task Type | Use When | Key Sections |
|-----------|----------|--------------|
| **Coding** | Building, refactoring, fixing code | requirements, constraints, verification |
| **Analysis** | Investigating code, finding issues | analysis_focus, data_sources, output_format |
| **Research** | Gathering information | scope, research_process, deliverables |
| **Creative** | Designing systems, UI, architectures | constraints, creative_direction, examples |
| **Multi-Step** | Complex workflows, sequential prompts | sequence_context, dependencies, execution_strategy |

## Coding Task Templates

### Feature Implementation

```xml
<objective>
[Action verb] [what to build] with [key features].
WHY: [Purpose, business value]
</objective>

<context>
Current state: [What exists, tech stack]
This solution will: [Benefits]
Integration: [How it fits with existing code]
</context>

<requirements>
<requirement name="[category]">
  <file path="[relative-path]">
    <purpose>[What this file does]</purpose>
    <specifications>
      - [Requirement with technical details: libraries, parameters]
    </specifications>
  </file>
</requirement>
</requirements>

<constraints>
- [Constraint] WHY: [Reason]
</constraints>

<examples>
<example name="[scenario]">
  <scenario>[When to use this pattern]</scenario>
  <implementation>
  ```[language]
  [Code example]
  ```
  </implementation>
  <quality_markers>
    - [Why this is good]
  </quality_markers>
</example>
</examples>

<parallel_tool_calling>
Invoke independent operations simultaneously. If operations depend on previous results, call sequentially.
</parallel_tool_calling>

<output>
Files to create:
- ./[path]/[file] - [Purpose]

After completing provide:
- Summary of implementation
- Files modified with line counts
- Usage instructions
</output>

<verification>
Structural:
- [ ] All files created at specified paths
- [ ] No syntax errors, all functions documented
- [ ] No TODO or placeholder content

Functional:
- [ ] [Functional check]

Testing:
- [ ] Run [test command] - all tests pass
- [ ] Manual test: [Step-by-step flow]
</verification>

<success_criteria>
- [Measurable outcome]
</success_criteria>
```

## Analysis Task Templates

### Performance Analysis

```xml
<objective>
Analyze [system/component] to identify performance bottlenecks.
Focus on [specific concern].
</objective>

<analysis_focus>
Analyze multiple perspectives:
- [Dimension 1: database queries]
- [Dimension 2: frontend rendering]
- [Dimension 3: network requests]

Explore various optimization approaches. Consider tradeoffs between [concern 1] and [concern 2].
</analysis_focus>

<data_sources>
Examine files:
@[file-pattern-1]

Run commands:
![profiling-command]
</data_sources>

<parallel_tool_calling>
All file reads and independent metric collections can run in parallel.
</parallel_tool_calling>

<analysis_requirements>
For each bottleneck:
1. Provide file:line references
2. Explain issue with quantified impact
3. Assess severity (Critical/High/Medium/Low)
4. Recommend remediation
5. Estimate expected improvement
</analysis_requirements>

<output_format>
Save to: ./analyses/[name]-analysis.md

Structure:
## Executive Summary
[2-3 sentences highlighting critical findings]

## Findings
| File | Line | Issue | Severity | Impact |
|------|------|-------|----------|--------|

## Detailed Analysis
### Finding 1: [Title]
**File:** [path:line]
**Issue:** [Description]
**Analysis:** [Root cause]
**Recommendation:** [Specific fix]
**Expected Impact:** [Performance improvement]

## Recommendations
1. [Priority with expected improvement]

## Tradeoffs
[Analysis of competing concerns]
</output_format>

<verification>
- [ ] All data sources examined
- [ ] Specific line references provided
- [ ] Recommendations are actionable
- [ ] Expected impact quantified
</verification>
```

## Research Task Templates

### Technology Research

```xml
<research_objective>
Gather information about [technology/pattern] to inform [decision].
Research will determine [key decision points].
</research_objective>

<scope>
Focus areas:
- [Area 1: core capabilities]
- [Area 2: integration patterns]

Boundaries:
- Time period: [e.g., 2024-2025]
- Version: [e.g., React 18+]
- Exclude: [Out of scope]

WHY: [How research informs decisions]
</scope>

<research_process>
1. **Source Discovery** - Identify authoritative sources (official docs prioritized)
2. **Information Gathering** - Extract patterns, anti-patterns, examples
3. **Synthesis** - Compare approaches, evaluate tradeoffs
4. **Validation** - Cross-reference sources, test examples
</research_process>

<deliverables>
Save to: ./research/[topic]-research.md

Structure:
## Executive Summary
[3-5 bullet points]

## Key Findings
### [Category]
[Findings by topic]

## Patterns Catalog
[Reusable patterns with examples]

## Anti-Patterns to Avoid
[Common mistakes with explanations]

## Recommendations
1. [Recommendation with rationale]

## Sources
- [Source with URL]
</deliverables>

<verification>
- [ ] All key questions answered
- [ ] Sources credible (official docs prioritized)
- [ ] Patterns include working examples
- [ ] Recommendations specific and actionable
</verification>
```

## Creative Task Templates

### System Design

```xml
<objective>
Design [system/architecture] that [purpose and goals].
Create comprehensive design addressing [requirements].

Go beyond basic functionality to create fully-featured, scalable design.
</objective>

<constraints>
- [Constraint] WHY: [How this focuses solution]
- [Constraint] WHY: [How this ensures quality]

WHY constraints matter: [How boundaries enable better solutions]
</constraints>

<creative_direction>
Style: [Design philosophy]
Inspiration: [Reference architectures]
Innovation: [Where to push boundaries]

Include:
- [Advanced feature]
- [Delightful detail]

Balance: [Competing concerns]
</creative_direction>

<examples>
<example name="exceptional-design">
  <scenario>[When this pattern excels]</scenario>
  <implementation>[Diagram, description, or code]</implementation>
  <why_exceptional>
    - [What makes this outstanding]
  </why_exceptional>
</example>
</examples>

<output>
Deliverables:
- [Primary output: diagram, specification]
- [Supporting documentation]

Quality bar:
- Production-ready design
- Comprehensive edge case handling
- Clear tradeoff documentation
</output>

<verification>
- [ ] Addresses all requirements
- [ ] Scalability considered
- [ ] Edge cases handled
- [ ] Tradeoffs documented
- [ ] Implementation path clear
</verification>
```

## Multi-Step Task Templates

### Sequential Prompt Chain

```xml
<objective>
[Overall goal across multiple prompts]
This is prompt [N of M]: [Description of this step]
</objective>

<sequence_context>
Previous prompts:
- Prompt 001: [What was accomplished]

This prompt (00[N]):
- [Specific focus]

Remaining prompts:
- Prompt 00[N+1]: [What comes next]
</sequence_context>

<dependencies>
Requires:
- [Completed work from previous prompts]
- [Files that must exist]

Produces:
- [Outputs for subsequent prompts]
- [State updates]
</dependencies>

<execution_strategy>
Strategy: SEQUENTIAL
Reason: [Why this must run after previous and before next]
</execution_strategy>

<state_management>
Before starting:
- Read STATE.md to verify dependencies met
- Confirm expected files exist

After completing:
- Update STATE.md:
  - Mark Prompt 00[N] complete
  - List files created/modified
  - Document decisions
- Set resume point for next prompt
</state_management>

<requirements>
[Standard requirements for this step]
</requirements>

<verification>
[Standard verification for this step]

State verification:
- [ ] STATE.md updated
- [ ] All outputs exist
- [ ] No blockers for next prompt
</verification>
```

### Parallel Prompt Group

```xml
<objective>
[Component to build]
Part of Parallel Group [X]: [Components that run simultaneously]
</objective>

<sequence_context>
Overall goal: [High-level objective]

Parallel Group [X] (run simultaneously):
- Prompt 00[A]: [This prompt - component A]
- Prompt 00[B]: [Component B]

These are independent with no shared file modifications.

After Group [X]:
- Prompt 00[Y]: [Integration step]
</sequence_context>

<dependencies>
Requires:
- [Prerequisites from earlier sequential prompts]

Produces:
- [Independent outputs that don't conflict]

No shared files with: Prompt 00[B], Prompt 00[C]
</dependencies>

<execution_strategy>
Strategy: PARALLEL
Reason: [Why this can run independently]

Example: Self-contained, no files touched by other prompts in group.
</execution_strategy>

<state_management>
Before starting:
- Read STATE.md to verify group prerequisites met

After completing:
- Update STATE.md:
  - Mark Prompt 00[A] complete
  - Note: Part of Parallel Group [X]
  - Wait for group completion before proceeding
</state_management>

<requirements>
[Standard requirements]

NOTE: Ensure no file path conflicts with parallel prompts
</requirements>
