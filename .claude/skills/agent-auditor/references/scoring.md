# Scoring Implementation

Complete scoring algorithm for agent audits, including category weights, calculation formulas, and grade mapping.

---

## Overview

The scoring system evaluates agents across three weighted categories, applies issue penalties and quality bonuses, then calculates a final 0-10 score with corresponding letter grade.

**Design Principles**:
- Content quality weighted highest (50%) - most important for effectiveness
- Structure ensures basic functionality (30%)
- Compliance prevents common pitfalls (20%)
- Transparent calculation with clear score impacts
- Bonuses reward exceptional quality

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
- Description clarity determines when agent is invoked
- System prompt quality determines how well agent performs
- Examples improve agent effectiveness
- Most impactful on user experience

**Structure (30%)**:
- Required fields enable basic functionality
- Valid YAML allows parsing
- Proper format prevents runtime errors
- Foundation for everything else

**Compliance (20%)**:
- Encoding and path issues cause subtle bugs
- Reserved words prevent naming conflicts
- Skill integration ensures knowledge reuse
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
- Missing required fields
- Invalid YAML syntax
- Malformed frontmatter
- Reserved word violations
- Referenced skills don't exist
- UTF-8 encoding issues

**WARNING (-0.5 points)**:
- Optional field format issues
- System prompt exceeds recommended length
- Missing role definition or workflow
- Windows path formatting
- Skill tool not available
- Content duplication with skill

**INFO (-0.1 or bonus points)**:
- Description quality rating (variable: -2.0 to +1.0)
- Proactive marker present (+0.5)
- Examples in system prompt (+0.3)
- Output format specified (+0.2)

**SUGGESTION (0.0 points)**:
- Purely optional enhancements
- Alternative approaches
- Minor optimizations

---

## Bonus Points

Quality indicators that add to score:

```python
BONUSES = {
    "proactive_marker": 0.5,          # "Use PROACTIVELY" in description
    "excellent_description": 1.0,     # Description quality score 5/5
    "good_description": 0.0,          # Description quality score 4/5 (neutral)
    "examples_in_prompt": 0.3,        # <example> tags or Example: headers
    "output_format_specified": 0.2,   # Output format section present
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

### Example 1: Excellent Agent (touchdesigner-python-specialist)

**Issues**:
- [A-CT-004] System prompt lengthy (126 lines): WARNING, -0.5 (content_quality)

**Bonuses**:
- Proactive marker present: +0.5 (content_quality)
- Excellent description (5/5): +1.0 (content_quality)
- Examples in prompt: +0.3 (content_quality)

**Calculation**:
```
Initial scores:
  Structure:       10.0
  Content Quality: 10.0
  Compliance:      10.0

Apply penalties:
  Structure:       10.0 (no issues)
  Content Quality: 10.0 - 0.5 = 9.5
  Compliance:      10.0 (no issues)

Apply bonuses:
  Structure:       10.0 (no bonuses)
  Content Quality: 9.5 + 0.5 + 1.0 + 0.3 = 11.3 → capped at 10.0
  Compliance:      10.0 (no bonuses)

Weighted total:
  = (10.0 * 0.30) + (10.0 * 0.50) + (10.0 * 0.20)
  = 3.0 + 5.0 + 2.0
  = 10.0

Grade: A+ (score ≥ 9.5)
Status: PASSED (10.0 ≥ 7.0)
```

**Note**: In practice, with the -0.5 penalty, the score would be:
```
Content Quality after penalty: 9.5
Content Quality after bonuses: 9.5 + 1.8 = 10.0 (capped, but effectively 10.0)

Weighted:
  = (10.0 * 0.30) + (10.0 * 0.50) + (10.0 * 0.20)
  = 10.0

