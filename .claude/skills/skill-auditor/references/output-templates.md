# Output Templates

Format templates for skill audit outputs in CLI, Markdown, and JSON formats. Consistent with agent-auditor output patterns.

---

## CLI Output Format

Terminal-friendly output with color coding and clear visual hierarchy.

### Template

```
============================================
AUDIT SUMMARY
============================================
File: {skill_path}/SKILL.md
Type: Skill
Overall Score: {score}/10 (Grade: {grade})
Status: {PASSED|FAILED} (threshold: {threshold})

Category Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structure          {score}/10 {✓|✗}
Content Quality    {score}/10 {✓|✗}
Compliance         {score}/10 {✓|✗}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERRORS ({count}):
{if count > 0}
  [{rule_id}] {title}
  {description}
  Current: {current_value}
  Expected: {expected_value}
  Fix: {suggested_fix}
{else}
(none)
{endif}

WARNINGS ({count}):
{if count > 0}
  [{rule_id}] {title}
  {description}
  Fix: {suggested_fix}
{else}
(none)
{endif}

INFO ({count}):
{if count > 0}
  [{rule_id}] {message}
{else}
(none)
{endif}

SUGGESTIONS ({count}):
{if count > 0}
  [{rule_id}] {message}
  Benefit: {benefit_description}
{else}
(none)
{endif}

============================================
RECOMMENDATIONS
============================================
{recommendation_list}

Audit completed in {time}s
```

### Color Coding

```python
COLORS = {
    'ERROR': '\033[91m',     # Red
    'WARNING': '\033[93m',   # Yellow
    'INFO': '\033[94m',      # Blue
    'SUCCESS': '\033[92m',   # Green
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
}
```

Apply colors:
- **ERROR** lines: Red
- **WARNING** lines: Yellow
- **INFO** lines: Blue
- **PASSED** status: Green
- **FAILED** status: Red
- Section headers: Bold

### Visual Elements

**Status Indicators:**
- `✓` - Passed (green)
- `✗` - Failed (red)
- `!` - Warning (yellow)

**Score Bar:**
```
Structure          9.5/10 ✓✓✓✓✓✓✓✓✓·
Content Quality    8.0/10 ✓✓✓✓✓✓✓✓··
Compliance        10.0/10 ✓✓✓✓✓✓✓✓✓✓
```
- `✓` for each full point
- `·` for partial point
- 10 total characters

### Example: Perfect Score

```
============================================
AUDIT SUMMARY
============================================
File: .claude/skills/touchdesigner-python/SKILL.md
Type: Skill
Overall Score: 10.0/10 (Grade: A+)
Status: ✓ PASSED (threshold: 7.0)

Category Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structure          10.0/10 ✓✓✓✓✓✓✓✓✓✓
Content Quality    10.0/10 ✓✓✓✓✓✓✓✓✓✓
Compliance         10.0/10 ✓✓✓✓✓✓✓✓✓✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERRORS (0):
(none)

WARNINGS (0):
(none)

INFO (3):
  [S-PD-001] Progressive disclosure used effectively
  Progressive disclosure pattern detected with 3 reference files

  [S-PD-002] Reference navigation clear and helpful
  "When to Load References" section provides clear guidance

  [S-SC-006] Common Pitfalls section excellent
  6 pitfalls documented with ❌/✅ format

SUGGESTIONS (0):
(none)

============================================
RECOMMENDATIONS
============================================
1. Maintain current quality standards
2. Exemplary skill structure and content
3. All best practices followed
4. Reference this skill as a model for others

Audit completed in 0.18s
```

### Example: Failing Score

