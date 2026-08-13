---
title: "Quick Reference: print()"
slug: print-basics-reference
description: "Quick syntax reference for the print() function"
course_id: PY101
module: python-foundations
module_order: 1
topic: print-basics
topic_order: 1
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - foundations
  - print
outcomes:
  - "Quickly look up print() syntax"
  - "Review print() options and patterns"
capstone_relevance: "Reference for displaying output throughout your application"
---

## Quick Reference: print()

### Basic Syntax

```python
print("Your text here")
```

### Common Operations

| Operation | Code | Result |
|-----------|------|--------|
| Display text | `print("Hello")` | Hello |
| Blank line | `print()` | (empty line) |
| Single quotes | `print('Hi')` | Hi |
| Double quotes | `print("Hi")` | Hi |

### Examples

```python
# Basic output
print("Welcome!")

# Multiple lines
print("Line 1")
print("Line 2")

# Blank line between text
print("Before")
print()
print("After")
```

```python
# Creating borders
print("============")
print("  MY TITLE  ")
print("============")
```

### Common Errors

- **SyntaxError: EOL while scanning string literal** - Missing closing quote. Check that every opening quote has a matching closing quote.

- **NameError: name 'Hello' is not defined** - Forgot quotes around text. Use `print("Hello")` not `print(Hello)`.

- **SyntaxError: invalid syntax** - Missing parentheses. Use `print("Hi")` not `print "Hi"`.

### See Also

- [Variables & Types](variables-types-lesson.html) - Store text in variables
- [String Formatting](string-formatting-lesson.html) - Dynamic text output
