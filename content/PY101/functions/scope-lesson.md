---
title: "Variable Scope"
slug: scope-lesson
description: "Understand where variables can be accessed in your code"
course_id: PY101
module: functions
module_order: 4
topic: scope
topic_order: 5
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - defining-functions-lesson
  - return-values-lesson
skills:
  - functions
  - scope
outcomes:
  - "Understand local and global scope"
  - "Know when variables are accessible"
  - "Avoid common scope-related bugs"
capstone_relevance: "Understanding scope prevents bugs in larger programs"
---

## Introduction

**Scope** determines where a variable can be accessed in your code. Understanding scope helps you avoid bugs and write cleaner programs. Python has two main scopes: **local** (inside functions) and **global** (outside functions).

## Local Scope

Variables created inside a function are **local**—they only exist inside that function:

```python live
def my_function():
    x = 10  # Local variable
    print("Inside function:", x)

my_function()

# This would cause an error:
# print(x)  # x doesn't exist here
```

:::expected_output
Inside function: 10
:::

The variable `x` is created when the function runs and destroyed when it ends.

## Global Scope

Variables created outside functions are **global**—they can be accessed anywhere:

```python live
message = "Hello"  # Global variable

def greet():
    print(message)  # Can read global variable

greet()
print(message)  # Can also access here
```

:::expected_output
Hello
Hello
:::

## Local Variables Hide Global Ones

If you create a local variable with the same name as a global one, the local variable takes precedence inside the function:

```python live
x = "global"

def my_function():
    x = "local"  # Creates a new local variable
    print("Inside:", x)

my_function()
print("Outside:", x)  # Global is unchanged
```

:::expected_output
Inside: local
Outside: global
:::

## Each Function Has Its Own Scope

```python live
def function_a():
    number = 1
    print("In A:", number)

def function_b():
    number = 2
    print("In B:", number)

function_a()
function_b()
# Each function has its own 'number' variable
```

:::expected_output
In A: 1
In B: 2
:::

## Parameters Are Local

Function parameters are local variables:

```python live
def greet(name):  # name is local
    print("Hello,", name)

greet("Alice")
# print(name)  # Would cause error - name is local to greet
```

:::expected_output
Hello, Alice
:::

## The global Keyword

To modify a global variable from inside a function, use `global`:

```python live
counter = 0

def increment():
    global counter  # Refers to the global variable
    counter = counter + 1
    print("Counter:", counter)

increment()
increment()
increment()
print("Final:", counter)
```

:::expected_output
Counter: 1
Counter: 2
Counter: 3
Final: 3
:::

Without `global`, Python would create a local variable instead:

```python live
counter = 0

def increment_local():
    counter = 1  # Creates local variable, doesn't affect global
    print("Inside:", counter)

increment_local()
print("Global unchanged:", counter)
```

:::expected_output
Inside: 1
Global unchanged: 0
:::

## Why Scope Matters

Scope prevents functions from accidentally changing each other's variables:

```python live
def calculate_tax(amount):
    rate = 0.2
    return amount * rate

def calculate_discount(amount):
    rate = 0.1  # Different rate, no conflict!
    return amount * rate

price = 100
tax = calculate_tax(price)
discount = calculate_discount(price)

print("Tax:", tax)
print("Discount:", discount)
```

:::expected_output
Tax: 20.0
Discount: 10.0
:::

## Best Practices

### 1. Prefer Local Variables

```python live
# Good: Use parameters and return values
def add_numbers(a, b):
    result = a + b
    return result

total = add_numbers(5, 3)
print(total)
```

:::expected_output
8
:::

### 2. Avoid Excessive Globals

```python live
# Less ideal: Relying on globals
count = 0

def increment():
    global count
    count += 1

# Better: Return new value
def increment_value(current):
    return current + 1

my_count = 0
my_count = increment_value(my_count)
print(my_count)
```

:::expected_output
1
:::

### 3. Use Globals for Constants

```python live
# Acceptable: Constants that don't change
MAX_ITEMS = 100
TAX_RATE = 0.08

def calculate_max_cost(price):
    return price * MAX_ITEMS * (1 + TAX_RATE)

print(calculate_max_cost(10))
```

:::expected_output
1080.0
:::

## Key Points

- Local variables exist only inside their function
- Global variables are accessible everywhere
- Local variables with same name hide global ones
- Use `global` keyword to modify global variables
- Prefer parameters and return values over global variables

:::hint Common Mistake
Trying to modify a global variable without `global` creates a local variable instead, leaving the global unchanged.
:::

