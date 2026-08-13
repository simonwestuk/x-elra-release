---
title: "Modules and Imports"
slug: modules-imports-lesson
description: "Learn to use Python's built-in modules and organize code"
course_id: PY101
module: building-apps
module_order: 7
topic: modules-imports
topic_order: 2
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - program-structure-lesson
skills:
  - modules
  - imports
outcomes:
  - "Import and use built-in modules"
  - "Understand import syntax variations"
  - "Use common standard library modules"
capstone_relevance: "Modules provide ready-made functionality for your app"
---

## Introduction

**Modules** are Python files containing functions, classes, and variables that you can use in your programs. Python comes with many built-in modules (the "standard library") that provide useful functionality.

## Basic Import

```python live
import math

# Use functions from the math module
print("Square root of 16:", math.sqrt(16))
print("Pi:", math.pi)
print("Ceiling of 4.3:", math.ceil(4.3))
print("Floor of 4.7:", math.floor(4.7))
```

:::expected_output
Square root of 16: 4.0
Pi: 3.141592653589793
Ceiling of 4.3: 5
Floor of 4.7: 4
:::

## Import Specific Items

```python live
from math import sqrt, pi

# Use directly without module prefix
print("Square root of 25:", sqrt(25))
print("Pi:", pi)
```

:::expected_output
Square root of 25: 5.0
Pi: 3.141592653589793
:::

## Import with Alias

```python live
import math as m

print("Using alias 'm':")
print("sqrt(9):", m.sqrt(9))
print("pow(2, 10):", m.pow(2, 10))
```

:::expected_output
Using alias 'm':
sqrt(9): 3.0
pow(2, 10): 1024.0
:::

## The random Module

```python live
import random

# Random number between 1 and 10
print("Random int:", random.randint(1, 10))

# Random float between 0 and 1
print("Random float:", random.random())

# Random choice from list
colors = ["red", "green", "blue", "yellow"]
print("Random color:", random.choice(colors))

# Shuffle a list
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print("Shuffled:", numbers)
```

## The time Module

```python live
import time

print("Current time (timestamp):", time.time())

# Format current time
# Note: Some time functions may have limited support in browser
local_time = time.localtime()
print("Year:", local_time.tm_year)
print("Month:", local_time.tm_mon)
print("Day:", local_time.tm_mday)
```

## The datetime Module

```python live
from datetime import datetime, date

# Current date and time
now = datetime.now()
print("Now:", now)

# Today's date
today = date.today()
print("Today:", today)

# Create specific date
birthday = date(1990, 5, 15)
print("Birthday:", birthday)

# Calculate age in days
age_days = (today - birthday).days
print("Days since birthday:", age_days)
```

## The re Module (Regular Expressions)

```python live
import re

text = "Contact us at support@example.com or sales@example.com"

# Find all email addresses
emails = re.findall(r'\S+@\S+', text)
print("Found emails:", emails)

# Check if text matches pattern
if re.search(r'support', text):
    print("Contains 'support'")

# Replace text
new_text = re.sub(r'example\.com', 'company.com', text)
print("Replaced:", new_text)
```

:::expected_output
Found emails: ['support@example.com', 'sales@example.com']
Contains 'support'
Replaced: Contact us at support@company.com or sales@company.com
:::

## The json Module (Concept)

```python live
import json

# Convert Python dict to JSON string
data = {"name": "Alice", "age": 30, "city": "New York"}
json_string = json.dumps(data)
print("JSON:", json_string)

# Convert JSON string back to Python dict
parsed = json.loads(json_string)
print("Parsed:", parsed)
print("Name:", parsed["name"])
```

:::expected_output
JSON: {"name": "Alice", "age": 30, "city": "New York"}
Parsed: {'name': 'Alice', 'age': 30, 'city': 'New York'}
Name: Alice
:::

## Common Built-in Modules

| Module | Purpose |
|--------|---------|
| `math` | Mathematical functions |
| `random` | Random number generation |
| `time` | Time-related functions |
| `datetime` | Date and time handling |
| `re` | Regular expressions |
| `json` | JSON encoding/decoding |
| `os` | Operating system interface |
| `sys` | System-specific parameters |

## Import Best Practices

```python live
# GOOD: Imports at top of file
import math
import random

# GOOD: Group standard library imports
# import os
# import sys

# GOOD: Specific imports for frequently used items
from datetime import datetime

# AVOID: Import everything (pollutes namespace)
# from math import *

def calculate_circle(radius):
    """Example using imported modules."""
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    return area, circumference

area, circ = calculate_circle(5)
print("Circle with radius 5:")
print("Area:", round(area, 2))
print("Circumference:", round(circ, 2))
```

:::expected_output
Circle with radius 5:
Area: 78.54
Circumference: 31.42
:::

## Key Points

- `import module` - import entire module
- `from module import item` - import specific items
- `import module as alias` - use a shorter name
- Put imports at the top of your file
- The standard library has many useful modules
- Avoid `from module import *`

:::hint Note
In the browser environment, some modules have limited functionality. When running Python locally, all standard library modules are fully available.
:::

