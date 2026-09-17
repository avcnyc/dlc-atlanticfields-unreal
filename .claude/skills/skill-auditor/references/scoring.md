# Scoring Implementation

Complete scoring algorithm for skill audits, including category weights, calculation formulas, and grade mapping. Consistent with agent-auditor scoring system.

---

## Overview

The scoring system evaluates skills across three weighted categories, applies issue penalties and quality bonuses, then calculates a final 0-10 score with corresponding letter grade.

**Design Principles**:
- Content quality weighted highest (50%) - most important for knowledge delivery
- Structure ensures basic functionality (30%)
- Compliance prevents common pitfalls (20%)
- Transparent calculation with clear score impacts
- Bonuses reward exceptional quality and progressive disclosure

---

## Category Weights

```python
CATEGORY_WEIGHTS = {
    "structure": 0.30,        # 30% - Foundational correctness
    "content_quality": 0.50,  # 50% - Most important for effectiveness
    "compliance": 0.20        # 20% - Standards adherence
}
```

### Rationale

**Content Quality (50%)**:
- Section completeness determines knowledge coverage
- Description clarity determines when skill is discovered
- Example quality determines how well users learn
- Most impactful on user experience and learning

**Structure (30%)**:
- Directory structure enables skill loading
- SKILL.md existence is fundamental
- Required sections provide complete knowledge package
- Foundation for everything else

**Compliance (20%)**:
- Line count limits prevent context bloat
- Reference organization enables progressive disclosure
- Third-person descriptions prevent point-of-view conflicts
- Best practices prevent common mistakes

---

## Severity Levels and Score Impact

```python
class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    SUGGESTION = "SUGGESTION"

SEVERITY_IMPACT = {
    Severity.ERROR: -2.0,      # Critical failure
    Severity.WARNING: -0.5,     # Should fix
    Severity.INFO: -0.1,        # Minor issue or informational
    Severity.SUGGESTION: 0.0    # No penalty, optional improvement
}
```

### Severity Guidelines

**ERROR (-2.0 points)**:
- Directory not a folder or SKILL.md missing
- Missing required fields (name, description)
- Invalid YAML syntax or frontmatter
- Reserved word violations
- Referenced files don't exist
- UTF-8 encoding issues
- Missing required sections (Quick Start, Examples)

**WARNING (-0.5 to -1.0 points)**:
- Optional field format issues
- SKILL.md exceeds recommended length (500 lines)
- Missing recommended sections (Common Pitfalls)
- Nested reference files (>1 level deep)
- Folder name doesn't match skill name
- Windows path formatting
- Insufficient examples (<2)

**INFO (-0.3 to +0.5 points)**:
- Description quality rating (variable)
- Section quality assessments
- Progressive disclosure bonuses
- Reference navigation quality
- Terminology consistency

**SUGGESTION (0.0 points)**:
- Purely optional enhancements
- Alternative organizational approaches
- Minor optimizations

---

## Bonus Points

Quality indicators that add to score:

```python
BONUSES = {
    "progressive_disclosure": 0.5,      # Reference files used effectively
    "reference_navigation": 0.2,        # Clear "When to Load" guidance
    "domain_organization": 0.2,         # References organized by domain
    "excellent_pitfalls": 0.3,          # Common Pitfalls with ≥3 items
    "core_concepts_present": 0.3,       # Core Concepts section exists
}
```

### Maximum Bonus Cap

Each category capped at 12.0 during calculation, then normalized to 10.0 for display. This allows bonuses to offset penalties while maintaining 0-10 scale.

---

## Scoring Algorithm

### Step 1: Initialize Scores

```python
def initialize_scores() -> dict[str, float]:
    """
    All categories start at perfect 10.0.

    Returns:
        Dictionary of category names to scores
    """
    return {
        "structure": 10.0,
        "content_quality": 10.0,
        "compliance": 10.0
    }
```

### Step 2: Apply Penalties

