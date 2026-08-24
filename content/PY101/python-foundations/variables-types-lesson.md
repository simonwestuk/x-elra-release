---
title: "Variables and Data Types"
slug: variables-types-lesson
description: "Learn to store and work with different types of data using variables"
course_id: PY101
module: python-foundations
module_order: 1
topic: variables-types
topic_order: 3
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - print-basics-lesson
  - comments-lesson
skills:
  - variables
  - types
outcomes:
  - "Create variables to store data"
  - "Identify Python's basic data types: str, int, float, bool"
  - "Use type() to check a variable's type"
capstone_relevance: "Variables store all your app's data: user names, quantities, prices, and settings"
---

## Introduction

Variables are containers that store data. Instead of using a value directly, you give it a name so you can use it multiple times and change it later.

## Creating Variables

Use the equals sign `=` to assign a value to a variable name:

```python
name = "Alice"
age = 25
```

Now `name` holds the text "Alice" and `age` holds the number 25.

## Try It

```python live
message = "Hello, Python!"
print(message)

message = "Goodbye!"
print(message)
```

:::expected_output
Hello, Python!
Goodbye!
:::

Notice how we can change what a variable holds.

## Data Types

Python has several basic data types:

| Type | Description | Example |
|------|-------------|---------|
| `str` | Text (string) | `"Hello"`, `'Python'` |
| `int` | Whole numbers | `42`, `-7`, `0` |
| `float` | Decimal numbers | `3.14`, `-0.5` |
| `bool` | True or False | `True`, `False` |

## Strings (str)

Text data, wrapped in quotes:

```python live
first_name = "Alice"
last_name = 'Smith'
print(first_name, last_name)
```

:::expected_output
Alice Smith
:::

## Integers (int)

Whole numbers without decimals:

```python live
count = 10
temperature = -5
year = 2024
print(count, temperature, year)
```

:::expected_output
10 -5 2024
:::

## Floats (float)

Numbers with decimal points:

```python live
price = 19.99
pi = 3.14159
percentage = 0.75
print(price, pi, percentage)
```

:::expected_output
19.99 3.14159 0.75
:::

## Booleans (bool)

True or False values (note the capital letters):

```python live
is_active = True
has_permission = False
print(is_active, has_permission)
```

:::expected_output
True False
:::

## Checking Types

Use `type()` to see what type a variable is:

```python live
name = "Alice"
age = 25
price = 19.99
active = True

print(type(name))
print(type(age))
print(type(price))
print(type(active))
```

:::expected_output
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
:::

## Variable Naming Rules

- Must start with a letter or underscore
- Can contain letters, numbers, underscores
- Case-sensitive (`name` and `Name` are different)
- Cannot use Python keywords (`if`, `for`, `True`, etc.)

```python
# Good names
user_name = "Alice"
total_count = 42
isValid = True

# Bad names (will cause errors)
# 2nd_place = "Bob"    # Can't start with number
# my-name = "Alice"    # No hyphens allowed
```

## Key Points

- Variables store data using `=`
- Four basic types: `str`, `int`, `float`, `bool`
- Use `type()` to check a variable's type
- Variable names are case-sensitive
- Choose descriptive names that explain the data

:::hint Common Mistake
Using a variable before creating it causes a NameError. Always assign a value before using the variable.
:::
