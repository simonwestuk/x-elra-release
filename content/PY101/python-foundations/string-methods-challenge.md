---
title: "Challenge: Text Analyzer"
slug: string-methods-challenge
description: "Build a text analyzer using string methods"
course_id: PY101
module: python-foundations
module_order: 1
topic: string-methods
topic_order: 6
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - string-methods-lesson
  - string-methods-practice
skills:
  - strings
  - string-methods
outcomes:
  - "Combine multiple string methods"
  - "Extract information from text"
  - "Create a practical text processing tool"
capstone_relevance: "Analyze and process text data in your application"
---

## The Challenge

Create a text analyzer that examines a sentence and reports various statistics and transformations.

### Requirements

Given a sentence, your analyzer should:
1. Show the original text
2. Show the text in uppercase
3. Count the total characters (including spaces)
4. Count the words (split by spaces)
5. Check if it contains the word "Python"
6. Replace spaces with underscores and show the result

### Example Output

```
=== Text Analyzer ===

Original: I love learning Python programming
Uppercase: I LOVE LEARNING PYTHON PROGRAMMING
Characters: 35
Words: 5
Contains 'Python': True
Underscored: I_love_learning_Python_programming
```

## Your Solution

```python live
text = "I love learning Python programming"

# Create your text analyzer




```

:::expected_output
=== Text Analyzer ===

Original: I love learning Python programming
Uppercase: I LOVE LEARNING PYTHON PROGRAMMING
Characters: 34
Words: 5
Contains 'Python': True
Underscored: I_love_learning_Python_programming
:::

:::hint Approach
Work through each requirement one at a time. Use the appropriate method for each task: upper(), len(), split(), in, replace().
:::

:::hint Structure
Print a header first, then tackle each analysis one by one. Use descriptive labels for each output.
:::

:::answer Reveal full solution
```python
text = "I love learning Python programming"

# Create your text analyzer
print("=== Text Analyzer ===")
print()
print("Original:", text)
print("Uppercase:", text.upper())
print("Characters:", len(text))
print("Words:", len(text.split()))
print("Contains 'Python':", "Python" in text)
print("Underscored:", text.replace(" ", "_"))
```
:::
