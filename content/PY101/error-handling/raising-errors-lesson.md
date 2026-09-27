---
title: "Raising Exceptions"
slug: raising-errors-lesson
description: "Learn to raise your own exceptions for error signaling"
course_id: PY101
module: error-handling
module_order: 5
topic: raising-errors
topic_order: 4
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - try-except-lesson
skills:
  - errors
  - exceptions
outcomes:
  - "Raise exceptions with the raise statement"
  - "Choose appropriate exception types"
  - "Write descriptive error messages"
capstone_relevance: "Input validation often requires raising exceptions"
---

## Introduction

Sometimes you want to signal that something went wrong in your own code. The `raise` statement lets you create exceptions to indicate errors. This is useful for input validation and enforcing requirements.

## Basic Raise

```python live
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

try:
    result = divide(10, 0)
except ValueError as e:
    print("Error:", e)
```

:::expected_output
Error: Cannot divide by zero!
:::

The `raise` statement creates an exception with your custom message.

## Why Raise Exceptions?

1. **Signal invalid input** - Tell callers their data is wrong
2. **Enforce requirements** - Ensure conditions are met
3. **Stop invalid operations** - Prevent bad state
4. **Communicate errors** - Clear error messages

## Choosing Exception Types

Use appropriate built-in exception types:

```python live
def process_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return "Valid age: " + str(age)

# Test with different inputs
test_cases = [25, -5, 200, "thirty"]
for test in test_cases:
    try:
        result = process_age(test)
        print(result)
    except (TypeError, ValueError) as e:
        print("Error:", e)
```

:::expected_output
Valid age: 25
Error: Age cannot be negative
Error: Age seems unrealistic
Error: Age must be an integer
:::

## Common Exception Types to Raise

| Exception | When to Use |
|-----------|-------------|
| `ValueError` | Value is wrong (out of range, invalid format) |
| `TypeError` | Wrong type passed |
| `RuntimeError` | General runtime problem |
| `NotImplementedError` | Feature not yet built |

## Input Validation

```python live
def create_user(name, age, email):
    """Create a user with validated data."""
    # Validate name
    if not name:
        raise ValueError("Name cannot be empty")
    if len(name) < 2:
        raise ValueError("Name must be at least 2 characters")

    # Validate age
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150")

    # Validate email (simple check)
    if "@" not in email:
        raise ValueError("Email must contain @")

    return {"name": name, "age": age, "email": email}

# Test valid user
try:
    user = create_user("Alice", 30, "alice@email.com")
    print("Created:", user)
except (ValueError, TypeError) as e:
    print("Error:", e)

# Test invalid user
try:
    user = create_user("", 30, "alice@email.com")
    print("Created:", user)
except (ValueError, TypeError) as e:
    print("Error:", e)
```

:::expected_output
Created: {'name': 'Alice', 'age': 30, 'email': 'alice@email.com'}
Error: Name cannot be empty
:::

## Raising with Context

Include helpful information in your error messages:

```python live
def get_item(items, index):
    if index < 0 or index >= len(items):
        raise IndexError(
            "Index " + str(index) + " is out of range. " +
            "Valid range: 0 to " + str(len(items) - 1)
        )
    return items[index]

fruits = ["apple", "banana", "cherry"]
try:
    print(get_item(fruits, 10))
except IndexError as e:
    print("Error:", e)
```

:::expected_output
Error: Index 10 is out of range. Valid range: 0 to 2
:::

## Re-raising Exceptions

Sometimes you want to catch an exception, do something, then re-raise it:

```python live
def process_data(data):
    try:
        # Some processing
        if data < 0:
            raise ValueError("Negative data")
        return data * 2
    except ValueError:
        print("Logging: Invalid data received")
        raise  # Re-raise the same exception

try:
    process_data(-5)
except ValueError as e:
    print("Caught in outer handler:", e)
```

:::expected_output
Logging: Invalid data received
Caught in outer handler: Negative data
:::

## Guard Clauses

Use `raise` early to validate inputs (guard clause pattern):

```python live
def calculate_bmi(weight, height):
    """Calculate BMI with input validation."""
    # Guard clauses - validate first
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if height <= 0:
        raise ValueError("Height must be positive")

    # Main logic (only reached with valid input)
    bmi = weight / (height ** 2)
    return round(bmi, 2)

print(calculate_bmi(70, 1.75))

try:
    print(calculate_bmi(-70, 1.75))
except ValueError as e:
    print("Error:", e)
```

:::expected_output
22.86
Error: Weight must be positive
:::

## Key Points

- Use `raise` to signal errors in your code
- Choose the appropriate exception type for the situation
- Write clear, descriptive error messages
- Validate inputs early (guard clauses)
- Include context in error messages when helpful

:::hint Best Practice
Raise exceptions at the point where you detect the problem, not later when it causes confusing errors.
:::

