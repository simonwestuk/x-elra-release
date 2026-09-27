---
title: "Challenge: Ticket Pricing"
slug: if-statements-challenge
description: "Build a ticket pricing system with multiple conditions"
course_id: PY101
module: control-flow
module_order: 2
topic: if-statements
topic_order: 3
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - if-statements-lesson
  - if-statements-practice
skills:
  - control-flow
  - if-else
outcomes:
  - "Design conditional logic for real scenarios"
  - "Apply multiple if statements"
  - "Calculate values based on conditions"
capstone_relevance: "Apply business logic rules to record processing"
---

## The Challenge

Create a ticket pricing system for a movie theater.

### Requirements

Base ticket price is $12.00. Apply these discounts:
- Senior (65+): 25% off
- Child (under 12): 50% off
- Student (with student ID): 15% off
- Matinee (before 5pm): Additional $2 off

Display the base price, each applicable discount, and final price.

### Test Data

```python
age = 70
is_student = False
is_matinee = True
```

### Example Output

```
=== Ticket Pricing ===
Base price: $12.00
Senior discount (25%): -$3.00
Matinee discount: -$2.00
---
Final price: $7.00
```

## Your Solution

```python live
# Customer info
age = 70
is_student = False
is_matinee = True

# Base price
base_price = 12.00
final_price = base_price

# Apply discounts and display




```

:::expected_output
=== Ticket Pricing ===
Base price: $12.00
Senior discount (25%): -$3.00
Matinee discount: -$2.00
---
Final price: $7.00
:::

:::hint Approach
Check each discount condition with a separate if statement. Subtract from final_price when a discount applies.
:::

:::hint Structure
Print the base price first. Then check each condition, print the discount if it applies, and update final_price. Print the final price at the end.
:::

:::answer Reveal full solution
```python
# Customer info
age = 70
is_student = False
is_matinee = True

# Base price
base_price = 12.00
final_price = base_price

# Apply discounts and display
print("=== Ticket Pricing ===")
print(f"Base price: ${base_price:.2f}")

if age >= 65:
    discount = base_price * 0.25
    final_price -= discount
    print(f"Senior discount (25%): -${discount:.2f}")

if age < 12:
    discount = base_price * 0.50
    final_price -= discount
    print(f"Child discount (50%): -${discount:.2f}")

if is_student:
    discount = base_price * 0.15
    final_price -= discount
    print(f"Student discount (15%): -${discount:.2f}")

if is_matinee:
    final_price -= 2.00
    print(f"Matinee discount: -$2.00")

print("---")
print(f"Final price: ${final_price:.2f}")
```
:::
