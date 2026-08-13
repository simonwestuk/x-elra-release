---
title: "Practice: Reading Files"
slug: reading-files-practice
description: "Practice reading and processing file data"
course_id: PY101
module: file-operations
module_order: 6
topic: reading-files
topic_order: 1
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - reading-files-lesson
skills:
  - file-io
  - files
outcomes:
  - "Process file data line by line"
  - "Parse structured file data"
  - "Handle file reading errors"
capstone_relevance: "Reading files is essential for data persistence"
---

## Exercise 1: Count Lines

Given file content as a string, count the number of lines.

```python live
file_content = """Line 1
Line 2
Line 3
Line 4
Line 5"""

# Count the lines
line_count = 0
# Your code here


print("Number of lines:", line_count)  # Should be 5
```

:::expected_output
Number of lines: 5
:::

:::hint Stuck?
Split by newline: `lines = file_content.split("\n")` then count with `len(lines)`.
:::

:::answer Reveal answer
```python
file_content = """Line 1
Line 2
Line 3
Line 4
Line 5"""

# Count the lines
line_count = 0
lines = file_content.split("\n")
line_count = len(lines)

print("Number of lines:", line_count)  # Should be 5
```
:::

## Exercise 2: Find Longest Line

Find the longest line in the file content.

```python live
file_content = """Short
A medium length line
This is the longest line in the file
Another one"""

# Find the longest line
longest = ""
# Your code here


print("Longest line:", longest)
print("Length:", len(longest))
```

:::expected_output
Longest line: This is the longest line in the file
Length: 36
:::

:::hint Stuck?
Loop through lines. If current line's length > longest's length, update longest.
:::

:::answer Reveal answer
```python
file_content = """Short
A medium length line
This is the longest line in the file
Another one"""

# Find the longest line
longest = ""
for line in file_content.split("\n"):
    if len(line) > len(longest):
        longest = line

print("Longest line:", longest)
print("Length:", len(longest))
```
:::

## Exercise 3: Parse Key-Value Pairs

Parse a configuration file format (key=value).

```python live
config_content = """name=MyApp
version=1.0
debug=true
max_users=100"""

# Parse into a dictionary
config = {}
# Your code here


print(config)
# Should be: {'name': 'MyApp', 'version': '1.0', 'debug': 'true', 'max_users': '100'}
```

:::expected_output
{'name': 'MyApp', 'version': '1.0', 'debug': 'true', 'max_users': '100'}
:::

:::hint Stuck?
Split each line by "=": `parts = line.split("=")` then `config[parts[0]] = parts[1]`.
:::

:::answer Reveal answer
```python
config_content = """name=MyApp
version=1.0
debug=true
max_users=100"""

# Parse into a dictionary
config = {}
for line in config_content.split("\n"):
    parts = line.split("=")
    config[parts[0]] = parts[1]

print(config)
# Should be: {'name': 'MyApp', 'version': '1.0', 'debug': 'true', 'max_users': '100'}
```
:::

## Exercise 4: Calculate Statistics

Read numbers from file content and calculate statistics.

```python live
numbers_content = """42
17
93
28
55
71
36"""

# Calculate sum, count, average, min, and max
numbers = []
# Parse the numbers


# Calculate statistics


print("Count:", len(numbers))
print("Sum:", sum(numbers))
print("Average:", sum(numbers) / len(numbers))
print("Min:", min(numbers))
print("Max:", max(numbers))
```

:::expected_output
Count: 7
Sum: 342
Average: 48.857142857142854
Min: 17
Max: 93
:::

:::hint Stuck?
Split by newline, then convert each line to int: `numbers.append(int(line.strip()))`.
:::

:::answer Reveal answer
```python
numbers_content = """42
17
93
28
55
71
36"""

# Calculate sum, count, average, min, and max
numbers = []
# Parse the numbers
for line in numbers_content.split("\n"):
    if line.strip():
        numbers.append(int(line.strip()))

# Calculate statistics

print("Count:", len(numbers))
print("Sum:", sum(numbers))
print("Average:", sum(numbers) / len(numbers))
print("Min:", min(numbers))
print("Max:", max(numbers))
```
:::

## Exercise 5: Search File Content

Search for lines containing a specific word.

```python live
log_content = """INFO: Application started
DEBUG: Loading config
ERROR: Database connection failed
INFO: Retrying connection
ERROR: Timeout occurred
INFO: Application shutdown"""

def find_lines(content, search_term):
    """Find all lines containing the search term."""
    results = []
    # Your code here

    return results

# Find all error lines
errors = find_lines(log_content, "ERROR")
print("Found", len(errors), "errors:")
for error in errors:
    print(" -", error)
```

:::expected_output
Found 2 errors:
 - ERROR: Database connection failed
 - ERROR: Timeout occurred
:::

:::hint Stuck?
Check if `search_term in line` for each line. If true, append to results.
:::

:::answer Reveal answer
```python
log_content = """INFO: Application started
DEBUG: Loading config
ERROR: Database connection failed
INFO: Retrying connection
ERROR: Timeout occurred
INFO: Application shutdown"""

def find_lines(content, search_term):
    """Find all lines containing the search term."""
    results = []
    for line in content.split("\n"):
        if search_term in line:
            results.append(line)
    return results

# Find all error lines
errors = find_lines(log_content, "ERROR")
print("Found", len(errors), "errors:")
for error in errors:
    print(" -", error)
```
:::

