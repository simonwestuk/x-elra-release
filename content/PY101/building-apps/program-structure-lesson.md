---
title: "Structuring Your Programs"
slug: program-structure-lesson
description: "Learn to organize code into well-structured programs"
course_id: PY101
module: building-apps
module_order: 7
topic: program-structure
topic_order: 1
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - defining-functions-lesson
  - scope-lesson
skills:
  - program-design
  - code-organization
outcomes:
  - "Organize code into logical sections"
  - "Separate concerns in your programs"
  - "Create maintainable program structures"
capstone_relevance: "Good structure is essential for your capstone project"
---

## Introduction

As your programs grow larger, organization becomes crucial. A well-structured program is easier to understand, maintain, and extend. This lesson covers patterns for organizing Python programs.

## Basic Program Structure

A typical Python program follows this pattern:

```python live
# 1. IMPORTS (if any)
# import module_name

# 2. CONSTANTS
MAX_ITEMS = 100
APP_NAME = "My Application"

# 3. HELPER FUNCTIONS
def helper_function():
    """Small utility functions."""
    pass

# 4. MAIN FUNCTIONS
def main_feature():
    """Core functionality."""
    pass

# 5. MAIN ENTRY POINT
def main():
    """Program entry point."""
    print("Starting " + APP_NAME)
    main_feature()

# 6. RUN IF MAIN
if __name__ == "__main__":
    main()
```

:::expected_output
Starting My Application
:::

## Why Structure Matters

```python live
# BAD: Everything mixed together
print("Welcome!")
name = "Alice"
total = 0
items = []
print("Processing...")
for i in range(5):
    items.append(i)
    total += i
print("Done!")
print("Total:", total)
print("Goodbye,", name)

print("\n" + "="*40 + "\n")

# GOOD: Organized into functions
def greet(name):
    print("Welcome!")
    return name

def process_items(count):
    items = []
    total = 0
    for i in range(count):
        items.append(i)
        total += i
    return items, total

def farewell(name):
    print("Goodbye,", name)

def main():
    user = greet("Alice")
    print("Processing...")
    items, total = process_items(5)
    print("Done!")
    print("Total:", total)
    farewell(user)

main()
```

:::expected_output
Welcome!
Processing...
Done!
Total: 10
Goodbye, Alice

========================================

Welcome!
Processing...
Done!
Total: 10
Goodbye, Alice
:::

## Separation of Concerns

Divide your program into distinct sections:

```python live
# ============ DATA LAYER ============
def create_user(name, email):
    """Create a user record."""
    return {"name": name, "email": email, "active": True}

def get_user_display_name(user):
    """Get formatted display name."""
    return user["name"]

# ============ BUSINESS LOGIC ============
def validate_email(email):
    """Check if email is valid."""
    return "@" in email and "." in email

def can_user_login(user):
    """Check if user can log in."""
    return user["active"]

# ============ USER INTERFACE ============
def display_welcome(user):
    """Show welcome message."""
    print("Welcome, " + get_user_display_name(user) + "!")

def display_error(message):
    """Show error message."""
    print("Error:", message)

# ============ MAIN PROGRAM ============
def main():
    email = "alice@example.com"

    if not validate_email(email):
        display_error("Invalid email")
        return

    user = create_user("Alice", email)

    if can_user_login(user):
        display_welcome(user)
    else:
        display_error("Account is disabled")

main()
```

:::expected_output
Welcome, Alice!
:::

## The main() Function Pattern

```python live
def setup():
    """Initialize the application."""
    print("Setting up...")
    return {"initialized": True}

def run(config):
    """Run the main application."""
    print("Running with config:", config)
    return True

def cleanup():
    """Clean up resources."""
    print("Cleaning up...")

def main():
    """Main entry point."""
    config = setup()

    try:
        success = run(config)
        if success:
            print("Completed successfully!")
    finally:
        cleanup()

# This pattern allows the program to be
# imported as a module without running
if __name__ == "__main__":
    main()
```

:::expected_output
Setting up...
Running with config: {'initialized': True}
Completed successfully!
Cleaning up...
:::

## Organizing by Feature

```python live
# ============ USER MANAGEMENT ============
def create_user(name):
    return {"name": name, "items": []}

def get_user_items(user):
    return user["items"]

# ============ ITEM MANAGEMENT ============
def create_item(name, price):
    return {"name": name, "price": price}

def add_item_to_user(user, item):
    user["items"].append(item)

# ============ REPORTING ============
def calculate_total(items):
    return sum(item["price"] for item in items)

def generate_report(user):
    items = get_user_items(user)
    total = calculate_total(items)
    print("User:", user["name"])
    print("Items:", len(items))
    print("Total: $" + str(total))

# ============ MAIN ============
def main():
    # Create user and add items
    user = create_user("Alice")
    add_item_to_user(user, create_item("Book", 15.99))
    add_item_to_user(user, create_item("Pen", 2.99))
    add_item_to_user(user, create_item("Notebook", 8.99))

    # Generate report
    generate_report(user)

main()
```

:::expected_output
User: Alice
Items: 3
Total: $27.97
:::

## Using Constants

```python live
# Constants at the top - easy to find and modify
APP_NAME = "Task Manager"
VERSION = "1.0"
MAX_TASKS = 100
DEFAULT_PRIORITY = "medium"

def show_header():
    print("=" * 30)
    print(APP_NAME + " v" + VERSION)
    print("=" * 30)

def create_task(title):
    return {
        "title": title,
        "priority": DEFAULT_PRIORITY,
        "done": False
    }

def main():
    show_header()
    task = create_task("Learn Python")
    print("Created task:", task["title"])
    print("Max tasks allowed:", MAX_TASKS)

main()
```

:::expected_output
==============================
Task Manager v1.0
==============================
Created task: Learn Python
Max tasks allowed: 100
:::

## Key Points

- Put imports at the top
- Define constants after imports
- Group related functions together
- Use a main() function as entry point
- Separate data, logic, and presentation
- Use comments to mark sections
- Keep functions focused on one task

:::hint Remember
Good structure isn't about following rules rigidly—it's about making your code easy to understand and modify. If someone (including future you) can quickly find what they're looking for, you've done it right!
:::

