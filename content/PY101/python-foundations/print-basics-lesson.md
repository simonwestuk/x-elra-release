---
title: "Your First Python Program"
slug: print-basics-lesson
description: "Learn to write and run your first Python program using the print() function"
course_id: PY101
module: python-foundations
module_order: 1
topic: print-basics
topic_order: 1
type: lesson
difficulty: beginner
estimated_minutes: 10
prerequisites: []
skills:
  - foundations
  - print
outcomes:
  - "Write a Python program that displays text"
  - "Use print() to output messages to the screen"
  - "Understand how Python executes code line by line"
capstone_relevance: "You'll use print() to display menus, confirmations, and data to users"
---

## Introduction

Every programmer starts by making the computer say "Hello, World!" This tradition has been around for over 50 years. Today, you'll write your first Python program.

Python is a programming language that lets you give instructions to a computer. The `print()` function is how you tell Python to display something on the screen.

## The print() Function

To display text in Python, use `print()` with your message inside quotation marks:

```python
print("Hello, World!")
```

When Python runs this code, it displays:
```
Hello, World!
```

## Try It

Run this code to see your first program in action:

```python live
print("Hello, World!")
```

:::expected_output
Hello, World!
:::

## Multiple Print Statements

You can have multiple print statements. Python runs them one after another, from top to bottom:

```python live
print("Line 1")
print("Line 2")
print("Line 3")
```

:::expected_output
Line 1
Line 2
Line 3
:::

Each `print()` creates a new line in the output.

## Printing Different Messages

The text inside the quotes can be anything you want:

```python live
print("Welcome to Python!")
print("This is fun.")
print("I am learning to code.")
```

:::expected_output
Welcome to Python!
This is fun.
I am learning to code.
:::

## Single vs Double Quotes

Python accepts both single quotes `'...'` and double quotes `"..."` for text:

```python live
print('Using single quotes')
print("Using double quotes")
```

:::expected_output
Using single quotes
Using double quotes
:::

Both work the same way. Pick one style and be consistent.

## Empty Print

Calling `print()` with nothing inside creates a blank line:

```python live
print("Before the gap")
print()
print("After the gap")
```

:::expected_output
Before the gap

After the gap
:::

This is useful for adding space in your output.

## Key Points

- `print()` displays text on the screen
- Put your text inside quotation marks
- Each `print()` statement creates a new line
- Python runs code from top to bottom
- Single quotes and double quotes both work

:::hint Common Mistake
Forgetting the quotation marks causes an error. Always wrap your text in quotes: `print("Hello")` not `print(Hello)`.
:::
