---
title: "Numbers and Math Operations"
slug: numbers-math-lesson
description: "Learn to perform calculations with Python's numeric operators"
course_id: PY101
module: python-foundations
module_order: 1
topic: numbers-math
topic_order: 4
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - variables-types-lesson
skills:
  - numbers
  - math
outcomes:
  - "Perform basic arithmetic operations"
  - "Understand the difference between / and //"
  - "Use the modulo operator for remainders"
capstone_relevance: "Calculate totals, averages, and statistics in your data application"
---

## Introduction

Python can work as a powerful calculator. You can perform arithmetic operations on numbers directly or with variables.

## Basic Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division | `5 / 2` | `2.5` |
| `//` | Floor Division | `5 // 2` | `2` |
| `%` | Modulo (remainder) | `5 % 2` | `1` |
| `**` | Exponent (power) | `5 ** 2` | `25` |

## Try It: Basic Math

```python live
print(10 + 5)   # Addition
print(10 - 5)   # Subtraction
print(10 * 5)   # Multiplication
print(10 / 5)   # Division
```

:::expected_output
15
5
50
2.0
:::

## Division Types

Regular division `/` always gives a float (decimal):

```python live
print(10 / 5)   # 2.0 (not 2)
print(10 / 3)   # 3.333...
```

Floor division `//` gives a whole number (rounds down):

```python live
print(10 // 3)  # 3 (not 3.333)
print(7 // 2)   # 3 (not 3.5)
```

:::expected_output
3
3
:::

## Modulo (Remainder)

The `%` operator gives the remainder after division:

```python live
print(10 % 3)   # 1 (10 = 3*3 + 1)
print(7 % 2)    # 1 (7 = 2*3 + 1)
print(8 % 4)    # 0 (divides evenly)
```

:::expected_output
1
1
0
:::

Useful for checking if a number is even or odd!

## Exponents

Use `**` for powers:

```python live
print(2 ** 3)   # 8 (2 cubed)
print(5 ** 2)   # 25 (5 squared)
print(10 ** 0)  # 1 (anything to power 0)
```

:::expected_output
8
25
1
:::

## Order of Operations

Python follows standard math order: PEMDAS
- **P**arentheses first
- **E**xponents
- **M**ultiplication and **D**ivision (left to right)
- **A**ddition and **S**ubtraction (left to right)

```python live
print(2 + 3 * 4)      # 14 (not 20)
print((2 + 3) * 4)    # 20 (parentheses first)
print(10 - 4 - 2)     # 4 (left to right)
```

:::expected_output
14
20
4
:::

## Math with Variables

Store results in variables for reuse:

```python live
price = 25
quantity = 4
subtotal = price * quantity
tax = subtotal * 0.1
total = subtotal + tax

print("Subtotal:", subtotal)
print("Tax:", tax)
print("Total:", total)
```

:::expected_output
Subtotal: 100
Tax: 10.0
Total: 110.0
:::

## Key Points

- Python supports all basic math operations
- `/` gives decimals, `//` gives whole numbers
- `%` gives the remainder (great for even/odd checks)
- `**` is for exponents (powers)
- Use parentheses to control operation order

:::hint Common Mistake
Confusing `/` and `//`. Use `/` when you want decimals (like money), use `//` when you only want whole numbers (like counting items).
:::
