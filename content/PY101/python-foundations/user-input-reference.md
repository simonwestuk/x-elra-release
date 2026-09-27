---
title: "Quick Reference: User Input"
slug: user-input-reference
description: "Quick syntax reference for input() and type conversion"
course_id: PY101
module: python-foundations
module_order: 1
topic: user-input
topic_order: 8
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - input
  - type-conversion
outcomes:
  - "Quickly look up input syntax"
  - "Review type conversion functions"
capstone_relevance: "Reference for capturing user data in your application"
---

## Quick Reference: User Input

### Basic Input

```python
variable = input("prompt message: ")
```

### Type Conversion

| Function | Use | Example |
|----------|-----|---------|
| `int()` | Whole numbers | `int(input("Age: "))` |
| `float()` | Decimals | `float(input("Price: "))` |
| `str()` | Text | `str(42)` → `"42"` |

### Common Patterns

```python
# String input
name = input("Enter name: ")

# Integer input
age = int(input("Enter age: "))

# Float input
price = float(input("Enter price: "))

# Cleaned input
answer = input("Yes/No: ").strip().lower()

# One-line with calculation
years = int(input("Age: "))
print(f"In 10 years: {years + 10}")
```

### Input + Validation Pattern

```python
# Basic yes/no check
answer = input("Continue? ").strip().lower()
if answer == "yes":
    print("Continuing...")
```

### Multi-Input Collection

```python
# Collect multiple values
name = input("Name: ")
age = int(input("Age: "))
email = input("Email: ")

# Display collected data
print(f"Name: {name}, Age: {age}, Email: {email}")
```

### Cleaning Input

| Method | Purpose |
|--------|---------|
| `.strip()` | Remove leading/trailing spaces |
| `.lower()` | Convert to lowercase |
| `.upper()` | Convert to uppercase |

```python
# Full cleanup
response = input("Enter: ").strip().lower()
```

### Common Errors

- **ValueError: invalid literal for int()** - User entered non-numeric text when you expected a number. Handle with try/except (Error Handling module).

- **TypeError: can't add str and int** - Forgot to convert input before doing math.

### See Also

- [Variables & Types](variables-types-lesson.html) - Data types
- [Error Handling](try-except-lesson.html) - Handle invalid input
- [Validation](validation-lesson.html) - Input validation patterns
