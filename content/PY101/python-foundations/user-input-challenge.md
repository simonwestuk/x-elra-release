---
title: "Challenge: Profile Builder"
slug: user-input-challenge
description: "Build an interactive profile creation program"
course_id: PY101
module: python-foundations
module_order: 1
topic: user-input
topic_order: 8
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - user-input-lesson
  - user-input-practice
skills:
  - input
  - type-conversion
outcomes:
  - "Design multi-input interactions"
  - "Process and display collected data"
  - "Create user-friendly prompts"
capstone_relevance: "Collect complete records from users in your application"
---

## The Challenge

Create a profile builder that collects information from the user and displays a formatted profile card.

### Requirements

Collect the following information:
1. Full name (string)
2. Age (integer)
3. Height in meters (float)
4. Email address (string)
5. Occupation (string)

Then display a formatted profile card with all the information, including:
- Calculated birth year (from age)
- Height converted to centimeters

### Example Interaction

```
=== Profile Builder ===

Enter your full name: Sarah Johnson
Enter your age: 28
Enter your height in meters: 1.68
Enter your email: sarah@example.com
Enter your occupation: Software Engineer

=== Your Profile ===
+----------------------------------+
| Name: Sarah Johnson              |
| Age: 28 (born ~1996)             |
| Height: 1.68m (168cm)            |
| Email: sarah@example.com         |
| Occupation: Software Engineer    |
+----------------------------------+
```

## Your Solution

```python live
print("=== Profile Builder ===")
print()

# Collect information




# Display the profile card




```

:::hint Approach
Collect all inputs first, then do any calculations (birth year, cm conversion), then build the display.
:::

:::hint Structure
Use appropriate conversion for each input: string for text, int for age, float for height. Remember height in cm = meters x 100.
:::

:::answer Reveal full solution
```python
print("=== Profile Builder ===")
print()

# Collect information
name = input("Enter your full name: ")
age = int(input("Enter your age: "))
height = float(input("Enter your height in meters: "))
email = input("Enter your email: ")
occupation = input("Enter your occupation: ")

# Calculate extra details
birth_year = 2026 - age
height_cm = int(height * 100)

# Display the profile card
print()
print("=== Your Profile ===")
print("+----------------------------------+")
print(f"| Name: {name:<27}|")
print(f"| Age: {age} (born ~{birth_year}){' ' * (19 - len(str(age)) - len(str(birth_year)))}|")
print(f"| Height: {height}m ({height_cm}cm){' ' * (22 - len(str(height)) - len(str(height_cm)))}|")
print(f"| Email: {email:<26}|")
print(f"| Occupation: {occupation:<21}|")
print("+----------------------------------+")
```
:::
