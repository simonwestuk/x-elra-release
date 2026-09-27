---
title: "Quick Reference: Docstrings"
slug: docstrings-reference
description: "Quick reference for documenting functions"
course_id: PY101
module: functions
module_order: 4
topic: docstrings
topic_order: 6
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - functions
  - documentation
outcomes:
  - "Quickly reference docstring formats"
  - "Review documentation conventions"
capstone_relevance: "Documentation reference for your project"
---

## Quick Reference: Docstrings

### Basic Syntax

```python
def function_name():
    """Brief description of function."""
    pass
```

### Single-Line Docstring

```python
def add(a, b):
    """Return the sum of a and b."""
    return a + b
```

### Multi-Line Docstring

```python
def process(data, options=None):
    """
    Process the input data.

    Parameters:
        data: The input data to process
        options: Optional configuration dict

    Returns:
        Processed data as a string
    """
    pass
```

### Full Template

```python
def function_name(param1, param2, optional=default):
    """
    Brief one-line description.

    Longer description if needed. Can span
    multiple lines.

    Parameters:
        param1: Description of param1
        param2: Description of param2
        optional: Description (default: value)

    Returns:
        Description of return value

    Raises:
        ErrorType: When this error occurs

    Example:
        >>> function_name(1, 2)
        3
    """
    pass
```

### Accessing Docstrings

```python
# Using __doc__
print(function_name.__doc__)

# Using help()
help(function_name)
```

### Common Sections

| Section | Purpose |
|---------|---------|
| First line | Brief summary |
| Parameters | Describe inputs |
| Returns | Describe output |
| Raises | Document exceptions |
| Example | Usage demonstration |
| Notes | Additional info |

### Style Guidelines

| Rule | Example |
|------|---------|
| Start with capital letter | `"""Return the sum."""` |
| End with period | `"""Calculate area."""` |
| Use triple quotes | `"""..."""` |
| First line is summary | Fits on one line |
| Blank line before sections | See template |

### Docstring vs Comment

```python
def func():
    """Docstring: WHAT and HOW to use."""
    # Comment: internal notes
    pass
```

| Feature | Docstring | Comment |
|---------|-----------|---------|
| Syntax | `"""..."""` | `# ...` |
| Audience | Users | Developers |
| Purpose | How to use | How it works |
| Accessible | `.__doc__` | No |

### Quick Examples

```python
# Getter
def get_name():
    """Return the user's name."""

# Setter
def set_name(name):
    """Set the user's name."""

# Boolean
def is_valid():
    """Return True if valid."""

# Calculator
def calculate(x, y):
    """
    Calculate result from x and y.

    Returns:
        The calculated value
    """
```

### See Also

- [Defining Functions](defining-functions-lesson.html) - Function basics
- [Parameters](parameters-lesson.html) - Function inputs
- [Return Values](return-values-lesson.html) - Function outputs

