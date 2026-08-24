---
title: "Challenge: Build a Mini CRUD Application"
slug: capstone-prep-challenge
description: "Build a small CRUD application as capstone practice"
course_id: PY101
module: building-apps
module_order: 7
topic: capstone-prep
topic_order: 6
type: challenge
difficulty: beginner
estimated_minutes: 30
prerequisites:
  - capstone-prep-practice
skills:
  - project-planning
  - application-design
outcomes:
  - "Build a complete mini application"
  - "Apply all course concepts"
  - "Prepare for full capstone"
capstone_relevance: "This is a practice run for your capstone"
---

## Challenge: Build a Note Manager

Build a complete mini CRUD application for managing notes. This is a smaller version of what your capstone will be.

### Requirements

**Data Structure:**
- Note: id, title, content, category, created_at

**Features:**
1. Add new notes
2. List all notes
3. View a single note
4. Update note content
5. Delete notes
6. Filter by category
7. Search notes

### Complete Implementation

```python live
# =============================================
# NOTE MANAGER - Mini CRUD Application
# =============================================

# ============ IMPORTS ============
from datetime import datetime

# ============ CONSTANTS ============
APP_NAME = "Note Manager"
CATEGORIES = ["personal", "work", "ideas", "other"]

# ============ STATE ============
app_state = {
    "notes": [],
    "next_id": 1
}

# ============ DATA FUNCTIONS ============
def create_note(title, content, category="other"):
    """Create a new note."""
    # Validate
    if not title or not title.strip():
        return None, "Title is required"
    if category not in CATEGORIES:
        return None, "Invalid category"

    # Create note
    note = {
        "id": app_state["next_id"],
        "title": title.strip(),
        "content": content.strip() if content else "",
        "category": category,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    app_state["notes"].append(note)
    app_state["next_id"] += 1
    return note, None

def get_all_notes():
    """Return all notes."""
    return app_state["notes"]

def get_note(note_id):
    """Get a single note by ID."""
    for note in app_state["notes"]:
        if note["id"] == note_id:
            return note
    return None

def update_note(note_id, title=None, content=None, category=None):
    """Update a note's fields."""
    note = get_note(note_id)
    if not note:
        return False, "Note not found"

    if title is not None:
        if not title.strip():
            return False, "Title cannot be empty"
        note["title"] = title.strip()

    if content is not None:
        note["content"] = content.strip()

    if category is not None:
        if category not in CATEGORIES:
            return False, "Invalid category"
        note["category"] = category

    return True, "Note updated"

def delete_note(note_id):
    """Delete a note by ID."""
    note = get_note(note_id)
    if not note:
        return False, "Note not found"

    app_state["notes"] = [n for n in app_state["notes"] if n["id"] != note_id]
    return True, "Note deleted"

# ============ SEARCH & FILTER ============
def search_notes(query):
    """Search notes by title or content."""
    query = query.lower()
    results = []
    for note in app_state["notes"]:
        if query in note["title"].lower() or query in note["content"].lower():
            results.append(note)
    return results

def filter_by_category(category):
    """Filter notes by category."""
    return [n for n in app_state["notes"] if n["category"] == category]

# ============ DISPLAY ============
def display_note(note, detailed=False):
    """Display a single note."""
    print("-" * 40)
    print("ID:", note["id"], "| Category:", note["category"])
    print("Title:", note["title"])
    if detailed:
        print("Content:", note["content"] if note["content"] else "(empty)")
        print("Created:", note["created_at"])
    print("-" * 40)

def display_notes(notes, title="Notes"):
    """Display a list of notes."""
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)

    if not notes:
        print("No notes found.")
    else:
        for note in notes:
            print("[" + str(note["id"]) + "] " + note["title"] + " (" + note["category"] + ")")

    print("=" * 40)

def show_menu():
    """Display main menu."""
    print("\n" + "=" * 40)
    print("  📝 " + APP_NAME)
    print("=" * 40)
    print("  1. Add Note")
    print("  2. List All Notes")
    print("  3. View Note")
    print("  4. Update Note")
    print("  5. Delete Note")
    print("  6. Search Notes")
    print("  7. Filter by Category")
    print("  0. Exit")
    print("=" * 40)

# ============ DEMO ============
def demo():
    """Demonstrate the note manager."""
    print("=== Note Manager Demo ===\n")

    # Create notes
    print("Creating notes...")
    create_note("Python Tips", "Remember to use list comprehensions!", "work")
    create_note("Shopping List", "Milk, eggs, bread", "personal")
    create_note("App Idea", "Build a habit tracker app", "ideas")
    create_note("Meeting Notes", "Discussed project timeline", "work")

    # List all notes
    display_notes(get_all_notes(), "All Notes")

    # View a single note
    print("\nViewing note #1:")
    note = get_note(1)
    if note:
        display_note(note, detailed=True)

    # Update a note
    print("\nUpdating note #2...")
    success, message = update_note(2, content="Milk, eggs, bread, butter, cheese")
    print(message)
    display_note(get_note(2), detailed=True)

    # Search
    print("\nSearching for 'python':")
    results = search_notes("python")
    display_notes(results, "Search Results")

    # Filter by category
    print("\nFiltering by 'work':")
    work_notes = filter_by_category("work")
    display_notes(work_notes, "Work Notes")

    # Delete a note
    print("\nDeleting note #3...")
    success, message = delete_note(3)
    print(message)

    # Final list
    display_notes(get_all_notes(), "Remaining Notes")

    print("\n=== Demo Complete ===")
    print("Ready to build your own capstone!")

# Run demo
demo()
```

