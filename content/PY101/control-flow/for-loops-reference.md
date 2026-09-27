---
title: "Quick Reference: For Loops"
slug: for-loops-reference
description: "Quick syntax reference for for loops and range"
course_id: PY101
module: control-flow
module_order: 2
topic: for-loops
topic_order: 8
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - for-loops
outcomes:
  - "Quickly look up for loop syntax"
  - "Review range() variations"
capstone_relevance: "Reference for iterating records in your application"
---

## Quick Reference: For Loops

### Basic Syntax

```python
for item in sequence:
    # process item
```

### Common Sequences

```python
# List
for x in [1, 2, 3]:
    print(x)

# String
for char in "hello":
    print(char)

# Range
for i in range(5):
    print(i)
```

### range() Variations

| Syntax | Result |
|--------|--------|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 5)` | 1, 2, 3, 4 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

### enumerate() for Index

```python
items = ["a", "b", "c"]
for i, item in enumerate(items):
    print(f"{i}: {item}")

# Start from 1
for i, item in enumerate(items, 1):
    print(f"{i}. {item}")
```

### Common Patterns

```python
# Accumulator
total = 0
for num in numbers:
    total += num

# Find max
max_val = items[0]
for item in items:
    if item > max_val:
        max_val = item

# Filter count
count = 0
for item in items:
    if condition:
        count += 1
```

### For vs While

| For | While |
|-----|-------|
| Known iterations | Unknown |
| Sequence iteration | Condition-based |
| Cleaner syntax | More flexible |

### Common Errors

- **Off-by-one** - `range(5)` gives 0-4, not 1-5

### See Also

- [While Loops](while-loops-lesson.html) - Condition-based loops
- [Loop Control](loop-control-lesson.html) - break, continue
- [List Iteration](list-iteration-lesson.html) - More techniques
