---
title: "Practice: State Management"
slug: state-management-practice
description: "Practice managing application state"
course_id: PY101
module: building-apps
module_order: 7
topic: state-management
topic_order: 4
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - state-management-lesson
skills:
  - state-management
  - data-structures
outcomes:
  - "Design state structures"
  - "Create state modification functions"
  - "Implement safe state changes"
capstone_relevance: "Practice patterns you'll use in your capstone"
---

## Exercise 1: Counter State

Create a simple counter with state management.

```python live
# State
counter_state = {"value": 0}

def increment():
    """Increase counter by 1."""
    # Your code here
    pass

def decrement():
    """Decrease counter by 1 (not below 0)."""
    # Your code here
    pass

def reset():
    """Reset counter to 0."""
    # Your code here
    pass

def get_value():
    """Get current counter value."""
    # Your code here
    pass

# Test
increment()
increment()
increment()
print("After 3 increments:", get_value())  # 3

decrement()
print("After decrement:", get_value())  # 2

reset()
print("After reset:", get_value())  # 0

decrement()  # Should not go below 0
print("After decrement at 0:", get_value())  # 0
```

:::expected_output
After 3 increments: 3
After decrement: 2
After reset: 0
After decrement at 0: 0
:::

:::hint Stuck?
For increment: `counter_state["value"] += 1`. For decrement: check if value > 0 first.
:::

:::answer Reveal answer
```python
# State
counter_state = {"value": 0}

def increment():
    """Increase counter by 1."""
    counter_state["value"] += 1

def decrement():
    """Decrease counter by 1 (not below 0)."""
    if counter_state["value"] > 0:
        counter_state["value"] -= 1

def reset():
    """Reset counter to 0."""
    counter_state["value"] = 0

def get_value():
    """Get current counter value."""
    return counter_state["value"]

# Test
increment()
increment()
increment()
print("After 3 increments:", get_value())  # 3

decrement()
print("After decrement:", get_value())  # 2

reset()
print("After reset:", get_value())  # 0

decrement()  # Should not go below 0
print("After decrement at 0:", get_value())  # 0
```
:::

## Exercise 2: User Session State

Create state management for user sessions.

```python live
# State
session = {
    "user": None,
    "logged_in_at": None,
    "permissions": []
}

def login(username, permissions=None):
    """Log in a user with optional permissions."""
    # Your code here
    pass

def logout():
    """Log out current user."""
    # Your code here
    pass

def is_logged_in():
    """Check if a user is logged in."""
    # Your code here
    pass

def has_permission(permission):
    """Check if current user has a permission."""
    # Your code here
    pass

# Test
print("Logged in:", is_logged_in())  # False

login("alice", ["read", "write"])
print("Logged in:", is_logged_in())  # True
print("User:", session["user"])
print("Has read:", has_permission("read"))  # True
print("Has delete:", has_permission("delete"))  # False

logout()
print("After logout:", is_logged_in())  # False
```

:::expected_output
Logged in: False
Logged in: True
User: alice
Has read: True
Has delete: False
After logout: False
:::

:::hint Stuck?
login sets session["user"] and session["permissions"]. logout resets them to None and [].
:::

:::answer Reveal answer
```python
# State
session = {
    "user": None,
    "logged_in_at": None,
    "permissions": []
}

def login(username, permissions=None):
    """Log in a user with optional permissions."""
    session["user"] = username
    session["logged_in_at"] = "now"
    session["permissions"] = permissions if permissions is not None else []

def logout():
    """Log out current user."""
    session["user"] = None
    session["logged_in_at"] = None
    session["permissions"] = []

def is_logged_in():
    """Check if a user is logged in."""
    return session["user"] is not None

def has_permission(permission):
    """Check if current user has a permission."""
    return permission in session["permissions"]

# Test
print("Logged in:", is_logged_in())  # False

login("alice", ["read", "write"])
print("Logged in:", is_logged_in())  # True
print("User:", session["user"])
print("Has read:", has_permission("read"))  # True
print("Has delete:", has_permission("delete"))  # False

logout()
print("After logout:", is_logged_in())  # False
```
:::

