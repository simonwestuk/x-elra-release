---
title: "Quick Reference: Function Parameters"
slug: parameters-reference
description: "Quick syntax reference for function parameters"
course_id: PY101
module: functions
module_order: 4
topic: parameters
topic_order: 2
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - functions
  - parameters
outcomes:
  - "Quickly look up parameter syntax"
  - "Review argument passing"
capstone_relevance: "Reference for function parameter patterns"
---

## Quick Reference: Function Parameters

### Single Parameter

```python
def greet(name):
    print("Hello, " + name)

greet("Alice")  # name = "Alice"
```

### Multiple Parameters

```python
def add(a, b):
    print(a + b)

add(5, 3)  # a=5, b=3 → prints 8
```

### Parameter vs Argument

| Term | Location | Example |
|------|----------|---------|
| Parameter | Definition | `def greet(name):` |
| Argument | Call | `greet("Alice")` |

### Positional Arguments

```python
def describe(animal, name):
    print(animal + " named " + name)

describe("dog", "Max")  # Order matters!
```

### Named (Keyword) Arguments

```python
def profile(name, age, city):
    print(name, age, city)

# Any order with names
profile(city="NYC", name="Bob", age=25)
```

### Mixed Arguments

```python
def func(a, b, c):
    print(a, b, c)

func(1, c=3, b=2)  # Positional first, then named
```

### Using Parameters

```python
# In math
def area(w, h):
    return w * h

# In conditions
def check(score):
    if score >= 50:
        print("Pass")

# In strings
def hello(name):
    print("Hi " + name + "!")
```

### Common Patterns

```python
# Processing input
def process(data):
    result = data * 2
    print(result)

# Formatted output
def display(label, value):
    print(label + ": " + str(value))

# Conditional logic
def validate(n):
    if n > 0:
        print("Valid")
    else:
        print("Invalid")
```

### Errors to Avoid

| Error | Cause | Fix |
|-------|-------|-----|
| `TypeError: missing argument` | Too few arguments | Pass all required values |
| `TypeError: takes X arguments` | Too many arguments | Match parameter count |
| `NameError` | Using undefined parameter | Check spelling |

### See Also

- [Return Values](return-values-lesson.html) - Getting data back
- [Default Parameters](defaults-lesson.html) - Optional arguments

