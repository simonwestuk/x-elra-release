---
title: "Lists Basics"
slug: lists-lesson
description: "Learn to create and work with Python lists"
course_id: PY101
module: data-structures
module_order: 3
topic: lists
topic_order: 1
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - variables-types-lesson
  - for-loops-lesson
skills:
  - data-structures
  - lists
outcomes:
  - "Create lists with multiple elements"
  - "Access list elements by index"
  - "Modify list contents"
capstone_relevance: "Store collections of records in your application"
---

## Introduction

Lists are ordered collections that can hold multiple items. Unlike single variables, lists let you store and work with groups of related data - perfect for managing records in your application.

## Creating Lists

Use square brackets `[]` to create a list:

```python live
# Empty list
empty = []

# List with items
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, True, 3.14]

print(fruits)
print(numbers)
print(mixed)
```

:::expected_output
['apple', 'banana', 'cherry']
[1, 2, 3, 4, 5]
['hello', 42, True, 3.14]
:::

## Accessing Elements

Use index numbers starting at 0:

```python live
colors = ["red", "green", "blue", "yellow"]

print(colors[0])   # First element
print(colors[1])   # Second element
print(colors[-1])  # Last element
print(colors[-2])  # Second to last
```

:::expected_output
red
green
yellow
blue
:::

## List Length

Use `len()` to get the number of elements:

```python live
items = ["a", "b", "c", "d", "e"]
print(f"List has {len(items)} elements")
```

:::expected_output
List has 5 elements
:::

## Modifying Elements

Lists are mutable - you can change elements:

```python live
tasks = ["email", "meeting", "report"]
print("Before:", tasks)

tasks[1] = "lunch"
print("After:", tasks)
```

:::expected_output
Before: ['email', 'meeting', 'report']
After: ['email', 'lunch', 'report']
:::

## Adding Elements

```python live
shopping = ["milk", "bread"]
print("Start:", shopping)

# Add to end
shopping.append("eggs")
print("After append:", shopping)

# Insert at position
shopping.insert(1, "cheese")
print("After insert:", shopping)
```

:::expected_output
Start: ['milk', 'bread']
After append: ['milk', 'bread', 'eggs']
After insert: ['milk', 'cheese', 'bread', 'eggs']
:::

## Removing Elements

```python live
numbers = [10, 20, 30, 40, 50]
print("Start:", numbers)

# Remove by value
numbers.remove(30)
print("After remove(30):", numbers)

# Remove by index
removed = numbers.pop(1)
print(f"Popped: {removed}, List: {numbers}")

# Remove last
last = numbers.pop()
print(f"Popped last: {last}, List: {numbers}")
```

:::expected_output
Start: [10, 20, 30, 40, 50]
After remove(30): [10, 20, 40, 50]
Popped: 20, List: [10, 40, 50]
Popped last: 50, List: [10, 40]
:::

## Checking Membership

```python live
fruits = ["apple", "banana", "cherry"]

print("banana" in fruits)  # True
print("grape" in fruits)   # False

if "apple" in fruits:
    print("We have apples!")
```

:::expected_output
True
False
We have apples!
:::

## List of Lists

Lists can contain other lists:

```python live
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[0])      # First row
print(matrix[1][2])   # Row 1, Column 2 (value: 6)
```

:::expected_output
[1, 2, 3]
6
:::

## Key Points

- Lists are ordered, mutable collections
- Create with `[]` or `list()`
- Index starts at 0, use -1 for last
- `append()` adds to end, `insert()` at position
- `remove()` by value, `pop()` by index
- Check membership with `in`

:::hint Common Mistake
Accessing an index that doesn't exist causes IndexError. A list of 5 items has indices 0-4, not 1-5.
:::
