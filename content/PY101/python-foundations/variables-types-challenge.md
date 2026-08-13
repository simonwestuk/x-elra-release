---
title: "Challenge: Personal Profile"
slug: variables-types-challenge
description: "Create a complete personal profile using multiple variable types"
course_id: PY101
module: python-foundations
module_order: 1
topic: variables-types
topic_order: 3
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - variables-types-lesson
  - variables-types-practice
skills:
  - variables
  - types
outcomes:
  - "Design a set of related variables"
  - "Use appropriate data types for different information"
  - "Create organized, readable output"
capstone_relevance: "Your capstone will store records with multiple fields of different types"
---

## The Challenge

Create a complete personal profile using variables of different types, then display it in a formatted way.

### Requirements

- Create at least 6 variables covering all 4 data types (str, int, float, bool)
- Include: name, age, height (in meters), employment status
- Add at least 2 more variables of your choice
- Display all information in a readable format
- Use descriptive variable names

### Example Output

```
=== Personal Profile ===
Name: Alex Johnson
Age: 28 years
Height: 1.75 meters
Employed: True
Favorite Number: 7
Account Balance: $1234.56
```

## Your Solution

```python live
# Create your profile variables here




# Display the profile




```

:::hint Approach
Start by listing what information you want to store. Decide the best type for each piece of data, then create the variables.
:::

:::hint Structure
Group your variables by type or by meaning. Use blank print() lines to add spacing in your output.
:::

:::answer Reveal full solution
```python
# Create your profile variables here
name = "Alex Johnson"
age = 28
height = 1.75
employed = True
favorite_number = 7
account_balance = 1234.56

# Display the profile
print("=== Personal Profile ===")
print("Name:", name)
print("Age:", age, "years")
print("Height:", height, "meters")
print("Employed:", employed)
print("Favorite Number:", favorite_number)
print("Account Balance: $" + str(account_balance))
```
:::
