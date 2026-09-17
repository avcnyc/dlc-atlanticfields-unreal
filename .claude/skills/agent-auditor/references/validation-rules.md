# Agent Validation Rules

Complete rule definitions for agent file validation. Each rule includes ID, description, severity, check logic, score impact, and suggested fix template.

---

## Frontmatter Validation

### Rule A-FM-001: Required Fields Present
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Agent must have `name` and `description` fields in YAML frontmatter
- **Check Logic**: Parse frontmatter, verify both keys exist
- **Score Impact**: -2.0 per missing field
- **Suggested Fix**:
  ```yaml
  ---
  name: agent-name
  description: TODO - Add description of what this agent does and when to use it
  ---
  ```

### Rule A-FM-002: Name Format Valid
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Name must match pattern `^[a-z0-9-]+$` (lowercase letters, numbers, hyphens only)
- **Check Logic**: `re.match(r'^[a-z0-9-]+$', name)`
- **Score Impact**: -2.0
- **Suggested Fix**: Convert name to lowercase, replace invalid characters with hyphens
  - Current: `MyAgent` → Suggested: `my-agent`
  - Current: `my_agent` → Suggested: `my-agent`
  - Current: `Agent.Name` → Suggested: `agent-name`

### Rule A-FM-003: Name Length Valid
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Name must be 1-64 characters
- **Check Logic**: `1 <= len(name) <= 64`
- **Score Impact**: -2.0
- **Suggested Fix**:
  - If too long: Truncate to 64 chars and suggest abbreviated version
  - If empty: Suggest meaningful name based on description or system prompt content

### Rule A-FM-004: Name No Reserved Words
- **Category**: Compliance
- **Severity**: ERROR
- **Description**: Name cannot contain "anthropic" or "claude"
- **Check Logic**: `"anthropic" not in name.lower() and "claude" not in name.lower()`
- **Score Impact**: -2.0
- **Suggested Fix**: Remove reserved word from name
  - Current: `claude-helper` → Suggested: `helper`
  - Current: `anthropic-agent` → Suggested: `agent`

### Rule A-FM-005: Name No XML Tags
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Name cannot contain `<` or `>` characters
- **Check Logic**: `"<" not in name and ">" not in name`
- **Score Impact**: -2.0
- **Suggested Fix**: Remove XML characters
  - Current: `<agent>` → Suggested: `agent`

### Rule A-FM-006: Description Present
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Description field must be non-empty
- **Check Logic**: `bool(description.strip()) if description else False`
- **Score Impact**: -2.0
- **Suggested Fix**:
  ```yaml
  description: |
    [What this agent does]. Use when [specific trigger condition].

    Example: "Expert code reviewer. Use PROACTIVELY after code changes to ensure quality standards."
  ```

### Rule A-FM-007: Description Length Valid
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Description must be 1-1024 characters
- **Check Logic**: `1 <= len(description) <= 1024`
- **Score Impact**: -2.0
- **Suggested Fix**:
  - If too long: Truncate and move detail to system prompt
  - If empty: See A-FM-006

### Rule A-FM-008: Description No XML Tags
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Description cannot contain XML-like tags
- **Check Logic**: Detect `<...>` patterns (excluding allowed markdown like `<example>`)
- **Score Impact**: -1.0
- **Suggested Fix**: Remove or escape XML tags, or use markdown code blocks instead

### Rule A-FM-009: Tools Field Valid (if present)
- **Category**: Structure
- **Severity**: WARNING
- **Description**: Tools field must be comma-separated list of valid tool names
- **Check Logic**: Parse CSV, validate each tool name is non-empty and alphanumeric
- **Score Impact**: -0.5
- **Suggested Fix**:
  - Current: `tools: Read Write,Grep` → Suggested: `tools: Read, Write, Grep`
  - Current: `tools: [Read, Write]` → Suggested: `tools: Read, Write`

### Rule A-FM-010: Model Field Valid (if present)
- **Category**: Structure
- **Severity**: WARNING
- **Description**: Model must be sonnet/opus/haiku/inherit or valid model ID
- **Check Logic**: `model in ['sonnet', 'opus', 'haiku', 'inherit'] or is_valid_model_id(model)`
- **Score Impact**: -0.5
- **Suggested Fix**:
  - Common aliases: `gpt-4` → Suggest: `opus`
  - Invalid: `claude-3` → Suggest: `sonnet` or `opus`

