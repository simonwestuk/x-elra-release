---
title: "Practice: String Formatting"
slug: string-formatting-practice
description: "Practice creating formatted output with f-strings"
course_id: PY101
module: python-foundations
module_order: 1
topic: string-formatting
topic_order: 7
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - string-formatting-lesson
skills:
  - strings
  - formatting
outcomes:
  - "Create formatted strings with variables"
  - "Format numbers and percentages"
  - "Build aligned output"
capstone_relevance: "Display records professionally in your application"
---

## Exercise 1: Simple Greeting

Create a greeting message using f-string formatting:

```python live
name = "Alex"
city = "London"
# Create and print: "Hello, Alex! Welcome to London."


```

:::expected_output
Hello, Alex! Welcome to London.
:::

:::hint Stuck?
Use f-string: `f"Hello, {name}! Welcome to {city}."`
:::

:::answer Reveal answer
```python
name = "Alex"
city = "London"
print(f"Hello, {name}! Welcome to {city}.")
```
:::

## Exercise 2: Price Display

Format a price to always show 2 decimal places:

```python live
price = 9.5
# Print the price as "$9.50"


```

:::expected_output
$9.50
:::

:::hint Stuck?
Use `:.2f` for 2 decimal places: `f"${price:.2f}"`
:::

:::answer Reveal answer
```python
price = 9.5
print(f"${price:.2f}")
```
:::

## Exercise 3: Large Number

Format a large number with comma separators:

```python live
sales = 1234567
# Print: "Total sales: 1,234,567"


```

:::expected_output
Total sales: 1,234,567
:::

:::hint Stuck?
Use `:,` for comma separators: `f"{sales:,}"`
:::

:::answer Reveal answer
```python
sales = 1234567
print(f"Total sales: {sales:,}")
```
:::

## Exercise 4: Percentage

Calculate and display a percentage:

```python live
correct = 18
total = 20
# Calculate the percentage and display as "Score: 90.0%"


```

:::expected_output
Score: 90.0%
:::

:::hint Stuck?
Divide to get the ratio, then use `:.1%` to format: `f"{correct/total:.1%}"`
:::

:::answer Reveal answer
```python
correct = 18
total = 20
print(f"Score: {correct/total:.1%}")
```
:::

## Exercise 5: Aligned Table Row

Create a formatted row with the item left-aligned (15 chars) and price right-aligned (10 chars):

```python live
item = "Laptop"
price = 999.99
# Print a row like: "Laptop           $999.99"


```

:::expected_output
Laptop         $    999.99
:::

:::hint Stuck?
Use `{item:<15}` for left-align and `{price:>10.2f}` for right-align with decimals.
:::

:::answer Reveal answer
```python
item = "Laptop"
price = 999.99
print(f"{item:<15}${price:>10.2f}")
```
:::
