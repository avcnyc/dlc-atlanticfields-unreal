# Skill Validation Rules

Complete rule definitions for skill validation. Each rule includes ID, description, severity, check logic, score impact, and suggested fix template.

---

## Structure Validation

### Rule S-ST-001: Directory Structure
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Skill must be a directory containing SKILL.md, not a single file
- **Check Logic**: Path is directory AND `SKILL.md` exists in directory
- **Score Impact**: -2.0
- **Suggested Fix**:
  ```bash
  # If skill is single file "my-skill.md"
  mkdir my-skill
  mv my-skill.md my-skill/SKILL.md
  ```

### Rule S-ST-002: SKILL.md Exists
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Directory must contain SKILL.md file (case-sensitive)
- **Check Logic**: File `SKILL.md` exists at directory root
- **Score Impact**: -2.0
- **Suggested Fix**: Create SKILL.md with required frontmatter and sections

### Rule S-ST-003: Folder Name Matches Skill Name
- **Category**: Structure
- **Severity**: WARNING
- **Description**: Directory name should match `name` field in frontmatter
- **Check Logic**: `os.path.basename(skill_dir) == frontmatter['name']`
- **Score Impact**: -0.5
- **Suggested Fix**:
  - Current: Directory `my_skill/` with `name: my-skill`
  - Suggested: Rename directory to `my-skill/`

### Rule S-ST-004: Forward Slashes Only
- **Category**: Compliance
- **Severity**: WARNING
- **Description**: All file references must use forward slashes (Unix-style)
- **Check Logic**: Detect backslashes in SKILL.md file references
- **Score Impact**: -0.1 per occurrence
- **Suggested Fix**: Replace all `\` with `/` in paths
  - Current: `references\workflows.md` → Suggested: `references/workflows.md`

---

## Frontmatter Validation

### Rule S-FM-001: Required Fields Present
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Skill must have `name` and `description` fields in YAML frontmatter
- **Check Logic**: Parse frontmatter, verify both keys exist
- **Score Impact**: -2.0 per missing field
- **Suggested Fix**:
  ```yaml
  ---
  name: skill-name
  description: Guide for [domain]. Use when [trigger condition].
  ---
  ```

### Rule S-FM-002: Name Format Valid
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Name must match pattern `^[a-z0-9-]+$` (lowercase letters, numbers, hyphens only)
- **Check Logic**: `re.match(r'^[a-z0-9-]+$', name)`
- **Score Impact**: -2.0
- **Suggested Fix**: Convert to lowercase, replace invalid chars with hyphens
  - Current: `MySkill` → Suggested: `my-skill`
  - Current: `my_skill` → Suggested: `my-skill`

### Rule S-FM-003: Name Length Valid
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Name must be 1-64 characters
- **Check Logic**: `1 <= len(name) <= 64`
- **Score Impact**: -2.0
- **Suggested Fix**:
  - If too long: Truncate and suggest abbreviated version
  - If empty: Suggest meaningful name based on description

### Rule S-FM-004: Name No Reserved Words
- **Category**: Compliance
- **Severity**: ERROR
- **Description**: Name cannot contain "anthropic" or "claude"
- **Check Logic**: `"anthropic" not in name.lower() and "claude" not in name.lower()`
- **Score Impact**: -2.0
- **Suggested Fix**: Remove reserved word
  - Current: `claude-helper` → Suggested: `helper`

### Rule S-FM-005: Name No XML Tags
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Name cannot contain `<` or `>` characters
- **Check Logic**: `"<" not in name and ">" not in name`
- **Score Impact**: -2.0
- **Suggested Fix**: Remove XML characters

### Rule S-FM-006: Description Present
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Description field must be non-empty
- **Check Logic**: `bool(description.strip()) if description else False`
- **Score Impact**: -2.0
- **Suggested Fix**:
  ```yaml
  description: Guide for [domain expertise]. Use when [specific trigger]. [Brief elaboration].
  ```

### Rule S-FM-007: Description Length Valid
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Description must be 1-1024 characters
- **Check Logic**: `1 <= len(description) <= 1024`
- **Score Impact**: -2.0
- **Suggested Fix**: Truncate if too long, move detail to Purpose section

### Rule S-FM-008: Description No XML Tags
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Description cannot contain XML-like tags
- **Check Logic**: Detect `<...>` patterns
- **Score Impact**: -1.0
- **Suggested Fix**: Remove or escape XML tags

### Rule S-FM-009: Description Third Person
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Skill descriptions must use third person voice (not "I", "you", "we")
- **Check Logic**: Detect first/second person pronouns in description
- **Score Impact**: -0.5
- **Suggested Fix**:
  - Current: "I help you build APIs" → Suggested: "Provides API development guidance"
  - Current: "You can use this for..." → Suggested: "Use when building..."

### Rule S-FM-010: Description Has Trigger Terms
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Description should include specific trigger words for discovery
- **Check Logic**: Semantic analysis - check for concrete domain terms vs vague language
- **Score Impact**: -0.5
- **Suggested Fix**: Add specific triggers
  - Current: "Helps with testing" → Suggested: "Guide for API testing with Jest. Use when writing integration tests."

### Rule S-FM-011: Allowed-Tools Valid (if present)
- **Category**: Structure
- **Severity**: WARNING
- **Description**: allowed-tools must be comma-separated list of valid tool names
- **Check Logic**: Parse CSV, validate each tool name
- **Score Impact**: -0.5
- **Suggested Fix**: Format as proper CSV
  - Current: `allowed-tools: Read Write` → Suggested: `allowed-tools: Read, Write`

### Rule S-FM-012: Version Format (if present)
- **Category**: Compliance
- **Severity**: INFO
- **Description**: Version should follow semantic versioning (X.Y.Z)
- **Check Logic**: `re.match(r'^\d+\.\d+\.\d+$', version)`
- **Score Impact**: -0.1
- **Suggested Fix**: Use semver format
  - Current: `version: 1` → Suggested: `version: 1.0.0`

---

## Section Validation

### Rule S-SC-001: Role Statement Present
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: SKILL.md should start with role statement after title
- **Check Logic**: First paragraph after `# {Title}` contains "You are the [Role]"
- **Score Impact**: -0.5
- **Suggested Fix**:
  ```markdown
  # Skill Title

  You are the [Role Name], responsible for [primary responsibility].
  ```

