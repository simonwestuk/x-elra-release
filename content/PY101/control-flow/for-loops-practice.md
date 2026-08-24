---
title: "Practice: For Loops"
slug: for-loops-practice
description: "Practice iterating with for loops and range"
course_id: PY101
module: control-flow
module_order: 2
topic: for-loops
topic_order: 8
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - for-loops-lesson
skills:
  - control-flow
  - for-loops
outcomes:
  - "Iterate over lists and strings"
  - "Use range() effectively"
  - "Process sequences with for loops"
capstone_relevance: "Loop through and process records in your application"
---

## Exercise 1: Print List Items

Print each item in the list on its own line:

```python live
colors = ["red", "green", "blue", "yellow"]
# Print each color


```

:::expected_output
red
green
blue
yellow
:::

:::hint Stuck?
Use `for color in colors:` then print inside the loop.
:::

:::answer Reveal answer
```python
colors = ["red", "green", "blue", "yellow"]
for color in colors:
    print(color)
```
:::

## Exercise 2: Sum a List

Calculate the sum of all numbers in the list:

```python live
numbers = [4, 7, 2, 9, 1, 6]
total = 0
# Add each number to total


```

:::expected_output
29
:::

:::hint Stuck?
Loop through numbers, add each to total: `total = total + num`
:::

:::answer Reveal answer
```python
numbers = [4, 7, 2, 9, 1, 6]
total = 0
for num in numbers:
    total = total + num
print(total)
```
:::

## Exercise 3: Print 1 to 10

Use range() to print numbers 1 through 10:

```python live
# Use range to print 1-10


```

:::expected_output
1
2
3
4
5
6
7
8
9
10
:::

:::hint Stuck?
Use `range(1, 11)` since range stops before the end value.
:::

:::answer Reveal answer
```python
for i in range(1, 11):
    print(i)
```
:::

## Exercise 4: Count Characters

Count the number of 'a' characters in the string:

```python live
text = "abracadabra"
count = 0
# Count the 'a' characters


```

:::expected_output
5
:::

:::hint Stuck?
Loop through each character, if it equals 'a', increment count.
:::

:::answer Reveal answer
```python
text = "abracadabra"
count = 0
for char in text:
    if char == 'a':
        count = count + 1
print(count)
```
:::

## Exercise 5: Numbered List

Print items with their numbers (1-based):

```python live
tasks = ["Buy groceries", "Clean room", "Do homework"]
# Print: 1. Buy groceries, etc.


```

:::expected_output
1. Buy groceries
2. Clean room
3. Do homework
:::

:::hint Stuck?
Use `enumerate()` with start=1: `for i, task in enumerate(tasks, 1):`
:::

:::answer Reveal answer
```python
tasks = ["Buy groceries", "Clean room", "Do homework"]
for i, task in enumerate(tasks, 1):
    print(f"{i}. {task}")
```
:::
