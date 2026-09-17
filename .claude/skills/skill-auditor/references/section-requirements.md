# Section Requirements

Detailed requirements for each required section in SKILL.md files, based on skill-creator specification and touchdesigner-python reference implementation.

---

## Required Sections Overview

Based on the skill-creator specification, every SKILL.md must include:

1. **Role Statement** - Opening paragraph defining responsibility
2. **Purpose** - 2-3 paragraphs on what, why, value
3. **Quick Start** - 3 actionable steps
4. **Core Concepts** - Essential knowledge (3-5 subsections typical)
5. **Common Pitfalls** - Minimum 3 items with ❌/✅ format
6. **When to Load References** - Triggers for loading reference files
7. **Examples** - Minimum 2 concrete examples

---

## 1. Role Statement

### Location
First paragraph immediately after the `# {Skill Title}` header.

### Format
```markdown
# Skill Title

You are the [Role Name], responsible for [primary responsibility and scope].
```

### Requirements
- **Must start with**: "You are the [Role]"
- **Length**: 1-2 sentences
- **Content**: Define what the skill does and primary responsibility
- **Tone**: Clear, authoritative, concise

### Examples

**Good:**
```markdown
You are the TouchDesigner Python Guide, responsible for helping developers create properly structured extensions with reactive state management, lifecycle callbacks, and modern Python 3.11+ type hints.
```

**Bad:**
```markdown
This skill helps with Python.
```
*Issue: No role definition, too vague*

**Bad:**
```markdown
You are responsible for many things including Python development, testing, debugging, refactoring, and documentation.
```
*Issue: Too broad, violates single responsibility*

### Validation Criteria
- [ ] Starts with "You are the"
- [ ] Includes specific role name
- [ ] Defines clear responsibility
- [ ] Single, focused scope
- [ ] 1-2 sentences maximum

---

## 2. Purpose Section

### Location
Immediately following the role statement, typically unlabeled or under `## Purpose` header.

### Format
```markdown
## Purpose

[2-3 paragraphs explaining]:
- Paragraph 1: What this skill provides (capabilities, knowledge domain)
- Paragraph 2: Why it's valuable (problems solved, benefits)
- Paragraph 3: What it enables (outcomes, applications)
```

### Requirements
- **Paragraph count**: 2-3 paragraphs (minimum 2, maximum 5)
- **Content depth**: Substantive explanation, not just repetition of description
- **Focus**: What, why, and value proposition
- **Avoid**: Implementation details (those go in Core Concepts)

### Examples

**Good (from touchdesigner-python):**
```markdown
## Purpose

TouchDesigner extensions are Python classes that add custom behavior to components. Well-structured extensions use reactive state (`tdu.Dependency`) to automatically update UI and parameter expressions, lifecycle callbacks (`onInitTD`, `onDestroyTD`) for proper initialization and cleanup, and consistent naming conventions that enable promotion to the component level.

This skill provides patterns for creating extensions that integrate seamlessly with TouchDesigner's architecture. Extensions follow a consistent naming convention: PascalCase component names with `Ext` suffix (e.g., `MyComp` component → `MyCompExt` class). Capitalized members are automatically promoted to the component level for external access.

Proper extension architecture eliminates common issues like timing errors during initialization, memory leaks from uncleared runs, and cryptic "NoneType" errors from using `op()` instead of `opex()`.
```

**Bad:**
```markdown
## Purpose

This skill is about Python extensions.
```
*Issue: Only 1 sentence, no depth*

**Bad:**
```markdown
## Purpose

Python extensions are important. They let you write code. Code is good. You should use this skill when you need extensions. Extensions make things better. This is a useful skill.
```
*Issue: Verbose without substance, 6 paragraphs of fluff*

### Validation Criteria
- [ ] 2-3 paragraphs (minimum 2, maximum 5)
- [ ] Explains what skill provides
- [ ] Explains why it's valuable
- [ ] Explains what it enables
- [ ] Substantive content, not repetitive
- [ ] No implementation details (those belong in Core Concepts)

---

## 3. Quick Start Section

### Location
Section with header `## Quick Start`

### Format
```markdown
## Quick Start

### Step 1: [Action Name]
[Concrete instructions for first step]

### Step 2: [Action Name]
[Concrete instructions for second step]

### Step 3: [Action Name]
[Concrete instructions for third step]
```

### Requirements
- **Step count**: Exactly 3 steps (can be 1-3 but 3 is strongly recommended)
- **Headers**: Use `### Step N:` format
- **Action orientation**: Steps describe actions, not concepts
- **Concreteness**: Specific instructions, not vague guidance
- **Completeness**: User can follow steps without reading further

