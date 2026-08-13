---
title: "Practice: Context Managers"
slug: context-managers-practice
description: "Practice using context managers for file operations"
course_id: PY101
module: file-operations
module_order: 6
topic: context-managers
topic_order: 4
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - context-managers-lesson
skills:
  - file-io
  - files
  - context-managers
outcomes:
  - "Write code using with statements"
  - "Convert manual file handling to context managers"
  - "Use context managers for various file operations"
capstone_relevance: "Context managers are the standard for file handling"
---

## Exercise 1: Convert to with Statement

Rewrite this code using a `with` statement.

```python live
# Original code (manual open/close)
# file = open("data.txt", "r")
# content = file.read()
# file.close()
# print(content)

# Rewrite using 'with':
def read_with_context():
    # Write your code here
    print("Code should be:")
    print('with open("data.txt", "r") as file:')
    print('    content = file.read()')
    print('print(content)')

read_with_context()
```

:::expected_output
Code should be:
with open("data.txt", "r") as file:
    content = file.read()
print(content)
:::

:::hint Stuck?
Replace `file = open(...)` with `with open(...) as file:`, indent the body, and remove `file.close()`.
:::

:::answer Reveal answer
```python
# Rewrite using 'with':
def read_with_context():
    with open("data.txt", "r") as file:
        content = file.read()
    print(content)

# Since file operations may not work in sandbox, show the code:
print("Code should be:")
print('with open("data.txt", "r") as file:')
print('    content = file.read()')
print('print(content)')
```
:::

## Exercise 2: Safe File Writing

Complete this function using a `with` statement.

```python live
def save_list_to_file(items, filename):
    """Save a list of items to a file, one per line."""
    # Simulate the code structure
    print("Function should be:")
    print('def save_list_to_file(items, filename):')
    print('    with open(filename, "w") as file:')
    print('        for item in items:')
    print('            file.write(str(item) + "\\n")')

    # Simulate output
    print("\nSimulated file content:")
    for item in items:
        print(item)

items = ["apple", "banana", "cherry"]
save_list_to_file(items, "fruits.txt")
```

:::expected_output
Function should be:
def save_list_to_file(items, filename):
    with open(filename, "w") as file:
        for item in items:
            file.write(str(item) + "\n")

Simulated file content:
apple
banana
cherry
:::

:::hint Stuck?
Use `with open(filename, "w") as file:` then loop through items and write each with a newline.
:::

:::answer Reveal answer
```python
def save_list_to_file(items, filename):
    """Save a list of items to a file, one per line."""
    with open(filename, "w") as file:
        for item in items:
            file.write(str(item) + "\n")

    # Simulate output
    print("Simulated file content:")
    for item in items:
        print(item)

items = ["apple", "banana", "cherry"]
save_list_to_file(items, "fruits.txt")
```
:::

## Exercise 3: Reading and Processing

Write code that reads a file and counts words.

```python live
def count_words_in_file():
    """Count total words in a file."""
    # Simulated file content
    file_content = """Hello world
This is a test file
Python is fun"""

    print("Code should be:")
    print('with open("text.txt", "r") as file:')
    print('    content = file.read()')
    print('    words = content.split()')
    print('    count = len(words)')
    print('print("Word count:", count)')

    # Simulate execution
    words = file_content.split()
    count = len(words)
    print("\nResult:")
    print("Word count:", count)

count_words_in_file()
```

:::expected_output
Code should be:
with open("text.txt", "r") as file:
    content = file.read()
    words = content.split()
    count = len(words)
print("Word count:", count)

Result:
Word count: 10
:::

:::answer Reveal answer
```python
def count_words_in_file():
    """Count total words in a file."""
    with open("text.txt", "r") as file:
        content = file.read()
        words = content.split()
        count = len(words)
    print("Word count:", count)

# Simulated version that runs without file:
file_content = """Hello world
This is a test file
Python is fun"""

words = file_content.split()
count = len(words)
print("Result:")
print("Word count:", count)
```
:::

## Exercise 4: Copy File Contents

Write code to copy contents from one file to another.

```python live
def copy_file():
    """Copy contents from source to destination."""
    # Simulated source content
    source_content = "This is the source file content."

    print("Code for copying files:")
    print('with open("source.txt", "r") as source:')
    print('    content = source.read()')
    print()
    print('with open("dest.txt", "w") as dest:')
    print('    dest.write(content)')
    print()
    print("Or in one statement:")
    print('with open("source.txt", "r") as src, \\')
    print('     open("dest.txt", "w") as dst:')
    print('    dst.write(src.read())')

copy_file()
```

:::expected_output
Code for copying files:
with open("source.txt", "r") as source:
    content = source.read()

with open("dest.txt", "w") as dest:
    dest.write(content)

Or in one statement:
with open("source.txt", "r") as src, \
     open("dest.txt", "w") as dst:
    dst.write(src.read())
:::

:::hint Stuck?
You can use two separate `with` statements, or combine them with a comma.
:::

:::answer Reveal answer
```python
def copy_file():
    """Copy contents from source to destination."""
    with open("source.txt", "r") as src, \
         open("dest.txt", "w") as dst:
        dst.write(src.read())

# Simulated source content
source_content = "This is the source file content."

print("Code for copying files:")
print('with open("source.txt", "r") as src, \\')
print('     open("dest.txt", "w") as dst:')
print('    dst.write(src.read())')
```
:::

## Exercise 5: Append Log Entry

Write a function that appends a log entry with timestamp.

```python live
def append_log(message):
    """Append a log entry with timestamp."""
    # Simulated timestamp
    timestamp = "2024-01-15 10:30:00"

    print("Code should be:")
    print('def append_log(message):')
    print('    timestamp = get_timestamp()  # Get current time')
    print('    with open("app.log", "a") as log_file:')
    print('        log_file.write(f"[{timestamp}] {message}\\n")')
    print()

    # Simulate log entries
    print("Simulated log file after multiple calls:")
    entries = [
        "[2024-01-15 10:30:00] Application started",
        "[2024-01-15 10:30:05] User logged in",
        "[2024-01-15 10:31:00] Data processed"
    ]
    for entry in entries:
        print(entry)

append_log("Application started")
```

:::expected_output
Code should be:
def append_log(message):
    timestamp = get_timestamp()  # Get current time
    with open("app.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

Simulated log file after multiple calls:
[2024-01-15 10:30:00] Application started
[2024-01-15 10:30:05] User logged in
[2024-01-15 10:31:00] Data processed
:::

:::hint Stuck?
Use mode `"a"` to append. Format the line as `"[" + timestamp + "] " + message + "\n"`.
:::

:::answer Reveal answer
```python
def append_log(message):
    """Append a log entry with timestamp."""
    timestamp = "2024-01-15 10:30:00"  # In real code, use datetime module
    with open("app.log", "a") as log_file:
        log_file.write("[" + timestamp + "] " + message + "\n")

    # Simulate log entries
    print("Simulated log file after multiple calls:")
    entries = [
        "[2024-01-15 10:30:00] Application started",
        "[2024-01-15 10:30:05] User logged in",
        "[2024-01-15 10:31:00] Data processed"
    ]
    for entry in entries:
        print(entry)

append_log("Application started")
```
:::

