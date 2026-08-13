---
title: "Practice: Function Parameters"
slug: parameters-practice
description: "Practice passing values to functions"
course_id: PY101
module: functions
module_order: 4
topic: parameters
topic_order: 2
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - parameters-lesson
skills:
  - functions
  - parameters
outcomes:
  - "Create functions with parameters"
  - "Call functions with correct arguments"
  - "Use multiple parameters effectively"
capstone_relevance: "Parameter passing is essential for data handling"
---

## Exercise 1: Personalised Greeting

Create a function `greet` that takes a `name` parameter and prints "Hello, [name]!".

```python live
# Define greet with a name parameter


# Test it
greet("Alice")
greet("Bob")
```

:::expected_output
Hello, Alice!
Hello, Bob!
:::

:::hint Stuck?
`def greet(name):` then use `name` in your print statement with string concatenation.
:::

:::answer Reveal answer
```python
def greet(name):
    print("Hello, " + name + "!")

# Test it
greet("Alice")
greet("Bob")
```
:::

## Exercise 2: Double a Number

Create a function `double` that takes a number and prints its doubled value.

```python live
# Define double


# Test it
double(5)   # Should print 10
double(13)  # Should print 26
```

:::expected_output
10
26
:::

:::hint Stuck?
`def double(n):` then `print(n * 2)` in the body.
:::

:::answer Reveal answer
```python
def double(n):
    print(n * 2)

# Test it
double(5)   # Should print 10
double(13)  # Should print 26
```
:::

## Exercise 3: Full Name

Create a function `full_name` that takes `first` and `last` parameters and prints the complete name.

```python live
# Define full_name with two parameters


# Test it
full_name("John", "Smith")
full_name("Jane", "Doe")
```

:::expected_output
John Smith
Jane Doe
:::

:::hint Stuck?
`def full_name(first, last):` then concatenate them with a space between.
:::

:::answer Reveal answer
```python
def full_name(first, last):
    print(first + " " + last)

# Test it
full_name("John", "Smith")
full_name("Jane", "Doe")
```
:::

## Exercise 4: Rectangle Info

Create a function `rectangle_info` that takes `width` and `height` and prints both the area and perimeter.

```python live
# Define rectangle_info


# Test it
rectangle_info(5, 3)
# Should print:
# Area: 15
# Perimeter: 16
```

:::expected_output
Area: 15
Perimeter: 16
:::

:::hint Stuck?
Area = width × height, Perimeter = 2 × (width + height). Use str() to convert numbers for printing.
:::

:::answer Reveal answer
```python
def rectangle_info(width, height):
    print("Area: " + str(width * height))
    print("Perimeter: " + str(2 * (width + height)))

# Test it
rectangle_info(5, 3)
# Should print:
# Area: 15
# Perimeter: 16
```
:::

## Exercise 5: Grade Check

Create a function `check_grade` that takes a `score` parameter and prints:
- "Pass" if score is 50 or above
- "Fail" if score is below 50

```python live
# Define check_grade


# Test it
check_grade(75)  # Pass
check_grade(45)  # Fail
check_grade(50)  # Pass
```

:::expected_output
Pass
Fail
Pass
:::

:::hint Stuck?
Use an if/else inside your function to check if `score >= 50`.
:::

:::answer Reveal answer
```python
def check_grade(score):
    if score >= 50:
        print("Pass")
    else:
        print("Fail")

# Test it
check_grade(75)  # Pass
check_grade(45)  # Fail
check_grade(50)  # Pass
```
:::

