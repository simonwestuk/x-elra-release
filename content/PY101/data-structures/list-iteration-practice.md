---
title: "Practice: List Iteration"
slug: list-iteration-practice
description: "Practice iterating through lists with various techniques"
course_id: PY101
module: data-structures
module_order: 3
topic: list-iteration
topic_order: 4
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - list-iteration-lesson
skills:
  - data-structures
  - list-iteration
outcomes:
  - "Use different iteration techniques"
  - "Process list elements effectively"
  - "Build new lists from iteration"
capstone_relevance: "Process all records in your application"
---

## Exercise 1: Print Numbered

Print each item with its number (1-based):

```python live
items = ["apple", "banana", "cherry"]
# Print: 1. apple, 2. banana, 3. cherry


```

:::expected_output
1. apple
2. banana
3. cherry
:::

:::hint Stuck?
Use `enumerate(items, 1)` to start numbering at 1.
:::

:::answer Reveal answer
```python
items = ["apple", "banana", "cherry"]
for num, item in enumerate(items, 1):
    print(f"{num}. {item}")
```
:::

## Exercise 2: Sum All

Calculate the sum of all numbers:

```python live
numbers = [15, 23, 8, 42, 16]
total = 0
# Sum all numbers


```

:::expected_output
104
:::

:::hint Stuck?
Loop through and add each to total: `total += num`
:::

:::answer Reveal answer
```python
numbers = [15, 23, 8, 42, 16]
total = 0
for num in numbers:
    total += num
print(total)
```
:::

## Exercise 3: Create Squares

Create a new list with squares of each number:

```python live
numbers = [1, 2, 3, 4, 5]
squares = []
# Create list of squares


```

:::expected_output
[1, 4, 9, 16, 25]
:::

:::hint Stuck?
Loop and append: `squares.append(num ** 2)`
:::

:::answer Reveal answer
```python
numbers = [1, 2, 3, 4, 5]
squares = []
for num in numbers:
    squares.append(num ** 2)
print(squares)
```
:::

## Exercise 4: Filter Positives

Create a list of only positive numbers:

```python live
numbers = [-5, 3, -2, 8, -1, 6]
positives = []
# Filter positive numbers


```

:::expected_output
[3, 8, 6]
:::

:::hint Stuck?
Check `if num > 0:` before appending.
:::

:::answer Reveal answer
```python
numbers = [-5, 3, -2, 8, -1, 6]
positives = []
for num in numbers:
    if num > 0:
        positives.append(num)
print(positives)
```
:::

## Exercise 5: Combine Lists

Print pairs from two lists using zip:

```python live
names = ["Alice", "Bob", "Carol"]
ages = [25, 30, 28]
# Print: Alice is 25, Bob is 30, etc.


```

:::expected_output
Alice is 25
Bob is 30
Carol is 28
:::

:::hint Stuck?
Use `for name, age in zip(names, ages):`
:::

:::answer Reveal answer
```python
names = ["Alice", "Bob", "Carol"]
ages = [25, 30, 28]
for name, age in zip(names, ages):
    print(f"{name} is {age}")
```
:::
