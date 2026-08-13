---
title: "Quick Reference: Nested Conditions"
slug: nested-conditions-reference
description: "Quick syntax reference for nested if statements"
course_id: PY101
module: control-flow
module_order: 2
topic: nested-conditions
topic_order: 6
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - nested-conditions
outcomes:
  - "Quickly look up nesting patterns"
  - "Review indentation rules"
capstone_relevance: "Reference for hierarchical logic in your application"
---

## Quick Reference: Nested Conditions

### Basic Syntax

```python
if outer_condition:
    # Level 1
    if inner_condition:
        # Level 2
        if deeper_condition:
            # Level 3
```

### Nested If-Else

```python
if condition1:
    if condition2:
        # Both true
    else:
        # 1 true, 2 false
else:
    # 1 false
```

### Common Patterns

```python
# Sequential validation
if user_exists:
    if password_correct:
        if account_active:
            login()

# Early exit pattern
if not valid:
    print("Error")
else:
    if condition:
        action()
```

### Indentation Levels

```
if:           # Level 0 (no indent)
    code      # Level 1 (4 spaces)
    if:       # Level 1
        code  # Level 2 (8 spaces)
        if:   # Level 2
            code  # Level 3 (12 spaces)
```

### When to Nest vs Combine

| Use Nesting When | Use `and` When |
|------------------|----------------|
| Different messages per level | Single combined message |
| Actions depend on level | Same action for all |
| Complex else handling | Simple pass/fail |

### Examples Comparison

```python
# Nested (verbose feedback)
if a:
    print("A passed")
    if b:
        print("B passed too")

# Combined (simple check)
if a and b:
    print("Both passed")
```

### Common Errors

- **IndentationError** - Inconsistent spacing
- **Too deep** - Keep to 2-3 levels max

### See Also

- [If Statements](if-statements-lesson.html) - Basic conditionals
- [Logical Operators](logical-operators-lesson.html) - Combining conditions
