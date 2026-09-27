---
title: "Quick Reference: File Modes"
slug: file-modes-reference
description: "Quick reference for Python file modes"
course_id: PY101
module: file-operations
module_order: 6
topic: file-modes
topic_order: 3
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - file-io
  - files
outcomes:
  - "Quick lookup for file modes"
  - "Choose correct mode for task"
capstone_relevance: "File mode reference for your project"
---

## Quick Reference: File Modes

### Basic Modes

| Mode | Name | Read | Write | Creates | Erases |
|------|------|------|-------|---------|--------|
| `r` | Read | ✓ | ✗ | ✗ | ✗ |
| `w` | Write | ✗ | ✓ | ✓ | ✓ |
| `a` | Append | ✗ | ✓ | ✓ | ✗ |
| `x` | Exclusive | ✗ | ✓ | ✓* | ✗ |

*Fails if file exists

### Extended Modes

| Mode | Read | Write | Creates | Erases |
|------|------|-------|---------|--------|
| `r+` | ✓ | ✓ | ✗ | ✗ |
| `w+` | ✓ | ✓ | ✓ | ✓ |
| `a+` | ✓ | ✓ | ✓ | ✗ |

### Binary Modes

| Mode | Description |
|------|-------------|
| `rb` | Read binary |
| `wb` | Write binary |
| `ab` | Append binary |
| `rb+` | Read/write binary |

### Mode Selection Guide

| Task | Mode |
|------|------|
| Read existing file | `r` |
| Create new file | `w` or `x` |
| Overwrite file | `w` |
| Add to file | `a` |
| Read and modify | `r+` |
| Create and read | `w+` |
| Add and read | `a+` |
| Read image/binary | `rb` |
| Write image/binary | `wb` |

### Behavior Summary

```
r   - File MUST exist
w   - Creates OR ERASES
a   - Creates OR APPENDS
x   - Creates ONLY if doesn't exist

+   - Adds read capability to write modes
      OR write capability to read mode

b   - Binary mode (non-text files)
```

### Common Patterns

```python
# Read only
with open("file.txt", "r") as f:
    data = f.read()

# Write (creates/overwrites)
with open("file.txt", "w") as f:
    f.write("content")

# Append (safe add)
with open("log.txt", "a") as f:
    f.write("new entry\n")

# Create new only
try:
    with open("new.txt", "x") as f:
        f.write("content")
except FileExistsError:
    print("File already exists!")

# Read and modify
with open("file.txt", "r+") as f:
    content = f.read()
    f.seek(0)
    f.write("new " + content)
```

### Errors by Mode

| Mode | File Exists | File Missing |
|------|-------------|--------------|
| `r` | OK | FileNotFoundError |
| `w` | Overwrites! | Creates |
| `a` | Appends | Creates |
| `x` | FileExistsError | Creates |
| `r+` | OK | FileNotFoundError |

### Safety Tips

| Danger | Use Instead |
|--------|-------------|
| `w` erases content | `a` to append |
| `w` silently overwrites | `x` for new files |
| `r` fails on missing | Try/except |

### Quick Decision

```
Need to READ existing? → r
Need to WRITE new/replace? → w
Need to ADD to existing? → a
Need to CREATE only if new? → x
Need to READ and WRITE? → r+ (exists) or w+ (new)
Working with images/binary? → add 'b'
```

### See Also

- [Reading Files](reading-files-lesson.html) - Reading basics
- [Writing Files](writing-files-lesson.html) - Writing basics
- [Context Managers](context-managers-lesson.html) - Safe file handling

