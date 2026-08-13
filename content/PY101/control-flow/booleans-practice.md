---
title: "Practice: Boolean Values"
slug: booleans-practice
description: "Practice working with boolean values and truthiness"
course_id: PY101
module: control-flow
module_order: 2
topic: booleans
topic_order: 2
type: practice
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - booleans-lesson
skills:
  - control-flow
  - booleans
outcomes:
  - "Create and use boolean variables"
  - "Understand truthy and falsy evaluation"
  - "Toggle boolean values"
capstone_relevance: "Manage record states and application flags"
---

## Exercise 1: Create Flags

Create boolean variables to track: completed (True), archived (False):

```python live
# Create two boolean flag variables
# Print both


```

:::expected_output
True
False
:::

:::hint Stuck?
Use `True` and `False` (capital letters): `completed = True`
:::

:::answer Reveal answer
```python
completed = True
archived = False
print(completed)
print(archived)
```
:::

## Exercise 2: Check Truthiness

Check if these values are truthy or falsy using bool():

```python live
value1 = 0
value2 = "hello"
value3 = ""
# Print the bool() of each


```

:::expected_output
False
True
False
:::

:::hint Stuck?
Use `print(bool(value1))` for each value.
:::

:::answer Reveal answer
```python
value1 = 0
value2 = "hello"
value3 = ""
print(bool(value1))
print(bool(value2))
print(bool(value3))
```
:::

## Exercise 3: Empty Check

Check if a list has items (is truthy):

```python live
shopping_list = ["apples", "bread"]
empty_list = []
# Print whether each list has items


```

:::expected_output
True
False
:::

:::hint Stuck?
Use `bool(list_name)` - True if has items, False if empty.
:::

:::answer Reveal answer
```python
shopping_list = ["apples", "bread"]
empty_list = []
print(bool(shopping_list))
print(bool(empty_list))
```
:::

## Exercise 4: Toggle Switch

Start with a boolean set to False, toggle it twice, printing after each:

```python live
switch = False
print(f"Initial: {switch}")
# Toggle and print
# Toggle again and print


```

:::expected_output
Initial: False
After first toggle: True
After second toggle: False
:::

:::hint Stuck?
Use `switch = not switch` to flip the value.
:::

:::answer Reveal answer
```python
switch = False
print(f"Initial: {switch}")
switch = not switch
print(f"After first toggle: {switch}")
switch = not switch
print(f"After second toggle: {switch}")
```
:::

## Exercise 5: Validation Flags

Create boolean flags for form validation (has_name, has_email, has_password):

```python live
name = "Alice"
email = ""
password = "secret"

# Create flags based on whether each field has content
# Print all three flags


```

:::expected_output
True
False
True
:::

:::hint Stuck?
Use `has_name = bool(name)` - True if name has content.
:::

:::answer Reveal answer
```python
name = "Alice"
email = ""
password = "secret"

has_name = bool(name)
has_email = bool(email)
has_password = bool(password)
print(has_name)
print(has_email)
print(has_password)
```
:::
