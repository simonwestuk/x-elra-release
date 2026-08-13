---
title: "Quick Reference: Else and Elif"
slug: else-elif-reference
description: "Quick syntax reference for else and elif statements"
course_id: PY101
module: control-flow
module_order: 2
topic: else-elif
topic_order: 4
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - elif
outcomes:
  - "Quickly look up else/elif syntax"
  - "Review decision structure patterns"
capstone_relevance: "Reference for conditional logic in your application"
---

## Quick Reference: Else and Elif

### If-Else Syntax

```python
if condition:
    # runs if True
else:
    # runs if False
```

### If-Elif-Else Syntax

```python
if condition1:
    # first option
elif condition2:
    # second option
elif condition3:
    # third option
else:
    # default/catch-all
```

### Examples

```python
# Simple if-else
if age >= 18:
    print("Adult")
else:
    print("Minor")

# Multiple conditions
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

### Common Patterns

```python
# Menu handling
if choice == "1":
    action1()
elif choice == "2":
    action2()
else:
    print("Invalid")

# Range checking
if value > 100:
    print("High")
elif value > 50:
    print("Medium")
else:
    print("Low")
```

### Key Rules

| Rule | Example |
|------|---------|
| Colons required | `else:` not `else` |
| Only one branch runs | First True wins |
| Order matters | Specific before general |
| else is optional | Can omit if not needed |

### Common Errors

- **SyntaxError: invalid syntax** - Missing colon after else/elif
- **Wrong order** - Checking >= 70 before >= 90 gives wrong result

### See Also

- [If Statements](if-statements-lesson.html) - Basic conditionals
- [Logical Operators](logical-operators-lesson.html) - Complex conditions
- [Nested Conditions](nested-conditions-lesson.html) - If inside if
