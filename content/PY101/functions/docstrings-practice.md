---
title: "Practice: Writing Docstrings"
slug: docstrings-practice
description: "Practice documenting your functions with docstrings"
course_id: PY101
module: functions
module_order: 4
topic: docstrings
topic_order: 6
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - docstrings-lesson
skills:
  - functions
  - documentation
outcomes:
  - "Write clear docstrings"
  - "Document parameters and return values"
  - "Follow documentation conventions"
capstone_relevance: "Well-documented code is essential for collaboration"
---

## Exercise 1: Simple Docstring

Add a docstring to this function that describes what it does.

```python live
def double(n):
    # Add a docstring here
    return n * 2

print(double(5))
print(double.__doc__)
```

:::hint Stuck?
Add `"""Return the number multiplied by 2."""` right after the `def` line.
:::

:::answer Reveal answer
```python
def double(n):
    """Return the number multiplied by 2."""
    return n * 2

print(double(5))
print(double.__doc__)
```
:::

## Exercise 2: Docstring with Parameters

Add a complete docstring to this function that includes parameter descriptions.

```python live
def greet(name, greeting):
    # Add a docstring with parameter descriptions
    return greeting + ", " + name + "!"

print(greet("Alice", "Hello"))
print(greet.__doc__)
```

:::hint Stuck?
Include "Parameters:" section listing both `name` and `greeting` with descriptions.
:::

:::answer Reveal answer
```python
def greet(name, greeting):
    """Create a personalised greeting message.

    Parameters:
        name: The name of the person to greet.
        greeting: The greeting word to use.

    Returns:
        A formatted greeting string.
    """
    return greeting + ", " + name + "!"

print(greet("Alice", "Hello"))
print(greet.__doc__)
```
:::

## Exercise 3: Document Return Value

Add a docstring that describes the parameters AND what the function returns.

```python live
def is_valid_age(age):
    # Add docstring with Parameters and Returns sections
    return age >= 0 and age <= 150

print(is_valid_age(25))
print(is_valid_age(-5))
print(is_valid_age.__doc__)
```

:::hint Stuck?
Include both "Parameters:" section and "Returns:" section describing the boolean return value.
:::

:::answer Reveal answer
```python
def is_valid_age(age):
    """Check whether an age value is valid.

    Parameters:
        age: The age to validate.

    Returns:
        True if age is between 0 and 150 inclusive, False otherwise.
    """
    return age >= 0 and age <= 150

print(is_valid_age(25))
print(is_valid_age(-5))
print(is_valid_age.__doc__)
```
:::

## Exercise 4: Include an Example

Write a function `celsius_to_fahrenheit` that converts temperature. Include a docstring with an example.

```python live
def celsius_to_fahrenheit(celsius):
    # Add docstring with example
    # Formula: F = C * 9/5 + 32
    pass

print(celsius_to_fahrenheit(0))    # Should print 32.0
print(celsius_to_fahrenheit(100))  # Should print 212.0
print(celsius_to_fahrenheit.__doc__)
```

:::hint Stuck?
In the docstring, add an "Example:" section showing `celsius_to_fahrenheit(0) -> 32.0`.
:::

:::answer Reveal answer
```python
def celsius_to_fahrenheit(celsius):
    """Convert a temperature from Celsius to Fahrenheit.

    Parameters:
        celsius: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit.

    Example:
        celsius_to_fahrenheit(0) -> 32.0
        celsius_to_fahrenheit(100) -> 212.0
    """
    return celsius * 9/5 + 32

print(celsius_to_fahrenheit(0))    # Should print 32.0
print(celsius_to_fahrenheit(100))  # Should print 212.0
print(celsius_to_fahrenheit.__doc__)
```
:::

## Exercise 5: Complete Documentation

Create a well-documented function `calculate_bmi` that:
- Takes `weight` (in kg) and `height` (in meters)
- Returns the BMI (weight / height²)
- Includes full docstring with parameters, return value, and example

```python live
# Write your fully documented function


# Test it
print(calculate_bmi(70, 1.75))  # Should print approximately 22.86
print()
print("Documentation:")
print(calculate_bmi.__doc__)
```

:::hint BMI Formula
BMI = weight / (height * height). Return `weight / (height ** 2)`.
:::

:::hint Docstring Structure
```
"""
Brief description.

Parameters:
    weight: ...
    height: ...

Returns:
    ...

Example:
    ...
"""
```
:::

:::answer Reveal answer
```python
def calculate_bmi(weight, height):
    """Calculate Body Mass Index (BMI).

    Parameters:
        weight: Weight in kilograms.
        height: Height in meters.

    Returns:
        The BMI value as a float (weight / height squared).

    Example:
        calculate_bmi(70, 1.75) -> 22.857142857142858
    """
    return weight / (height ** 2)

# Test it
print(calculate_bmi(70, 1.75))  # Should print approximately 22.86
print()
print("Documentation:")
print(calculate_bmi.__doc__)
```
:::

