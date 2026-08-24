---
title: "Quick Reference: Context Managers"
slug: context-managers-reference
description: "Quick reference for the with statement and context managers"
course_id: PY101
module: file-operations
module_order: 6
topic: context-managers
topic_order: 4
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - file-io
  - files
  - context-managers
outcomes:
  - "Quick lookup for with statement syntax"
  - "Review context manager patterns"
capstone_relevance: "Context manager reference for file handling"
---

## Quick Reference: Context Managers

### Basic Syntax

```python
with open(filename, mode) as file:
    # work with file
# file automatically closed
```

### Reading Files

```python
# Read entire file
with open("file.txt", "r") as f:
    content = f.read()

# Read lines as list
with open("file.txt", "r") as f:
    lines = f.readlines()

# Read line by line
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())
```

### Writing Files

```python
# Write (creates/overwrites)
with open("file.txt", "w") as f:
    f.write("content")

# Append
with open("file.txt", "a") as f:
    f.write("more content\n")

# Write lines
with open("file.txt", "w") as f:
    f.writelines(["line1\n", "line2\n"])
```

### Multiple Files

```python
# Two files at once
with open("in.txt", "r") as src, \
     open("out.txt", "w") as dst:
    dst.write(src.read())

# Alternative (Python 3.10+)
with (
    open("in.txt", "r") as src,
    open("out.txt", "w") as dst
):
    dst.write(src.read())
```

### with vs Manual

```python
# DON'T do this
file = open("file.txt")
data = file.read()
file.close()  # Easy to forget!

# DO this instead
with open("file.txt") as file:
    data = file.read()
# Automatically closed!
```

### Error Safety

```python
# with handles errors safely
with open("file.txt") as f:
    data = f.read()
    risky_operation(data)  # Even if this fails
# File still gets closed!

# Equivalent to:
f = open("file.txt")
try:
    data = f.read()
    risky_operation(data)
finally:
    f.close()  # Always runs
```

### Common Patterns

```python
# Read, process, write
with open("input.txt") as f:
    data = f.read()

processed = transform(data)

with open("output.txt", "w") as f:
    f.write(processed)

# Copy file
with open("src.txt") as src, open("dst.txt", "w") as dst:
    for line in src:
        dst.write(line)

# Append log entry
with open("log.txt", "a") as log:
    log.write(f"[{timestamp}] {message}\n")

# Read JSON (concept)
import json
with open("data.json") as f:
    data = json.load(f)
```

### Benefits

| Feature | with | Manual |
|---------|------|--------|
| Auto-close | ✓ | Must remember |
| Error-safe | ✓ | Need try/finally |
| Clean code | ✓ | More boilerplate |
| Resource leak | No | Possible |

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError` | File doesn't exist | Check path, use try/except |
| `PermissionError` | No access | Check permissions |
| Forgetting `as` | Syntax error | `with open(...) as f:` |

### See Also

- [Reading Files](reading-files-lesson.html) - File reading basics
- [Writing Files](writing-files-lesson.html) - File writing basics
- [File Modes](file-modes-lesson.html) - Mode options

