---
title: "Quick Reference: Tuples"
slug: tuples-reference
description: "Quick syntax reference for tuples"
course_id: PY101
module: data-structures
module_order: 3
topic: tuples
topic_order: 6
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - data-structures
  - tuples
outcomes:
  - "Quickly look up tuple syntax"
  - "Review tuple operations"
capstone_relevance: "Reference for fixed data structures"
---

## Quick Reference: Tuples

### Creating Tuples

```python
t = (1, 2, 3)       # With parentheses
t = 1, 2, 3         # Without parentheses
t = (42,)           # Single element (comma!)
t = tuple([1,2,3])  # From list
```

### Accessing

```python
t[0]     # First element
t[-1]    # Last element
t[1:3]   # Slice
len(t)   # Length
```

### Unpacking

```python
# Basic unpacking
x, y, z = (1, 2, 3)

# In loops
for a, b in [(1, 2), (3, 4)]:
    print(a, b)

# Swap values
a, b = b, a
```

### Tuple vs List

| Tuple | List |
|-------|------|
| Immutable | Mutable |
| `()` | `[]` |
| Can be dict key | Cannot |
| Faster | Slower |

### Common Patterns

```python
# Return multiple values
def get_point():
    return 10, 20

x, y = get_point()

# As dict keys
locations = {(0, 0): "Origin"}

# Named data
person = ("Alice", 25, "NYC")
name, age, city = person
```

### Methods

| Method | Result |
|--------|--------|
| `t.count(x)` | Count of x |
| `t.index(x)` | Index of x |

### Common Errors

- **TypeError** - Cannot modify tuple elements
- Missing comma in single-element tuple

### See Also

- [Lists](lists-lesson.html) - Mutable sequences
- [Dictionaries](dicts-lesson.html) - Key-value pairs
