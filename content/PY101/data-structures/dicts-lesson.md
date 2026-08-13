---
title: "Dictionaries"
slug: dicts-lesson
description: "Learn to store key-value pairs with dictionaries"
course_id: PY101
module: data-structures
module_order: 3
topic: dicts
topic_order: 7
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - lists-lesson
skills:
  - data-structures
  - dicts
outcomes:
  - "Create dictionaries with key-value pairs"
  - "Access, add, and modify values"
  - "Check for key existence"
capstone_relevance: "Store records as dictionaries with named fields"
---

## Introduction

Dictionaries store data as key-value pairs. Instead of accessing items by position (like lists), you access them by name. This makes them perfect for storing structured data like user profiles or product information.

## Creating Dictionaries

Use curly braces `{}` with `key: value` pairs:

```python live
# Empty dictionary
empty = {}

# Dictionary with data
person = {
    "name": "Alice",
    "age": 25,
    "city": "London"
}

print(person)
```

:::expected_output
{'name': 'Alice', 'age': 25, 'city': 'London'}
:::

## Accessing Values

Use the key in square brackets:

```python live
product = {
    "name": "Laptop",
    "price": 999.99,
    "in_stock": True
}

print(product["name"])
print(product["price"])
```

:::expected_output
Laptop
999.99
:::

## Safe Access with get()

`get()` returns None (or default) if key doesn't exist:

```python live
person = {"name": "Alice", "age": 25}

# Using get() - returns None if missing
print(person.get("name"))
print(person.get("email"))  # None, no error

# With default value
email = person.get("email", "not provided")
print(f"Email: {email}")
```

:::expected_output
Alice
None
Email: not provided
:::

## Adding and Modifying

```python live
user = {"name": "Bob"}
print("Initial:", user)

# Add new key
user["email"] = "bob@example.com"
print("After add:", user)

# Modify existing
user["name"] = "Robert"
print("After modify:", user)
```

:::expected_output
Initial: {'name': 'Bob'}
After add: {'name': 'Bob', 'email': 'bob@example.com'}
After modify: {'name': 'Robert', 'email': 'bob@example.com'}
:::

## Removing Items

```python live
data = {"a": 1, "b": 2, "c": 3}
print("Before:", data)

# Remove and get value
removed = data.pop("b")
print(f"Removed: {removed}")
print("After:", data)

# Delete without getting
del data["a"]
print("After del:", data)
```

:::expected_output
Before: {'a': 1, 'b': 2, 'c': 3}
Removed: 2
After: {'a': 1, 'c': 3}
After del: {'c': 3}
:::

## Checking Keys

```python live
inventory = {"apple": 50, "banana": 30}

# Check if key exists
print("apple" in inventory)    # True
print("orange" in inventory)   # False

if "apple" in inventory:
    print(f"We have {inventory['apple']} apples")
```

:::expected_output
True
False
We have 50 apples
:::

## Dictionary with Multiple Data Types

```python live
record = {
    "id": 1,
    "name": "Widget",
    "price": 19.99,
    "active": True,
    "tags": ["sale", "popular"],
    "details": {
        "weight": 0.5,
        "color": "blue"
    }
}

print(record["tags"][0])           # First tag
print(record["details"]["color"])  # Nested access
```

:::expected_output
sale
blue
:::

## Getting All Keys and Values

```python live
person = {"name": "Alice", "age": 25, "city": "NYC"}

print("Keys:", list(person.keys()))
print("Values:", list(person.values()))
print("Items:", list(person.items()))
```

:::expected_output
Keys: ['name', 'age', 'city']
Values: ['Alice', 25, 'NYC']
Items: [('name', 'Alice'), ('age', 25), ('city', 'NYC')]
:::

## Key Points

- Dictionaries store key-value pairs
- Access values with `dict["key"]` or `dict.get("key")`
- Keys must be unique and immutable
- Use `in` to check if key exists
- Values can be any type, including lists and other dicts

:::hint Common Mistake
Using `dict["key"]` for a key that doesn't exist causes KeyError. Use `dict.get("key")` for safe access or check with `"key" in dict` first.
:::
