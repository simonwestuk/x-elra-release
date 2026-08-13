---
title: "Documenting Functions with Docstrings"
slug: docstrings-lesson
description: "Learn to document your functions for better code clarity"
course_id: PY101
module: functions
module_order: 4
topic: docstrings
topic_order: 6
type: lesson
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - parameters-lesson
  - return-values-lesson
skills:
  - functions
  - documentation
outcomes:
  - "Write docstrings for functions"
  - "Describe parameters and return values"
  - "Access docstrings programmatically"
capstone_relevance: "Good documentation makes your code maintainable"
---

## Introduction

A **docstring** is a special string that documents what a function does. It helps other programmers (and future you!) understand how to use your code. Docstrings are written right after the function definition.

## Basic Docstring

```python live
def greet(name):
    """Display a greeting message."""
    print("Hello, " + name + "!")

greet("Alice")

# View the docstring
print("\nDocumentation:")
print(greet.__doc__)
```

:::expected_output
Hello, Alice!

Documentation:
Display a greeting message.
:::

The docstring is the text between triple quotes right after `def`.

## Why Use Docstrings?

1. **Self-documenting code** - Others understand what functions do
2. **IDE help** - Many editors show docstrings as you type
3. **Future reference** - You'll forget what your code does!
4. **Professional practice** - Standard in real-world projects

## Single-Line Docstrings

For simple functions, use a one-line docstring:

```python live
def square(n):
    """Return the square of a number."""
    return n * n

def is_positive(n):
    """Return True if n is positive, False otherwise."""
    return n > 0

print(square(5))
print(is_positive(-3))
```

:::expected_output
25
False
:::

## Multi-Line Docstrings

For complex functions, describe parameters and return values:

```python live
def calculate_discount(price, percent, min_purchase=0):
    """
    Calculate the discounted price.

    Parameters:
        price: The original price
        percent: Discount percentage (e.g., 20 for 20%)
        min_purchase: Minimum purchase required for discount

    Returns:
        The price after discount, or original if under minimum
    """
    if price < min_purchase:
        return price
    discount = price * percent / 100
    return price - discount

print(calculate_discount(100, 20))
print(calculate_discount(50, 20, min_purchase=75))
```

:::expected_output
80.0
50
:::

## Docstring Structure

```python
def function_name(param1, param2):
    """
    Brief description of what the function does.

    Parameters:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of what is returned

    Example:
        >>> function_name(1, 2)
        3
    """
    # Function body
```

## Examples in Docstrings

Include usage examples to show how the function works:

```python live
def format_name(first, last, uppercase=False):
    """
    Combine first and last name into full name.

    Parameters:
        first: First name
        last: Last name
        uppercase: If True, return in all caps

    Returns:
        The formatted full name

    Examples:
        format_name("John", "Doe") -> "John Doe"
        format_name("Jane", "Doe", True) -> "JANE DOE"
    """
    full = first + " " + last
    if uppercase:
        return full.upper()
    return full

print(format_name("John", "Doe"))
print(format_name("Jane", "Doe", True))
```

:::expected_output
John Doe
JANE DOE
:::

## Accessing Docstrings

You can access a function's docstring with `.__doc__`:

```python live
def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def multiply(a, b):
    """Return the product of two numbers."""
    return a * b

# Access the docstrings
print("add:", add.__doc__)
print("multiply:", multiply.__doc__)
```

:::expected_output
add: Return the sum of two numbers.
multiply: Return the product of two numbers.
:::

## Docstrings vs Comments

```python live
# This is a comment - for internal notes
# Comments explain HOW the code works

def calculate_area(width, height):
    """
    Calculate the area of a rectangle.

    Docstrings explain WHAT the function does
    and HOW to use it.
    """
    # Multiply dimensions (internal note)
    return width * height

print(calculate_area(5, 3))
```

:::expected_output
15
:::

- **Comments** (`#`): Internal notes for developers reading the code
- **Docstrings** (`"""`): External documentation for users of the function

## Key Points

- Docstrings go immediately after the function definition
- Use triple quotes `""" """` for docstrings
- Single line for simple functions
- Multi-line for complex functions with parameters
- Include examples when helpful
- Access with `function.__doc__`

:::hint Best Practice
Write docstrings even for your own code. When you return to it months later, you'll thank yourself!
:::

