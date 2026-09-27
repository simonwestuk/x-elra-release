---
title: "Practice: Using print()"
slug: print-basics-practice
description: "Practice displaying text with the print() function"
course_id: PY101
module: python-foundations
module_order: 1
topic: print-basics
topic_order: 1
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - print-basics-lesson
skills:
  - foundations
  - print
outcomes:
  - "Write print statements independently"
  - "Create multi-line output"
  - "Use print() to display custom messages"
capstone_relevance: "You'll use print() throughout your capstone to communicate with users"
---

## Exercise 1: Say Hello

Write code to display exactly: `Hello, Python!`

```python live
# Write your code below


```

:::expected_output
Hello, Python!
:::

:::hint Stuck?
Use print() with your message in quotes: `print("your message")`
:::

:::answer Reveal answer
```python
print("Hello, Python!")
```
:::

## Exercise 2: Your Name

Write code to display your name on the screen.

```python live
# Display your name


```

:::hint Stuck?
Replace the text inside the quotes with your actual name.
:::

:::answer Reveal answer
```python
print("Alice")
```
:::

## Exercise 3: Two Lines

Display these two lines:
```
Learning Python
One step at a time
```

```python live
# Write two print statements


```

:::expected_output
Learning Python
One step at a time
:::

:::hint Stuck?
You need two separate print() statements, one for each line.
:::

:::answer Reveal answer
```python
print("Learning Python")
print("One step at a time")
```
:::

## Exercise 4: Add a Blank Line

Display this output with a blank line in the middle:
```
Part 1

Part 2
```

```python live
# Use print() three times


```

:::expected_output
Part 1

Part 2
:::

:::hint Stuck?
Use `print()` with no text inside to create a blank line.
:::

:::answer Reveal answer
```python
print("Part 1")
print()
print("Part 2")
```
:::

## Exercise 5: Recipe Header

Create output that looks like this:
```
=================
   RECIPE CARD
=================
```

```python live
# Create the recipe header


```

:::expected_output
=================
   RECIPE CARD
=================
:::

:::hint Stuck?
Use three print statements. The equals signs and text are just characters inside quotes.
:::

:::answer Reveal answer
```python
print("=================")
print("   RECIPE CARD")
print("=================")
```
:::
