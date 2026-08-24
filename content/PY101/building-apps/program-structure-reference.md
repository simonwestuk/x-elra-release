---
title: "Quick Reference: Program Structure"
slug: program-structure-reference
description: "Quick reference for organizing Python programs"
course_id: PY101
module: building-apps
module_order: 7
topic: program-structure
topic_order: 1
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - program-design
  - code-organization
outcomes:
  - "Quick lookup for program structure"
  - "Review organization patterns"
capstone_relevance: "Structure reference for your project"
---

## Quick Reference: Program Structure

### Standard Layout

```python
# 1. IMPORTS
import module_name

# 2. CONSTANTS
MAX_SIZE = 100
APP_NAME = "My App"

# 3. HELPER FUNCTIONS
def utility_function():
    pass

# 4. MAIN FUNCTIONS
def core_feature():
    pass

# 5. ENTRY POINT
def main():
    core_feature()

# 6. RUN GUARD
if __name__ == "__main__":
    main()
```

### Section Comments

```python
# ============ CONSTANTS ============
# ============ DATA LAYER ============
# ============ BUSINESS LOGIC ============
# ============ PRESENTATION ============
# ============ MAIN ============
```

### Separation of Concerns

| Layer | Purpose | Example |
|-------|---------|---------|
| Data | Store/retrieve | `get_user()`, `save_item()` |
| Logic | Process/validate | `calculate_total()`, `is_valid()` |
| Presentation | Display | `show_menu()`, `print_report()` |

### The main() Pattern

```python
def main():
    """Program entry point."""
    setup()
    run()
    cleanup()

if __name__ == "__main__":
    main()
```

### Constants

```python
# At top of file - easy to find
APP_NAME = "My Application"
VERSION = "1.0"
MAX_ITEMS = 100
DEFAULT_VALUE = 0
```

### Function Grouping

```python
# --- User Functions ---
def create_user(): pass
def get_user(): pass
def delete_user(): pass

# --- Item Functions ---
def create_item(): pass
def get_item(): pass
def delete_item(): pass
```

### Common Patterns

```python
# Initialize → Process → Cleanup
def main():
    config = initialize()
    try:
        process(config)
    finally:
        cleanup()

# Setup → Main Loop → Exit
def main():
    setup()
    while running:
        handle_input()
        update()
        display()
    shutdown()
```

### What Goes Where

| Element | Location |
|---------|----------|
| Imports | Top of file |
| Constants | After imports |
| Classes | After constants |
| Functions | Grouped by purpose |
| main() | Near bottom |
| if __name__ | Very bottom |

### Good Practices

| Do | Don't |
|----|-------|
| Group related code | Scatter functions randomly |
| Use descriptive names | Use single letters |
| Add section comments | Leave no comments |
| Keep functions focused | Make giant functions |
| Use constants | Use magic numbers |

### Code Smell Signs

| Sign | Problem |
|------|---------|
| Function > 50 lines | Too much responsibility |
| Deep nesting | Complexity too high |
| Global variables | Tight coupling |
| Duplicated code | Missing abstraction |
| No main() | Hard to test/import |

### See Also

- [Functions](defining-functions-lesson.html) - Function basics
- [Scope](scope-lesson.html) - Variable visibility
- [Modules](modules-imports-lesson.html) - Code organization

