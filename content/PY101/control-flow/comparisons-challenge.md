---
title: "Challenge: Eligibility Checker"
slug: comparisons-challenge
description: "Build an eligibility checker using comparisons"
course_id: PY101
module: control-flow
module_order: 2
topic: comparisons
topic_order: 1
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - comparisons-lesson
  - comparisons-practice
skills:
  - control-flow
  - comparisons
outcomes:
  - "Apply multiple comparisons to real scenarios"
  - "Create meaningful output from comparison results"
  - "Design eligibility criteria checks"
capstone_relevance: "Validate record data against business rules"
---

## The Challenge

Create a program that checks eligibility for a movie rental membership.

### Requirements

Check the following criteria and display the results:
1. Age is 18 or older (can rent any movie)
2. Age is between 13-17 (can rent PG-13 movies)
3. Has valid ID (ID number greater than 0)
4. Lives locally (zip code starts with "90")

Display each check result as True/False.

### Example Output

```
=== Membership Eligibility Check ===

Applicant Information:
- Age: 16
- ID Number: 12345
- Zip Code: 90210

Eligibility Results:
- Adult rental (18+): False
- Teen rental (13-17): True
- Valid ID: True
- Local resident: True
```

## Your Solution

```python live
# Applicant information
age = 16
id_number = 12345
zip_code = "90210"

# Perform checks and display results




```

:::expected_output
=== Membership Eligibility Check ===

Applicant Information:
- Age: 16
- ID Number: 12345
- Zip Code: 90210

Eligibility Results:
- Adult rental (18+): False
- Teen rental (13-17): True
- Valid ID: True
- Local resident: True
:::

:::hint Approach
Create a variable for each check result, then display them all in a formatted way.
:::

:::hint Structure
Use `startswith()` to check the zip code. Use chained comparison for the teen age range.
:::

:::answer Reveal full solution
```python
# Applicant information
age = 16
id_number = 12345
zip_code = "90210"

# Perform checks and display results
adult_rental = age >= 18
teen_rental = 13 <= age <= 17
valid_id = id_number > 0
local_resident = zip_code.startswith("90")

print("=== Membership Eligibility Check ===")
print()
print("Applicant Information:")
print(f"- Age: {age}")
print(f"- ID Number: {id_number}")
print(f"- Zip Code: {zip_code}")
print()
print("Eligibility Results:")
print(f"- Adult rental (18+): {adult_rental}")
print(f"- Teen rental (13-17): {teen_rental}")
print(f"- Valid ID: {valid_id}")
print(f"- Local resident: {local_resident}")
```
:::
