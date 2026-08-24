---
title: "Quick Reference: Nested Loops"
slug: nested-loops-reference
description: "Quick syntax reference for nested loops"
course_id: PY101
module: control-flow
module_order: 2
topic: nested-loops
topic_order: 10
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - control-flow
  - nested-loops
outcomes:
  - "Quickly look up nested loop syntax"
  - "Review common patterns"
capstone_relevance: "Reference for complex iterations in your application"
---

## Quick Reference: Nested Loops

### Basic Syntax

```python
for outer in outer_sequence:
    for inner in inner_sequence:
        # runs for each combination
```

### Execution Order

```
outer=0, inner=0,1,2
outer=1, inner=0,1,2
outer=2, inner=0,1,2
```

### Common Patterns

```python
# Grid/Rectangle
for row in range(rows):
    for col in range(cols):
        print("*", end="")
    print()

# 2D List Processing
for row in grid:
    for cell in row:
        process(cell)

# With Indices
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        item = matrix[i][j]

# Combinations
for a in list1:
    for b in list2:
        print(f"{a}, {b}")
```

### Printing Patterns

| Pattern | Outer | Inner |
|---------|-------|-------|
| Rectangle | rows | cols |
| Triangle | 1 to n | 1 to row |
| Inverted | n to 1 | 1 to row |

### Break in Nested Loops

```python
# break only exits innermost loop
for outer in range(3):
    for inner in range(3):
        if condition:
            break  # exits inner only
    # continues here
```

### Using enumerate

```python
for i, row in enumerate(matrix):
    for j, cell in enumerate(row):
        print(f"[{i}][{j}] = {cell}")
```

### Common Errors

- Same variable for both loops
- Forgetting `print()` for new line
- Off-by-one in range

### See Also

- [For Loops](for-loops-lesson.html) - Basic iteration
- [Lists](lists-lesson.html) - Working with lists
- [Dict Operations](dict-operations-lesson.html) - Nested dictionaries
