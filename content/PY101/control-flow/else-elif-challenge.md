---
title: "Challenge: Tax Calculator"
slug: else-elif-challenge
description: "Build a progressive tax calculator using elif chains"
course_id: PY101
module: control-flow
module_order: 2
topic: else-elif
topic_order: 4
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - else-elif-lesson
  - else-elif-practice
skills:
  - control-flow
  - elif
outcomes:
  - "Design multi-tier conditional logic"
  - "Calculate values based on ranges"
  - "Present results clearly"
capstone_relevance: "Implement tiered pricing or categorization in your application"
---

## The Challenge

Create a simple tax calculator with progressive tax brackets.

### Tax Brackets

| Income Range | Tax Rate |
|--------------|----------|
| $0 - $10,000 | 0% |
| $10,001 - $40,000 | 10% |
| $40,001 - $85,000 | 20% |
| $85,001+ | 30% |

### Requirements

1. Determine which tax bracket applies
2. Calculate the tax amount
3. Calculate net income (income - tax)
4. Display all information

### Example Output

```
=== Tax Calculator ===

Income: $55,000.00
Tax Bracket: 20%
Tax Amount: $11,000.00
Net Income: $44,000.00
```

## Your Solution

```python live
income = 55000

# Determine tax bracket and calculate tax




# Display results




```

:::expected_output
=== Tax Calculator ===

Income: $55,000.00
Tax Bracket: 20%
Tax Amount: $11,000.00
Net Income: $44,000.00
:::

:::hint Approach
Use if-elif-else to determine the tax rate based on income ranges. Then calculate tax as income * rate.
:::

:::hint Structure
Start with the highest bracket check first, or the lowest - just be consistent. Store the rate, then calculate everything.
:::

:::answer Reveal full solution
```python
income = 55000

# Determine tax bracket and calculate tax
if income <= 10000:
    tax_rate = 0
elif income <= 40000:
    tax_rate = 10
elif income <= 85000:
    tax_rate = 20
else:
    tax_rate = 30

tax_amount = income * (tax_rate / 100)
net_income = income - tax_amount

# Display results
print("=== Tax Calculator ===")
print()
print(f"Income: ${income:,.2f}")
print(f"Tax Bracket: {tax_rate}%")
print(f"Tax Amount: ${tax_amount:,.2f}")
print(f"Net Income: ${net_income:,.2f}")
```
:::
