---
title: "Quick Reference: Comparisons"
slug: comparisons-reference
description: "Quick syntax reference for comparison operators"
course_id: PY101
module: control-flow
module_order: 2
topic: comparisons
topic_order: 1
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - comparisons
outcomes:
  - "Quickly look up comparison operators"
  - "Review comparison patterns"
capstone_relevance: "Reference for data validation and filtering"
---

## Quick Reference: Comparisons

### Comparison Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | Equal | `5 == 5` | `True` |
| `!=` | Not equal | `5 != 3` | `True` |
| `<` | Less than | `3 < 5` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<=` | Less or equal | `5 <= 5` | `True` |
| `>=` | Greater or equal | `5 >= 3` | `True` |

### Examples

```python
# Number comparisons
age >= 18           # Adult check
price <= budget     # Within budget
score > 90          # High score

# String comparisons
name == "admin"     # Exact match
status != "deleted" # Not deleted

# Case-insensitive
name.lower() == "alice"

# Range check (chained)
18 <= age <= 65     # Between 18 and 65
```

### Common Patterns

```python
# Store result
is_valid = value > 0
is_match = password == confirm

# Multiple conditions (with if)
if age >= 18:
    print("Adult")

# Range validation
in_range = min_val <= x <= max_val
```

### String vs Number

| Comparison | Result | Note |
|------------|--------|------|
| `5 == 5.0` | `True` | int/float OK |
| `"5" == 5` | `False` | str/int always False |
| `"abc" < "abd"` | `True` | Alphabetical |

### Common Errors

- **Using `=` instead of `==`** - `=` assigns, `==` compares
- **Case mismatch** - `"A" != "a"`, convert to same case first

### See Also

- [Booleans](booleans-lesson.html) - True/False values
- [If Statements](if-statements-lesson.html) - Using comparisons
- [Logical Operators](logical-operators-lesson.html) - Combining comparisons
