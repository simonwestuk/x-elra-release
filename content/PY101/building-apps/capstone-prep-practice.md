---
title: "Practice: Planning Your Capstone"
slug: capstone-prep-practice
description: "Practice planning your capstone application"
course_id: PY101
module: building-apps
module_order: 7
topic: capstone-prep
topic_order: 6
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - capstone-prep-lesson
skills:
  - project-planning
  - application-design
outcomes:
  - "Define application requirements"
  - "Design data structures"
  - "Plan feature implementation"
capstone_relevance: "Direct preparation for your capstone"
---

## Exercise 1: Choose Your Domain

Pick a capstone idea and define it clearly.

```python live
# Fill in your capstone plan
my_capstone = {
    "name": "",  # e.g., "Contact Manager"
    "description": "",  # What does it do?
    "main_entity": "",  # What are you managing?
    "why_chosen": ""  # Why this topic?
}

# Example:
example = {
    "name": "Book Library",
    "description": "Track books I own and want to read",
    "main_entity": "Books",
    "why_chosen": "I love reading and want to organize my collection"
}

print("Example capstone plan:")
for key, value in example.items():
    print("  " + key + ": " + value)

print("\nNow define yours!")
# Fill in my_capstone and print it
```

:::expected_output
Example capstone plan:
  name: Book Library
  description: Track books I own and want to read
  main_entity: Books
  why_chosen: I love reading and want to organize my collection

Now define yours!
:::

:::answer Reveal answer
```python
# Fill in your capstone plan
my_capstone = {
    "name": "Contact Manager",
    "description": "Store and organize personal and professional contacts",
    "main_entity": "Contacts",
    "why_chosen": "I want to keep track of people I meet and their details"
}

# Example:
example = {
    "name": "Book Library",
    "description": "Track books I own and want to read",
    "main_entity": "Books",
    "why_chosen": "I love reading and want to organize my collection"
}

print("Example capstone plan:")
for key, value in example.items():
    print("  " + key + ": " + value)

print("\nMy capstone plan:")
for key, value in my_capstone.items():
    print("  " + key + ": " + value)
```
:::

## Exercise 2: Design Your Data Structure

Design the data structure for your main entity.

```python live
# Design your entity's data structure
# What information do you need to store?

# Example for a Book entity:
book_structure = {
    "id": "int - unique identifier",
    "title": "str - book title",
    "author": "str - author name",
    "isbn": "str - ISBN number (optional)",
    "status": "str - 'to_read', 'reading', 'completed'",
    "rating": "int - 1-5 stars (optional)",
    "notes": "str - personal notes (optional)",
    "added_date": "str - when added"
}

print("Book entity structure:")
for field, description in book_structure.items():
    print("  " + field + ": " + description)

# Now design YOUR entity
print("\nDesign your entity's fields:")
# my_entity = { ... }
```

:::expected_output
Book entity structure:
  id: int - unique identifier
  title: str - book title
  author: str - author name
  isbn: str - ISBN number (optional)
  status: str - 'to_read', 'reading', 'completed'
  rating: int - 1-5 stars (optional)
  notes: str - personal notes (optional)
  added_date: str - when added

Design your entity's fields:
:::

:::hint Thinking Points
- What's the minimum info needed?
- What would be nice to have?
- What type is each field?
- Is it required or optional?
:::

:::answer Reveal answer
```python
# Example for a Contact entity:
contact_structure = {
    "id": "int - unique identifier",
    "name": "str - contact name (required)",
    "email": "str - email address (optional)",
    "phone": "str - phone number (optional)",
    "category": "str - 'personal', 'work', 'family' (required)",
    "notes": "str - personal notes (optional)",
    "added_date": "str - when added (auto-generated)"
}

print("Contact entity structure:")
for field, description in contact_structure.items():
    print("  " + field + ": " + description)

# Tips for designing your entity:
# - Include an 'id' field for unique identification
# - Mark fields as required or optional
# - Choose appropriate types (str, int, float, bool)
# - Consider a 'status' or 'category' field for filtering
```
:::

## Exercise 3: List Your CRUD Operations

Define the specific operations for your application.

```python live
# Define CRUD operations for your application

# Example for Book Library:
book_operations = {
    "Create": {
        "function": "add_book(title, author, status='to_read')",
        "description": "Add a new book to the library",
        "validations": ["title required", "author required", "status must be valid"]
    },
    "Read": {
        "functions": [
            "list_books() - show all books",
            "get_book(id) - get one book",
            "search_books(query) - find by title/author",
            "filter_by_status(status) - show by status"
        ]
    },
    "Update": {
        "function": "update_book(id, **fields)",
        "description": "Update any book field",
        "validations": ["book must exist", "new values must be valid"]
    },
    "Delete": {
        "function": "delete_book(id)",
        "description": "Remove a book",
        "confirmations": ["confirm before delete"]
    }
}

print("Book Library CRUD Operations:")
for operation, details in book_operations.items():
    print("\n" + operation + ":")
    if isinstance(details, dict):
        for key, value in details.items():
            print("  " + key + ": " + str(value))

# Now define YOUR operations
```