```python
def apply_penalties(scores: dict[str, float], issues: list[Issue]) -> dict[str, float]:
    """
    Deduct points based on issue severity and category.

    Args:
        scores: Current category scores
        issues: List of validation issues

    Returns:
        Updated scores after penalties
    """
    for issue in issues:
        # Map issue category to score category key
        category_key = issue.category.lower().replace(" ", "_")

        # Apply score impact (negative for penalties)
        scores[category_key] = max(0.0, scores[category_key] + issue.score_impact)

    return scores
```

### Step 3: Apply Bonuses

```python
def apply_bonuses(scores: dict[str, float], bonuses: list[Bonus]) -> dict[str, float]:
    """
    Add bonus points for exceptional quality indicators.

    Args:
        scores: Current category scores
        bonuses: List of quality bonuses

    Returns:
        Updated scores after bonuses (capped at 12.0, then normalized to 10.0)
    """
    for bonus in bonuses:
        category_key = bonus.category.lower().replace(" ", "_")

        # Add bonus (cap at 12.0 to allow offsetting penalties)
        scores[category_key] = min(12.0, scores[category_key] + bonus.value)

    # Normalize back to 10.0 max for final display
    return {k: min(10.0, v) for k, v in scores.items()}
```

### Step 4: Calculate Weighted Total

```python
def calculate_overall_score(category_scores: dict[str, float]) -> float:
    """
    Compute weighted average across categories.

    Formula:
        total = Σ(category_score * category_weight)

    Args:
        category_scores: Final category scores (after penalties and bonuses)

    Returns:
        Overall score (0-10, rounded to 1 decimal place)
    """
    total = 0.0

    for category, score in category_scores.items():
        weight = CATEGORY_WEIGHTS[category]
        total += score * weight

    return round(total, 1)
```

### Step 5: Determine Grade

```python
def calculate_grade(score: float) -> str:
    """
    Map 0-10 score to letter grade.

    Grade Boundaries:
        9.5-10.0: A+ (Exceptional)
        9.0-9.4:  A  (Excellent)
        8.5-8.9:  B+ (Very Good)
        8.0-8.4:  B  (Good)
        7.5-7.9:  C+ (Satisfactory)
        7.0-7.4:  C  (Acceptable)
        6.0-6.9:  D  (Needs Improvement)
        0.0-5.9:  F  (Failing)

    Args:
        score: Overall score (0-10)

    Returns:
        Letter grade
    """
    if score >= 9.5: return "A+"
    if score >= 9.0: return "A"
    if score >= 8.5: return "B+"
    if score >= 8.0: return "B"
    if score >= 7.5: return "C+"
    if score >= 7.0: return "C"
    if score >= 6.0: return "D"
    return "F"
```

### Step 6: Check Pass/Fail

```python
def check_passed(score: float, threshold: float = 7.0) -> bool:
    """
    Determine if audit passed.

    Default threshold: 7.0 (Grade C)
    Rationale: C grade means "acceptable for production use"

    Args:
        score: Overall score
        threshold: Minimum passing score (default 7.0)

    Returns:
        True if passed, False otherwise
    """
    return score >= threshold
```

---

## Complete Scoring Function

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Issue:
    """Validation issue."""
    rule_id: str
    severity: str
    category: str  # "Structure", "Content Quality", or "Compliance"
    message: str
    score_impact: float  # Negative for penalties

@dataclass
class Bonus:
    """Quality bonus."""
    name: str
    category: str
    value: float  # Positive

@dataclass
class CategoryScore:
    """Score for a single category."""
    name: str
    score: float
    weight: float
    max_score: float
    passed: bool
    issues: List[Issue]

@dataclass
class OverallScore:
    """Complete audit score."""
    total: float
    grade: str
    categories: dict[str, CategoryScore]
    passed: bool
    pass_threshold: float

