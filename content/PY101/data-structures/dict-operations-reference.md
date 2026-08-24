---
title: "Quick Reference: Dictionary Operations"
slug: dict-operations-reference
description: "Quick syntax reference for dictionary operations"
course_id: PY101
module: data-structures
module_order: 3
topic: dict-operations
topic_order: 8
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - data-structures
  - dict-operations
outcomes:
  - "Quickly look up dictionary operations"
  - "Review advanced patterns"
capstone_relevance: "Reference for data analysis in your application"
---

## Quick Reference: Dictionary Operations

### Iteration

```python
# Keys
for key in d:
    print(key)

# Key-value pairs
for key, value in d.items():
    print(key, value)

# Values only
for value in d.values():
    print(value)
```

### Merging

```python
# Spread syntax
merged = {**d1, **d2}

# Update in place
d1.update(d2)

# Defaults + overrides
settings = {**defaults, **user_settings}
```

### Counting Pattern

```python
counts = {}
for item in items:
    counts[item] = counts.get(item, 0) + 1
```

### Grouping Pattern

```python
groups = {}
for item in items:
    key = item["category"]
    if key not in groups:
        groups[key] = []
    groups[key].append(item)
```

### Dict Comprehension

```python
# Basic
{k: v for k, v in items}

# From two lists
{k: v for k, v in zip(keys, values)}

# Filtering
{k: v for k, v in d.items() if v > 0}

# Transforming
{k: v * 2 for k, v in d.items()}
```

### Useful Functions

| Function | Result |
|----------|--------|
| `len(d)` | Number of pairs |
| `max(d, key=d.get)` | Key with max value |
| `min(d, key=d.get)` | Key with min value |
| `sum(d.values())` | Sum of values |

### Common Patterns

```python
# Safe nested access
d.get("key1", {}).get("key2", default)

# Invert dict
{v: k for k, v in d.items()}

# Remove key safely
d.pop("key", None)  # No error if missing
```

### See Also

- [Dictionaries](dicts-lesson.html) - Basics
- [Comprehensions](comprehensions-lesson.html) - List versions