### Your Task

The code above is a complete working example. Now:

1. **Study the structure** - Notice how it's organized
2. **Trace the flow** - Follow how data moves through functions
3. **Identify patterns** - See the validation, CRUD, and display separation
4. **Plan your capstone** - Use this as a template

### Extension Challenges

Try extending this code:

1. Add a "priority" field to notes
2. Add a "sort by date" feature
3. Add statistics (count by category)
4. Add a "favorite" feature

:::hint Key Patterns
- State is centralized in `app_state`
- CRUD functions return (result, error) tuples
- Validation happens early in functions
- Display is separate from logic
:::

:::hint For Your Capstone
- Copy this structure
- Replace "note" with your entity
- Adjust fields and categories
- Add your specific features
:::

:::answer Reveal full solution
```python
# =============================================
# NOTE MANAGER - Mini CRUD Application
# =============================================

# ============ IMPORTS ============
from datetime import datetime

# ============ CONSTANTS ============
APP_NAME = "Note Manager"
CATEGORIES = ["personal", "work", "ideas", "other"]

# ============ STATE ============
app_state = {
    "notes": [],
    "next_id": 1
}

# ============ DATA FUNCTIONS ============
def create_note(title, content, category="other"):
    """Create a new note."""
    # Validate
    if not title or not title.strip():
        return None, "Title is required"
    if category not in CATEGORIES:
        return None, "Invalid category"

    # Create note
    note = {
        "id": app_state["next_id"],
        "title": title.strip(),
        "content": content.strip() if content else "",
        "category": category,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    app_state["notes"].append(note)
    app_state["next_id"] += 1
    return note, None

def get_all_notes():
    """Return all notes."""
    return app_state["notes"]

def get_note(note_id):
    """Get a single note by ID."""
    for note in app_state["notes"]:
        if note["id"] == note_id:
            return note
    return None

def update_note(note_id, title=None, content=None, category=None):
    """Update a note's fields."""
    note = get_note(note_id)
    if not note:
        return False, "Note not found"

    if title is not None:
        if not title.strip():
            return False, "Title cannot be empty"
        note["title"] = title.strip()

    if content is not None:
        note["content"] = content.strip()

    if category is not None:
        if category not in CATEGORIES:
            return False, "Invalid category"
        note["category"] = category

    return True, "Note updated"

def delete_note(note_id):
    """Delete a note by ID."""
    note = get_note(note_id)
    if not note:
        return False, "Note not found"

    app_state["notes"] = [n for n in app_state["notes"] if n["id"] != note_id]
    return True, "Note deleted"

# ============ SEARCH & FILTER ============
def search_notes(query):
    """Search notes by title or content."""
    query = query.lower()
    results = []
    for note in app_state["notes"]:
        if query in note["title"].lower() or query in note["content"].lower():
            results.append(note)
    return results

def filter_by_category(category):
    """Filter notes by category."""
    return [n for n in app_state["notes"] if n["category"] == category]

# ============ DISPLAY ============
def display_note(note, detailed=False):
    """Display a single note."""
    print("-" * 40)
    print("ID:", note["id"], "| Category:", note["category"])
    print("Title:", note["title"])
    if detailed:
        print("Content:", note["content"] if note["content"] else "(empty)")
        print("Created:", note["created_at"])
    print("-" * 40)

def display_notes(notes, title="Notes"):
    """Display a list of notes."""
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)

    if not notes:
        print("No notes found.")
    else:
        for note in notes:
            print("[" + str(note["id"]) + "] " + note["title"] + " (" + note["category"] + ")")

    print("=" * 40)

def show_menu():
    """Display main menu."""
    print("\n" + "=" * 40)
    print("  📝 " + APP_NAME)
    print("=" * 40)
    print("  1. Add Note")
    print("  2. List All Notes")
    print("  3. View Note")
    print("  4. Update Note")
    print("  5. Delete Note")
    print("  6. Search Notes")
    print("  7. Filter by Category")
    print("  0. Exit")
    print("=" * 40)

# ============ DEMO ============
def demo():
    """Demonstrate the note manager."""
    print("=== Note Manager Demo ===\n")

    # Create notes
    print("Creating notes...")
    create_note("Python Tips", "Remember to use list comprehensions!", "work")
    create_note("Shopping List", "Milk, eggs, bread", "personal")
    create_note("App Idea", "Build a habit tracker app", "ideas")
    create_note("Meeting Notes", "Discussed project timeline", "work")

    # List all notes
    display_notes(get_all_notes(), "All Notes")

    # View a single note
    print("\nViewing note #1:")
    note = get_note(1)
    if note:
        display_note(note, detailed=True)

    # Update a note
    print("\nUpdating note #2...")
    success, message = update_note(2, content="Milk, eggs, bread, butter, cheese")
    print(message)
    display_note(get_note(2), detailed=True)

    # Search
    print("\nSearching for 'python':")
    results = search_notes("python")
    display_notes(results, "Search Results")

    # Filter by category
    print("\nFiltering by 'work':")
    work_notes = filter_by_category("work")
    display_notes(work_notes, "Work Notes")

    # Delete a note
    print("\nDeleting note #3...")
    success, message = delete_note(3)
    print(message)

    # Final list
    display_notes(get_all_notes(), "Remaining Notes")

    print("\n=== Demo Complete ===")
    print("Ready to build your own capstone!")

# Run demo
demo()
```
:::

