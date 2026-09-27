---
title: "Practice: Program Structure"
slug: program-structure-practice
description: "Practice organizing code into well-structured programs"
course_id: PY101
module: building-apps
module_order: 7
topic: program-structure
topic_order: 1
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - program-structure-lesson
skills:
  - program-design
  - code-organization
outcomes:
  - "Identify good and bad program structure"
  - "Reorganize messy code"
  - "Apply separation of concerns"
capstone_relevance: "Structured code is easier to build and maintain"
---

## Exercise 1: Identify the Structure

This code is disorganized. Identify which sections it should be split into.

```python live
print("Welcome!")
name = input() if False else "User"  # Simulated input
items = []
TAX_RATE = 0.08
def add_item(name, price):
    items.append({"name": name, "price": price})
add_item("Book", 20)
total = sum(item["price"] for item in items)
def calculate_tax(amount):
    return amount * TAX_RATE
tax = calculate_tax(total)
print("Subtotal: $" + str(total))
print("Tax: $" + str(tax))
print("Total: $" + str(total + tax))
print("Thank you, " + name + "!")

# What sections should this be split into?
# 1. ?
# 2. ?
# 3. ?
# 4. ?
```

:::expected_output
Welcome!
Subtotal: $20
Tax: $1.6
Total: $21.6
Thank you, User!
:::

:::hint Answer
1. Constants (TAX_RATE)
2. Data functions (add_item)
3. Business logic (calculate_tax)
4. Main program (user interaction, display)
:::

:::answer Reveal answer
```python
# ============ CONSTANTS ============
TAX_RATE = 0.08

# ============ DATA FUNCTIONS ============
items = []

def add_item(name, price):
    items.append({"name": name, "price": price})

# ============ BUSINESS LOGIC ============
def calculate_tax(amount):
    return amount * TAX_RATE

# ============ MAIN PROGRAM ============
def main():
    print("Welcome!")
    name = input() if False else "User"  # Simulated input
    add_item("Book", 20)
    total = sum(item["price"] for item in items)
    tax = calculate_tax(total)
    print("Subtotal: $" + str(total))
    print("Tax: $" + str(tax))
    print("Total: $" + str(total + tax))
    print("Thank you, " + name + "!")

main()
```
:::

## Exercise 2: Add Section Comments

Add appropriate section comments to this code.

```python live
MAX_USERS = 100
DEFAULT_ROLE = "user"

def create_user(name, role=None):
    if role is None:
        role = DEFAULT_ROLE
    return {"name": name, "role": role, "active": True}

def is_admin(user):
    return user["role"] == "admin"

def deactivate_user(user):
    user["active"] = False

def display_user(user):
    status = "Active" if user["active"] else "Inactive"
    print(user["name"] + " (" + user["role"] + ") - " + status)

def main():
    admin = create_user("Alice", "admin")
    user = create_user("Bob")

    display_user(admin)
    display_user(user)

    if is_admin(admin):
        print(admin["name"] + " has admin privileges")

main()

# Add comments like:
# # ============ CONSTANTS ============
# # ============ USER FUNCTIONS ============
# # ============ DISPLAY ============
# # ============ MAIN ============
```

:::expected_output
Alice (admin) - Active
Bob (user) - Active
Alice has admin privileges
:::

:::answer Reveal answer
```python
# ============ CONSTANTS ============
MAX_USERS = 100
DEFAULT_ROLE = "user"

# ============ USER FUNCTIONS ============
def create_user(name, role=None):
    if role is None:
        role = DEFAULT_ROLE
    return {"name": name, "role": role, "active": True}

def is_admin(user):
    return user["role"] == "admin"

def deactivate_user(user):
    user["active"] = False

# ============ DISPLAY ============
def display_user(user):
    status = "Active" if user["active"] else "Inactive"
    print(user["name"] + " (" + user["role"] + ") - " + status)

# ============ MAIN ============
def main():
    admin = create_user("Alice", "admin")
    user = create_user("Bob")

    display_user(admin)
    display_user(user)

    if is_admin(admin):
        print(admin["name"] + " has admin privileges")

main()
```
:::

## Exercise 3: Extract Functions

This code does everything in one place. Extract it into proper functions.

```python live
# Messy version - refactor this!
scores = [85, 92, 78, 95, 88, 76, 91]
print("=== Grade Report ===")
total = 0
for score in scores:
    total += score
average = total / len(scores)
print("Scores:", scores)
print("Average:", round(average, 2))
highest = max(scores)
lowest = min(scores)
print("Highest:", highest)
print("Lowest:", lowest)
passing = 0
for score in scores:
    if score >= 70:
        passing += 1
print("Passing:", passing, "of", len(scores))
print("===================")

# Refactored version - complete the functions:
def calculate_average(scores):
    # Your code here
    pass

def count_passing(scores, threshold=70):
    # Your code here
    pass

def print_report(scores):
    # Your code here
    pass
```

