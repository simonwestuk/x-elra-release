---
title: "Quick Reference: Loop Control"
slug: loop-control-reference
description: "Quick syntax reference for break, continue, and loop else"
course_id: PY101
module: control-flow
module_order: 2
topic: loop-control
topic_order: 9
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - loop-control
outcomes:
  - "Quickly look up break/continue syntax"
  - "Review loop control patterns"
capstone_relevance: "Reference for controlling loop flow in your application"
---

## Quick Reference: Loop Control

### Statements

| Statement | Effect |
|-----------|--------|
| `break` | Exit loop immediately |
| `continue` | Skip to next iteration |

### break Example

```python
for item in items:
    if found_it:
        break  # Exit loop now

# Execution continues here
```

### continue Example

```python
for item in items:
    if should_skip:
        continue  # Go to next item
    process(item)
```

### Loop else Clause

```python
for item in items:
    if match:
        print("Found!")
        break
else:
    print("Not found")  # Only if no break
```

### Common Patterns

```python
# Search and stop
for item in items:
    if item == target:
        result = item
        break

# Skip invalid
for item in items:
    if not valid(item):
        continue
    process(item)

# Menu loop
while True:
    choice = input("Choice: ")
    if choice == "quit":
        break
    handle(choice)
```

### In Nested Loops

```python
# break only exits innermost loop
for outer in range(3):
    for inner in range(3):
        if condition:
            break  # Exits inner loop only
```

### When to Use

| Use break | Use continue |
|-----------|--------------|
| Found target | Invalid item |
| Error occurred | Special case |
| User quit | Skip this one |

### Common Errors

- Code after break/continue in same block won't run
- break only exits the innermost loop

### See Also

- [For Loops](for-loops-lesson.html) - Basic iteration
- [While Loops](while-loops-lesson.html) - Condition loops
- [Nested Loops](nested-loops-lesson.html) - Multiple levels
