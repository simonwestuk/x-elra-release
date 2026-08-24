---
title: "Practice: User Input"
slug: user-input-practice
description: "Practice capturing and processing user input"
course_id: PY101
module: python-foundations
module_order: 1
topic: user-input
topic_order: 8
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - user-input-lesson
skills:
  - input
  - type-conversion
outcomes:
  - "Capture user input effectively"
  - "Convert input to appropriate types"
  - "Build interactive programs"
capstone_relevance: "Handle user interaction in your data application"
---

## Exercise 1: Greeting

Ask the user for their name and print a personalised greeting:

```python live
# Ask for name
# Print "Hello, [name]! Nice to meet you."


```

:::hint Stuck?
Use `input("prompt")` to get the name, then use an f-string to greet them.
:::

:::answer Reveal answer
```python
# Note: input() does not work in the browser
name = input("What is your name? ")
print(f"Hello, {name}! Nice to meet you.")
```
:::

## Exercise 2: Age Calculator

Ask for the user's birth year and calculate their age:

```python live
# Ask for birth year (remember to convert!)
# Calculate age (use 2024 as current year)
# Print their age


```

:::hint Stuck?
Convert input to int: `birth_year = int(input("prompt"))`. Then subtract from 2024.
:::

:::answer Reveal answer
```python
# Note: input() does not work in the browser
birth_year = int(input("What year were you born? "))
age = 2024 - birth_year
print(f"You are {age} years old.")
```
:::

## Exercise 3: Rectangle Area

Ask for width and height, then calculate and display the area:

```python live
# Get width and height as floats
# Calculate area
# Display with 2 decimal places


```

:::hint Stuck?
Use `float(input("prompt"))` for decimal numbers. Format output with `:.2f`.
:::

:::answer Reveal answer
```python
# Note: input() does not work in the browser
width = float(input("Enter width: "))
height = float(input("Enter height: "))
area = width * height
print(f"Area: {area:.2f}")
```
:::

## Exercise 4: Temperature Converter

Ask for a temperature in Celsius and convert to Fahrenheit:
Formula: F = C × 9/5 + 32

```python live
# Get Celsius temperature
# Convert to Fahrenheit
# Display both values


```

:::hint Stuck?
Get input as float, apply the formula, then display both values with the f-string.
:::

:::answer Reveal answer
```python
# Note: input() does not work in the browser
celsius = float(input("Enter temperature in Celsius: "))
fahrenheit = celsius * 9/5 + 32
print(f"{celsius}°C = {fahrenheit}°F")
```
:::

## Exercise 5: Clean Input

Ask a yes/no question and normalize the response to lowercase without extra spaces:

```python live
# Ask "Do you want to continue? (yes/no): "
# Clean the input (strip and lowercase)
# Print the cleaned response


```

:::hint Stuck?
Chain methods: `answer = input("prompt").strip().lower()`
:::

:::answer Reveal answer
```python
# Note: input() does not work in the browser
answer = input("Do you want to continue? (yes/no): ").strip().lower()
print(answer)
```
:::
