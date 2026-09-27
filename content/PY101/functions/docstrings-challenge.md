---
title: "Challenge: Create a Documented Utility Library"
slug: docstrings-challenge
description: "Build a collection of well-documented utility functions"
course_id: PY101
module: functions
module_order: 4
topic: docstrings
topic_order: 6
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - docstrings-practice
skills:
  - functions
  - documentation
outcomes:
  - "Create production-quality documentation"
  - "Build reusable, well-documented functions"
  - "Apply documentation best practices"
capstone_relevance: "Professional code requires professional documentation"
---

## Challenge: String Utility Library

Create a mini-library of string utility functions, each with complete documentation.

### Requirements

Create these 5 functions with **full docstrings** including:
- Brief description
- Parameters section
- Returns section
- At least one example

**1. `truncate(text, max_length, suffix="...")`**
- Truncates text to max_length characters
- Adds suffix if truncated
- Returns original if already short enough

**2. `count_words(text)`**
- Counts the number of words in text
- Words are separated by spaces

**3. `is_palindrome(text)`**
- Returns True if text is a palindrome (same forwards and backwards)
- Should be case-insensitive
- Ignore spaces

**4. `title_case(text)`**
- Capitalizes the first letter of each word
- Returns the title-cased string

**5. `repeat_string(text, times, separator="")`**
- Repeats text the specified number of times
- Joins with separator between repetitions

### Your Solution

```python live
# Implement all 5 functions with complete docstrings




# Test all functions
print("=== Testing truncate ===")
print(truncate("Hello, World!", 5))
print(truncate("Hi", 10))
print(truncate.__doc__)
print()

print("=== Testing count_words ===")
print(count_words("Hello world"))
print(count_words("One two three four five"))
print(count_words.__doc__)
print()

print("=== Testing is_palindrome ===")
print(is_palindrome("racecar"))
print(is_palindrome("hello"))
print(is_palindrome("A man a plan a canal Panama"))
print(is_palindrome.__doc__)
print()

print("=== Testing title_case ===")
print(title_case("hello world"))
print(title_case("python programming"))
print(title_case.__doc__)
print()

print("=== Testing repeat_string ===")
print(repeat_string("ab", 3))
print(repeat_string("hi", 3, "-"))
print(repeat_string.__doc__)
```

### Expected Output

```
=== Testing truncate ===
He...
Hi
[docstring content]

=== Testing count_words ===
2
5
[docstring content]

=== Testing is_palindrome ===
True
False
True
[docstring content]

=== Testing title_case ===
Hello World
Python Programming
[docstring content]

=== Testing repeat_string ===
ababab
hi-hi-hi
[docstring content]
```

:::hint Truncate Logic
Check if `len(text) <= max_length`. If so, return text. Otherwise, return `text[:max_length - len(suffix)] + suffix`.
:::

:::hint Palindrome Check
Remove spaces with `text.replace(" ", "")`, convert to lowercase with `.lower()`, then compare to its reverse `text[::-1]`.
:::

:::hint Title Case
Use the built-in `.title()` method, or split, capitalize first letter of each word, and join.
:::

:::hint Repeat with Separator
Create a list with text repeated, then join with separator: `separator.join([text] * times)`.
:::

:::answer Reveal full solution
```python
def truncate(text, max_length, suffix="..."):
    """Truncate text to a maximum length, adding a suffix if needed.

    Parameters:
        text: The string to truncate.
        max_length: The maximum allowed length of the result.
        suffix: The string to append when truncating (default "...").

    Returns:
        The original text if short enough, otherwise the truncated
        text with suffix appended.

    Example:
        >>> truncate("Hello, World!", 5)
        'He...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def count_words(text):
    """Count the number of words in a string.

    Parameters:
        text: The string to count words in.

    Returns:
        An integer representing the number of words.

    Example:
        >>> count_words("Hello world")
        2
    """
    return len(text.split())

def is_palindrome(text):
    """Check whether a string is a palindrome.

    The check is case-insensitive and ignores spaces.

    Parameters:
        text: The string to check.

    Returns:
        True if text is a palindrome, False otherwise.

    Example:
        >>> is_palindrome("racecar")
        True
    """
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]

def title_case(text):
    """Capitalize the first letter of each word in a string.

    Parameters:
        text: The string to convert.

    Returns:
        The string with each word's first letter capitalized.

    Example:
        >>> title_case("hello world")
        'Hello World'
    """
    return text.title()

def repeat_string(text, times, separator=""):
    """Repeat a string multiple times with an optional separator.

    Parameters:
        text: The string to repeat.
        times: The number of times to repeat the string.
        separator: The string placed between repetitions (default "").

    Returns:
        A new string with text repeated and joined by separator.

    Example:
        >>> repeat_string("ab", 3)
        'ababab'
    """
    return separator.join([text] * times)

# Test all functions
print("=== Testing truncate ===")
print(truncate("Hello, World!", 5))
print(truncate("Hi", 10))
print(truncate.__doc__)
print()

print("=== Testing count_words ===")
print(count_words("Hello world"))
print(count_words("One two three four five"))
print(count_words.__doc__)
print()

print("=== Testing is_palindrome ===")
print(is_palindrome("racecar"))
print(is_palindrome("hello"))
print(is_palindrome("A man a plan a canal Panama"))
print(is_palindrome.__doc__)
print()

print("=== Testing title_case ===")
print(title_case("hello world"))
print(title_case("python programming"))
print(title_case.__doc__)
print()

print("=== Testing repeat_string ===")
print(repeat_string("ab", 3))
print(repeat_string("hi", 3, "-"))
print(repeat_string.__doc__)
```
:::

