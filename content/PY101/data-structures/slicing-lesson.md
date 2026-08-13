---
title: "List Slicing"
slug: slicing-lesson
description: "Learn to extract portions of lists with slicing"
course_id: PY101
module: data-structures
module_order: 3
topic: slicing
topic_order: 3
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - lists-lesson
skills:
  - data-structures
  - slicing
outcomes:
  - "Extract list portions with slice syntax"
  - "Use start, stop, and step parameters"
  - "Create copies and reverse lists with slicing"
capstone_relevance: "Get subsets of records for pagination and display"
---

## Introduction

Slicing lets you extract portions of a list using a simple syntax: `list[start:stop:step]`. It's a powerful way to get sublists without modifying the original.

## Basic Slicing

```python
list[start:stop]  # Elements from start to stop-1
```

```python live
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:5])   # Elements 2, 3, 4
print(numbers[0:3])   # First three
print(numbers[7:10])  # Last three
```

:::expected_output
[2, 3, 4]
[0, 1, 2]
[7, 8, 9]
:::

## Omitting Start or Stop

```python live
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[:4])    # First 4 (start from 0)
print(numbers[6:])    # From 6 to end
print(numbers[:])     # Everything (copy)
```

:::expected_output
[0, 1, 2, 3]
[6, 7, 8, 9]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
:::

## Negative Indices

```python live
items = ["a", "b", "c", "d", "e"]

print(items[-3:])     # Last 3
print(items[:-2])     # All except last 2
print(items[-4:-1])   # From 4th-last to 2nd-last
```

:::expected_output
['c', 'd', 'e']
['a', 'b', 'c']
['b', 'c', 'd']
:::

## Step (Third Parameter)

```python live
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[::2])   # Every 2nd element
print(numbers[1::2])  # Every 2nd, starting at 1
print(numbers[::3])   # Every 3rd element
```

:::expected_output
[0, 2, 4, 6, 8]
[1, 3, 5, 7, 9]
[0, 3, 6, 9]
:::

## Reversing with Slicing

```python live
items = [1, 2, 3, 4, 5]

reversed_list = items[::-1]
print("Reversed:", reversed_list)
print("Original:", items)  # Unchanged
```

:::expected_output
Reversed: [5, 4, 3, 2, 1]
Original: [1, 2, 3, 4, 5]
:::

## Practical Examples

```python live
# First and last N elements
data = [10, 20, 30, 40, 50, 60, 70, 80]

first_3 = data[:3]
last_3 = data[-3:]
middle = data[2:-2]

print(f"First 3: {first_3}")
print(f"Last 3: {last_3}")
print(f"Middle: {middle}")
```

:::expected_output
First 3: [10, 20, 30]
Last 3: [60, 70, 80]
Middle: [30, 40, 50, 60]
:::

## Slicing Creates Copies

```python live
original = [1, 2, 3, 4, 5]
slice_copy = original[1:4]

slice_copy[0] = 99
print("Original:", original)  # Unchanged
print("Slice:", slice_copy)
```

:::expected_output
Original: [1, 2, 3, 4, 5]
Slice: [99, 3, 4]
:::

## Assigning to Slices

You can replace a portion of a list:

```python live
letters = ["a", "b", "c", "d", "e"]
print("Before:", letters)

letters[1:4] = ["X", "Y"]  # Replace 3 with 2
print("After:", letters)
```

:::expected_output
Before: ['a', 'b', 'c', 'd', 'e']
After: ['a', 'X', 'Y', 'e']
:::

## Key Points

- `[start:stop]` - Elements from start to stop-1
- Omit start to begin at 0
- Omit stop to go to end
- `[::step]` - Every Nth element
- `[::-1]` - Reverse the list
- Slicing creates a new list (copy)

:::hint Common Mistake
The stop index is exclusive - `[0:3]` gives elements 0, 1, 2 (not 3). Think of it as "up to but not including."
:::