Final: 10.0 (A+)
```

### Example 2: Poor Agent (helper)

**Issues**:
- [A-FM-002] Name format invalid: ERROR, -2.0 (structure)
- [A-QL-001] Description quality poor (1/5): INFO, -2.0 (content_quality)
- [A-QL-003] No role definition: WARNING, -0.5 (content_quality)
- [A-QL-004] No workflow: WARNING, -0.5 (content_quality)
- [A-QL-005] No examples: WARNING, -0.5 (content_quality)

**Bonuses**: None

**Calculation**:
```
Initial scores:
  Structure:       10.0
  Content Quality: 10.0
  Compliance:      10.0

Apply penalties:
  Structure:       10.0 - 2.0 = 8.0
  Content Quality: 10.0 - 2.0 - 0.5 - 0.5 - 0.5 = 6.5
  Compliance:      10.0 (no issues)

Apply bonuses:
  (none)

Weighted total:
  = (8.0 * 0.30) + (6.5 * 0.50) + (10.0 * 0.20)
  = 2.4 + 3.25 + 2.0
  = 7.65
  = 7.7 (rounded)

Grade: C+ (7.5 ≤ score < 8.0)
Status: PASSED (7.7 ≥ 7.0)
```

### Example 3: Failing Agent (multiple errors)

**Issues**:
- [A-FM-001] Missing description: ERROR, -2.0 (structure)
- [A-FM-002] Invalid name format: ERROR, -2.0 (structure)
- [A-CT-003] No system prompt: ERROR, -2.0 (content_quality)
- [A-QL-003] No role: WARNING, -0.5 (content_quality)
- [A-QL-004] No workflow: WARNING, -0.5 (content_quality)

**Bonuses**: None

**Calculation**:
```
Initial scores:
  Structure:       10.0
  Content Quality: 10.0
  Compliance:      10.0

Apply penalties:
  Structure:       10.0 - 2.0 - 2.0 = 6.0
  Content Quality: 10.0 - 2.0 - 0.5 - 0.5 = 7.0
  Compliance:      10.0 (no issues)

Weighted total:
  = (6.0 * 0.30) + (7.0 * 0.50) + (10.0 * 0.20)
  = 1.8 + 3.5 + 2.0
  = 7.3

Grade: C (7.0 ≤ score < 7.5)
Status: PASSED (7.3 ≥ 7.0) - barely
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
- Encourages quality improvement beyond minimum

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
Structure          6.0/10 ✗ (failed)
Content Quality    8.5/10 ✓ (passed)
Compliance        10.0/10 ✓ (passed)
```

---

## Score Impact Reference

Quick reference for common issues:

| Issue Type | Severity | Impact | Category |
|-----------|----------|--------|----------|
| Missing required field | ERROR | -2.0 | Structure |
| Invalid name format | ERROR | -2.0 | Structure |
| YAML malformed | ERROR | -2.0 | Structure |
| Missing description | ERROR | -2.0 | Structure |
| No system prompt | ERROR | -2.0 | Content Quality |
| Reserved word in name | ERROR | -2.0 | Compliance |
| UTF-8 encoding issue | ERROR | -2.0 | Compliance |
| Referenced skill missing | ERROR | -1.0 | Compliance |
| System prompt >200 lines | WARNING | -0.5 to -1.0 | Content Quality |
| No role definition | WARNING | -0.5 | Content Quality |
| No workflow | WARNING | -0.5 | Content Quality |
| Windows paths | WARNING | -0.1 each | Compliance |
| Content duplication | WARNING | -1.0 | Content Quality |
| Description quality poor | INFO | -2.0 | Content Quality |
| Description quality fair | INFO | -1.0 | Content Quality |
| Description quality average | INFO | -0.5 | Content Quality |
| Description quality good | INFO | 0.0 | Content Quality |
| Description quality excellent | INFO | +1.0 | Content Quality |
| Proactive marker present | INFO | +0.5 | Content Quality |
| Examples in prompt | INFO | +0.3 | Content Quality |
| Output format specified | INFO | +0.2 | Content Quality |

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
