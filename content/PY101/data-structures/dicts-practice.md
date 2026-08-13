---
title: "Practice: Dictionaries"
slug: dicts-practice
description: "Practice creating and using dictionaries"
course_id: PY101
module: data-structures
module_order: 3
topic: dicts
topic_order: 7
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - dicts-lesson
skills:
  - data-structures
  - dicts
outcomes:
  - "Create dictionaries"
  - "Access and modify values"
  - "Check for key existence"
capstone_relevance: "Work with record data in your application"
---

## Exercise 1: Create a Dictionary

Create a dictionary for a book with title, author, and year:

```python live
# Create a book dictionary and print it


```

:::hint Stuck?
Use `book = {"title": "...", "author": "...", "year": ...}`
:::

:::answer Reveal answer
```python
# Create a book dictionary and print it
book = {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925}
print(book)
```
:::

## Exercise 2: Access Value

Print the price from the product dictionary:

```python live
product = {"name": "Phone", "price": 599.99, "brand": "TechCo"}
# Print the price


```

:::expected_output
599.99
:::

:::hint Stuck?
Use `product["price"]` to access the value.
:::

:::answer Reveal answer
```python
product = {"name": "Phone", "price": 599.99, "brand": "TechCo"}
print(product["price"])
```
:::

## Exercise 3: Add New Key

Add an "email" key to the user dictionary:

```python live
user = {"name": "Alice", "age": 30}
# Add email key
# Print the updated dictionary


```

:::expected_output
{'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}
:::

:::hint Stuck?
Use `user["email"] = "alice@example.com"`
:::

:::answer Reveal answer
```python
user = {"name": "Alice", "age": 30}
user["email"] = "alice@example.com"
print(user)
```
:::

## Exercise 4: Safe Access

Get the "phone" value safely (return "N/A" if not found):

```python live
contact = {"name": "Bob", "email": "bob@example.com"}
# Get phone safely with default


```

:::expected_output
N/A
:::

:::hint Stuck?
Use `contact.get("phone", "N/A")`
:::

:::answer Reveal answer
```python
contact = {"name": "Bob", "email": "bob@example.com"}
phone = contact.get("phone", "N/A")
print(phone)
```
:::

## Exercise 5: Check Key

Check if "admin" key exists in user settings:

```python live
settings = {"theme": "dark", "language": "en"}
# Check if "admin" exists and print result


```

:::expected_output
admin key does not exist
:::

:::hint Stuck?
Use `"admin" in settings` to check.
:::

:::answer Reveal answer
```python
settings = {"theme": "dark", "language": "en"}
if "admin" in settings:
    print("admin key exists")
else:
    print("admin key does not exist")
```
:::
