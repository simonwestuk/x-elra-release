---
title: "Quick Reference: String Formatting"
slug: string-formatting-reference
description: "Quick syntax reference for f-strings and formatting"
course_id: PY101
module: python-foundations
module_order: 1
topic: string-formatting
topic_order: 7
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - strings
  - formatting
outcomes:
  - "Quickly look up f-string syntax"
  - "Review format specifiers"
capstone_relevance: "Reference for formatting output in your application"
---

## Quick Reference: String Formatting

### F-String Syntax

```python
f"text {variable} more text"
f"result: {expression}"
```

### Number Formatting

| Format | Example | Result |
|--------|---------|--------|
| `:.2f` | `f"{3.14159:.2f}"` | `3.14` |
| `:.0f` | `f"{3.7:.0f}"` | `4` |
| `:,` | `f"{1000000:,}"` | `1,000,000` |
| `:.2%` | `f"{0.15:.2%}"` | `15.00%` |
| `:,.2f` | `f"{1234.5:,.2f}"` | `1,234.50` |

### Alignment

| Format | Meaning | Example |
|--------|---------|---------|
| `:<10` | Left, 10 chars | `f"{'hi':<10}"` → `"hi        "` |
| `:>10` | Right, 10 chars | `f"{'hi':>10}"` → `"        hi"` |
| `:^10` | Center, 10 chars | `f"{'hi':^10}"` → `"    hi    "` |

### Padding with Characters

```python
f"{'hi':*^10}"  # "****hi****"
f"{42:0>5}"     # "00042"
```

### Common Patterns

```python
# Money formatting
price = 19.99
print(f"${price:.2f}")        # $19.99
print(f"${price:>10.2f}")     # $     19.99

# Large numbers
pop = 8000000
print(f"{pop:,}")             # 8,000,000

# Percentages
rate = 0.0825
print(f"{rate:.2%}")          # 8.25%

# Table columns
print(f"{'Name':<15} {'Score':>8}")
print(f"{'Alice':<15} {95:>8}")
```

### Format Specification

```
{value:fill align width .precision type}

fill  = character for padding
align = < left, > right, ^ center
width = minimum characters
.precision = decimal places
type  = f float, % percent, , comma
```

### Common Errors

- Missing `f` prefix: `"Hello {name}"` prints literally
- Wrong braces: Use `{` not `(` for variables

### See Also

- [Strings](strings-lesson.html) - String basics
- [String Methods](string-methods-lesson.html) - Transform strings
