---
title: "Iterating Lists"
slug: list-iteration-lesson
description: "Learn different techniques for processing list elements"
course_id: PY101
module: data-structures
module_order: 3
topic: list-iteration
topic_order: 4
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - lists-lesson
  - for-loops-lesson
skills:
  - data-structures
  - list-iteration
outcomes:
  - "Iterate with for loops"
  - "Use enumerate for index and value"
  - "Process lists with various patterns"
capstone_relevance: "Process and display all your records"
---

## Introduction

Processing each element in a list is one of the most common programming tasks. Python offers several ways to iterate through lists, each suited for different situations.

## Basic For Loop

```python live
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

:::expected_output
apple
banana
cherry
:::

## enumerate() for Index and Value

```python live
colors = ["red", "green", "blue"]

for index, color in enumerate(colors):
    print(f"{index}: {color}")

# Start from 1
print()
for num, color in enumerate(colors, 1):
    print(f"{num}. {color}")
```

:::expected_output
0: red
1: green
2: blue

1. red
2. green
3. blue
:::

## Processing and Accumulating

```python live
numbers = [10, 20, 30, 40, 50]
total = 0

for num in numbers:
    total += num
    print(f"Added {num}, total: {total}")

print(f"Final: {total}")
```

:::expected_output
Added 10, total: 10
Added 20, total: 30
Added 30, total: 60
Added 40, total: 100
Added 50, total: 150
Final: 150
:::

## Building New Lists

```python live
numbers = [1, 2, 3, 4, 5]
doubled = []

for num in numbers:
    doubled.append(num * 2)

print("Original:", numbers)
print("Doubled:", doubled)
```

:::expected_output
Original: [1, 2, 3, 4, 5]
Doubled: [2, 4, 6, 8, 10]
:::

## Filtering While Iterating

```python live
scores = [45, 82, 67, 91, 55, 78]
passing = []

for score in scores:
    if score >= 70:
        passing.append(score)

print("All scores:", scores)
print("Passing:", passing)
```

:::expected_output
All scores: [45, 82, 67, 91, 55, 78]
Passing: [82, 91, 78]
:::

## Finding Elements

```python live
names = ["Alice", "Bob", "Charlie", "Diana"]
search = "Charlie"

for i, name in enumerate(names):
    if name == search:
        print(f"Found '{search}' at index {i}")
        break
else:
    print(f"'{search}' not found")
```

:::expected_output
Found 'Charlie' at index 2
:::

## Processing List of Dicts

```python live
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Carol", "grade": 78}
]

for student in students:
    print(f"{student['name']}: {student['grade']}")
```

:::expected_output
Alice: 85
Bob: 92
Carol: 78
:::

## zip() for Parallel Iteration

```python live
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

:::expected_output
Alice: 85
Bob: 92
Charlie: 78
:::

## Key Points

- Basic `for item in list` for simple iteration
- `enumerate()` when you need indices
- Build new lists by appending in loop
- Use `break` with `else` for search patterns
- `zip()` for parallel list iteration

:::hint Common Mistake
Don't modify a list while iterating over it. Create a new list or iterate over a copy if you need to add/remove elements.
:::