## Exercise 3: Shopping Cart State

Implement a shopping cart with item management.

```python live
# State
cart = {
    "items": [],
    "total": 0
}

def add_to_cart(name, price, quantity=1):
    """Add item to cart."""
    # Your code here
    pass

def remove_from_cart(name):
    """Remove item from cart by name."""
    # Your code here
    pass

def update_total():
    """Recalculate cart total."""
    # Your code here
    pass

def get_cart_summary():
    """Return cart summary."""
    # Your code here
    pass

# Test
add_to_cart("Book", 15.99, 2)
add_to_cart("Pen", 2.99, 5)
print(get_cart_summary())

remove_from_cart("Book")
print(get_cart_summary())
```

:::expected_output
Cart (2 items):
  Book x2 = $31.98
  Pen x5 = $14.95
Total: $46.93
Cart (1 items):
  Pen x5 = $14.95
Total: $14.95
:::

:::hint Stuck?
Store items as dicts: `{"name": name, "price": price, "quantity": quantity}`. Total = sum of (price × quantity) for all items.
:::

:::answer Reveal answer
```python
# State
cart = {
    "items": [],
    "total": 0
}

def add_to_cart(name, price, quantity=1):
    """Add item to cart."""
    cart["items"].append({"name": name, "price": price, "quantity": quantity})
    update_total()

def remove_from_cart(name):
    """Remove item from cart by name."""
    cart["items"] = [item for item in cart["items"] if item["name"] != name]
    update_total()

def update_total():
    """Recalculate cart total."""
    cart["total"] = sum(item["price"] * item["quantity"] for item in cart["items"])

def get_cart_summary():
    """Return cart summary."""
    summary = "Cart (" + str(len(cart["items"])) + " items):\n"
    for item in cart["items"]:
        summary += "  " + item["name"] + " x" + str(item["quantity"]) + " = $" + str(round(item["price"] * item["quantity"], 2)) + "\n"
    summary += "Total: $" + str(round(cart["total"], 2))
    return summary

# Test
add_to_cart("Book", 15.99, 2)
add_to_cart("Pen", 2.99, 5)
print(get_cart_summary())

remove_from_cart("Book")
print(get_cart_summary())
```
:::

## Exercise 4: Inventory State

Create inventory state with stock tracking.

```python live
# State
inventory = {
    "products": {},
    "low_stock_threshold": 10
}

def add_product(product_id, name, stock):
    """Add a product to inventory."""
    # Your code here
    pass

def update_stock(product_id, change):
    """Update stock level (positive or negative)."""
    # Your code here
    pass

def get_low_stock_products():
    """Return products below threshold."""
    # Your code here
    pass

def get_product(product_id):
    """Get product details."""
    # Your code here
    pass

# Test
add_product("P001", "Widget", 50)
add_product("P002", "Gadget", 8)
add_product("P003", "Gizmo", 25)

print("Low stock:", get_low_stock_products())  # Should show P002

update_stock("P001", -45)  # Sell 45 widgets
print("After sale:", get_product("P001"))

print("Low stock now:", get_low_stock_products())  # P001 and P002
```

:::expected_output
Low stock: ['P002: Gadget (8)']
After sale: {'name': 'Widget', 'stock': 5}
Low stock now: ['P001: Widget (5)', 'P002: Gadget (8)']
:::

:::hint Stuck?
Store products as `inventory["products"][product_id] = {"name": name, "stock": stock}`. Check stock against threshold.
:::

