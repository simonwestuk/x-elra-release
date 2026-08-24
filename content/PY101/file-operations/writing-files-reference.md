---
title: "Quick Reference: Writing Files"
slug: writing-files-reference
description: "Quick reference for file writing operations"
course_id: PY101
module: file-operations
module_order: 6
topic: writing-files
topic_order: 2
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - file-io
  - files
outcomes:
  - "Quick lookup for file writing syntax"
  - "Review write modes and methods"
capstone_relevance: "File writing reference for your project"
---

## Quick Reference: Writing Files

### Opening for Writing

```python
# Write (creates/overwrites)
file = open("output.txt", "w")

# Append (adds to end)
file = open("output.txt", "a")

# Don't forget to close!
file.close()
```

### Write Modes

| Mode | Creates? | Overwrites? | Position |
|------|----------|-------------|----------|
| `"w"` | Yes | Yes | Start |
| `"a"` | Yes | No | End |
| `"x"` | Yes (error if exists) | N/A | Start |

### Writing Methods

```python
# Write a string
file.write("Hello, World!")

# Write multiple strings
file.writelines(["Line 1\n", "Line 2\n"])
```

### Remember: Add Newlines!

```python
# write() doesn't add newlines
file.write("Line 1\n")  # Include \n
file.write("Line 2\n")

# Or use join
lines = ["Line 1", "Line 2", "Line 3"]
file.write("\n".join(lines) + "\n")
```

### With Statement (Recommended)

```python
with open("output.txt", "w") as file:
    file.write("Hello!")
# File automatically closed
```

### Common Patterns

```python
# Write list of items
with open("items.txt", "w") as f:
    for item in items:
        f.write(item + "\n")

# Write dictionary as config
with open("config.txt", "w") as f:
    for key, value in config.items():
        f.write(key + "=" + value + "\n")

# Write numbers
with open("numbers.txt", "w") as f:
    for num in numbers:
        f.write(str(num) + "\n")

# Write CSV-style data
with open("data.csv", "w") as f:
    f.write("name,value\n")  # Header
    for name, value in data:
        f.write(name + "," + str(value) + "\n")
```

### Append Example

```python
# Log file (append new entries)
with open("log.txt", "a") as f:
    f.write("[INFO] New event\n")
```

### Error Handling

```python
try:
    with open("output.txt", "w") as f:
        f.write("Data")
except PermissionError:
    print("Cannot write to file!")
except IOError as e:
    print("I/O error:", e)
```

### Convert to Strings

```python
# Numbers
f.write(str(42) + "\n")

# Formatted numbers
f.write(str(round(3.14159, 2)) + "\n")

# Multiple values
f.write(name + "," + str(age) + "\n")
```

### Flushing Output

```python
# Force write to disk immediately
file.write("Important data")
file.flush()  # Ensure it's written
```

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `PermissionError` | No write access | Check permissions |
| `FileExistsError` | File exists (mode "x") | Use "w" or choose new name |
| `IsADirectoryError` | Path is a directory | Use file path |
| `TypeError` | Writing non-string | Convert with `str()` |

### See Also

- [Reading Files](reading-files-lesson.html) - Reading data
- [File Modes](file-modes-lesson.html) - All mode options
- [Context Managers](context-managers-lesson.html) - Safe file handling

