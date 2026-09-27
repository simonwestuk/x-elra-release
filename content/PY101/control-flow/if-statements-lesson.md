---
title: "If Statements"
slug: if-statements-lesson
description: "Learn to make decisions in your code with if statements"
course_id: PY101
module: control-flow
module_order: 2
topic: if-statements
topic_order: 3
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - comparisons-lesson
  - booleans-lesson
skills:
  - control-flow
  - if-else
outcomes:
  - "Write if statements with proper indentation"
  - "Execute code conditionally based on conditions"
  - "Understand code block structure"
capstone_relevance: "Control application flow based on user choices and data values"
---

## Introduction

If statements let your program make decisions. Code inside an if block only runs when the condition is True. This is how programs respond differently to different situations.

## Basic If Statement

```python
if condition:
    # code runs if condition is True
```

The colon `:` and indentation are required!

## Try It

```python live
age = 20

if age >= 18:
    print("You are an adult")
    print("You can vote")

print("Program continues...")
```

:::expected_output
You are an adult
You can vote
Program continues...
:::

Change `age` to 15 and run again to see the difference.

## Indentation Matters

Python uses indentation (spaces) to define code blocks:

```python live
temperature = 35

if temperature > 30:
    print("It's hot outside!")
    print("Stay hydrated!")
    print("Wear sunscreen!")

print("This always prints")
```

:::expected_output
It's hot outside!
Stay hydrated!
Wear sunscreen!
This always prints
:::

Everything indented under `if` is part of the block.

## Condition Examples

Any expression that returns True/False can be a condition:

```python live
# Comparison
score = 85
if score >= 70:
    print("You passed!")

# Boolean variable
is_member = True
if is_member:
    print("Welcome back, member!")

# Truthiness
name = "Alice"
if name:  # Non-empty string is truthy
    print(f"Hello, {name}!")
```

:::expected_output
You passed!
Welcome back, member!
Hello, Alice!
:::

## Multiple Statements in a Block

```python live
balance = 150
withdrawal = 100

if balance >= withdrawal:
    print("Processing withdrawal...")
    balance = balance - withdrawal
    print(f"Withdrew ${withdrawal}")
    print(f"New balance: ${balance}")
```

:::expected_output
Processing withdrawal...
Withdrew $100
New balance: $50
:::

## Nested If Statements

You can put if statements inside other if statements:

```python live
age = 25
has_license = True

if age >= 18:
    print("Old enough to drive")
    if has_license:
        print("You can rent a car!")
```

:::expected_output
Old enough to drive
You can rent a car!
:::

## Empty Blocks (pass)

If you need a placeholder if block, use `pass`:

```python live
condition = True

if condition:
    pass  # TODO: implement later

print("Code continues")
```

:::expected_output
Code continues
:::

## Key Points

- `if condition:` starts a conditional block
- End the line with a colon `:`
- Indent the code block (4 spaces is standard)
- The block only runs if condition is True
- Use `pass` for empty blocks

:::hint Common Mistake
Forgetting the colon after the condition, or not indenting the code block. Both will cause errors.
:::
