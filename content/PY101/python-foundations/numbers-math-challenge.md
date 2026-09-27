---
title: "Challenge: Trip Cost Calculator"
slug: numbers-math-challenge
description: "Build a calculator to estimate trip costs"
course_id: PY101
module: python-foundations
module_order: 1
topic: numbers-math
topic_order: 4
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - numbers-math-lesson
  - numbers-math-practice
skills:
  - numbers
  - math
outcomes:
  - "Design calculations with multiple steps"
  - "Apply math operations to real-world problems"
  - "Present calculated results clearly"
capstone_relevance: "Real applications need multi-step calculations with clear output"
---

## The Challenge

Create a trip cost calculator that estimates the total cost of a road trip based on distance, fuel efficiency, and fuel price.

### Requirements

Calculate and display:
- Total fuel needed (gallons)
- Fuel cost
- Add a 10% buffer for unexpected stops
- Show the grand total

### Given Information

- Distance: 450 miles
- Car fuel efficiency: 28 miles per gallon
- Fuel price: $3.49 per gallon

### Example Output

```
=== Trip Cost Calculator ===
Distance: 450 miles
Efficiency: 28 mpg

Fuel needed: 16.07 gallons
Base fuel cost: $56.09
Buffer (10%): $5.61
---
Total estimated cost: $61.70
```

## Your Solution

```python live
# Trip details
distance = 450
mpg = 28
price_per_gallon = 3.49

# Calculate fuel needed


# Calculate costs


# Display results




```

:::hint Approach
Break it into steps: 1) Calculate gallons needed, 2) Calculate base cost, 3) Calculate buffer, 4) Sum for total.
:::

:::hint Structure
Use variables to store each intermediate result. This makes the code readable and easy to debug.
:::

:::answer Reveal full solution
```python
# Trip details
distance = 450
mpg = 28
price_per_gallon = 3.49

# Calculate fuel needed
fuel_needed = distance / mpg

# Calculate costs
base_cost = fuel_needed * price_per_gallon
buffer = base_cost * 0.10
total_cost = base_cost + buffer

# Display results
print("=== Trip Cost Calculator ===")
print("Distance:", distance, "miles")
print("Efficiency:", mpg, "mpg")
print()
print("Fuel needed:", round(fuel_needed, 2), "gallons")
print("Base fuel cost: $" + str(round(base_cost, 2)))
print("Buffer (10%): $" + str(round(buffer, 2)))
print("---")
print("Total estimated cost: $" + str(round(total_cost, 2)))
```
:::
