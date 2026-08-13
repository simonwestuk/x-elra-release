---
title: "Quick Reference: Lists"
slug: lists-reference
description: "Quick syntax reference for Python lists"
course_id: PY101
module: data-structures
module_order: 3
topic: lists
topic_order: 1
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - data-structures
  - lists
outcomes:
  - "Quickly look up list syntax"
  - "Review list operations"
capstone_relevance: "Reference for managing collections"
---

## Quick Reference: Lists

### Creating Lists

```python
empty = []
numbers = [1, 2, 3]
mixed = ["a", 1, True]
from_range = list(range(5))
```

### Accessing Elements

| Syntax | Meaning |
|--------|---------|
| `lst[0]` | First element |
| `lst[-1]` | Last element |
| `lst[2]` | Third element |
| `len(lst)` | Number of elements |

### Modifying

```python
# Change element
lst[0] = "new"

# Add to end
lst.append(item)

# Insert at position
lst.insert(index, item)

# Add multiple
lst.extend([a, b, c])
```

### Removing

```python
# By value (first occurrence)
lst.remove(value)

# By index (returns removed item)
item = lst.pop(index)

# Last item
item = lst.pop()

# Clear all
lst.clear()
```

### Searching

```python
# Check membership
if item in lst:
    ...

# Find index
idx = lst.index(item)

# Count occurrences
n = lst.count(item)
```

### Common Patterns

```python
# Iterate
for item in lst:
    process(item)

# With index
for i, item in enumerate(lst):
    print(f"{i}: {item}")

# Check empty
if not lst:
    print("Empty")
```

### Common Errors

- **IndexError** - Index out of range
- **ValueError** - remove() item not found

### See Also

- [List Operations](list-operations-lesson.html) - More methods
- [Slicing](slicing-lesson.html) - Get portions
- [List Iteration](list-iteration-lesson.html) - Loop techniques
