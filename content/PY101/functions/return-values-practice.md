---
title: "Practice: Return Values"
slug: return-values-practice
description: "Practice returning values from functions"
course_id: PY101
module: functions
module_order: 4
topic: return-values
topic_order: 3
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - return-values-lesson
skills:
  - functions
  - return-values
outcomes:
  - "Write functions that return values"
  - "Use returned values in expressions"
  - "Choose between print and return"
capstone_relevance: "Return values are essential for data processing"
---

## Exercise 1: Triple a Number

Create a function `triple` that takes a number and returns it multiplied by 3.

```python live
# Define triple


# Test it
result = triple(4)
print(result)  # Should print 12
print(triple(7))  # Should print 21
```

:::expected_output
12
21
:::

:::hint Stuck?
`return n * 3` instead of printing it.
:::

:::answer Reveal answer
```python
def triple(n):
    return n * 3

# Test it
result = triple(4)
print(result)  # Should print 12
print(triple(7))  # Should print 21
```
:::

## Exercise 2: Create a Greeting

Create a function `make_greeting` that takes a name and returns "Hello, [name]!".

```python live
# Define make_greeting


# Test it
message = make_greeting("Alice")
print(message)  # Should print "Hello, Alice!"
```

:::expected_output
Hello, Alice!
:::

:::hint Stuck?
Use string concatenation: `return "Hello, " + name + "!"`
:::

:::answer Reveal answer
```python
def make_greeting(name):
    return "Hello, " + name + "!"

# Test it
message = make_greeting("Alice")
print(message)  # Should print "Hello, Alice!"
```
:::

## Exercise 3: Calculate Average

Create a function `average` that takes two numbers and returns their average.

```python live
# Define average


# Test it
print(average(10, 20))  # Should print 15.0
print(average(7, 3))    # Should print 5.0
```

:::expected_output
15.0
5.0
:::

:::hint Stuck?
Add the numbers and divide by 2: `return (a + b) / 2`
:::

:::answer Reveal answer
```python
def average(a, b):
    return (a + b) / 2

# Test it
print(average(10, 20))  # Should print 15.0
print(average(7, 3))    # Should print 5.0
```
:::

## Exercise 4: Is Even?

Create a function `is_even` that takes a number and returns `True` if it's even, `False` otherwise.

```python live
# Define is_even


# Test it
print(is_even(4))   # True
print(is_even(7))   # False
print(is_even(100)) # True
```

:::expected_output
True
False
True
:::

:::hint Stuck?
Use the modulo operator: `return n % 2 == 0`
:::

:::answer Reveal answer
```python
def is_even(n):
    return n % 2 == 0

# Test it
print(is_even(4))   # True
print(is_even(7))   # False
print(is_even(100)) # True
```
:::

## Exercise 5: Max of Three

Create a function `max_of_three` that takes three numbers and returns the largest.

```python live
# Define max_of_three


# Test it
print(max_of_three(5, 9, 3))   # Should print 9
print(max_of_three(12, 7, 12)) # Should print 12
print(max_of_three(1, 2, 3))   # Should print 3
```

:::expected_output
9
12
3
:::

:::hint Stuck?
You can use nested if statements, or use the built-in max() function: `return max(a, b, c)`.
:::

:::answer Reveal answer
```python
def max_of_three(a, b, c):
    return max(a, b, c)

# Test it
print(max_of_three(5, 9, 3))   # Should print 9
print(max_of_three(12, 7, 12)) # Should print 12
print(max_of_three(1, 2, 3))   # Should print 3
```
:::

