---
title: "List Comprehensions"
slug: comprehensions-lesson
description: "Learn concise syntax for creating and transforming lists"
course_id: PY101
module: data-structures
module_order: 3
topic: comprehensions
topic_order: 5
type: lesson
difficulty: intermediate
estimated_minutes: 15
prerequisites:
  - list-iteration-lesson
skills:
  - data-structures
  - comprehensions
outcomes:
  - "Create lists with comprehension syntax"
  - "Add conditions to comprehensions"
  - "Transform data concisely"
capstone_relevance: "Efficiently transform and filter your records"
---

## Introduction

List comprehensions are a concise way to create lists. They combine the creation of a new list with a for loop in a single line. Once you learn them, they become your go-to tool for list transformations.

## Basic Comprehension

```python
[expression for item in iterable]
```

```python live
# Traditional loop
squares1 = []
for x in range(5):
    squares1.append(x ** 2)

# Comprehension (same result)
squares2 = [x ** 2 for x in range(5)]

print("Loop:", squares1)
print("Comprehension:", squares2)
```

:::expected_output
Loop: [0, 1, 4, 9, 16]
Comprehension: [0, 1, 4, 9, 16]
:::

## Transforming Lists

```python live
names = ["alice", "bob", "charlie"]

# Capitalize each name
capitalized = [name.capitalize() for name in names]
print(capitalized)

# Get lengths
lengths = [len(name) for name in names]
print(lengths)
```

:::expected_output
['Alice', 'Bob', 'Charlie']
[5, 3, 7]
:::

## With Condition (Filtering)

```python
[expression for item in iterable if condition]
```

```python live
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Only even numbers
evens = [n for n in numbers if n % 2 == 0]
print("Evens:", evens)

# Only numbers > 5
above_five = [n for n in numbers if n > 5]
print("Above 5:", above_five)
```

:::expected_output
Evens: [2, 4, 6, 8, 10]
Above 5: [6, 7, 8, 9, 10]
:::

## Transform and Filter

```python live
numbers = [1, 2, 3, 4, 5, 6, 7, 8]

# Square only the even numbers
even_squares = [n ** 2 for n in numbers if n % 2 == 0]
print(even_squares)  # [4, 16, 36, 64]
```

:::expected_output
[4, 16, 36, 64]
:::

## String Processing

```python live
words = ["Hello", "World", "Python"]

# Get first letters
initials = [word[0] for word in words]
print(initials)  # ['H', 'W', 'P']

# Words longer than 4 characters
long_words = [w for w in words if len(w) > 4]
print(long_words)  # ['Hello', 'World', 'Python']
```

:::expected_output
['H', 'W', 'P']
['Hello', 'World', 'Python']
:::

## Processing Data

```python live
products = [
    {"name": "Apple", "price": 1.50},
    {"name": "Banana", "price": 0.75},
    {"name": "Orange", "price": 2.00}
]

# Get just the names
names = [p["name"] for p in products]
print("Names:", names)

# Get prices over $1
expensive = [p["name"] for p in products if p["price"] > 1]
print("Expensive:", expensive)
```

:::expected_output
Names: ['Apple', 'Banana', 'Orange']
Expensive: ['Apple', 'Orange']
:::

## Nested Comprehensions

```python live
# Flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

:::expected_output
[1, 2, 3, 4, 5, 6, 7, 8, 9]
:::

## When to Use Comprehensions

Use comprehensions for:
- Simple transformations
- Filtering
- Short, readable expressions

Use regular loops for:
- Complex logic
- Multiple operations per item
- When readability suffers

## Key Points

- `[expr for item in iterable]` creates a list
- Add `if condition` to filter
- Great for transforming and filtering
- Keep them readable - complex logic goes in loops

:::hint Common Mistake
Making comprehensions too complex. If it's hard to read, use a regular loop instead. Readability matters more than brevity.
:::
