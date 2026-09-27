---
title: "Working with Strings"
slug: strings-lesson
description: "Learn to create, combine, and access text data in Python"
course_id: PY101
module: python-foundations
module_order: 1
topic: strings
topic_order: 5
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - variables-types-lesson
skills:
  - strings
outcomes:
  - "Create strings with quotes"
  - "Concatenate strings with +"
  - "Access characters using indexing"
  - "Get string length with len()"
capstone_relevance: "Handle names, descriptions, and all text data in your application"
---

## Introduction

Strings are sequences of characters used to represent text. In Python, you create strings by wrapping text in quotes. Understanding strings is essential for any program that works with text data.

## Creating Strings

Use single or double quotes:

```python live
message1 = "Hello, World!"
message2 = 'Hello, World!'
print(message1)
print(message2)
```

:::expected_output
Hello, World!
Hello, World!
:::

Both work the same way.

## Quotes Inside Strings

Use opposite quote types to include quotes in your text:

```python live
# Double quotes allow single quotes inside
phrase1 = "It's a beautiful day"
print(phrase1)

# Single quotes allow double quotes inside
phrase2 = 'She said "Hello"'
print(phrase2)
```

:::expected_output
It's a beautiful day
She said "Hello"
:::

## String Concatenation

Join strings together with `+`:

```python live
first_name = "Alice"
last_name = "Smith"
full_name = first_name + " " + last_name
print(full_name)
```

:::expected_output
Alice Smith
:::

Notice we added a space `" "` between the names.

## String Repetition

Repeat strings with `*`:

```python live
line = "-" * 20
print(line)
print("TITLE")
print(line)
```

:::expected_output
--------------------
TITLE
--------------------
:::

## String Length

Use `len()` to count characters:

```python live
text = "Hello"
print(len(text))  # 5

password = "secret123"
print(len(password))  # 9
```

:::expected_output
5
9
:::

## Accessing Characters (Indexing)

Each character has a position number (index), starting at 0:

```
 H  e  l  l  o
 0  1  2  3  4
```

```python live
word = "Hello"
print(word[0])  # H (first character)
print(word[1])  # e (second character)
print(word[4])  # o (last character)
```

:::expected_output
H
e
o
:::

## Negative Indexing

Count backwards from the end with negative numbers:

```
  H   e   l   l   o
 -5  -4  -3  -2  -1
```

```python live
word = "Hello"
print(word[-1])  # o (last)
print(word[-2])  # l (second to last)
```

:::expected_output
o
l
:::

## Strings Are Immutable

You cannot change individual characters in a string:

```python
word = "Hello"
# word[0] = "J"  # This would cause an error!
```

Instead, create a new string:

```python live
word = "Hello"
new_word = "J" + word[1:]  # Jello
print(new_word)
```

:::expected_output
Jello
:::

## Key Points

- Strings are text wrapped in quotes (single or double)
- Concatenate with `+`, repeat with `*`
- `len()` returns the number of characters
- Indexing starts at 0 (or -1 from the end)
- Strings cannot be modified in place

:::hint Common Mistake
Index out of range errors happen when you try to access a position that doesn't exist. A 5-character string has indices 0-4 (not 1-5).
:::
