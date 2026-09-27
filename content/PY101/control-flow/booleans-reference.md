---
title: "Quick Reference: Booleans"
slug: booleans-reference
description: "Quick syntax reference for boolean values"
course_id: PY101
module: control-flow
module_order: 2
topic: booleans
topic_order: 2
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - booleans
outcomes:
  - "Quickly look up boolean syntax"
  - "Review truthy and falsy values"
capstone_relevance: "Reference for state management in your application"
---

## Quick Reference: Booleans

### Boolean Values

```python
True   # Positive/yes/on
False  # Negative/no/off
```

### Falsy Values (evaluate to False)

| Value | Type |
|-------|------|
| `False` | bool |
| `None` | NoneType |
| `0` | int |
| `0.0` | float |
| `""` | str (empty) |
| `[]` | list (empty) |
| `{}` | dict (empty) |

### Truthy Values (evaluate to True)

Everything else:
- Non-zero numbers
- Non-empty strings
- Non-empty collections
- Objects

### Converting to Boolean

```python
bool(0)        # False
bool(42)       # True
bool("")       # False
bool("hello")  # True
```

### Common Patterns

```python
# Boolean flags
is_active = True
is_deleted = False

# Toggle
switch = not switch

# Check if value exists
has_value = bool(value)

# Conditional display
status = "Online" if is_active else "Offline"
```

### Boolean Operations

| Operation | Result |
|-----------|--------|
| `not True` | `False` |
| `not False` | `True` |
| `True and True` | `True` |
| `True and False` | `False` |
| `True or False` | `True` |

### Common Errors

- **NameError: name 'true' is not defined** - Use `True` not `true`
- **NameError: name 'false' is not defined** - Use `False` not `false`

### See Also

- [Comparisons](comparisons-lesson.html) - Creating booleans
- [Logical Operators](logical-operators-lesson.html) - Combining booleans
- [If Statements](if-statements-lesson.html) - Using booleans
