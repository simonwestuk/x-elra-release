---
title: "Quick Reference: Input Validation"
slug: input-validation-reference
description: "Quick reference for input validation patterns"
course_id: PY101
module: building-apps
module_order: 7
topic: input-validation
topic_order: 3
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - validation
  - error-handling
outcomes:
  - "Quick lookup for validation patterns"
  - "Review common validation rules"
capstone_relevance: "Validation reference for your project"
---

## Quick Reference: Input Validation

### Basic Validation Pattern

```python
def validate_field(value, field_name):
    if not valid_condition:
        return False, f"{field_name} error message"
    return True, None
```

### Type Validation

```python
# Check type
isinstance(value, str)
isinstance(value, int)
isinstance(value, (int, float))
isinstance(value, list)
isinstance(value, dict)
```

### String Validation

```python
# Length
len(value) >= min_len
len(value) <= max_len

# Content
value.strip()           # Remove whitespace
value.isalpha()         # Only letters
value.isdigit()         # Only digits
value.isalnum()         # Letters and digits

# Pattern
"@" in value           # Contains character
value.startswith("...")
value.endswith("...")
```

### Number Validation

```python
# Range
value > 0              # Positive
min_val <= value <= max_val

# Type conversion
try:
    num = int(value)
except ValueError:
    # Not a valid number
```

### Common Validators

```python
# Required field
def validate_required(value, name):
    if value is None or value == "":
        return False, f"{name} is required"
    return True, None

# Length range
def validate_length(value, min_len, max_len, name):
    if len(value) < min_len:
        return False, f"{name} too short"
    if len(value) > max_len:
        return False, f"{name} too long"
    return True, None

# Numeric range
def validate_range(value, min_val, max_val, name):
    if value < min_val or value > max_val:
        return False, f"{name} must be {min_val}-{max_val}"
    return True, None

# Email (basic)
def validate_email(email):
    if "@" not in email or "." not in email:
        return False, "Invalid email"
    return True, None
```

### Validation Rules Table

| Type | Rule | Check |
|------|------|-------|
| Required | Not empty | `value is not None and value != ""` |
| Min length | At least N | `len(value) >= n` |
| Max length | At most N | `len(value) <= n` |
| Min value | At least N | `value >= n` |
| Max value | At most N | `value <= n` |
| In list | One of options | `value in options` |
| Pattern | Contains/matches | `pattern in value` |

### Sanitization

```python
# String cleanup
value = value.strip()           # Remove whitespace
value = value.lower()           # Lowercase
value = " ".join(value.split()) # Single spaces

# Number conversion
try:
    value = int(value)
except ValueError:
    value = None
```

### Error Collection Pattern

```python
def validate_form(data):
    errors = []

    if not data.get("name"):
        errors.append("Name is required")

    if not data.get("email"):
        errors.append("Email is required")

    return len(errors) == 0, errors
```

### Nested Validation

```python
def validate_object(obj):
    errors = {
        "field1": validate_field1(obj.get("field1")),
        "field2": validate_field2(obj.get("field2"))
    }
    return errors
```

### Best Practices

| Do | Don't |
|----|-------|
| Validate early | Validate late |
| Return helpful messages | Return generic errors |
| Check types first | Assume correct type |
| Sanitize before validating | Validate raw input |
| Handle missing fields | Assume fields exist |

### See Also

- [Error Handling](try-except-lesson.html) - Exception handling
- [Raising Errors](raising-errors-lesson.html) - Custom exceptions

