---
title: "Default Parameter Values"
slug: defaults-lesson
description: "Learn to create flexible functions with default parameter values"
course_id: PY101
module: functions
module_order: 4
topic: defaults
topic_order: 4
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - parameters-lesson
  - return-values-lesson
skills:
  - functions
  - parameters
outcomes:
  - "Define functions with default parameter values"
  - "Call functions with optional arguments"
  - "Know when to use defaults"
capstone_relevance: "Default values make your functions more flexible"
---

## Introduction

Sometimes you want a function to have a "standard" behavior but also allow customization. Default parameter values let you do exactly that—specify a default that's used when the caller doesn't provide a value.

## Basic Default Values

```python live
def greet(name="World"):
    print("Hello, " + name + "!")

greet()           # Uses default
greet("Alice")    # Overrides default
```

:::expected_output
Hello, World!
Hello, Alice!
:::

The `= "World"` sets a default value. If no argument is passed, `name` becomes `"World"`.

## Multiple Parameters with Defaults

```python live
def make_coffee(size="medium", milk=False):
    order = size + " coffee"
    if milk:
        order += " with milk"
    print(order)

make_coffee()                    # medium coffee
make_coffee("large")             # large coffee
make_coffee("small", True)       # small coffee with milk
make_coffee(milk=True)           # medium coffee with milk
```

:::expected_output
medium coffee
large coffee
small coffee with milk
medium coffee with milk
:::

## Mixing Required and Default Parameters

Required parameters must come before default parameters:

```python live
def introduce(name, greeting="Hello"):
    print(greeting + ", " + name + "!")

introduce("Alice")               # Hello, Alice!
introduce("Bob", "Hi")           # Hi, Bob!
introduce("Charlie", "Welcome")  # Welcome, Charlie!
```

:::expected_output
Hello, Alice!
Hi, Bob!
Welcome, Charlie!
:::

## Using Named Arguments

Named arguments are very useful with defaults:

```python live
def format_price(amount, currency="$", decimals=2):
    formatted = round(amount, decimals)
    return currency + str(formatted)

print(format_price(19.99))                    # $19.99
print(format_price(19.99, "£"))               # £19.99
print(format_price(19.99, decimals=0))        # $20
print(format_price(19.99, "€", 1))            # €20.0
```

:::expected_output
$19.99
£19.99
$20.0
€20.0
:::

## Practical Example: Text Formatter

```python live
def format_text(text, uppercase=False, border=False):
    result = text
    if uppercase:
        result = result.upper()
    if border:
        line = "=" * (len(result) + 4)
        result = line + "\n| " + result + " |\n" + line
    return result

print(format_text("hello"))
print()
print(format_text("hello", uppercase=True))
print()
print(format_text("hello", border=True))
print()
print(format_text("hello", True, True))
```

:::expected_output
hello

HELLO

=========
| hello |
=========

=========
| HELLO |
=========
:::

## Default Values for Calculations

```python live
def calculate_tip(amount, percent=15):
    tip = amount * percent / 100
    return round(tip, 2)

print("15% tip:", calculate_tip(50))      # Default 15%
print("20% tip:", calculate_tip(50, 20))  # Custom 20%
print("10% tip:", calculate_tip(50, 10))  # Custom 10%
```

:::expected_output
15% tip: 7.5
20% tip: 10.0
10% tip: 5.0
:::

## Boolean Defaults

```python live
def display_item(name, price, on_sale=False):
    info = name + ": $" + str(price)
    if on_sale:
        info += " (SALE!)"
    print(info)

display_item("Shirt", 29.99)
display_item("Pants", 49.99, True)
display_item("Shoes", 89.99, on_sale=True)
```

:::expected_output
Shirt: $29.99
Pants: $49.99 (SALE!)
Shoes: $89.99 (SALE!)
:::

## Common Pattern: Optional Behavior

```python live
def search(items, query, case_sensitive=False):
    results = []
    for item in items:
        if case_sensitive:
            if query in item:
                results.append(item)
        else:
            if query.lower() in item.lower():
                results.append(item)
    return results

fruits = ["Apple", "Banana", "APRICOT", "Cherry"]
print(search(fruits, "ap"))                    # All matches (case-insensitive)
print(search(fruits, "ap", True))              # Only exact case
print(search(fruits, "AP", case_sensitive=True))  # Uppercase only
```

:::expected_output
['Apple', 'APRICOT']
[]
['APRICOT']
:::

## Key Points

- Default values are assigned with `=` in the parameter list
- Parameters with defaults are optional when calling
- Required parameters must come before defaults
- Named arguments let you skip to specific parameters
- Defaults make functions more flexible and user-friendly

:::hint Common Mistake
Putting required parameters after default parameters causes a syntax error. Always put required parameters first.
:::

