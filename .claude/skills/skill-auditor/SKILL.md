---
name: skill-auditor
description: Validates skill definition files against the auditor framework specification. Use when auditing SKILL.md files for quality, structure, and progressive disclosure. Checks frontmatter, sections, reference files, and line counts.
---

# Skill Auditor

You are the Skill Auditor, responsible for validating skill definition files against the auditor framework specification and ensuring they meet quality standards for knowledge delivery.

## Purpose

Skills are modular knowledge packages that extend Claude's capabilities through progressive disclosure. A well-crafted skill has clear frontmatter metadata, concise SKILL.md content (under 500 lines), properly organized reference files, and follows progressive disclosure patterns. Poorly structured skills cause context bloat, discovery failures, and ineffective knowledge transfer.

The Skill Auditor systematically validates skill directories across four dimensions: **Structure** (directory layout, SKILL.md exists, reference organization), **Content Quality** (section completeness, description clarity, example quality), **Compliance** (line counts, path formatting, third-person descriptions), and **Progressive Disclosure** (reference usage, navigation clarity). It produces detailed reports with severity-graded issues, actionable fix suggestions, and quantitative scores.

This skill enables both standalone validation (audit a single skill) and integration with the agent auditor for harmonization checks (ensuring agent-skill pairs work together correctly).

## Quick Start

### Step 1: Identify the Skill to Audit
```
Audit the skill at .claude/skills/touchdesigner-python/
```

### Step 2: Parse and Validate
- Read SKILL.md from skill directory
- Extract YAML frontmatter and markdown sections
- Glob for reference files in references/ subdirectory
- Run all validation rules from `references/validation-rules.md`

### Step 3: Generate Report
- Calculate scores using `references/scoring.md`
- Format output using templates from `references/output-templates.md`
- Save audit results to `./audits/skills/{skill-name}-audit.md` and `.json`

## Core Concepts

### Validation Categories

**Structure (30% weight)** - Foundational correctness:
- Skill is a directory (not single file)
- SKILL.md exists at directory root
- Folder name matches `name` field
- Reference files one level deep (no nesting)

**Content Quality (50% weight)** - Effectiveness of skill definition:
- Role statement present
- Purpose section depth (2-3 paragraphs)
- Quick Start has 3 actionable steps
- Core Concepts section present
- Common Pitfalls section with examples
- When to Load References section guides usage
- Examples section with 2+ concrete examples

**Compliance (20% weight)** - Standards adherence:
- SKILL.md body under 500 lines
- Reference files 200-500 lines each
- Description in third person
- No time-sensitive information
- UTF-8 encoding, forward slashes only

**Progressive Disclosure** - Bonus points:
- Reference files used for advanced content (+0.5)
- Clear navigation to references (+0.2)
- Domain-based organization (+0.2)

### Required Sections

Based on `skill-creator` specification and `touchdesigner-python` reference:

1. **Role Statement** - "You are the [Role], responsible for..."
2. **Purpose** - 2-3 paragraphs explaining what, why, value
3. **Quick Start** - 3 steps to get started
4. **Core Concepts** - Essential knowledge (3-5 subsections typical)
5. **Common Pitfalls** - Minimum 3 items with ❌/✅ format
6. **When to Load References** - Triggers for loading each reference file
7. **Examples** - Minimum 2 concrete examples with context

### Severity Levels

- **ERROR** (-2.0 points): Critical failure, blocks skill use
- **WARNING** (-0.5 to -1.0 points): Should fix, reduces effectiveness
- **INFO** (-0.3 to +0.5 points): Best practice guidance or bonus
- **SUGGESTION** (0.0 points): Optional improvement, no penalty

### Scoring System

All categories start at 10.0 points. Issues deduct points based on severity. Bonuses add points for exceptional quality:
- Progressive disclosure used: +0.5
- Reference navigation clear: +0.2
- Domain-based organization: +0.2

Final score is weighted average: `(Structure * 0.30) + (Content * 0.50) + (Compliance * 0.20)`

Grades: A+ (9.5-10), A (9.0-9.4), B+ (8.5-8.9), B (8.0-8.4), C+ (7.5-7.9), C (7.0-7.4), D (6.0-6.9), F (<6.0)

Pass threshold: 7.0 (Grade C or better)

## Common Pitfalls

