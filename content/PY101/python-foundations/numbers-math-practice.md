---
title: "Practice: Numbers and Math"
slug: numbers-math-practice
description: "Practice arithmetic operations and mathematical calculations"
course_id: PY101
module: python-foundations
module_order: 1
topic: numbers-math
topic_order: 4
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - numbers-math-lesson
skills:
  - numbers
  - math
outcomes:
  - "Apply arithmetic operators correctly"
  - "Solve practical calculation problems"
  - "Use appropriate division operators"
capstone_relevance: "Calculate record statistics and totals in your application"
---

## Exercise 1: Simple Calculation

Calculate and print the result of: `15 + 7 * 3`

```python live
# Calculate and print the result


```

:::expected_output
36
:::

:::hint Stuck?
Remember order of operations: multiplication happens before addition.
:::

:::answer Reveal answer
```python
print(15 + 7 * 3)
```
:::

## Exercise 2: Rectangle Area

Calculate the area of a rectangle with width 12 and height 8:

```python live
# Create variables for width and height
# Calculate and print the area


```

:::expected_output
96
:::

:::hint Stuck?
Area = width * height. Store the result in a variable before printing.
:::

:::answer Reveal answer
```python
width = 12
height = 8
area = width * height
print(area)
```
:::

## Exercise 3: Even or Odd

Use the modulo operator to check if 47 is even or odd. Print the remainder when divided by 2:

```python live
# Check if 47 is even or odd


```

:::expected_output
1
:::

:::hint Stuck?
If `number % 2` equals 0, it's even. If it equals 1, it's odd.
:::

:::answer Reveal answer
```python
remainder = 47 % 2
print(remainder)
```
:::

## Exercise 4: Time Conversion

Convert 185 minutes into hours and remaining minutes. Use floor division and modulo:

```python live
total_minutes = 185
# Calculate hours (whole number)
# Calculate remaining minutes
# Print the result


```

:::expected_output
3 hours and 5 minutes
:::

:::hint Stuck?
Hours = total_minutes // 60 (whole hours). Remaining = total_minutes % 60.
:::

:::answer Reveal answer
```python
total_minutes = 185
hours = total_minutes // 60
remaining = total_minutes % 60
print(hours, "hours and", remaining, "minutes")
```
:::

## Exercise 5: Shopping Cart

Calculate the final price with a 15% discount:
- Original price: $89.99
- Discount: 15%

```python live
original_price = 89.99
discount_percent = 15
# Calculate the discount amount
# Calculate the final price
# Print both


```

:::hint Stuck?
Discount amount = original_price * (discount_percent / 100). Final = original - discount.
:::

:::answer Reveal answer
```python
original_price = 89.99
discount_percent = 15
discount_amount = original_price * (discount_percent / 100)
final_price = original_price - discount_amount
print("Discount:", discount_amount)
print("Final price:", final_price)
```
:::
