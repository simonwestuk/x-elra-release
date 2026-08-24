---
title: "Practice: List Slicing"
slug: slicing-practice
description: "Practice extracting list portions with slicing"
course_id: PY101
module: data-structures
module_order: 3
topic: slicing
topic_order: 3
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - slicing-lesson
skills:
  - data-structures
  - slicing
outcomes:
  - "Extract specific portions of lists"
  - "Use all slice parameters"
  - "Apply slicing to practical problems"
capstone_relevance: "Get subsets of data for display"
---

## Exercise 1: First Three

Get the first three elements:

```python live
items = ["a", "b", "c", "d", "e", "f"]
# Get first three


```

:::expected_output
['a', 'b', 'c']
:::

:::hint Stuck?
Use `[:3]` to get elements from start to index 3 (exclusive).
:::

:::answer Reveal answer
```python
items = ["a", "b", "c", "d", "e", "f"]
first_three = items[:3]
print(first_three)
```
:::

## Exercise 2: Last Three

Get the last three elements:

```python live
numbers = [10, 20, 30, 40, 50, 60, 70]
# Get last three


```

:::expected_output
[50, 60, 70]
:::

:::hint Stuck?
Use `[-3:]` to get from third-last to end.
:::

:::answer Reveal answer
```python
numbers = [10, 20, 30, 40, 50, 60, 70]
last_three = numbers[-3:]
print(last_three)
```
:::

## Exercise 3: Middle Section

Get elements from index 2 to 5 (not including 5):

```python live
data = [0, 1, 2, 3, 4, 5, 6, 7]
# Get indices 2, 3, 4


```

:::expected_output
[2, 3, 4]
:::

:::hint Stuck?
Use `[2:5]` for elements at indices 2, 3, 4.
:::

:::answer Reveal answer
```python
data = [0, 1, 2, 3, 4, 5, 6, 7]
middle = data[2:5]
print(middle)
```
:::

## Exercise 4: Every Other

Get every other element:

```python live
letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
# Get a, c, e, g


```

:::expected_output
['a', 'c', 'e', 'g']
:::

:::hint Stuck?
Use `[::2]` to get every second element starting from 0.
:::

:::answer Reveal answer
```python
letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
every_other = letters[::2]
print(every_other)
```
:::

## Exercise 5: Reverse

Create a reversed copy of the list:

```python live
original = [1, 2, 3, 4, 5]
# Create reversed version


```

:::expected_output
[5, 4, 3, 2, 1]
:::

:::hint Stuck?
Use `[::-1]` to reverse.
:::

:::answer Reveal answer
```python
original = [1, 2, 3, 4, 5]
reversed_list = original[::-1]
print(reversed_list)
```
:::
