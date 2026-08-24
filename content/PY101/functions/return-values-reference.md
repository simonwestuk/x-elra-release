---
title: "Quick Reference: Return Values"
slug: return-values-reference
description: "Quick syntax reference for return statements"
course_id: PY101
module: functions
module_order: 4
topic: return-values
topic_order: 3
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - functions
  - return-values
outcomes:
  - "Quickly look up return syntax"
  - "Review print vs return"
capstone_relevance: "Reference for return value patterns"
---

## Quick Reference: Return Values

### Basic Return

```python
def add(a, b):
    return a + b

result = add(5, 3)  # result = 8
```

### Print vs Return

| Feature | `print()` | `return` |
|---------|-----------|----------|
| Displays output | Yes | No |
| Gives back value | No | Yes |
| Can store result | No | Yes |
| Can use in expressions | No | Yes |

```python
# Print - can't reuse
def add_print(a, b):
    print(a + b)

# Return - can reuse
def add_return(a, b):
    return a + b
```

### Using Returned Values

```python
# Store in variable
x = func()

# Use directly
print(func())

# In expressions
total = func() + 10

# In conditions
if func() > 0:
    print("Positive")

# Pass to another function
other_func(func())
```

### Return Types

```python
# Number
def double(n):
    return n * 2

# String
def greet(name):
    return "Hi " + name

# Boolean
def is_valid(x):
    return x > 0

# List
def get_numbers():
    return [1, 2, 3]
```

### Multiple Returns

```python
def grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    return "C"  # Default
```

### Return Stops Execution

```python
def check(n):
    if n < 0:
        return "Negative"  # Stops here
    return "Non-negative"  # Only if n >= 0
```

### No Return = None

```python
def no_return():
    x = 5  # No return statement

result = no_return()
print(result)  # None
```

### Common Patterns

```python
# Calculation
def area(w, h):
    return w * h

# Transformation
def uppercase(text):
    return text.upper()

# Validation
def is_even(n):
    return n % 2 == 0

# Lookup
def get_status(code):
    if code == 200:
        return "OK"
    return "Error"
```

### Chaining Functions

```python
def double(n):
    return n * 2

def add_one(n):
    return n + 1

# Chain: double(5)=10, add_one(10)=11
result = add_one(double(5))
```

### See Also

- [Parameters](parameters-lesson.html) - Inputs to functions
- [Default Parameters](defaults-lesson.html) - Optional inputs

