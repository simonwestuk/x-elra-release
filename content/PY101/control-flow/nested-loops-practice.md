---
title: "Practice: Nested Loops"
slug: nested-loops-practice
description: "Practice using loops inside loops"
course_id: PY101
module: control-flow
module_order: 2
topic: nested-loops
topic_order: 10
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - nested-loops-lesson
skills:
  - control-flow
  - nested-loops
outcomes:
  - "Write nested loop structures"
  - "Create patterns with nested loops"
  - "Process multi-dimensional data"
capstone_relevance: "Handle complex data structures in your application"
---

## Exercise 1: Rectangle

Print a 4x6 rectangle of '#' characters:

```python live
# 4 rows, 6 columns of # characters


```

:::expected_output
######
######
######
######
:::

:::hint Stuck?
Outer loop for rows, inner loop for columns. Use `print("#", end="")` then `print()` after inner loop.
:::

:::answer Reveal answer
```python
for row in range(4):
    for col in range(6):
        print("#", end="")
    print()
```
:::

## Exercise 2: Multiplication Table

Print the 5x5 multiplication table:

```python live
# Print 1x1 through 5x5


```

:::expected_output
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
   4   8  12  16  20
   5  10  15  20  25
:::

:::hint Stuck?
Both loops go from 1 to 5. Print `i * j` in each iteration.
:::

:::answer Reveal answer
```python
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i * j:4}", end="")
    print()
```
:::

## Exercise 3: Sum Grid Values

Calculate the sum of all numbers in the grid:

```python live
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
total = 0
# Sum all values


```

:::expected_output
45
:::

:::hint Stuck?
Outer loop through rows, inner loop through cells. Add each cell to total.
:::

:::answer Reveal answer
```python
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
total = 0
for row in grid:
    for cell in row:
        total = total + cell
print(total)
```
:::

## Exercise 4: Right Triangle

Print a right triangle with 5 rows:
```
*
**
***
****
*****
```

```python live
# Print triangle pattern


```

:::expected_output
*
**
***
****
*****
:::

:::hint Stuck?
Outer loop from 1 to 5. Inner loop prints that many stars.
:::

:::answer Reveal answer
```python
for i in range(1, 6):
    for j in range(i):
        print("*", end="")
    print()
```
:::

## Exercise 5: All Pairs

Print all pairs from two lists:

```python live
list1 = ["a", "b"]
list2 = [1, 2, 3]
# Print all combinations like (a, 1)


```

:::expected_output
(a, 1)
(a, 2)
(a, 3)
(b, 1)
(b, 2)
(b, 3)
:::

:::hint Stuck?
Outer loop through list1, inner loop through list2. Print each combination.
:::

:::answer Reveal answer
```python
list1 = ["a", "b"]
list2 = [1, 2, 3]
for item1 in list1:
    for item2 in list2:
        print(f"({item1}, {item2})")
```
:::
