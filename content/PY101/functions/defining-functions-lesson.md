---
title: "Defining Functions"
slug: defining-functions-lesson
description: "Learn to create reusable code with function definitions"
course_id: PY101
module: functions
module_order: 4
topic: defining-functions
topic_order: 1
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - variables-types-lesson
  - if-statements-lesson
skills:
  - functions
outcomes:
  - "Define functions with the def keyword"
  - "Call functions correctly"
  - "Understand function structure"
capstone_relevance: "Organize your application into reusable functions"
---

## Introduction

Functions are reusable blocks of code. Instead of writing the same code over and over, you define it once in a function and call it whenever needed. Functions make your code organized, readable, and maintainable.

## Defining a Function

Use the `def` keyword:

```python
def function_name():
    # code goes here
```

```python live
def greet():
    print("Hello!")
    print("Welcome to Python!")

# Call the function
greet()
```

:::expected_output
Hello!
Welcome to Python!
:::

## Function Structure

```python
def say_hello():       # 1. def keyword + name + parentheses + colon
    print("Hello!")    # 2. Indented body
    print("Hi there!") # 3. Can have multiple lines
                       # 4. Function ends when indentation ends

say_hello()            # Call the function by its name
```

## Calling Functions Multiple Times

```python live
def display_separator():
    print("=" * 30)

display_separator()
print("SECTION 1")
display_separator()
print("SECTION 2")
display_separator()
```

:::expected_output
==============================
SECTION 1
==============================
SECTION 2
==============================
:::

## Functions with Logic

```python live
def check_temperature():
    temp = 35
    if temp > 30:
        print("It's hot!")
    else:
        print("It's nice outside")

check_temperature()
```

:::expected_output
It's hot!
:::

## Order Matters

Define functions before calling them:

```python live
# Define first
def show_menu():
    print("1. View items")
    print("2. Add item")
    print("3. Exit")

# Then call
print("=== Main Menu ===")
show_menu()
```

:::expected_output
=== Main Menu ===
1. View items
2. Add item
3. Exit
:::

## Naming Functions

Use lowercase with underscores (snake_case):

```python
# Good names
calculate_total()
display_menu()
get_user_input()
validate_email()

# Avoid
CalculateTotal()   # PascalCase is for classes
calculate-total()  # Hyphens not allowed
```

## Functions Calling Functions

```python live
def print_header():
    print("=" * 20)
    print("  MY PROGRAM")
    print("=" * 20)

def print_footer():
    print("-" * 20)
    print("  Goodbye!")
    print("-" * 20)

def run_program():
    print_header()
    print("Main content here...")
    print_footer()

run_program()
```

:::expected_output
====================
  MY PROGRAM
====================
Main content here...
--------------------
  Goodbye!
--------------------
:::

## Key Points

- Functions are defined with `def function_name():`
- Function body must be indented
- Call functions by name with parentheses: `function_name()`
- Define functions before calling them
- Use descriptive names in snake_case

:::hint Common Mistake
Forgetting to call the function. `def greet()` just defines it; you need `greet()` to run it.
:::
