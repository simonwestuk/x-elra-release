---
title: "Tuples"
slug: tuples-lesson
description: "Learn to use immutable sequences with tuples"
course_id: PY101
module: data-structures
module_order: 3
topic: tuples
topic_order: 6
type: lesson
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - lists-lesson
skills:
  - data-structures
  - tuples
outcomes:
  - "Create and access tuples"
  - "Understand tuple immutability"
  - "Use tuple unpacking"
capstone_relevance: "Store fixed data like coordinates and record fields"
---

## Introduction

Tuples are like lists, but immutable - once created, they cannot be changed. Use them for data that shouldn't be modified, like coordinates, dates, or database records.

## Creating Tuples

Use parentheses `()` or just commas:

```python live
# With parentheses
point = (10, 20)
colors = ("red", "green", "blue")

# Without parentheses
numbers = 1, 2, 3

# Single element (note the comma!)
single = (42,)

print(point)
print(numbers)
print(type(single))
```

:::expected_output
(10, 20)
(1, 2, 3)
<class 'tuple'>
:::

## Accessing Elements

Same as lists - use indexing:

```python live
coords = (100, 200, 300)

print(coords[0])   # First
print(coords[-1])  # Last
print(coords[1:])  # Slicing works too
```

:::expected_output
100
300
(200, 300)
:::

## Tuples Are Immutable

You cannot change tuple elements:

```python live
point = (10, 20)
print("Point:", point)

# This would cause an error:
# point[0] = 99  # TypeError!

# Create a new tuple instead
new_point = (99, point[1])
print("New point:", new_point)
```

:::expected_output
Point: (10, 20)
New point: (99, 20)
:::

## Tuple Unpacking

Assign tuple elements to variables:

```python live
# Unpack to variables
point = (10, 20)
x, y = point

print(f"x: {x}, y: {y}")

# Works in loops too
pairs = [(1, "a"), (2, "b"), (3, "c")]
for num, letter in pairs:
    print(f"{num}: {letter}")
```

:::expected_output
x: 10, y: 20
1: a
2: b
3: c
:::

## Swapping Values

```python live
a = 5
b = 10
print(f"Before: a={a}, b={b}")

a, b = b, a  # Tuple swap
print(f"After: a={a}, b={b}")
```

:::expected_output
Before: a=5, b=10
After: a=10, b=5
:::

## Returning Multiple Values

Functions can return tuples:

```python live
def get_dimensions():
    return 1920, 1080  # Returns a tuple

width, height = get_dimensions()
print(f"Screen: {width}x{height}")
```

:::expected_output
Screen: 1920x1080
:::

## Tuples vs Lists

| Tuples | Lists |
|--------|-------|
| Immutable | Mutable |
| `()` | `[]` |
| Faster | Slower |
| Hashable (dict keys) | Not hashable |

```python live
# Tuples can be dict keys
locations = {
    (0, 0): "Origin",
    (10, 20): "Point A"
}

print(locations[(10, 20)])
```

:::expected_output
Point A
:::

## Converting Between Types

```python live
# List to tuple
my_list = [1, 2, 3]
my_tuple = tuple(my_list)
print(my_tuple)

# Tuple to list
my_tuple = (4, 5, 6)
my_list = list(my_tuple)
print(my_list)
```

:::expected_output
(1, 2, 3)
[4, 5, 6]
:::

## Key Points

- Tuples are immutable sequences
- Created with `()` or just commas
- Access elements same as lists
- Unpack into multiple variables
- Use for fixed data like coordinates
- Can be dictionary keys (lists cannot)

:::hint Common Mistake
Creating a single-element tuple: `(42)` is just `42`. Use a comma: `(42,)` to make it a tuple.
:::
