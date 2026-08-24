---
title: "Practice: List Comprehensions"
slug: comprehensions-practice
description: "Practice creating lists with comprehension syntax"
course_id: PY101
module: data-structures
module_order: 3
topic: comprehensions
topic_order: 5
type: practice
difficulty: intermediate
estimated_minutes: 15
prerequisites:
  - comprehensions-lesson
skills:
  - data-structures
  - comprehensions
outcomes:
  - "Write list comprehensions"
  - "Add filtering conditions"
  - "Transform data efficiently"
capstone_relevance: "Efficiently process your data records"
---

## Exercise 1: Squares

Create a list of squares from 1 to 10 using a comprehension:

```python live
# Create [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]


```

:::expected_output
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
:::

:::hint Stuck?
Use `[x**2 for x in range(1, 11)]`
:::

:::answer Reveal answer
```python
# Create [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
squares = [x**2 for x in range(1, 11)]
print(squares)
```
:::

## Exercise 2: Uppercase

Convert all strings to uppercase:

```python live
words = ["hello", "world", "python"]
# Create uppercase list


```

:::expected_output
['HELLO', 'WORLD', 'PYTHON']
:::

:::hint Stuck?
Use `[w.upper() for w in words]`
:::

:::answer Reveal answer
```python
words = ["hello", "world", "python"]
uppercase = [w.upper() for w in words]
print(uppercase)
```
:::

## Exercise 3: Filter Positives

Get only positive numbers:

```python live
numbers = [-5, 3, -2, 8, -1, 6, 0, -4]
# Get only positive numbers


```

:::expected_output
[3, 8, 6]
:::

:::hint Stuck?
Add condition: `[n for n in numbers if n > 0]`
:::

:::answer Reveal answer
```python
numbers = [-5, 3, -2, 8, -1, 6, 0, -4]
positives = [n for n in numbers if n > 0]
print(positives)
```
:::

## Exercise 4: Transform and Filter

Double only the even numbers:

```python live
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Double the even numbers only


```

:::expected_output
[4, 8, 12, 16, 20]
:::

:::hint Stuck?
Combine: `[n*2 for n in numbers if n % 2 == 0]`
:::

:::answer Reveal answer
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
doubled_evens = [n * 2 for n in numbers if n % 2 == 0]
print(doubled_evens)
```
:::

## Exercise 5: Extract Data

Get names from the list of dictionaries:

```python live
people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Carol", "age": 35}
]
# Create list of names


```

:::expected_output
['Alice', 'Bob', 'Carol']
:::

:::hint Stuck?
Use `[p["name"] for p in people]`
:::

:::answer Reveal answer
```python
people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Carol", "age": 35}
]
names = [p["name"] for p in people]
print(names)
```
:::
