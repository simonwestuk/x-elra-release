---
title: "Quick Reference: Comprehensions"
slug: comprehensions-reference
description: "Quick syntax reference for list comprehensions"
course_id: PY101
module: data-structures
module_order: 3
topic: comprehensions
topic_order: 5
type: reference
difficulty: intermediate
estimated_minutes: 5
prerequisites: []
skills:
  - data-structures
  - comprehensions
outcomes:
  - "Quickly look up comprehension syntax"
  - "Review common patterns"
capstone_relevance: "Reference for data transformation"
---

## Quick Reference: Comprehensions

### Basic Syntax

```python
[expression for item in iterable]
```

### With Condition

```python
[expression for item in iterable if condition]
```

### Examples

```python
# Transform
[x * 2 for x in numbers]
[s.upper() for s in strings]
[len(s) for s in words]

# Filter
[x for x in numbers if x > 0]
[s for s in words if len(s) > 3]

# Both
[x * 2 for x in numbers if x > 0]
```

### Common Patterns

```python
# Squares
[x**2 for x in range(1, 11)]

# Filter even
[x for x in nums if x % 2 == 0]

# String cleaning
[s.strip().lower() for s in strings]

# Extract from dicts
[d["name"] for d in records]

# Filter dicts
[d for d in records if d["active"]]

# Flatten
[x for row in matrix for x in row]
```

### Loop vs Comprehension

```python
# Loop
result = []
for x in items:
    if x > 0:
        result.append(x * 2)

# Comprehension
result = [x * 2 for x in items if x > 0]
```

### When to Use

| Use Comprehension | Use Loop |
|-------------------|----------|
| Simple transform | Complex logic |
| Single condition | Multiple steps |
| Readable one-liner | Debugging needed |

### See Also

- [List Iteration](list-iteration-lesson.html) - Loop patterns
- [Lists](lists-lesson.html) - List basics
