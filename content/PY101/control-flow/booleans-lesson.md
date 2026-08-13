---
title: "Boolean Values"
slug: booleans-lesson
description: "Understand True and False values and how Python evaluates truthiness"
course_id: PY101
module: control-flow
module_order: 2
topic: booleans
topic_order: 2
type: lesson
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - comparisons-lesson
skills:
  - control-flow
  - booleans
outcomes:
  - "Use True and False values"
  - "Understand truthy and falsy values"
  - "Convert values to booleans with bool()"
capstone_relevance: "Track states and flags in your application (active, complete, etc.)"
---

## Introduction

Boolean values represent truth: `True` or `False`. They're named after mathematician George Boole. Every decision in your program ultimately comes down to booleans.

## True and False

Python's boolean values (note the capital letters):

```python live
is_active = True
is_deleted = False

print(is_active)
print(is_deleted)
print(type(is_active))
```

:::expected_output
True
False
<class 'bool'>
:::

## Booleans from Comparisons

Comparison operators return booleans:

```python live
age = 20
print(age >= 18)      # True
print(age == 25)      # False
print(age < 100)      # True
```

:::expected_output
True
False
True
:::

## Truthy and Falsy Values

Python treats some values as "truthy" (act like True) and others as "falsy" (act like False).

### Falsy Values

These are considered False:
- `False`
- `None`
- `0` (zero)
- `""` (empty string)
- `[]` (empty list)
- `{}` (empty dict)

```python live
print(bool(False))  # False
print(bool(0))      # False
print(bool(""))     # False
print(bool([]))     # False
```

:::expected_output
False
False
False
False
:::

### Truthy Values

Everything else is considered True:

```python live
print(bool(True))    # True
print(bool(1))       # True
print(bool(-5))      # True (any non-zero)
print(bool("hello")) # True (non-empty string)
print(bool([1, 2]))  # True (non-empty list)
```

:::expected_output
True
True
True
True
True
:::

## Using bool() to Check

The `bool()` function converts any value to a boolean:

```python live
name = "Alice"
empty_name = ""

print(bool(name))       # True (has content)
print(bool(empty_name)) # False (empty)
```

:::expected_output
True
False
:::

## Practical Uses

Check if a value exists:

```python live
username = ""
password = "secret"

print("Username provided:", bool(username))
print("Password provided:", bool(password))
```

:::expected_output
Username provided: False
Password provided: True
:::

## Boolean Variables as Flags

Use booleans to track states:

```python live
logged_in = False
is_admin = True
has_notifications = True

print(f"Logged in: {logged_in}")
print(f"Is admin: {is_admin}")
print(f"Has notifications: {has_notifications}")
```

:::expected_output
Logged in: False
Is admin: True
Has notifications: True
:::

## Toggling Booleans

Use `not` to flip a boolean:

```python live
light_on = True
print(f"Light on: {light_on}")

light_on = not light_on  # Toggle
print(f"Light on: {light_on}")

light_on = not light_on  # Toggle again
print(f"Light on: {light_on}")
```

:::expected_output
Light on: True
Light on: False
Light on: True
:::

## Key Points

- Booleans are `True` or `False` (capital first letter)
- Comparisons return booleans
- Empty values (0, "", [], None) are falsy
- Non-empty values are truthy
- `bool()` converts any value to boolean
- Use `not` to flip a boolean

:::hint Common Mistake
Writing `true` or `false` (lowercase). Python requires `True` and `False` with capital letters.
:::
