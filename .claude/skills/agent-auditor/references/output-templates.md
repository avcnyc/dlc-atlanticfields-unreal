# Output Templates

Complete format specifications for agent audit outputs in CLI, Markdown, and JSON formats.

---

## CLI Output Format

Terminal-friendly output with ANSI color codes for readability.

### ANSI Color Codes

```python
COLORS = {
    'ERROR': '\033[91m',     # Red
    'WARNING': '\033[93m',   # Yellow
    'INFO': '\033[94m',      # Blue
    'SUCCESS': '\033[92m',   # Green
    'BOLD': '\033[1m',       # Bold
    'RESET': '\033[0m'       # Reset
}
```

### Full CLI Template

```
============================================
AUDIT SUMMARY
============================================
File: {file_path}
Type: Agent
Overall Score: {score}/10 (Grade: {grade})
Status: {✓ PASSED | ✗ FAILED} (threshold: {threshold})

Category Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structure          {score}/10 {visual_bar}
Content Quality    {score}/10 {visual_bar}
Compliance         {score}/10 {visual_bar}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{if errors > 0}
ERRORS ({count}):
  {for each error}
  [{rule_id}] {title}
  {description}
  Current: {current_value}
  Expected: {expected_value}
  Fix: {suggested_fix}
  {end for}
{else}
ERRORS (0):
(none)
{end if}

{if warnings > 0}
WARNINGS ({count}):
  {for each warning}
  [{rule_id}] {title}
  {description}
  {if has_suggestion}
  Suggestion: {suggestion}
  {end if}
  {end for}
{end if}

{if info_items > 0}
INFO ({count}):
  {for each info}
  [{rule_id}] {title}
  {details}
  {end for}
{end if}

{if suggestions > 0}
SUGGESTIONS ({count}):
  {for each suggestion}
  [{rule_id}] {title}
  Benefit: {benefit}
  {end for}
{end if}

============================================
RECOMMENDATIONS
============================================
{recommendations_list}

Audit completed in {execution_time}s
```

### Visual Score Bar

Convert numeric score to visual representation:

```python
def create_visual_bar(score: float, max_score: float = 10.0) -> str:
    """
    Create visual bar for score display.

    Examples:
        10.0 → ✓✓✓✓✓✓✓✓✓✓
        8.5  → ✓✓✓✓✓✓✓✓·
        5.0  → ✓✓✓✓✓·····
    """
    filled = int(score)
    partial = 1 if (score - filled) >= 0.5 else 0
    empty = max_score - filled - partial

    return '✓' * filled + ('·' if partial else '') + ' ' * int(empty)
```

### Example: High-Quality Agent

```
============================================
AUDIT SUMMARY
============================================
File: .claude/agents/touchdesigner-python-specialist.md
Type: Agent
Overall Score: 9.8/10 (Grade: A+)
Status: ✓ PASSED (threshold: 7.0)

Category Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structure          10.0/10 ✓✓✓✓✓✓✓✓✓✓
Content Quality     9.7/10 ✓✓✓✓✓✓✓✓✓·
Compliance         10.0/10 ✓✓✓✓✓✓✓✓✓✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERRORS (0):
(none)

WARNINGS (1):
  [A-CT-004] System prompt is lengthy (126 lines)
  Line count: 126, Recommended: <200, Optimal: <100
  Suggestion: Consider extracting examples to skill reference

INFO (2):
  [A-QL-001] Excellent description quality (Score: 5/5)
  Contains what, when, examples, and trigger terms

  [A-QL-002] Proactive invocation marker present
  Found: "Use PROACTIVELY"

SUGGESTIONS (1):
  [S001] Consider adding output format specification
  Current: Not explicitly defined
  Benefit: Helps users know what to expect

============================================
RECOMMENDATIONS
============================================
1. Maintain current quality standards
2. System prompt is acceptable but could be more concise
3. All critical requirements met

Audit completed in 0.23s
```

### Example: Failed Agent

