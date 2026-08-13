---
title: "Understanding Exceptions"
slug: exceptions-lesson
description: "Learn about runtime errors and common exception types"
course_id: PY101
module: error-handling
module_order: 5
topic: exceptions
topic_order: 2
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - syntax-errors-lesson
skills:
  - debugging
  - errors
  - exceptions
outcomes:
  - "Understand the difference between syntax errors and exceptions"
  - "Recognize common exception types"
  - "Read and understand exception messages"
capstone_relevance: "Understanding exceptions helps build robust applications"
---

## Introduction

**Exceptions** are errors that happen while your program is running. Unlike syntax errors (which Python catches before running), exceptions occur during execution when something unexpected happens.

## Syntax Errors vs Exceptions

| Syntax Errors | Exceptions |
|---------------|------------|
| Caught before running | Happen while running |
| Code structure is wrong | Code logic causes error |
| Python can't parse the code | Python can't complete an operation |

## Common Exception Types

### NameError

Occurs when you use a variable that doesn't exist:

```python live
# This will cause a NameError
print(undefined_variable)
```

### TypeError

Occurs when you use the wrong type:

```python live
# Can't add string and number
result = "hello" + 5
```

### ValueError

Occurs when a value is inappropriate:

```python live
# Can't convert "hello" to a number
number = int("hello")
```

### ZeroDivisionError

Occurs when dividing by zero:

```python live
# Division by zero is undefined
result = 10 / 0
```

### IndexError

Occurs when accessing a list index that doesn't exist:

```python live
# List only has indices 0, 1, 2
fruits = ["apple", "banana", "cherry"]
print(fruits[10])
```

### KeyError

Occurs when accessing a dictionary key that doesn't exist:

```python live
# "age" key doesn't exist
person = {"name": "Alice"}
print(person["age"])
```

## Reading Exception Messages

Exception messages have valuable information:

```
Traceback (most recent call last):
  File "example.py", line 3, in <module>
    result = 10 / 0
ZeroDivisionError: division by zero
```

| Part | Meaning |
|------|---------|
| Traceback | Shows where error occurred |
| File, line | Location of error |
| Code line | The actual problematic code |
| Exception type | `ZeroDivisionError` |
| Message | `division by zero` |

## When Exceptions Happen

```python live
print("Step 1")
print("Step 2")
result = 10 / 0  # Exception here - program stops
print("Step 3")  # This never runs
```

When an exception occurs, Python stops executing and shows the error.

## Exceptions in Functions

Exceptions show the full call stack:

```python live
def calculate(x, y):
    return x / y

def process():
    result = calculate(10, 0)
    return result

process()
```

The traceback shows each function call leading to the error.

## Why Exceptions Are Useful

Exceptions tell you:
- **What** went wrong (exception type)
- **Where** it went wrong (line number)
- **Why** it went wrong (error message)

## Common Scenarios

```python live
# User input can cause exceptions
user_input = "abc"
try:
    number = int(user_input)
except ValueError:
    print("That's not a valid number!")
```

:::expected_output
That's not a valid number!
:::

## Key Points

- Exceptions are runtime errors (happen while code runs)
- Different exception types indicate different problems
- Error messages tell you type, location, and cause
- Unhandled exceptions stop your program
- In the next lesson, you'll learn to handle exceptions gracefully

:::hint Remember
Each exception type tells you what went wrong. `TypeError` = wrong type, `ValueError` = bad value, `NameError` = unknown name, etc.
:::

