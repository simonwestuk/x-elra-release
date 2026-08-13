---
title: "Challenge: Data Transformer"
slug: comprehensions-challenge
description: "Build a data transformation utility with comprehensions"
course_id: PY101
module: data-structures
module_order: 3
topic: comprehensions
topic_order: 5
type: challenge
difficulty: intermediate
estimated_minutes: 18
prerequisites:
  - comprehensions-lesson
  - comprehensions-practice
skills:
  - data-structures
  - comprehensions
outcomes:
  - "Apply comprehensions to real data"
  - "Chain multiple transformations"
  - "Clean and filter datasets"
capstone_relevance: "Transform and clean your application data"
---

## The Challenge

Create a data transformation utility that cleans and processes a messy dataset.

### Requirements

Given messy product data, use comprehensions to:
1. Get all product names (cleaned - trimmed and title case)
2. Get products priced under $50
3. Calculate discounted prices (10% off each)
4. Create a summary with name and discounted price

### Test Data

```python
products = [
    {"name": "  laptop  ", "price": 999.99, "in_stock": True},
    {"name": "MOUSE", "price": 29.99, "in_stock": True},
    {"name": "  keyboard  ", "price": 49.99, "in_stock": False},
    {"name": "monitor", "price": 199.99, "in_stock": True},
    {"name": "  USB CABLE  ", "price": 9.99, "in_stock": True},
]
```

### Example Output

```
=== Data Transformer ===

Clean Names:
['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Usb Cable']

Products Under $50:
['Mouse', 'Keyboard', 'Usb Cable']

Discounted Prices (10% off):
[899.99, 26.99, 44.99, 179.99, 8.99]

In-Stock Deals (discounted, in-stock only):
- Laptop: $899.99
- Mouse: $26.99
- Monitor: $179.99
- Usb Cable: $8.99
```

## Your Solution

```python live
products = [
    {"name": "  laptop  ", "price": 999.99, "in_stock": True},
    {"name": "MOUSE", "price": 29.99, "in_stock": True},
    {"name": "  keyboard  ", "price": 49.99, "in_stock": False},
    {"name": "monitor", "price": 199.99, "in_stock": True},
    {"name": "  USB CABLE  ", "price": 9.99, "in_stock": True},
]

print("=== Data Transformer ===")
print()

# 1. Clean names


# 2. Products under $50


# 3. Discounted prices


# 4. In-stock deals


```

:::expected_output
=== Data Transformer ===

Clean Names:
['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Usb Cable']

Products Under $50:
['Mouse', 'Keyboard', 'Usb Cable']

Discounted Prices (10% off):
[899.99, 26.99, 44.99, 179.99, 8.99]

In-Stock Deals (discounted, in-stock only):
- Laptop: $899.99
- Mouse: $26.99
- Monitor: $179.99
- Usb Cable: $8.99
:::

:::hint Approach
Each task is one comprehension. Use .strip().title() for cleaning names. Filter with if conditions.
:::

:::hint Structure
Names: `[p["name"].strip().title() for p in products]`. Under 50: add condition. Discounted: `round(p["price"] * 0.9, 2)`.
:::

:::answer Reveal full solution
```python
products = [
    {"name": "  laptop  ", "price": 999.99, "in_stock": True},
    {"name": "MOUSE", "price": 29.99, "in_stock": True},
    {"name": "  keyboard  ", "price": 49.99, "in_stock": False},
    {"name": "monitor", "price": 199.99, "in_stock": True},
    {"name": "  USB CABLE  ", "price": 9.99, "in_stock": True},
]

print("=== Data Transformer ===")
print()

# 1. Clean names
clean_names = [p["name"].strip().title() for p in products]
print("Clean Names:")
print(clean_names)
print()

# 2. Products under $50
under_50 = [p["name"].strip().title() for p in products if p["price"] < 50]
print("Products Under $50:")
print(under_50)
print()

# 3. Discounted prices
discounted = [round(p["price"] * 0.9, 2) for p in products]
print("Discounted Prices (10% off):")
print(discounted)
print()

# 4. In-stock deals
in_stock_deals = [
    (p["name"].strip().title(), round(p["price"] * 0.9, 2))
    for p in products
    if p["in_stock"]
]
print("In-Stock Deals (discounted, in-stock only):")
for name, price in in_stock_deals:
    print(f"- {name}: ${price}")
```
:::
