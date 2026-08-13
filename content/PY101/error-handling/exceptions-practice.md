---
title: "Practice: Identifying Exceptions"
slug: exceptions-practice
description: "Practice recognizing and understanding exception types"
course_id: PY101
module: error-handling
module_order: 5
topic: exceptions
topic_order: 2
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - exceptions-lesson
skills:
  - debugging
  - errors
  - exceptions
outcomes:
  - "Identify exception types from code"
  - "Predict which exceptions will occur"
  - "Understand error messages"
capstone_relevance: "Recognizing exceptions helps prevent bugs"
---

## Exercise 1: Predict the Exception

What exception will this code raise? Run it to check.

```python live
# What exception type?
numbers = [1, 2, 3]
print(numbers[5])
```

:::hint Answer
`IndexError` - the list only has indices 0, 1, 2.
:::

:::answer Reveal answer
```python
# What exception type?
# IndexError - the list only has indices 0, 1, 2
numbers = [1, 2, 3]
# print(numbers[5])  # Raises IndexError: list index out of range

# To safely access:
if len(numbers) > 5:
    print(numbers[5])
else:
    print("Index 5 is out of range for a list of length", len(numbers))
```
:::

## Exercise 2: Type Error

What exception will this raise?

```python live
# What exception type?
length = len(42)
```

:::hint Answer
`TypeError` - `len()` expects a sequence (string, list, etc.), not an integer.
:::

:::answer Reveal answer
```python
# What exception type?
# TypeError - len() expects a sequence (string, list, etc.), not an integer
# length = len(42)  # Raises TypeError: object of type 'int' has no len()

# To fix, pass a sequence:
length = len("42")
print(length)  # Prints 2
```
:::

## Exercise 3: Key Error

What exception will this raise?

```python live
# What exception type?
scores = {"Alice": 95, "Bob": 87}
print(scores["Charlie"])
```

:::hint Answer
`KeyError` - "Charlie" is not a key in the dictionary.
:::

:::answer Reveal answer
```python
# What exception type?
# KeyError - "Charlie" is not a key in the dictionary
scores = {"Alice": 95, "Bob": 87}
# print(scores["Charlie"])  # Raises KeyError: 'Charlie'

# To safely access:
print(scores.get("Charlie", "Not found"))  # Prints "Not found"
```
:::

## Exercise 4: Name Error

What exception will this raise?

```python live
# What exception type?
total = price * quantity
```

:::hint Answer
`NameError` - `price` (and `quantity`) have not been defined.
:::

:::answer Reveal answer
```python
# What exception type?
# NameError - price (and quantity) have not been defined
# total = price * quantity  # Raises NameError: name 'price' is not defined

# To fix, define the variables first:
price = 10
quantity = 5
total = price * quantity
print(total)  # Prints 50
```
:::

## Exercise 5: Match the Exception

For each code snippet, identify which exception type it would raise:
- `TypeError`
- `ValueError`
- `ZeroDivisionError`
- `IndexError`
- `KeyError`

```python live
# Snippet A
# number = int("abc")

# Snippet B
# result = 100 / 0

# Snippet C
# text = "hello" * "world"

# Snippet D
# items = [1, 2, 3]
# print(items[-10])

# Uncomment each one individually to test your prediction
```

:::hint Answers
- A: `ValueError` - can't convert "abc" to int
- B: `ZeroDivisionError` - division by zero
- C: `TypeError` - can't multiply string by string
- D: `IndexError` - index -10 is out of range
:::

:::answer Reveal answer
```python
# Snippet A - ValueError
try:
    number = int("abc")
except ValueError as e:
    print("Snippet A - ValueError:", e)

# Snippet B - ZeroDivisionError
try:
    result = 100 / 0
except ZeroDivisionError as e:
    print("Snippet B - ZeroDivisionError:", e)

# Snippet C - TypeError
try:
    text = "hello" * "world"
except TypeError as e:
    print("Snippet C - TypeError:", e)

# Snippet D - IndexError
try:
    items = [1, 2, 3]
    print(items[-10])
except IndexError as e:
    print("Snippet D - IndexError:", e)
```
:::

