---
title: "Writing Files"
slug: writing-files-lesson
description: "Learn to write data to files in Python"
course_id: PY101
module: file-operations
module_order: 6
topic: writing-files
topic_order: 2
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - reading-files-lesson
skills:
  - file-io
  - files
outcomes:
  - "Write text to files"
  - "Append to existing files"
  - "Write multiple lines"
capstone_relevance: "Saving data to files enables persistence"
---

## Introduction

Writing files lets your programs save data that persists after the program ends. This is essential for saving user data, logs, exports, and more.

## Basic File Writing

Use `open()` with mode `"w"` for writing:

```python
file = open("output.txt", "w")  # "w" = write mode
file.write("Hello, World!")
file.close()
```

**Warning**: Write mode `"w"` creates a new file or **overwrites** an existing file!

## The write() Method

```python live
# Simulating file writing
content_to_write = []

# Simulating write operations
content_to_write.append("Line 1: Hello")
content_to_write.append("Line 2: World")

# See what would be written
print("File contents would be:")
print("\n".join(content_to_write))
```

:::expected_output
File contents would be:
Line 1: Hello
Line 2: World
:::

## Writing Multiple Lines

`write()` doesn't add newlines automatically - you must add them:

```python live
# Simulating writing multiple lines
lines = []

lines.append("First line\n")   # Include newline
lines.append("Second line\n")
lines.append("Third line\n")

# Show the result
print("Written content:")
print("".join(lines))
```

:::expected_output
Written content:
First line
Second line
Third line
:::

## Using writelines()

Write a list of strings at once:

```python live
# writelines() writes all strings without adding newlines
lines = ["Line 1", "Line 2", "Line 3"]

# You need to add newlines yourself
lines_with_newlines = [line + "\n" for line in lines]

print("Written with writelines:")
print("".join(lines_with_newlines))
```

:::expected_output
Written with writelines:
Line 1
Line 2
Line 3
:::

## Appending to Files

Use mode `"a"` to add to an existing file without overwriting:

```python live
# Simulating append vs write

# Initial content (like writing first)
content = ["Entry 1\n", "Entry 2\n"]

# Appending adds to the end (mode "a")
content.append("Entry 3\n")  # Appended
content.append("Entry 4\n")  # Appended

print("After appending:")
print("".join(content))
```

:::expected_output
After appending:
Entry 1
Entry 2
Entry 3
Entry 4
:::

## Write vs Append

| Mode | Description | Creates file? | Overwrites? |
|------|-------------|---------------|-------------|
| `"w"` | Write | Yes | Yes |
| `"a"` | Append | Yes | No |

## Practical Example: Save Data

```python live
def save_scores(scores):
    """Simulate saving scores to a file."""
    output = []
    for name, score in scores.items():
        line = name + "," + str(score) + "\n"
        output.append(line)
    return "".join(output)

scores = {
    "Alice": 95,
    "Bob": 87,
    "Charlie": 92
}

file_content = save_scores(scores)
print("File would contain:")
print(file_content)
```

:::expected_output
File would contain:
Alice,95
Bob,87
Charlie,92
:::

## Writing Numbers

Convert numbers to strings before writing:

```python live
def save_numbers(numbers):
    """Simulate saving numbers to a file."""
    lines = []
    for num in numbers:
        lines.append(str(num) + "\n")
    return "".join(lines)

data = [42, 17, 93, 28, 55]
output = save_numbers(data)
print("Numbers file:")
print(output)
```

:::expected_output
Numbers file:
42
17
93
28
55
:::

## Creating Log Files

```python live
def log_message(logs, level, message):
    """Add a log entry."""
    # In real code, you'd get actual time
    timestamp = "2024-01-15 10:30:00"
    entry = "[" + timestamp + "] [" + level + "] " + message + "\n"
    logs.append(entry)

# Simulate logging
log_entries = []
log_message(log_entries, "INFO", "Application started")
log_message(log_entries, "DEBUG", "Loading config")
log_message(log_entries, "INFO", "Ready")

print("Log file content:")
print("".join(log_entries))
```

:::expected_output
Log file content:
[2024-01-15 10:30:00] [INFO] Application started
[2024-01-15 10:30:00] [DEBUG] Loading config
[2024-01-15 10:30:00] [INFO] Ready
:::

## Error Handling When Writing

```python live
def safe_write(filename, content):
    """Write with error handling."""
    try:
        # In real code: file = open(filename, "w")
        # Simulating potential errors
        if "/" in filename or "\\" in filename:
            raise PermissionError("Cannot write to path")
        print("Successfully wrote to " + filename)
        print("Content:", content)
        return True
    except PermissionError as e:
        print("Error: Could not write file -", e)
        return False

safe_write("valid.txt", "Hello!")
safe_write("/root/forbidden.txt", "Can't write here")
```

:::expected_output
Successfully wrote to valid.txt
Content: Hello!
Error: Could not write file - Cannot write to path
:::

## Key Points

- Use `"w"` mode to write (creates/overwrites)
- Use `"a"` mode to append (adds to end)
- `write()` doesn't add newlines - add `\n` yourself
- `writelines()` writes a list of strings
- Always close files when done
- Convert numbers to strings with `str()` before writing

:::hint Remember
Write mode `"w"` will DELETE existing file contents! Use `"a"` (append) to add to a file without losing existing data.
:::

