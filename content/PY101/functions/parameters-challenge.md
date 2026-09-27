---
title: "Challenge: Build a Report Generator"
slug: parameters-challenge
description: "Create functions that generate formatted reports from data"
course_id: PY101
module: functions
module_order: 4
topic: parameters
topic_order: 2
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - parameters-practice
skills:
  - functions
  - parameters
outcomes:
  - "Design functions with appropriate parameters"
  - "Create flexible, reusable functions"
  - "Build a complete system using parameters"
capstone_relevance: "Report generation is similar to displaying records in your capstone"
---

## Challenge: Student Report Generator

Create a system of functions that generates formatted student reports.

### Requirements

1. Create `print_header(title)` that prints:
```
========================================
            [TITLE]
========================================
```
(Title should be centered and uppercase)

2. Create `print_student(name, grade)` that prints:
```
Student: [name]
Grade: [grade]
Status: [Pass/Fail based on grade >= 50]
```

3. Create `print_separator()` that prints a line of 40 dashes.

4. Create `print_footer(total_students)` that prints:
```
----------------------------------------
Total Students: [total_students]
========================================
```

5. Use all your functions to create this report:

### Your Solution

```python live
# Define your functions here




# Generate the report
print_header("Class Report")
print_student("Alice Johnson", 85)
print_separator()
print_student("Bob Smith", 42)
print_separator()
print_student("Charlie Brown", 78)
print_footer(3)
```

:::expected_output
========================================
              CLASS REPORT
========================================
Student: Alice Johnson
Grade: 85
Status: Pass
----------------------------------------
Student: Bob Smith
Grade: 42
Status: Fail
----------------------------------------
Student: Charlie Brown
Grade: 78
Status: Pass
----------------------------------------
Total Students: 3
========================================
:::

### Expected Output

```
========================================
            CLASS REPORT
========================================
Student: Alice Johnson
Grade: 85
Status: Pass
----------------------------------------
Student: Bob Smith
Grade: 42
Status: Fail
----------------------------------------
Student: Charlie Brown
Grade: 78
Status: Pass
----------------------------------------
Total Students: 3
========================================
```

:::hint Header Centering
To center text in 40 characters, use string method `.center(40)` or calculate spaces manually.
:::

:::hint Pass/Fail Logic
Use an if/else inside print_student to determine the status based on the grade parameter.
:::

:::answer Reveal full solution
```python
def print_header(title):
    print("========================================")
    print(title.upper().center(40))
    print("========================================")

def print_student(name, grade):
    print("Student: " + name)
    print("Grade: " + str(grade))
    if grade >= 50:
        print("Status: Pass")
    else:
        print("Status: Fail")

def print_separator():
    print("-" * 40)

def print_footer(total_students):
    print("-" * 40)
    print("Total Students: " + str(total_students))
    print("=" * 40)

# Generate the report
print_header("Class Report")
print_student("Alice Johnson", 85)
print_separator()
print_student("Bob Smith", 42)
print_separator()
print_student("Charlie Brown", 78)
print_footer(3)
```
:::

