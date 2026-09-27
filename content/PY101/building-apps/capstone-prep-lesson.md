---
title: "Preparing for Your Capstone"
slug: capstone-prep-lesson
description: "Plan and prepare for building your capstone CRUD application"
course_id: PY101
module: building-apps
module_order: 7
topic: capstone-prep
topic_order: 6
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - program-structure-lesson
  - state-management-lesson
  - input-validation-lesson
skills:
  - project-planning
  - application-design
outcomes:
  - "Plan a CRUD application"
  - "Design application structure"
  - "Identify necessary features"
capstone_relevance: "This prepares you to build your capstone project"
---

## Introduction

You've learned Python fundamentals—now it's time to bring it all together! Your **capstone project** is a CRUD (Create, Read, Update, Delete) application that demonstrates everything you've learned.

## What is a CRUD Application?

CRUD apps manage data with four basic operations:

| Operation | Description | Example |
|-----------|-------------|---------|
| **C**reate | Add new items | Add a contact |
| **R**ead | View items | List all contacts |
| **U**pdate | Modify items | Change a phone number |
| **D**elete | Remove items | Remove a contact |

## Sample Capstone Ideas

Choose a domain that interests you:

```python live
capstone_ideas = [
    {
        "name": "Contact Manager",
        "entities": ["Contacts"],
        "features": ["Add contact", "Search contacts", "Update info", "Delete contact"]
    },
    {
        "name": "Task Tracker",
        "entities": ["Tasks", "Categories"],
        "features": ["Create task", "Mark complete", "Filter by status", "Delete task"]
    },
    {
        "name": "Recipe Book",
        "entities": ["Recipes", "Ingredients"],
        "features": ["Add recipe", "Search", "Edit recipe", "Delete recipe"]
    },
    {
        "name": "Expense Tracker",
        "entities": ["Expenses", "Categories"],
        "features": ["Log expense", "View by date/category", "Edit expense", "Reports"]
    },
    {
        "name": "Book Library",
        "entities": ["Books", "Authors"],
        "features": ["Add book", "Search", "Track reading status", "Reviews"]
    }
]

print("=== Capstone Ideas ===\n")
for idea in capstone_ideas:
    print("📁 " + idea["name"])
    print("   Entities:", ", ".join(idea["entities"]))
    print("   Features:", ", ".join(idea["features"][:3]) + "...")
    print()
```

:::expected_output
=== Capstone Ideas ===

📁 Contact Manager
   Entities: Contacts
   Features: Add contact, Search contacts, Update info...

📁 Task Tracker
   Entities: Tasks, Categories
   Features: Create task, Mark complete, Filter by status...

📁 Recipe Book
   Entities: Recipes, Ingredients
   Features: Add recipe, Search, Edit recipe...

📁 Expense Tracker
   Entities: Expenses, Categories
   Features: Log expense, View by date/category, Edit expense...

📁 Book Library
   Entities: Books, Authors
   Features: Add book, Search, Track reading status...
:::

## Planning Your Application

### Step 1: Define Your Data

```python live
# Example: Contact Manager data structure
contact = {
    "id": 1,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "phone": "555-123-4567",
    "category": "friend",
    "created_at": "2024-01-15"
}

# Example: Task Tracker data structure
task = {
    "id": 1,
    "title": "Complete Python course",
    "description": "Finish all modules and capstone",
    "status": "in_progress",  # pending, in_progress, completed
    "priority": "high",
    "due_date": "2024-02-01",
    "created_at": "2024-01-15"
}

print("Contact structure:", contact)
print("\nTask structure:", task)
```

:::expected_output
Contact structure: {'id': 1, 'name': 'Alice Smith', 'email': 'alice@example.com', 'phone': '555-123-4567', 'category': 'friend', 'created_at': '2024-01-15'}

Task structure: {'id': 1, 'title': 'Complete Python course', 'description': 'Finish all modules and capstone', 'status': 'in_progress', 'priority': 'high', 'due_date': '2024-02-01', 'created_at': '2024-01-15'}
:::

### Step 2: Plan Your Functions

```python live
# CRUD functions you'll need
print("=== Functions to Implement ===\n")

functions = {
    "Create": [
        "create_item(data) - Add new item",
        "validate_item(data) - Check data is valid"
    ],
    "Read": [
        "get_all_items() - List all items",
        "get_item(id) - Get one item",
        "search_items(query) - Search items",
        "filter_items(criteria) - Filter by criteria"
    ],
    "Update": [
        "update_item(id, data) - Modify item",
        "validate_update(data) - Check update data"
    ],
    "Delete": [
        "delete_item(id) - Remove item",
        "confirm_delete(id) - Safety check"
    ],
    "Display": [
        "show_menu() - Main menu",
        "display_item(item) - Show one item",
        "display_list(items) - Show list"
    ]
}

for category, funcs in functions.items():
    print(category + ":")
    for func in funcs:
        print("  - " + func)
    print()
```

