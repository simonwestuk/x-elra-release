---
title: "Practice: Variable Scope"
slug: scope-practice
description: "Practice understanding local and global scope"
course_id: PY101
module: functions
module_order: 4
topic: scope
topic_order: 5
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - scope-lesson
skills:
  - functions
  - scope
outcomes:
  - "Identify local and global variables"
  - "Use global keyword correctly"
  - "Debug scope-related issues"
capstone_relevance: "Scope understanding prevents bugs in complex programs"
---

## Exercise 1: Predict the Output

Read this code and predict what it will print. Then run it to check.

```python live
x = 5

def change_x():
    x = 10
    print("Inside:", x)

change_x()
print("Outside:", x)
```

:::expected_output
Inside: 10
Outside: 5
:::

What happened? Why didn't the global `x` change?

:::hint Explanation
Inside the function, `x = 10` creates a *new local variable*. It doesn't modify the global `x`.
:::

:::answer Reveal answer
```python
x = 5

def change_x():
    x = 10
    print("Inside:", x)

change_x()
print("Outside:", x)
# Output:
# Inside: 10
# Outside: 5
```
:::

## Exercise 2: Fix the Counter

This code tries to count function calls but doesn't work correctly. Fix it using the `global` keyword.

```python live
call_count = 0

def my_function():
    # Fix this function so it increments the global counter
    call_count = call_count + 1
    print("Function called", call_count, "times")

my_function()
my_function()
my_function()
print("Total calls:", call_count)
```

:::expected_output
Function called 1 times
Function called 2 times
Function called 3 times
Total calls: 3
:::

:::hint Stuck?
Add `global call_count` as the first line inside the function.
:::

:::answer Reveal answer
```python
call_count = 0

def my_function():
    global call_count
    call_count = call_count + 1
    print("Function called", call_count, "times")

my_function()
my_function()
my_function()
print("Total calls:", call_count)
```
:::

## Exercise 3: Local Variables

Create a function `calculate` that:
1. Creates a local variable `result`
2. Sets it to the parameter `a` times the parameter `b`
3. Returns the result

```python live
def calculate(a, b):
    # Create local variable and return it
    pass

# Test it
print(calculate(4, 5))   # Should print 20
print(calculate(7, 3))   # Should print 21

# This should NOT work (result is local):
# print(result)
```

:::expected_output
20
21
:::

:::hint Stuck?
`result = a * b` then `return result`. The variable `result` is local to the function.
:::

:::answer Reveal answer
```python
def calculate(a, b):
    result = a * b
    return result

# Test it
print(calculate(4, 5))   # Should print 20
print(calculate(7, 3))   # Should print 21

# This should NOT work (result is local):
# print(result)
```
:::

## Exercise 4: Reading Global Variables

Create a program with:
1. A global variable `tax_rate = 0.08`
2. A function `add_tax(price)` that returns the price plus tax

```python live
# Define global tax rate


# Define function that uses it


# Test
print(add_tax(100))   # Should print 108.0
print(add_tax(50))    # Should print 54.0
```

:::expected_output
108.0
54.0
:::

:::hint Stuck?
You can *read* global variables without using `global`. Just `return price * (1 + tax_rate)`.
:::

:::answer Reveal answer
```python
tax_rate = 0.08

def add_tax(price):
    return price * (1 + tax_rate)

# Test
print(add_tax(100))   # Should print 108.0
print(add_tax(50))    # Should print 54.0
```
:::

## Exercise 5: Independent Functions

Create two functions that each use a local variable named `total`, but they don't interfere with each other.

```python live
def sum_of_squares(a, b):
    # Use local 'total' to compute a² + b²
    pass

def sum_of_cubes(a, b):
    # Use local 'total' to compute a³ + b³
    pass

# Test both - they should work independently
print(sum_of_squares(2, 3))  # Should print 13 (4 + 9)
print(sum_of_cubes(2, 3))    # Should print 35 (8 + 27)
```

:::expected_output
13
35
:::

:::hint Stuck?
Each function can have `total = ...` without affecting the other. They're separate local variables.
:::

:::answer Reveal answer
```python
def sum_of_squares(a, b):
    total = a ** 2 + b ** 2
    return total

def sum_of_cubes(a, b):
    total = a ** 3 + b ** 3
    return total

# Test both - they should work independently
print(sum_of_squares(2, 3))  # Should print 13 (4 + 9)
print(sum_of_cubes(2, 3))    # Should print 35 (8 + 27)
```
:::

