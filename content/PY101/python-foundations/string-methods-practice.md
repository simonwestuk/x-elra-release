---
title: "Practice: String Methods"
slug: string-methods-practice
description: "Practice transforming and searching strings with methods"
course_id: PY101
module: python-foundations
module_order: 1
topic: string-methods
topic_order: 6
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - string-methods-lesson
skills:
  - strings
  - string-methods
outcomes:
  - "Apply string methods to transform text"
  - "Search and replace within strings"
  - "Chain multiple methods together"
capstone_relevance: "Process user input and format output in your application"
---

## Exercise 1: Normalize Username

Clean up a username by removing spaces and converting to lowercase:

```python live
username = "  JohnDoe123  "
# Clean and normalize the username
# Print the result


```

:::expected_output
johndoe123
:::

:::hint Stuck?
Use `strip()` to remove spaces and `lower()` for lowercase. Chain them: `text.strip().lower()`
:::

:::answer Reveal answer
```python
username = "  JohnDoe123  "
cleaned = username.strip().lower()
print(cleaned)
```
:::

## Exercise 2: Title Case

Convert a book title to proper title case:

```python live
book = "the great gatsby"
# Convert to title case and print


```

:::expected_output
The Great Gatsby
:::

:::hint Stuck?
Use the `title()` method.
:::

:::answer Reveal answer
```python
book = "the great gatsby"
print(book.title())
```
:::

## Exercise 3: Search for Keyword

Check if the word "error" appears in a log message:

```python live
log = "System started. No error detected."
# Check if "error" is in the log (case-insensitive)
# Print True or False


```

:::expected_output
True
:::

:::hint Stuck?
Convert to lowercase first, then use `in`: `"error" in log.lower()`
:::

:::answer Reveal answer
```python
log = "System started. No error detected."
print("error" in log.lower())
```
:::

## Exercise 4: Replace Words

Replace all occurrences of "bad" with "good":

```python live
review = "The service was bad. The food was bad too."
# Replace "bad" with "good"
# Print the new review


```

:::expected_output
The service was good. The food was good too.
:::

:::hint Stuck?
Use `replace("bad", "good")` - it replaces all occurrences.
:::

:::answer Reveal answer
```python
review = "The service was bad. The food was bad too."
new_review = review.replace("bad", "good")
print(new_review)
```
:::

## Exercise 5: File Extension Check

Check if a filename is a Python file (ends with .py):

```python live
filename = "script.py"
# Check if it ends with ".py"
# Print True or False


```

:::expected_output
True
:::

:::hint Stuck?
Use `endswith(".py")` method.
:::

:::answer Reveal answer
```python
filename = "script.py"
print(filename.endswith(".py"))
```
:::
