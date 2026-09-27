---
title: "Challenge: Document a Recipe Program"
slug: comments-challenge
description: "Apply commenting skills to document a complete program"
course_id: PY101
module: python-foundations
module_order: 1
topic: comments
topic_order: 2
type: challenge
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - comments-lesson
  - comments-practice
skills:
  - foundations
  - comments
outcomes:
  - "Write a program header comment"
  - "Organize code with section comments"
  - "Add meaningful inline comments"
capstone_relevance: "Documentation makes your capstone understandable to assessors"
---

## The Challenge

The code below works but has no comments. Your job is to add comments that make the code easy to understand for someone seeing it for the first time.

### Requirements

- Add a header comment explaining the program's purpose
- Add section comments to group related code
- Add at least 2 inline comments explaining non-obvious lines
- Don't comment obvious things (like "print hello")

### The Code to Document

```python live
print("=== Recipe Calculator ===")
print()

servings_needed = 6
original_servings = 4

flour_original = 2
sugar_original = 1
eggs_original = 3

multiplier = servings_needed / original_servings

flour_new = flour_original * multiplier
sugar_new = sugar_original * multiplier
eggs_new = eggs_original * multiplier

print("Adjusted Recipe for", servings_needed, "servings:")
print("Flour:", flour_new, "cups")
print("Sugar:", sugar_new, "cups")
print("Eggs:", eggs_new)
```

:::expected_output
=== Recipe Calculator ===

Adjusted Recipe for 6 servings:
Flour: 3.0 cups
Sugar: 1.5 cups
Eggs: 4.5
:::

:::hint Approach
Read through the code first. What does it do? Why? Then add comments that explain the purpose, not just restate the code.
:::

:::hint Structure
Consider these sections: Header/Title, Original Recipe Data, Scaling Calculation, Output Results
:::

:::answer Reveal full solution
```python
# Recipe Calculator - Scales ingredient amounts for different serving sizes

# --- Display program title ---
print("=== Recipe Calculator ===")
print()

# --- Original recipe settings ---
servings_needed = 6
original_servings = 4

flour_original = 2
sugar_original = 1
eggs_original = 3

# Calculate scaling factor based on desired vs original servings
multiplier = servings_needed / original_servings

# --- Scale each ingredient by the multiplier ---
flour_new = flour_original * multiplier
sugar_new = sugar_original * multiplier
eggs_new = eggs_original * multiplier  # eggs may need rounding in practice

# --- Display adjusted recipe ---
print("Adjusted Recipe for", servings_needed, "servings:")
print("Flour:", flour_new, "cups")
print("Sugar:", sugar_new, "cups")
print("Eggs:", eggs_new)
```
:::
