---
title: "Quick Reference: Variables and Types"
slug: variables-types-reference
description: "Quick syntax reference for variables and data types"
course_id: PY101
module: python-foundations
module_order: 1
topic: variables-types
topic_order: 3
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - variables
  - types
outcomes:
  - "Quickly look up variable syntax"
  - "Review data type examples"
capstone_relevance: "Reference for storing different types of data"
---

## Quick Reference: Variables and Types

### Creating Variables

```python
variable_name = value
```

### Data Types

| Type | Description | Examples |
|------|-------------|----------|
| `str` | Text | `"Hello"`, `'World'` |
| `int` | Whole numbers | `42`, `-7`, `0` |
| `float` | Decimals | `3.14`, `-0.5`, `2.0` |
| `bool` | True/False | `True`, `False` |

### Examples

```python
# Strings
name = "Alice"
message = 'Hello'

# Integers
age = 25
count = -3

# Floats
price = 19.99
temperature = -4.5

# Booleans
is_active = True
has_error = False
```

### Type Checking

```python
x = "hello"
print(type(x))  # <class 'str'>

y = 42
print(type(y))  # <class 'int'>
```

### Variable Naming Rules

| Valid | Invalid | Why |
|-------|---------|-----|
| `user_name` | `user-name` | No hyphens |
| `_private` | `2nd_place` | Can't start with number |
| `totalCount` | `class` | Reserved keyword |
| `item1` | `my var` | No spaces |

### Common Errors

- **NameError: name 'x' is not defined** - Using a variable before creating it
- **SyntaxError** - Invalid variable name (starts with number, contains spaces)

### See Also

- [Numbers & Math](numbers-math-lesson.html) - Working with numeric types
- [Strings](strings-lesson.html) - Working with text