:::expected_output
Book Library CRUD Operations:

Create:
  function: add_book(title, author, status='to_read')
  description: Add a new book to the library
  validations: ['title required', 'author required', 'status must be valid']

Read:
  functions: ['list_books() - show all books', 'get_book(id) - get one book', 'search_books(query) - find by title/author', 'filter_by_status(status) - show by status']

Update:
  function: update_book(id, **fields)
  description: Update any book field
  validations: ['book must exist', 'new values must be valid']

Delete:
  function: delete_book(id)
  description: Remove a book
  confirmations: ['confirm before delete']
:::

:::answer Reveal answer
```python
# Example CRUD operations for a Contact Manager:
contact_operations = {
    "Create": {
        "function": "add_contact(name, category, email=None, phone=None)",
        "description": "Add a new contact",
        "validations": ["name required", "category must be valid"]
    },
    "Read": {
        "functions": [
            "list_contacts() - show all contacts",
            "get_contact(id) - get one contact",
            "search_contacts(query) - find by name/email",
            "filter_by_category(category) - show by category"
        ]
    },
    "Update": {
        "function": "update_contact(id, **fields)",
        "description": "Update any contact field",
        "validations": ["contact must exist", "new values must be valid"]
    },
    "Delete": {
        "function": "delete_contact(id)",
        "description": "Remove a contact",
        "confirmations": ["confirm before delete"]
    }
}

print("Contact Manager CRUD Operations:")
for operation, details in contact_operations.items():
    print("\n" + operation + ":")
    if isinstance(details, dict):
        for key, value in details.items():
            print("  " + key + ": " + str(value))
```
:::

## Exercise 4: Design Your Menu

Design the user menu for your application.

```python live
def design_menu():
    """Design your application menu."""
    # Example menu structure
    menu = """
    ╔══════════════════════════════════════╗
    ║          📚 BOOK LIBRARY             ║
    ╠══════════════════════════════════════╣
    ║  1. Add New Book                     ║
    ║  2. View All Books                   ║
    ║  3. Search Books                     ║
    ║  4. Update Book                      ║
    ║  5. Delete Book                      ║
    ║  6. View by Status                   ║
    ║  7. Statistics                       ║
    ║  0. Exit                             ║
    ╚══════════════════════════════════════╝
    """
    print(menu)

    # Menu options with descriptions
    options = {
        "1": ("Add New Book", "Enter title, author, and initial status"),
        "2": ("View All Books", "Display complete book list"),
        "3": ("Search Books", "Find books by title or author"),
        "4": ("Update Book", "Modify book details"),
        "5": ("Delete Book", "Remove a book (with confirmation)"),
        "6": ("View by Status", "Filter: to_read, reading, completed"),
        "7": ("Statistics", "Show reading progress stats"),
        "0": ("Exit", "Save and quit")
    }

    print("Menu option details:")
    for num, (name, desc) in options.items():
        print("  " + num + ". " + name + " - " + desc)

design_menu()

# Now design YOUR menu
```

:::expected_output

    ╔══════════════════════════════════════╗
    ║          📚 BOOK LIBRARY             ║
    ╠══════════════════════════════════════╣
    ║  1. Add New Book                     ║
    ║  2. View All Books                   ║
    ║  3. Search Books                     ║
    ║  4. Update Book                      ║
    ║  5. Delete Book                      ║
    ║  6. View by Status                   ║
    ║  7. Statistics                       ║
    ║  0. Exit                             ║
    ╚══════════════════════════════════════╝

Menu option details:
  1. Add New Book - Enter title, author, and initial status
  2. View All Books - Display complete book list
  3. Search Books - Find books by title or author
  4. Update Book - Modify book details
  5. Delete Book - Remove a book (with confirmation)
  6. View by Status - Filter: to_read, reading, completed
  7. Statistics - Show reading progress stats
  0. Exit - Save and quit
:::

