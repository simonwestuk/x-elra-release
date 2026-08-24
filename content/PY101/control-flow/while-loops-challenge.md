---
title: "Challenge: Number Guessing Game"
slug: while-loops-challenge
description: "Build a number guessing game using while loops"
course_id: PY101
module: control-flow
module_order: 2
topic: while-loops
topic_order: 7
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - while-loops-lesson
  - while-loops-practice
skills:
  - control-flow
  - while-loops
outcomes:
  - "Design game loops"
  - "Track state across iterations"
  - "Provide feedback within loops"
capstone_relevance: "Create interactive loops in your application"
---

## The Challenge

Create a number guessing game where the player tries to guess a secret number.

### Requirements

1. Secret number is 42
2. Player keeps guessing until correct
3. After each guess, tell them "Higher" or "Lower"
4. Track the number of attempts
5. Congratulate them with their attempt count

### Example Interaction

```
=== Number Guessing Game ===
I'm thinking of a number between 1 and 100.

Your guess: 50
Too high! Guess lower.

Your guess: 25
Too low! Guess higher.

Your guess: 37
Too low! Guess higher.

Your guess: 42
CORRECT! You got it in 4 attempts!
```

## Your Solution

```python live
secret = 42
attempts = 0

print("=== Number Guessing Game ===")
print("I'm thinking of a number between 1 and 100.")
print()

# Game loop




```

:::hint Approach
Use a while loop that continues until the guess equals the secret. Increment attempts each time. Compare guess to secret for hints.
:::

:::hint Structure
Get input, increment counter, compare to secret. If wrong, give hint and continue. If right, break out and show results.
:::

:::answer Reveal full solution
```python
secret = 42
attempts = 0

print("=== Number Guessing Game ===")
print("I'm thinking of a number between 1 and 100.")
print()

# Game loop
# Simulate guesses since we can't use input()
guesses = [50, 25, 37, 42]

for guess in guesses:
    attempts += 1
    print(f"Your guess: {guess}")

    if guess > secret:
        print("Too high! Guess lower.")
    elif guess < secret:
        print("Too low! Guess higher.")
    else:
        print(f"CORRECT! You got it in {attempts} attempts!")
        break
    print()
```
:::
