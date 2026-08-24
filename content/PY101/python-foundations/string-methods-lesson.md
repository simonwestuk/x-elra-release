---
title: "String Methods"
slug: string-methods-lesson
description: "Learn to transform and search text using built-in string methods"
course_id: PY101
module: python-foundations
module_order: 1
topic: string-methods
topic_order: 6
type: lesson
difficulty: beginner
estimated_minutes: 14
prerequisites:
  - strings-lesson
skills:
  - strings
  - string-methods
outcomes:
  - "Change case with upper(), lower(), title()"
  - "Remove whitespace with strip()"
  - "Search strings with find() and in"
  - "Replace text with replace()"
capstone_relevance: "Clean and validate user input, search through records"
---

## Introduction

String methods are built-in functions that transform or search strings. You call them using dot notation: `string.method()`. These are essential for processing text data.

## Case Methods

Change the capitalization of text:

```python live
text = "Hello World"

print(text.upper())   # HELLO WORLD
print(text.lower())   # hello world
print(text.title())   # Hello World
```

:::expected_output
HELLO WORLD
hello world
Hello World
:::

## Try It: Normalizing Input

```python live
user_input = "  YES  "
cleaned = user_input.strip().lower()
print(cleaned)  # "yes"
```

:::expected_output
yes
:::

## Removing Whitespace

`strip()` removes spaces from both ends:

```python live
messy = "   hello   "
clean = messy.strip()
print("[" + clean + "]")  # [hello]
```

:::expected_output
[hello]
:::

Also available: `lstrip()` (left only) and `rstrip()` (right only).

## Searching Strings

Use `in` to check if text exists:

```python live
sentence = "The quick brown fox"
print("quick" in sentence)  # True
print("slow" in sentence)   # False
```

:::expected_output
True
False
:::

Use `find()` to get the position:

```python live
text = "Hello World"
print(text.find("World"))  # 6
print(text.find("xyz"))    # -1 (not found)
```

:::expected_output
6
-1
:::

## Replacing Text

`replace()` substitutes text:

```python live
message = "Hello World"
new_message = message.replace("World", "Python")
print(new_message)  # Hello Python
```

:::expected_output
Hello Python
:::

Replace all occurrences:

```python live
text = "one two one three one"
result = text.replace("one", "1")
print(result)  # 1 two 1 three 1
```

:::expected_output
1 two 1 three 1
:::

## Checking Start and End

```python live
filename = "report.txt"
print(filename.startswith("report"))  # True
print(filename.endswith(".txt"))      # True
print(filename.endswith(".pdf"))      # False
```

:::expected_output
True
True
False
:::

## Checking Content

```python live
print("123".isdigit())    # True - all digits
print("abc".isalpha())    # True - all letters
print("abc123".isalnum()) # True - letters and digits
print("   ".isspace())    # True - all whitespace
```

:::expected_output
True
True
True
True
:::

## Splitting Strings

Break a string into a list:

```python live
data = "apple,banana,cherry"
fruits = data.split(",")
print(fruits)  # ['apple', 'banana', 'cherry']
```

:::expected_output
['apple', 'banana', 'cherry']
:::

## Joining Strings

Combine a list into a string:

```python live
words = ["Hello", "World"]
sentence = " ".join(words)
print(sentence)  # Hello World
```

:::expected_output
Hello World
:::

## Method Chaining

Call multiple methods in sequence:

```python live
text = "  HELLO world  "
result = text.strip().lower().replace("hello", "hi")
print(result)  # hi world
```

:::expected_output
hi world
:::

## Key Points

- Methods are called with `string.method()`
- Case methods: `upper()`, `lower()`, `title()`
- `strip()` removes leading/trailing whitespace
- `find()` returns position (-1 if not found)
- `replace()` substitutes text
- Methods return new strings (originals unchanged)

:::hint Common Mistake
String methods don't modify the original string. Always save the result: `text = text.upper()` not just `text.upper()`.
:::
