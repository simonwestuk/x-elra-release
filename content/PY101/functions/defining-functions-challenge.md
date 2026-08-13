---
title: "Challenge: Build a Receipt Printer"
slug: defining-functions-challenge
description: "Create functions to print a formatted store receipt"
course_id: PY101
module: functions
module_order: 4
topic: defining-functions
topic_order: 1
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - defining-functions-practice
skills:
  - functions
outcomes:
  - "Break a problem into functions"
  - "Organize code logically"
  - "Create reusable display functions"
capstone_relevance: "You'll use functions to display records and menus in your capstone"
---

## Challenge: Receipt Printer

Create a set of functions to print a nicely formatted store receipt.

### Requirements

1. Create `print_header()` that displays:
```
================================
        PYTHON MART
     Thank you for shopping!
================================
```

2. Create `print_items()` that displays some sample items:
```
Apples          $3.99
Bread           $2.49
Milk            $4.99
```

3. Create `print_divider()` that prints a line of dashes:
```
--------------------------------
```

4. Create `print_total()` that displays:
```
TOTAL:         $11.47
```

5. Create `print_footer()` that displays:
```
================================
   Have a great day!
================================
```

6. Create `print_receipt()` that calls all the above functions in order.

### Your Solution

```python live
# Define all your functions here




# This should print the complete receipt
print_receipt()
```

:::expected_output
================================
        PYTHON MART
     Thank you for shopping!
================================
Apples          $3.99
Bread           $2.49
Milk            $4.99
--------------------------------
TOTAL:         $11.47
================================
   Have a great day!
================================
:::

### Expected Output

```
================================
        PYTHON MART
     Thank you for shopping!
================================
Apples          $3.99
Bread           $2.49
Milk            $4.99
--------------------------------
TOTAL:         $11.47
================================
   Have a great day!
================================
```

:::hint Structure
Define each small function first, then create print_receipt() that calls them all.
:::

:::hint Alignment
Use spaces inside your strings to align the text. Count characters to match the expected output.
:::

:::answer Reveal full solution
```python
def print_header():
    print("================================")
    print("        PYTHON MART")
    print("     Thank you for shopping!")
    print("================================")

def print_items():
    print("Apples          $3.99")
    print("Bread           $2.49")
    print("Milk            $4.99")

def print_divider():
    print("--------------------------------")

def print_total():
    print("TOTAL:         $11.47")

def print_footer():
    print("================================")
    print("   Have a great day!")
    print("================================")

def print_receipt():
    print_header()
    print_items()
    print_divider()
    print_total()
    print_footer()

# This should print the complete receipt
print_receipt()
```
:::

