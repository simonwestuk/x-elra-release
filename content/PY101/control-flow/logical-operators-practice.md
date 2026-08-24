---
title: "Practice: Logical Operators"
slug: logical-operators-practice
description: "Practice combining conditions with and, or, not"
course_id: PY101
module: control-flow
module_order: 2
topic: logical-operators
topic_order: 5
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - logical-operators-lesson
skills:
  - control-flow
  - logic
outcomes:
  - "Combine conditions effectively"
  - "Choose the right logical operator"
  - "Build complex validation rules"
capstone_relevance: "Create sophisticated filters and validation in your application"
---

## Exercise 1: Both Conditions

Check if both username AND password are provided:

```python live
username = "alice"
password = "secret"
# Print "Login ready" if both exist


```

:::expected_output
Login ready
:::

:::hint Stuck?
Use `if username and password:` - both must be truthy.
:::

:::answer Reveal answer
```python
username = "alice"
password = "secret"
if username and password:
    print("Login ready")
```
:::

## Exercise 2: Either Condition

Give a discount if customer is a student OR a senior:

```python live
is_student = False
is_senior = True
# Print "Discount applied" if either is True


```

:::expected_output
Discount applied
:::

:::hint Stuck?
Use `if is_student or is_senior:`
:::

:::answer Reveal answer
```python
is_student = False
is_senior = True
if is_student or is_senior:
    print("Discount applied")
```
:::

## Exercise 3: Negation

Show login prompt only if user is NOT logged in:

```python live
logged_in = False
# Print "Please log in" if not logged in


```

:::expected_output
Please log in
:::

:::hint Stuck?
Use `if not logged_in:`
:::

:::answer Reveal answer
```python
logged_in = False
if not logged_in:
    print("Please log in")
```
:::

## Exercise 4: Age Range

Check if age is between 13 and 19 (inclusive) for teen discount:

```python live
age = 16
# Print "Teen discount!" if in range


```

:::expected_output
Teen discount!
:::

:::hint Stuck?
Use `if age >= 13 and age <= 19:` or `if 13 <= age <= 19:`
:::

:::answer Reveal answer
```python
age = 16
if 13 <= age <= 19:
    print("Teen discount!")
```
:::

## Exercise 5: Complex Condition

Allow access if user is admin OR (is verified AND has premium):

```python live
is_admin = False
is_verified = True
has_premium = True
# Print "Access granted" based on the rules


```

:::expected_output
Access granted
:::

:::hint Stuck?
Use `if is_admin or (is_verified and has_premium):`
:::

:::answer Reveal answer
```python
is_admin = False
is_verified = True
has_premium = True
if is_admin or (is_verified and has_premium):
    print("Access granted")
```
:::
