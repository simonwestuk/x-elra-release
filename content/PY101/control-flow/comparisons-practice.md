---
title: "Practice: Comparison Operators"
slug: comparisons-practice
description: "Practice comparing values with comparison operators"
course_id: PY101
module: control-flow
module_order: 2
topic: comparisons
topic_order: 1
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - comparisons-lesson
skills:
  - control-flow
  - comparisons
outcomes:
  - "Apply comparison operators correctly"
  - "Compare different types of values"
  - "Store and use comparison results"
capstone_relevance: "Filter and validate data based on comparisons"
---

## Exercise 1: Age Check

Check if a person is an adult (18 or older):

```python live
age = 21
# Write a comparison that checks if age is 18 or older
# Print the result


```

:::expected_output
True
:::

:::hint Stuck?
Use `>=` for "greater than or equal to": `age >= 18`
:::

:::answer Reveal answer
```python
age = 21
is_adult = age >= 18
print(is_adult)
```
:::

## Exercise 2: Password Match

Check if two passwords match:

```python live
password = "secret123"
confirm = "secret123"
# Check if they're equal and print the result


```

:::expected_output
True
:::

:::hint Stuck?
Use `==` to compare: `password == confirm`
:::

:::answer Reveal answer
```python
password = "secret123"
confirm = "secret123"
result = password == confirm
print(result)
```
:::

## Exercise 3: Price Range

Check if a price is within budget ($50 or less):

```python live
price = 45.99
budget = 50.00
# Check if price is within budget


```

:::expected_output
True
:::

:::hint Stuck?
Use `<=` for "less than or equal to": `price <= budget`
:::

:::answer Reveal answer
```python
price = 45.99
budget = 50.00
within_budget = price <= budget
print(within_budget)
```
:::

## Exercise 4: Case-Insensitive Check

Check if two names match, ignoring case:

```python live
name1 = "John"
name2 = "JOHN"
# Compare them ignoring case


```

:::expected_output
True
:::

:::hint Stuck?
Convert both to lowercase before comparing: `name1.lower() == name2.lower()`
:::

:::answer Reveal answer
```python
name1 = "John"
name2 = "JOHN"
match = name1.lower() == name2.lower()
print(match)
```
:::

## Exercise 5: Range Check

Check if a temperature is in the comfortable range (60-80):

```python live
temp = 72
# Check if temp is between 60 and 80 (inclusive)


```

:::expected_output
True
:::

:::hint Stuck?
Use a chained comparison: `60 <= temp <= 80` or two comparisons combined.
:::

:::answer Reveal answer
```python
temp = 72
is_comfortable = 60 <= temp <= 80
print(is_comfortable)
```
:::
