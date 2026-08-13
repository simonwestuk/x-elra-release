---
title: "Dictionary Operations"
slug: dict-operations-lesson
description: "Learn advanced dictionary methods and patterns"
course_id: PY101
module: data-structures
module_order: 3
topic: dict-operations
topic_order: 8
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - dicts-lesson
skills:
  - data-structures
  - dict-operations
outcomes:
  - "Iterate through dictionaries"
  - "Merge and update dictionaries"
  - "Use dictionaries for counting and grouping"
capstone_relevance: "Advanced record manipulation in your application"
---

## Introduction

Beyond basic access and modification, dictionaries have powerful methods for iteration, merging, and data processing. These techniques are essential for working with structured data.

## Iterating Dictionaries

```python live
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Iterate keys
print("Keys:")
for key in person:
    print(f"  {key}")

# Iterate key-value pairs
print("\nKey-Value pairs:")
for key, value in person.items():
    print(f"  {key}: {value}")
```

:::expected_output
Keys:
  name
  age
  city

Key-Value pairs:
  name: Alice
  age: 25
  city: NYC
:::

## Iterating Values Only

```python live
prices = {"apple": 1.50, "banana": 0.75, "orange": 2.00}

total = 0
for price in prices.values():
    total += price

print(f"Total: ${total:.2f}")
```

:::expected_output
Total: $4.25
:::

## Merging Dictionaries

```python live
defaults = {"theme": "light", "font_size": 12}
user_settings = {"theme": "dark"}

# Merge (user overrides defaults)
settings = {**defaults, **user_settings}
print(settings)

# Or use update()
defaults.update(user_settings)
print(defaults)
```

:::expected_output
{'theme': 'dark', 'font_size': 12}
{'theme': 'dark', 'font_size': 12}
:::

## Counting with Dictionaries

```python live
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# Count occurrences
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print("Word counts:", counts)

# Find most common
most_common = max(counts, key=counts.get)
print(f"Most common: {most_common}")
```

:::expected_output
Word counts: {'apple': 3, 'banana': 2, 'cherry': 1}
Most common: apple
:::

## Grouping Data

```python live
people = [
    {"name": "Alice", "dept": "Sales"},
    {"name": "Bob", "dept": "IT"},
    {"name": "Carol", "dept": "Sales"},
    {"name": "Dave", "dept": "IT"},
]

# Group by department
by_dept = {}
for person in people:
    dept = person["dept"]
    if dept not in by_dept:
        by_dept[dept] = []
    by_dept[dept].append(person["name"])

print("By department:")
for dept, names in by_dept.items():
    print(f"  {dept}: {names}")
```

:::expected_output
By department:
  Sales: ['Alice', 'Carol']
  IT: ['Bob', 'Dave']
:::

## Dictionary Comprehension

```python live
# Create dict from lists
names = ["Alice", "Bob", "Carol"]
scores = [85, 92, 78]

grades = {name: score for name, score in zip(names, scores)}
print("Grades:", grades)

# Filter and transform
passing = {name: score for name, score in grades.items() if score >= 80}
print("Passing:", passing)
```

:::expected_output
Grades: {'Alice': 85, 'Bob': 92, 'Carol': 78}
Passing: {'Alice': 85, 'Bob': 92}
:::

## Nested Dictionary Access

```python live
data = {
    "user": {
        "profile": {
            "name": "Alice",
            "settings": {"theme": "dark"}
        }
    }
}

# Safe nested access
def get_nested(d, *keys, default=None):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key)
        else:
            return default
    return d if d is not None else default

theme = get_nested(data, "user", "profile", "settings", "theme")
print(f"Theme: {theme}")
```

:::expected_output
Theme: dark
:::

## Key Points

- `.items()` for key-value iteration
- `.keys()` and `.values()` for specific iteration
- `{**d1, **d2}` or `.update()` to merge
- Use `.get(key, 0)` pattern for counting
- Dict comprehensions for transforming data

:::hint Common Mistake
Modifying a dictionary while iterating over it causes RuntimeError. Create a copy or new dict instead.
:::
