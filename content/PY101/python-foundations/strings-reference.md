---
title: "Quick Reference: Strings"
slug: strings-reference
description: "Quick syntax reference for string operations"
course_id: PY101
module: python-foundations
module_order: 1
topic: strings
topic_order: 5
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - strings
outcomes:
  - "Quickly look up string syntax"
  - "Review string operations"
capstone_relevance: "Reference for text handling in your application"
---

## Quick Reference: Strings

### Creating Strings

```python
text = "Hello"      # Double quotes
text = 'Hello'      # Single quotes
text = "It's OK"    # Single quote inside double
text = 'Say "Hi"'   # Double quotes inside single
```

### Common Operations

| Operation | Code | Result |
|-----------|------|--------|
| Concatenation | `"Hi" + " " + "there"` | `"Hi there"` |
| Repetition | `"ab" * 3` | `"ababab"` |
| Length | `len("Hello")` | `5` |
| First char | `"Hello"[0]` | `"H"` |
| Last char | `"Hello"[-1]` | `"o"` |

### Indexing

```
String:   P  y  t  h  o  n
Index:    0  1  2  3  4  5
Negative: -6 -5 -4 -3 -2 -1
```

```python
word = "Python"
word[0]   # 'P' - first
word[2]   # 't' - third
word[-1]  # 'n' - last
word[-2]  # 'o' - second to last
```

### Examples

```python
# Combine names
full = first + " " + last

# Create border
line = "-" * 40

# Check length
if len(password) >= 8:
    print("OK")

# Get initials
initials = first[0] + middle[0] + last[0]
```

### Common Errors

- **IndexError: string index out of range** - Accessing position that doesn't exist
- **TypeError: can only concatenate str** - Mixing strings and numbers without conversion

### See Also

- [String Methods](string-methods-lesson.html) - Transform and search strings
- [String Formatting](string-formatting-lesson.html) - Insert values into strings
