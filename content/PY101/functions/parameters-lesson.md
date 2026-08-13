---
title: "Function Parameters"
slug: parameters-lesson
description: "Learn to pass information into functions using parameters"
course_id: PY101
module: functions
module_order: 4
topic: parameters
topic_order: 2
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - defining-functions-lesson
skills:
  - functions
  - parameters
outcomes:
  - "Define functions with parameters"
  - "Pass arguments when calling functions"
  - "Use multiple parameters"
capstone_relevance: "Pass data to functions for processing and display"
---

## Introduction

Functions become much more powerful when they can accept input. **Parameters** are variables that receive values when you call a function. This lets you write flexible, reusable code.

## Function with One Parameter

```python live
def greet(name):
    print("Hello, " + name + "!")

greet("Alice")
greet("Bob")
greet("Charlie")
```

:::expected_output
Hello, Alice!
Hello, Bob!
Hello, Charlie!
:::

- `name` is the **parameter** (in the function definition)
- `"Alice"`, `"Bob"`, `"Charlie"` are **arguments** (values passed in)

## How It Works

```python
def greet(name):        # Parameter: name receives the value
    print("Hello, " + name + "!")

greet("Alice")          # Argument: "Alice" is passed to name
```

When you call `greet("Alice")`:
1. Python creates a variable `name` with value `"Alice"`
2. The function body runs with that value
3. It prints "Hello, Alice!"

## Multiple Parameters

Functions can have multiple parameters, separated by commas:

```python live
def introduce(name, age):
    print("Name: " + name)
    print("Age: " + str(age))

introduce("Alice", 25)
introduce("Bob", 30)
```

:::expected_output
Name: Alice
Age: 25
Name: Bob
Age: 30
:::

## Parameter Order Matters

Arguments are matched to parameters by position:

```python live
def describe_pet(animal, name):
    print("I have a " + animal + " named " + name)

describe_pet("dog", "Max")      # animal="dog", name="Max"
describe_pet("cat", "Whiskers") # animal="cat", name="Whiskers"
```

:::expected_output
I have a dog named Max
I have a cat named Whiskers
:::

## Using Parameters in Calculations

```python live
def calculate_area(width, height):
    area = width * height
    print("Area: " + str(area))

calculate_area(5, 3)   # 15
calculate_area(10, 4)  # 40
calculate_area(7, 7)   # 49
```

:::expected_output
Area: 15
Area: 40
Area: 49
:::

## Parameters with Conditionals

```python live
def check_age(age):
    if age >= 18:
        print("You are an adult")
    else:
        print("You are a minor")

check_age(25)
check_age(15)
check_age(18)
```

:::expected_output
You are an adult
You are a minor
You are an adult
:::

## Reusing Functions

The power of parameters is reusability:

```python live
def print_box(text):
    length = len(text) + 4
    print("+" + "-" * length + "+")
    print("|  " + text + "  |")
    print("+" + "-" * length + "+")

print_box("Hello")
print()
print_box("Python is fun!")
print()
print_box("Parameters rock!")
```

:::expected_output
+---------+
|  Hello  |
+---------+

+------------------+
|  Python is fun!  |
+------------------+

+--------------------+
|  Parameters rock!  |
+--------------------+
:::

## Named Arguments

You can specify which parameter gets which value:

```python live
def create_profile(name, age, city):
    print("Name: " + name)
    print("Age: " + str(age))
    print("City: " + city)

# Using named arguments (any order)
create_profile(city="London", name="Alice", age=25)
```

:::expected_output
Name: Alice
Age: 25
City: London
:::

## Key Points

- Parameters are variables that receive values when called
- Arguments are the actual values passed to the function
- Multiple parameters are separated by commas
- Order matters unless you use named arguments
- Parameters make functions reusable with different data

:::hint Common Mistake
Forgetting to pass an argument causes an error. If your function needs a value, you must provide it when calling.
:::