```
============================================
AUDIT SUMMARY
============================================
File: .claude/skills/helper/SKILL.md
Type: Skill
Overall Score: 5.7/10 (Grade: F)
Status: ✗ FAILED (threshold: 7.0)

Category Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structure           7.5/10 ✓✓✓✓✓✓✓··· !
Content Quality     5.0/10 ✓✓✓✓✓····· ✗
Compliance          7.0/10 ✓✓✓✓✓✓✓··· !
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERRORS (3):
  [S-FM-002] Name format invalid
  Name contains invalid characters
  Current: "Helper-Tool"
  Expected: "helper-tool"
  Fix: Convert to lowercase, remove invalid characters

  [S-FM-009] Description not in third person
  Description uses first/second person pronouns
  Current: "I can help you with tasks"
  Expected: "Provides assistance with tasks. Use when..."
  Fix: Rewrite in third person with trigger terms

  [S-SC-003] Quick Start section missing
  Required section not found
  Fix: Add Quick Start with 3 actionable steps

WARNINGS (4):
  [S-CT-004] SKILL.md exceeds line limit
  Line count: 632, Recommended: <500
  Suggestion: Move detailed content to references/

  [S-SC-008] Examples section missing
  Required section not found
  Fix: Add Examples section with 2+ concrete examples

  [S-SC-009] Insufficient Common Pitfalls
  Current: 1 item, Required: 3 minimum
  Fix: Add 2 more pitfalls with ❌/✅ format

  [S-RF-001] Nested reference detected
  File: references/advanced/patterns.md
  Required: Maximum 1 level deep
  Fix: Move to references/patterns.md

INFO (0):
(none)

SUGGESTIONS (1):
  [S-PD-001] Consider using progressive disclosure
  Benefit: Move advanced content to references/ for better token efficiency

============================================
RECOMMENDATIONS
============================================
Priority: Fix ERROR issues first
1. Rename skill to "helper-tool" (lowercase)
2. Rewrite description in third person with trigger terms
3. Add Quick Start section with 3 steps
4. Add Examples section with 2+ examples
5. Expand Common Pitfalls to 3+ items
6. Move content to references/ to get under 500 lines
7. Flatten reference structure (no nesting)

Audit completed in 0.24s
```

---

## Markdown Report Template

Complete audit report for saving to file.

### Template

```markdown
# Audit Report: {skill_name}

**Generated**: {timestamp}
**Type**: Skill
**Framework Version**: {version}

---

## Executive Summary

**Overall Score**: {score}/10 ({grade})
**Status**: {PASSED|FAILED} (threshold: {threshold})

{brief_summary_paragraph}

---

## Score Breakdown

| Category | Score | Weight | Weighted | Status |
|----------|-------|--------|----------|--------|
| Structure | {score}/10 | 30% | {weighted} | {✓|✗} |
| Content Quality | {score}/10 | 50% | {weighted} | {✓|✗} |
| Compliance | {score}/10 | 20% | {weighted} | {✓|✗} |
| **Total** | **{score}/10** | **100%** | **{score}** | **{✓|✗}** |

---

## Issues by Severity

### Errors ({count})

{if count > 0}
#### [{rule_id}] {title}

- **Severity**: ERROR
- **Category**: {category}
- **Description**: {description}
- **Current**: `{current_value}`
- **Expected**: `{expected_value}`
- **Fix**: {suggested_fix}

---
{else}
No errors found.
{endif}

### Warnings ({count})

{similar format}

### Info ({count})

{similar format}

### Suggestions ({count})

{similar format}

---

## Section Analysis

### Required Sections

| Section | Present | Quality | Issues |
|---------|---------|---------|--------|
| Role Statement | {✓|✗} | {score}/5 | {issue_list} |
| Purpose | {✓|✗} | {score}/5 | {issue_list} |
| Quick Start | {✓|✗} | {score}/5 | {issue_list} |
| Core Concepts | {✓|✗} | {score}/5 | {issue_list} |
| Common Pitfalls | {✓|✗} | {score}/5 | {issue_list} |
| When to Load References | {✓|✗} | {score}/5 | {issue_list} |
| Examples | {✓|✗} | {score}/5 | {issue_list} |

---

## Reference File Analysis

{if references exist}
### Reference Files Found

| File | Lines | Status | Issues |
|------|-------|--------|--------|
| {filename} | {line_count} | {✓|!|✗} | {issue_summary} |

### Reference Structure

```
{skill_name}/
├── SKILL.md ({line_count} lines)
└── references/
    ├── {file1}.md ({line_count} lines)
    ├── {file2}.md ({line_count} lines)
    └── {file3}.md ({line_count} lines)
