---
title: "File Modes"
slug: file-modes-lesson
description: "Learn the different file access modes in Python"
course_id: PY101
module: file-operations
module_order: 6
topic: file-modes
topic_order: 3
type: lesson
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - reading-files-lesson
  - writing-files-lesson
skills:
  - file-io
  - files
outcomes:
  - "Understand different file modes"
  - "Choose the correct mode for each task"
  - "Use read-write modes"
capstone_relevance: "Choosing correct file modes prevents data loss"
---

## Introduction

When you open a file in Python, you specify a **mode** that tells Python how you want to access the file. Using the wrong mode can cause errors or accidentally delete your data!

## Basic File Modes

| Mode | Name | Description |
|------|------|-------------|
| `"r"` | Read | Read only (file must exist) |
| `"w"` | Write | Write only (creates/overwrites) |
| `"a"` | Append | Write only (creates/adds to end) |
| `"x"` | Exclusive | Write only (fails if exists) |

## Read Mode ("r")

```python live
# "r" is the default mode
# file = open("data.txt", "r")  # Explicit
# file = open("data.txt")       # Same thing

# Simulating read mode behavior
def simulate_read(filename, content_exists):
    if not content_exists:
        raise FileNotFoundError("File not found: " + filename)
    return "File content here"

# Works if file exists
try:
    result = simulate_read("exists.txt", True)
    print("Read:", result)
except FileNotFoundError as e:
    print("Error:", e)

# Fails if file doesn't exist
try:
    result = simulate_read("missing.txt", False)
    print("Read:", result)
except FileNotFoundError as e:
    print("Error:", e)
```

:::expected_output
Read: File content here
Error: File not found: missing.txt
:::

## Write Mode ("w")

**Warning**: Write mode DELETES existing content!

```python live
# Simulating write mode behavior
def simulate_write_mode():
    print("Mode 'w' behavior:")
    print("- Creates file if it doesn't exist")
    print("- DELETES all content if file exists")
    print("- File is empty, ready for writing")

simulate_write_mode()

# Example of what happens
existing_content = "Important data!\nDon't delete me!"
print("\nBefore 'w' mode:")
print(existing_content)

# After opening with 'w', content is gone!
print("\nAfter opening with 'w' mode:")
print("(file is now empty)")
```

:::expected_output
Mode 'w' behavior:
- Creates file if it doesn't exist
- DELETES all content if file exists
- File is empty, ready for writing

Before 'w' mode:
Important data!
Don't delete me!

After opening with 'w' mode:
(file is now empty)
:::

## Append Mode ("a")

Safely add to a file without losing existing content:

```python live
# Simulating append mode
def simulate_append():
    content = ["Line 1\n", "Line 2\n"]  # Existing content

    print("Before append:")
    print("".join(content))

    # Append adds to the end
    content.append("New line appended!\n")

    print("After append:")
    print("".join(content))

simulate_append()
```

:::expected_output
Before append:
Line 1
Line 2

After append:
Line 1
Line 2
New line appended!
:::

## Exclusive Mode ("x")

Create a file only if it doesn't exist:

```python live
def simulate_exclusive_mode(filename, exists):
    """Simulate exclusive mode - fail if file exists."""
    if exists:
        raise FileExistsError("File already exists: " + filename)
    return "Created new file: " + filename

# New file - succeeds
try:
    result = simulate_exclusive_mode("new_file.txt", False)
    print(result)
except FileExistsError as e:
    print("Error:", e)

# Existing file - fails
try:
    result = simulate_exclusive_mode("existing.txt", True)
    print(result)
except FileExistsError as e:
    print("Error:", e)
```

:::expected_output
Created new file: new_file.txt
Error: File already exists: existing.txt
:::

## Adding Binary Mode

Add `"b"` for binary files (images, etc.):

| Mode | Description |
|------|-------------|
| `"rb"` | Read binary |
| `"wb"` | Write binary |
| `"ab"` | Append binary |

```python
# For non-text files (images, etc.)
# file = open("image.png", "rb")
```

## Read-Write Modes

Add `"+"` to enable both reading and writing:

| Mode | Can Read | Can Write | Creates | Overwrites |
|------|----------|-----------|---------|------------|
| `"r+"` | Yes | Yes | No | No |
| `"w+"` | Yes | Yes | Yes | Yes |
| `"a+"` | Yes | Yes | Yes | No |

## Choosing the Right Mode

```python live
def recommend_mode(task):
    """Recommend file mode based on task."""
    recommendations = {
        "read data": "r",
        "create new file": "w or x",
        "overwrite file": "w",
        "add to file": "a",
        "update file": "r+",
        "create and read": "w+",
        "append and read": "a+",
        "binary read": "rb",
        "binary write": "wb"
    }
    return recommendations.get(task, "Unknown task")

tasks = ["read data", "create new file", "add to file", "update file"]
for task in tasks:
    mode = recommend_mode(task)
    print(task + " -> mode: " + mode)
```

:::expected_output
read data -> mode: r
create new file -> mode: w or x
add to file -> mode: a
update file -> mode: r+
:::

## Mode Comparison

```python live
# Visual comparison of modes
print("Mode | Read | Write | Creates | Erases")
print("-----|------|-------|---------|-------")
print("r    | Yes  | No    | No      | No    ")
print("w    | No   | Yes   | Yes     | YES!  ")
print("a    | No   | Yes   | Yes     | No    ")
print("x    | No   | Yes   | Yes*    | No    ")
print("r+   | Yes  | Yes   | No      | No    ")
print("w+   | Yes  | Yes   | Yes     | YES!  ")
print("a+   | Yes  | Yes   | Yes     | No    ")
print()
print("* x mode fails if file exists")
```

:::expected_output
Mode | Read | Write | Creates | Erases
-----|------|-------|---------|-------
r    | Yes  | No    | No      | No
w    | No   | Yes   | Yes     | YES!
a    | No   | Yes   | Yes     | No
x    | No   | Yes   | Yes*    | No
r+   | Yes  | Yes   | No      | No
w+   | Yes  | Yes   | Yes     | YES!
a+   | Yes  | Yes   | Yes     | No

* x mode fails if file exists
:::

## Key Points

- `"r"` for reading existing files
- `"w"` for creating new files (WARNING: erases existing!)
- `"a"` for safely adding to files
- `"x"` for creating only if file doesn't exist
- Add `"b"` for binary files
- Add `"+"` for read-write access

:::hint Safety Tip
When in doubt, use `"a"` (append) instead of `"w"` (write). You can always delete extra content, but you can't recover deleted data!
:::

