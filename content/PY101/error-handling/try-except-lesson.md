---
title: "Handling Exceptions with Try-Except"
slug: try-except-lesson
description: "Learn to catch and handle exceptions gracefully"
course_id: PY101
module: error-handling
module_order: 5
topic: try-except
topic_order: 3
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - exceptions-lesson
skills:
  - errors
  - exceptions
  - try-except
outcomes:
  - "Use try-except to catch exceptions"
  - "Handle specific exception types"
  - "Use else and finally clauses"
capstone_relevance: "Graceful error handling makes robust applications"
---

## Introduction

Instead of letting your program crash when an exception occurs, you can **catch** the exception and handle it gracefully. This is done using `try` and `except` blocks.

## Basic Try-Except

```python live
try:
    result = 10 / 0
except:
    print("Something went wrong!")

print("Program continues...")
```

:::expected_output
Something went wrong!
Program continues...
:::

The code in `try` runs. If an exception occurs, Python jumps to `except` instead of crashing.

## Catching Specific Exceptions

It's better to catch specific exception types:

```python live
try:
    number = int("hello")
except ValueError:
    print("That's not a valid number!")

print("Moving on...")
```

:::expected_output
That's not a valid number!
Moving on...
:::

This only catches `ValueError`. Other exceptions would still crash the program.

## Multiple Except Blocks

Handle different exceptions differently:

```python live
def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        print("Error: Invalid types for division!")
        return None

print(divide(10, 2))
print(divide(10, 0))
print(divide("10", 2))
```

:::expected_output
5.0
Error: Cannot divide by zero!
None
Error: Invalid types for division!
None
:::

## Catching Multiple Exceptions Together

```python live
try:
    value = int("abc")
except (ValueError, TypeError):
    print("Invalid input!")
```

:::expected_output
Invalid input!
:::

## The Exception Variable

Get details about the exception:

```python live
try:
    number = int("hello")
except ValueError as e:
    print("Error occurred:", e)
```

## The Else Clause

Code in `else` runs only if no exception occurred:

```python live
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    else:
        print("Division successful!")
        return result

print(safe_divide(10, 2))
print()
print(safe_divide(10, 0))
```

:::expected_output
Division successful!
5.0

Cannot divide by zero!
None
:::

## The Finally Clause

Code in `finally` ALWAYS runs, whether or not an exception occurred:

```python live
def process_data():
    print("Starting...")
    try:
        result = 10 / 2
        print("Result:", result)
    except ZeroDivisionError:
        print("Division error!")
    finally:
        print("Cleanup done!")  # Always runs

process_data()
```

:::expected_output
Starting...
Result: 5.0
Cleanup done!
:::

## Complete Structure

```python live
def safe_operation(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    except TypeError:
        print("Invalid types")
        return None
    else:
        print("Operation successful")
        return result
    finally:
        print("Operation complete")

print("Test 1:")
print(safe_operation(10, 2))
print("\nTest 2:")
print(safe_operation(10, 0))
```

:::expected_output
Test 1:
Operation successful
Operation complete
5.0

Test 2:
Cannot divide by zero
Operation complete
None
:::

## Practical Example: User Input

```python live
def get_number(prompt):
    """Keep asking until user enters a valid number."""
    while True:
        user_input = "42"  # Simulating input
        try:
            number = int(user_input)
            return number
        except ValueError:
            print("Please enter a valid number!")
            break  # In real code, would continue asking

result = get_number("Enter a number: ")
print("You entered:", result)
```

:::expected_output
You entered: 42
:::

## Practical Example: Safe Division

```python live
def calculator():
    operations = [
        (10, 2),
        (20, 0),
        (15, 3),
        ("a", 5)
    ]

    for a, b in operations:
        try:
            result = a / b
            print(str(a) + " / " + str(b) + " = " + str(result))
        except ZeroDivisionError:
            print(str(a) + " / " + str(b) + " = Error (division by zero)")
        except TypeError:
            print(str(a) + " / " + str(b) + " = Error (invalid types)")

calculator()
```

:::expected_output
10 / 2 = 5.0
20 / 0 = Error (division by zero)
15 / 3 = 5.0
a / 5 = Error (invalid types)
:::

## Key Points

- `try` contains code that might fail
- `except` handles specific exceptions
- `else` runs if no exception occurred
- `finally` always runs (cleanup)
- Always catch specific exceptions when possible
- Use `as e` to get exception details

:::hint Best Practice
Avoid bare `except:` without specifying an exception type. It catches everything, including keyboard interrupts, making bugs harder to find.
:::

