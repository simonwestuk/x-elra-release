---
title: "Quick Reference: Syntax Errors"
slug: syntax-errors-reference
description: "Quick reference for common syntax errors and fixes"
course_id: PY101
module: error-handling
module_order: 5
topic: syntax-errors
topic_order: 1
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - debugging
  - errors
outcomes:
  - "Quickly identify syntax error types"
  - "Apply common fixes"
capstone_relevance: "Quick debugging reference"
---

## Quick Reference: Syntax Errors

### Reading Error Messages

```
  File "script.py", line 5
    if x > 5
           ^
SyntaxError: invalid syntax
```

| Part | Meaning |
|------|---------|
| File "script.py" | Which file |
| line 5 | Which line |
| `^` | Where error detected |
| SyntaxError | Error type |
| invalid syntax | Description |

### Common Errors and Fixes

#### Missing Colon

```python
# Wrong
if x > 5
for i in range(10)
def greet()
while True

# Correct
if x > 5:
for i in range(10):
def greet():
while True:
```

#### Missing Parenthesis

```python
# Wrong
print("Hello"
result = add(5, 3

# Correct
print("Hello")
result = add(5, 3)
```

#### Mismatched Quotes

```python
# Wrong
message = "Hello'
name = 'World"

# Correct
message = "Hello"
name = 'World'
```

#### Indentation Errors

```python
# Wrong
def greet():
print("Hi")  # Not indented

# Correct
def greet():
    print("Hi")
```

#### Invalid Variable Names

```python
# Wrong
2var = 5       # Starts with number
my-var = 10    # Contains hyphen
class = "A"    # Reserved keyword

# Correct
var2 = 5
my_var = 10
grade = "A"
```

### Error Types

| Error | Common Cause |
|-------|--------------|
| `SyntaxError: invalid syntax` | Missing `:`, `)`, or typo |
| `SyntaxError: EOL while scanning` | Unclosed string |
| `SyntaxError: unexpected EOF` | Missing `)` or `]` |
| `IndentationError: expected an indented block` | Missing indent |
| `IndentationError: unexpected indent` | Extra indent |

### Debugging Strategy

1. Read the error message
2. Note the line number
3. Check that line for obvious issues
4. Check the line BEFORE (errors often reported on next line)
5. Look for missing `:`, `)`, `"`, or indentation

### Quick Checklist

| Check | Look For |
|-------|----------|
| Colons | After `if`, `for`, `while`, `def`, `class` |
| Parentheses | Opening `(` matches closing `)` |
| Brackets | Opening `[` matches closing `]` |
| Quotes | Opening quote matches closing quote |
| Indentation | Consistent (4 spaces or 1 tab) |

### See Also

- [Exceptions](exceptions-lesson.html) - Runtime errors
- [Try-Except](try-except-lesson.html) - Handling errors
- [Debugging](debugging-lesson.html) - Finding bugs

