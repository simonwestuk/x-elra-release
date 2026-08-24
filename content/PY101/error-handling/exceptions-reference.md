---
title: "Quick Reference: Exceptions"
slug: exceptions-reference
description: "Quick reference for common Python exceptions"
course_id: PY101
module: error-handling
module_order: 5
topic: exceptions
topic_order: 2
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - debugging
  - errors
  - exceptions
outcomes:
  - "Quickly identify exception types"
  - "Understand common causes"
capstone_relevance: "Exception reference for debugging"
---

## Quick Reference: Exceptions

### Common Exception Types

| Exception | Cause | Example |
|-----------|-------|---------|
| `NameError` | Unknown variable | `print(undefined)` |
| `TypeError` | Wrong type | `"a" + 5` |
| `ValueError` | Invalid value | `int("abc")` |
| `ZeroDivisionError` | Divide by zero | `10 / 0` |
| `IndexError` | Invalid index | `[1,2,3][10]` |
| `KeyError` | Missing dict key | `{}["key"]` |
| `AttributeError` | Missing attribute | `5.upper()` |
| `FileNotFoundError` | File doesn't exist | `open("missing.txt")` |

### Reading Tracebacks

```
Traceback (most recent call last):
  File "script.py", line 5, in <module>
    result = calculate(10, 0)
  File "script.py", line 2, in calculate
    return a / b
ZeroDivisionError: division by zero
```

| Line | Meaning |
|------|---------|
| 1 | Error occurred (read bottom-up) |
| 2-3 | Where it was called from |
| 4-5 | Where error actually happened |
| 6 | Exception type and message |

### Exception Hierarchy

```
BaseException
└── Exception
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── IndexError
    ├── ZeroDivisionError
    ├── NameError
    ├── AttributeError
    └── FileNotFoundError
```

### Quick Fixes

| Exception | Common Fix |
|-----------|------------|
| `NameError` | Check spelling, define variable |
| `TypeError` | Convert types, check inputs |
| `ValueError` | Validate input before using |
| `ZeroDivisionError` | Check if divisor is zero |
| `IndexError` | Check list length first |
| `KeyError` | Use `.get()` or check with `in` |

### Prevention Patterns

```python
# KeyError - use .get()
value = d.get("key", default)

# IndexError - check length
if i < len(items):
    item = items[i]

# ZeroDivisionError - check divisor
if divisor != 0:
    result = num / divisor

# ValueError - validate input
if text.isdigit():
    num = int(text)

# TypeError - check type
if isinstance(x, str):
    x = int(x)
```

### Syntax Error vs Exception

| Syntax Error | Exception |
|--------------|-----------|
| Before running | While running |
| Invalid Python | Valid but fails |
| Missing `:`, `)` | Bad value, type |
| Can't be caught | Can be caught |

### See Also

- [Syntax Errors](syntax-errors-lesson.html) - Parse-time errors
- [Try-Except](try-except-lesson.html) - Handling exceptions
- [Raising Errors](raising-errors-lesson.html) - Creating exceptions

