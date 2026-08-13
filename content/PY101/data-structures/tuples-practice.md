---
title: "Practice: Tuples"
slug: tuples-practice
description: "Practice working with immutable tuples"
course_id: PY101
module: data-structures
module_order: 3
topic: tuples
topic_order: 6
type: practice
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - tuples-lesson
skills:
  - data-structures
  - tuples
outcomes:
  - "Create and access tuples"
  - "Unpack tuple values"
  - "Use tuples effectively"
capstone_relevance: "Work with fixed record data"
---

## Exercise 1: Create a Tuple

Create a tuple with your name, age, and city:

```python live
# Create a person tuple with 3 elements


```

:::hint Stuck?
Use `person = ("Alice", 25, "London")` or without parentheses.
:::

:::answer Reveal answer
```python
# Create a person tuple with 3 elements
person = ("Alice", 25, "London")
print(person)
```
:::

## Exercise 2: Access Elements

Print the first and last elements:

```python live
colors = ("red", "green", "blue", "yellow")
# Print first and last


```

:::expected_output
red
yellow
:::

:::hint Stuck?
Use `colors[0]` and `colors[-1]`.
:::

:::answer Reveal answer
```python
colors = ("red", "green", "blue", "yellow")
print(colors[0])
print(colors[-1])
```
:::

## Exercise 3: Unpack Tuple

Unpack the coordinates into x and y variables:

```python live
point = (150, 200)
# Unpack to x, y and print


```

:::expected_output
x = 150
y = 200
:::

:::hint Stuck?
Use `x, y = point` then print both.
:::

:::answer Reveal answer
```python
point = (150, 200)
x, y = point
print(f"x = {x}")
print(f"y = {y}")
```
:::

## Exercise 4: Swap Values

Swap the values of a and b using tuple unpacking:

```python live
a = 10
b = 20
# Swap them
# Print to verify


```

:::expected_output
a = 20
b = 10
:::

:::hint Stuck?
Use `a, b = b, a` to swap in one line.
:::

:::answer Reveal answer
```python
a = 10
b = 20
a, b = b, a
print(f"a = {a}")
print(f"b = {b}")
```
:::

## Exercise 5: Loop with Tuples

Print each person's info from the list of tuples:

```python live
people = [
    ("Alice", 25),
    ("Bob", 30),
    ("Carol", 28)
]
# Print: Alice is 25 years old, etc.


```

:::expected_output
Alice is 25 years old
Bob is 30 years old
Carol is 28 years old
:::

:::hint Stuck?
Use `for name, age in people:` to unpack each tuple.
:::

:::answer Reveal answer
```python
people = [
    ("Alice", 25),
    ("Bob", 30),
    ("Carol", 28)
]
for name, age in people:
    print(f"{name} is {age} years old")
```
:::
