---
title: "Comments and Code Readability"
slug: comments-lesson
description: "Learn to write comments that explain your code to others and your future self"
course_id: PY101
module: python-foundations
module_order: 1
topic: comments
topic_order: 2
type: lesson
difficulty: beginner
estimated_minutes: 8
prerequisites:
  - print-basics-lesson
skills:
  - foundations
  - comments
outcomes:
  - "Write single-line comments using #"
  - "Explain the purpose of comments in code"
  - "Use comments to organize and document code"
capstone_relevance: "Good comments make your capstone code maintainable and easier to debug"
---

## Introduction

Comments are notes you write in your code for humans to read. Python ignores them completely when running your program. They're essential for explaining what your code does and why.

## Single-Line Comments

Start a comment with the `#` symbol. Everything after `#` on that line is ignored:

```python
# This is a comment
print("Hello")  # This comment is at the end of a line
```

## Try It

Run this code. Notice the comments don't appear in the output:

```python live
# Display a greeting
print("Welcome!")

# This line is ignored by Python
print("Goodbye!")  # So is this part
```

:::expected_output
Welcome!
Goodbye!
:::

## Why Use Comments?

Comments help you and others understand code:

```python live
# Calculate the total price with tax
price = 100
tax_rate = 0.08
total = price + (price * tax_rate)
print(total)
```

:::expected_output
108.0
:::

Without the comment, someone reading this code might not immediately know what the calculation represents.

## Commenting Out Code

You can temporarily disable code by putting `#` in front of it:

```python live
print("This line runs")
# print("This line is commented out")
print("This line also runs")
```

:::expected_output
This line runs
This line also runs
:::

This is useful when testing or debugging.

## Organizing Code with Comments

Use comments as section headers:

```python live
# --- Setup ---
name = "Alice"
age = 25

# --- Display Info ---
print("Name:", name)
print("Age:", age)

# --- End of Program ---
print("Done!")
```

:::expected_output
Name: Alice
Age: 25
Done!
:::

## Good vs Bad Comments

**Good comments** explain *why*, not *what*:

```python
# Convert to cents to avoid floating point errors
total_cents = dollars * 100
```

**Bad comments** state the obvious:

```python
# Set x to 5
x = 5
```

## Key Points

- Comments start with `#`
- Python ignores all comment text
- Use comments to explain *why* code exists
- Comments help others (and future you) understand code
- You can comment out code to temporarily disable it

:::hint Common Mistake
Don't over-comment obvious code. `x = 5  # set x to 5` adds no value. Comment on the purpose, not the mechanics.
:::
