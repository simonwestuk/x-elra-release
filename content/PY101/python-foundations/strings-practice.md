---
title: "Practice: Working with Strings"
slug: strings-practice
description: "Practice string creation, concatenation, and indexing"
course_id: PY101
module: python-foundations
module_order: 1
topic: strings
topic_order: 5
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - strings-lesson
skills:
  - strings
outcomes:
  - "Create and combine strings"
  - "Access characters by index"
  - "Work with string length"
capstone_relevance: "String handling is essential for user data in your application"
---

## Exercise 1: Full Name

Create variables for first and last name, then combine them with a space:

```python live
# Create first_name and last_name variables
# Combine them into full_name with a space between
# Print the full name


```

:::hint Stuck?
Use `+` to join strings: `full = first + " " + last`
:::

:::answer Reveal answer
```python
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print(full_name)
```
:::

## Exercise 2: Border Line

Create a border line of 30 equals signs using string repetition:

```python live
# Create a line of 30 "=" characters and print it


```

:::expected_output
==============================
:::

:::hint Stuck?
Use the `*` operator: `"=" * 30`
:::

:::answer Reveal answer
```python
border = "=" * 30
print(border)
```
:::

## Exercise 3: First and Last

Given the word "Python", print the first and last characters:

```python live
word = "Python"
# Print the first character
# Print the last character


```

:::expected_output
P
n
:::

:::hint Stuck?
First character is index 0, last is index -1.
:::

:::answer Reveal answer
```python
word = "Python"
print(word[0])
print(word[-1])
```
:::

## Exercise 4: Password Length Check

Check if a password is long enough (at least 8 characters):

```python live
password = "secret"
# Get the length and print it
# Print whether it's at least 8 characters


```

:::expected_output
6
False
:::

:::hint Stuck?
Use `len(password)` to get the length.
:::

:::answer Reveal answer
```python
password = "secret"
length = len(password)
print(length)
print(length >= 8)
```
:::

## Exercise 5: Initial Builder

Given first, middle, and last names, create initials (first letter of each):

```python live
first = "John"
middle = "Robert"
last = "Smith"
# Create initials using indexing
# Print the initials (e.g., "J.R.S.")


```

:::expected_output
J.R.S.
:::

:::hint Stuck?
Get the first character of each name with `[0]`, then concatenate with dots.
:::

:::answer Reveal answer
```python
first = "John"
middle = "Robert"
last = "Smith"
initials = first[0] + "." + middle[0] + "." + last[0] + "."
print(initials)
```
:::
