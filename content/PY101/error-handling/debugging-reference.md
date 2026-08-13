---
title: "Quick Reference: Debugging"
slug: debugging-reference
description: "Quick reference for debugging techniques"
course_id: PY101
module: error-handling
module_order: 5
topic: debugging
topic_order: 5
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - debugging
outcomes:
  - "Quickly apply debugging techniques"
  - "Reference common bug patterns"
capstone_relevance: "Debugging reference while developing"
---

## Quick Reference: Debugging

### Print Debugging

```python
# See variable values
print("DEBUG - variable:", variable)

# Check types
print("DEBUG - type:", type(variable))

# Track function calls
print("DEBUG - entering function_name")
print("DEBUG - params:", param1, param2)
print("DEBUG - returning:", result)

# Mark code sections
print("=== Starting section ===")
print("=== Section complete ===")
```

### Reading Error Messages

```
Traceback (most recent call last):
  File "script.py", line 10, in <module>
    result = process(data)
  File "script.py", line 5, in process
    return data["key"]
KeyError: 'key'
```

| Part | Read |
|------|------|
| Line 10 | Where you called the function |
| Line 5 | Where error occurred |
| KeyError | Type of error |
| 'key' | What caused it |

### Common Bug Patterns

| Bug | Symptom | Fix |
|-----|---------|-----|
| Off-by-one | Missing first/last item | Check loop bounds |
| Wrong operator | `=` vs `==`, `+` vs `+=` | Review operators |
| Wrong indent | Code runs at wrong time | Check indentation |
| Wrong variable | Uses wrong value | Check variable names |
| Uninitialized | NameError or wrong value | Initialize variables |
| Type mismatch | TypeError | Check and convert types |

### Debugging Checklist

```
□ Read error message completely
□ Note the line number
□ Check that line and line before
□ Add print statements
□ Check input values
□ Check variable types
□ Trace through code manually
□ Simplify the problem
□ Take a break if stuck
```

### Quick Debug Snippets

```python
# Print all local variables
print("DEBUG - locals:", locals())

# Print object attributes
print("DEBUG - attrs:", dir(object))

# Check truthiness
print("DEBUG - bool:", bool(variable))

# Detailed type info
print("DEBUG - repr:", repr(variable))
```

### Binary Search Debugging

```python
# When bug is somewhere in many lines:
# 1. Add print halfway through
print("DEBUG - reached midpoint")
# 2. If prints: bug is AFTER
# 3. If doesn't: bug is BEFORE
# 4. Repeat with smaller section
```

### Common Error Types

| Error | Likely Cause |
|-------|--------------|
| NameError | Typo or undefined variable |
| TypeError | Wrong type for operation |
| ValueError | Right type, wrong value |
| IndexError | List index out of range |
| KeyError | Dict key doesn't exist |
| AttributeError | Method/property doesn't exist |

### Prevention Tips

```python
# Validate inputs early
if not data:
    print("Warning: data is empty")
    return None

# Use meaningful variable names
# Bad: x, temp, data
# Good: user_count, temp_celsius, user_data

# Add comments for tricky parts
# Calculate discount (10% off if > $100)
discount = total * 0.1 if total > 100 else 0
```

### See Also

- [Syntax Errors](syntax-errors-lesson.html) - Parse-time errors
- [Exceptions](exceptions-lesson.html) - Runtime errors
- [Try-Except](try-except-lesson.html) - Handling errors