### Examples

**Good (from touchdesigner-python):**
```markdown
## Quick Start

### Step 1: Copy Boilerplate

Copy the extension boilerplate from [extensions.md](references/extensions.md#boilerplate):

```python
"""MyComp extension."""

import logging
logger = logging.getLogger(__name__)

class MyCompExt:
    """Brief description of component."""

    def __init__(self, ownerComp: baseCOMP) -> None:
        self.ownerComp: baseCOMP = ownerComp
        self.my_op: someOP = self.ownerComp.opex('my_op')
```

### Step 2: Add Reactive State and Properties

Add Dependencies for values that should update UI/expressions:

```python
# In __init__
self.MyAttr = tdu.Dependency(0)

# Property bound to Custom Parameter
@property
def MyPar(self) -> float:
    return self.ownerComp.par.MyPar.eval()
```

### Step 3: Implement Parameter Routing

Add a Parameter Execute DAT that routes changes to your extension:

```python
def onValueChange(par, prev):
    op.MyComp.UpdateParameter(par)
```
```

**Bad:**
```markdown
## Quick Start

Just read the documentation and you'll understand how to use this.
```
*Issue: No steps, not actionable*

**Bad:**
```markdown
## Quick Start

1. Learn about the concepts
2. Understand the patterns
3. Read the examples
4. Try it yourself
5. Debug any issues
```
*Issue: 5 steps (too many), not concrete, conceptual not actionable*

### Validation Criteria
- [ ] Has `## Quick Start` header
- [ ] Contains 1-3 steps (3 preferred)
- [ ] Each step uses `### Step N:` format
- [ ] Steps are actionable (verbs, not concepts)
- [ ] Steps are concrete (specific instructions)
- [ ] Steps can be followed without reading rest of skill
- [ ] Code examples or commands included where appropriate

---

## 4. Core Concepts Section

### Location
Section with header `## Core Concepts` or similar (`## Key Concepts`, `## Overview`)

### Format
```markdown
## Core Concepts

### Concept 1 Name
Brief explanation or pattern description.
```python
# Code example if applicable
```

### Concept 2 Name
Brief explanation or pattern description.

### Concept 3 Name
Brief explanation or pattern description.
```

### Requirements
- **Subsection count**: 3-5 subsections typical (minimum 2)
- **Content**: Essential knowledge only
- **Depth**: Brief explanations, not exhaustive
- **Examples**: Code snippets or illustrations where helpful
- **Focus**: What user needs to know to use skill effectively

### Examples

**Good:**
```markdown
## Core Concepts

### Dependencies
Reactive values that auto-update parameter expressions when changed.
```python
self.MyAttr = tdu.Dependency(0)
self.MyAttr.val = 5  # Triggers updates
```

### Lifecycle Callbacks
- `onInitTD()` - Called when extension fully initialized (preferred for init)
- `onDestroyTD()` - Cleanup before reinit

### Operator Access
**Critical:** Always use `opex()` instead of `op()` for operator references:
```python
# CORRECT - fails fast with clear error
self.my_op: someOP = self.ownerComp.opex('my_op')

# WRONG - returns None silently
self.my_op = self.ownerComp.op('my_op')
```
```

**Bad:**
```markdown
## Core Concepts

Extensions are written in Python. Python is a programming language. You write code in files. Files have extensions like .py.
```
*Issue: Explains basics, not skill-specific concepts*

### Validation Criteria
- [ ] Has `## Core Concepts` or similar header
- [ ] Contains 2+ subsections
- [ ] Each subsection has clear name
- [ ] Explanations are brief but complete
- [ ] Code examples where appropriate
- [ ] Focuses on essential knowledge
- [ ] No exhaustive detail (save for references)

---

## 5. Common Pitfalls Section

### Location
Section with header `## Common Pitfalls` (or `## Troubleshooting`, `## Gotchas`)

### Format
```markdown
## Common Pitfalls

- ❌ **[Mistake Description]** - [Why it's wrong] → ✅ **[Correct Approach]**
- ❌ **[Mistake Description]** - [Why it's wrong] → ✅ **[Correct Approach]**
- ❌ **[Mistake Description]** - [Why it's wrong] → ✅ **[Correct Approach]**
```

### Requirements
- **Minimum count**: 3 pitfalls
- **Format**: Use ❌ for wrong, ✅ for correct
- **Structure**: **Bold** mistake, plain explanation, → separator, **Bold** solution
- **Content**: Real mistakes users make, not hypothetical
- **Actionability**: Clear contrast between wrong and right

