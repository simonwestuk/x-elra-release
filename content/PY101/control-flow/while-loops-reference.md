---
title: "Quick Reference: While Loops"
slug: while-loops-reference
description: "Quick syntax reference for while loops"
course_id: PY101
module: control-flow
module_order: 2
topic: while-loops
topic_order: 7
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - while-loops
outcomes:
  - "Quickly look up while loop syntax"
  - "Review common patterns"
capstone_relevance: "Reference for repeating menus in your application"
---

## Quick Reference: While Loops

### Basic Syntax

```python
while condition:
    # code repeats
    # update condition variable
```

### Common Patterns

```python
# Counting
count = 0
while count < 5:
    print(count)
    count += 1

# Countdown
num = 10
while num > 0:
    print(num)
    num -= 1

# Input validation
while True:
    value = input("Enter: ")
    if valid(value):
        break

# Accumulator
total = 0
while condition:
    total += value
```

### Loop Control

| Statement | Effect |
|-----------|--------|
| `break` | Exit loop immediately |
| `continue` | Skip to next iteration |

### Examples

```python
# Break on condition
while True:
    cmd = input("> ")
    if cmd == "quit":
        break
    process(cmd)

# Continue to skip
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue  # Skip even
    print(i)
```

### Avoiding Infinite Loops

```python
# Always ensure condition changes
count = 0
while count < 5:
    print(count)
    count += 1  # REQUIRED!

# Or use break
while True:
    if done:
        break  # Exit point
```

### Common Errors

- **Infinite loop** - Condition never becomes False
- **Off-by-one** - Wrong boundary in condition

### See Also

- [For Loops](for-loops-lesson.html) - Known iteration count
- [Loop Control](loop-control-lesson.html) - break and continue
