---
title: "Quick Reference: Slicing"
slug: slicing-reference
description: "Quick syntax reference for list slicing"
course_id: PY101
module: data-structures
module_order: 3
topic: slicing
topic_order: 3
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - data-structures
  - slicing
outcomes:
  - "Quickly look up slice syntax"
  - "Review common slicing patterns"
capstone_relevance: "Reference for extracting data subsets"
---

## Quick Reference: Slicing

### Syntax

```python
list[start:stop:step]
```

### Basic Slices

| Slice | Result |
|-------|--------|
| `lst[2:5]` | Elements 2, 3, 4 |
| `lst[:3]` | First 3 |
| `lst[3:]` | From index 3 to end |
| `lst[:]` | Copy of entire list |

### Negative Indices

| Slice | Result |
|-------|--------|
| `lst[-3:]` | Last 3 |
| `lst[:-2]` | All except last 2 |
| `lst[-4:-1]` | 4th-last to 2nd-last |

### Step

| Slice | Result |
|-------|--------|
| `lst[::2]` | Every 2nd element |
| `lst[1::2]` | Every 2nd, from index 1 |
| `lst[::-1]` | Reversed |

### Common Patterns

```python
# Pagination
page_items = items[start:start+size]

# First/last N
first_5 = lst[:5]
last_5 = lst[-5:]

# Excluding ends
middle = lst[1:-1]

# Reversing
backwards = lst[::-1]
```

### Key Rules

- Stop index is exclusive
- Negative indices count from end
- Out-of-range indices are handled gracefully
- Slicing creates a new list

### Common Errors

- Forgetting stop is exclusive
- Expecting in-place modification

### See Also

- [Lists](lists-lesson.html) - Basic list operations
- [List Iteration](list-iteration-lesson.html) - Processing lists