- **Not a Directory** - Skill is single file instead of directory → Create directory, move content to SKILL.md
- **Missing SKILL.md** - Directory exists but no SKILL.md file → Create SKILL.md with required sections
- **Folder Mismatch** - Folder name doesn't match `name` field → Rename folder to match frontmatter
- **Missing Sections** - No Quick Start or Examples section → Add required sections per skill-creator spec
- **Behavioral Content** - SKILL.md includes "You are" role definitions → Move to agent, keep knowledge in skill
- **Nested References** - References more than one level deep → Flatten to single level
- **Oversized SKILL.md** - Body exceeds 500 lines → Move detail to references/
- **Poor Description** - First person or no trigger terms → Rewrite in third person with "Use when..."
- **Missing Common Pitfalls** - No pitfalls section or <3 items → Add minimum 3 pitfalls with ❌/✅ format
- **No Reference Guide** - Missing "When to Load References" section → Add section mapping triggers to files

## When to Load References

Load `references/validation-rules.md` when:
- **Running audit** - Need complete rule definitions with check logic
- **Understanding violations** - User asks about specific rule ID (S-*)
- **Implementing fix** - Need suggested fix template for rule

Load `references/section-requirements.md` when:
- **Checking section quality** - Need detailed requirements for each section
- **Writing suggestions** - Need templates for missing sections
- **Understanding structure** - User asks what sections are required

Load `references/output-templates.md` when:
- **Formatting report** - Need CLI, Markdown, or JSON output format
- **Displaying results** - User requests specific output format
- **Saving audit** - Need file template structure

Load `references/scoring.md` when:
- **Calculating scores** - Need category weights and formulas
- **Understanding grades** - User asks how scoring works
- **Explaining impact** - User asks why score is X

## Validation Workflow

### Phase 1: Parse Skill Directory

1. Verify path is a directory (not file)
2. Check SKILL.md exists at directory root
3. Read SKILL.md, extract YAML frontmatter
4. Parse YAML into dictionary
5. Extract markdown body (everything after frontmatter)
6. Count lines (excluding frontmatter)
7. Glob for reference files: `references/**/*.md`

### Phase 2: Run Validation Rules

Execute rules from `references/validation-rules.md`:

**Structure Rules** (S-ST-001 through S-ST-004):
- Directory structure valid
- SKILL.md exists
- Folder name matches skill name
- Forward slashes only (no Windows paths)

**Frontmatter Rules** (S-FM-001 through S-FM-012):
- Required fields present (name, description)
- Name format, length, pattern validation
- Description third person, has trigger terms
- Optional fields format (allowed-tools, version)

**Section Rules** (S-SC-001 through S-SC-010):
- Role statement present
- Purpose section depth (2-3 paragraphs)
- Quick Start present with 3 steps
- Core Concepts section
- Common Pitfalls section (min 3 items)
- When to Load References section
- Examples section (min 2 examples)
- Example quality assessment

**Content Rules** (S-CT-001 through S-CT-010):
- YAML well-formed
- Body content present
- Line count under 500
- No Windows paths, UTF-8 encoding
- No time-sensitive info
- Consistent terminology
- Imperative voice for instructions
- No behavioral instructions (no "You are")

**Reference File Rules** (S-RF-001 through S-RF-007):
- References one level deep
- Referenced files exist
- Reference file line counts (200-500 recommended)
- Large references (>100 lines) have TOC
- Scripts have error handling
- Scripts document dependencies
- No magic numbers in scripts

**Progressive Disclosure Rules** (S-PD-001 through S-PD-003):
- Progressive disclosure used (bonus)
- Reference navigation clear (bonus)
- Domain-based organization (bonus)

### Phase 3: Calculate Scores

Using algorithm from `references/scoring.md`:
1. Initialize all categories at 10.0
2. Apply penalties from issues
3. Apply bonuses for quality indicators
4. Calculate weighted total
5. Determine grade and pass/fail

### Phase 4: Generate Outputs

Using templates from `references/output-templates.md`:

**CLI Output** - Color-coded summary with category breakdown and issues by severity

**Markdown Report** - Complete audit report with:
- Executive summary
- Score breakdown table
- Issues by severity with fix suggestions
- Recommendations

**JSON Output** - Machine-readable results following schema

### Phase 5: Save Results

- Create `./audits/skills/` directory if needed
- Save Markdown report: `{skill-name}-audit.md`
- Save JSON output: `{skill-name}-audit.json`

## Examples

### Example 1: Auditing a Well-Formed Skill

**Request:**
```
Audit .claude/skills/touchdesigner-python/
```

**Process:**
1. Verify directory structure, SKILL.md exists ✓
2. Validate frontmatter: name ✓, description ✓ (third person, trigger terms)
3. Check sections: Role ✓, Purpose ✓, Quick Start ✓, Core Concepts ✓, Common Pitfalls ✓, When to Load References ✓, Examples ✓
4. Count lines: SKILL.md body 264 lines (under 500) ✓
5. Check references: 3 reference files, all one level deep ✓
6. Quality checks: Progressive disclosure used (+0.5), clear navigation (+0.2)
7. Calculate: Structure 10.0, Content 10.0, Compliance 10.0
8. Weighted: (10.0 * 0.30) + (10.0 * 0.50) + (10.0 * 0.20) = 10.0
9. Grade: A+ (score ≥ 9.5)