### Rule A-FM-011: PermissionMode Valid (if present)
- **Category**: Structure
- **Severity**: WARNING
- **Description**: Must be default/acceptEdits/bypassPermissions/plan/ignore
- **Check Logic**: `permissionMode in ['default', 'acceptEdits', 'bypassPermissions', 'plan', 'ignore']`
- **Score Impact**: -0.5
- **Suggested Fix**: List valid options and recommend `default` for most cases

### Rule A-FM-012: Skills Field Format (if present)
- **Category**: Structure
- **Severity**: WARNING
- **Description**: Skills must be comma-separated list
- **Check Logic**: Parse CSV format, validate each skill name matches `^[a-z0-9-]+$`
- **Score Impact**: -0.5
- **Suggested Fix**:
  - Current: `skills: skill1 skill2` → Suggested: `skills: skill1, skill2`

---

## Content Validation

### Rule A-CT-001: YAML Well-Formed
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Frontmatter must be valid YAML
- **Check Logic**: `yaml.safe_load(frontmatter_content)` succeeds without exception
- **Score Impact**: -2.0
- **Suggested Fix**: Show YAML parse error with line number, suggest correction
  - Common issue: Unescaped quotes
  - Common issue: Incorrect indentation
  - Common issue: Missing closing quote

### Rule A-CT-002: Frontmatter Delimiters Present
- **Category**: Structure
- **Severity**: ERROR
- **Description**: File must start with `---` and contain closing `---`
- **Check Logic**: `content.startswith('---\n') and '\n---\n' in content`
- **Score Impact**: -2.0
- **Suggested Fix**:
  ```markdown
  ---
  name: agent-name
  description: Agent description
  ---

  System prompt content here.
  ```

### Rule A-CT-003: System Prompt Present
- **Category**: Content Quality
- **Severity**: ERROR
- **Description**: Content after frontmatter must exist and be non-empty
- **Check Logic**: Extract body after closing `---`, verify `bool(body.strip())`
- **Score Impact**: -2.0
- **Suggested Fix**:
  ```markdown
  You are a [role description].

  When invoked:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
  ```

### Rule A-CT-004: System Prompt Line Count
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: System prompt should be <200 lines for optimal performance
- **Check Logic**: Count non-frontmatter lines
- **Score Impact**:
  - 200-300 lines: -0.5
  - 300+ lines: -1.0
- **Suggested Fix**: Extract procedural knowledge to skill, keep only behavioral instructions in agent
  - Identify code examples → Move to skill references
  - Identify API documentation → Move to skill
  - Keep role definition, workflow, constraints

