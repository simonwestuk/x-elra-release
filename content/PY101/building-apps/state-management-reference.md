---
title: "Quick Reference: State Management"
slug: state-management-reference
description: "Quick reference for managing application state"
course_id: PY101
module: building-apps
module_order: 7
topic: state-management
topic_order: 4
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - state-management
  - data-structures
outcomes:
  - "Quick lookup for state patterns"
  - "Review state management techniques"
capstone_relevance: "State management reference for your project"
---

## Quick Reference: State Management

### Centralized State

```python
# Single state object
app_state = {
    "users": [],
    "current_user": None,
    "settings": {},
    "data": []
}
```

### State Modifier Pattern

```python
def modify_state(value):
    """Modify state through functions."""
    app_state["key"] = value

# Read-only access
def get_value():
    return app_state["key"]
```

### CRUD Operations

```python
# CREATE
def create_item(name):
    item = {"id": next_id(), "name": name}
    state["items"].append(item)
    return item

# READ
def get_item(item_id):
    for item in state["items"]:
        if item["id"] == item_id:
            return item
    return None

# UPDATE
def update_item(item_id, name):
    item = get_item(item_id)
    if item:
        item["name"] = name
        return True
    return False

# DELETE
def delete_item(item_id):
    state["items"] = [i for i in state["items"]
                      if i["id"] != item_id]
```

### ID Generation

```python
state = {"next_id": 1}

def get_next_id():
    id = state["next_id"]
    state["next_id"] += 1
    return id
```

### Session Pattern

```python
session = {
    "user": None,
    "logged_in": False
}

def login(user):
    session["user"] = user
    session["logged_in"] = True

def logout():
    session["user"] = None
    session["logged_in"] = False

def is_logged_in():
    return session["logged_in"]
```

### Filtering Data

```python
# Get filtered items
def get_active_items():
    return [i for i in state["items"]
            if i["status"] == "active"]

# Get by owner
def get_user_items(user_id):
    return [i for i in state["items"]
            if i["user_id"] == user_id]
```

### Safe Updates

```python
def update_safely(item_id, updates):
    item = get_item(item_id)
    if not item:
        return False, "Not found"

    # Validate updates
    if "name" in updates and not updates["name"]:
        return False, "Name required"

    # Apply updates
    for key, value in updates.items():
        item[key] = value
    return True, "Updated"
```

### Common State Structures

```python
# User state
user_state = {
    "users": [],
    "current_user": None
}

# List with filtering
list_state = {
    "items": [],
    "filter": "all",  # "all", "active", "done"
    "sort": "date"
}

# Inventory
inventory = {
    "products": {},  # id -> product
    "categories": []
}

# Session
session = {
    "user_id": None,
    "token": None,
    "expires": None
}
```

### State Best Practices

| Do | Don't |
|----|-------|
| Centralize state | Scatter variables |
| Use functions to modify | Modify directly |
| Validate before changing | Assume valid data |
| Return copies for reads | Return references |
| Keep state structure flat | Deep nesting |

### Debugging State

```python
def print_state():
    """Debug helper."""
    import json
    print(json.dumps(state, indent=2))
```

### See Also

- [Dictionaries](dicts-lesson.html) - Dict operations
- [Functions](defining-functions-lesson.html) - Creating functions
- [Program Structure](program-structure-lesson.html) - Code organization