def calculate_audit_score(issues: List[Issue], bonuses: List[Bonus]) -> OverallScore:
    """
    Main scoring algorithm.

    Process:
    1. Initialize perfect scores (10.0 each category)
    2. Apply penalties from issues
    3. Apply bonuses for quality indicators
    4. Calculate weighted total
    5. Determine grade and pass/fail

    Args:
        issues: List of validation issues
        bonuses: List of quality bonuses

    Returns:
        Complete audit score
    """
    # Step 1: Initialize
    scores = initialize_scores()

    # Step 2: Penalties
    scores = apply_penalties(scores, issues)

    # Step 3: Bonuses
    scores = apply_bonuses(scores, bonuses)

    # Step 4: Weighted total
    total = calculate_overall_score(scores)

    # Step 5: Grade
    grade = calculate_grade(total)

    # Step 6: Pass/fail
    passed = check_passed(total)

    # Build category score objects
    categories = {}
    for name, score in scores.items():
        category_name = name.replace("_", " ").title()
        category_issues = [i for i in issues if i.category.lower().replace(" ", "_") == name]

        categories[name] = CategoryScore(
            name=category_name,
            score=score,
            weight=CATEGORY_WEIGHTS[name],
            max_score=10.0,
            passed=score >= 7.0,
            issues=category_issues
        )

    return OverallScore(
        total=total,
        grade=grade,
        categories=categories,
        passed=passed,
        pass_threshold=7.0
    )
```

---

## Example Calculations

### Example 1: Excellent Skill (touchdesigner-python)

**Issues**: None

**Bonuses**:
- Progressive disclosure used: +0.5 (content_quality)
- Reference navigation clear: +0.2 (content_quality)
- Common Pitfalls excellent (6 items): +0.3 (content_quality)
- Core Concepts present: +0.3 (content_quality)

**Calculation**:
```
Initial scores:
  Structure:       10.0
  Content Quality: 10.0
  Compliance:      10.0

Apply penalties:
  (none)

Apply bonuses:
  Structure:       10.0 (no bonuses)
  Content Quality: 10.0 + 0.5 + 0.2 + 0.3 + 0.3 = 11.3 → capped at 10.0
  Compliance:      10.0 (no bonuses)

Weighted total:
  = (10.0 * 0.30) + (10.0 * 0.50) + (10.0 * 0.20)
  = 3.0 + 5.0 + 2.0
  = 10.0

Grade: A+ (score ≥ 9.5)
Status: PASSED (10.0 ≥ 7.0)
```

### Example 2: Poor Skill (helper)

**Issues**:
- [S-FM-002] Name format invalid: ERROR, -2.0 (structure)
- [S-FM-009] Description first person: ERROR, -2.0 (structure)
- [S-SC-003] Quick Start missing: WARNING, -1.0 (content_quality)
- [S-SC-008] Examples missing: WARNING, -1.0 (content_quality)
- [S-SC-009] Insufficient pitfalls (1 item): WARNING, -0.5 (content_quality)
- [S-CT-004] SKILL.md too long (632 lines): WARNING, -0.5 (compliance)

**Bonuses**: None

**Calculation**:
```
Initial scores:
  Structure:       10.0
  Content Quality: 10.0
  Compliance:      10.0

Apply penalties:
  Structure:       10.0 - 2.0 - 2.0 = 6.0
  Content Quality: 10.0 - 1.0 - 1.0 - 0.5 = 7.5
  Compliance:      10.0 - 0.5 = 9.5

Apply bonuses:
  (none)

Weighted total:
  = (6.0 * 0.30) + (7.5 * 0.50) + (9.5 * 0.20)
  = 1.8 + 3.75 + 1.9
  = 7.45
  = 7.5 (rounded)