### Rule A-CT-005: No Windows Paths
- **Category**: Compliance
- **Severity**: WARNING
- **Description**: Use forward slashes, not backslashes in paths
- **Check Logic**: Detect `\` in paths (excluding escaped characters like `\n`, `\t`)
- **Score Impact**: -0.1 per occurrence
- **Suggested Fix**: Replace all `\` with `/`
  - Current: `.claude\agents\agent.md` → Suggested: `.claude/agents/agent.md`

### Rule A-CT-006: UTF-8 Encoding
- **Category**: Compliance
- **Severity**: ERROR
- **Description**: File must be UTF-8 encoded
- **Check Logic**: Attempt to decode file as UTF-8
- **Score Impact**: -2.0
- **Suggested Fix**: Re-save file with UTF-8 encoding (without BOM)

---

## Quality Checks

### Rule A-QL-001: Description Quality Score
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Description should include what agent does AND when to use it with examples
- **Check Logic**: Semantic analysis based on quality rubric
- **Quality Rubric**:
  - **5**: Specific what + when + trigger terms + use case clarity
    - Example: "Expert code reviewer. Use PROACTIVELY after code changes to ensure quality standards. Checks style, tests, security, and performance."
  - **4**: Clear what + when + some trigger terms
    - Example: "Code reviewer. Use when reviewing code changes."
  - **3**: What + when but vague
    - Example: "Reviews code. Use when needed."
  - **2**: What only, no trigger terms
    - Example: "Reviews code."
  - **1**: Generic/vague
    - Example: "Helps with tasks."
- **Score Impact**:
  - Rating 5: +1.0 bonus
  - Rating 4: 0.0 (neutral)
  - Rating 3: -0.5
  - Rating 2: -1.0
  - Rating 1: -2.0
- **Suggested Fix**: Provide template based on rating
  - For rating 1-2: Add specific domain, add "Use when..." clause, add concrete examples
  - For rating 3: Add trigger terms, add concrete use cases

### Rule A-QL-002: Proactive Invocation Marker
- **Category**: Content Quality
- **Severity**: SUGGESTION
- **Description**: Consider adding proactive invocation marker for automatic triggering
- **Check Logic**: Search for "PROACTIVELY", "MUST BE USED", "ALWAYS USE" (case-insensitive)
- **Score Impact**: +0.5 bonus if present
- **Suggested Fix**:
  ```yaml
  description: |
    [Agent role and capability]. Use PROACTIVELY when [trigger condition].
  ```

### Rule A-QL-003: System Prompt Has Role Definition
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: System prompt should define agent's role ("You are...")
- **Check Logic**: Search for "You are" pattern in system prompt
- **Score Impact**: -0.5
- **Suggested Fix**:
  ```markdown
  You are a [specific role] specializing in [domain/expertise].
  ```

### Rule A-QL-004: System Prompt Has Workflow
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: System prompt should include step-by-step workflow
- **Check Logic**: Look for numbered lists, "When invoked:", "Steps:", "Process:"
- **Score Impact**: -0.5
- **Suggested Fix**:
  ```markdown
  When invoked:
  1. [First step - what to do]
  2. [Second step - what to do]
  3. [Third step - what to do]
  ```

### Rule A-QL-005: System Prompt Has Examples
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: System prompt benefits from concrete examples
- **Check Logic**: Search for `<example>` tags or "Example:" headers
- **Score Impact**: +0.3 bonus if present
- **Suggested Fix**:
  ```markdown
  <example>
  user: [Example user request]
  assistant: [How agent should respond]
  </example>
  ```

### Rule A-QL-006: System Prompt Specifies Output Format
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Good prompts specify expected output format
- **Check Logic**: Search for "output", "format", "response" keywords
- **Score Impact**: +0.2 bonus if present
- **Suggested Fix**:
  ```markdown
  ## Response Format

  Provide:
  1. [What to include]
  2. [How to format]
  3. [What to emphasize]
  ```

### Rule A-QL-007: Single Responsibility
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Agent should have one clear focus/responsibility
- **Check Logic**: Semantic analysis - detect if agent description or prompt covers multiple unrelated domains
- **Score Impact**: -1.0
- **Suggested Fix**: Split into multiple focused agents, each with single responsibility

### Rule A-QL-008: No Code Examples in Prompt
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Extensive code examples should be in a skill
- **Check Logic**: Count fenced code blocks, flag if >3
- **Score Impact**: -0.5
- **Suggested Fix**: Move code examples to skill reference file, agent system prompt references skill

### Rule A-QL-009: Tools Minimized
- **Category**: Compliance
- **Severity**: SUGGESTION
- **Description**: Only list necessary tools or omit to inherit all
- **Check Logic**: If tools field has >10 items, suggest review
- **Score Impact**: -0.2
- **Suggested Fix**: Either omit `tools:` field to inherit all, or minimize to only essential tools

---

## Skill Reference Validation

### Rule A-SK-001: Referenced Skills Exist
- **Category**: Compliance
- **Severity**: ERROR
- **Description**: All skills in `skills:` field must exist at expected path
- **Check Logic**: For each skill name, check if `.claude/skills/{skill-name}/SKILL.md` exists
- **Score Impact**: -1.0 per missing skill
- **Suggested Fix**:
  - Show expected path: `.claude/skills/{skill-name}/SKILL.md`
  - Suggest either creating skill or removing from `skills:` field

### Rule A-SK-002: Skill Tool Available
- **Category**: Compliance
- **Severity**: WARNING
- **Description**: If `skills:` field is used, `tools:` should include `Skill` or be omitted
- **Check Logic**: `"Skill" in tools_list or tools is None`
- **Score Impact**: -0.5
- **Suggested Fix**:
  ```yaml
  tools: Read, Write, Skill  # Add 'Skill' to enable skill loading
  ```
  Or omit `tools:` field entirely to inherit all tools.

### Rule A-SK-003: No Skill Content Duplication
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Agent system prompt shouldn't duplicate content from referenced skills
- **Check Logic**:
  - If agent has `skills:` field, read each skill's SKILL.md
  - Perform line-level comparison
  - Flag if >30 consecutive lines overlap
- **Score Impact**: -1.0 per 30 lines duplicated
- **Suggested Fix**:
  - Identify duplicated sections (show line ranges)
  - Suggest removing duplication from agent
  - Agent should reference skill instead: "Use the {skill-name} skill for [topic]"

---

## Validation Implementation Notes

### Parsing YAML Frontmatter

```python
import re
import yaml

