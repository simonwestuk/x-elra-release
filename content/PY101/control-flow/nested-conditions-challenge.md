---
title: "Challenge: Order Processing System"
slug: nested-conditions-challenge
description: "Build an order processing system with hierarchical validation"
course_id: PY101
module: control-flow
module_order: 2
topic: nested-conditions
topic_order: 6
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - nested-conditions-lesson
  - nested-conditions-practice
skills:
  - control-flow
  - nested-conditions
outcomes:
  - "Design multi-level validation logic"
  - "Handle complex business rules"
  - "Provide clear user feedback"
capstone_relevance: "Process and validate records in your application"
---

## The Challenge

Create an order processing system with multiple validation steps.

### Validation Hierarchy

1. First check: Is item in stock?
2. If in stock: Is quantity valid (> 0 and <= stock)?
3. If quantity valid: Is payment method accepted?
4. If payment accepted: Process order

Provide specific feedback at each level of failure.

### Test Data

```python
item_name = "Widget"
in_stock = True
stock_quantity = 10
order_quantity = 3
payment_method = "credit"
accepted_payments = ["credit", "debit", "paypal"]
```

### Example Output (Success)

```
=== Order Processing ===

Item: Widget
Checking availability... IN STOCK (10 available)
Checking quantity (3)... VALID
Checking payment (credit)... ACCEPTED

ORDER CONFIRMED!
- Item: Widget
- Quantity: 3
- Payment: credit
- Remaining stock: 7
```

### Example Output (Failure at quantity)

```
=== Order Processing ===

Item: Widget
Checking availability... IN STOCK (10 available)
Checking quantity (15)... FAILED
  Error: Only 10 items available

ORDER CANCELLED
```

## Your Solution

```python live
item_name = "Widget"
in_stock = True
stock_quantity = 10
order_quantity = 3
payment_method = "credit"
accepted_payments = ["credit", "debit", "paypal"]

# Process order with nested validation




```

:::expected_output
=== Order Processing ===

Item: Widget
Checking availability... IN STOCK (10 available)
Checking quantity (3)... VALID
Checking payment (credit)... ACCEPTED

ORDER CONFIRMED!
- Item: Widget
- Quantity: 3
- Payment: credit
- Remaining stock: 7
:::

:::hint Approach
Check each condition in sequence using nested ifs. Print status at each check, and only proceed to the next check if the current one passes.
:::

:::hint Structure
Each level: print what you're checking, check the condition, print result, either continue to next level or print error.
:::

:::answer Reveal full solution
```python
item_name = "Widget"
in_stock = True
stock_quantity = 10
order_quantity = 3
payment_method = "credit"
accepted_payments = ["credit", "debit", "paypal"]

# Process order with nested validation
print("=== Order Processing ===")
print()
print(f"Item: {item_name}")

if in_stock:
    print(f"Checking availability... IN STOCK ({stock_quantity} available)")
    if order_quantity > 0 and order_quantity <= stock_quantity:
        print(f"Checking quantity ({order_quantity})... VALID")
        if payment_method in accepted_payments:
            print(f"Checking payment ({payment_method})... ACCEPTED")
            print()
            print("ORDER CONFIRMED!")
            print(f"- Item: {item_name}")
            print(f"- Quantity: {order_quantity}")
            print(f"- Payment: {payment_method}")
            print(f"- Remaining stock: {stock_quantity - order_quantity}")
        else:
            print(f"Checking payment ({payment_method})... FAILED")
            print(f"  Error: {payment_method} is not accepted")
            print()
            print("ORDER CANCELLED")
    else:
        print(f"Checking quantity ({order_quantity})... FAILED")
        if order_quantity <= 0:
            print(f"  Error: Quantity must be greater than 0")
        else:
            print(f"  Error: Only {stock_quantity} items available")
        print()
        print("ORDER CANCELLED")
else:
    print("Checking availability... OUT OF STOCK")
    print()
    print("ORDER CANCELLED")
```
:::
