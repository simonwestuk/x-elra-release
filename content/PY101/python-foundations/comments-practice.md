---
title: "Practice: Writing Comments"
slug: comments-practice
description: "Practice adding meaningful comments to code"
course_id: PY101
module: python-foundations
module_order: 1
topic: comments
topic_order: 2
type: practice
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - comments-lesson
skills:
  - foundations
  - comments
outcomes:
  - "Add comments that explain code purpose"
  - "Use comments to organize code sections"
  - "Comment out code temporarily"
capstone_relevance: "Well-commented code is easier to maintain and debug"
---

## Exercise 1: Add a Header Comment

Add a comment at the top explaining what this code does:

```python live
# Your comment here
print("Welcome to the Quiz!")
print("You have 5 questions.")
print("Good luck!")
```

:::expected_output
Welcome to the Quiz!
You have 5 questions.
Good luck!
:::

:::hint Stuck?
Describe the overall purpose: what does this code display and why?
:::

:::answer Reveal answer
```python
# Display a welcome message and instructions for the quiz
print("Welcome to the Quiz!")
print("You have 5 questions.")
print("Good luck!")
```
:::

## Exercise 2: Explain the Why

Add a comment explaining *why* this calculation is done:

```python live
seconds = 90

minutes = seconds // 60
remaining = seconds % 60
print(minutes, "minutes and", remaining, "seconds")
```

:::expected_output
1 minutes and 30 seconds
:::

:::hint Stuck?
Think about what problem this code solves. Why convert seconds?
:::

:::answer Reveal answer
```python
seconds = 90
# Convert total seconds into minutes and remaining seconds for easier reading
minutes = seconds // 60
remaining = seconds % 60
print(minutes, "minutes and", remaining, "seconds")
```
:::

## Exercise 3: Section Headers

Add section header comments to organize this code into logical groups:

```python live
name = "Product A"
price = 29.99
quantity = 3

total = price * quantity
tax = total * 0.1
final = total + tax

print("Item:", name)
print("Total:", final)
```

:::hint Stuck?
Group the code into: Setup/Data, Calculations, and Output sections.
:::

:::answer Reveal answer
```python
# --- Product Data ---
name = "Product A"
price = 29.99
quantity = 3

# --- Calculations ---
total = price * quantity
tax = total * 0.1
final = total + tax

# --- Output ---
print("Item:", name)
print("Total:", final)
```
:::

## Exercise 4: Comment Out Code

Comment out the middle print statement so only the first and last lines display:

```python live
print("Start")
print("This should be hidden")
print("End")
```

:::expected_output
Start
End
:::

:::hint Stuck?
Put # at the beginning of the line you want to hide.
:::

:::answer Reveal answer
```python
print("Start")
# print("This should be hidden")
print("End")
```
:::

## Exercise 5: Inline Comments

Add inline comments (at the end of lines) explaining each variable:

```python live
width = 10
height = 5
area = width * height
print("Area:", area)
```

:::expected_output
Area: 50
:::

:::hint Stuck?
Add `# comment` after each line to explain what that variable represents.
:::

:::answer Reveal answer
```python
width = 10  # width of the rectangle in units
height = 5  # height of the rectangle in units
area = width * height  # calculated area (width x height)
print("Area:", area)
```
:::
