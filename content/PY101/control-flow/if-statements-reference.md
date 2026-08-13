---
title: "Quick Reference: If Statements"
slug: if-statements-reference
description: "Quick syntax reference for if statements"
course_id: PY101
module: control-flow
module_order: 2
topic: if-statements
topic_order: 3
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - if-else
outcomes:
  - "Quickly look up if statement syntax"
  - "Review conditional patterns"
capstone_relevance: "Reference for conditional logic in your application"
---

## Quick Reference: If Statements

### Basic Syntax

```python
if condition:
    # code runs if True
```

### Examples

```python
# Simple comparison
if age >= 18:
    print("Adult")

# Boolean variable
if is_active:
    print("Active")

# Truthiness check
if name:  # non-empty
    print(f"Hello, {name}")
```

### Multiple Statements

```python
if score >= 70:
    print("Passed!")
    print("Congratulations!")
    passed_count += 1
```

### Nested If

```python
if has_account:
    if is_verified:
        print("Welcome!")
```

### Empty Block (Placeholder)

```python
if condition:
    pass  # TODO: implement
```

### Common Patterns

```python
# Value check
if value > 0:
    print("Positive")

# String check
if name == "admin":
    print("Hello, admin!")

# Empty check
if not items:  # empty list
    print("No items")

# Membership check
if item in allowed_list:
    process(item)
```

### Common Errors

- **SyntaxError: expected ':'** - Missing colon after condition
- **IndentationError** - Code not indented under if
- **Wrong comparison** - Using `=` instead of `==`

### Structure

```
if condition:     # Line ends with colon
    statement1    # Indented (4 spaces)
    statement2    # Same indentation
statement3        # Not indented = outside if
```

### See Also

- [Else & Elif](else-elif-lesson.html) - Alternative branches
- [Logical Operators](logical-operators-lesson.html) - Combine conditions
- [Nested Conditions](nested-conditions-lesson.html) - Complex logic
