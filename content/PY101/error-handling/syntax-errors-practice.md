---
title: "Practice: Fixing Syntax Errors"
slug: syntax-errors-practice
description: "Practice identifying and fixing syntax errors"
course_id: PY101
module: error-handling
module_order: 5
topic: syntax-errors
topic_order: 1
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - syntax-errors-lesson
skills:
  - debugging
  - errors
outcomes:
  - "Identify syntax errors in code"
  - "Fix common syntax mistakes"
  - "Read error messages effectively"
capstone_relevance: "Debugging is a daily skill for developers"
---

## Exercise 1: Missing Colon

This code has a missing colon. Find and fix it.

```python live
# Fix the syntax error
if True
    print("This should work!")
```

:::expected_output
This should work!
:::

:::hint Stuck?
The `if` statement needs a colon at the end: `if True:`
:::

:::answer Reveal answer
```python
# Fix the syntax error
if True:
    print("This should work!")
```
:::

## Exercise 2: Unmatched Parenthesis

Fix the parenthesis error in this code.

```python live
# Fix the syntax error
print("Hello, World!"
print("Second line")
```

:::expected_output
Hello, World!
Second line
:::

:::hint Stuck?
The first print statement is missing a closing parenthesis.
:::

:::answer Reveal answer
```python
# Fix the syntax error
print("Hello, World!")
print("Second line")
```
:::

## Exercise 3: Indentation Error

Fix the indentation in this function.

```python live
# Fix the indentation
def say_hello():
print("Hello!")
print("How are you?")

say_hello()
```

:::expected_output
Hello!
How are you?
:::

:::hint Stuck?
The print statements inside the function need to be indented with 4 spaces.
:::

:::answer Reveal answer
```python
# Fix the indentation
def say_hello():
    print("Hello!")
    print("How are you?")

say_hello()
```
:::

## Exercise 4: Quote Mismatch

Fix the string quote error.

```python live
# Fix the quote error
message = "Welcome to Python!'
print(message)
```

:::expected_output
Welcome to Python!
:::

:::hint Stuck?
The opening quote is a double quote but the closing is a single quote. They must match.
:::

:::answer Reveal answer
```python
# Fix the quote error
message = "Welcome to Python!"
print(message)
```
:::

## Exercise 5: Multiple Errors

This code has THREE syntax errors. Find and fix all of them.

```python live
# Fix all three errors
def calculate(x, y)
    result = x + y
    print("The sum is: " + str(result)
    return result

calculate(5, 3
```

:::expected_output
The sum is: 8
:::

:::hint Error 1
The function definition is missing a colon after `(x, y)`.
:::

:::hint Error 2
The print statement is missing a closing parenthesis.
:::

:::hint Error 3
The function call is missing a closing parenthesis.
:::

:::answer Reveal answer
```python
# Fix all three errors
def calculate(x, y):
    result = x + y
    print("The sum is: " + str(result))
    return result

calculate(5, 3)
```
:::

