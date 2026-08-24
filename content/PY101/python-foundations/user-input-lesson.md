---
title: "Getting User Input"
slug: user-input-lesson
description: "Learn to capture and convert user input in Python"
course_id: PY101
module: python-foundations
module_order: 1
topic: user-input
topic_order: 8
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - variables-types-lesson
  - string-formatting-lesson
skills:
  - input
  - type-conversion
outcomes:
  - "Use input() to capture text from users"
  - "Convert string input to numbers with int() and float()"
  - "Handle basic input scenarios"
capstone_relevance: "Capture user data entries and menu selections in your application"
---

## Introduction

Interactive programs need user input. Python's `input()` function pauses the program and waits for the user to type something. This is how you make programs that respond to users.

## The input() Function

`input()` displays a prompt and returns what the user types:

```python live
name = input("What is your name? ")
print(f"Hello, {name}!")
```

## Try It

```python live
color = input("What is your favorite color? ")
print(f"Nice! {color} is a great color.")
```

## Input Always Returns a String

Even if the user types a number, `input()` returns it as text:

```python live
age = input("Enter your age: ")
print(f"Type of age: {type(age)}")
print(f"You are {age} years old.")
```

Notice the type is `str`, not `int`.

## Converting to Numbers

Use `int()` or `float()` to convert input to numbers:

```python live
age_text = input("Enter your age: ")
age = int(age_text)
print(f"In 10 years you'll be {age + 10}")
```

Or do it in one line:

```python live
price = float(input("Enter price: "))
tax = price * 0.08
print(f"Tax: ${tax:.2f}")
```

## Type Conversion Functions

| Function | Converts to | Example |
|----------|-------------|---------|
| `int()` | Integer | `int("42")` → `42` |
| `float()` | Decimal | `float("3.14")` → `3.14` |
| `str()` | String | `str(42)` → `"42"` |

## Building a Simple Calculator

```python live
num1 = float(input("First number: "))
num2 = float(input("Second number: "))

print(f"Sum: {num1 + num2}")
print(f"Product: {num1 * num2}")
```

## Combining Input with String Methods

Clean up user input immediately:

```python live
answer = input("Continue? (yes/no): ").strip().lower()
print(f"You entered: '{answer}'")
```

This handles variations like "  YES  " or "Yes".

## Multi-Step Input

Build a complete interaction:

```python live
print("=== Registration ===")
name = input("Your name: ")
email = input("Your email: ")
age = int(input("Your age: "))

print()
print("=== Confirmation ===")
print(f"Name: {name}")
print(f"Email: {email}")
print(f"Age: {age}")
```

## Key Points

- `input(prompt)` displays a message and waits for user input
- Input is always returned as a string
- Use `int()` to convert to whole numbers
- Use `float()` to convert to decimal numbers
- Clean input with `.strip().lower()` for consistency
- Invalid conversions cause errors (covered in Error Handling module)

:::hint Common Mistake
Trying to do math with input directly: `input("age: ") + 5` fails because you can't add a string to a number. Convert first: `int(input("age: ")) + 5`.
:::
