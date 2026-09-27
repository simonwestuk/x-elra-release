---
title: "Quick Reference: Comments"
slug: comments-reference
description: "Quick syntax reference for Python comments"
course_id: PY101
module: python-foundations
module_order: 1
topic: comments
topic_order: 2
type: reference
difficulty: beginner
estimated_minutes: 4
prerequisites: []
skills:
  - foundations
  - comments
outcomes:
  - "Quickly look up comment syntax"
  - "Review comment best practices"
capstone_relevance: "Reference for documenting your capstone code"
---

## Quick Reference: Comments

### Basic Syntax

```python
# Single line comment
code_here  # Inline comment
```

### Common Patterns

| Pattern | Example |
|---------|---------|
| Full line | `# This explains the next line` |
| Inline | `x = 5  # Store the count` |
| Section header | `# --- Section Name ---` |
| Commented code | `# print("disabled")` |

### Examples

```python
# Calculate area of a rectangle
width = 10
height = 5
area = width * height  # width times height
```

```python
# --- Configuration ---
max_items = 100
debug_mode = False

# --- Main Logic ---
print("Starting...")
```

### Best Practices

| Do | Don't |
|-----|-------|
| Explain *why* | State the obvious |
| Be concise | Write paragraphs |
| Keep comments updated | Leave outdated comments |
| Use section headers | Comment every line |

### Comment Templates

```python
# Purpose: [what this code does]
# Input: [what it needs]
# Output: [what it produces]
```

### Common Errors

- **SyntaxError** - Comment symbol `#` inside a string is not a comment: `print("Use # for comments")` prints the # literally.

### See Also

- [Docstrings](docstrings-lesson.html) - Multi-line documentation for functions
