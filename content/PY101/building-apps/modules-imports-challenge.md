---
title: "Challenge: Build a Quiz Game"
slug: modules-imports-challenge
description: "Create an interactive quiz game using multiple modules"
course_id: PY101
module: building-apps
module_order: 7
topic: modules-imports
topic_order: 2
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - modules-imports-practice
skills:
  - modules
  - imports
outcomes:
  - "Combine multiple modules in one application"
  - "Use random for game mechanics"
  - "Apply datetime for timing"
capstone_relevance: "Real applications use many modules together"
---

## Challenge: Math Quiz Game

Build an interactive math quiz game that uses multiple modules.

### Requirements

Use these modules:
- `random` - Generate quiz questions and shuffle
- `time` - Track quiz duration
- `math` - Create mathematical questions

### Features

1. Generate random math questions (add, subtract, multiply)
2. Track score and time taken
3. Show different difficulty levels
4. Display final statistics

### Your Solution

```python live
import random
import time
import math

# ============ QUIZ CONFIGURATION ============
QUESTIONS_PER_QUIZ = 5
DIFFICULTY_RANGES = {
    "easy": (1, 10),
    "medium": (10, 50),
    "hard": (50, 100)
}

# ============ QUESTION GENERATION ============
def generate_question(difficulty="easy"):
    """Generate a random math question."""
    min_val, max_val = DIFFICULTY_RANGES[difficulty]
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)

    operation = random.choice(["+", "-", "*"])

    if operation == "+":
        answer = a + b
    elif operation == "-":
        answer = a - b
    else:
        answer = a * b

    question = str(a) + " " + operation + " " + str(b)
    return question, answer

def generate_quiz(num_questions, difficulty):
    """Generate a complete quiz."""
    # Your code here - return list of (question, answer) tuples
    pass

# ============ QUIZ LOGIC ============
def check_answer(user_answer, correct_answer):
    """Check if user's answer is correct."""
    # Your code here
    pass

def calculate_score(correct, total):
    """Calculate percentage score."""
    # Your code here
    pass

def get_grade(percentage):
    """Convert percentage to letter grade."""
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    return "F"

# ============ DISPLAY FUNCTIONS ============
def display_header():
    print("=" * 40)
    print("      MATH QUIZ CHALLENGE")
    print("=" * 40)

def display_question(number, question):
    print("\nQuestion " + str(number) + ": " + question + " = ?")

def display_result(is_correct, correct_answer):
    if is_correct:
        print("✓ Correct!")
    else:
        print("✗ Wrong! The answer was " + str(correct_answer))

def display_summary(correct, total, time_taken, difficulty):
    percentage = calculate_score(correct, total)
    grade = get_grade(percentage)

    print("\n" + "=" * 40)
    print("         QUIZ COMPLETE!")
    print("=" * 40)
    print("Difficulty:", difficulty)
    print("Score:", str(correct) + "/" + str(total))
    print("Percentage:", str(percentage) + "%")
    print("Grade:", grade)
    print("Time:", str(round(time_taken, 1)) + " seconds")
    print("=" * 40)

# ============ MAIN GAME ============
def run_quiz(difficulty="easy"):
    """Run a complete quiz session."""
    display_header()
    print("Difficulty:", difficulty)

    # Generate questions
    quiz = generate_quiz(QUESTIONS_PER_QUIZ, difficulty)
    if not quiz:
        print("Quiz generation not implemented yet!")
        return

    # Track score and time
    correct = 0
    start_time = time.time()

    # Simulated answers (since we can't get real input)
    # In a real app, you'd use input()
    simulated_answers = []
    for q, a in quiz:
        # Simulate: 80% chance of correct answer
        if random.random() < 0.8:
            simulated_answers.append(a)
        else:
            simulated_answers.append(a + random.randint(1, 5))

    # Run through questions
    for i, (question, answer) in enumerate(quiz):
        display_question(i + 1, question)
        user_answer = simulated_answers[i]
        print("Your answer:", user_answer)

        is_correct = check_answer(user_answer, answer)
        display_result(is_correct, answer)

        if is_correct:
            correct += 1

    # Calculate time taken
    end_time = time.time()
    time_taken = end_time - start_time

    # Show summary
    display_summary(correct, QUESTIONS_PER_QUIZ, time_taken, difficulty)


# Run quizzes at different difficulties
print("\n--- EASY QUIZ ---")
run_quiz("easy")

print("\n--- MEDIUM QUIZ ---")
run_quiz("medium")
```