:::expected_output
=== Functions to Implement ===

Create:
  - create_item(data) - Add new item
  - validate_item(data) - Check data is valid

Read:
  - get_all_items() - List all items
  - get_item(id) - Get one item
  - search_items(query) - Search items
  - filter_items(criteria) - Filter by criteria

Update:
  - update_item(id, data) - Modify item
  - validate_update(data) - Check update data

Delete:
  - delete_item(id) - Remove item
  - confirm_delete(id) - Safety check

Display:
  - show_menu() - Main menu
  - display_item(item) - Show one item
  - display_list(items) - Show list
:::

### Step 3: Design Your Menu

```python live
def show_sample_menu():
    """Example menu structure."""
    print("=" * 40)
    print("      CONTACT MANAGER")
    print("=" * 40)
    print()
    print("  1. Add Contact")
    print("  2. View All Contacts")
    print("  3. Search Contacts")
    print("  4. Update Contact")
    print("  5. Delete Contact")
    print("  6. Exit")
    print()
    print("=" * 40)

show_sample_menu()
```

:::expected_output
========================================
      CONTACT MANAGER
========================================

  1. Add Contact
  2. View All Contacts
  3. Search Contacts
  4. Update Contact
  5. Delete Contact
  6. Exit

========================================
:::

## Application Structure Template

```python live
print("""
# =============================================
# MY CAPSTONE APPLICATION
# =============================================

# ============ IMPORTS ============
import json  # For data persistence

# ============ CONSTANTS ============
APP_NAME = "My App"
DATA_FILE = "data.json"

# ============ STATE ============
app_state = {
    "items": [],
    "next_id": 1
}

# ============ DATA FUNCTIONS (CRUD) ============
def create_item(data):
    pass

def get_all_items():
    pass

def get_item(item_id):
    pass

def update_item(item_id, data):
    pass

def delete_item(item_id):
    pass

# ============ VALIDATION ============
def validate_item(data):
    pass

# ============ SEARCH & FILTER ============
def search_items(query):
    pass

# ============ DISPLAY ============
def show_menu():
    pass

def display_item(item):
    pass

def display_list(items):
    pass

# ============ MAIN LOOP ============
def main():
    while True:
        show_menu()
        choice = get_user_choice()
        handle_choice(choice)

if __name__ == "__main__":
    main()
""")
```

## Features Checklist

```python live
features = {
    "Core CRUD": [
        ("Create new items", True),
        ("View all items", True),
        ("View single item", True),
        ("Update items", True),
        ("Delete items", True)
    ],
    "Data Quality": [
        ("Input validation", True),
        ("Error handling", True),
        ("Confirmation for delete", True)
    ],
    "User Experience": [
        ("Clear menu", True),
        ("Helpful messages", True),
        ("Search functionality", False),  # Optional
        ("Filter/sort", False)  # Optional
    ],
    "Code Quality": [
        ("Organized structure", True),
        ("Meaningful names", True),
        ("Functions documented", True)
    ]
}

print("=== Capstone Checklist ===\n")
for category, items in features.items():
    print(category + ":")
    for item, required in items:
        req = "[Required]" if required else "[Optional]"
        print("  □ " + item + " " + req)
    print()
```

:::expected_output
=== Capstone Checklist ===

Core CRUD:
  □ Create new items [Required]
  □ View all items [Required]
  □ View single item [Required]
  □ Update items [Required]
  □ Delete items [Required]

Data Quality:
  □ Input validation [Required]
  □ Error handling [Required]
  □ Confirmation for delete [Required]

User Experience:
  □ Clear menu [Required]
  □ Helpful messages [Required]
  □ Search functionality [Optional]
  □ Filter/sort [Optional]

Code Quality:
  □ Organized structure [Required]
  □ Meaningful names [Required]
  □ Functions documented [Required]
:::

## Key Points

- Choose a domain that interests you
- Plan your data structure first
- Implement CRUD operations
- Add validation and error handling
- Create a user-friendly menu
- Keep code organized and clean
- Test thoroughly!

:::hint Start Simple
Begin with the simplest version that works—add contacts, list them, delete them. Then enhance with search, validation, and other features.
:::

