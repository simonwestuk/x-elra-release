---
title: "Challenge: Build a Calculator"
slug: return-values-challenge
description: "Create a calculator using functions with return values"
course_id: PY101
module: functions
module_order: 4
topic: return-values
topic_order: 3
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - return-values-practice
skills:
  - functions
  - return-values
outcomes:
  - "Design a system of related functions"
  - "Chain function calls effectively"
  - "Build practical applications with return values"
capstone_relevance: "Calculation functions are common in applications"
---

## Challenge: Shopping Calculator

Build a shopping calculator that computes totals with discounts and tax.

### Requirements

1. Create `calculate_subtotal(price, quantity)` - returns price × quantity

2. Create `apply_discount(amount, percent)` - returns the amount after applying a percentage discount
   - Example: apply_discount(100, 10) returns 90 (10% off of 100)

3. Create `add_tax(amount, tax_rate)` - returns the amount plus tax
   - Example: add_tax(100, 8) returns 108 (100 + 8% tax)

4. Create `format_price(amount)` - returns a string formatted as "$X.XX"
   - Example: format_price(42.5) returns "$42.50"

5. Create `calculate_total(price, quantity, discount_percent, tax_rate)` that:
   - Calculates the subtotal
   - Applies the discount
   - Adds tax
   - Returns the final amount

### Your Solution

```python live
# Define your functions here




# Test individual functions
print("Subtotal:", calculate_subtotal(25, 4))  # 100
print("After 10% discount:", apply_discount(100, 10))  # 90
print("With 8% tax:", add_tax(90, 8))  # 97.2
print("Formatted:", format_price(97.2))  # $97.20

print()

# Test complete calculation
# 3 items at $50, 20% discount, 8% tax
total = calculate_total(50, 3, 20, 8)
print("Final total:", format_price(total))
```

:::expected_output
Subtotal: 100
After 10% discount: 90.0
With 8% tax: 97.2
Formatted: $97.20

Final total: $129.60
:::

### Expected Output

```
Subtotal: 100
After 10% discount: 90.0
With 8% tax: 97.2
Formatted: $97.20

Final total: $129.60
```

### Calculation Breakdown

For the complete calculation:
- Subtotal: 50 × 3 = $150.00
- Discount: 150 - 20% = $120.00
- Tax: 120 + 8% = $129.60

:::hint Discount Formula
To apply a 20% discount: `amount * (1 - percent/100)` or `amount - (amount * percent/100)`
:::

:::hint Format Price
Use string formatting: `"$" + str(round(amount, 2))` or explore Python's format options.
:::

:::hint Chaining Functions
In calculate_total, call your other functions and pass results to each other.
:::

:::answer Reveal full solution
```python
def calculate_subtotal(price, quantity):
    return price * quantity

def apply_discount(amount, percent):
    return amount * (1 - percent / 100)

def add_tax(amount, tax_rate):
    return amount * (1 + tax_rate / 100)

def format_price(amount):
    return "$" + format(amount, ".2f")

def calculate_total(price, quantity, discount_percent, tax_rate):
    subtotal = calculate_subtotal(price, quantity)
    discounted = apply_discount(subtotal, discount_percent)
    total = add_tax(discounted, tax_rate)
    return total

# Test individual functions
print("Subtotal:", calculate_subtotal(25, 4))  # 100
print("After 10% discount:", apply_discount(100, 10))  # 90
print("With 8% tax:", add_tax(90, 8))  # 97.2
print("Formatted:", format_price(97.2))  # $97.20

print()

# Test complete calculation
# 3 items at $50, 20% discount, 8% tax
total = calculate_total(50, 3, 20, 8)
print("Final total:", format_price(total))
```
:::