:::answer Reveal answer
```python
def design_menu():
    """Design your application menu."""
    menu = """
    ======================================
            CONTACT MANAGER
    ======================================
      1. Add New Contact
      2. View All Contacts
      3. Search Contacts
      4. Update Contact
      5. Delete Contact
      6. View by Category
      7. Statistics
      0. Exit
    ======================================
    """
    print(menu)

    options = {
        "1": ("Add New Contact", "Enter name, category, email, phone"),
        "2": ("View All Contacts", "Display complete contact list"),
        "3": ("Search Contacts", "Find contacts by name or email"),
        "4": ("Update Contact", "Modify contact details"),
        "5": ("Delete Contact", "Remove a contact (with confirmation)"),
        "6": ("View by Category", "Filter: personal, work, family"),
        "7": ("Statistics", "Show contact count by category"),
        "0": ("Exit", "Save and quit")
    }

    print("Menu option details:")
    for num, (name, desc) in options.items():
        print("  " + num + ". " + name + " - " + desc)

design_menu()
```
:::

## Exercise 5: Implementation Roadmap

Create a step-by-step plan for building your capstone.

```python live
roadmap = [
    {
        "phase": "Phase 1: Setup",
        "tasks": [
            "Create project file structure",
            "Define constants and configuration",
            "Set up state/data storage",
            "Create main() function shell"
        ],
        "time": "Day 1"
    },
    {
        "phase": "Phase 2: Core CRUD",
        "tasks": [
            "Implement create function",
            "Implement read/list function",
            "Implement update function",
            "Implement delete function"
        ],
        "time": "Days 2-3"
    },
    {
        "phase": "Phase 3: Validation",
        "tasks": [
            "Add input validation",
            "Add error handling",
            "Add delete confirmation"
        ],
        "time": "Day 4"
    },
    {
        "phase": "Phase 4: UI & Polish",
        "tasks": [
            "Create menu system",
            "Add display formatting",
            "Improve user messages",
            "Test all features"
        ],
        "time": "Day 5"
    },
    {
        "phase": "Phase 5: Enhancements",
        "tasks": [
            "Add search functionality",
            "Add filtering/sorting",
            "Add statistics/reports",
            "Final testing"
        ],
        "time": "Days 6-7"
    }
]

print("=== Capstone Implementation Roadmap ===\n")
for phase in roadmap:
    print(phase["phase"] + " (" + phase["time"] + ")")
    for task in phase["tasks"]:
        print("  □ " + task)
    print()

# Now customize this for YOUR capstone
```

:::expected_output
=== Capstone Implementation Roadmap ===

Phase 1: Setup (Day 1)
  □ Create project file structure
  □ Define constants and configuration
  □ Set up state/data storage
  □ Create main() function shell

Phase 2: Core CRUD (Days 2-3)
  □ Implement create function
  □ Implement read/list function
  □ Implement update function
  □ Implement delete function

Phase 3: Validation (Day 4)
  □ Add input validation
  □ Add error handling
  □ Add delete confirmation

Phase 4: UI & Polish (Day 5)
  □ Create menu system
  □ Add display formatting
  □ Improve user messages
  □ Test all features

Phase 5: Enhancements (Days 6-7)
  □ Add search functionality
  □ Add filtering/sorting
  □ Add statistics/reports
  □ Final testing
:::

:::hint Planning Tips
- Start with the minimum viable product
- Get CRUD working before adding extras
- Test each feature before moving on
- Keep a list of "nice to have" features
:::

:::answer Reveal answer
```python
roadmap = [
    {
        "phase": "Phase 1: Setup",
        "tasks": [
            "Create project file structure",
            "Define constants and configuration",
            "Set up state/data storage",
            "Create main() function shell"
        ],
        "time": "Day 1"
    },
    {
        "phase": "Phase 2: Core CRUD",
        "tasks": [
            "Implement create function",
            "Implement read/list function",
            "Implement update function",
            "Implement delete function"
        ],
        "time": "Days 2-3"
    },
    {
        "phase": "Phase 3: Validation",
        "tasks": [
            "Add input validation",
            "Add error handling",
            "Add delete confirmation"
        ],
        "time": "Day 4"
    },
    {
        "phase": "Phase 4: UI & Polish",
        "tasks": [
            "Create menu system",
            "Add display formatting",
            "Improve user messages",
            "Test all features"
        ],
        "time": "Day 5"
    },
    {
        "phase": "Phase 5: Enhancements",
        "tasks": [
            "Add search functionality",
            "Add filtering/sorting",
            "Add statistics/reports",
            "Final testing"
        ],
        "time": "Days 6-7"
    }
]

print("=== Capstone Implementation Roadmap ===\n")
for phase in roadmap:
    print(phase["phase"] + " (" + phase["time"] + ")")
    for task in phase["tasks"]:
        print("  - " + task)
    print()

# Key tips:
# 1. Start with Phase 1 - get the skeleton working
# 2. Phase 2 is the most important - core CRUD operations
# 3. Don't skip Phase 3 - validation prevents bugs
# 4. Phase 4 makes it user-friendly
# 5. Phase 5 is bonus - only if time permits
```
:::

