---
title: "Challenge: Refactor a Messy Application"
slug: refactoring-challenge
description: "Transform messy code into clean, maintainable code"
course_id: PY101
module: building-apps
module_order: 7
topic: refactoring
topic_order: 5
type: challenge
difficulty: beginner
estimated_minutes: 25
prerequisites:
  - refactoring-practice
skills:
  - refactoring
  - code-quality
outcomes:
  - "Apply multiple refactoring techniques"
  - "Transform real messy code"
  - "Create production-quality code"
capstone_relevance: "You'll refactor your capstone as it grows"
---

## Challenge: Refactor the Order System

The code below works but is a mess. Your task is to refactor it into clean, maintainable code.

### The Messy Code

```python live
# This code works but is terrible! Refactor it.

d = []  # data
c = 0   # counter

def a(n, p, q):  # add item
    global c
    c = c + 1
    i = {"id": c, "n": n, "p": p, "q": q}
    d.append(i)
    return i

def g():  # get all
    return d

def t():  # total
    x = 0
    for i in d:
        x = x + i["p"] * i["q"]
    return x

def f(id):  # find
    for i in d:
        if i["id"] == id:
            return i
    return None

def u(id, q):  # update quantity
    i = f(id)
    if i != None:
        i["q"] = q
        return 1
    return 0

def r(id):  # remove
    global d
    d = [i for i in d if i["id"] != id]

def p():  # print
    print("="*30)
    print("ORDER")
    print("="*30)
    for i in d:
        print(i["n"] + " x" + str(i["q"]) + " @ $" + str(i["p"]))
    print("-"*30)
    x = t()
    if x > 100:
        print("Subtotal: $" + str(x))
        disc = x * 0.1
        print("Discount: -$" + str(disc))
        x = x - disc
    print("Total: $" + str(x))
    print("="*30)

# Test
a("Widget", 25.0, 2)
a("Gadget", 15.0, 3)
a("Gizmo", 10.0, 5)
p()

u(2, 5)  # Update gadget quantity
r(3)     # Remove gizmo
print("\nAfter updates:")
p()
```

:::expected_output
==============================
ORDER
==============================
Widget x2 @ $25.0
Gadget x3 @ $15.0
Gizmo x5 @ $10.0
------------------------------
Subtotal: $145.0
Discount: -$14.5
Total: $130.5
==============================

After updates:
==============================
ORDER
==============================
Widget x2 @ $25.0
Gadget x5 @ $15.0
------------------------------
Subtotal: $125.0
Discount: -$12.5
Total: $112.5
==============================
:::

### Your Refactored Version

Create a clean version with:

1. **Meaningful names** - Variables, functions, and parameters
2. **Constants** - For magic numbers like discount threshold
3. **Extracted functions** - Separate concerns
4. **Clear structure** - Section comments
5. **Good documentation** - Docstrings

```python live
# ============ CONSTANTS ============
DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.10

# ============ STATE ============
order_state = {
    "items": [],
    "next_id": 1
}

# ============ ITEM OPERATIONS ============
def add_item(name, price, quantity):
    """Add an item to the order."""
    # Your refactored code
    pass

def get_all_items():
    """Return all items in the order."""
    # Your refactored code
    pass

def find_item(item_id):
    """Find an item by ID."""
    # Your refactored code
    pass

def update_quantity(item_id, new_quantity):
    """Update an item's quantity."""
    # Your refactored code
    pass

def remove_item(item_id):
    """Remove an item from the order."""
    # Your refactored code
    pass

# ============ CALCULATIONS ============
def calculate_subtotal():
    """Calculate order subtotal."""
    # Your refactored code
    pass

def calculate_discount(subtotal):
    """Calculate discount if applicable."""
    # Your refactored code
    pass

def calculate_total():
    """Calculate final total with discount."""
    # Your refactored code
    pass

# ============ DISPLAY ============
def format_item_line(item):
    """Format a single item for display."""
    # Your refactored code
    pass

def print_order():
    """Print formatted order receipt."""
    # Your refactored code
    pass

# ============ TEST ============
def test_order_system():
    """Test the refactored order system."""
    print("=== Testing Refactored Order System ===\n")

    # Add items
    add_item("Widget", 25.0, 2)
    add_item("Gadget", 15.0, 3)
    add_item("Gizmo", 10.0, 5)

    print_order()

    # Update and remove
    update_quantity(2, 5)
    remove_item(3)

    print("\nAfter updates:")
    print_order()

# Run test
test_order_system()
```

