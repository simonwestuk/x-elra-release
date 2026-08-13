---
title: "Quick Reference: Defining Functions"
slug: defining-functions-reference
description: "Quick syntax reference for function definitions"
course_id: PY101
module: functions
module_order: 4
topic: defining-functions
topic_order: 1
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - functions
outcomes:
  - "Quickly look up function syntax"
  - "Review function structure"
capstone_relevance: "Reference while building your application functions"
---

## Quick Reference: Defining Functions

### Basic Syntax

```python
def function_name():
    # code goes here
    pass
```

### Calling a Function

```python
function_name()  # Executes the function
```

### Complete Example

```python
def greet():
    print("Hello!")
    print("Welcome!")

greet()  # Call it
```

### Function Structure

| Part | Description |
|------|-------------|
| `def` | Keyword to define a function |
| `function_name` | Name you choose (snake_case) |
| `()` | Parentheses (required) |
| `:` | Colon (required) |
| Indented body | Code that runs when called |

### Naming Conventions

```python
# Good (snake_case)
calculate_total()
display_menu()
get_user_input()

# Avoid
CalculateTotal()   # PascalCase (for classes)
calculate-total()  # Invalid syntax
```

### Multiple Calls

```python
def say_hi():
    print("Hi!")

say_hi()  # First call
say_hi()  # Second call
say_hi()  # Third call
```

### Functions Calling Functions

```python
def header():
    print("=====")

def footer():
    print("-----")

def full_display():
    header()
    print("Content")
    footer()

full_display()
```

### Empty Function

```python
def placeholder():
    pass  # Does nothing (placeholder)
```

### Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `def greet` | Missing parentheses | `def greet():` |
| `def greet():` then no indent | No body | Add indented code |
| `greet` | Missing parentheses in call | `greet()` |
| Calling before defining | NameError | Define first |

### See Also

- [Parameters](parameters-lesson.html) - Functions with inputs
- [Return Values](return-values-lesson.html) - Getting results back

