---
title: "Practice: Modules and Imports"
slug: modules-imports-practice
description: "Practice using Python modules"
course_id: PY101
module: building-apps
module_order: 7
topic: modules-imports
topic_order: 2
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - modules-imports-lesson
skills:
  - modules
  - imports
outcomes:
  - "Import and use various modules"
  - "Choose appropriate import styles"
  - "Apply module functions to problems"
capstone_relevance: "Modules extend your application's capabilities"
---

## Exercise 1: Math Module

Use the math module to solve these problems.

```python live
import math

# 1. Calculate the square root of 144
sqrt_result = 0  # Your code here

# 2. Round 7.8 up to nearest integer
ceil_result = 0  # Your code here

# 3. Round 7.8 down to nearest integer
floor_result = 0  # Your code here

# 4. Calculate 2 to the power of 8
power_result = 0  # Your code here

print("sqrt(144):", sqrt_result)    # Should be 12.0
print("ceil(7.8):", ceil_result)    # Should be 8
print("floor(7.8):", floor_result)  # Should be 7
print("2^8:", power_result)         # Should be 256.0
```

:::expected_output
sqrt(144): 12.0
ceil(7.8): 8
floor(7.8): 7
2^8: 256.0
:::

:::hint Stuck?
Use `math.sqrt()`, `math.ceil()`, `math.floor()`, and `math.pow()`.
:::

:::answer Reveal answer
```python
import math

# 1. Calculate the square root of 144
sqrt_result = math.sqrt(144)

# 2. Round 7.8 up to nearest integer
ceil_result = math.ceil(7.8)

# 3. Round 7.8 down to nearest integer
floor_result = math.floor(7.8)

# 4. Calculate 2 to the power of 8
power_result = math.pow(2, 8)

print("sqrt(144):", sqrt_result)    # Should be 12.0
print("ceil(7.8):", ceil_result)    # Should be 8
print("floor(7.8):", floor_result)  # Should be 7
print("2^8:", power_result)         # Should be 256.0
```
:::

## Exercise 2: Random Module

Use the random module to create a simple dice roller.

```python live
import random

def roll_dice(num_dice, sides=6):
    """Roll num_dice dice with given number of sides."""
    # Return list of random numbers between 1 and sides
    # Your code here
    pass

# Test
rolls = roll_dice(3)
print("Rolling 3 six-sided dice:", rolls)
print("Total:", sum(rolls) if rolls else 0)

rolls = roll_dice(2, 20)
print("Rolling 2 twenty-sided dice:", rolls)
print("Total:", sum(rolls) if rolls else 0)
```

:::hint Stuck?
Use `random.randint(1, sides)` in a list comprehension: `[random.randint(1, sides) for _ in range(num_dice)]`
:::

:::answer Reveal answer
```python
import random

def roll_dice(num_dice, sides=6):
    """Roll num_dice dice with given number of sides."""
    return [random.randint(1, sides) for _ in range(num_dice)]

# Test
rolls = roll_dice(3)
print("Rolling 3 six-sided dice:", rolls)
print("Total:", sum(rolls) if rolls else 0)

rolls = roll_dice(2, 20)
print("Rolling 2 twenty-sided dice:", rolls)
print("Total:", sum(rolls) if rolls else 0)
```
:::

## Exercise 3: Date Calculations

Calculate how many days until a future date.

```python live
from datetime import date

def days_until(target_date):
    """Calculate days from today until target date."""
    # Your code here
    pass

# Test with New Year's Day 2025
new_year = date(2025, 1, 1)
days = days_until(new_year)
print("Days until 2025:", days)

# Test with a birthday
birthday = date(2024, 12, 25)
days = days_until(birthday)
print("Days until Dec 25:", days)
```

:::hint Stuck?
Get today with `date.today()`, then subtract: `(target_date - today).days`.
:::

:::answer Reveal answer
```python
from datetime import date

def days_until(target_date):
    """Calculate days from today until target date."""
    today = date.today()
    return (target_date - today).days

# Test with New Year's Day 2025
new_year = date(2025, 1, 1)
days = days_until(new_year)
print("Days until 2025:", days)

# Test with a birthday
birthday = date(2024, 12, 25)
days = days_until(birthday)
print("Days until Dec 25:", days)
```
:::

## Exercise 4: Choose Import Style

Rewrite this code using different import styles.

```python live
# Original - full import
import math
area = math.pi * 5 ** 2
print("Area:", round(area, 2))

# Version 1: Import just pi
# from math import pi
# area = ?

# Version 2: Import with alias
# import math as m
# area = ?

# Which style do you prefer and why?
```

:::expected_output
Area: 78.54
:::

:::answer Reveal answer
```python
# Version 1: Import just pi
from math import pi
area = pi * 5 ** 2
print("Area:", round(area, 2))

# Version 2: Import with alias
import math as m
area = m.pi * 5 ** 2
print("Area:", round(area, 2))

# All three styles produce the same result.
# - "import math" is best when using many math functions
# - "from math import pi" is best when you only need one thing
# - "import math as m" is best for shortening long module names
```
:::

## Exercise 5: Build a Simple Tool

Create a password generator using random module.

```python live
import random

def generate_password(length=8, include_numbers=True, include_special=False):
    """Generate a random password."""
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    special = "!@#$%^&*"

    # Build character pool
    chars = letters
    # Add numbers if requested
    # Add special if requested

    # Generate password
    # Your code here
    pass

# Test
print("Basic:", generate_password())
print("With numbers:", generate_password(10, True))
print("With special:", generate_password(12, True, True))
```

:::hint Stuck?
Build the `chars` string based on parameters, then use `random.choice(chars)` in a loop or comprehension to generate the password.
:::

:::answer Reveal answer
```python
import random

def generate_password(length=8, include_numbers=True, include_special=False):
    """Generate a random password."""
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    special = "!@#$%^&*"

    # Build character pool
    chars = letters
    if include_numbers:
        chars += numbers
    if include_special:
        chars += special

    # Generate password
    password = ""
    for _ in range(length):
        password += random.choice(chars)
    return password

# Test
print("Basic:", generate_password())
print("With numbers:", generate_password(10, True))
print("With special:", generate_password(12, True, True))
```
:::

