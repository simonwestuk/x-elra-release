---
title: "Challenge: Grade Report Generator"
slug: for-loops-challenge
description: "Build a grade report generator using for loops"
course_id: PY101
module: control-flow
module_order: 2
topic: for-loops
topic_order: 8
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - for-loops-lesson
  - for-loops-practice
skills:
  - control-flow
  - for-loops
outcomes:
  - "Process collections with for loops"
  - "Calculate statistics from data"
  - "Format output from iterations"
capstone_relevance: "Generate reports from your data records"
---

## The Challenge

Create a grade report generator that processes student scores and produces statistics.

### Requirements

Given a list of scores, calculate and display:
1. Each score with its letter grade
2. The highest and lowest scores
3. The average score
4. Count of passing scores (70+)

### Grade Scale

- A: 90-100
- B: 80-89
- C: 70-79
- D: 60-69
- F: below 60

### Test Data

```python
scores = [85, 92, 78, 65, 88, 74, 95, 58, 81, 70]
```

### Example Output

```
=== Grade Report ===

Student Scores:
1. 85 - B
2. 92 - A
3. 78 - C
4. 65 - D
5. 88 - B
6. 74 - C
7. 95 - A
8. 58 - F
9. 81 - B
10. 70 - C

Statistics:
- Highest: 95
- Lowest: 58
- Average: 78.6
- Passing (70+): 8 of 10 students
```

## Your Solution

```python live
scores = [85, 92, 78, 65, 88, 74, 95, 58, 81, 70]

print("=== Grade Report ===")
print()

# Process scores and generate report




```

:::expected_output
=== Grade Report ===

Student Scores:
1. 85 - B
2. 92 - A
3. 78 - C
4. 65 - D
5. 88 - B
6. 74 - C
7. 95 - A
8. 58 - F
9. 81 - B
10. 70 - C

Statistics:
- Highest: 95
- Lowest: 58
- Average: 78.6
- Passing (70+): 8 of 10 students
:::

:::hint Approach
First loop prints each score with grade. Track highest, lowest, total, and passing count during iteration.
:::

:::hint Structure
Initialize tracking variables before loop. Update them inside. Calculate average and print summary after loop.
:::

:::answer Reveal full solution
```python
scores = [85, 92, 78, 65, 88, 74, 95, 58, 81, 70]

print("=== Grade Report ===")
print()

# Process scores and generate report
highest = scores[0]
lowest = scores[0]
total = 0
passing = 0

print("Student Scores:")
for i in range(len(scores)):
    score = scores[i]
    total += score

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

    if score > highest:
        highest = score
    if score < lowest:
        lowest = score
    if score >= 70:
        passing += 1

    print(f"{i + 1}. {score} - {grade}")

average = total / len(scores)

print()
print("Statistics:")
print(f"- Highest: {highest}")
print(f"- Lowest: {lowest}")
print(f"- Average: {average}")
print(f"- Passing (70+): {passing} of {len(scores)} students")
```
:::