Grade: C+ (7.5 ≤ score < 8.0)
Status: PASSED (7.5 ≥ 7.0) - barely
```

### Example 3: Failing Skill (multiple errors)

**Issues**:
- [S-ST-002] SKILL.md missing: ERROR, -2.0 (structure)
- [S-FM-001] Missing description: ERROR, -2.0 (structure)
- [S-SC-003] Quick Start missing: WARNING, -1.0 (content_quality)
- [S-SC-008] Examples missing: WARNING, -1.0 (content_quality)
- [S-CT-003] No body content: ERROR, -2.0 (content_quality)

**Bonuses**: None

**Calculation**:
```
Initial scores:
  Structure:       10.0
  Content Quality: 10.0
  Compliance:      10.0

Apply penalties:
  Structure:       10.0 - 2.0 - 2.0 = 6.0
  Content Quality: 10.0 - 1.0 - 1.0 - 2.0 = 6.0
  Compliance:      10.0 (no issues)

Weighted total:
  = (6.0 * 0.30) + (6.0 * 0.50) + (10.0 * 0.20)
  = 1.8 + 3.0 + 2.0
  = 6.8

Grade: D (6.0 ≤ score < 7.0)
Status: FAILED (6.8 < 7.0)
```

### Example 4: Good Skill with Minor Issues

**Issues**:
- [S-CT-004] SKILL.md slightly long (550 lines): WARNING, -0.5 (compliance)
- [S-RF-003] Reference file short (150 lines): INFO, -0.2 (compliance)

**Bonuses**:
- Progressive disclosure used: +0.5 (content_quality)
- Common Pitfalls present (3 items): +0.3 (content_quality)

**Calculation**:
```
Initial scores:
  Structure:       10.0
  Content Quality: 10.0
  Compliance:      10.0

Apply penalties:
  Structure:       10.0 (no issues)
  Content Quality: 10.0 (no direct penalties)
  Compliance:      10.0 - 0.5 - 0.2 = 9.3

Apply bonuses:
  Structure:       10.0 (no bonuses)
  Content Quality: 10.0 + 0.5 + 0.3 = 10.8 → capped at 10.0
  Compliance:      9.3 (no bonuses)

Weighted total:
  = (10.0 * 0.30) + (10.0 * 0.50) + (9.3 * 0.20)
  = 3.0 + 5.0 + 1.86
  = 9.86
  = 9.9 (rounded)

Grade: A+ (score ≥ 9.5)
Status: PASSED (9.9 ≥ 7.0)
```

---

## Grade Mapping Table

| Grade | Score Range | Meaning | Production Ready? |
|-------|-------------|---------|-------------------|
| A+ | 9.5-10.0 | Exceptional quality, exemplary | Yes |
| A | 9.0-9.4 | Excellent, minor room for improvement | Yes |
| B+ | 8.5-8.9 | Very good, recommended fixes available | Yes |
| B | 8.0-8.4 | Good, some improvements needed | Yes |
| C+ | 7.5-7.9 | Satisfactory, several issues to address | Yes (with caution) |
| C | 7.0-7.4 | Acceptable minimum, fix warnings | Yes (minimum bar) |
| D | 6.0-6.9 | Needs improvement, has errors | No (fix errors first) |
| F | 0.0-5.9 | Failing, major issues | No (extensive fixes needed) |

---

## Pass/Fail Threshold

**Default Threshold**: 7.0 (Grade C)

**Rationale**:
- Grade C represents "acceptable for production use"
- Ensures no critical errors (ERRORs typically drop score below 7.0)
- Allows some warnings but not excessive
- Requires minimum quality standards met
- Encourages improvement beyond minimum

**Configurable**:
```python
# Default
passed = check_passed(score)  # Uses 7.0

# Custom threshold
passed = check_passed(score, threshold=8.0)  # Stricter (Grade B minimum)
passed = check_passed(score, threshold=6.0)  # Lenient (Grade D acceptable)
```

---

## Category Pass Criteria

Individual categories also have implicit pass criteria:

```python
CATEGORY_PASS_THRESHOLD = 7.0

for category_name, category_score in categories.items():
    category_score.passed = category_score.score >= CATEGORY_PASS_THRESHOLD
