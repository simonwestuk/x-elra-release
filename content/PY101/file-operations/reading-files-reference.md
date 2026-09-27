---
title: "Quick Reference: Reading Files"
slug: reading-files-reference
description: "Quick reference for file reading operations"
course_id: PY101
module: file-operations
module_order: 6
topic: reading-files
topic_order: 1
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - file-io
  - files
outcomes:
  - "Quick lookup for file reading syntax"
  - "Review file reading methods"
capstone_relevance: "File reading reference for your project"
---

## Quick Reference: Reading Files

### Opening Files

```python
# Open for reading
file = open("filename.txt", "r")

# Don't forget to close!
file.close()
```

### Reading Methods

| Method | Returns | Use Case |
|--------|---------|----------|
| `read()` | Entire file as string | Small files |
| `readline()` | Next line as string | One line at a time |
| `readlines()` | List of all lines | Process all lines |

### Read Entire File

```python
file = open("data.txt", "r")
content = file.read()
file.close()
print(content)
```

### Read All Lines as List

```python
file = open("data.txt", "r")
lines = file.readlines()
file.close()

for line in lines:
    print(line.strip())
```

### Read Line by Line (Memory Efficient)

```python
file = open("data.txt", "r")
for line in file:
    print(line.strip())
file.close()
```

### With Statement (Recommended)

```python
with open("data.txt", "r") as file:
    content = file.read()
# File automatically closed
```

### Error Handling

```python
try:
    file = open("data.txt", "r")
    content = file.read()
    file.close()
except FileNotFoundError:
    print("File not found!")
```

### Common Patterns

```python
# Count lines
with open("file.txt") as f:
    line_count = len(f.readlines())

# Find lines containing text
with open("file.txt") as f:
    matches = [line for line in f if "search" in line]

# Read as list of stripped lines
with open("file.txt") as f:
    lines = [line.strip() for line in f]
```

### Processing Data Files

```python
# Numbers (one per line)
with open("numbers.txt") as f:
    numbers = [int(line.strip()) for line in f]

# CSV-like (comma separated)
with open("data.txt") as f:
    for line in f:
        parts = line.strip().split(",")
        name, value = parts[0], parts[1]

# Key=value config
config = {}
with open("config.txt") as f:
    for line in f:
        key, value = line.strip().split("=")
        config[key] = value
```

### File Object Attributes

| Attribute | Description |
|-----------|-------------|
| `file.name` | Filename |
| `file.mode` | Open mode ("r", "w", etc.) |
| `file.closed` | True if closed |

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError` | File doesn't exist | Check path, use try/except |
| `UnicodeDecodeError` | Encoding issue | Specify encoding |
| `PermissionError` | No read access | Check file permissions |

### See Also

- [Writing Files](writing-files-lesson.html) - Creating files
- [File Modes](file-modes-lesson.html) - Mode options
- [Context Managers](context-managers-lesson.html) - Safe file handling