```
============================================
AUDIT SUMMARY
============================================
File: .claude/agents/helper.md
Type: Agent
Overall Score: 5.9/10 (Grade: F)
Status: ✗ FAILED (threshold: 7.0)

Category Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structure           6.0/10 ✓✓✓✓✓✓····
Content Quality     5.0/10 ✓✓✓✓✓·····
Compliance          8.0/10 ✓✓✓✓✓✓✓✓··
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERRORS (2):
  [A-FM-002] Name format invalid
  Name must use lowercase letters, numbers, and hyphens only
  Current: "Helper"
  Expected: "helper"
  Fix: Change name to "helper" in frontmatter

  [A-QL-001] Description quality poor (Score: 1/5)
  Description is too vague and lacks trigger terms
  Current: "Helps with tasks"
  Expected: Specific domain + when to use + examples
  Fix: Rewrite as: "[Domain expert]. Use PROACTIVELY when [trigger]. [Examples]."

WARNINGS (3):
  [A-QL-003] System prompt lacks role definition
  Recommendation: Add "You are a [specific role]..." at start

  [A-QL-004] System prompt lacks workflow
  Recommendation: Add "When invoked:" section with steps

  [A-QL-005] No examples provided
  Recommendation: Add <example> tags with concrete scenarios

============================================
RECOMMENDATIONS
============================================
1. Fix critical errors first (name format, description quality)
2. Add clear role definition and workflow to system prompt
3. Consider what specific problem this agent solves
4. Review agent-skill-best-practices.md for guidance

Audit completed in 0.18s
```

---

## Markdown Report Template

Comprehensive report suitable for saving to file or viewing in markdown viewer.

### Full Template

```markdown
# Audit Report: {filename}

**Generated**: {timestamp}
**Type**: Agent
**Framework Version**: {version}
**Auditor**: agent-auditor skill

---

## Executive Summary

**Overall Score**: {score}/10 ({grade})
**Status**: {PASSED|FAILED} (threshold: {threshold})

{2-3 sentence summary of audit results}

---

## Score Breakdown

| Category | Score | Weight | Weighted | Status |
|----------|-------|--------|----------|--------|
| Structure | {score}/10 | {weight}% | {weighted} | {✓|✗} |
| Content Quality | {score}/10 | {weight}% | {weighted} | {✓|✗} |
| Compliance | {score}/10 | {weight}% | {weighted} | {✓|✗} |
| **Total** | **{total}/10** | **100%** | **{total}** | **{✓|✗}** |

---

## Issues by Severity

### Errors ({count})

{if count > 0}
{for each error}
#### [{rule_id}] {title}

- **Severity**: ERROR
- **Category**: {category}
- **Description**: {description}
- **Location**: {location_info}
- **Current Value**: `{current_value}`
- **Expected Value**: `{expected_value}`
- **Score Impact**: -{impact} points

**Suggested Fix**:
```{language}
{fix_code_or_text}
```

---
{end for}
{else}
No errors found.
{end if}

### Warnings ({count})

{similar structure to errors}

### Info ({count})

{similar structure}

### Suggestions ({count})

{similar structure}

---

## Recommendations

Based on the audit results, here are prioritized recommendations:

1. **{priority_level}**: {recommendation_text}
2. **{priority_level}**: {recommendation_text}
3. **{priority_level}**: {recommendation_text}

---

## Detailed Analysis

### Frontmatter Analysis

**Required Fields**: {✓|✗}
- `name`: {value} {✓|✗}
- `description`: {value} {✓|✗}

**Optional Fields**:
- `tools`: {value_or_omitted}
- `model`: {value_or_omitted}
- `permissionMode`: {value_or_omitted}
- `skills`: {value_or_omitted}

### Content Analysis

**System Prompt Statistics**:
- Line count: {count} (recommended: <200)
- Has role definition: {✓|✗}
- Has workflow: {✓|✗}
- Has examples: {✓|✗}
- Has output format: {✓|✗}

**Description Quality**: {rating}/5
- What: {✓|✗}
- When: {✓|✗}
- Trigger terms: {✓|✗}
- Examples: {✓|✗}

### Compliance Analysis

**File Format**:
- UTF-8 encoding: {✓|✗}
- YAML well-formed: {✓|✗}
- Forward slashes: {✓|✗}

**Skill Integration** {if applicable}:
- Referenced skills exist: {✓|✗}
- Skill tool available: {✓|✗}
- No content duplication: {✓|✗}

---

## Rule Reference

All validation rules evaluated in this audit:

| Rule ID | Category | Severity | Status | Score Impact |
|---------|----------|----------|--------|--------------|
| A-FM-001 | Structure | ERROR | {✓|✗|N/A} | {impact} |
| A-FM-002 | Structure | ERROR | {✓|✗|N/A} | {impact} |
{... all applicable rules ...}

**Legend**:
- ✓ = Passed
- ✗ = Failed
- N/A = Not applicable

---

## Next Steps

{if passed}
**Congratulations!** This agent meets quality standards.

Consider:
- Sharing this agent with team via git
- Testing invocation with actual use cases
- Monitoring performance in production
{else}
**Action Required**: Address {error_count} error(s) before using in production.

Priority:
1. Fix all ERROR-level issues
2. Review and address WARNING-level issues
3. Consider INFO and SUGGESTION items for improvement
{end if}

---

**Report Generated**: {timestamp}
**Audit Duration**: {duration}s
**Framework**: Claude Code Orchestration System
**Specification**: auditor-framework-spec.md v1.0
```

