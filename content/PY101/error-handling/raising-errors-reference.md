---
title: "Quick Reference: Raising Exceptions"
slug: raising-errors-reference
description: "Quick reference for raising your own exceptions"
course_id: PY101
module: error-handling
module_order: 5
topic: raising-errors
topic_order: 4
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - errors
  - exceptions
outcomes:
  - "Quickly look up raise syntax"
  - "Choose correct exception types"
capstone_relevance: "Reference for input validation"
---

## Quick Reference: Raising Exceptions

### Basic Syntax

```python
raise ExceptionType("Error message")
```

### Common Exception Types

| Exception | Use For |
|-----------|---------|
| `ValueError` | Invalid value (wrong range, format) |
| `TypeError` | Wrong type passed |
| `KeyError` | Missing dictionary key |
| `IndexError` | Invalid list index |
| `RuntimeError` | General runtime problem |
| `NotImplementedError` | Unfinished feature |

### Raise Examples

```python
# Value out of range
if age < 0:
    raise ValueError("Age cannot be negative")

# Wrong type
if not isinstance(name, str):
    raise TypeError("Name must be a string")

# Missing required value
if not email:
    raise ValueError("Email is required")

# Out of bounds
if index >= len(items):
    raise IndexError("Index out of range")
```

### Guard Clause Pattern

```python
def process(value):
    # Validate first
    if value is None:
        raise ValueError("Value cannot be None")
    if value < 0:
        raise ValueError("Value must be positive")

    # Main logic (only with valid input)
    return value * 2
```

### Re-raising Exceptions

```python
try:
    risky_operation()
except ValueError:
    log_error()
    raise  # Re-raise same exception
```

### Raise with Context

```python
# Include helpful details
raise ValueError(
    f"Invalid score {score}. Must be 0-100."
)

# Without f-strings
raise ValueError(
    "Invalid score " + str(score) + ". Must be 0-100."
)
```

### Validation Pattern

```python
def validate_user(name, age, email):
    if not name:
        raise ValueError("Name is required")
    if not isinstance(age, int):
        raise TypeError("Age must be integer")
    if age < 0 or age > 150:
        raise ValueError("Age must be 0-150")
    if "@" not in email:
        raise ValueError("Invalid email format")
    return True
```

### Best Practices

| Do | Don't |
|----|----- |
| Use specific exception types | Use generic `Exception` |
| Write clear messages | Use vague messages |
| Validate early | Validate late |
| Include context | Omit helpful details |

### Message Guidelines

```python
# Good messages
raise ValueError("Age must be positive, got: -5")
raise TypeError("Expected string, got int")
raise ValueError("Email must contain @")

# Bad messages
raise ValueError("Invalid")
raise TypeError("Wrong type")
raise ValueError("Error")
```

### See Also

- [Exceptions](exceptions-lesson.html) - Exception types
- [Try-Except](try-except-lesson.html) - Catching exceptions
- [Debugging](debugging-lesson.html) - Finding problems

