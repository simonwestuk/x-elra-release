---
title: "Managing Application State"
slug: state-management-lesson
description: "Learn to manage data that changes over time in your applications"
course_id: PY101
module: building-apps
module_order: 7
topic: state-management
topic_order: 4
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - dicts-lesson
  - defining-functions-lesson
skills:
  - state-management
  - data-structures
outcomes:
  - "Understand application state"
  - "Design state structures"
  - "Implement state changes safely"
capstone_relevance: "State management is central to CRUD applications"
---

## Introduction

**Application state** is the data your program tracks as it runs. Managing state well is crucial for building interactive applications. This includes user data, settings, session information, and any data that changes during program execution.

## What is State?

```python live
# These variables hold application state
current_user = None
cart_items = []
is_logged_in = False

# State changes as the program runs
current_user = "Alice"
is_logged_in = True
cart_items.append("Book")

print("User:", current_user)
print("Logged in:", is_logged_in)
print("Cart:", cart_items)
```

:::expected_output
User: Alice
Logged in: True
Cart: ['Book']
:::

## Centralizing State

Instead of scattered variables, use a single state object:

```python live
# BAD: Scattered state
username = None
user_email = None
user_role = None
login_time = None

# GOOD: Centralized state
app_state = {
    "user": {
        "username": None,
        "email": None,
        "role": None
    },
    "session": {
        "logged_in": False,
        "login_time": None
    },
    "cart": {
        "items": [],
        "total": 0
    }
}

print("Initial state:")
print(app_state)
```

:::expected_output
Initial state:
{'user': {'username': None, 'email': None, 'role': None}, 'session': {'logged_in': False, 'login_time': None}, 'cart': {'items': [], 'total': 0}}
:::

## State Management Functions

Create functions to modify state safely:

```python live
# Application state
state = {
    "users": [],
    "current_user": None,
    "tasks": []
}

# State modifiers
def add_user(name, email):
    """Add a new user to state."""
    user = {"name": name, "email": email, "id": len(state["users"]) + 1}
    state["users"].append(user)
    return user

def login(user_id):
    """Set current user by ID."""
    for user in state["users"]:
        if user["id"] == user_id:
            state["current_user"] = user
            return True
    return False

def logout():
    """Clear current user."""
    state["current_user"] = None

def add_task(title):
    """Add task for current user."""
    if not state["current_user"]:
        return None
    task = {
        "title": title,
        "user_id": state["current_user"]["id"],
        "done": False
    }
    state["tasks"].append(task)
    return task

# Use the state functions
alice = add_user("Alice", "alice@email.com")
bob = add_user("Bob", "bob@email.com")

print("Users:", state["users"])

login(1)
print("Logged in as:", state["current_user"]["name"])

add_task("Learn Python")
add_task("Build capstone")
print("Tasks:", state["tasks"])

logout()
print("Current user after logout:", state["current_user"])
```

:::expected_output
Users: [{'name': 'Alice', 'email': 'alice@email.com', 'id': 1}, {'name': 'Bob', 'email': 'bob@email.com', 'id': 2}]
Logged in as: Alice
Tasks: [{'title': 'Learn Python', 'user_id': 1, 'done': False}, {'title': 'Build capstone', 'user_id': 1, 'done': False}]
Current user after logout: None
:::

## State Patterns

### 1. Read-Only Access

```python live
state = {"count": 0, "items": ["a", "b", "c"]}

def get_count():
    """Read-only access to count."""
    return state["count"]

def get_items():
    """Return a copy to prevent direct modification."""
    return state["items"].copy()

# Safe access
items = get_items()
items.append("d")  # Modifies the copy

print("Original items:", state["items"])  # Unchanged
print("Modified copy:", items)
```

:::expected_output
Original items: ['a', 'b', 'c']
Modified copy: ['a', 'b', 'c', 'd']
:::

### 2. Controlled Updates

```python live
state = {"score": 0}

def add_score(points):
    """Add points with validation."""
    if points < 0:
        print("Error: Cannot add negative points")
        return
    state["score"] += points
    print("Score is now:", state["score"])

add_score(10)
add_score(5)
add_score(-3)  # Rejected
```

:::expected_output
Score is now: 10
Score is now: 15
Error: Cannot add negative points
:::

### 3. Transaction-like Updates

```python live
def transfer_money(from_account, to_account, amount, accounts):
    """Transfer money safely between accounts."""
    # Validate first
    if from_account not in accounts:
        return False, "Source account not found"
    if to_account not in accounts:
        return False, "Destination account not found"
    if accounts[from_account] < amount:
        return False, "Insufficient funds"

    # Then update (both changes together)
    accounts[from_account] -= amount
    accounts[to_account] += amount
    return True, "Transfer complete"

accounts = {"alice": 100, "bob": 50}
print("Before:", accounts)

success, message = transfer_money("alice", "bob", 30, accounts)
print(message)
print("After:", accounts)
```

:::expected_output
Before: {'alice': 100, 'bob': 50}
Transfer complete
After: {'alice': 70, 'bob': 80}
:::

## State for a Todo Application

```python live
# Complete state structure for a todo app
todo_state = {
    "todos": [],
    "next_id": 1,
    "filter": "all"  # "all", "active", "completed"
}

def add_todo(title):
    """Add a new todo item."""
    todo = {
        "id": todo_state["next_id"],
        "title": title,
        "completed": False
    }
    todo_state["todos"].append(todo)
    todo_state["next_id"] += 1
    return todo

def toggle_todo(todo_id):
    """Toggle todo completion status."""
    for todo in todo_state["todos"]:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            return True
    return False

def delete_todo(todo_id):
    """Delete a todo by ID."""
    todo_state["todos"] = [t for t in todo_state["todos"] if t["id"] != todo_id]

def get_filtered_todos():
    """Get todos based on current filter."""
    filter_type = todo_state["filter"]
    if filter_type == "active":
        return [t for t in todo_state["todos"] if not t["completed"]]
    elif filter_type == "completed":
        return [t for t in todo_state["todos"] if t["completed"]]
    return todo_state["todos"]

def set_filter(filter_type):
    """Set the current filter."""
    if filter_type in ["all", "active", "completed"]:
        todo_state["filter"] = filter_type

# Demo
add_todo("Learn Python")
add_todo("Build project")
add_todo("Deploy app")

toggle_todo(1)  # Complete "Learn Python"

print("All todos:", get_filtered_todos())

set_filter("active")
print("Active todos:", get_filtered_todos())

set_filter("completed")
print("Completed todos:", get_filtered_todos())
```

:::expected_output
All todos: [{'id': 1, 'title': 'Learn Python', 'completed': True}, {'id': 2, 'title': 'Build project', 'completed': False}, {'id': 3, 'title': 'Deploy app', 'completed': False}]
Active todos: [{'id': 2, 'title': 'Build project', 'completed': False}, {'id': 3, 'title': 'Deploy app', 'completed': False}]
Completed todos: [{'id': 1, 'title': 'Learn Python', 'completed': True}]
:::

## Key Points

- Centralize state in a single structure
- Create functions to modify state
- Validate before modifying
- Provide read-only access when possible
- Keep state changes predictable
- Design state structure upfront

:::hint Remember
Good state management makes your application predictable and easier to debug. When something goes wrong, you know exactly where to look!
:::

