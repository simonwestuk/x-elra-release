---
title: "String Formatting"
slug: string-formatting-lesson
description: "Learn to create dynamic strings by inserting variables and values"
course_id: PY101
module: python-foundations
module_order: 1
topic: string-formatting
topic_order: 7
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - strings-lesson
skills:
  - strings
  - formatting
outcomes:
  - "Use f-strings to insert values into text"
  - "Format numbers with decimal places"
  - "Create aligned and padded output"
capstone_relevance: "Display data records with proper formatting in your application"
---

## Introduction

String formatting lets you insert variables and expressions into text. This is much cleaner than concatenating strings with `+`. Python's f-strings make this easy.

## F-Strings (Formatted String Literals)

Put `f` before the string and use `{variable}` to insert values:

```python live
name = "Alice"
age = 25
print(f"My name is {name} and I am {age} years old.")
```

:::expected_output
My name is Alice and I am 25 years old.
:::

## Try It

```python live
item = "Coffee"
price = 4.99
quantity = 2
print(f"You ordered {quantity} {item}(s) at ${price} each.")
```

:::expected_output
You ordered 2 Coffee(s) at $4.99 each.
:::

## Expressions in F-Strings

You can put calculations inside the braces:

```python live
width = 5
height = 3
print(f"Area: {width * height} square units")
print(f"Half of 10 is {10 / 2}")
```

:::expected_output
Area: 15 square units
Half of 10 is 5.0
:::

## Formatting Numbers

Control decimal places with `:.Nf` where N is the number of decimals:

```python live
price = 19.99
tax = price * 0.08

print(f"Price: ${price:.2f}")
print(f"Tax: ${tax:.2f}")
print(f"Pi: {3.14159:.3f}")
```

:::expected_output
Price: $19.99
Tax: $1.60
Pi: 3.142
:::

## Adding Commas to Large Numbers

Use `:,` to add thousand separators:

```python live
population = 8405837
print(f"Population: {population:,}")
```

:::expected_output
Population: 8,405,837
:::

## Padding and Alignment

Control width and alignment:

| Format | Meaning |
|--------|---------|
| `{x:10}` | 10 characters wide, right-aligned (default for numbers) |
| `{x:<10}` | Left-aligned |
| `{x:>10}` | Right-aligned |
| `{x:^10}` | Centered |

```python live
name = "Alice"
print(f"|{name:10}|")   # Right-aligned in 10 chars
print(f"|{name:<10}|")  # Left-aligned
print(f"|{name:^10}|")  # Centered
```

:::expected_output
|Alice     |
|Alice     |
|  Alice   |
:::

## Creating Tables

Use formatting to align columns:

```python live
print(f"{'Item':<12} {'Price':>8}")
print(f"{'-'*12} {'-'*8}")
print(f"{'Apple':<12} {'$1.50':>8}")
print(f"{'Banana':<12} {'$0.75':>8}")
print(f"{'Orange':<12} {'$2.00':>8}")
```

:::expected_output
Item            Price
------------ --------
Apple           $1.50
Banana          $0.75
Orange          $2.00
:::

## Combining Formats

You can combine alignment and number formatting:

```python live
products = [("Widget", 9.99), ("Gadget", 24.50), ("Gizmo", 199.00)]

print(f"{'Product':<10} {'Price':>10}")
print("-" * 21)
for name, price in products:
    print(f"{name:<10} ${price:>9.2f}")
```

:::expected_output
Product         Price
---------------------
Widget     $     9.99
Gadget     $    24.50
Gizmo      $   199.00
:::

## Percent Formatting

Format as percentage with `:.N%`:

```python live
rate = 0.0825
print(f"Tax rate: {rate:.2%}")  # 8.25%

score = 45
total = 50
print(f"Score: {score/total:.1%}")  # 90.0%
```

:::expected_output
Tax rate: 8.25%
Score: 90.0%
:::

## Key Points

- F-strings start with `f` before the opening quote
- Put variables in `{braces}` to insert them
- Use `:.2f` for 2 decimal places
- Use `:,` for thousand separators
- Use `:<`, `:>`, `:^` for alignment
- F-strings can contain any expression

:::hint Common Mistake
Forgetting the `f` before the string. `"Hello {name}"` prints literally, but `f"Hello {name}"` inserts the variable.
:::
