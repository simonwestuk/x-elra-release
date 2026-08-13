---
title: "Reading Files"
slug: reading-files-lesson
description: "Learn to read data from text files in Python"
course_id: PY101
module: file-operations
module_order: 6
topic: reading-files
topic_order: 1
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - try-except-lesson
skills:
  - file-io
  - files
outcomes:
  - "Open and read text files"
  - "Read files line by line"
  - "Handle file reading errors"
capstone_relevance: "File operations enable data persistence in applications"
---

## Introduction

Files let your programs store and retrieve data that persists even after the program ends. This is essential for saving user data, configuration, and more. Let's learn how to read text files in Python.

## Opening and Reading a File

The basic pattern for reading a file:

```python
file = open("filename.txt", "r")  # "r" = read mode
content = file.read()              # Read entire file
file.close()                       # Always close the file!
print(content)
```

## The read() Method

`read()` returns the entire file as a single string:

```python
# Simulating file content for demonstration
sample_content = """Line 1: Hello
Line 2: World
Line 3: Python is fun!"""

print(sample_content)
print()
print("Length:", len(sample_content), "characters")
```

## Reading Line by Line

Use `readlines()` to get a list of lines:

```python live
# Simulating file with multiple lines
file_content = """apple
banana
cherry
date
elderberry"""

# Split into lines (like readlines() does)
lines = file_content.split("\n")

print("Number of lines:", len(lines))
for line in lines:
    print("Line:", line)
```

:::expected_output
Number of lines: 5
Line: apple
Line: banana
Line: cherry
Line: date
Line: elderberry
:::

## The readline() Method

Read one line at a time:

```python live
# Simulating reading line by line
lines = ["First line", "Second line", "Third line"]

# Like calling readline() multiple times
for i, line in enumerate(lines):
    print("Read line", i + 1 + ":", line)
```

## Iterating Over a File

The most Pythonic way to read line by line:

```python live
# In real file reading:
# for line in file:
#     print(line)

# Demonstration
sample_lines = ["Name: Alice", "Age: 25", "City: London"]

for line in sample_lines:
    print(line)
```

:::expected_output
Name: Alice
Age: 25
City: London
:::

## Processing File Data

```python live
# Simulating a data file
data_content = """Alice,95
Bob,87
Charlie,92
Diana,78
Eve,88"""

# Process each line
lines = data_content.split("\n")
for line in lines:
    parts = line.split(",")
    name = parts[0]
    score = int(parts[1])
    print(name + " scored " + str(score))
```

:::expected_output
Alice scored 95
Bob scored 87
Charlie scored 92
Diana scored 78
Eve scored 88
:::

## Handling Missing Files

Always handle the case where a file doesn't exist:

```python live
def read_file_safely(filename):
    """Read a file with error handling."""
    try:
        # In real code: file = open(filename, "r")
        # For demo, we'll simulate success/failure
        if filename == "exists.txt":
            return "File contents here"
        else:
            raise FileNotFoundError("No such file: " + filename)
    except FileNotFoundError:
        print("Error: File '" + filename + "' not found!")
        return None

# Test with existing file
result = read_file_safely("exists.txt")
print("Result:", result)

# Test with missing file
result = read_file_safely("missing.txt")
print("Result:", result)
```

:::expected_output
Result: File contents here
Error: File 'missing.txt' not found!
Result: None
:::

## Stripping Whitespace

Lines often have trailing newlines. Use `strip()` to remove them:

```python live
# Lines with whitespace
raw_lines = ["  hello  \n", "world\n", "  python  \n"]

for line in raw_lines:
    clean = line.strip()
    print("'" + clean + "'")
```

:::expected_output
'hello'
'world'
'python'
:::

## Reading Numbers from Files

```python live
# Simulating a file with numbers
number_data = """10
25
30
15
20"""

lines = number_data.split("\n")
numbers = []

for line in lines:
    number = int(line.strip())
    numbers.append(number)

print("Numbers:", numbers)
print("Sum:", sum(numbers))
print("Average:", sum(numbers) / len(numbers))
```

:::expected_output
Numbers: [10, 25, 30, 15, 20]
Sum: 100
Average: 20.0
:::

## Key Points

- Use `open(filename, "r")` to open a file for reading
- `read()` returns the entire file as one string
- `readlines()` returns a list of lines
- Always close files when done (or use `with` - next lesson!)
- Handle `FileNotFoundError` for missing files
- Use `strip()` to remove whitespace from lines

:::hint Remember
In the browser environment, file operations are simulated. When running Python locally, these operations work with actual files on your computer.
:::

