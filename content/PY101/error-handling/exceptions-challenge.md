---
title: "Challenge: Exception Detective"
slug: exceptions-challenge
description: "Identify and fix exception-causing code"
course_id: PY101
module: error-handling
module_order: 5
topic: exceptions
topic_order: 2
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - exceptions-practice
skills:
  - debugging
  - errors
  - exceptions
outcomes:
  - "Analyze code for potential exceptions"
  - "Fix code to prevent exceptions"
  - "Add defensive checks"
capstone_relevance: "Writing defensive code prevents runtime crashes"
---

## Challenge: Fix the Data Processor

This data processing program has several bugs that cause exceptions. Your job is to:
1. Identify what exception each bug would cause
2. Fix the code to work correctly

### The Buggy Code

```python live
# This program processes student data
# It has 5 bugs that cause exceptions - fix them all!

def get_student_grade(students, name):
    """Get a student's grade."""
    # Bug 1: What if name isn't in students?
    return students[name]

def calculate_average(scores):
    """Calculate average of scores."""
    # Bug 2: What if scores is empty?
    total = sum(scores)
    return total / len(scores)

def get_letter_grade(percentage):
    """Convert percentage to letter grade."""
    # Bug 3: What if percentage is a string?
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    return "F"

def get_score_at_position(scores, position):
    """Get score at a specific position."""
    # Bug 4: What if position is out of range?
    return scores[position]

def parse_score(score_string):
    """Parse a score from string input."""
    # Bug 5: What if score_string isn't a valid number?
    return int(score_string)


# Test the functions
students = {"Alice": 95, "Bob": 87}
scores = [85, 92, 78, 95, 88]

# These should all work after fixes:
print("Testing get_student_grade:")
print("Alice:", get_student_grade(students, "Alice"))
print("Unknown:", get_student_grade(students, "Unknown"))

print("\nTesting calculate_average:")
print("Average:", calculate_average(scores))
print("Empty list:", calculate_average([]))

print("\nTesting get_letter_grade:")
print("95 ->", get_letter_grade(95))
print("'85' ->", get_letter_grade("85"))

print("\nTesting get_score_at_position:")
print("Position 0:", get_score_at_position(scores, 0))
print("Position 100:", get_score_at_position(scores, 100))

print("\nTesting parse_score:")
print("Parse '42':", parse_score("42"))
print("Parse 'abc':", parse_score("abc"))
```

:::expected_output
Testing get_student_grade:
Alice: 95
Unknown: None

Testing calculate_average:
Average: 87.6
Empty list: 0

Testing get_letter_grade:
95 -> A
'85' -> B

Testing get_score_at_position:
Position 0: 85
Position 100: None

Testing parse_score:
Parse '42': 42
Parse 'abc': None
:::

### Expected Output (after fixes)

```
Testing get_student_grade:
Alice: 95
Unknown: None

Testing calculate_average:
Average: 87.6
Empty list: 0

Testing get_letter_grade:
95 -> A
'85' -> B

Testing get_score_at_position:
Position 0: 85
Position 100: None

Testing parse_score:
Parse '42': 42
Parse 'abc': None
```

:::hint Bug 1 - KeyError
Use `students.get(name)` which returns `None` if key doesn't exist, or check `if name in students:` first.
:::

:::hint Bug 2 - ZeroDivisionError
Check `if len(scores) == 0:` before dividing, and return 0 or appropriate value.
:::

:::hint Bug 3 - TypeError
Convert to int first: `percentage = int(percentage)` or check the type.
:::

:::hint Bug 4 - IndexError
Check `if position < len(scores):` before accessing, or use try/except.
:::

:::hint Bug 5 - ValueError
Use try/except around `int()` or check if string is numeric with `.isdigit()`.
:::

:::answer Reveal full solution
```python
# This program processes student data
# It has 5 bugs that cause exceptions - fix them all!

def get_student_grade(students, name):
    """Get a student's grade."""
    # Fix 1: Use .get() to avoid KeyError
    return students.get(name)

def calculate_average(scores):
    """Calculate average of scores."""
    # Fix 2: Check for empty list to avoid ZeroDivisionError
    if len(scores) == 0:
        return 0
    total = sum(scores)
    return total / len(scores)

def get_letter_grade(percentage):
    """Convert percentage to letter grade."""
    # Fix 3: Convert to int to avoid TypeError
    percentage = int(percentage)
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    return "F"

def get_score_at_position(scores, position):
    """Get score at a specific position."""
    # Fix 4: Check position is in range to avoid IndexError
    if position < len(scores):
        return scores[position]
    return None

def parse_score(score_string):
    """Parse a score from string input."""
    # Fix 5: Use try/except to avoid ValueError
    try:
        return int(score_string)
    except ValueError:
        return None


# Test the functions
students = {"Alice": 95, "Bob": 87}
scores = [85, 92, 78, 95, 88]

# These should all work after fixes:
print("Testing get_student_grade:")
print("Alice:", get_student_grade(students, "Alice"))
print("Unknown:", get_student_grade(students, "Unknown"))

print("\nTesting calculate_average:")
print("Average:", calculate_average(scores))
print("Empty list:", calculate_average([]))

print("\nTesting get_letter_grade:")
print("95 ->", get_letter_grade(95))
print("'85' ->", get_letter_grade("85"))

print("\nTesting get_score_at_position:")
print("Position 0:", get_score_at_position(scores, 0))
print("Position 100:", get_score_at_position(scores, 100))

print("\nTesting parse_score:")
print("Parse '42':", parse_score("42"))
print("Parse 'abc':", parse_score("abc"))
```
:::

