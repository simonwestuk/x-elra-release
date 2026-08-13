---
title: "Quick Reference: Dictionaries"
slug: dicts-reference
description: "Quick syntax reference for dictionaries"
course_id: PY101
module: data-structures
module_order: 3
topic: dicts
topic_order: 7
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - data-structures
  - dicts
outcomes:
  - "Quickly look up dictionary syntax"
  - "Review common operations"
capstone_relevance: "Reference for record data"
---

## Quick Reference: Dictionaries

### Creating

```python
d = {}                       # Empty
d = {"name": "Alice"}       # With data
d = dict(name="Alice")      # Alternative
```

### Accessing

```python
d["key"]                    # Get (KeyError if missing)
d.get("key")               # Get (None if missing)
d.get("key", default)      # Get with default
```

### Modifying

```python
d["key"] = value           # Add or update
d.update({"a": 1})         # Merge in
del d["key"]               # Delete
d.pop("key")               # Remove and return
d.clear()                  # Remove all
```

### Checking

```python
"key" in d                 # Key exists?
"key" not in d             # Key missing?
len(d)                     # Number of pairs
```

### Iterating

```python
# Keys only
for key in d:
    print(key)

# Key and value
for key, value in d.items():
    print(key, value)

# Values only
for value in d.values():
    print(value)
```

### Getting Contents

```python
d.keys()                   # All keys
d.values()                 # All values
d.items()                  # Key-value tuples
```

### Common Patterns

```python
# Counting
counts = {}
for item in items:
    counts[item] = counts.get(item, 0) + 1

# Grouping
groups = {}
for item in items:
    key = item["type"]
    if key not in groups:
        groups[key] = []
    groups[key].append(item)
```

### Common Errors

- **KeyError** - Accessing missing key
- Keys must be immutable (no lists)

### See Also

- [Dict Operations](dict-operations-lesson.html) - More methods
- [Lists](lists-lesson.html) - Ordered sequences