def parse_agent_file(content: str) -> tuple[dict, str]:
    """
    Extract YAML frontmatter and body from agent file.

    Returns:
        (frontmatter_dict, body_content)
    """
    if not content.startswith('---\n'):
        raise ValueError("File must start with YAML frontmatter delimiter '---'")

    # Find closing delimiter
    parts = content.split('\n---\n', 1)
    if len(parts) != 2:
        raise ValueError("Missing closing frontmatter delimiter")

    yaml_content = parts[0].replace('---\n', '', 1)
    body = parts[1]

    try:
        frontmatter = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")

    return frontmatter, body
```

### Description Quality Analysis

```python
def analyze_description_quality(description: str) -> int:
    """
    Rate description quality 1-5 based on rubric.

    Returns:
        Quality score (1=poor, 5=excellent)
    """
    score = 1

    # Check for "what" (domain/capability mention)
    has_what = any(word in description.lower() for word in
                   ['expert', 'specialist', 'reviewer', 'builder', 'analyzer'])

    # Check for "when" (trigger phrase)
    has_when = any(phrase in description.lower() for phrase in
                   ['use when', 'use proactively', 'invoke when', 'apply when'])

    # Check for trigger terms (specific keywords that aid discovery)
    trigger_words = ['after', 'before', 'during', 'for', 'with']
    has_triggers = sum(1 for word in trigger_words if word in description.lower())

    # Check for examples
    has_examples = '<example>' in description or 'example:' in description.lower()

    # Score logic
    if has_what and has_when and has_triggers >= 2 and has_examples:
        score = 5
    elif has_what and has_when and has_triggers >= 1:
        score = 4
    elif has_what and has_when:
        score = 3
    elif has_what:
        score = 2

    return score
```

### Windows Path Detection

```python
def detect_windows_paths(content: str) -> list[str]:
    """
    Find Windows-style paths (backslashes).

    Returns:
        List of lines containing backslashes
    """
    issues = []
    for i, line in enumerate(content.split('\n'), 1):
        # Exclude escaped characters
        if '\\' in line and not any(esc in line for esc in ['\\n', '\\t', '\\r', '\\"', "\\'"]):
            issues.append(f"Line {i}: {line.strip()}")
    return issues
```

### Content Duplication Detection

```python
def detect_duplication(agent_content: str, skill_content: str, threshold: int = 30) -> list[tuple]:
    """
    Find duplicated content between agent and skill.

    Args:
        agent_content: Agent system prompt
        skill_content: Skill SKILL.md content
        threshold: Minimum consecutive matching lines to flag

    Returns:
        List of (agent_line_start, skill_line_start, match_length) tuples
    """
    agent_lines = agent_content.split('\n')
    skill_lines = skill_content.split('\n')

    duplicates = []

    for i, agent_line in enumerate(agent_lines):
        if not agent_line.strip():
            continue

        for j, skill_line in enumerate(skill_lines):
            if agent_line.strip() == skill_line.strip():
                # Found match, check how long it continues
                match_len = 1
                while (i + match_len < len(agent_lines) and
                       j + match_len < len(skill_lines) and
                       agent_lines[i + match_len].strip() == skill_lines[j + match_len].strip()):
                    match_len += 1

                if match_len >= threshold:
                    duplicates.append((i + 1, j + 1, match_len))

    return duplicates
```

---

## Rule Application Order

Execute rules in this sequence for optimal error reporting:

1. **Structure Rules First** (A-CT-001, A-CT-002)
   - YAML well-formed
   - Frontmatter delimiters present
   - Stop if these fail (can't parse file)

2. **Required Field Rules** (A-FM-001, A-FM-006)
   - Check required fields exist
   - Critical for agent functionality

3. **Field Format Rules** (A-FM-002 through A-FM-012)
   - Validate field values
   - Can proceed even if some fail

4. **Content Rules** (A-CT-003 through A-CT-006)
   - Validate system prompt presence and quality
   - Check encoding and path formatting

5. **Quality Rules** (A-QL-001 through A-QL-009)
   - Score description and prompt quality
   - Apply bonuses for best practices

6. **Skill Reference Rules** (A-SK-001 through A-SK-003)
   - Only if `skills:` field present
   - Check skill existence and integration

---

## Severity Guidelines

**Use ERROR when:**
- Issue prevents agent from functioning
- Required field missing
- Invalid syntax or format
- Reserved word violation

**Use WARNING when:**
- Issue reduces effectiveness but agent still works
- Best practice violation
- Recommended limit exceeded
- Optional field format issue

**Use INFO when:**
- Providing quality feedback
- Highlighting bonus opportunities
- Suggesting improvements
- Explaining quality score

**Use SUGGESTION when:**
- Purely optional enhancement
- Alternative approach available
- Minor optimization possible
- No functional impact
