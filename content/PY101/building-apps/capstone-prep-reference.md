---
title: "Quick Reference: Capstone Preparation"
slug: capstone-prep-reference
description: "Quick reference for building your capstone application"
course_id: PY101
module: building-apps
module_order: 7
topic: capstone-prep
topic_order: 6
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - project-planning
  - application-design
outcomes:
  - "Quick reference for capstone planning"
  - "Review CRUD application patterns"
capstone_relevance: "Reference while building your capstone"
---

## Quick Reference: Capstone Prep

### CRUD Operations

| Operation | Purpose | Function Pattern |
|-----------|---------|------------------|
| **C**reate | Add new | `create_item(data)` |
| **R**ead | View | `get_item(id)`, `get_all()` |
| **U**pdate | Modify | `update_item(id, data)` |
| **D**elete | Remove | `delete_item(id)` |

### Application Structure

```python
# ============ CONSTANTS ============
APP_NAME = "My App"

# ============ STATE ============
app_state = {
    "items": [],
    "next_id": 1
}

# ============ CRUD FUNCTIONS ============
def create_item(data): pass
def get_all_items(): pass
def get_item(item_id): pass
def update_item(item_id, data): pass
def delete_item(item_id): pass

# ============ VALIDATION ============
def validate_item(data): pass

# ============ DISPLAY ============
def show_menu(): pass
def display_item(item): pass

# ============ MAIN ============
def main():
    while True:
        show_menu()
        # Handle user choice

if __name__ == "__main__":
    main()
```

### Entity Template

```python
entity = {
    "id": 1,              # Auto-generated
    "name": "required",   # Main field
    "field2": "value",    # Additional data
    "status": "active",   # State tracking
    "created_at": "date"  # Metadata
}
```

### CRUD Function Templates

```python
# CREATE
def create_item(name, **fields):
    item = {"id": next_id(), "name": name, **fields}
    state["items"].append(item)
    return item

# READ ALL
def get_all_items():
    return state["items"]

# READ ONE
def get_item(item_id):
    for item in state["items"]:
        if item["id"] == item_id:
            return item
    return None

# UPDATE
def update_item(item_id, **updates):
    item = get_item(item_id)
    if item:
        item.update(updates)
        return True
    return False

# DELETE
def delete_item(item_id):
    state["items"] = [i for i in state["items"]
                      if i["id"] != item_id]
```

### Validation Pattern

```python
def validate_item(data):
    errors = []

    if not data.get("name"):
        errors.append("Name is required")

    if data.get("value", 0) < 0:
        errors.append("Value must be positive")

    return len(errors) == 0, errors
```

### Menu Template

```python
def show_menu():
    print("=" * 30)
    print("  APP NAME")
    print("=" * 30)
    print("1. Add Item")
    print("2. View All")
    print("3. Update Item")
    print("4. Delete Item")
    print("0. Exit")
```

### Feature Checklist

**Core (Required):**
- [ ] Create items
- [ ] List all items
- [ ] View single item
- [ ] Update items
- [ ] Delete items

**Quality (Required):**
- [ ] Input validation
- [ ] Error handling
- [ ] Delete confirmation

**Extras (Optional):**
- [ ] Search
- [ ] Filter/sort
- [ ] Statistics

### Common Patterns

| Pattern | Use For |
|---------|---------|
| Guard clause | Early validation |
| (result, error) tuple | Return with status |
| List comprehension | Filtering |
| State dict | Centralized data |
| Constants | Config values |

### Development Order

1. Define data structure
2. Implement Create
3. Implement Read (all and single)
4. Implement Update
5. Implement Delete
6. Add validation
7. Build menu/UI
8. Add extras

### Quick Tips

- Start simple, add features later
- Test each function before moving on
- Keep functions small and focused
- Use meaningful variable names
- Add comments for complex logic
- Handle errors gracefully

### See Also

- [Program Structure](program-structure-lesson.html)
- [State Management](state-management-lesson.html)
- [Input Validation](input-validation-lesson.html)
- [Refactoring](refactoring-lesson.html)

