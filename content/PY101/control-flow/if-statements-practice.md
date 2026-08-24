---
title: "Practice: If Statements"
slug: if-statements-practice
description: "Practice writing conditional code with if statements"
course_id: PY101
module: control-flow
module_order: 2
topic: if-statements
topic_order: 3
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - if-statements-lesson
skills:
  - control-flow
  - if-else
outcomes:
  - "Write if statements with correct syntax"
  - "Use conditions to control code execution"
  - "Structure code blocks properly"
capstone_relevance: "Implement conditional logic in your application"
---

## Exercise 1: Age Check

Print "You can vote!" if age is 18 or older:

```python live
age = 21
# Write an if statement to check voting eligibility


```

:::expected_output
You can vote!
:::

:::hint Stuck?
Use `if age >= 18:` followed by an indented print statement.
:::

:::answer Reveal answer
```python
age = 21
if age >= 18:
    print("You can vote!")
```
:::

## Exercise 2: Password Length

Print "Password is strong" if it's at least 8 characters:

```python live
password = "mysecret123"
# Check password length


```

:::expected_output
Password is strong
:::

:::hint Stuck?
Use `len(password) >= 8` as your condition.
:::

:::answer Reveal answer
```python
password = "mysecret123"
if len(password) >= 8:
    print("Password is strong")
```
:::

## Exercise 3: Discount Eligibility

Apply a 10% discount if purchase is $100 or more:

```python live
purchase = 125
# If eligible, print the discount amount


```

:::expected_output
Discount: $12.5
:::

:::hint Stuck?
Calculate discount inside the if block: `discount = purchase * 0.10`
:::

:::answer Reveal answer
```python
purchase = 125
if purchase >= 100:
    discount = purchase * 0.10
    print(f"Discount: ${discount}")
```
:::

## Exercise 4: Username Exists

Print a welcome message only if username is not empty:

```python live
username = "alice"
# Check if username exists (is truthy)


```

:::hint Stuck?
Non-empty strings are truthy, so just use `if username:`
:::

:::answer Reveal answer
```python
username = "alice"
if username:
    print(f"Welcome, {username}!")
```
:::

## Exercise 5: Multiple Checks

Check if a score is passing (70+) and print two messages:

```python live
score = 85
# If passing, print "Passed!" and "Great job!"


```

:::expected_output
Passed!
Great job!
:::

:::hint Stuck?
Both print statements should be indented inside the if block.
:::

:::answer Reveal answer
```python
score = 85
if score >= 70:
    print("Passed!")
    print("Great job!")
```
:::
