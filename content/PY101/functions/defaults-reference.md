---
title: "Quick Reference: Default Parameters"
slug: defaults-reference
description: "Quick syntax reference for default parameter values"
course_id: PY101
module: functions
module_order: 4
topic: defaults
topic_order: 4
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - functions
  - parameters
outcomes:
  - "Quickly look up default parameter syntax"
  - "Review parameter ordering rules"
capstone_relevance: "Reference for flexible function design"
---

## Quick Reference: Default Parameters

### Basic Syntax

```python
def greet(name="World"):
    print("Hello, " + name)

greet()         # Hello, World
greet("Alice")  # Hello, Alice
```

### Multiple Defaults

```python
def config(host="localhost", port=8080):
    print(host + ":" + str(port))

config()                    # localhost:8080
config("server.com")        # server.com:8080
config("api.com", 3000)     # api.com:3000
```

### Parameter Order

```python
# CORRECT: required before defaults
def func(required, optional="default"):
    pass

# WRONG: causes SyntaxError
def func(optional="default", required):
    pass
```

### Named Arguments

```python
def create(name, size="M", color="blue"):
    print(name, size, color)

create("Shirt")                    # Shirt M blue
create("Shirt", "L")               # Shirt L blue
create("Shirt", color="red")       # Shirt M red
create("Shirt", "XL", "green")     # Shirt XL green
```

### Common Default Values

| Type | Example |
|------|---------|
| String | `name="default"` |
| Number | `count=0`, `value=1.0` |
| Boolean | `enabled=True`, `debug=False` |
| None | `data=None` |

### Boolean Flags

```python
def search(query, case_sensitive=False):
    if case_sensitive:
        # exact match
    else:
        # ignore case
```

### Numeric Defaults

```python
def calculate(amount, tax=0, discount=0):
    total = amount + tax - discount
    return total
```

### None as Default

```python
def process(data=None):
    if data is None:
        data = []  # Create new list
    # work with data
```

### Calling Patterns

```python
def func(a, b=1, c=2):
    pass

func(0)           # a=0, b=1, c=2
func(0, 5)        # a=0, b=5, c=2
func(0, 5, 10)    # a=0, b=5, c=10
func(0, c=10)     # a=0, b=1, c=10
func(a=0, c=10)   # a=0, b=1, c=10
```

### When to Use Defaults

| Scenario | Example |
|----------|---------|
| Common case | `sort(reverse=False)` |
| Optional feature | `log(timestamp=True)` |
| Configuration | `connect(timeout=30)` |
| Flexible behavior | `format(decimals=2)` |

### See Also

- [Parameters](parameters-lesson.html) - Basic parameter usage
- [Scope](scope-lesson.html) - Variable visibility

