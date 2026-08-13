---
title: "Challenge: Score Analyzer"
slug: list-operations-challenge
description: "Build a score analyzer using list operations"
course_id: PY101
module: data-structures
module_order: 3
topic: list-operations
topic_order: 2
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - list-operations-lesson
  - list-operations-practice
skills:
  - data-structures
  - list-operations
outcomes:
  - "Apply multiple list operations"
  - "Generate statistical summaries"
  - "Present sorted and analyzed data"
capstone_relevance: "Analyze and report on your application data"
---

## The Challenge

Create a comprehensive score analyzer that processes and reports on a list of test scores.

### Requirements

1. Display original scores
2. Sort and display in descending order
3. Calculate statistics (min, max, average)
4. Show top 3 scores
5. Show bottom 3 scores
6. Count scores above average

### Example Output

```
=== Score Analyzer ===

Original Scores: [78, 92, 85, 90, 65, 88, 76, 95, 82, 70]

Sorted (High to Low): [95, 92, 90, 88, 85, 82, 78, 76, 70, 65]

Statistics:
- Highest: 95
- Lowest: 65
- Average: 82.1
- Total Students: 10

Top 3 Scores: [95, 92, 90]
Bottom 3 Scores: [70, 76, 78]

Above Average (82.1): 5 students
```

## Your Solution

```python live
scores = [78, 92, 85, 90, 65, 88, 76, 95, 82, 70]

print("=== Score Analyzer ===")
print()

# Your analysis code here




```

:::expected_output
=== Score Analyzer ===

Original Scores: [78, 92, 85, 90, 65, 88, 76, 95, 82, 70]

Sorted (High to Low): [95, 92, 90, 88, 85, 82, 78, 76, 70, 65]

Statistics:
- Highest: 95
- Lowest: 65
- Average: 82.1
- Total Students: 10

Top 3 Scores: [95, 92, 90]
Bottom 3 Scores: [65, 70, 76]

Above Average (82.1): 5 students
:::

:::hint Approach
Create a sorted copy (don't modify original). Use slicing for top/bottom 3. Count above average with a loop.
:::

:::hint Structure
Print original, create sorted copy, calculate stats, extract subsets, count above average.
:::

:::answer Reveal full solution
```python
scores = [78, 92, 85, 90, 65, 88, 76, 95, 82, 70]

print("=== Score Analyzer ===")
print()

# Display original scores
print(f"Original Scores: {scores}")
print()

# Sort and display in descending order
sorted_scores = sorted(scores, reverse=True)
print(f"Sorted (High to Low): {sorted_scores}")
print()

# Calculate statistics
highest = max(scores)
lowest = min(scores)
average = sum(scores) / len(scores)
total_students = len(scores)

print("Statistics:")
print(f"- Highest: {highest}")
print(f"- Lowest: {lowest}")
print(f"- Average: {average}")
print(f"- Total Students: {total_students}")
print()

# Top 3 and bottom 3
top_3 = sorted_scores[:3]
bottom_3 = sorted_scores[-3:]
bottom_3.reverse()

print(f"Top 3 Scores: {top_3}")
print(f"Bottom 3 Scores: {bottom_3}")
print()

# Count above average
above_average = 0
for score in scores:
    if score > average:
        above_average += 1

print(f"Above Average ({average}): {above_average} students")
```
:::