### Rule S-SC-002: Purpose Section Depth
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Purpose/Introduction section should be 2-3 paragraphs
- **Check Logic**: Count paragraphs in Purpose or first section after role
- **Score Impact**: -0.3 if <2 or >5 paragraphs
- **Suggested Fix**: Aim for 2-3 paragraphs explaining what, why, and value

### Rule S-SC-003: Quick Start Present
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Must have Quick Start section
- **Check Logic**: Search for `## Quick Start` header
- **Score Impact**: -1.0
- **Suggested Fix**:
  ```markdown
  ## Quick Start

  ### Step 1: [First Action]
  [Instructions]

  ### Step 2: [Second Action]
  [Instructions]

  ### Step 3: [Third Action]
  [Instructions]
  ```

### Rule S-SC-004: Quick Start Has Steps
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Quick Start should have 1-3 actionable steps
- **Check Logic**: Count `### Step` headers or numbered items in Quick Start section
- **Score Impact**: -0.5
- **Suggested Fix**: Add 3 concrete steps users can follow immediately

### Rule S-SC-005: Core Concepts Section
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Should include Core Concepts or similar overview section
- **Check Logic**: Search for `## Core Concepts`, `## Key Concepts`, `## Overview`
- **Score Impact**: +0.3 bonus if present
- **Suggested Fix**:
  ```markdown
  ## Core Concepts

  ### Concept 1
  [Explanation]

  ### Concept 2
  [Explanation]
  ```