:::expected_output
=== Grade Report ===
Scores: [85, 92, 78, 95, 88, 76, 91]
Average: 72.14
Highest: 95
Lowest: 76
Passing: 7 of 7
===================
:::

:::hint Stuck?
Create functions for: calculate_average, count_passing, find_extremes, and print_report. Then call print_report(scores) in main.
:::

:::answer Reveal answer
```python
scores = [85, 92, 78, 95, 88, 76, 91]

def calculate_average(scores):
    total = 0
    for score in scores:
        total += score
    return total / len(scores)

def count_passing(scores, threshold=70):
    passing = 0
    for score in scores:
        if score >= threshold:
            passing += 1
    return passing

def find_extremes(scores):
    return max(scores), min(scores)

def print_report(scores):
    print("=== Grade Report ===")
    average = calculate_average(scores)
    highest, lowest = find_extremes(scores)
    passing = count_passing(scores)
    print("Scores:", scores)
    print("Average:", round(average, 2))
    print("Highest:", highest)
    print("Lowest:", lowest)
    print("Passing:", passing, "of", len(scores))
    print("===================")

print_report(scores)
```
:::

## Exercise 4: Separate Concerns

Reorganize this code to separate data, logic, and presentation.

```python live
# Everything mixed together
products = [
    {"name": "Laptop", "price": 999, "stock": 5},
    {"name": "Mouse", "price": 30, "stock": 50},
    {"name": "Keyboard", "price": 80, "stock": 0}
]

print("=== Inventory Report ===")
for p in products:
    status = "In Stock" if p["stock"] > 0 else "OUT OF STOCK"
    print(p["name"] + ": $" + str(p["price"]) + " - " + status)

low_stock = []
for p in products:
    if p["stock"] < 10:
        low_stock.append(p["name"])

if low_stock:
    print("\nLow stock warning:", ", ".join(low_stock))

# Reorganize into:
# 1. DATA LAYER - functions to access product data
# 2. BUSINESS LOGIC - functions to check stock, etc.
# 3. PRESENTATION - functions to display information
# 4. MAIN - orchestrate everything
```

:::expected_output
=== Inventory Report ===
Laptop: $999 - In Stock
Mouse: $30 - In Stock
Keyboard: $80 - OUT OF STOCK

Low stock warning: Laptop, Keyboard
:::

:::answer Reveal answer
```python
# ============ DATA LAYER ============
products = [
    {"name": "Laptop", "price": 999, "stock": 5},
    {"name": "Mouse", "price": 30, "stock": 50},
    {"name": "Keyboard", "price": 80, "stock": 0}
]

def get_all_products():
    return products

# ============ BUSINESS LOGIC ============
def get_stock_status(product):
    return "In Stock" if product["stock"] > 0 else "OUT OF STOCK"

def find_low_stock(products, threshold=10):
    low_stock = []
    for p in products:
        if p["stock"] < threshold:
            low_stock.append(p["name"])
    return low_stock

# ============ PRESENTATION ============
def display_inventory(products):
    print("=== Inventory Report ===")
    for p in products:
        status = get_stock_status(p)
        print(p["name"] + ": $" + str(p["price"]) + " - " + status)

def display_low_stock_warning(low_stock_items):
    if low_stock_items:
        print("\nLow stock warning:", ", ".join(low_stock_items))

# ============ MAIN ============
def main():
    all_products = get_all_products()
    display_inventory(all_products)
    low_stock = find_low_stock(all_products)
    display_low_stock_warning(low_stock)

main()
```
:::

## Exercise 5: Create a main() Function

Wrap this program in a proper main() function structure.

```python live
# Raw code without main()
APP_NAME = "Calculator"
print("Starting", APP_NAME)

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

result = add(5, 3)
print("5 + 3 =", result)

result = multiply(4, 7)
print("4 * 7 =", result)

print("Goodbye!")

# Rewrite with proper structure:
# - Constants at top
# - Functions defined
# - main() function that runs the program
# - if __name__ == "__main__": main()
```

:::expected_output
Starting Calculator
5 + 3 = 8
4 * 7 = 28
Goodbye!
:::

:::hint Stuck?
Move the print statements and calculations into a main() function. Keep the function definitions outside main(). Add the if __name__ check at the end.
:::

:::answer Reveal answer
```python
# ============ CONSTANTS ============
APP_NAME = "Calculator"

# ============ FUNCTIONS ============
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

# ============ MAIN ============
def main():
    print("Starting", APP_NAME)

    result = add(5, 3)
    print("5 + 3 =", result)

    result = multiply(4, 7)
    print("4 * 7 =", result)

    print("Goodbye!")

if __name__ == "__main__":
    main()
```
:::

