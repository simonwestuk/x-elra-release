---
title: "Practice: Dictionary Operations"
slug: dict-operations-practice
description: "Practice advanced dictionary operations"
course_id: PY101
module: data-structures
module_order: 3
topic: dict-operations
topic_order: 8
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - dict-operations-lesson
skills:
  - data-structures
  - dict-operations
outcomes:
  - "Iterate dictionaries effectively"
  - "Use dictionaries for data processing"
  - "Merge and transform dictionary data"
capstone_relevance: "Process and analyze your application data"
---

## Exercise 1: Iterate Items

Print each person's name and age:

```python live
people = {"Alice": 25, "Bob": 30, "Carol": 28}
# Print: Alice is 25 years old, etc.


```

:::expected_output
Alice is 25 years old
Bob is 30 years old
Carol is 28 years old
:::

:::hint Stuck?
Use `for name, age in people.items():`
:::

:::answer Reveal answer
```python
people = {"Alice": 25, "Bob": 30, "Carol": 28}
for name, age in people.items():
    print(f"{name} is {age} years old")
```
:::

## Exercise 2: Sum Values

Calculate the total of all values:

```python live
expenses = {"rent": 1000, "food": 300, "transport": 150}
# Calculate and print total


```

:::expected_output
1450
:::

:::hint Stuck?
Loop through `.values()` and sum them.
:::

:::answer Reveal answer
```python
expenses = {"rent": 1000, "food": 300, "transport": 150}
total = sum(expenses.values())
print(total)
```
:::

## Exercise 3: Count Items

Count how many times each color appears:

```python live
colors = ["red", "blue", "red", "green", "blue", "red"]
# Count each color


```

:::expected_output
{'red': 3, 'blue': 2, 'green': 1}
:::

:::hint Stuck?
Use `counts[color] = counts.get(color, 0) + 1` pattern.
:::

:::answer Reveal answer
```python
colors = ["red", "blue", "red", "green", "blue", "red"]
counts = {}
for color in colors:
    counts[color] = counts.get(color, 0) + 1
print(counts)
```
:::

## Exercise 4: Merge Dicts

Merge user settings with defaults (user overrides):

```python live
defaults = {"volume": 50, "brightness": 70}
user = {"volume": 80}
# Merge into final settings


```

:::expected_output
{'volume': 80, 'brightness': 70}
:::

:::hint Stuck?
Use `{**defaults, **user}` to merge with user taking precedence.
:::

:::answer Reveal answer
```python
defaults = {"volume": 50, "brightness": 70}
user = {"volume": 80}
settings = {**defaults, **user}
print(settings)
```
:::

## Exercise 5: Filter Dict

Create a new dict with only items where value > 50:

```python live
scores = {"Alice": 85, "Bob": 45, "Carol": 92, "Dave": 38}
# Filter passing scores (> 50)


```

:::expected_output
{'Alice': 85, 'Carol': 92}
:::

:::hint Stuck?
Use dict comprehension: `{k: v for k, v in scores.items() if v > 50}`
:::

:::answer Reveal answer
```python
scores = {"Alice": 85, "Bob": 45, "Carol": 92, "Dave": 38}
passing = {k: v for k, v in scores.items() if v > 50}
print(passing)
```
:::
