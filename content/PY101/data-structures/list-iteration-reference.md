---
title: "Quick Reference: List Iteration"
slug: list-iteration-reference
description: "Quick syntax reference for iterating lists"
course_id: PY101
module: data-structures
module_order: 3
topic: list-iteration
topic_order: 4
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - data-structures
  - list-iteration
outcomes:
  - "Quickly look up iteration syntax"
  - "Review iteration patterns"
capstone_relevance: "Reference for processing records"
---

## Quick Reference: List Iteration

### Basic Iteration

```python
for item in list:
    process(item)
```

### With Index (enumerate)

```python
for i, item in enumerate(list):
    print(f"{i}: {item}")

# Start from 1
for num, item in enumerate(list, 1):
    print(f"{num}. {item}")
```

### Parallel Lists (zip)

```python
for a, b in zip(list1, list2):
    print(f"{a}, {b}")
```

### Common Patterns

```python
# Accumulate
total = 0
for num in numbers:
    total += num

# Build new list
result = []
for item in items:
    result.append(transform(item))

# Filter
matches = []
for item in items:
    if condition(item):
        matches.append(item)

# Search
for i, item in enumerate(items):
    if item == target:
        print(f"Found at {i}")
        break
else:
    print("Not found")
```

### Functions for Lists

| Function | Result |
|----------|--------|
| `len(lst)` | Count |
| `sum(lst)` | Total |
| `min(lst)` | Smallest |
| `max(lst)` | Largest |

### Warnings

- Don't modify list while iterating
- Use copy if modifying: `for item in list[:]:`

### See Also

- [Comprehensions](comprehensions-lesson.html) - Concise syntax
- [For Loops](for-loops-lesson.html) - Loop basics
