---
title: "Challenge: Debug the Calculator"
slug: syntax-errors-challenge
description: "Fix all syntax errors in a broken calculator program"
course_id: PY101
module: error-handling
module_order: 5
topic: syntax-errors
topic_order: 1
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - syntax-errors-practice
skills:
  - debugging
  - errors
outcomes:
  - "Debug complex code with multiple errors"
  - "Systematically find and fix issues"
  - "Test fixes thoroughly"
capstone_relevance: "Debugging multi-part programs is a key skill"
---

## Challenge: Fix the Calculator

This calculator program has **6 syntax errors**. Find and fix all of them to make the program work.

### The Broken Code

```python live
# This calculator has 6 syntax errors - fix them all!

def add(a, b)
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a.'
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    result = a * b
return result

def divide(a, b):
    """Divide a by b."""
    if b == 0
        return "Error: Division by zero"
    return a / b

def calculator():
    """Run the calculator."""
    print("=== Simple Calculator ===")
    print("5 + 3 =", add(5, 3)
    print("10 - 4 =", subtract(10, 4))
    print("6 * 7 =", multiply(6, 7))
    print("20 / 4 =", divide(20, 4))
    print("10 / 0 =", divide(10, 0))
    print("=== Done ===")

calculator()
```

:::expected_output
=== Simple Calculator ===
5 + 3 = 8
10 - 4 = 6
6 * 7 = 42
20 / 4 = 5.0
10 / 0 = Error: Division by zero
=== Done ===
:::

### Expected Output (after fixing)

```
=== Simple Calculator ===
5 + 3 = 8
10 - 4 = 6
6 * 7 = 42
20 / 4 = 5.0
10 / 0 = Error: Division by zero
=== Done ===
```

### Hints

:::hint Error Count
There are exactly 6 syntax errors. Keep looking until you've found and fixed all of them.
:::

:::hint Systematic Approach
Start at the top and work down. Run the code after each fix to see if more errors appear.
:::

:::hint Common Issues
Look for: missing colons, mismatched quotes, indentation problems, and missing parentheses.
:::

:::answer Reveal full solution
```python
# This calculator has 6 syntax errors - fix them all!

def add(a, b):  # Fix 1: Added missing colon
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""  # Fix 2: Changed closing ' to "
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    result = a * b
    return result  # Fix 3: Fixed indentation (added 4 spaces)

def divide(a, b):
    """Divide a by b."""
    if b == 0:  # Fix 4: Added missing colon
        return "Error: Division by zero"
    return a / b

def calculator():
    """Run the calculator."""
    print("=== Simple Calculator ===")
    print("5 + 3 =", add(5, 3))  # Fix 5: Added missing closing parenthesis
    print("10 - 4 =", subtract(10, 4))
    print("6 * 7 =", multiply(6, 7))
    print("20 / 4 =", divide(20, 4))
    print("10 / 0 =", divide(10, 0))
    print("=== Done ===")

calculator()
```
:::

