---
title: "Practice: Debugging"
slug: debugging-practice
description: "Practice finding and fixing bugs in code"
course_id: PY101
module: error-handling
module_order: 5
topic: debugging
topic_order: 5
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - debugging-lesson
skills:
  - debugging
outcomes:
  - "Find bugs using print statements"
  - "Fix common programming errors"
  - "Apply debugging strategies"
capstone_relevance: "Every developer debugs code daily"
---

## Exercise 1: Find the Bug

This function should return the sum of all numbers, but it's broken. Add print statements to find and fix the bug.

```python live
def sum_all(numbers):
    total = 0
    for num in numbers:
        total = num  # There's a bug here!
    return total

# Should return 15, but returns 5
result = sum_all([1, 2, 3, 4, 5])
print("Result:", result)
```

:::expected_output
Result: 15
:::

:::hint Stuck?
Add `print("total:", total)` inside the loop. The bug is that it's assigning instead of adding.
:::

:::answer Reveal answer
```python
def sum_all(numbers):
    total = 0
    for num in numbers:
        total += num  # Fixed: changed = to +=
    return total

# Should return 15
result = sum_all([1, 2, 3, 4, 5])
print("Result:", result)
```
:::

## Exercise 2: Debug the Average

This function should calculate the average, but gives wrong results. Find and fix the bug.

```python live
def calculate_average(numbers):
    total = 0
    count = 0
    for num in numbers:
        total += num
    count += 1  # Bug: wrong indentation
    return total / count

# Should return 3.0, but crashes or gives wrong answer
result = calculate_average([1, 2, 3, 4, 5])
print("Average:", result)
```

:::expected_output
Average: 3.0
:::

:::hint Stuck?
The `count += 1` line has wrong indentation. It should be inside the loop.
:::

:::answer Reveal answer
```python
def calculate_average(numbers):
    total = 0
    count = 0
    for num in numbers:
        total += num
        count += 1  # Fixed: moved inside the loop
    return total / count

# Should return 3.0
result = calculate_average([1, 2, 3, 4, 5])
print("Average:", result)
```
:::

## Exercise 3: Debug the Maximum Finder

This function should find the maximum value but doesn't work correctly. Debug it.

```python live
def find_max(numbers):
    maximum = 0  # Bug: what if all numbers are negative?
    for num in numbers:
        if num > maximum:
            maximum = num
    return maximum

# Test with negative numbers
result = find_max([-5, -3, -8, -1])
print("Maximum:", result)  # Should be -1, but returns 0
```

:::expected_output
Maximum: -1
:::

:::hint Stuck?
Initialize `maximum` to the first element of the list: `maximum = numbers[0]`, not 0.
:::

:::answer Reveal answer
```python
def find_max(numbers):
    maximum = numbers[0]  # Fixed: initialize to first element, not 0
    for num in numbers:
        if num > maximum:
            maximum = num
    return maximum

# Test with negative numbers
result = find_max([-5, -3, -8, -1])
print("Maximum:", result)  # Should be -1
```
:::

## Exercise 4: Debug the Counter

This function should count how many times each word appears. Debug it.

```python live
def count_words(words):
    counts = {}
    for word in words:
        if word in counts:
            counts[word] = 1  # Bug!
        else:
            counts[word] = 1
    return counts

words = ["apple", "banana", "apple", "cherry", "apple"]
result = count_words(words)
print(result)  # Should show apple: 3, but shows apple: 1
```

:::expected_output
{'apple': 3, 'banana': 1, 'cherry': 1}
:::

:::hint Stuck?
In the `if word in counts:` branch, we should increment, not reset. Use `counts[word] += 1`.
:::

:::answer Reveal answer
```python
def count_words(words):
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1  # Fixed: changed = 1 to += 1
        else:
            counts[word] = 1
    return counts

words = ["apple", "banana", "apple", "cherry", "apple"]
result = count_words(words)
print(result)  # Should show apple: 3
```
:::

## Exercise 5: Debug the Filter

This function should return only even numbers. Find all the bugs.

```python live
def get_evens(numbers):
    evens = []
    for num in numbers:
        if num % 2 == 1:  # Bug 1: wrong condition
            evens.append(num)
        return evens  # Bug 2: wrong indentation

result = get_evens([1, 2, 3, 4, 5, 6])
print("Evens:", result)  # Should be [2, 4, 6]
```

:::expected_output
Evens: [2, 4, 6]
:::

:::hint Bugs
1. `num % 2 == 1` checks for odd numbers. Should be `num % 2 == 0`.
2. `return evens` is inside the loop. Should be outside (less indentation).
:::

:::answer Reveal answer
```python
def get_evens(numbers):
    evens = []
    for num in numbers:
        if num % 2 == 0:  # Fixed: changed == 1 to == 0
            evens.append(num)
    return evens  # Fixed: moved outside the loop

result = get_evens([1, 2, 3, 4, 5, 6])
print("Evens:", result)  # Should be [2, 4, 6]
```
:::

