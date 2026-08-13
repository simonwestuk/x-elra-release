---
title: "Understanding Syntax Errors"
slug: syntax-errors-lesson
description: "Learn to identify and fix Python syntax errors"
course_id: PY101
module: error-handling
module_order: 5
topic: syntax-errors
topic_order: 1
type: lesson
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - print-basics-lesson
  - variables-types-lesson
skills:
  - debugging
  - errors
outcomes:
  - "Understand what syntax errors are"
  - "Read and interpret error messages"
  - "Fix common syntax mistakes"
capstone_relevance: "Debugging skills are essential for any project"
---

## Introduction

A **syntax error** occurs when Python can't understand your code because it doesn't follow the rules of the language. Think of it like a grammatical error—Python knows something is wrong but can't figure out what you meant.

## What Causes Syntax Errors?

Syntax errors happen before your code runs. Python reads your code and checks if it's valid. If it finds a problem, it stops and shows an error.

Common causes:
- Missing colons (`:`)
- Unmatched parentheses, brackets, or quotes
- Incorrect indentation
- Typos in keywords

## Reading Error Messages

When Python encounters a syntax error, it tells you:
1. **What file** has the error
2. **Which line** the error is on
3. **What went wrong** (error type and description)

```
  File "example.py", line 3
    print("Hello"
                 ^
SyntaxError: unexpected EOF while parsing
```

The `^` arrow points to where Python noticed the problem.

## Common Syntax Errors

### Missing Colon

```python
# Wrong
if x > 5
    print("Big")

# Correct
if x > 5:
    print("Big")
```

### Missing Parenthesis

```python
# Wrong
print("Hello"

# Correct
print("Hello")
```

### Mismatched Quotes

```python
# Wrong
message = "Hello'

# Correct
message = "Hello"
# Or
message = 'Hello'
```

### Indentation Errors

```python
# Wrong
def greet():
print("Hello")  # Not indented!

# Correct
def greet():
    print("Hello")
```

### Invalid Variable Names

```python
# Wrong
2name = "Alice"  # Can't start with number
my-var = 5      # Can't use hyphens

# Correct
name2 = "Alice"
my_var = 5
```

## Finding the Error

The error might not be exactly where Python points:

```python live
# This code has an error - can you find it?
name = "Alice"
age = 25
print("Name: " + name)
print("Age: " + str(age)
print("Done")  # Error appears here, but problem is above!
```

Python often reports the error on the line *after* the actual problem.

## Fixing Strategy

1. **Read the error message** - Note the line number
2. **Check that line** - Look for obvious mistakes
3. **Check the line before** - The error might be there
4. **Look for common issues** - Missing `:`, `)`, `"`, or indentation

## Practice Reading Errors

```python live
# Run this to see the error
# Then fix it!

def greet(name)
    print("Hello, " + name)

greet("Alice")
```

## Key Points

- Syntax errors happen when code doesn't follow Python's rules
- Error messages tell you the file, line, and problem
- The actual error might be on the line before
- Common issues: missing colons, parentheses, quotes, indentation
- Read error messages carefully—they help you fix problems!

:::hint Debugging Tip
When you get a syntax error, start at the line mentioned, then work backwards. Check parentheses, brackets, quotes, and colons carefully.
:::