### Rule S-SC-006: Common Pitfalls Section
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Should document common mistakes with ❌/✅ format
- **Check Logic**: Search for `## Common Pitfalls` with ≥3 items
- **Score Impact**: +0.3 bonus if present with ≥3 items
- **Suggested Fix**:
  ```markdown
  ## Common Pitfalls

  - ❌ **[Mistake]** - [Why wrong] → ✅ **[Correct approach]**
  - ❌ **[Mistake]** - [Why wrong] → ✅ **[Correct approach]**
  - ❌ **[Mistake]** - [Why wrong] → ✅ **[Correct approach]**
  ```

### Rule S-SC-007: When to Load References
- **Category**: Content Quality
- **Severity**: SUGGESTION
- **Description**: Should guide when to load specific reference files
- **Check Logic**: Search for `## When to Load References` or similar section
- **Score Impact**: +0.2 bonus if present
- **Suggested Fix**:
  ```markdown
  ## When to Load References

  Load `references/workflows.md` when:
  - **[Trigger condition]** - [What it provides]

  Load `references/patterns.md` when:
  - **[Trigger condition]** - [What it provides]
  ```

### Rule S-SC-008: Examples Section Present
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Must include Examples or Usage section
- **Check Logic**: Search for `## Examples` or `## Usage`
- **Score Impact**: -1.0
- **Suggested Fix**:
  ```markdown
  ## Examples

  ### Example 1: [Scenario]
  [Working example with context and explanation]

  ### Example 2: [Scenario]
  [Working example with context and explanation]
  ```

### Rule S-SC-009: Minimum Example Count
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Should have at least 2 concrete examples
- **Check Logic**: Count example subsections (`### Example`) or numbered examples
- **Score Impact**: -0.5 if <2 examples
- **Suggested Fix**: Add minimum 2 examples showing different use cases

### Rule S-SC-010: Example Quality
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Examples should show complete usage with context
- **Check Logic**: Verify examples include scenario description, code/implementation, and explanation
- **Score Impact**: Variable based on completeness (-0.3 to +0.3)
- **Suggested Fix**: Ensure each example has:
  - Clear scenario description
  - Complete working code or process
  - Explanation of what's happening
  - Expected outcome

---

## Content Validation

### Rule S-CT-001: YAML Well-Formed
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Frontmatter must be valid YAML
- **Check Logic**: `yaml.safe_load(frontmatter)` succeeds
- **Score Impact**: -2.0
- **Suggested Fix**: Show YAML parse error with line number

### Rule S-CT-002: Frontmatter Delimiters
- **Category**: Structure
- **Severity**: ERROR
- **Description**: SKILL.md must start/end frontmatter with `---` markers
- **Check Logic**: Content starts with `---\n` and contains closing `---`
- **Score Impact**: -2.0
- **Suggested Fix**:
  ```markdown
  ---
  name: skill-name
  description: ...
  ---

  # Skill Title
  ```

### Rule S-CT-003: Body Content Present
- **Category**: Structure
- **Severity**: ERROR
- **Description**: Content after frontmatter must exist and be non-empty
- **Check Logic**: Extract body after closing `---`, verify `bool(body.strip())`
- **Score Impact**: -2.0
- **Suggested Fix**: Add skill content following skill-creator template

### Rule S-CT-004: Line Count Compliance
- **Category**: Compliance
- **Severity**: WARNING
- **Description**: SKILL.md body should be <500 lines for optimal performance
- **Check Logic**: Count lines excluding frontmatter
- **Score Impact**:
  - 500-700 lines: -0.5
  - 700-1000 lines: -1.0
  - 1000+ lines: -2.0
- **Suggested Fix**: Move detailed content to reference files
  - Extract code examples → `references/examples.md`
  - Extract detailed workflows → `references/workflows.md`
  - Extract advanced patterns → `references/patterns.md`

