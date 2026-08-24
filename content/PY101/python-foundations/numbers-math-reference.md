---
title: "Quick Reference: Numbers and Math"
slug: numbers-math-reference
description: "Quick syntax reference for arithmetic operations"
course_id: PY101
module: python-foundations
module_order: 1
topic: numbers-math
topic_order: 4
type: reference
difficulty: beginner
estimated_minutes: 5
prerequisites: []
skills:
  - numbers
  - math
outcomes:
  - "Quickly look up math operators"
  - "Review operation precedence"
capstone_relevance: "Reference for calculations in your application"
---

## Quick Reference: Numbers and Math

### Arithmetic Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division | `5 / 2` | `2.5` |
| `//` | Floor Division | `5 // 2` | `2` |
| `%` | Modulo | `5 % 2` | `1` |
| `**` | Exponent | `5 ** 2` | `25` |

### Division Comparison

| Expression | Result | Use When |
|------------|--------|----------|
| `7 / 2` | `3.5` | Need exact decimal |
| `7 // 2` | `3` | Need whole number |
| `7 % 2` | `1` | Need remainder |

### Order of Operations (PEMDAS)

1. **P**arentheses `()`
2. **E**xponents `**`
3. **M**ultiplication `*` / **D**ivision `/` `//` `%`
4. **A**ddition `+` / **S**ubtraction `-`

### Examples

```python
# Basic operations
total = price * quantity
average = total / count
remainder = number % divisor

# With parentheses
result = (a + b) * c
percent = (part / whole) * 100

# Common patterns
is_even = number % 2 == 0
squared = value ** 2
```

### Useful Patterns

```python
# Split into whole and remainder
hours = minutes // 60
remaining = minutes % 60

# Percentage calculation
discount = price * (percent / 100)
final = price - discount

# Round to 2 decimal places
rounded = int(value * 100) / 100
```

### Common Errors

- **ZeroDivisionError** - Cannot divide by zero
- **TypeError** - Mixing incompatible types (like str + int)

### See Also

- [Variables & Types](variables-types-lesson.html) - Store calculation results
- [String Formatting](string-formatting-lesson.html) - Display numbers nicely
