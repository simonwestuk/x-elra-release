---
title: "Quick Reference: Logical Operators"
slug: logical-operators-reference
description: "Quick syntax reference for and, or, not"
course_id: PY101
module: control-flow
module_order: 2
topic: logical-operators
topic_order: 5
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - logic
outcomes:
  - "Quickly look up logical operator syntax"
  - "Review truth tables"
capstone_relevance: "Reference for complex conditions in your application"
---

## Quick Reference: Logical Operators

### Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `and` | Both True | `a and b` |
| `or` | Either True | `a or b` |
| `not` | Negate | `not a` |

### Truth Tables

**and** - Both must be True:
| A | B | A and B |
|---|---|---------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

**or** - At least one True:
| A | B | A or B |
|---|---|--------|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

**not** - Flip the value:
| A | not A |
|---|-------|
| T | F |
| F | T |

### Common Patterns

```python
# Both required
if username and password:
    login()

# Either qualifies
if is_admin or is_owner:
    allow()

# Exclusion
if not is_banned:
    proceed()

# Range check
if min_val <= x <= max_val:
    valid()

# Complex rule
if (a and b) or c:
    action()
```

### Operator Precedence

1. `not` (highest)
2. `and`
3. `or` (lowest)

```python
# These are equivalent:
a or b and c
a or (b and c)

# Use parentheses for clarity:
(a or b) and c
```

### Short-Circuit Evaluation

```python
# and: stops at first False
False and expensive_call()  # call skipped

# or: stops at first True
True or expensive_call()    # call skipped
```

### Common Errors

- Using `&&` or `||` (not Python syntax)
- Using `&` or `|` (bitwise, not logical)

### See Also

- [Comparisons](comparisons-lesson.html) - Creating conditions
- [If Statements](if-statements-lesson.html) - Using conditions