### Example Report (Excerpt)

```markdown
# Audit Report: touchdesigner-python-specialist.md

**Generated**: 2025-12-11 14:32:18
**Type**: Agent
**Framework Version**: 1.0
**Auditor**: agent-auditor skill

---

## Executive Summary

**Overall Score**: 9.8/10 (A+)
**Status**: PASSED (threshold: 7.0)

This agent demonstrates exceptional quality with well-structured frontmatter, clear description with proactive invocation marker, and comprehensive system prompt. Minor room for improvement in system prompt length (126 lines).

---

## Score Breakdown

| Category | Score | Weight | Weighted | Status |
|----------|-------|--------|----------|--------|
| Structure | 10.0/10 | 30% | 3.0 | ✓ |
| Content Quality | 9.7/10 | 50% | 4.85 | ✓ |
| Compliance | 10.0/10 | 20% | 2.0 | ✓ |
| **Total** | **9.8/10** | **100%** | **9.85** | **✓** |

---

## Issues by Severity

### Errors (0)

No errors found.

### Warnings (1)

#### [A-CT-004] System prompt is lengthy (126 lines)

- **Severity**: WARNING
- **Category**: Content Quality
- **Description**: System prompt exceeds recommended 100-line optimal length
- **Current Value**: `126 lines`
- **Expected Value**: `<100 lines (optimal) or <200 lines (acceptable)`
- **Score Impact**: -0.3 points

**Suggested Fix**:
Consider extracting detailed examples and patterns to skill reference files. Keep core workflow and behavioral instructions in agent.

---

### Info (2)

#### [A-QL-001] Excellent description quality (Score: 5/5)

Description includes what the agent does, when to use it, trigger terms, and concrete examples. Sets clear expectation for invocation.

#### [A-QL-002] Proactive invocation marker present

Found "Use PROACTIVELY" in description, enabling automatic invocation by orchestration system.

---

## Recommendations

1. **Maintain**: Continue current quality standards
2. **Optimize**: Consider extracting examples to skill for slight improvement
3. **Monitor**: Test proactive invocation in real scenarios

---
```

---

## JSON Schema

Machine-readable output for integration with other tools.

### Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AgentAuditResults",
  "type": "object",
  "required": ["metadata", "score", "issues", "recommendations"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["file_path", "file_type", "timestamp", "framework_version"],
      "properties": {
        "file_path": {
          "type": "string",
          "description": "Absolute path to audited file"
        },
        "file_type": {
          "type": "string",
          "enum": ["agent"],
          "description": "Type of file audited"
        },
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp of audit"
        },
        "framework_version": {
          "type": "string",
          "description": "Version of auditor framework"
        },
        "execution_time_ms": {
          "type": "number",
          "description": "Audit execution time in milliseconds"
        }
      }
    },
    "score": {
      "type": "object",
      "required": ["total", "grade", "passed", "categories"],
      "properties": {
        "total": {
          "type": "number",
          "minimum": 0,
          "maximum": 10,
          "description": "Overall weighted score"
        },
        "grade": {
          "type": "string",
          "pattern": "^(A\\+|A|B\\+|B|C\\+|C|D|F)$",
          "description": "Letter grade"
        },
        "passed": {
          "type": "boolean",
          "description": "Whether audit passed threshold"
        },
        "threshold": {
          "type": "number",
          "default": 7.0,
          "description": "Pass/fail threshold"
        },
        "categories": {
          "type": "object",
          "required": ["structure", "content_quality", "compliance"],
          "properties": {
            "structure": {
              "$ref": "#/definitions/CategoryScore"
            },
            "content_quality": {
              "$ref": "#/definitions/CategoryScore"
            },
            "compliance": {
              "$ref": "#/definitions/CategoryScore"
            }
          }
        }
      }
    },
    "issues": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/Issue"
      },
      "description": "List of all issues found"
    },
    "recommendations": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "High-level recommendations"
    },
    "fixes": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/Fix"
      },
      "description": "Suggested fixes for issues"
    }
  },
  "definitions": {
    "CategoryScore": {
      "type": "object",
      "required": ["score", "weight", "max_score", "passed"],
      "properties": {
        "score": {
          "type": "number",
          "minimum": 0,
          "maximum": 10
        },
        "weight": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Weight in overall score calculation"
        },
        "max_score": {
          "type": "number",
          "default": 10
        },
        "passed": {
          "type": "boolean"
        },
        "issue_count": {
          "type": "object",
          "properties": {
            "errors": {"type": "integer", "minimum": 0},
            "warnings": {"type": "integer", "minimum": 0},
            "info": {"type": "integer", "minimum": 0},
            "suggestions": {"type": "integer", "minimum": 0}
          }
        }
      }
    },
    "Issue": {
      "type": "object",
      "required": ["rule_id", "severity", "category", "message"],
      "properties": {
        "rule_id": {
          "type": "string",
          "pattern": "^A-[A-Z]+-\\d{3}$",
          "description": "Rule identifier (e.g., A-FM-001)"
        },
        "severity": {
          "type": "string",
          "enum": ["ERROR", "WARNING", "INFO", "SUGGESTION"]
        },
        "category": {
          "type": "string",
          "enum": ["Structure", "Content Quality", "Compliance"]
        },
        "message": {
          "type": "string",
          "description": "Brief issue description"
        },
        "description": {
          "type": "string",
          "description": "Detailed issue explanation"
        },
        "location": {
          "type": "object",
          "properties": {
            "line": {"type": "integer", "minimum": 1},
            "column": {"type": "integer", "minimum": 1},
            "context": {"type": "string"}
          }
        },
        "current_value": {
          "type": "string",
          "description": "Current (problematic) value"
        },
        "expected_value": {
          "type": "string",
          "description": "Expected/correct value"
        },
        "score_impact": {
          "type": "number",
          "description": "Points deducted (negative) or added (positive)"
        }
      }
    },
    "Fix": {
      "type": "object",
      "required": ["rule_id", "file", "type", "suggested"],
      "properties": {
        "rule_id": {
          "type": "string",
          "description": "Rule that triggered this fix"
        },
        "file": {
          "type": "string",
          "description": "File to modify"
        },
        "type": {
          "type": "string",
          "enum": ["replace", "insert", "delete", "reformat"],
          "description": "Type of fix operation"
        },
        "line": {
          "type": "integer",
          "description": "Line number (1-indexed)"
        },
        "current": {
          "type": "string",
          "description": "Current text"
        },
        "suggested": {
          "type": "string",
          "description": "Suggested replacement"
        },
        "confidence": {
          "type": "string",
          "enum": ["high", "medium", "low"],
          "description": "Confidence in auto-fix safety"
        },
        "auto_fixable": {
          "type": "boolean",
          "description": "Whether fix can be applied automatically"
        }
      }
    }
  }
}
```

### Example JSON Output

```json
{
  "metadata": {
    "file_path": ".claude/agents/touchdesigner-python-specialist.md",
    "file_type": "agent",
    "timestamp": "2025-12-11T14:32:18Z",
    "framework_version": "1.0",
    "execution_time_ms": 234
  },
  "score": {
    "total": 9.8,
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
          "info": 0,
          "suggestions": 0
        }
      },
      "content_quality": {
        "score": 9.7,
        "weight": 0.50,
        "max_score": 10.0,
        "passed": true,
        "issue_count": {
          "errors": 0,
          "warnings": 1,
          "info": 2,
          "suggestions": 0
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
          "info": 0,
          "suggestions": 0
        }
      }
    }
  },
  "issues": [
    {
      "rule_id": "A-CT-004",
      "severity": "WARNING",
      "category": "Content Quality",
      "message": "System prompt is lengthy (126 lines)",
      "description": "System prompt exceeds recommended 100-line optimal length but is under 200-line acceptable limit",
      "current_value": "126 lines",
      "expected_value": "<100 lines (optimal) or <200 lines (acceptable)",
      "score_impact": -0.3
    },
    {
      "rule_id": "A-QL-001",
      "severity": "INFO",
      "category": "Content Quality",
      "message": "Excellent description quality (Score: 5/5)",
      "description": "Description includes what, when, trigger terms, and examples",
      "score_impact": 1.0
    },
    {
      "rule_id": "A-QL-002",
      "severity": "INFO",
      "category": "Content Quality",
      "message": "Proactive invocation marker present",
      "description": "Found 'Use PROACTIVELY' in description",
      "score_impact": 0.5
    }
  ],
  "recommendations": [
    "Maintain current quality standards",
    "Consider extracting examples to skill for slight optimization",
    "Test proactive invocation in production scenarios"
  ],
  "fixes": []
}
```

---

## Output Generation Guidelines

### When to Use Each Format

**CLI Output**:
- Interactive terminal usage
- Quick validation checks
- CI/CD pipeline integration
- Real-time feedback during development

**Markdown Report**:
- Detailed review documentation
- Sharing with team
- Archiving audit history
- Integration into documentation sites

**JSON Output**:
- Programmatic processing
- Integration with other tools
- Batch analysis
- Dashboard visualization
- CI/CD automated decision-making

### File Naming Conventions

Save outputs to `./audits/agents/` directory:

- Markdown: `{agent-name}-audit.md`
- JSON: `{agent-name}-audit.json`
- Combined: `{agent-name}-audit-{timestamp}.md`

Examples:
- `./audits/agents/touchdesigner-python-specialist-audit.md`
- `./audits/agents/code-reviewer-audit.json`
- `./audits/agents/api-tester-audit-2025-12-11.md`

### Color Coding Guidelines (CLI)

Use colors to enhance readability:

- **Red (ERROR)**: Critical issues requiring immediate attention
- **Yellow (WARNING)**: Important issues to address soon
- **Blue (INFO)**: Informational, positive feedback, or bonuses
- **Green (SUCCESS)**: Pass status, high scores
- **Bold**: Section headers, scores, grades

Ensure compatibility:
- Include plain text fallback for terminals without color support
- Use `--no-color` flag option for CI/CD environments
- Test with both light and dark terminal themes