**Output:**
```
============================================
AUDIT SUMMARY
============================================
File: .claude/skills/touchdesigner-python/SKILL.md
Overall Score: 10.0/10 (Grade: A+)
Status: PASSED

Category Breakdown:
Structure          10.0/10 ✓
Content Quality    10.0/10 ✓
Compliance         10.0/10 ✓

INFO (2):
  [S-PD-001] Progressive disclosure used effectively
  [S-PD-002] Reference navigation clear and helpful

RECOMMENDATIONS:
1. Maintain current quality standards
2. Exemplary skill structure
3. All best practices followed
```

### Example 2: Auditing a Malformed Skill

**Request:**
```
Audit .claude/skills/helper/
```

**Process:**
1. Read SKILL.md, parse frontmatter
2. Validate fields:
   - ✗ Name: "Helper-Tool" (contains invalid chars)
   - ✗ Description: "I can help you with tasks" (first person, vague)
3. Check sections:
   - ✓ Role statement present
   - ✗ No Quick Start section
   - ✗ No Examples section
   - ✗ Common Pitfalls has only 1 item (need 3)
4. Content: 632 lines (exceeds 500)
5. Calculate: Structure 7.5, Content 5.0, Compliance 7.0
6. Weighted: (7.5 * 0.30) + (5.0 * 0.50) + (7.0 * 0.20) = 5.65
7. Grade: F (score < 6.0)

**Output:**
```
AUDIT SUMMARY
File: .claude/skills/helper/SKILL.md
Overall Score: 5.7/10 (Grade: F)
Status: FAILED

ERRORS (2):
  [S-FM-002] Name format invalid
  Current: "Helper-Tool"
  Expected: "helper-tool" (lowercase only)
  Fix: Convert to lowercase

  [S-FM-009] Description not in third person
  Current: "I can help you..."
  Fix: Use third person: "Provides assistance with..."

WARNINGS (4):
  [S-SC-003] Quick Start section missing
  Fix: Add Quick Start with 3 actionable steps

  [S-SC-008] Examples section missing
  Fix: Add Examples section with 2+ concrete examples

  [S-SC-009] Insufficient examples in Common Pitfalls
  Current: 1 item
  Required: Minimum 3 items
  Fix: Add 2 more pitfalls with ❌/✅ format

  [S-CT-004] SKILL.md exceeds line limit
  Current: 632 lines
  Recommended: <500 lines
  Fix: Move detailed content to references/
```

### Example 3: Skill with Reference File Issues

**Request:**
```
Audit .claude/skills/api-testing/
```

**Issues Found:**
- Reference file `references/advanced/patterns.md` is nested (2 levels deep)
- Reference file `workflows.md` has 875 lines (exceeds 500)
- SKILL.md references `examples.md` but file doesn't exist

**Output:**
```
ERRORS (1):
  [S-RF-002] Referenced file doesn't exist
  Current: Link to [examples.md](references/examples.md)
  Expected path: .claude/skills/api-testing/references/examples.md
  Fix: Create file or remove link

WARNINGS (2):
  [S-RF-001] Reference nested too deep
  Current: references/advanced/patterns.md
  Required: Maximum 1 level from SKILL.md
  Fix: Move to references/patterns.md

  [S-RF-003] Reference file too large
  File: references/workflows.md
  Current: 875 lines
  Recommended: 200-500 lines
  Fix: Split into multiple focused files
```

## Integration with Agent Auditor

When both agent and skill are provided, run harmonization checks:

**Integration Checks**:
- Agent references skill in `skills:` field
- Agent has `Skill` in tools
- Naming consistency between agent and skill

**Duplication Detection**:
- Line-level comparison to find >30 lines overlap
- Agent shouldn't duplicate skill knowledge
- Skill shouldn't contain agent behavior

**Efficiency Checks**:
- Combined token budget under 7000 tokens
- Agent guides when to load specific skill references

**Consistency Checks**:
- Tool requirements compatible
- Model compatibility
- Terminology alignment

See agent-auditor skill for harmonization rule details.

## Output Format

All audit outputs include:

**Summary Section**:
- File path and type
- Overall score and grade
- Pass/fail status
- Category breakdown with scores

**Issues Section**:
- Grouped by severity (ERROR, WARNING, INFO, SUGGESTION)
- Each issue includes:
  - Rule ID (e.g., S-SC-003)
  - Description
  - Current value
  - Expected value
  - Suggested fix

**Recommendations**:
- High-level guidance based on score
- Prioritized action items
- Links to relevant documentation

See `references/output-templates.md` for complete format specifications.
