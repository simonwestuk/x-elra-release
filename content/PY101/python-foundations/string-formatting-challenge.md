---
title: "Challenge: Invoice Generator"
slug: string-formatting-challenge
description: "Create a formatted invoice using f-strings"
course_id: PY101
module: python-foundations
module_order: 1
topic: string-formatting
topic_order: 7
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - string-formatting-lesson
  - string-formatting-practice
skills:
  - strings
  - formatting
outcomes:
  - "Combine formatting techniques"
  - "Create professional-looking output"
  - "Handle multiple data values"
capstone_relevance: "Generate formatted reports and displays in your application"
---

## The Challenge

Create a mini invoice display that shows items, quantities, prices, and totals with proper formatting.

### Requirements

- Display a header with company name
- Show 3 items with quantity and price
- Calculate line totals (quantity × price)
- Show subtotal, tax (8%), and grand total
- All prices aligned and showing 2 decimal places
- Use proper column alignment

### Example Output

```
================================
         TECH SUPPLIES INC
================================

Item            Qty      Price       Total
--------------------------------------------
Keyboard          2     $45.00      $90.00
Mouse             3     $25.00      $75.00
Monitor           1    $299.99     $299.99
--------------------------------------------
                        Subtotal:  $464.99
                        Tax (8%):   $37.20
                        TOTAL:     $502.19
================================
```

## Your Solution

```python live
# Items data
item1, qty1, price1 = "Keyboard", 2, 45.00
item2, qty2, price2 = "Mouse", 3, 25.00
item3, qty3, price3 = "Monitor", 1, 299.99

# Create the invoice display




```

:::hint Approach
Build the invoice section by section: header, column titles, each item row, separator, then totals.
:::

:::hint Structure
Calculate line totals first. Use consistent formatting: `{item:<15}` for names, `{price:>10.2f}` for money values.
:::

:::answer Reveal full solution
```python
# Items data
item1, qty1, price1 = "Keyboard", 2, 45.00
item2, qty2, price2 = "Mouse", 3, 25.00
item3, qty3, price3 = "Monitor", 1, 299.99

# Calculate line totals
total1 = qty1 * price1
total2 = qty2 * price2
total3 = qty3 * price3

# Calculate subtotal, tax, and grand total
subtotal = total1 + total2 + total3
tax = subtotal * 0.08
grand_total = subtotal + tax

# Create the invoice display
print("================================")
print("         TECH SUPPLIES INC")
print("================================")
print()
print(f"{'Item':<15} {'Qty':>3}  {'Price':>9}   {'Total':>9}")
print("-" * 44)
print(f"{item1:<15} {qty1:>3}     ${price1:>6.2f}      ${total1:>6.2f}")
print(f"{item2:<15} {qty2:>3}     ${price2:>6.2f}      ${total2:>6.2f}")
print(f"{item3:<15} {qty3:>3}    ${price3:>7.2f}     ${total3:>7.2f}")
print("-" * 44)
print(f"{'Subtotal:':>36}  ${subtotal:>.2f}")
print(f"{'Tax (8%):':>36}   ${tax:>.2f}")
print(f"{'TOTAL:':>36}     ${grand_total:>.2f}")
print("================================")
```
:::
