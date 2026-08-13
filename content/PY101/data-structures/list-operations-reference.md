---
title: "Quick Reference: List Operations"
slug: list-operations-reference
description: "Quick syntax reference for list operations"
course_id: PY101
module: data-structures
module_order: 3
topic: list-operations
topic_order: 2
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - data-structures
  - list-operations
outcomes:
  - "Quickly look up list operations"
  - "Review sorting and copying patterns"
capstone_relevance: "Reference for organizing data"
---

## Quick Reference: List Operations

### Sorting

| Method | Effect |
|--------|--------|
| `lst.sort()` | Sort in place |
| `lst.sort(reverse=True)` | Sort descending |
| `sorted(lst)` | New sorted list |
| `lst.sort(key=str.lower)` | Custom sort |

### Reversing

```python
lst.reverse()           # In place
list(reversed(lst))     # New list
lst[::-1]               # New list (slicing)
```

### Copying

```python
# Correct copies
copy = lst.copy()
copy = lst[:]
copy = list(lst)

# Wrong! Creates reference
alias = lst  # Both point to same list
```

### Combining

```python
combined = list1 + list2  # New list
list1.extend(list2)       # Modify list1
```

### Statistics

| Function | Result |
|----------|--------|
| `min(lst)` | Smallest |
| `max(lst)` | Largest |
| `sum(lst)` | Total |
| `len(lst)` | Count |
| `sum(lst)/len(lst)` | Average |

### Common Patterns

```python
# Sort without modifying
display = sorted(original)

# Get top N
top_3 = sorted(lst, reverse=True)[:3]

# Get bottom N
bottom_3 = sorted(lst)[:3]
```

### Common Errors

- Modifying list while iterating
- Forgetting `sort()` returns None

### See Also

- [Lists](lists-lesson.html) - Basic operations
- [Slicing](slicing-lesson.html) - Extract portions
