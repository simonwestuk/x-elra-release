---
title: "For Loops and Range"
slug: for-loops-lesson
description: "Learn to iterate over sequences with for loops"
course_id: PY101
module: control-flow
module_order: 2
topic: for-loops
topic_order: 8
type: lesson
difficulty: beginner
estimated_minutes: 14
prerequisites:
  - while-loops-lesson
skills:
  - control-flow
  - for-loops
outcomes:
  - "Write for loops to iterate over sequences"
  - "Use range() for numeric iteration"
  - "Understand for vs while loop use cases"
capstone_relevance: "Loop through records to display, search, and process data"
---

## Introduction

For loops iterate over sequences (like lists, strings, or ranges). Unlike while loops, you don't need to manage a counter variable - Python handles it for you.

## Basic For Loop

```python
for item in sequence:
    # do something with item
```

## Iterating Over a List

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

## Iterating Over a String

```python live
word = "Python"
for letter in word:
    print(letter)
```

:::expected_output
P
y
t
h
o
n
:::

## The range() Function

`range()` generates a sequence of numbers:

```python live
# range(stop) - 0 to stop-1
for i in range(5):
    print(i)
```

:::expected_output
0
1
2
3
4
:::

## range() Variations

```python live
# range(start, stop)
print("1 to 4:")
for i in range(1, 5):
    print(i)

print()

# range(start, stop, step)
print("0, 2, 4, 6, 8:")
for i in range(0, 10, 2):
    print(i)
```

:::expected_output
1 to 4:
1
2
3
4

0, 2, 4, 6, 8:
0
2
4
6
8
:::

## Counting Backwards

```python live
# Negative step
for i in range(5, 0, -1):
    print(i)
print("Blast off!")
```

:::expected_output
5
4
3
2
1
Blast off!
:::

## Using Index with enumerate()

Get both index and value:

```python live
colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"{index}: {color}")
```

:::expected_output
0: red
1: green
2: blue
:::

## Practical Example: Processing Items

```python live
prices = [10.99, 5.50, 8.25, 12.00]
total = 0

for price in prices:
    total = total + price
    print(f"Added ${price:.2f}, running total: ${total:.2f}")

print(f"\nFinal total: ${total:.2f}")
```

:::expected_output
Added $10.99, running total: $10.99
Added $5.50, running total: $16.49
Added $8.25, running total: $24.74
Added $12.00, running total: $36.74

Final total: $36.74
:::

## For vs While

| Use For When | Use While When |
|--------------|----------------|
| Iterating over a sequence | Condition-based repetition |
| Known number of iterations | Unknown iterations |
| Processing each item | Waiting for user input |

```python live
# For: Process each item
items = [1, 2, 3, 4, 5]
for item in items:
    print(item * 2)
```

:::expected_output
2
4
6
8
10
:::

## Key Points

- `for item in sequence:` iterates over each element
- `range(n)` generates 0 to n-1
- `range(start, stop, step)` for more control
- `enumerate()` gives index and value
- For loops are cleaner than while for sequences

:::hint Common Mistake
Using `range(5)` and expecting 1-5. It actually gives 0-4. Use `range(1, 6)` for 1-5.
:::
