---
title: "Else and Elif"
slug: else-elif-lesson
description: "Learn to handle multiple conditions with else and elif"
course_id: PY101
module: control-flow
module_order: 2
topic: else-elif
topic_order: 4
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - if-statements-lesson
skills:
  - control-flow
  - elif
outcomes:
  - "Use else for alternative actions"
  - "Chain multiple conditions with elif"
  - "Create complete decision structures"
capstone_relevance: "Handle all possible cases in your menu systems and validations"
---

## Introduction

Sometimes you need to do one thing if a condition is True, and something else if it's False. That's where `else` comes in. For multiple options, use `elif` (else if).

## If-Else

`else` runs when the `if` condition is False:

```python live
age = 15

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```

:::expected_output
You are a minor
:::

## Try It

```python live
temperature = 25

if temperature > 30:
    print("It's hot!")
else:
    print("It's not that hot")
```

:::expected_output
It's not that hot
:::

Change `temperature` to 35 and run again.

## If-Elif-Else

Use `elif` for multiple conditions:

```python live
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score}, Grade: {grade}")
```

:::expected_output
Score: 85, Grade: B
:::

Only the first matching condition runs!

## Order Matters

Python checks conditions top to bottom and stops at the first True:

```python live
value = 95

# This works correctly
if value >= 90:
    print("A")
elif value >= 80:
    print("B")
elif value >= 70:
    print("C")
```

:::expected_output
A
:::

If you reversed the order, 95 would match `>= 70` first!

## Multiple Elif Branches

```python live
day = "Saturday"

if day == "Monday":
    print("Start of work week")
elif day == "Friday":
    print("End of work week!")
elif day == "Saturday" or day == "Sunday":
    print("Weekend!")
else:
    print("Regular weekday")
```

:::expected_output
Weekend!
:::

## Without Else

`else` is optional:

```python live
number = 5

if number > 10:
    print("Big number")
elif number > 5:
    print("Medium number")
# No else - nothing prints for numbers <= 5
```

## Practical Example: Menu System

```python live
choice = "2"

print("Menu:")
print("1. View items")
print("2. Add item")
print("3. Quit")

if choice == "1":
    print("Viewing items...")
elif choice == "2":
    print("Adding new item...")
elif choice == "3":
    print("Goodbye!")
else:
    print("Invalid choice")
```

:::expected_output
Menu:
1. View items
2. Add item
3. Quit
Adding new item...
:::

## Key Points

- `else` runs when `if` is False
- `elif` checks another condition (short for "else if")
- Only one branch executes (first True condition)
- Check conditions from most specific to least specific
- `else` is optional but catches all remaining cases

:::hint Common Mistake
Forgetting colons after `elif` and `else`. Every branch needs a colon: `elif condition:` and `else:`
:::