### Examples

**Good (from touchdesigner-python):**
```markdown
## Common Pitfalls

- ❌ **Using `op()` for required operators** - Returns `None` silently → ✅ **Use `opex()` to fail fast with clear error**
- ❌ **Direct assignment to Dependency** - `self.MyAttr = 5` breaks tracking → ✅ **Use `self.MyAttr.val = 5`**
- ❌ **Skipping `onDestroyTD` cleanup** - Causes memory leaks → ✅ **Kill runs by group in `onDestroyTD`**
- ❌ **Using `.ext` for promoted members** - Verbose and unnecessary → ✅ **Use `op('MyComp').Method()` directly**
- ❌ **String type hints** - `"baseCOMP"` is incorrect → ✅ **Use `baseCOMP`**
```

**Bad:**
```markdown
## Common Pitfalls

- Don't make mistakes
- Be careful when coding
- Read the documentation
```
*Issue: Vague, no ❌/✅ format, not specific*

**Bad:**
```markdown
## Common Pitfalls

- ❌ **Writing bad code** → ✅ **Write good code**
```
*Issue: Only 1 pitfall, too vague, not actionable*

### Validation Criteria
- [ ] Has `## Common Pitfalls` or similar header
- [ ] Contains minimum 3 pitfalls
- [ ] Uses ❌ emoji for wrong approach
- [ ] Uses ✅ emoji for correct approach
- [ ] Each pitfall uses **bold** for mistake and solution
- [ ] Explanations are specific and concrete
- [ ] Solutions are actionable
- [ ] Pitfalls are realistic (users actually make these mistakes)

---

## 6. When to Load References Section

### Location
Section with header `## When to Load References`

### Format
```markdown
## When to Load References

Load `references/[file].md` when:
- **[Trigger condition]** - [What the file provides]
- **[Trigger condition]** - [What the file provides]

Load `references/[another-file].md` when:
- **[Trigger condition]** - [What the file provides]
```

### Requirements
- **One entry per reference file**: Each reference file listed separately
- **Trigger clarity**: Specific conditions for loading each file
- **Value description**: Brief explanation of what file provides
- **Format**: Bold trigger, plain description
- **Organization**: Group by file

### Examples

**Good (from touchdesigner-python):**
```markdown
## When to Load References

Load `references/conventions.md` when:
- **Checking code style** - Need DO/DON'T guidance
- **Implementing properties** - Need the 5 property patterns
- **Setting up UpdateParameter** - Need universal routing pattern
- **Module imports** - Need `op().module` vs `mod()` guidance

Load `references/extensions.md` when:
- **Creating new extension** - Need boilerplate scaffolding
- **Adding reactive state** - Need Dependency patterns with callbacks
- **Advanced patterns** - Dual-source crossfade, scheduled execution, module-level state

Load `references/callbacks.md` when:
- **Implementing specific callbacks** - Parameter, DAT, CHOP, Timer, Panel
- **Routing patterns** - One-line callback routing to extension
- **Shortcut selection** - `parent.myComp` vs `op.MyComp`
```

**Bad:**
```markdown
## References

See the references folder for more info.
```
*Issue: No specific guidance, not per-file*

**Bad:**
```markdown
## When to Load References

Load references when you need more detail.
```
*Issue: Vague, no file-specific guidance*

### Validation Criteria
- [ ] Has `## When to Load References` or similar header
- [ ] Lists each reference file separately
- [ ] Provides 1+ trigger conditions per file
- [ ] Triggers are specific and actionable
- [ ] Explains what each file provides
- [ ] Uses bold for triggers
- [ ] Helps user decide which reference to load

---

## 7. Examples Section

### Location
Section with header `## Examples` or `## Usage`

### Format
```markdown
## Examples

### Example 1: [Scenario Name]

[Context and setup description]

```language
# Working code example
```

**Usage:**
```language
# How to use it
```

[Explanation of what's happening]

### Example 2: [Scenario Name]

[Context and setup description]

```language
# Working code example
```

[Explanation]
```

### Requirements
- **Minimum count**: 2 examples
- **Scenario names**: Descriptive, not generic ("Example 1")
- **Context**: Setup or scenario description
- **Code**: Complete, working examples
- **Explanation**: What the code does and why
- **Variety**: Different use cases, not variations of same thing

### Examples

**Good (from touchdesigner-python):**
```markdown
## Examples

### Example 1: Simple Extension with Property

```python
"""MyComp extension."""

import logging
logger = logging.getLogger(__name__)

