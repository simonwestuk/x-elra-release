---
title: "Challenge: Build a Robust Calculator"
slug: try-except-challenge
description: "Create a calculator that handles all errors gracefully"
course_id: PY101
module: error-handling
module_order: 5
topic: try-except
topic_order: 3
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - try-except-practice
skills:
  - errors
  - exceptions
  - try-except
outcomes:
  - "Build robust error-handling systems"
  - "Handle multiple error scenarios"
  - "Create user-friendly error messages"
capstone_relevance: "Robust error handling is essential for any application"
---

## Challenge: Robust Expression Calculator

Build a calculator that can evaluate simple expressions and handle ALL errors gracefully.

### Requirements

1. Create `parse_number(text)`:
   - Converts string to float
   - Returns `None` if invalid, with appropriate message

2. Create `calculate(num1, num2, operator)`:
   - Supports: `+`, `-`, `*`, `/`
   - Handles division by zero
   - Handles invalid operators
   - Returns result or error message

3. Create `evaluate_expression(expression)`:
   - Takes a string like "10 + 5"
   - Parses the numbers and operator
   - Returns the result or error message
   - Handles malformed expressions

### Your Solution

```python live
def parse_number(text):
    """
    Convert text to a number.
    Returns tuple (success, value_or_error)
    """
    # Handle conversion with try-except
    pass

def calculate(num1, num2, operator):
    """
    Perform calculation with error handling.
    Returns tuple (success, value_or_error)
    """
    # Handle all possible errors
    pass

def evaluate_expression(expression):
    """
    Evaluate a simple expression like "10 + 5".
    Returns a user-friendly result string.
    """
    # Parse and calculate with full error handling
    pass


# Test the calculator
expressions = [
    "10 + 5",      # Should work: 15.0
    "20 - 8",      # Should work: 12.0
    "6 * 7",       # Should work: 42.0
    "100 / 4",     # Should work: 25.0
    "10 / 0",      # Error: division by zero
    "abc + 5",     # Error: invalid number
    "10 + xyz",    # Error: invalid number
    "10 % 3",      # Error: invalid operator
    "hello",       # Error: invalid expression format
    "10 +",        # Error: invalid expression format
]

print("=== Calculator Test ===")
for expr in expressions:
    result = evaluate_expression(expr)
    print(expr + " -> " + str(result))
```

:::expected_output
=== Calculator Test ===
10 + 5 -> 15.0
20 - 8 -> 12.0
6 * 7 -> 42.0
100 / 4 -> 25.0
10 / 0 -> Error: Cannot divide by zero
abc + 5 -> Error: 'abc' is not a valid number
10 + xyz -> Error: 'xyz' is not a valid number
10 % 3 -> Error: Unknown operator '%'
hello -> Error: Invalid expression format
10 + -> Error: Invalid expression format
:::

### Expected Output

```
=== Calculator Test ===
10 + 5 -> 15.0
20 - 8 -> 12.0
6 * 7 -> 42.0
100 / 4 -> 25.0
10 / 0 -> Error: Cannot divide by zero
abc + 5 -> Error: 'abc' is not a valid number
10 + xyz -> Error: 'xyz' is not a valid number
10 % 3 -> Error: Unknown operator '%'
hello -> Error: Invalid expression format
10 + -> Error: Invalid expression format
```

:::hint Parsing Expression
Split the expression by spaces: `parts = expression.split()`. If you don't get exactly 3 parts, it's invalid.
:::

:::hint Number Parsing
Use try-except around `float(text)`. Catch `ValueError` for invalid numbers.
:::

:::hint Calculator Logic
Use if-elif for operators. For division, check if second number is zero before dividing.
:::

:::hint Return Format
Consider returning tuples like `(True, result)` or `(False, error_message)` to indicate success/failure.
:::

:::answer Reveal full solution
```python
def parse_number(text):
    """
    Convert text to a number.
    Returns tuple (success, value_or_error)
    """
    try:
        return (True, float(text))
    except ValueError:
        return (False, "'" + text + "' is not a valid number")

def calculate(num1, num2, operator):
    """
    Perform calculation with error handling.
    Returns tuple (success, value_or_error)
    """
    if operator == "+":
        return (True, num1 + num2)
    elif operator == "-":
        return (True, num1 - num2)
    elif operator == "*":
        return (True, num1 * num2)
    elif operator == "/":
        if num2 == 0:
            return (False, "Cannot divide by zero")
        return (True, num1 / num2)
    else:
        return (False, "Unknown operator '" + operator + "'")

def evaluate_expression(expression):
    """
    Evaluate a simple expression like "10 + 5".
    Returns a user-friendly result string.
    """
    parts = expression.split()
    if len(parts) != 3:
        return "Error: Invalid expression format"

    left, operator, right = parts

    success1, result1 = parse_number(left)
    if not success1:
        return "Error: " + result1

    success2, result2 = parse_number(right)
    if not success2:
        return "Error: " + result2

    success, result = calculate(result1, result2, operator)
    if not success:
        return "Error: " + result

    return result


# Test the calculator
expressions = [
    "10 + 5",      # Should work: 15.0
    "20 - 8",      # Should work: 12.0
    "6 * 7",       # Should work: 42.0
    "100 / 4",     # Should work: 25.0
    "10 / 0",      # Error: division by zero
    "abc + 5",     # Error: invalid number
    "10 + xyz",    # Error: invalid number
    "10 % 3",      # Error: invalid operator
    "hello",       # Error: invalid expression format
    "10 +",        # Error: invalid expression format
]

print("=== Calculator Test ===")
for expr in expressions:
    result = evaluate_expression(expr)
    print(expr + " -> " + str(result))
```
:::

