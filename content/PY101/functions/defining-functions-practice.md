---
title: "Practice: Defining Functions"
slug: defining-functions-practice
description: "Practice creating and calling your own functions"
course_id: PY101
module: functions
module_order: 4
topic: defining-functions
topic_order: 1
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - defining-functions-lesson
skills:
  - functions
outcomes:
  - "Define functions independently"
  - "Call functions correctly"
  - "Organize code into functions"
capstone_relevance: "Functions are the building blocks of your application"
---

## Exercise 1: Create a Greeting

Define a function called `greet` that prints "Hello there!".

```python live
# Define the greet function


# Call it
greet()
```

:::expected_output
Hello there!
:::

:::hint Stuck?
Use `def greet():` followed by an indented print statement.
:::

:::answer Reveal answer
```python
def greet():
    print("Hello there!")

# Call it
greet()
```
:::

## Exercise 2: Display a Border

Create a function called `print_border` that prints a line of 25 asterisks.

```python live
# Define the function


# Call it twice
print_border()
print("Content")
print_border()
```

:::expected_output
*************************
Content
*************************
:::

:::hint Stuck?
Use `print("*" * 25)` inside your function body.
:::

:::answer Reveal answer
```python
def print_border():
    print("*" * 25)

# Call it twice
print_border()
print("Content")
print_border()
```
:::

## Exercise 3: Welcome Message

Create a function called `welcome` that prints three lines:
- "========================"
- "Welcome to My Program"
- "========================"

```python live
# Define the welcome function


# Call it
welcome()
```

:::expected_output
========================
Welcome to My Program
========================
:::

:::hint Stuck?
Your function needs three print() statements inside it.
:::

:::answer Reveal answer
```python
def welcome():
    print("========================")
    print("Welcome to My Program")
    print("========================")

# Call it
welcome()
```
:::

## Exercise 4: Menu Display

Create a function called `show_options` that displays:
```
1. Start
2. Settings
3. Quit
```

```python live
# Define the function


# Call it
print("Main Menu")
show_options()
```

:::expected_output
Main Menu
1. Start
2. Settings
3. Quit
:::

:::hint Stuck?
Define the function with three print statements, one for each menu option.
:::

:::answer Reveal answer
```python
def show_options():
    print("1. Start")
    print("2. Settings")
    print("3. Quit")

# Call it
print("Main Menu")
show_options()
```
:::

## Exercise 5: Full Program Structure

Create three functions:
- `header()` - prints "=== MY APP ==="
- `content()` - prints "Welcome!" and "This is my program."
- `footer()` - prints "=== END ==="

Then call all three in order.

```python live
# Define all three functions


# Call them in order

```

:::expected_output
=== MY APP ===
Welcome!
This is my program.
=== END ===
:::

:::hint Stuck?
Define each function separately, then call them: `header()`, `content()`, `footer()`.
:::

:::answer Reveal answer
```python
def header():
    print("=== MY APP ===")

def content():
    print("Welcome!")
    print("This is my program.")

def footer():
    print("=== END ===")

# Call them in order
header()
content()
footer()
```
:::