:::expected_output
=== Testing Refactored Order System ===

==============================
ORDER
==============================
Widget x2 @ $25.0
Gadget x3 @ $15.0
Gizmo x5 @ $10.0
------------------------------
Subtotal: $145.0
Discount: -$14.5
Total: $130.5
==============================

After updates:
==============================
ORDER
==============================
Widget x2 @ $25.0
Gadget x5 @ $15.0
------------------------------
Subtotal: $125.0
Discount: -$12.5
Total: $112.5
==============================
:::

### Expected Output

Same output as the messy version, but with clean code!

```
=== Testing Refactored Order System ===

==============================
ORDER
==============================
Widget x2 @ $25.0
Gadget x3 @ $15.0
Gizmo x5 @ $10.0
------------------------------
Subtotal: $145.0
Discount: -$14.5
Total: $130.5
==============================

After updates:
==============================
ORDER
==============================
Widget x2 @ $25.0
Gadget x5 @ $15.0
------------------------------
Subtotal: $125.0
Discount: -$12.5
Total: $112.5
==============================
```

:::hint Step 1
Start by renaming: `d` → `order_state["items"]`, `c` → ID counter, `n` → name, `p` → price, `q` → quantity.
:::

:::hint Step 2
Extract the discount logic into its own function that takes subtotal and returns the discount amount.
:::

:::hint Step 3
Move the print formatting into small helper functions like `format_item_line()`.
:::

:::hint Step 4
Add docstrings to explain what each function does.
:::

:::answer Reveal full solution
```python
# ============ CONSTANTS ============
DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.10

# ============ STATE ============
order_state = {
    "items": [],
    "next_id": 1
}

# ============ ITEM OPERATIONS ============
def add_item(name, price, quantity):
    """Add an item to the order."""
    item = {
        "id": order_state["next_id"],
        "name": name,
        "price": price,
        "quantity": quantity
    }
    order_state["items"].append(item)
    order_state["next_id"] += 1
    return item

def get_all_items():
    """Return all items in the order."""
    return order_state["items"]

def find_item(item_id):
    """Find an item by ID."""
    for item in order_state["items"]:
        if item["id"] == item_id:
            return item
    return None

def update_quantity(item_id, new_quantity):
    """Update an item's quantity."""
    item = find_item(item_id)
    if item is not None:
        item["quantity"] = new_quantity
        return True
    return False

def remove_item(item_id):
    """Remove an item from the order."""
    order_state["items"] = [item for item in order_state["items"] if item["id"] != item_id]

# ============ CALCULATIONS ============
def calculate_subtotal():
    """Calculate order subtotal."""
    total = 0
    for item in order_state["items"]:
        total += item["price"] * item["quantity"]
    return total

def calculate_discount(subtotal):
    """Calculate discount if applicable."""
    if subtotal > DISCOUNT_THRESHOLD:
        return subtotal * DISCOUNT_RATE
    return 0

def calculate_total():
    """Calculate final total with discount."""
    subtotal = calculate_subtotal()
    discount = calculate_discount(subtotal)
    return subtotal - discount

# ============ DISPLAY ============
def format_item_line(item):
    """Format a single item for display."""
    return item["name"] + " x" + str(item["quantity"]) + " @ $" + str(item["price"])

def print_order():
    """Print formatted order receipt."""
    print("=" * 30)
    print("ORDER")
    print("=" * 30)
    for item in order_state["items"]:
        print(format_item_line(item))
    print("-" * 30)
    subtotal = calculate_subtotal()
    discount = calculate_discount(subtotal)
    if discount > 0:
        print("Subtotal: $" + str(subtotal))
        print("Discount: -$" + str(discount))
    print("Total: $" + str(subtotal - discount))
    print("=" * 30)

# ============ TEST ============
def test_order_system():
    """Test the refactored order system."""
    print("=== Testing Refactored Order System ===\n")

    # Add items
    add_item("Widget", 25.0, 2)
    add_item("Gadget", 15.0, 3)
    add_item("Gizmo", 10.0, 5)

    print_order()

    # Update and remove
    update_quantity(2, 5)
    remove_item(3)

    print("\nAfter updates:")
    print_order()

# Run test
test_order_system()
```
:::