```
{else}
No reference files found.

**Recommendation**: Consider using progressive disclosure for advanced content.
{endif}

---

## Recommendations

### Priority: {High|Medium|Low}

{ordered_recommendation_list}

---

## Suggested Fixes

{if auto-fixable issues exist}
The following issues can be addressed with specific fixes:

### [{rule_id}] {title}

**Current**:
```
{current_content}
```

**Suggested**:
```
{suggested_content}
```

**Explanation**: {why_this_fix}

---
{endif}

---

## Rule Reference

All rules evaluated in this audit:

| Rule ID | Category | Severity | Status | Description |
|---------|----------|----------|--------|-------------|
| {rule_id} | {category} | {severity} | {✓|✗|N/A} | {short_description} |

---

## Appendix: Skill Metadata

**Name**: `{name}`
**Description**: {description}
**Line Count**: {line_count} (body only, excluding frontmatter)
**Reference Files**: {count}
**Total Size**: ~{token_estimate} tokens

---

**Report Generated**: {timestamp}
**Audit Duration**: {duration}s
**Framework Version**: {version}
```

### Example Report

```markdown
# Audit Report: touchdesigner-python

**Generated**: 2025-12-11 14:30:45 UTC
**Type**: Skill
**Framework Version**: 1.0

---

## Executive Summary

**Overall Score**: 10.0/10 (A+)
**Status**: PASSED (threshold: 7.0)

The touchdesigner-python skill demonstrates exemplary structure and content quality. All required sections are present with high quality implementation. Progressive disclosure is used effectively with 3 well-organized reference files. The skill serves as an excellent reference for other skill implementations.

---

## Score Breakdown

| Category | Score | Weight | Weighted | Status |
|----------|-------|--------|----------|--------|
| Structure | 10.0/10 | 30% | 3.0 | ✓ |
| Content Quality | 10.0/10 | 50% | 5.0 | ✓ |
| Compliance | 10.0/10 | 20% | 2.0 | ✓ |
| **Total** | **10.0/10** | **100%** | **10.0** | **✓** |

---

## Issues by Severity

### Errors (0)

No errors found.

### Warnings (0)

No warnings found.

### Info (3)

#### [S-PD-001] Progressive disclosure used effectively

- **Severity**: INFO
- **Category**: Content Quality
- **Description**: Skill uses reference files for advanced content
- **Bonus**: +0.5 points

#### [S-PD-002] Reference navigation clear and helpful

- **Severity**: INFO
- **Category**: Content Quality
- **Description**: "When to Load References" section provides clear guidance
- **Bonus**: +0.2 points

#### [S-SC-006] Common Pitfalls section excellent

- **Severity**: INFO
- **Category**: Content Quality
- **Description**: 6 pitfalls documented with ❌/✅ format exceeds minimum requirement
- **Bonus**: +0.3 points

### Suggestions (0)

No suggestions.

---

## Section Analysis

### Required Sections

| Section | Present | Quality | Issues |
|---------|---------|---------|--------|
| Role Statement | ✓ | 5/5 | None |
| Purpose | ✓ | 5/5 | None |
| Quick Start | ✓ | 5/5 | None |
| Core Concepts | ✓ | 5/5 | None |
| Common Pitfalls | ✓ | 5/5 | None |
| When to Load References | ✓ | 5/5 | None |
| Examples | ✓ | 5/5 | None |

---

## Reference File Analysis

### Reference Files Found

| File | Lines | Status | Issues |
|------|-------|--------|--------|
| conventions.md | 385 | ✓ | None |
| extensions.md | 412 | ✓ | None |
| callbacks.md | 298 | ✓ | None |

### Reference Structure

```
touchdesigner-python/
├── SKILL.md (264 lines)
└── references/
    ├── conventions.md (385 lines)
    ├── extensions.md (412 lines)
    └── callbacks.md (298 lines)
```

---

## Recommendations

### Priority: Maintain

1. Continue following current structure and quality standards
2. This skill serves as an excellent reference for other implementations
3. Progressive disclosure pattern is well-executed
4. Reference this skill when creating similar domain-specific skills

---

## Rule Reference

All rules evaluated in this audit:

| Rule ID | Category | Severity | Status | Description |
|---------|----------|----------|--------|-------------|
| S-ST-001 | Structure | ERROR | ✓ | Directory structure valid |
| S-ST-002 | Structure | ERROR | ✓ | SKILL.md exists |
| S-FM-001 | Structure | ERROR | ✓ | Required fields present |
| S-SC-003 | Content Quality | WARNING | ✓ | Quick Start section present |
| S-SC-006 | Content Quality | INFO | ✓ | Common Pitfalls section |
| S-PD-001 | Content Quality | SUGGESTION | ✓ | Progressive disclosure used |
| ... | ... | ... | ... | ... |

---

## Appendix: Skill Metadata

**Name**: `touchdesigner-python`
**Description**: Guide for TouchDesigner Python extension development with tdu.Dependency, lifecycle callbacks, and type hints. Use when creating TD extensions, implementing callbacks, managing reactive state, or refactoring TD Python code.
**Line Count**: 264 (body only, excluding frontmatter)
**Reference Files**: 3
**Total Size**: ~4,200 tokens (estimated)

---

**Report Generated**: 2025-12-11 14:30:45 UTC
**Audit Duration**: 0.18s
**Framework Version**: 1.0
```

