---
title: "Challenge: Name Tag Generator"
slug: strings-challenge
description: "Create formatted name tags using string operations"
course_id: PY101
module: python-foundations
module_order: 1
topic: strings
topic_order: 5
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - strings-lesson
  - strings-practice
skills:
  - strings
outcomes:
  - "Combine string operations creatively"
  - "Create formatted text output"
  - "Apply string concepts to practical problems"
capstone_relevance: "Creating formatted displays for records in your application"
---

## The Challenge

Create a name tag generator that displays a person's information in a bordered box.

### Requirements

- Create a bordered box using characters like `+`, `-`, and `|`
- Display the person's name prominently
- Display their role/title
- The box should be at least 30 characters wide
- Make it look professional and aligned

### Example Output

```
+------------------------------+
|                              |
|        SARAH CONNOR          |
|       Event Coordinator      |
|                              |
+------------------------------+
```

### Given Information

```python
name = "Sarah Connor"
role = "Event Coordinator"
```

## Your Solution

```python live
name = "Sarah Connor"
role = "Event Coordinator"

# Create the name tag display




```

:::hint Approach
Start with the border. Calculate spacing to center the text. Build each line separately.
:::

:::hint Structure
Think of it as rows: top border, blank line, name line, role line, blank line, bottom border. Use string repetition for borders.
:::

:::answer Reveal full solution
```python
name = "Sarah Connor"
role = "Event Coordinator"

# Create the name tag display
border = "+" + "-" * 30 + "+"
blank_line = "|" + " " * 30 + "|"

name_display = name.upper()
name_line = "|" + name_display.center(30) + "|"
role_line = "|" + role.center(30) + "|"

print(border)
print(blank_line)
print(name_line)
print(role_line)
print(blank_line)
print(border)
```
:::
