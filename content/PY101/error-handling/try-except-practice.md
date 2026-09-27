---
title: "Practice: Try-Except Blocks"
slug: try-except-practice
description: "Practice handling exceptions with try-except"
course_id: PY101
module: error-handling
module_order: 5
topic: try-except
topic_order: 3
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - try-except-lesson
skills:
  - errors
  - exceptions
  - try-except
outcomes:
  - "Write try-except blocks"
  - "Handle specific exception types"
  - "Use else and finally clauses"
capstone_relevance: "Error handling is essential for user-facing applications"
---

## Exercise 1: Basic Try-Except

Wrap this code in a try-except to handle the ZeroDivisionError.

```python live
# Add try-except to handle the error
result = 10 / 0
print("Result:", result)

print("Program continues!")
```

:::expected_output
Error: Cannot divide by zero!
Program continues!
:::

:::hint Stuck?
Wrap the division in `try:` and add `except ZeroDivisionError:` to print an error message.
:::

:::answer Reveal answer
```python
# Add try-except to handle the error
try:
    result = 10 / 0
    print("Result:", result)
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")

print("Program continues!")
```
:::

## Exercise 2: Handle ValueError

Create a function `safe_int` that takes a string and returns the integer value. If conversion fails, return 0.

```python live
def safe_int(text):
    # Add try-except to handle ValueError
    return int(text)

print(safe_int("42"))     # Should print 42
print(safe_int("hello"))  # Should print 0
print(safe_int("3.14"))   # Should print 0
```

:::expected_output
42
0
0
:::

:::hint Stuck?
Wrap `int(text)` in a try block, and in the except block, return 0.
:::

:::answer Reveal answer
```python
def safe_int(text):
    # Add try-except to handle ValueError
    try:
        return int(text)
    except ValueError:
        return 0

print(safe_int("42"))     # Should print 42
print(safe_int("hello"))  # Should print 0
print(safe_int("3.14"))   # Should print 0
```
:::

## Exercise 3: Multiple Exceptions

Create a function `safe_get` that takes a list and an index, returning the item at that index. Handle both IndexError (return None) and TypeError (return None).

```python live
def safe_get(items, index):
    # Add try-except for IndexError and TypeError
    return items[index]

numbers = [10, 20, 30]
print(safe_get(numbers, 1))    # Should print 20
print(safe_get(numbers, 10))   # Should print None (IndexError)
print(safe_get(numbers, "a"))  # Should print None (TypeError)
```

:::expected_output
20
None
None
:::

:::hint Stuck?
Use `except (IndexError, TypeError):` to catch both exception types.
:::

:::answer Reveal answer
```python
def safe_get(items, index):
    # Add try-except for IndexError and TypeError
    try:
        return items[index]
    except (IndexError, TypeError):
        return None

numbers = [10, 20, 30]
print(safe_get(numbers, 1))    # Should print 20
print(safe_get(numbers, 10))   # Should print None (IndexError)
print(safe_get(numbers, "a"))  # Should print None (TypeError)
```
:::

## Exercise 4: Using Else

Create a function that divides two numbers. Use `else` to print "Division successful!" only when no error occurs.

```python live
def divide_with_message(a, b):
    # Use try-except-else
    pass

divide_with_message(10, 2)   # Should print success message and 5.0
print()
divide_with_message(10, 0)   # Should print error, no success message
```

:::expected_output
Division successful!
5.0

Error: Cannot divide by zero!
:::

:::hint Stuck?
The `else` block goes after `except` and only runs if no exception was raised.
:::

:::answer Reveal answer
```python
def divide_with_message(a, b):
    # Use try-except-else
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
    else:
        print("Division successful!")
        print(result)

divide_with_message(10, 2)   # Should print success message and 5.0
print()
divide_with_message(10, 0)   # Should print error, no success message
```
:::

## Exercise 5: Using Finally

Create a function that simulates opening and closing a resource. Use `finally` to always print "Resource closed" whether or not an error occurs.

```python live
def process_resource(should_fail):
    """Process a resource that might fail."""
    # Add try-except-finally
    print("Opening resource...")
    if should_fail:
        raise ValueError("Processing failed!")
    print("Processing complete!")

print("Test 1 - Success:")
process_resource(False)
print()
print("Test 2 - Failure:")
process_resource(True)
```

:::expected_output
Test 1 - Success:
Opening resource...
Processing complete!
Resource closed

Test 2 - Failure:
Opening resource...
Error: Processing failed!
Resource closed
:::

:::hint Stuck?
`finally:` always runs. Use it to print "Resource closed" regardless of whether an exception occurred.
:::

:::answer Reveal answer
```python
def process_resource(should_fail):
    """Process a resource that might fail."""
    # Add try-except-finally
    try:
        print("Opening resource...")
        if should_fail:
            raise ValueError("Processing failed!")
        print("Processing complete!")
    except ValueError as e:
        print("Error:", e)
    finally:
        print("Resource closed")

print("Test 1 - Success:")
process_resource(False)
print()
print("Test 2 - Failure:")
process_resource(True)
```
:::

