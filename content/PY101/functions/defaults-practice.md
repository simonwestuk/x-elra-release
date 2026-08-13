---
title: "Practice: Default Parameters"
slug: defaults-practice
description: "Practice using default parameter values"
course_id: PY101
module: functions
module_order: 4
topic: defaults
topic_order: 4
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - defaults-lesson
skills:
  - functions
  - parameters
outcomes:
  - "Write functions with default parameters"
  - "Call functions with and without optional arguments"
  - "Use named arguments effectively"
capstone_relevance: "Defaults create more user-friendly functions"
---

## Exercise 1: Power Function

Create a function `power` that takes a number and an optional exponent (default 2). Return the number raised to that power.

```python live
# Define power with default exponent=2


# Test it
print(power(5))      # 25 (5^2)
print(power(5, 3))   # 125 (5^3)
print(power(2, 10))  # 1024 (2^10)
```

:::expected_output
25
125
1024
:::

:::hint Stuck?
`def power(n, exponent=2):` then `return n ** exponent`
:::

:::answer Reveal answer
```python
def power(n, exponent=2):
    return n ** exponent

print(power(5))      # 25 (5^2)
print(power(5, 3))   # 125 (5^3)
print(power(2, 10))  # 1024 (2^10)
```
:::

## Exercise 2: Greeting with Time

Create a function `greet` that takes a name and an optional time of day (default "day"). Print an appropriate greeting.

```python live
# Define greet with default time_of_day="day"


# Test it
greet("Alice")              # Good day, Alice!
greet("Bob", "morning")     # Good morning, Bob!
greet("Charlie", "evening") # Good evening, Charlie!
```

:::expected_output
Good day, Alice!
Good morning, Bob!
Good evening, Charlie!
:::

:::hint Stuck?
Concatenate: `"Good " + time_of_day + ", " + name + "!"`
:::

:::answer Reveal answer
```python
def greet(name, time_of_day="day"):
    print("Good " + time_of_day + ", " + name + "!")

greet("Alice")              # Good day, Alice!
greet("Bob", "morning")     # Good morning, Bob!
greet("Charlie", "evening") # Good evening, Charlie!
```
:::

## Exercise 3: Repeat Text

Create a function `repeat` that takes text and an optional count (default 1). Return the text repeated that many times.

```python live
# Define repeat with default count=1


# Test it
print(repeat("Hi"))        # Hi
print(repeat("Hi", 3))     # HiHiHi
print(repeat("abc", 5))    # abcabcabcabcabc
```

:::expected_output
Hi
HiHiHi
abcabcabcabcabc
:::

:::hint Stuck?
In Python, `"text" * 3` gives `"texttexttext"`. Return `text * count`.
:::

:::answer Reveal answer
```python
def repeat(text, count=1):
    return text * count

print(repeat("Hi"))        # Hi
print(repeat("Hi", 3))     # HiHiHi
print(repeat("abc", 5))    # abcabcabcabcabc
```
:::

## Exercise 4: Format Name

Create a function `format_name` that takes first name, last name, and an optional `reverse` parameter (default False). Return "First Last" normally, or "Last, First" if reversed.

```python live
# Define format_name with default reverse=False


# Test it
print(format_name("John", "Smith"))               # John Smith
print(format_name("Jane", "Doe", True))           # Doe, Jane
print(format_name("Alice", "Wonder", reverse=True)) # Wonder, Alice
```

:::expected_output
John Smith
Doe, Jane
Wonder, Alice
:::

:::hint Stuck?
Use if/else to check `reverse`. If True, return `last + ", " + first`.
:::

:::answer Reveal answer
```python
def format_name(first, last, reverse=False):
    if reverse:
        return last + ", " + first
    else:
        return first + " " + last

print(format_name("John", "Smith"))               # John Smith
print(format_name("Jane", "Doe", True))           # Doe, Jane
print(format_name("Alice", "Wonder", reverse=True)) # Wonder, Alice
```
:::

## Exercise 5: Build URL

Create a function `build_url` that takes:
- `path` (required)
- `domain` (default "example.com")
- `protocol` (default "https")

Return the complete URL.

```python live
# Define build_url


# Test it
print(build_url("/home"))                              # https://example.com/home
print(build_url("/api", "mysite.com"))                # https://mysite.com/api
print(build_url("/page", protocol="http"))            # http://example.com/page
print(build_url("/test", "test.com", "http"))         # http://test.com/test
```

:::expected_output
https://example.com/home
https://mysite.com/api
http://example.com/page
http://test.com/test
:::

:::hint Stuck?
Concatenate: `protocol + "://" + domain + path`
:::

:::answer Reveal answer
```python
def build_url(path, domain="example.com", protocol="https"):
    return protocol + "://" + domain + path

print(build_url("/home"))                              # https://example.com/home
print(build_url("/api", "mysite.com"))                # https://mysite.com/api
print(build_url("/page", protocol="http"))            # http://example.com/page
print(build_url("/test", "test.com", "http"))         # http://test.com/test
```
:::