```

This allows reporting which categories passed/failed independently:

```
Category Breakdown:
Structure           6.0/10 ✗ (failed)
Content Quality     8.5/10 ✓ (passed)
Compliance         10.0/10 ✓ (passed)
```

---

## Score Impact Reference

Quick reference for common skill issues:

| Issue Type | Severity | Impact | Category |
|-----------|----------|--------|----------|
| SKILL.md missing | ERROR | -2.0 | Structure |
| Missing required field | ERROR | -2.0 | Structure |
| Invalid name format | ERROR | -2.0 | Structure |
| YAML malformed | ERROR | -2.0 | Structure |
| Quick Start missing | WARNING | -1.0 | Content Quality |
| Examples missing | WARNING | -1.0 | Content Quality |
| Missing description | ERROR | -2.0 | Structure |
| Description first person | ERROR | -2.0 | Structure |
| No body content | ERROR | -2.0 | Content Quality |
| Referenced file missing | ERROR | -1.0 | Structure |
| SKILL.md >500 lines | WARNING | -0.5 to -2.0 | Compliance |
| Insufficient pitfalls (<3) | WARNING | -0.5 | Content Quality |
| Nested references | WARNING | -0.5 each | Compliance |
| Reference file wrong size | INFO | -0.2 | Compliance |
| Windows paths | WARNING | -0.1 each | Compliance |
| UTF-8 encoding issue | ERROR | -2.0 | Compliance |
| Progressive disclosure used | INFO | +0.5 | Content Quality |
| Reference navigation clear | INFO | +0.2 | Content Quality |
| Domain organization | INFO | +0.2 | Content Quality |
| Common Pitfalls excellent | INFO | +0.3 | Content Quality |
| Core Concepts present | INFO | +0.3 | Content Quality |

---

## Implementation Notes

### Handling Edge Cases

**Multiple Penalties in Same Category**:
- Sum all penalties
- Apply floor at 0.0 (category can't go negative)
- Example: Structure with 3 ERROR issues = 10.0 - 6.0 = 4.0

**Bonuses Without Offsetting Penalties**:
- Cap at 10.0 for display
- During calculation, allow up to 12.0 to offset penalties
- Normalize before final output

**Mixed Severity Issues**:
- Process all issues regardless of order
- Final score is deterministic (order doesn't matter)

### Precision

- Category scores: 1 decimal place (e.g., 9.5)
- Overall score: 1 decimal place (e.g., 8.7)
- Weights: 2 decimal places (e.g., 0.30)
- Score impacts: 1 decimal place (e.g., -0.5)

### Validation

Before outputting score:
1. Verify all category scores in range [0.0, 10.0]
2. Verify overall score in range [0.0, 10.0]
3. Verify grade matches score range
4. Verify weights sum to 1.0

---

## Skill-Specific Scoring Considerations

### Line Count Impact

SKILL.md line count has tiered impact:
- <500 lines: No penalty
- 500-700 lines: -0.5 (warning)
- 700-1000 lines: -1.0 (strong warning)
- 1000+ lines: -2.0 (error level, requires refactoring)

### Section Quality

Each required section contributes to content quality:
- Missing section: -1.0 (Quick Start, Examples)
- Missing section: -0.5 (Role statement, Common Pitfalls)
- Present with issues: -0.3 to -0.5
- Present and high quality: +0.3 bonus

### Reference File Organization

Quality indicators for references:
- 0 references, skill >500 lines: Missed opportunity (-0.5)
- 1+ references, well-organized: Bonus (+0.5)
- References with clear navigation: Bonus (+0.2)
- Domain-based structure: Bonus (+0.2)

### Progressive Disclosure Bonus Stacking

Maximum bonus for progressive disclosure pattern:
- Base: +0.5 (references used)
- Navigation: +0.2 (clear guidance)
- Organization: +0.2 (domain structure)
- **Total possible**: +0.9 bonus to Content Quality

This can offset up to 1.8 WARNING issues or lift already-perfect content to account for minor penalties elsewhere.
