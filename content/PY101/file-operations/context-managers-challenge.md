---
title: "Challenge: Build a File-Based Note System"
slug: context-managers-challenge
description: "Create a note-taking system using context managers"
course_id: PY101
module: file-operations
module_order: 6
topic: context-managers
topic_order: 4
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - context-managers-practice
skills:
  - file-io
  - files
  - context-managers
outcomes:
  - "Build complete file-based applications"
  - "Use context managers throughout"
  - "Handle file operations safely"
capstone_relevance: "File-based data storage is common in applications"
---

## Challenge: Note Manager

Build a simple note-taking system that stores notes in files. Since we can't use actual files in the browser, we'll simulate the file system with a dictionary.

### Requirements

1. **`save_note(notes_db, title, content)`** - Save a note
   - Store content with title as key
   - Include creation timestamp
   - Return success message

2. **`load_note(notes_db, title)`** - Load a specific note
   - Return the note content
   - Raise KeyError if note doesn't exist

3. **`list_notes(notes_db)`** - List all note titles

4. **`delete_note(notes_db, title)`** - Delete a note
   - Raise KeyError if note doesn't exist

5. **`search_notes(notes_db, keyword)`** - Search notes for keyword
   - Return list of titles containing the keyword in content

6. **`export_all_notes(notes_db)`** - Export all notes as formatted text

### Your Solution

```python live
def get_timestamp():
    """Get current timestamp (simulated)."""
    return "2024-01-15 10:30:00"

def save_note(notes_db, title, content):
    """Save a note with timestamp."""
    # Simulate: with open(f"notes/{title}.txt", "w") as f: f.write(...)
    # Your code here
    pass

def load_note(notes_db, title):
    """Load a note by title."""
    # Simulate: with open(f"notes/{title}.txt", "r") as f: return f.read()
    # Your code here
    pass

def list_notes(notes_db):
    """List all note titles."""
    # Simulate: listing files in notes/ directory
    # Your code here
    pass

def delete_note(notes_db, title):
    """Delete a note."""
    # Simulate: os.remove(f"notes/{title}.txt")
    # Your code here
    pass

def search_notes(notes_db, keyword):
    """Search notes for keyword."""
    # Simulate: reading each file and checking content
    # Your code here
    pass

def export_all_notes(notes_db):
    """Export all notes as formatted text."""
    # Simulate: reading all files and formatting
    # Your code here
    pass


# Test the Note Manager
notes = {}  # Simulated file system

print("=== Note Manager Test ===\n")

# Save some notes
print("Saving notes...")
save_note(notes, "shopping", "Milk, Eggs, Bread, Butter")
save_note(notes, "todo", "Finish Python course\nBuild capstone project")
save_note(notes, "ideas", "Build a weather app\nCreate a game with Python")
print()

# List notes
print("All notes:", list_notes(notes))
print()

# Load a note
print("Loading 'shopping':")
print(load_note(notes, "shopping"))
print()

# Search notes
print("Searching for 'Python':")
results = search_notes(notes, "Python")
print("Found in:", results)
print()

# Delete a note
print("Deleting 'ideas'...")
delete_note(notes, "ideas")
print("Remaining notes:", list_notes(notes))
print()

# Try loading deleted note
print("Trying to load deleted note:")
try:
    load_note(notes, "ideas")
except KeyError as e:
    print("Error:", e)
print()

# Export all notes
print("=== Exported Notes ===")
print(export_all_notes(notes))
```

:::expected_output
=== Note Manager Test ===

Saving notes...

All notes: ['shopping', 'todo', 'ideas']

Loading 'shopping':
[2024-01-15 10:30:00]
Milk, Eggs, Bread, Butter

Searching for 'Python':
Found in: ['todo', 'ideas']

Deleting 'ideas'...
Remaining notes: ['shopping', 'todo']

Trying to load deleted note:
Error: 'Note not found: ideas'

=== Exported Notes ===
=== shopping ===
[2024-01-15 10:30:00]
Milk, Eggs, Bread, Butter

=== todo ===
[2024-01-15 10:30:00]
Finish Python course
Build capstone project
:::

### Expected Output

```
=== Note Manager Test ===

Saving notes...

All notes: ['shopping', 'todo', 'ideas']

Loading 'shopping':
[2024-01-15 10:30:00]
Milk, Eggs, Bread, Butter

Searching for 'Python':
Found in: ['todo', 'ideas']

Deleting 'ideas'...
Remaining notes: ['shopping', 'todo']

Trying to load deleted note:
Error: 'Note not found: ideas'

=== Exported Notes ===
=== shopping ===
[2024-01-15 10:30:00]
Milk, Eggs, Bread, Butter

=== todo ===
[2024-01-15 10:30:00]
Finish Python course
Build capstone project
```

:::hint Save Note
Store in dictionary as `notes_db[title] = {"content": content, "timestamp": timestamp}`.
:::

:::hint Load Note
Check if title exists, raise KeyError if not. Format output with timestamp and content.
:::

:::hint Search Notes
Loop through all notes, check if keyword is in content (case-insensitive is nice!).
:::

:::hint Export Notes
Loop through all notes and format each with title header and content.
:::

:::answer Reveal full solution
```python
def get_timestamp():
    """Get current timestamp (simulated)."""
    return "2024-01-15 10:30:00"

def save_note(notes_db, title, content):
    """Save a note with timestamp."""
    notes_db[title] = {
        "content": content,
        "timestamp": get_timestamp()
    }

def load_note(notes_db, title):
    """Load a note by title."""
    if title not in notes_db:
        raise KeyError("Note not found: " + title)
    note = notes_db[title]
    return "[" + note["timestamp"] + "]\n" + note["content"]

def list_notes(notes_db):
    """List all note titles."""
    return list(notes_db.keys())

def delete_note(notes_db, title):
    """Delete a note."""
    if title not in notes_db:
        raise KeyError("Note not found: " + title)
    del notes_db[title]

def search_notes(notes_db, keyword):
    """Search notes for keyword."""
    results = []
    keyword_lower = keyword.lower()
    for title in notes_db:
        if keyword_lower in notes_db[title]["content"].lower():
            results.append(title)
    return results

def export_all_notes(notes_db):
    """Export all notes as formatted text."""
    lines = []
    for title in notes_db:
        note = notes_db[title]
        lines.append("=== " + title + " ===")
        lines.append("[" + note["timestamp"] + "]")
        lines.append(note["content"])
        lines.append("")
    return "\n".join(lines).rstrip()


# Test the Note Manager
notes = {}  # Simulated file system

print("=== Note Manager Test ===\n")

# Save some notes
print("Saving notes...")
save_note(notes, "shopping", "Milk, Eggs, Bread, Butter")
save_note(notes, "todo", "Finish Python course\nBuild capstone project")
save_note(notes, "ideas", "Build a weather app\nCreate a game with Python")
print()

# List notes
print("All notes:", list_notes(notes))
print()

# Load a note
print("Loading 'shopping':")
print(load_note(notes, "shopping"))
print()

# Search notes
print("Searching for 'Python':")
results = search_notes(notes, "Python")
print("Found in:", results)
print()

# Delete a note
print("Deleting 'ideas'...")
delete_note(notes, "ideas")
print("Remaining notes:", list_notes(notes))
print()

# Try loading deleted note
print("Trying to load deleted note:")
try:
    load_note(notes, "ideas")
except KeyError as e:
    print("Error:", e)
print()

# Export all notes
print("=== Exported Notes ===")
print(export_all_notes(notes))
```
:::