### Rule S-CT-005: No Windows Paths
- **Category**: Compliance
- **Severity**: WARNING
- **Description**: Use forward slashes, not backslashes
- **Check Logic**: Detect `\` in paths (excluding escaped chars)
- **Score Impact**: -0.1 per occurrence
- **Suggested Fix**: Replace all `\` with `/`

### Rule S-CT-006: UTF-8 Encoding
- **Category**: Compliance
- **Severity**: ERROR
- **Description**: File must be UTF-8 encoded
- **Check Logic**: Attempt UTF-8 decode
- **Score Impact**: -2.0
- **Suggested Fix**: Re-save with UTF-8 encoding (without BOM)

### Rule S-CT-007: No Time-Sensitive Information
- **Category**: Compliance
- **Severity**: WARNING
- **Description**: Avoid time-sensitive content or mark as "old patterns"
- **Check Logic**: Detect dates, version numbers, "latest", "new", "current"
- **Score Impact**: -0.5
- **Suggested Fix**: Either remove time-sensitive content or create "Historical Patterns" section

### Rule S-CT-008: Consistent Terminology
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Use consistent terms throughout skill
- **Check Logic**: Track term usage, flag inconsistencies
- **Score Impact**: -0.3
- **Suggested Fix**: Choose standard term and use consistently
  - Example: "component" vs "widget" - pick one

### Rule S-CT-009: Imperative Voice
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Instructions should use imperative voice
- **Check Logic**: Detect "you can", "you should", "you might"
- **Score Impact**: -0.2
- **Suggested Fix**:
  - Current: "You can run the command" → Suggested: "Run the command"
  - Current: "You should check" → Suggested: "Check"

### Rule S-CT-010: No Behavioral Instructions
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Skills provide knowledge, not behavior directives
- **Check Logic**: Detect "You are", "When invoked:", role definitions
- **Score Impact**: -1.0
- **Suggested Fix**: Move behavioral instructions to agent file
  - Remove: "You are an expert..."
  - Remove: "When invoked, you must..."
  - Keep: Procedural knowledge, patterns, examples

---

## Reference File Validation

### Rule S-RF-001: References One Level Deep
- **Category**: Compliance
- **Severity**: WARNING
- **Description**: Reference files must be one level from SKILL.md (no nesting)
- **Check Logic**: Parse markdown links, verify max depth is 1
- **Score Impact**: -0.5 per nested reference
- **Suggested Fix**: Flatten reference structure
  - Current: `references/advanced/patterns.md`
  - Suggested: `references/patterns.md` or `references/advanced-patterns.md`

### Rule S-RF-002: Referenced Files Exist
- **Category**: Structure
- **Severity**: ERROR
- **Description**: All files linked from SKILL.md must exist
- **Check Logic**: Extract markdown links, resolve paths, check existence
- **Score Impact**: -1.0 per broken link
- **Suggested Fix**: Create missing file or remove link
  - Expected path: `.claude/skills/{skill-name}/references/{file}.md`

### Rule S-RF-003: Reference File Line Count
- **Category**: Compliance
- **Severity**: INFO
- **Description**: Reference files should be 200-500 lines for optimal loading
- **Check Logic**: Count lines in each reference file
- **Score Impact**: -0.2 if outside range
- **Suggested Fix**:
  - If <200 lines: Consider consolidating with another reference
  - If >500 lines: Split into focused topic files

### Rule S-RF-004: Large References Have TOC
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Files >100 lines should include table of contents
- **Check Logic**: Check for TOC markdown in files >100 lines
- **Score Impact**: -0.2
- **Suggested Fix**:
  ```markdown
  # Reference Topic

  ## Table of Contents
  - [Section 1](#section-1)
  - [Section 2](#section-2)

  ## Section 1
  ...
  ```

### Rule S-RF-005: Scripts Have Error Handling
- **Category**: Content Quality
- **Severity**: WARNING
- **Description**: Executable scripts should include explicit error handling
- **Check Logic**: Parse Python/JS scripts, look for try/except or error checks
- **Score Impact**: -0.5
- **Suggested Fix**: Add error handling
  ```python
  try:
      # operation
  except SpecificError as e:
      # handle error
  ```

### Rule S-RF-006: Scripts Document Dependencies
- **Category**: Compliance
- **Severity**: WARNING
- **Description**: Scripts should list required packages/imports
- **Check Logic**: Look for requirements comment or docstring
- **Score Impact**: -0.3
- **Suggested Fix**:
  ```python
  """
  Script description.

  Requirements:
  - package>=1.0.0
  - another-package
  """
  ```

### Rule S-RF-007: No Magic Numbers
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: Scripts should explain numeric constants
- **Check Logic**: Detect numeric literals without nearby comments
- **Score Impact**: -0.1
- **Suggested Fix**: Use named constants with explanatory comments
  ```python
  # Maximum retry attempts before failing
  MAX_RETRIES = 3
  ```

---

## Progressive Disclosure

### Rule S-PD-001: Progressive Disclosure Used
- **Category**: Content Quality
- **Severity**: SUGGESTION
- **Description**: Consider using reference files for advanced content
- **Check Logic**: Detect if content is distributed vs all in SKILL.md
- **Score Impact**: +0.5 bonus if reference files used effectively
- **Suggested Fix**: Extract advanced topics to references/
  - Basic usage → SKILL.md
  - Advanced patterns → references/patterns.md
  - Complete examples → references/examples.md

### Rule S-PD-002: Reference Navigation Clear
- **Category**: Content Quality
- **Severity**: INFO
- **Description**: SKILL.md should guide readers to references with descriptive links
- **Check Logic**: Verify reference links have context, not just "see file"
- **Score Impact**: +0.2 bonus if well-organized
- **Suggested Fix**:
  ```markdown
  Load `references/workflows.md` when:
  - **Planning migration** - Complete step-by-step process
  - **Writing migration script** - Template and patterns
  ```

### Rule S-PD-003: Domain-Based Organization
- **Category**: Content Quality
- **Severity**: SUGGESTION
- **Description**: Consider organizing references by domain/topic
- **Check Logic**: Detect if references/ subdirectory structure used
- **Score Impact**: +0.2 bonus if present
- **Suggested Fix**: Organize by topic
  ```
  references/
  ├── workflows.md      # Multi-step processes
  ├── patterns.md       # Code patterns
  ├── examples.md       # Complete examples
  └── troubleshooting.md # Common issues
  ```

---

## Rule Application Order

Execute rules in this sequence for optimal error reporting:

1. **Structure Rules First** (S-ST-001, S-ST-002)
   - Directory structure valid
   - SKILL.md exists
   - Stop if these fail (can't proceed)

2. **Frontmatter Rules** (S-CT-001, S-CT-002, S-FM-001, S-FM-006)
   - YAML well-formed
   - Frontmatter delimiters present
   - Required fields exist
   - Can't validate content without these

3. **Field Format Rules** (S-FM-002 through S-FM-012)
   - Validate field values
   - Can proceed even if some fail

4. **Content Rules** (S-CT-003 through S-CT-010)
   - Body content validation
   - Line counts, encoding, paths

5. **Section Rules** (S-SC-001 through S-SC-010)
   - Required sections present
   - Section quality assessment
   - Apply bonuses for best practices

6. **Reference Rules** (S-RF-001 through S-RF-007)
   - Only if references exist
   - Validate structure and quality

7. **Progressive Disclosure Rules** (S-PD-001 through S-PD-003)
   - Bonus points for advanced patterns
   - No penalties, only bonuses

---

## Severity Guidelines

**Use ERROR when:**
- Issue prevents skill from functioning
- Required structure missing (directory, SKILL.md)
- Required field missing
- Invalid syntax (YAML, frontmatter)
- Referenced files don't exist

**Use WARNING when:**
- Issue reduces effectiveness but skill works
- Best practice violation
- Recommended limit exceeded
- Optional field format issue
- Missing recommended sections

**Use INFO when:**
- Providing quality feedback
- Highlighting bonus opportunities
- Suggesting improvements
- Minor optimization available

**Use SUGGESTION when:**
- Purely optional enhancement
- Alternative approach available
- No functional impact
- Advanced pattern recommendation
