---
title: "Quick Reference: Refactoring"
slug: refactoring-reference
description: "Quick reference for code refactoring techniques"
course_id: PY101
module: building-apps
module_order: 7
topic: refactoring
topic_order: 5
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - refactoring
  - code-quality
outcomes:
  - "Quick lookup for refactoring techniques"
  - "Review code improvement patterns"
capstone_relevance: "Refactoring reference for your project"
---

## Quick Reference: Refactoring

### Common Techniques

| Technique | Before | After |
|-----------|--------|-------|
| Rename | `def f(x):` | `def calculate_total(items):` |
| Extract Function | 50-line function | 5 small functions |
| Replace Magic Number | `if score > 90:` | `if score > GRADE_A_THRESHOLD:` |
| Simplify Conditional | Nested if/else | Guard clauses |
| Remove Duplication | Copy-pasted code | Shared function |

### Rename for Clarity

```python
# Bad names
def f(l, n):
    return [x for x in l if x > n]

# Good names
def filter_above_threshold(numbers, threshold):
    return [num for num in numbers if num > threshold]
```

### Extract Function

```python
# Before: Long function
def process(data):
    # validate (10 lines)
    # calculate (10 lines)
    # format (10 lines)
    pass

# After: Small functions
def validate(data): pass
def calculate(data): pass
def format_output(result): pass

def process(data):
    validate(data)
    result = calculate(data)
    return format_output(result)
```

### Replace Magic Numbers

```python
# Before
if total > 100:
    total = total * 0.9

# After
DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.9

if total > DISCOUNT_THRESHOLD:
    total = total * DISCOUNT_RATE
```

### Simplify Conditionals

```python
# Before: Nested
if a:
    if b:
        if c:
            return True
return False

# After: Guard clauses
if not a:
    return False
if not b:
    return False
if not c:
    return False
return True

# Or combined
return a and b and c
```

### Remove Duplication

```python
# Before: Duplicated
def process_user(user):
    print("Name:", user["name"])
    print("Email:", user["email"])

def process_admin(admin):
    print("Name:", admin["name"])
    print("Email:", admin["email"])
    print("Role: Admin")

# After: Shared
def print_person(person, role=None):
    print("Name:", person["name"])
    print("Email:", person["email"])
    if role:
        print("Role:", role)
```

### Use Comprehensions

```python
# Before: Verbose loop
result = []
for item in items:
    if item["active"]:
        result.append(item["name"])

# After: Comprehension
result = [item["name"] for item in items if item["active"]]
```

### Code Smells to Fix

| Smell | Problem | Fix |
|-------|---------|-----|
| Long function | >20 lines | Extract functions |
| Deep nesting | >3 levels | Use guard clauses |
| Magic numbers | Unexplained values | Use constants |
| Duplicate code | Copy-paste | Create function |
| Bad names | Single letters | Descriptive names |
| Giant class | Too much responsibility | Split into parts |

### When to Refactor

| Timing | Reason |
|--------|--------|
| Before adding feature | Clean foundation |
| After bug fix | Prevent future bugs |
| During code review | Fresh perspective |
| When confused | Improve understanding |
| When code smells | Quality improvement |

### Refactoring Steps

1. Identify the problem
2. Make small change
3. Test it works
4. Repeat

### Quick Checklist

- [ ] Are names meaningful?
- [ ] Are functions small?
- [ ] Are magic numbers named?
- [ ] Is code DRY (Don't Repeat Yourself)?
- [ ] Are conditions simple?
- [ ] Is structure clear?

### See Also

- [Program Structure](program-structure-lesson.html) - Code organization
- [Functions](defining-functions-lesson.html) - Function design
- [Docstrings](docstrings-lesson.html) - Documentation

