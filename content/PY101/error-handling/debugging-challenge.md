---
title: "Challenge: Debug the Shopping Cart"
slug: debugging-challenge
description: "Find and fix all bugs in a shopping cart system"
course_id: PY101
module: error-handling
module_order: 5
topic: debugging
topic_order: 5
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - debugging-practice
skills:
  - debugging
outcomes:
  - "Debug complex multi-function code"
  - "Track down bugs systematically"
  - "Verify fixes thoroughly"
capstone_relevance: "Debugging real systems requires patience and method"
---

## Challenge: Fix the Shopping Cart

This shopping cart system has **7 bugs**. Find and fix all of them to make the program work correctly.

### The Buggy Code

```python live
# Shopping Cart System with 7 bugs - fix them all!

cart = []

def add_item(name, price, quantity):
    """Add item to cart."""
    item = {
        "name": name,
        "price": price,
        "quantity": quantity
    }
    item.append(cart)  # Bug 1
    print("Added:", name)

def remove_item(name):
    """Remove item from cart by name."""
    for i in range(len(cart)):
        if cart[i]["name"] == name:
            del cart[i]
            print("Removed:", name)
            # Bug 2: Should return/break after removing

def get_item_total(item):
    """Calculate total for one item."""
    return item["price"] + item["quantity"]  # Bug 3

def calculate_subtotal():
    """Calculate cart subtotal."""
    subtotal = 0
    for item in cart:
        item_total = get_item_total(item)
        subtotal = item_total  # Bug 4
    return subtotal

def apply_discount(total, percent):
    """Apply percentage discount."""
    discount = total * percent  # Bug 5
    return total - discount

def calculate_tax(amount, rate):
    """Calculate tax amount."""
    return amount * rate / 100

def checkout(discount_percent, tax_rate):
    """Complete checkout process."""
    if len(cart) > 0:  # Bug 6: Should handle empty cart gracefully
        print("Cart is empty!")
        return 0

    print("=== Checkout ===")
    for item in cart:
        total = get_item_total(item)
        print(item["name"] + " x" + str(item["quantity"]) + ": $" + str(total))

    subtotal = calculate_subtotal()
    print("Subtotal: $" + str(subtotal))

    after_discount = apply_discount(subtotal, discount_percent)
    print("After " + str(discount_percent) + "% discount: $" + str(after_discount))

    tax = calculate_tax(after_discount, tax_rate)
    print("Tax (" + str(tax_rate) + "%): $" + str(round(tax, 2)))

    final_total = subtotal + tax  # Bug 7
    print("Total: $" + str(round(final_total, 2)))

    return round(final_total, 2)


# Test the shopping cart
print("Adding items...")
add_item("Apple", 1.50, 3)      # $4.50
add_item("Banana", 0.75, 4)     # $3.00
add_item("Orange", 2.00, 2)     # $4.00
# Subtotal should be $11.50

print("\nRemoving Banana...")
remove_item("Banana")
# Subtotal should now be $8.50

print("\nCheckout with 10% discount and 8% tax:")
# Expected:
# Subtotal: $8.50
# After 10% discount: $7.65
# Tax (8%): $0.61
# Total: $8.26
final = checkout(10, 8)
print("\nFinal amount:", final)
```

:::expected_output
Adding items...
Added: Apple
Added: Banana
Added: Orange

Removing Banana...
Removed: Banana

Checkout with 10% discount and 8% tax:
=== Checkout ===
Apple x3: $4.5
Orange x2: $4.0
Subtotal: $8.5
After 10% discount: $7.65
Tax (8%): $0.61
Total: $8.26

Final amount: 8.26
:::

### Expected Output (after fixing)

```
Adding items...
Added: Apple
Added: Banana
Added: Orange

Removing Banana...
Removed: Banana

Checkout with 10% discount and 8% tax:
=== Checkout ===
Apple x3: $4.5
Orange x2: $4.0
Subtotal: $8.5
After 10% discount: $7.65
Tax (8%): $0.61
Total: $8.26

Final amount: 8.26
```

### Bug Hints

:::hint Bug 1
Look at `add_item`. The syntax for appending to a list is `list.append(item)`, not `item.append(list)`.
:::

:::hint Bug 2
In `remove_item`, after deleting an item, the function continues looping which can cause issues. Add `return` or `break` after deleting.
:::

:::hint Bug 3
`get_item_total` should multiply price by quantity, not add them.
:::

:::hint Bug 4
In `calculate_subtotal`, we should add to subtotal, not replace it: `subtotal += item_total`.
:::

:::hint Bug 5
`apply_discount` should divide percent by 100: `discount = total * percent / 100`.
:::

:::hint Bug 6
The condition in `checkout` is backwards. It should be `if len(cart) == 0:` (not `> 0`).
:::

:::hint Bug 7
`final_total` should use `after_discount + tax`, not `subtotal + tax`.
:::

:::answer Reveal full solution
```python
# Shopping Cart System with 7 bugs - fix them all!

cart = []

def add_item(name, price, quantity):
    """Add item to cart."""
    item = {
        "name": name,
        "price": price,
        "quantity": quantity
    }
    cart.append(item)  # Fix 1: Changed item.append(cart) to cart.append(item)
    print("Added:", name)

def remove_item(name):
    """Remove item from cart by name."""
    for i in range(len(cart)):
        if cart[i]["name"] == name:
            del cart[i]
            print("Removed:", name)
            return  # Fix 2: Added return after removing

def get_item_total(item):
    """Calculate total for one item."""
    return item["price"] * item["quantity"]  # Fix 3: Changed + to *

def calculate_subtotal():
    """Calculate cart subtotal."""
    subtotal = 0
    for item in cart:
        item_total = get_item_total(item)
        subtotal += item_total  # Fix 4: Changed = to +=
    return subtotal

def apply_discount(total, percent):
    """Apply percentage discount."""
    discount = total * percent / 100  # Fix 5: Added / 100
    return total - discount

def calculate_tax(amount, rate):
    """Calculate tax amount."""
    return amount * rate / 100

def checkout(discount_percent, tax_rate):
    """Complete checkout process."""
    if len(cart) == 0:  # Fix 6: Changed > 0 to == 0
        print("Cart is empty!")
        return 0

    print("=== Checkout ===")
    for item in cart:
        total = get_item_total(item)
        print(item["name"] + " x" + str(item["quantity"]) + ": $" + str(total))

    subtotal = calculate_subtotal()
    print("Subtotal: $" + str(subtotal))

    after_discount = apply_discount(subtotal, discount_percent)
    print("After " + str(discount_percent) + "% discount: $" + str(after_discount))

    tax = calculate_tax(after_discount, tax_rate)
    print("Tax (" + str(tax_rate) + "%): $" + str(round(tax, 2)))

    final_total = after_discount + tax  # Fix 7: Changed subtotal to after_discount
    print("Total: $" + str(round(final_total, 2)))

    return round(final_total, 2)


# Test the shopping cart
print("Adding items...")
add_item("Apple", 1.50, 3)      # $4.50
add_item("Banana", 0.75, 4)     # $3.00
add_item("Orange", 2.00, 2)     # $4.00
# Subtotal should be $11.50

print("\nRemoving Banana...")
remove_item("Banana")
# Subtotal should now be $8.50

print("\nCheckout with 10% discount and 8% tax:")
# Expected:
# Subtotal: $8.50
# After 10% discount: $7.65
# Tax (8%): $0.61
# Total: $8.26
final = checkout(10, 8)
print("\nFinal amount:", final)
```
:::

