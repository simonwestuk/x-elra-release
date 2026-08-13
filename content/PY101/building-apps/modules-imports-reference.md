---
title: "Quick Reference: Modules and Imports"
slug: modules-imports-reference
description: "Quick reference for Python modules and import syntax"
course_id: PY101
module: building-apps
module_order: 7
topic: modules-imports
topic_order: 2
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - modules
  - imports
outcomes:
  - "Quick lookup for import syntax"
  - "Review common modules"
capstone_relevance: "Module reference for your project"
---

## Quick Reference: Modules and Imports

### Import Syntax

```python
# Import entire module
import math
math.sqrt(16)

# Import specific items
from math import sqrt, pi
sqrt(16)

# Import with alias
import math as m
m.sqrt(16)

# Import all (avoid this)
from math import *
```

### Common Modules

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `math` | Mathematics | `sqrt`, `ceil`, `floor`, `pi` |
| `random` | Randomness | `randint`, `choice`, `shuffle` |
| `time` | Time functions | `time`, `sleep`, `localtime` |
| `datetime` | Dates/times | `datetime.now`, `date.today` |
| `json` | JSON data | `dumps`, `loads` |
| `re` | Regex | `search`, `findall`, `sub` |

### math Module

```python
import math

math.sqrt(16)      # 4.0
math.ceil(4.2)     # 5
math.floor(4.8)    # 4
math.pow(2, 3)     # 8.0
math.pi            # 3.14159...
math.e             # 2.71828...
```

### random Module

```python
import random

random.randint(1, 10)     # Random int 1-10
random.random()           # Random float 0-1
random.choice([1,2,3])    # Random item
random.shuffle(list)      # Shuffle in place
random.sample(list, 3)    # 3 random items
```

### datetime Module

```python
from datetime import datetime, date, timedelta

datetime.now()            # Current datetime
date.today()              # Current date
date(2024, 1, 15)        # Specific date
timedelta(days=7)        # 7-day duration
date.today() + timedelta(days=30)  # 30 days from now
```

### time Module

```python
import time

time.time()               # Unix timestamp
time.sleep(1)             # Pause 1 second
time.localtime()          # Local time struct
```

### json Module

```python
import json

# Python → JSON string
json.dumps({"a": 1})      # '{"a": 1}'

# JSON string → Python
json.loads('{"a": 1}')    # {'a': 1}
```

### re Module (Regex)

```python
import re

re.search(r'\d+', text)          # Find pattern
re.findall(r'\d+', text)         # Find all matches
re.sub(r'\d+', 'X', text)        # Replace
re.split(r'\s+', text)           # Split by pattern
```

### Import Best Practices

| Do | Don't |
|----|-------|
| Put imports at top | Import inside functions |
| Import specific items | Use `from x import *` |
| Group related imports | Scatter imports |
| Use aliases for long names | Use confusing aliases |

### Import Order

```python
# 1. Standard library
import os
import sys

# 2. Third-party (if any)
# import requests

# 3. Local modules
# from myproject import utils
```

### See Also

- [Program Structure](program-structure-lesson.html) - Code organization
- [Functions](defining-functions-lesson.html) - Creating functions

