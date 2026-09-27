---
title: "Challenge: Seating Chart"
slug: nested-loops-challenge
description: "Build a seating chart display using nested loops"
course_id: PY101
module: control-flow
module_order: 2
topic: nested-loops
topic_order: 10
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - nested-loops-lesson
  - nested-loops-practice
skills:
  - control-flow
  - nested-loops
outcomes:
  - "Design nested loop solutions"
  - "Format grid-based output"
  - "Process 2D data structures"
capstone_relevance: "Display tabular data from your records"
---

## The Challenge

Create a seating chart display for a small theater.

### Requirements

Given seat data, create a visual display showing:
1. Row labels (A, B, C...)
2. Seat numbers (1, 2, 3...)
3. Occupied seats marked with [X]
4. Available seats marked with [ ]
5. Summary of available/occupied seats per row

### Seating Data

```python
seats = [
    [True, True, False, True, True],    # Row A
    [True, False, False, False, True],  # Row B
    [False, False, False, False, False],# Row C
    [True, True, True, True, True],     # Row D
]
# True = occupied, False = available
```

### Example Output

```
=== Theater Seating Chart ===

     1   2   3   4   5
A   [X] [X] [ ] [X] [X]  (4 occupied, 1 available)
B   [X] [ ] [ ] [ ] [X]  (2 occupied, 3 available)
C   [ ] [ ] [ ] [ ] [ ]  (0 occupied, 5 available)
D   [X] [X] [X] [X] [X]  (5 occupied, 0 available)

Total: 11 occupied, 9 available
```

## Your Solution

```python live
seats = [
    [True, True, False, True, True],
    [True, False, False, False, True],
    [False, False, False, False, False],
    [True, True, True, True, True],
]
row_labels = ["A", "B", "C", "D"]

print("=== Theater Seating Chart ===")
print()

# Create the seating display




```

:::expected_output
=== Theater Seating Chart ===

     1   2   3   4   5
A   [X] [X] [ ] [X] [X]  (4 occupied, 1 available)
B   [X] [ ] [ ] [ ] [X]  (2 occupied, 3 available)
C   [ ] [ ] [ ] [ ] [ ]  (0 occupied, 5 available)
D   [X] [X] [X] [X] [X]  (5 occupied, 0 available)

Total: 11 occupied, 9 available
:::

:::hint Approach
First print the column numbers. Then loop through rows, printing the row label, each seat, and the row summary.
:::

:::hint Structure
Track occupied/available counts for each row. Use chr(65 + i) for row labels or use the row_labels list. Use "[X]" or "[ ]" based on True/False.
:::

:::answer Reveal full solution
```python
seats = [
    [True, True, False, True, True],
    [True, False, False, False, True],
    [False, False, False, False, False],
    [True, True, True, True, True],
]
row_labels = ["A", "B", "C", "D"]

print("=== Theater Seating Chart ===")
print()

# Create the seating display
# Print column headers
print("     ", end="")
for col in range(1, len(seats[0]) + 1):
    print(f"{col}   ", end="")
print()

total_occupied = 0
total_available = 0

for i in range(len(seats)):
    row = seats[i]
    label = row_labels[i]
    occupied = 0
    available = 0

    print(f"{label}   ", end="")
    for seat in row:
        if seat:
            print("[X] ", end="")
            occupied += 1
        else:
            print("[ ] ", end="")
            available += 1

    print(f" ({occupied} occupied, {available} available)")
    total_occupied += occupied
    total_available += available

print()
print(f"Total: {total_occupied} occupied, {total_available} available")
```
:::
