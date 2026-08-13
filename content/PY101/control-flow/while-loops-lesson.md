---
title: "While Loops"
slug: while-loops-lesson
description: "Learn to repeat code while a condition is true"
course_id: PY101
module: control-flow
module_order: 2
topic: while-loops
topic_order: 7
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - if-statements-lesson
  - comparisons-lesson
skills:
  - control-flow
  - while-loops
outcomes:
  - "Write while loops with proper conditions"
  - "Avoid infinite loops"
  - "Use while loops for input validation"
capstone_relevance: "Keep your menu running until user chooses to quit"
---

## Introduction

While loops repeat code as long as a condition is True. They're perfect for when you don't know how many times you need to repeat something.

## Basic While Loop

```python
while condition:
    # code repeats while condition is True
```

## Try It: Counting

```python live
count = 1
while count <= 5:
    print(count)
    count = count + 1

print("Done!")
```

:::expected_output
1
2
3
4
5
Done!
:::

## The Loop Flow

1. Check condition
2. If True, run the block
3. Go back to step 1
4. If False, exit loop

```python live
number = 10
while number > 0:
    print(f"Countdown: {number}")
    number = number - 1

print("Liftoff!")
```

:::expected_output
Countdown: 10
Countdown: 9
Countdown: 8
Countdown: 7
Countdown: 6
Countdown: 5
Countdown: 4
Countdown: 3
Countdown: 2
Countdown: 1
Liftoff!
:::

## Updating the Condition Variable

You MUST change something that affects the condition, or the loop runs forever:

```python live
total = 0
current = 1

while current <= 5:
    total = total + current
    print(f"Added {current}, total is {total}")
    current = current + 1  # This is crucial!

print(f"Final total: {total}")
```

:::expected_output
Added 1, total is 1
Added 2, total is 3
Added 3, total is 6
Added 4, total is 10
Added 5, total is 15
Final total: 15
:::

## While with User Input

Perfect for asking until valid input is received:

```python live
password = ""
while password != "secret":
    password = input("Enter password: ")
    if password != "secret":
        print("Wrong password, try again")

print("Access granted!")
```

## Accumulator Pattern

Building up a result over iterations:

```python live
numbers = [4, 7, 2, 9, 1]
index = 0
total = 0

while index < len(numbers):
    total = total + numbers[index]
    index = index + 1

print(f"Sum: {total}")
```

:::expected_output
Sum: 23
:::

## While True with Break

Sometimes it's cleaner to use `while True` with `break`:

```python live
attempts = 0
while True:
    guess = input("Guess the number (1-10): ")
    attempts = attempts + 1

    if guess == "7":
        print(f"Correct! Took {attempts} attempts")
        break  # Exit the loop
    else:
        print("Try again!")
```

## Avoiding Infinite Loops

```python
# DANGER: This runs forever!
# count = 1
# while count > 0:  # Always true!
#     print(count)
#     count = count + 1

# Always ensure the condition can become False
count = 1
while count <= 5:
    print(count)
    count = count + 1  # Eventually makes count > 5
```

## Key Points

- `while condition:` repeats while True
- Must update something to eventually make condition False
- Great for unknown number of repetitions
- Use `break` to exit early when needed
- Be careful to avoid infinite loops

:::hint Common Mistake
Forgetting to update the loop variable. If nothing changes, the condition stays True forever, creating an infinite loop.
:::
