---
title: "Challenge: Inventory Analyzer"
slug: dict-operations-challenge
description: "Build an inventory analyzer using dictionary operations"
course_id: PY101
module: data-structures
module_order: 3
topic: dict-operations
topic_order: 8
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - dict-operations-lesson
  - dict-operations-practice
skills:
  - data-structures
  - dict-operations
outcomes:
  - "Process complex dictionary data"
  - "Generate statistical summaries"
  - "Group and analyze information"
capstone_relevance: "Analyze your application's record data"
---

## The Challenge

Create an inventory analyzer that processes product data and generates insights.

### Requirements

Analyze the inventory to:
1. Total inventory value (price × quantity)
2. Group products by category
3. Find low-stock items (quantity < 10)
4. Find the most valuable product (highest price × quantity)

### Test Data

```python
inventory = [
    {"name": "Laptop", "category": "Electronics", "price": 999, "quantity": 15},
    {"name": "Mouse", "category": "Electronics", "price": 29, "quantity": 50},
    {"name": "Desk", "category": "Furniture", "price": 299, "quantity": 8},
    {"name": "Chair", "category": "Furniture", "price": 199, "quantity": 12},
    {"name": "Monitor", "category": "Electronics", "price": 349, "quantity": 5},
    {"name": "Lamp", "category": "Furniture", "price": 49, "quantity": 25},
]
```

### Example Output

```
=== Inventory Analyzer ===

Total Inventory Value: $25,847

Products by Category:
- Electronics: Laptop, Mouse, Monitor
- Furniture: Desk, Chair, Lamp

Low Stock (< 10):
- Desk: 8 units
- Monitor: 5 units

Most Valuable Item:
Laptop ($14,985 total value)
```

## Your Solution

```python live
inventory = [
    {"name": "Laptop", "category": "Electronics", "price": 999, "quantity": 15},
    {"name": "Mouse", "category": "Electronics", "price": 29, "quantity": 50},
    {"name": "Desk", "category": "Furniture", "price": 299, "quantity": 8},
    {"name": "Chair", "category": "Furniture", "price": 199, "quantity": 12},
    {"name": "Monitor", "category": "Electronics", "price": 349, "quantity": 5},
    {"name": "Lamp", "category": "Furniture", "price": 49, "quantity": 25},
]

print("=== Inventory Analyzer ===")
print()

# Analyze the inventory




```

:::expected_output
=== Inventory Analyzer ===

Total Inventory Value: $24,185

Products by Category:
- Electronics: Laptop, Mouse, Monitor
- Furniture: Desk, Chair, Lamp

Low Stock (< 10):
- Desk: 8 units
- Monitor: 5 units

Most Valuable Item:
Laptop ($14,985 total value)
:::

:::hint Approach
Loop through inventory for each analysis. Use a dict for grouping by category. Track max value item separately.
:::

:::hint Structure
Total value: sum(price * quantity). Grouping: build dict with category keys and list of names. Low stock: filter by quantity.
:::

:::answer Reveal full solution
```python
inventory = [
    {"name": "Laptop", "category": "Electronics", "price": 999, "quantity": 15},
    {"name": "Mouse", "category": "Electronics", "price": 29, "quantity": 50},
    {"name": "Desk", "category": "Furniture", "price": 299, "quantity": 8},
    {"name": "Chair", "category": "Furniture", "price": 199, "quantity": 12},
    {"name": "Monitor", "category": "Electronics", "price": 349, "quantity": 5},
    {"name": "Lamp", "category": "Furniture", "price": 49, "quantity": 25},
]

print("=== Inventory Analyzer ===")
print()

# Total inventory value
total_value = 0
for item in inventory:
    total_value += item["price"] * item["quantity"]
print(f"Total Inventory Value: ${total_value:,}")
print()

# Group products by category
categories = {}
for item in inventory:
    category = item["category"]
    if category not in categories:
        categories[category] = []
    categories[category].append(item["name"])

print("Products by Category:")
for category, names in categories.items():
    print(f"- {category}: {', '.join(names)}")
print()

# Low stock items
print("Low Stock (< 10):")
for item in inventory:
    if item["quantity"] < 10:
        print(f"- {item['name']}: {item['quantity']} units")
print()

# Most valuable item
most_valuable = None
max_value = 0
for item in inventory:
    item_value = item["price"] * item["quantity"]
    if item_value > max_value:
        max_value = item_value
        most_valuable = item

print("Most Valuable Item:")
print(f"{most_valuable['name']} (${max_value:,} total value)")
```
:::
