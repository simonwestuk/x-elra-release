---
title: "Practice: List Operations"
slug: list-operations-practice
description: "Practice sorting, copying, and combining lists"
course_id: PY101
module: data-structures
module_order: 3
topic: list-operations
topic_order: 2
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - list-operations-lesson
skills:
  - data-structures
  - list-operations
outcomes:
  - "Sort lists in various ways"
  - "Create proper list copies"
  - "Combine lists effectively"
capstone_relevance: "Organize and sort your application data"
---

## Exercise 1: Sort Numbers

Sort the list in ascending order:

```python live
numbers = [45, 12, 89, 34, 67]
# Sort and print


```

:::expected_output
[12, 34, 45, 67, 89]
:::

:::hint Stuck?
Use `numbers.sort()` or `sorted(numbers)`.
:::

:::answer Reveal answer
```python
numbers = [45, 12, 89, 34, 67]
numbers.sort()
print(numbers)
```
:::

## Exercise 2: Sort Descending

Sort names in reverse alphabetical order:

```python live
names = ["Eve", "Alice", "Charlie", "Bob"]
# Sort descending


```

:::expected_output
['Eve', 'Charlie', 'Bob', 'Alice']
:::

:::hint Stuck?
Use `sort(reverse=True)` or `sorted(..., reverse=True)`.
:::

:::answer Reveal answer
```python
names = ["Eve", "Alice", "Charlie", "Bob"]
names.sort(reverse=True)
print(names)
```
:::

## Exercise 3: Safe Copy

Create a copy of the list, add an item to the copy only:

```python live
original = [1, 2, 3]
# Create copy, add 4 to copy only
# Print both to verify original unchanged


```

:::expected_output
Original: [1, 2, 3]
Copy: [1, 2, 3, 4]
:::

:::hint Stuck?
Use `copy = original.copy()` then `copy.append(4)`.
:::

:::answer Reveal answer
```python
original = [1, 2, 3]
copy = original.copy()
copy.append(4)
print("Original:", original)
print("Copy:", copy)
```
:::

## Exercise 4: Combine Lists

Combine two lists into a new list:

```python live
list1 = ["a", "b", "c"]
list2 = ["d", "e", "f"]
# Combine into new list


```

:::expected_output
['a', 'b', 'c', 'd', 'e', 'f']
:::

:::hint Stuck?
Use `combined = list1 + list2`.
:::

:::answer Reveal answer
```python
list1 = ["a", "b", "c"]
list2 = ["d", "e", "f"]
combined = list1 + list2
print(combined)
```
:::

## Exercise 5: Statistics

Calculate and print min, max, sum, and average:

```python live
scores = [78, 92, 85, 90, 88, 76, 95]
# Calculate and print all statistics


```

:::hint Stuck?
Use `min()`, `max()`, `sum()`. Average = `sum/len`.
:::

:::answer Reveal answer
```python
scores = [78, 92, 85, 90, 88, 76, 95]
print("Min:", min(scores))
print("Max:", max(scores))
print("Sum:", sum(scores))
print("Average:", sum(scores) / len(scores))
```
:::
