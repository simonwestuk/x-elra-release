---
title: "Challenge: Student Report Card"
slug: list-iteration-challenge
description: "Build a report card generator using list iteration"
course_id: PY101
module: data-structures
module_order: 3
topic: list-iteration
topic_order: 4
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - list-iteration-lesson
  - list-iteration-practice
skills:
  - data-structures
  - list-iteration
outcomes:
  - "Process complex list data"
  - "Calculate statistics from iterations"
  - "Generate formatted reports"
capstone_relevance: "Generate reports from your record data"
---

## The Challenge

Create a student report card generator that processes grades and produces a formatted report.

### Requirements

Process student data to:
1. Display each subject with grade and status (Pass/Fail)
2. Calculate average grade
3. Count passed subjects (70+)
4. Determine overall status

### Test Data

```python
student = "Alice Johnson"
subjects = ["Math", "Science", "English", "History", "Art"]
grades = [85, 72, 91, 68, 88]
```

### Example Output

```
=== Report Card ===
Student: Alice Johnson

Subject Grades:
1. Math: 85 - Pass
2. Science: 72 - Pass
3. English: 91 - Pass
4. History: 68 - Fail
5. Art: 88 - Pass

Summary:
- Total Subjects: 5
- Passed: 4
- Failed: 1
- Average Grade: 80.8

Overall Status: PASSED (4 of 5 subjects)
```

## Your Solution

```python live
student = "Alice Johnson"
subjects = ["Math", "Science", "English", "History", "Art"]
grades = [85, 72, 91, 68, 88]

print("=== Report Card ===")
print(f"Student: {student}")
print()

# Generate the report




```

:::expected_output
=== Report Card ===
Student: Alice Johnson

Subject Grades:
1. Math: 85 - Pass
2. Science: 72 - Pass
3. English: 91 - Pass
4. History: 68 - Fail
5. Art: 88 - Pass

Summary:
- Total Subjects: 5
- Passed: 4
- Failed: 1
- Average Grade: 80.8

Overall Status: PASSED (4 of 5 subjects)
:::

:::hint Approach
Use zip() to iterate subjects and grades together. Track totals and pass count. Calculate average after loop.
:::

:::hint Structure
Print each subject with grade and Pass/Fail. Count passed and sum grades. Calculate average and determine overall status.
:::

:::answer Reveal full solution
```python
student = "Alice Johnson"
subjects = ["Math", "Science", "English", "History", "Art"]
grades = [85, 72, 91, 68, 88]

print("=== Report Card ===")
print(f"Student: {student}")
print()

# Generate the report
print("Subject Grades:")
passed = 0
total = 0

for i, (subject, grade) in enumerate(zip(subjects, grades), 1):
    status = "Pass" if grade >= 70 else "Fail"
    if grade >= 70:
        passed += 1
    total += grade
    print(f"{i}. {subject}: {grade} - {status}")

failed = len(subjects) - passed
average = total / len(grades)

print()
print("Summary:")
print(f"- Total Subjects: {len(subjects)}")
print(f"- Passed: {passed}")
print(f"- Failed: {failed}")
print(f"- Average Grade: {average}")

print()
print(f"Overall Status: PASSED ({passed} of {len(subjects)} subjects)")
```
:::