class MyCompExt:
    """Component with reactive state."""

    def __init__(self, ownerComp: baseCOMP) -> None:
        self.ownerComp: baseCOMP = ownerComp
        self.my_dat: nullDAT = self.ownerComp.opex('my_dat')
        self.MyAttr = tdu.Dependency(0)

    def onInitTD(self) -> None:
        logger.info(f'{__name__} initialized')

    @property
    def Active(self) -> bool:
        return self.ownerComp.par.Active.eval()

    def MyMethod(self) -> None:
        """Execute action."""
        self.MyAttr.val += 1
        logger.info(f'MyAttr is now {self.MyAttr.val}')
```

**Usage:**
```python
op.MyComp.MyMethod()
op.MyComp.MyAttr.val  # Access reactive value
op.MyComp.Active      # Access property
```

### Example 2: Extension with Dependency Callback

```python
"""MyComp extension with change notification."""

import logging
logger = logging.getLogger(__name__)

class MyCompExt:
    """Component that responds to state changes."""

    def __init__(self, ownerComp: baseCOMP) -> None:
        self.ownerComp: baseCOMP = ownerComp
        self.MyIndex = tdu.Dependency(0)
        # Register callback BEFORE any .val assignments
        self.MyIndex.callbacks.append(self.onIndexChanged)

    def onIndexChanged(self, info: dict) -> None:
        """Called when MyIndex changes."""
        prev = info['prev']
        current = info['dependency'].val
        logger.debug(f'Index changed: {prev} -> {current}')
        self.doAction(current)

    def doAction(self, index: int) -> None:
        """Internal action on index change."""
        pass
```
```

**Bad:**
```markdown
## Examples

### Example 1

```python
x = 1
```

This is an example.
```
*Issue: Only 1 example, too trivial, no context*

**Bad:**
```markdown
## Examples

### Example: Basic
Some code here

### Example: Advanced
Some more code here
```
*Issue: No actual code blocks, no explanations*

### Validation Criteria
- [ ] Has `## Examples` or `## Usage` header
- [ ] Contains minimum 2 examples
- [ ] Each example has descriptive scenario name
- [ ] Each example has context/setup description
- [ ] Each example has complete, working code
- [ ] Code is properly formatted in code blocks
- [ ] Each example has explanation
- [ ] Examples show different use cases
- [ ] Examples are realistic and useful

---

## Optional Sections

While not required, these sections add value:

### Reference Files List
```markdown
## Reference Files

**[Filename](references/filename.md)**
- Topic 1 coverage
- Topic 2 coverage
```

### Workflow Section
For complex multi-step processes not suitable for Quick Start:
```markdown
## Complete Workflow

[Detailed end-to-end process]
```

### Advanced Topics
For advanced content that would bloat Core Concepts:
```markdown
## Advanced Topics

See [references/advanced.md](references/advanced.md) for:
- Advanced pattern 1
- Advanced pattern 2
```

---

## Section Order

Recommended order based on skill-creator spec and reference implementations:

1. **Title** (`# Skill Name`)
2. **Role Statement** (first paragraph, no header)
3. **Purpose** (`## Purpose` or unlabeled)
4. **Quick Start** (`## Quick Start`)
5. **Core Concepts** (`## Core Concepts`)
6. **Common Pitfalls** (`## Common Pitfalls`)
7. **When to Load References** (`## When to Load References`)
8. **Examples** (`## Examples`)
9. **[Optional sections]**

This order provides progressive disclosure:
- What/why first (Purpose)
- How to start quickly (Quick Start)
- Essential knowledge (Core Concepts)
- Mistakes to avoid (Common Pitfalls)
- Where to find more (When to Load References)
- Real-world usage (Examples)

---

## Validation Summary

For each section, validate:

| Section | Required | Min Count | Format Requirements | Quality Checks |
|---------|----------|-----------|---------------------|----------------|
| Role Statement | Yes | 1 sentence | "You are the [Role]" | Clear, focused responsibility |
| Purpose | Yes | 2 paragraphs | 2-3 paragraphs | What, why, value |
| Quick Start | Yes | 3 steps | `### Step N:` format | Actionable, concrete, complete |
| Core Concepts | Yes | 2 subsections | `### Concept` format | Essential only, with examples |
| Common Pitfalls | Yes | 3 items | ❌/✅ format | Specific, realistic, actionable |
| When to Load References | Recommended | 1 per file | Bold triggers | Clear guidance per file |
| Examples | Yes | 2 examples | `### Example:` + code | Complete, explained, varied |
