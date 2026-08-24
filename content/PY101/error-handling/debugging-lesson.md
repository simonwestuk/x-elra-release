---
title: "Debugging Techniques"
slug: debugging-lesson
description: "Learn strategies for finding and fixing bugs in your code"
course_id: PY101
module: error-handling
module_order: 5
topic: debugging
topic_order: 5
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - try-except-lesson
skills:
  - debugging
outcomes:
  - "Use print statements for debugging"
  - "Read and understand error messages"
  - "Apply systematic debugging strategies"
capstone_relevance: "Debugging skills are essential for building any application"
---

## Introduction

**Debugging** is the process of finding and fixing errors (bugs) in your code. It's a crucial skill that you'll use constantly as a programmer. This lesson covers practical debugging techniques.

## Reading Error Messages Carefully

Error messages are your friends! They tell you exactly what went wrong.

```python live
# Let's create an error and read the message
def calculate(items):
    total = 0
    for item in items:
        total += item["price"]
    return total

data = [
    {"name": "Apple", "price": 1.50},
    {"name": "Banana"},  # Missing price!
    {"name": "Cherry", "price": 2.00}
]

# This will fail - read the error carefully!
# calculate(data)
```

The error message tells you:
- **Line number** where it failed
- **Exception type** (KeyError)
- **What was missing** ("price")

## Print Debugging

The simplest debugging technique is adding print statements:

```python live
def find_average(numbers):
    print("Input:", numbers)  # Debug: See what was passed
    total = 0
    for num in numbers:
        print("  Adding:", num)  # Debug: See each step
        total += num
    print("Total:", total)  # Debug: Check intermediate result
    average = total / len(numbers)
    print("Average:", average)  # Debug: Verify final result
    return average

result = find_average([10, 20, 30])
print("Returned:", result)
```

:::expected_output
Input: [10, 20, 30]
  Adding: 10
  Adding: 20
  Adding: 30
Total: 60
Average: 20.0
Returned: 20.0
:::

## Strategic Print Placement

Print at key points:

```python live
def process_order(items, discount_percent):
    print("=== Starting process_order ===")
    print("Items:", items)
    print("Discount:", discount_percent)

    subtotal = sum(item["price"] for item in items)
    print("Subtotal calculated:", subtotal)

    discount = subtotal * (discount_percent / 100)
    print("Discount amount:", discount)

    total = subtotal - discount
    print("Final total:", total)
    print("=== Ending process_order ===")

    return total

items = [{"name": "A", "price": 10}, {"name": "B", "price": 20}]
result = process_order(items, 10)
```

:::expected_output
=== Starting process_order ===
Items: [{'name': 'A', 'price': 10}, {'name': 'B', 'price': 20}]
Discount: 10
Subtotal calculated: 30
Discount amount: 3.0
Final total: 27.0
=== Ending process_order ===
:::

## Checking Types

When you get unexpected behavior, check your data types:

```python live
def debug_types(value):
    print("Value:", value)
    print("Type:", type(value))
    print("Length:", len(value) if hasattr(value, '__len__') else "N/A")

debug_types("hello")
debug_types([1, 2, 3])
debug_types(42)
```

:::expected_output
Value: hello
Type: <class 'str'>
Length: 5
Value: [1, 2, 3]
Type: <class 'list'>
Length: 3
Value: 42
Type: <class 'int'>
Length: N/A
:::

## Isolate the Problem

When debugging, narrow down where the bug is:

```python live
def complex_calculation(data):
    # Step 1: Extract values
    values = [item["value"] for item in data]
    print("Step 1 - Values:", values)  # Check this works

    # Step 2: Filter positives
    positives = [v for v in values if v > 0]
    print("Step 2 - Positives:", positives)  # Check this works

    # Step 3: Calculate average
    if positives:
        average = sum(positives) / len(positives)
    else:
        average = 0
    print("Step 3 - Average:", average)  # Check this works

    return average

test_data = [
    {"value": 10},
    {"value": -5},
    {"value": 20},
    {"value": -3}
]

result = complex_calculation(test_data)
```

:::expected_output
Step 1 - Values: [10, -5, 20, -3]
Step 2 - Positives: [10, 20]
Step 3 - Average: 15.0
:::

## Common Bug Patterns

### 1. Off-by-One Errors

```python live
# Bug: Stops one early
items = ["a", "b", "c", "d", "e"]

# Wrong - misses last item
print("Wrong:")
for i in range(len(items) - 1):  # Bug!
    print(items[i])

# Correct
print("\nCorrect:")
for i in range(len(items)):
    print(items[i])
```

:::expected_output
Wrong:
a
b
c
d

Correct:
a
b
c
d
e
:::

### 2. Uninitialized Variables

```python live
def sum_positive(numbers):
    # Bug: Forgetting to initialize
    # total would cause NameError if not initialized
    total = 0
    for num in numbers:
        if num > 0:
            total += num
    return total

print(sum_positive([1, -2, 3, -4, 5]))
```

:::expected_output
9
:::

### 3. Wrong Variable

```python live
def calculate_area(width, height):
    # Bug example: using wrong variable
    # area = width * width  # Oops! Should be height
    area = width * height  # Correct
    return area

print(calculate_area(5, 3))
```

:::expected_output
15
:::

## Rubber Duck Debugging

Explain your code line by line (to a rubber duck or yourself):

1. "First, I get the list of items..."
2. "Then I loop through each item..."
3. "For each item, I add its price to the total..."
4. "Wait - what if an item doesn't have a price?"

Often, just explaining the problem helps you find the bug!

## Debugging Checklist

When you have a bug:

1. **Read the error message** - Line number, error type, details
2. **Check inputs** - Are they what you expected?
3. **Add print statements** - See what's happening
4. **Check types** - Are variables the types you expect?
5. **Simplify** - Can you reproduce with simpler data?
6. **Take a break** - Fresh eyes find bugs faster

## Key Points

- Error messages contain valuable debugging information
- Print statements help you see what's happening
- Check types when behavior is unexpected
- Isolate problems by testing parts separately
- Explain your code out loud to find logic errors

:::hint Remember
The bug is always in the last place you look... so look there first! Think about the assumptions you're making.
:::