### Expected Output

```
--- EASY QUIZ ---
========================================
      MATH QUIZ CHALLENGE
========================================
Difficulty: easy

Question 1: 5 + 3 = ?
Your answer: 8
✓ Correct!

Question 2: 7 - 2 = ?
Your answer: 5
✓ Correct!

[... more questions ...]

========================================
         QUIZ COMPLETE!
========================================
Difficulty: easy
Score: 4/5
Percentage: 80%
Grade: B
Time: 0.1 seconds
========================================
```

:::hint Generate Quiz
Use list comprehension: `[generate_question(difficulty) for _ in range(num_questions)]`
:::

:::hint Calculate Score
`int((correct / total) * 100)` gives the percentage.
:::

:::hint Check Answer
Convert both to same type and compare: `int(user_answer) == int(correct_answer)`
:::

:::answer Reveal full solution
```python
import random
import time
import math

# ============ QUIZ CONFIGURATION ============
QUESTIONS_PER_QUIZ = 5
DIFFICULTY_RANGES = {
    "easy": (1, 10),
    "medium": (10, 50),
    "hard": (50, 100)
}

# ============ QUESTION GENERATION ============
def generate_question(difficulty="easy"):
    """Generate a random math question."""
    min_val, max_val = DIFFICULTY_RANGES[difficulty]
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)

    operation = random.choice(["+", "-", "*"])

    if operation == "+":
        answer = a + b
    elif operation == "-":
        answer = a - b
    else:
        answer = a * b

    question = str(a) + " " + operation + " " + str(b)
    return question, answer

def generate_quiz(num_questions, difficulty):
    """Generate a complete quiz."""
    return [generate_question(difficulty) for _ in range(num_questions)]

# ============ QUIZ LOGIC ============
def check_answer(user_answer, correct_answer):
    """Check if user's answer is correct."""
    return int(user_answer) == int(correct_answer)

def calculate_score(correct, total):
    """Calculate percentage score."""
    if total == 0:
        return 0
    return int((correct / total) * 100)

def get_grade(percentage):
    """Convert percentage to letter grade."""
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    return "F"

# ============ DISPLAY FUNCTIONS ============
def display_header():
    print("=" * 40)
    print("      MATH QUIZ CHALLENGE")
    print("=" * 40)

def display_question(number, question):
    print("\nQuestion " + str(number) + ": " + question + " = ?")

def display_result(is_correct, correct_answer):
    if is_correct:
        print("✓ Correct!")
    else:
        print("✗ Wrong! The answer was " + str(correct_answer))

def display_summary(correct, total, time_taken, difficulty):
    percentage = calculate_score(correct, total)
    grade = get_grade(percentage)

    print("\n" + "=" * 40)
    print("         QUIZ COMPLETE!")
    print("=" * 40)
    print("Difficulty:", difficulty)
    print("Score:", str(correct) + "/" + str(total))
    print("Percentage:", str(percentage) + "%")
    print("Grade:", grade)
    print("Time:", str(round(time_taken, 1)) + " seconds")
    print("=" * 40)

# ============ MAIN GAME ============
def run_quiz(difficulty="easy"):
    """Run a complete quiz session."""
    display_header()
    print("Difficulty:", difficulty)

    # Generate questions
    quiz = generate_quiz(QUESTIONS_PER_QUIZ, difficulty)
    if not quiz:
        print("Quiz generation not implemented yet!")
        return

    # Track score and time
    correct = 0
    start_time = time.time()

    # Simulated answers (since we can't get real input)
    # In a real app, you'd use input()
    simulated_answers = []
    for q, a in quiz:
        # Simulate: 80% chance of correct answer
        if random.random() < 0.8:
            simulated_answers.append(a)
        else:
            simulated_answers.append(a + random.randint(1, 5))

    # Run through questions
    for i, (question, answer) in enumerate(quiz):
        display_question(i + 1, question)
        user_answer = simulated_answers[i]
        print("Your answer:", user_answer)

        is_correct = check_answer(user_answer, answer)
        display_result(is_correct, answer)

        if is_correct:
            correct += 1

    # Calculate time taken
    end_time = time.time()
    time_taken = end_time - start_time

    # Show summary
    display_summary(correct, QUESTIONS_PER_QUIZ, time_taken, difficulty)


# Run quizzes at different difficulties
print("\n--- EASY QUIZ ---")
run_quiz("easy")

print("\n--- MEDIUM QUIZ ---")
run_quiz("medium")
```
:::

