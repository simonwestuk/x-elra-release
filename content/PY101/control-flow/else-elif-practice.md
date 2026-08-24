---
title: "Practice: Else and Elif"
slug: else-elif-practice
description: "Practice handling multiple conditions with else and elif"
course_id: PY101
module: control-flow
module_order: 2
topic: else-elif
topic_order: 4
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - else-elif-lesson
skills:
  - control-flow
  - elif
outcomes:
  - "Write if-else structures"
  - "Chain multiple conditions with elif"
  - "Handle all cases appropriately"
capstone_relevance: "Implement complete menu and validation logic"
---

## Exercise 1: Pass or Fail

Print "Pass" if score is 60+, otherwise print "Fail":

```python live
score = 55
# Use if-else to determine pass or fail


```

:::expected_output
Fail
:::

:::hint Stuck?
Use `if score >= 60:` followed by print, then `else:` with another print.
:::

:::answer Reveal answer
```python
score = 55
if score >= 60:
    print("Pass")
else:
    print("Fail")
```
:::

## Exercise 2: Sign Check

Print "Positive", "Negative", or "Zero" based on the number:

```python live
number = -5
# Use if-elif-else to check the sign


```

:::expected_output
Negative
:::

:::hint Stuck?
Check `> 0` first, then `< 0`, then `else` for zero.
:::

:::answer Reveal answer
```python
number = -5
if number > 0:
    print("Positive")
elif number < 0:
    print("Negative")
else:
    print("Zero")
```
:::

## Exercise 3: Letter Grade

Convert a numeric score to a letter grade (A: 90+, B: 80-89, C: 70-79, D: 60-69, F: below 60):

```python live
score = 78
# Determine and print the letter grade


```

:::expected_output
C
:::

:::hint Stuck?
Check from highest to lowest: `if score >= 90`, `elif score >= 80`, etc.
:::

:::answer Reveal answer
```python
score = 78
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")
```
:::

## Exercise 4: Shipping Cost

Calculate shipping: Free if order >= $50, otherwise $5.99:

```python live
order_total = 35.00
# Determine shipping cost and print it


```

:::expected_output
Shipping cost: $5.99
:::

:::hint Stuck?
Use if-else: one branch sets shipping to 0, the other to 5.99.
:::

:::answer Reveal answer
```python
order_total = 35.00
if order_total >= 50:
    shipping = 0
else:
    shipping = 5.99
print(f"Shipping cost: ${shipping}")
```
:::

## Exercise 5: Age Category

Categorize age: Child (0-12), Teen (13-19), Adult (20-64), Senior (65+):

```python live
age = 45
# Determine and print the age category


```

:::expected_output
Adult
:::

:::hint Stuck?
Use if-elif-elif-else structure. Check ranges from specific to general.
:::

:::answer Reveal answer
```python
age = 45
if age <= 12:
    print("Child")
elif age <= 19:
    print("Teen")
elif age <= 64:
    print("Adult")
else:
    print("Senior")
```
:::
