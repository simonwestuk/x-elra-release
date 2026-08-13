---
title: "Nested Loops"
slug: nested-loops-lesson
description: "Learn to use loops inside loops for multi-dimensional iteration"
course_id: PY101
module: control-flow
module_order: 2
topic: nested-loops
topic_order: 10
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - for-loops-lesson
skills:
  - control-flow
  - nested-loops
outcomes:
  - "Write loops inside other loops"
  - "Understand inner and outer loop execution order"
  - "Create patterns and grids with nested loops"
capstone_relevance: "Process multi-level data structures in your application"
---

## Introduction

A nested loop is a loop inside another loop. The inner loop completes all its iterations for each iteration of the outer loop. This is useful for working with grids, tables, and combinations.

## Basic Nested Loop

```python live
for outer in range(3):
    print(f"Outer: {outer}")
    for inner in range(2):
        print(f"  Inner: {inner}")
```

:::expected_output
Outer: 0
  Inner: 0
  Inner: 1
Outer: 1
  Inner: 0
  Inner: 1
Outer: 2
  Inner: 0
  Inner: 1
:::

## Try It: Multiplication Table

```python live
for i in range(1, 4):
    for j in range(1, 4):
        result = i * j
        print(f"{i} x {j} = {result}")
    print("---")
```

:::expected_output
1 x 1 = 1
1 x 2 = 2
1 x 3 = 3
---
2 x 1 = 2
2 x 2 = 4
2 x 3 = 6
---
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
---
:::

## How Nested Loops Execute

For each outer iteration:
1. Start outer loop iteration
2. Run entire inner loop (all iterations)
3. Continue to next outer iteration

```python live
print("Starting...")
for row in range(1, 4):
    print(f"Row {row}:")
    for col in range(1, 4):
        print(f"  ({row}, {col})")
print("Done!")
```

:::expected_output
Starting...
Row 1:
  (1, 1)
  (1, 2)
  (1, 3)
Row 2:
  (2, 1)
  (2, 2)
  (2, 3)
Row 3:
  (3, 1)
  (3, 2)
  (3, 3)
Done!
:::

## Creating Patterns

```python live
# Rectangle of stars
rows = 3
cols = 5

for r in range(rows):
    for c in range(cols):
        print("*", end="")
    print()  # New line after each row
```

:::expected_output
*****
*****
*****
:::

## Triangle Pattern

```python live
for row in range(1, 6):
    for star in range(row):
        print("*", end="")
    print()
```

:::expected_output
*
**
***
****
*****
:::

## Processing Grid Data

```python live
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for row in grid:
    for cell in row:
        print(cell, end=" ")
    print()
```

:::expected_output
1 2 3
4 5 6
7 8 9
:::

## Finding in Nested Structure

```python live
students = [
    {"name": "Alice", "grades": [85, 90, 88]},
    {"name": "Bob", "grades": [78, 82, 80]},
]

for student in students:
    print(f"{student['name']}:")
    total = 0
    for grade in student['grades']:
        total = total + grade
    average = total / len(student['grades'])
    print(f"  Average: {average:.1f}")
```

:::expected_output
Alice:
  Average: 87.7
Bob:
  Average: 80.0
:::

## Nested Loop with Indices

```python live
matrix = [
    ["A", "B", "C"],
    ["D", "E", "F"],
]

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print(f"[{i}][{j}] = {matrix[i][j]}")
```

:::expected_output
[0][0] = A
[0][1] = B
[0][2] = C
[1][0] = D
[1][1] = E
[1][2] = F
:::

## Combinations

```python live
colors = ["red", "green"]
sizes = ["S", "M", "L"]

print("All combinations:")
for color in colors:
    for size in sizes:
        print(f"  {color}-{size}")
```

:::expected_output
All combinations:
  red-S
  red-M
  red-L
  green-S
  green-M
  green-L
:::

## Key Points

- Inner loop runs completely for each outer iteration
- Useful for grids, tables, and combinations
- Use meaningful variable names (row/col, i/j)
- `end=""` in print prevents new lines
- Be careful with deeply nested loops (can be slow)

:::hint Common Mistake
Using the same variable name for both loops. `for i in range(3): for i in range(3):` will cause unexpected behavior. Use different names.
:::
