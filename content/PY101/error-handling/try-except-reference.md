---
title: "Quick Reference: Try-Except"
slug: try-except-reference
description: "Quick reference for exception handling syntax"
course_id: PY101
module: error-handling
module_order: 5
topic: try-except
topic_order: 3
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - errors
  - exceptions
  - try-except
outcomes:
  - "Quickly look up try-except syntax"
  - "Review exception handling patterns"
capstone_relevance: "Exception handling quick reference"
---

## Quick Reference: Try-Except

### Basic Syntax

```python
try:
    # Code that might fail
    risky_operation()
except ExceptionType:
    # Handle the error
    handle_error()
```

### Catch Specific Exception

```python
try:
    number = int("hello")
except ValueError:
    print("Invalid number")
```

### Catch Multiple Exceptions

```python
# Separate handlers
try:
    x = data[key] / value
except KeyError:
    print("Key not found")
except ZeroDivisionError:
    print("Cannot divide by zero")

# Combined handler
try:
    x = data[key] / value
except (KeyError, ZeroDivisionError):
    print("Operation failed")
```

### Get Exception Details

```python
try:
    number = int("hello")
except ValueError as e:
    print("Error:", e)
```

### Complete Structure

```python
try:
    # Code that might fail
    result = operation()
except ExceptionType:
    # Handle error
    result = default
else:
    # Runs if NO exception
    print("Success!")
finally:
    # ALWAYS runs
    cleanup()
```

### When Each Block Runs

| Block | Runs When |
|-------|-----------|
| `try` | Always (first) |
| `except` | Exception raised |
| `else` | No exception |
| `finally` | Always (last) |

### Common Patterns

```python
# Safe conversion
def safe_int(text, default=0):
    try:
        return int(text)
    except ValueError:
        return default

# Safe dictionary access
def safe_get(d, key, default=None):
    try:
        return d[key]
    except KeyError:
        return default

# Safe list access
def safe_index(lst, i, default=None):
    try:
        return lst[i]
    except IndexError:
        return default

# Safe division
def safe_divide(a, b, default=0):
    try:
        return a / b
    except ZeroDivisionError:
        return default
```

### What to Catch

| Catch | When |
|-------|------|
| Specific exception | You know what might fail |
| Multiple exceptions | Similar handling needed |
| `Exception` | Catch most errors (use sparingly) |
| Bare `except:` | Avoid (catches everything) |

### Bad Practices

```python
# Too broad - catches everything
try:
    code()
except:  # Avoid!
    pass

# Silently ignoring errors
try:
    code()
except Exception:
    pass  # Lost error info!
```

### Good Practices

```python
# Specific and informative
try:
    number = int(user_input)
except ValueError as e:
    print("Invalid input:", e)
    number = 0

# Log or handle appropriately
try:
    result = operation()
except SpecificError as e:
    log_error(e)
    result = fallback_value
```

### See Also

- [Exceptions](exceptions-lesson.html) - Exception types
- [Raising Errors](raising-errors-lesson.html) - Creating exceptions
- [Debugging](debugging-lesson.html) - Finding problems

