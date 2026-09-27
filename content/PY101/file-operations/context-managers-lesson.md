---
title: "Context Managers and the with Statement"
slug: context-managers-lesson
description: "Learn to use context managers for safe file handling"
course_id: PY101
module: file-operations
module_order: 6
topic: context-managers
topic_order: 4
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - reading-files-lesson
  - writing-files-lesson
skills:
  - file-io
  - files
  - context-managers
outcomes:
  - "Use the with statement for file handling"
  - "Understand automatic resource cleanup"
  - "Write safer file handling code"
capstone_relevance: "Context managers ensure resources are properly released"
---

## Introduction

The **with statement** provides a clean way to handle files that automatically closes them when you're done. This prevents resource leaks and makes your code safer and cleaner.

## The Problem with Manual File Handling

```python live
# The old way - easy to forget to close!
def risky_read(filename):
    # Simulating file operations
    print("Opening file...")
    # file = open(filename)
    print("Reading data...")
    # data = file.read()

    # What if an error happens here?
    # The file might never get closed!

    print("Closing file...")
    # file.close()

risky_read("data.txt")
print("\nProblem: If an error occurs, file.close() never runs!")
```

:::expected_output
Opening file...
Reading data...
Closing file...

Problem: If an error occurs, file.close() never runs!
:::

## The with Statement Solution

```python live
# The better way - with statement
def safe_read():
    print("Using 'with' statement:")
    print("with open('data.txt') as file:")
    print("    data = file.read()")
    print("# File automatically closed here!")
    print()
    print("Benefits:")
    print("- File closes automatically")
    print("- Even if errors occur!")
    print("- Cleaner code")

safe_read()
```

:::expected_output
Using 'with' statement:
with open('data.txt') as file:
    data = file.read()
# File automatically closed here!

Benefits:
- File closes automatically
- Even if errors occur!
- Cleaner code
:::

## Basic Syntax

```python
# General pattern
with open(filename, mode) as variable_name:
    # work with the file
    # ...
# file is automatically closed here
```

## Reading with Context Manager

```python live
# Simulating with statement for reading
def demo_read_with():
    sample_content = "Line 1\nLine 2\nLine 3"

    print("Code would be:")
    print('with open("data.txt", "r") as file:')
    print('    content = file.read()')
    print('    print(content)')
    print()
    print("Output:")
    print(sample_content)
    print()
    print("# File automatically closed!")

demo_read_with()
```

:::expected_output
Code would be:
with open("data.txt", "r") as file:
    content = file.read()
    print(content)

Output:
Line 1
Line 2
Line 3

# File automatically closed!
:::

## Writing with Context Manager

```python live
def demo_write_with():
    print("Code would be:")
    print('with open("output.txt", "w") as file:')
    print('    file.write("Hello, World!")')
    print('    file.write("More content")')
    print()
    print("# File automatically closed and saved!")

demo_write_with()
```

:::expected_output
Code would be:
with open("output.txt", "w") as file:
    file.write("Hello, World!")
    file.write("More content")

# File automatically closed and saved!
:::

## Automatic Cleanup on Errors

The file closes even if an error occurs:

```python live
def demo_error_handling():
    print("Code:")
    print('try:')
    print('    with open("data.txt", "r") as file:')
    print('        data = file.read()')
    print('        result = int(data)  # What if this fails?')
    print('except ValueError:')
    print('    print("Error converting data")')
    print()
    print("# Even with error, file is closed!")
    print("# The 'with' statement guarantees cleanup.")

demo_error_handling()
```

:::expected_output
Code:
try:
    with open("data.txt", "r") as file:
        data = file.read()
        result = int(data)  # What if this fails?
except ValueError:
    print("Error converting data")

# Even with error, file is closed!
# The 'with' statement guarantees cleanup.
:::

## Multiple Files

You can open multiple files at once:

```python live
def demo_multiple_files():
    print("Opening two files at once:")
    print()
    print('with open("input.txt", "r") as infile, \\')
    print('     open("output.txt", "w") as outfile:')
    print('    data = infile.read()')
    print('    outfile.write(data.upper())')
    print()
    print("# Both files automatically closed!")

demo_multiple_files()
```

:::expected_output
Opening two files at once:

with open("input.txt", "r") as infile, \
     open("output.txt", "w") as outfile:
    data = infile.read()
    outfile.write(data.upper())

# Both files automatically closed!
:::

## Line-by-Line Processing

```python live
def demo_line_processing():
    sample_lines = ["Line 1: Hello", "Line 2: World", "Line 3: Python"]

    print("Processing file line by line:")
    print('with open("data.txt", "r") as file:')
    print('    for line in file:')
    print('        print(line.strip())')
    print()
    print("Output:")
    for line in sample_lines:
        print(line)

demo_line_processing()
```

:::expected_output
Processing file line by line:
with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())

Output:
Line 1: Hello
Line 2: World
Line 3: Python
:::

## with vs try-finally

The `with` statement replaces this pattern:

```python live
def comparison():
    print("OLD WAY (try-finally):")
    print("file = open('data.txt', 'r')")
    print("try:")
    print("    data = file.read()")
    print("finally:")
    print("    file.close()  # Always closes")
    print()
    print("NEW WAY (with):")
    print("with open('data.txt', 'r') as file:")
    print("    data = file.read()")
    print("# Automatically closes!")
    print()
    print("The 'with' statement is cleaner and safer!")

comparison()
```

:::expected_output
OLD WAY (try-finally):
file = open('data.txt', 'r')
try:
    data = file.read()
finally:
    file.close()  # Always closes

NEW WAY (with):
with open('data.txt', 'r') as file:
    data = file.read()
# Automatically closes!

The 'with' statement is cleaner and safer!
:::

## Common Patterns

```python live
def show_patterns():
    print("=== Common with Statement Patterns ===\n")

    print("1. Read entire file:")
    print('with open("file.txt") as f:')
    print('    content = f.read()')
    print()

    print("2. Read lines into list:")
    print('with open("file.txt") as f:')
    print('    lines = f.readlines()')
    print()

    print("3. Process line by line:")
    print('with open("file.txt") as f:')
    print('    for line in f:')
    print('        process(line)')
    print()

    print("4. Write data:")
    print('with open("file.txt", "w") as f:')
    print('    f.write("data")')
    print()

    print("5. Append data:")
    print('with open("log.txt", "a") as f:')
    print('    f.write("new entry\\n")')

show_patterns()
```

:::expected_output
=== Common with Statement Patterns ===

1. Read entire file:
with open("file.txt") as f:
    content = f.read()

2. Read lines into list:
with open("file.txt") as f:
    lines = f.readlines()

3. Process line by line:
with open("file.txt") as f:
    for line in f:
        process(line)

4. Write data:
with open("file.txt", "w") as f:
    f.write("data")

5. Append data:
with open("log.txt", "a") as f:
    f.write("new entry\n")
:::

## Key Points

- `with` automatically closes files when the block ends
- Files close even if an error occurs
- Cleaner and safer than manual open/close
- Use `with` for ALL file operations
- Can open multiple files in one `with` statement

:::hint Best Practice
Always use `with` for file operations. There's rarely a good reason to use manual `open()` and `close()` anymore.
:::

