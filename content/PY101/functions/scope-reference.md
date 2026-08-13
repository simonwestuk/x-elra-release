---
title: "Quick Reference: Variable Scope"
slug: scope-reference
description: "Quick reference for variable scope in Python"
course_id: PY101
module: functions
module_order: 4
topic: scope
topic_order: 5
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - functions
  - scope
outcomes:
  - "Quickly review scope rules"
  - "Understand global keyword usage"
capstone_relevance: "Reference for scope when debugging"
---

## Quick Reference: Variable Scope

### Local vs Global

```python
global_var = "I'm global"

def my_function():
    local_var = "I'm local"
    print(global_var)   # Can read global
    print(local_var)    # Can read local
```

### Scope Rules

| Location | Scope | Accessible Where |
|----------|-------|------------------|
| Outside functions | Global | Everywhere |
| Inside function | Local | Only in that function |
| Function parameter | Local | Only in that function |

### Reading Global Variables

```python
name = "Alice"  # Global

def greet():
    print("Hi " + name)  # Can read global

greet()  # Hi Alice
```

### Modifying Global Variables

```python
count = 0

def increment():
    global count  # Required to modify
    count += 1

increment()
print(count)  # 1
```

### Local Shadows Global

```python
x = "global"

def func():
    x = "local"  # New local variable
    print(x)     # Prints "local"

func()
print(x)  # Still "global"
```

### Global Keyword Rules

| Action | Need `global`? |
|--------|---------------|
| Read global variable | No |
| Modify global variable | Yes |
| Create new local with same name | No |

### Each Function Has Own Scope

```python
def func_a():
    x = 1  # Local to func_a

def func_b():
    x = 2  # Local to func_b (different x)
```

### Parameters Are Local

```python
def greet(name):  # name is local
    print(name)

greet("Bob")
# print(name)  # Error: name not defined here
```

### Common Patterns

```python
# Constants (read-only globals)
MAX_SIZE = 100
PI = 3.14159

def calculate(r):
    return PI * r * r

# Stateful globals (with global keyword)
counter = 0

def increment():
    global counter
    counter += 1
```

### Best Practices

| Practice | Why |
|----------|-----|
| Minimize globals | Reduces bugs |
| Use parameters | Explicit data flow |
| Use return values | Clear outputs |
| Name globals UPPERCASE | Shows they're constants |

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `UnboundLocalError` | Modify global without `global` | Add `global var` |
| `NameError` | Access local outside function | Return the value |
| Unexpected value | Local shadows global | Use different names |

### See Also

- [Functions](defining-functions-lesson.html) - Function basics
- [Parameters](parameters-lesson.html) - Function inputs
- [Return Values](return-values-lesson.html) - Function outputs

