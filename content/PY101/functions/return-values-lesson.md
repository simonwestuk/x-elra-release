---
title: "Return Values"
slug: return-values-lesson
description: "Learn to get results back from functions using return"
course_id: PY101
module: functions
module_order: 4
topic: return-values
topic_order: 3
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - parameters-lesson
skills:
  - functions
  - return-values
outcomes:
  - "Use return to send values back from functions"
  - "Store returned values in variables"
  - "Understand the difference between print and return"
capstone_relevance: "Return values for calculations and data retrieval"
---

## Introduction

So far, our functions have printed output but haven't given us anything back to work with. The `return` statement sends a value back to the code that called the function. This is incredibly powerful for calculations, data processing, and building reusable code.

## The return Statement

```python live
def add(a, b):
    return a + b

result = add(5, 3)
print("The sum is:", result)
```

:::expected_output
The sum is: 8
:::

The function calculates `a + b` and sends that value back. We store it in `result`.

## Print vs Return

```python live
# With print - just displays
def add_print(a, b):
    print(a + b)

# With return - gives back a value
def add_return(a, b):
    return a + b

# Print version - can't use the result
add_print(5, 3)

# Return version - can use the result
answer = add_return(5, 3)
print("Answer:", answer)
print("Doubled:", answer * 2)
```

:::expected_output
8
Answer: 8
Doubled: 16
:::

**Key difference**: `print` shows output; `return` gives back a value you can use.

## Using Returned Values

You can use returned values in many ways:

```python live
def square(n):
    return n * n

# Store in a variable
result = square(5)
print(result)

# Use directly in expressions
print(square(4) + square(3))

# Use in conditions
if square(5) > 20:
    print("That's a big square!")
```

:::expected_output
25
25
That's a big square!
:::

## Returning Different Types

Functions can return any type:

```python live
# Return a number
def calculate_tax(amount):
    return amount * 0.2

# Return a string
def get_greeting(name):
    return "Hello, " + name + "!"

# Return a boolean
def is_adult(age):
    return age >= 18

print(calculate_tax(100))
print(get_greeting("Alice"))
print(is_adult(25))
```

:::expected_output
20.0
Hello, Alice!
True
:::

## Return Ends the Function

When Python hits `return`, the function stops immediately:

```python live
def check_positive(n):
    if n <= 0:
        return "Not positive"
    return "Positive"

print(check_positive(-5))
print(check_positive(10))
```

:::expected_output
Not positive
Positive
:::

## Multiple Return Statements

Functions can have multiple returns (but only one executes):

```python live
def get_grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"

print(get_grade(95))
print(get_grade(82))
print(get_grade(55))
```

:::expected_output
A
B
F
:::

## Returning Calculated Results

```python live
def calculate_area(width, height):
    area = width * height
    return area

def calculate_perimeter(width, height):
    perimeter = 2 * (width + height)
    return perimeter

w = 5
h = 3
print("Area:", calculate_area(w, h))
print("Perimeter:", calculate_perimeter(w, h))
```

:::expected_output
Area: 15
Perimeter: 16
:::

## Chaining Function Calls

Returned values can be passed to other functions:

```python live
def double(n):
    return n * 2

def add_ten(n):
    return n + 10

# Chain the calls
result = add_ten(double(5))  # double(5)=10, add_ten(10)=20
print(result)
```

:::expected_output
20
:::

## Functions Without Return

A function without `return` gives back `None`:

```python live
def just_print(message):
    print(message)

result = just_print("Hello")
print("Returned:", result)
```

:::expected_output
Hello
Returned: None
:::

## Key Points

- `return` sends a value back to the caller
- `print` only displays; `return` gives back data
- Returned values can be stored in variables
- `return` immediately ends the function
- Functions without `return` give back `None`

:::hint Common Mistake
Using `print` when you meant `return`. If you need to use the result later, you must `return` it.
:::

