---
title: "Challenge: Create a Business Card"
slug: print-basics-challenge
description: "Apply print() skills to create a formatted business card display"
course_id: PY101
module: python-foundations
module_order: 1
topic: print-basics
topic_order: 1
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - print-basics-lesson
  - print-basics-practice
skills:
  - foundations
  - print
outcomes:
  - "Plan multi-line output structure"
  - "Create visually formatted text displays"
  - "Apply print() in a practical scenario"
capstone_relevance: "Formatted output makes your capstone app professional and user-friendly"
---

## The Challenge

Create a business card display using only `print()` statements. Your card should look professional with borders and aligned text.

### Requirements

- Create a border around the card using characters like `+`, `-`, and `|`
- Display a name on one line
- Display a job title on another line
- Display contact info (email or phone)
- The card should have at least 5 lines of output

### Example

```
+------------------------+
|     JANE SMITH         |
|     Python Developer   |
|                        |
|     jane@example.com   |
+------------------------+
```

## Your Solution

```python live
# Build your business card here




```

:::hint Approach
Start by creating the top border, then work your way down line by line. Each line is a separate print() statement.
:::

:::hint Structure
Think of the card as rows:
1. Top border
2. Name line
3. Title line
4. Blank line (for spacing)
5. Contact line
6. Bottom border
:::

:::answer Reveal full solution
```python
print("+------------------------+")
print("|     JANE SMITH         |")
print("|     Python Developer   |")
print("|                        |")
print("|     jane@example.com   |")
print("+------------------------+")
```
:::
