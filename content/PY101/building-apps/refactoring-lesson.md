---
title: "Refactoring Code"
slug: refactoring-lesson
description: "Learn to improve code without changing its behavior"
course_id: PY101
module: building-apps
module_order: 7
topic: refactoring
topic_order: 5
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - defining-functions-lesson
  - program-structure-lesson
skills:
  - refactoring
  - code-quality
outcomes:
  - "Identify code that needs refactoring"
  - "Apply common refactoring techniques"
  - "Write cleaner, more maintainable code"
capstone_relevance: "Refactoring improves your code as you build"
---

## Introduction

**Refactoring** is improving code structure without changing what it does. Clean code is easier to read, debug, and extend. As you build your capstone, you'll constantly refactor to keep your code manageable.

## Why Refactor?

```python live
# BEFORE: Hard to read and maintain
def p(d):
    t = 0
    for x in d:
        t += x["p"] * x["q"]
    if t > 100:
        t = t * 0.9
    return t

# AFTER: Clear and readable
def calculate_total(items):
    """Calculate total price with bulk discount."""
    total = sum(item["price"] * item["quantity"] for item in items)

    BULK_DISCOUNT_THRESHOLD = 100
    BULK_DISCOUNT_RATE = 0.9

    if total > BULK_DISCOUNT_THRESHOLD:
        total = total * BULK_DISCOUNT_RATE

    return total

# Both do the same thing, but one is much clearer!
items = [{"price": 20, "quantity": 3}, {"price": 15, "quantity": 2}]
print("Total:", calculate_total(items))
```

:::expected_output
Total: 90
:::

## Technique 1: Rename for Clarity

```python live
# BEFORE: Cryptic names
def calc(x, y, z):
    return x * y * (1 + z)

# AFTER: Meaningful names
def calculate_price_with_tax(base_price, quantity, tax_rate):
    return base_price * quantity * (1 + tax_rate)

# Now you know exactly what it does!
print(calculate_price_with_tax(10, 5, 0.08))
```

:::expected_output
54.0
:::

## Technique 2: Extract Function

```python live
# BEFORE: Long function doing many things
def process_order_bad(order):
    # Validate
    if not order.get("items"):
        return "Error: No items"
    if not order.get("customer"):
        return "Error: No customer"

    # Calculate totals
    subtotal = 0
    for item in order["items"]:
        subtotal += item["price"] * item["quantity"]
    tax = subtotal * 0.08
    total = subtotal + tax

    # Format output
    result = "Order for: " + order["customer"] + "\n"
    result += "Subtotal: $" + str(subtotal) + "\n"
    result += "Tax: $" + str(round(tax, 2)) + "\n"
    result += "Total: $" + str(round(total, 2))
    return result

# AFTER: Separate concerns into functions
def validate_order(order):
    if not order.get("items"):
        return False, "No items"
    if not order.get("customer"):
        return False, "No customer"
    return True, None

def calculate_order_total(items, tax_rate=0.08):
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = subtotal * tax_rate
    return subtotal, tax, subtotal + tax

def format_order_receipt(customer, subtotal, tax, total):
    return (
        "Order for: " + customer + "\n" +
        "Subtotal: $" + str(subtotal) + "\n" +
        "Tax: $" + str(round(tax, 2)) + "\n" +
        "Total: $" + str(round(total, 2))
    )

def process_order(order):
    is_valid, error = validate_order(order)
    if not is_valid:
        return "Error: " + error

    subtotal, tax, total = calculate_order_total(order["items"])
    return format_order_receipt(order["customer"], subtotal, tax, total)

# Test
order = {
    "customer": "Alice",
    "items": [
        {"price": 20, "quantity": 2},
        {"price": 15, "quantity": 1}
    ]
}
print(process_order(order))
```

:::expected_output
Order for: Alice
Subtotal: $55
Tax: $4.4
Total: $59.4
:::

## Technique 3: Replace Magic Numbers

```python live
# BEFORE: Magic numbers
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"

# AFTER: Named constants
GRADE_A_THRESHOLD = 90
GRADE_B_THRESHOLD = 80
GRADE_C_THRESHOLD = 70
GRADE_D_THRESHOLD = 60

def get_grade_better(score):
    if score >= GRADE_A_THRESHOLD:
        return "A"
    elif score >= GRADE_B_THRESHOLD:
        return "B"
    elif score >= GRADE_C_THRESHOLD:
        return "C"
    elif score >= GRADE_D_THRESHOLD:
        return "D"
    return "F"

print(get_grade_better(85))
```

:::expected_output
B
:::

## Technique 4: Simplify Conditionals

```python live
# BEFORE: Complex nested conditions
def can_vote_bad(age, is_citizen, is_registered):
    if age >= 18:
        if is_citizen:
            if is_registered:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# AFTER: Guard clauses
def can_vote(age, is_citizen, is_registered):
    if age < 18:
        return False
    if not is_citizen:
        return False
    if not is_registered:
        return False
    return True

# Even simpler
def can_vote_simple(age, is_citizen, is_registered):
    return age >= 18 and is_citizen and is_registered

print(can_vote_simple(25, True, True))
print(can_vote_simple(16, True, True))
```

:::expected_output
True
False
:::

## Technique 5: Remove Duplication

```python live
# BEFORE: Duplicated code
def print_user(user):
    print("Name: " + user["name"])
    print("Email: " + user["email"])
    print("-" * 20)

def print_admin(admin):
    print("Name: " + admin["name"])
    print("Email: " + admin["email"])
    print("Role: Admin")
    print("-" * 20)

# AFTER: Shared function
def print_person(person, role=None):
    print("Name: " + person["name"])
    print("Email: " + person["email"])
    if role:
        print("Role: " + role)
    print("-" * 20)

# Use the shared function
user = {"name": "Alice", "email": "alice@example.com"}
print_person(user)
print_person(user, "Admin")
```

:::expected_output
Name: Alice
Email: alice@example.com
--------------------
Name: Alice
Email: alice@example.com
Role: Admin
--------------------
:::

## Technique 6: Use List Comprehensions

```python live
# BEFORE: Verbose loop
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

evens = []
for num in numbers:
    if num % 2 == 0:
        evens.append(num)

squared = []
for num in evens:
    squared.append(num ** 2)

# AFTER: Concise comprehensions
evens = [num for num in numbers if num % 2 == 0]
squared = [num ** 2 for num in evens]

# Or combined
result = [num ** 2 for num in numbers if num % 2 == 0]
print("Squared evens:", result)
```

:::expected_output
Squared evens: [4, 16, 36, 64, 100]
:::

## When to Refactor

1. **Before adding a feature** - Clean up first
2. **After getting code to work** - Then make it clean
3. **When you find a bug** - Improve while fixing
4. **When code is hard to understand** - Even your own code!

## Key Points

- Refactor in small steps
- Test after each change
- Meaningful names are crucial
- Extract functions to reduce complexity
- Use constants instead of magic numbers
- Remove duplication
- Simplify conditionals

:::hint Remember
The best time to refactor is when you notice something could be clearer. The second best time is now!
:::