---

## JSON Output Schema

Machine-readable format for automation and integration.

### Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SkillAuditResults",
  "type": "object",
  "required": ["metadata", "score", "issues", "sections", "references"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["skill_path", "skill_name", "timestamp", "framework_version"],
      "properties": {
        "skill_path": {"type": "string"},
        "skill_name": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "framework_version": {"type": "string"},
        "audit_mode": {"enum": ["skill", "combined"]},
        "execution_time_ms": {"type": "number"}
      }
    },
    "score": {
      "type": "object",
      "required": ["total", "grade", "passed", "categories"],
      "properties": {
        "total": {"type": "number", "minimum": 0, "maximum": 10},
        "grade": {"type": "string", "pattern": "^(A\\+|A|B\\+|B|C\\+|C|D|F)$"},
        "passed": {"type": "boolean"},
        "threshold": {"type": "number", "default": 7.0},
        "categories": {
          "type": "object",
          "properties": {
            "structure": {"$ref": "#/definitions/CategoryScore"},
            "content_quality": {"$ref": "#/definitions/CategoryScore"},
            "compliance": {"$ref": "#/definitions/CategoryScore"}
          }
        }
      }
    },
    "issues": {
      "type": "array",
      "items": {"$ref": "#/definitions/Issue"}
    },
    "sections": {
      "type": "object",
      "properties": {
        "role_statement": {"$ref": "#/definitions/SectionStatus"},
        "purpose": {"$ref": "#/definitions/SectionStatus"},
        "quick_start": {"$ref": "#/definitions/SectionStatus"},
        "core_concepts": {"$ref": "#/definitions/SectionStatus"},
        "common_pitfalls": {"$ref": "#/definitions/SectionStatus"},
        "when_to_load_references": {"$ref": "#/definitions/SectionStatus"},
        "examples": {"$ref": "#/definitions/SectionStatus"}
      }
    },
    "references": {
      "type": "object",
      "properties": {
        "file_count": {"type": "integer", "minimum": 0},
        "files": {
          "type": "array",
          "items": {"$ref": "#/definitions/ReferenceFile"}
        }
      }
    },
    "suggestions": {
      "type": "array",
      "items": {"$ref": "#/definitions/Suggestion"}
    }
  },
  "definitions": {
    "CategoryScore": {
      "type": "object",
      "required": ["score", "weight", "max_score", "passed"],
      "properties": {
        "score": {"type": "number", "minimum": 0, "maximum": 10},
        "weight": {"type": "number", "minimum": 0, "maximum": 1},
        "max_score": {"type": "number", "default": 10},
        "passed": {"type": "boolean"},
        "issue_count": {
          "type": "object",
          "properties": {
            "errors": {"type": "integer", "minimum": 0},
            "warnings": {"type": "integer", "minimum": 0},
            "info": {"type": "integer", "minimum": 0}
          }
        }
      }
    },
    "Issue": {
      "type": "object",
      "required": ["rule_id", "severity", "category", "message"],
      "properties": {
        "rule_id": {"type": "string", "pattern": "^S-[A-Z]+-\\d{3}$"},
        "severity": {"enum": ["ERROR", "WARNING", "INFO", "SUGGESTION"]},
        "category": {"enum": ["Structure", "Content Quality", "Compliance"]},
        "message": {"type": "string"},
        "description": {"type": "string"},
        "current_value": {"type": "string"},
        "expected_value": {"type": "string"},
        "suggested_fix": {"type": "string"},
        "score_impact": {"type": "number"}
      }
    },
    "SectionStatus": {
      "type": "object",
      "required": ["present", "quality_score"],
      "properties": {
        "present": {"type": "boolean"},
        "quality_score": {"type": "number", "minimum": 0, "maximum": 5},
        "issues": {"type": "array", "items": {"type": "string"}}
      }
    },
    "ReferenceFile": {
      "type": "object",
      "required": ["filename", "path", "exists", "line_count"],
      "properties": {
        "filename": {"type": "string"},
        "path": {"type": "string"},
        "exists": {"type": "boolean"},
        "line_count": {"type": "integer", "minimum": 0},
        "issues": {"type": "array", "items": {"type": "string"}}
      }
    },
    "Suggestion": {
      "type": "object",
      "required": ["rule_id", "message"],
      "properties": {
        "rule_id": {"type": "string"},
        "message": {"type": "string"},
        "benefit": {"type": "string"}
      }
    }
  }
}
```

### Example JSON Output

```json
{
  "metadata": {
    "skill_path": ".claude/skills/touchdesigner-python",
    "skill_name": "touchdesigner-python",
    "timestamp": "2025-12-11T14:30:45.123Z",
    "framework_version": "1.0",
    "audit_mode": "skill",
    "execution_time_ms": 180
  },
  "score": {
    "total": 10.0,
    "grade": "A+",
    "passed": true,
    "threshold": 7.0,
    "categories": {
      "structure": {
        "score": 10.0,
        "weight": 0.30,
        "max_score": 10.0,
        "passed": true,
        "issue_count": {
          "errors": 0,
          "warnings": 0,
          "info": 0
        }
      },
      "content_quality": {
        "score": 10.0,
        "weight": 0.50,
        "max_score": 10.0,
        "passed": true,
        "issue_count": {
          "errors": 0,
          "warnings": 0,
          "info": 3
        }
      },
      "compliance": {
        "score": 10.0,
        "weight": 0.20,
        "max_score": 10.0,
        "passed": true,
        "issue_count": {
          "errors": 0,
          "warnings": 0,
          "info": 0
        }
      }
    }
  },
  "issues": [],
  "sections": {
    "role_statement": {
      "present": true,
      "quality_score": 5,
      "issues": []
    },
    "purpose": {
      "present": true,
      "quality_score": 5,
      "issues": []
    },
    "quick_start": {
      "present": true,
      "quality_score": 5,
      "issues": []
    },
    "core_concepts": {
      "present": true,
      "quality_score": 5,
      "issues": []
    },
    "common_pitfalls": {
      "present": true,
      "quality_score": 5,
      "issues": []
    },
    "when_to_load_references": {
      "present": true,
      "quality_score": 5,
      "issues": []
    },
    "examples": {
      "present": true,
      "quality_score": 5,
      "issues": []
    }
  },
  "references": {
    "file_count": 3,
    "files": [
      {
        "filename": "conventions.md",
        "path": "references/conventions.md",
        "exists": true,
        "line_count": 385,
        "issues": []
      },
      {
        "filename": "extensions.md",
        "path": "references/extensions.md",
        "exists": true,
        "line_count": 412,
        "issues": []
      },
      {
        "filename": "callbacks.md",
        "path": "references/callbacks.md",
        "exists": true,
        "line_count": 298,
        "issues": []
      }
    ]
  },
  "suggestions": [
    {
      "rule_id": "S-PD-001",
      "message": "Progressive disclosure used effectively",
      "benefit": "Advanced content organized in reference files reduces cognitive load"
    }
  ]
}
```

---

## Output File Naming

### Markdown Reports
- **Location**: `./audits/skills/`
- **Format**: `{skill-name}-audit.md`
- **Example**: `touchdesigner-python-audit.md`

### JSON Reports
- **Location**: `./audits/skills/`
- **Format**: `{skill-name}-audit.json`
- **Example**: `touchdesigner-python-audit.json`

### Combined Reports (with Agent Auditor)
- **Location**: `./audits/combined/`
- **Format**: `{agent-name}+{skill-name}-audit.{md|json}`
- **Example**: `touchdesigner-specialist+touchdesigner-python-audit.md`

---

## Formatting Guidelines

### CLI Output
- Use color sparingly for critical info
- Align columns for readability
- Use box drawing characters for section dividers
- Include visual score bars
- Keep under 120 columns wide

### Markdown Output
- Use tables for structured data
- Include expandable code blocks
- Link to rule definitions
- Provide complete context (standalone readable)
- Follow GitHub Flavored Markdown

### JSON Output
- Pretty-print with 2-space indentation
- Include all metadata for traceability
- Use consistent date formats (ISO 8601)
- Validate against schema before output
- Include version for backwards compatibility
