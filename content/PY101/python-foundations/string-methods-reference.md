---
title: "Quick Reference: String Methods"
slug: string-methods-reference
description: "Quick syntax reference for string methods"
course_id: PY101
module: python-foundations
module_order: 1
topic: string-methods
topic_order: 6
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - strings
  - string-methods
outcomes:
  - "Quickly look up string methods"
  - "Review method syntax and examples"
capstone_relevance: "Reference for text processing in your application"
---

## Quick Reference: String Methods

### Case Methods

| Method | Example | Result |
|--------|---------|--------|
| `upper()` | `"hello".upper()` | `"HELLO"` |
| `lower()` | `"HELLO".lower()` | `"hello"` |
| `title()` | `"hello world".title()` | `"Hello World"` |
| `capitalize()` | `"hello".capitalize()` | `"Hello"` |

### Whitespace Methods

| Method | Example | Result |
|--------|---------|--------|
| `strip()` | `"  hi  ".strip()` | `"hi"` |
| `lstrip()` | `"  hi  ".lstrip()` | `"hi  "` |
| `rstrip()` | `"  hi  ".rstrip()` | `"  hi"` |

### Search Methods

| Method | Example | Result |
|--------|---------|--------|
| `find()` | `"hello".find("l")` | `2` |
| `count()` | `"hello".count("l")` | `2` |
| `startswith()` | `"hello".startswith("he")` | `True` |
| `endswith()` | `"hello".endswith("lo")` | `True` |

### Validation Methods

| Method | Description | Example |
|--------|-------------|---------|
| `isdigit()` | All digits? | `"123".isdigit()` → `True` |
| `isalpha()` | All letters? | `"abc".isalpha()` → `True` |
| `isalnum()` | Letters/digits? | `"abc123".isalnum()` → `True` |
| `isspace()` | All whitespace? | `"  ".isspace()` → `True` |

### Transform Methods

| Method | Example | Result |
|--------|---------|--------|
| `replace(old, new)` | `"hi".replace("i", "ey")` | `"hey"` |
| `split(sep)` | `"a,b,c".split(",")` | `["a","b","c"]` |
| `join(list)` | `"-".join(["a","b"])` | `"a-b"` |

### Common Patterns

```python
# Clean user input
clean = user_input.strip().lower()

# Check for keyword (case-insensitive)
found = "error" in log.lower()

# Normalize filename
safe = filename.strip().lower().replace(" ", "_")

# Validate input
if text.strip():
    # text is not empty/whitespace
```

### Common Errors

- Method not saving result: Use `text = text.upper()` not just `text.upper()`
- `find()` returns -1 if not found (not an error)

### See Also

- [Strings](strings-lesson.html) - String basics
- [String Formatting](string-formatting-lesson.html) - Insert values