:::answer Reveal answer
```python
# State
inventory = {
    "products": {},
    "low_stock_threshold": 10
}

def add_product(product_id, name, stock):
    """Add a product to inventory."""
    inventory["products"][product_id] = {"name": name, "stock": stock}

def update_stock(product_id, change):
    """Update stock level (positive or negative)."""
    if product_id in inventory["products"]:
        inventory["products"][product_id]["stock"] += change
        if inventory["products"][product_id]["stock"] < 0:
            inventory["products"][product_id]["stock"] = 0

def get_low_stock_products():
    """Return products below threshold."""
    low_stock = []
    for product_id, product in inventory["products"].items():
        if product["stock"] < inventory["low_stock_threshold"]:
            low_stock.append(product_id + ": " + product["name"] + " (" + str(product["stock"]) + ")")
    return low_stock

def get_product(product_id):
    """Get product details."""
    if product_id in inventory["products"]:
        return inventory["products"][product_id]
    return None

# Test
add_product("P001", "Widget", 50)
add_product("P002", "Gadget", 8)
add_product("P003", "Gizmo", 25)

print("Low stock:", get_low_stock_products())  # Should show P002

update_stock("P001", -45)  # Sell 45 widgets
print("After sale:", get_product("P001"))

print("Low stock now:", get_low_stock_products())  # P001 and P002
```
:::

## Exercise 5: Game State

Create state for a simple game.

```python live
# State
game = {
    "player": {
        "name": None,
        "health": 100,
        "score": 0,
        "inventory": []
    },
    "level": 1,
    "game_over": False
}

def start_game(player_name):
    """Initialize game with player name."""
    # Your code here
    pass

def take_damage(amount):
    """Reduce health. Set game_over if health reaches 0."""
    # Your code here
    pass

def add_score(points):
    """Add to player score."""
    # Your code here
    pass

def pick_up_item(item):
    """Add item to inventory."""
    # Your code here
    pass

def next_level():
    """Advance to next level."""
    # Your code here
    pass

def get_game_status():
    """Return current game status."""
    # Your code here
    pass

# Test
start_game("Hero")
print(get_game_status())

add_score(100)
pick_up_item("Sword")
pick_up_item("Shield")
take_damage(30)
print(get_game_status())

next_level()
take_damage(80)  # Should trigger game over
print(get_game_status())
```

:::expected_output
Hero | Level: 1 | Health: 100 | Score: 0 | Items: []
Hero | Level: 1 | Health: 70 | Score: 100 | Items: ['Sword', 'Shield']
Hero | Level: 2 | Health: 0 | Score: 100 | Items: ['Sword', 'Shield'] | GAME OVER
:::

:::hint Stuck?
take_damage should check if health goes to 0 or below, then set game_over = True.
:::

:::answer Reveal answer
```python
# State
game = {
    "player": {
        "name": None,
        "health": 100,
        "score": 0,
        "inventory": []
    },
    "level": 1,
    "game_over": False
}

def start_game(player_name):
    """Initialize game with player name."""
    game["player"]["name"] = player_name
    game["player"]["health"] = 100
    game["player"]["score"] = 0
    game["player"]["inventory"] = []
    game["level"] = 1
    game["game_over"] = False

def take_damage(amount):
    """Reduce health. Set game_over if health reaches 0."""
    if game["game_over"]:
        return
    game["player"]["health"] -= amount
    if game["player"]["health"] <= 0:
        game["player"]["health"] = 0
        game["game_over"] = True

def add_score(points):
    """Add to player score."""
    game["player"]["score"] += points

def pick_up_item(item):
    """Add item to inventory."""
    game["player"]["inventory"].append(item)

def next_level():
    """Advance to next level."""
    game["level"] += 1

def get_game_status():
    """Return current game status."""
    p = game["player"]
    status = p["name"] + " | Level: " + str(game["level"])
    status += " | Health: " + str(p["health"])
    status += " | Score: " + str(p["score"])
    status += " | Items: " + str(p["inventory"])
    if game["game_over"]:
        status += " | GAME OVER"
    return status

# Test
start_game("Hero")
print(get_game_status())

add_score(100)
pick_up_item("Sword")
pick_up_item("Shield")
take_damage(30)
print(get_game_status())

next_level()
take_damage(80)  # Should trigger game over
print(get_game_status())
```
:::

