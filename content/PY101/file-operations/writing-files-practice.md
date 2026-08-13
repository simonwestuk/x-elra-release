---
title: "Practice: Writing Files"
slug: writing-files-practice
description: "Practice writing data to files"
course_id: PY101
module: file-operations
module_order: 6
topic: writing-files
topic_order: 2
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - writing-files-lesson
skills:
  - file-io
  - files
outcomes:
  - "Format data for file output"
  - "Create file content from data structures"
  - "Build text output programmatically"
capstone_relevance: "Writing data to files enables data persistence"
---

## Exercise 1: Write Multiple Lines

Create a function that formats a list of items for file output (one item per line).

```python live
def format_for_file(items):
    """Return a string with each item on its own line."""
    # Your code here
    pass

items = ["apple", "banana", "cherry", "date"]
output = format_for_file(items)
print("File would contain:")
print(output)
```

:::expected_output
File would contain:
apple
banana
cherry
date
:::

:::hint Stuck?
Loop through items, adding "\n" after each. Or use `"\n".join(items) + "\n"`.
:::

:::answer Reveal answer
```python
def format_for_file(items):
    """Return a string with each item on its own line."""
    return "\n".join(items) + "\n"

items = ["apple", "banana", "cherry", "date"]
output = format_for_file(items)
print("File would contain:")
print(output)
```
:::

## Exercise 2: Format Dictionary as Config

Format a dictionary as a config file (key=value format).

```python live
def dict_to_config(data):
    """Convert dictionary to config file format."""
    # Your code here
    pass

settings = {
    "username": "admin",
    "theme": "dark",
    "font_size": "14",
    "autosave": "true"
}

output = dict_to_config(settings)
print("Config file content:")
print(output)
```

:::expected_output
Config file content:
username=admin
theme=dark
font_size=14
autosave=true
:::

:::hint Stuck?
Loop through `data.items()` and format each as `key + "=" + value + "\n"`.
:::

:::answer Reveal answer
```python
def dict_to_config(data):
    """Convert dictionary to config file format."""
    result = ""
    for key, value in data.items():
        result += key + "=" + value + "\n"
    return result

settings = {
    "username": "admin",
    "theme": "dark",
    "font_size": "14",
    "autosave": "true"
}

output = dict_to_config(settings)
print("Config file content:")
print(output)
```
:::

## Exercise 3: Create a Report

Generate a formatted report from data.

```python live
def generate_report(title, data):
    """Generate a formatted report."""
    # Your code here - include title, separator, data rows
    pass

sales_data = [
    ("January", 1500),
    ("February", 1800),
    ("March", 2100),
    ("April", 1950)
]

report = generate_report("Monthly Sales", sales_data)
print(report)
```

:::expected_output
=== Monthly Sales ===
January: $1500
February: $1800
March: $2100
April: $1950
=====================
Total: $7350
:::

Expected format:
```
=== Monthly Sales ===
January: $1500
February: $1800
March: $2100
April: $1950
=====================
Total: $7350
```

:::hint Stuck?
Build the output string piece by piece. Calculate total with sum. Use string concatenation.
:::

:::answer Reveal answer
```python
def generate_report(title, data):
    """Generate a formatted report."""
    separator = "=" * (len(title) + 8)
    result = "=== " + title + " ===\n"
    total = 0
    for month, amount in data:
        result += month + ": $" + str(amount) + "\n"
        total += amount
    result += separator + "\n"
    result += "Total: $" + str(total)
    return result

sales_data = [
    ("January", 1500),
    ("February", 1800),
    ("March", 2100),
    ("April", 1950)
]

report = generate_report("Monthly Sales", sales_data)
print(report)
```
:::

## Exercise 4: Format Table Data

Format data as an aligned table.

```python live
def format_table(headers, rows):
    """Format data as a text table."""
    # Your code here
    pass

headers = ["Name", "Score", "Grade"]
rows = [
    ["Alice", "95", "A"],
    ["Bob", "87", "B"],
    ["Charlie", "72", "C"]
]

table = format_table(headers, rows)
print(table)
```

:::expected_output
Name    | Score | Grade
--------|-------|------
Alice   | 95    | A
Bob     | 87    | B
Charlie | 72    | C
:::

Expected format:
```
Name    | Score | Grade
--------|-------|------
Alice   | 95    | A
Bob     | 87    | B
Charlie | 72    | C
```

:::hint Stuck?
Use string methods like `ljust()` for padding, or calculate column widths first.
:::

:::answer Reveal answer
```python
def format_table(headers, rows):
    """Format data as a text table."""
    # Calculate column widths
    col_widths = []
    for i in range(len(headers)):
        max_width = len(headers[i])
        for row in rows:
            if len(row[i]) > max_width:
                max_width = len(row[i])
        col_widths.append(max_width)

    # Build header line
    header_line = " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
    # Build separator
    separator = "-|-".join("-" * col_widths[i] for i in range(len(headers)))
    # Build data rows
    result = header_line + "\n" + separator + "\n"
    for row in rows:
        row_line = " | ".join(row[i].ljust(col_widths[i]) for i in range(len(row)))
        result += row_line + "\n"
    return result.rstrip("\n")

headers = ["Name", "Score", "Grade"]
rows = [
    ["Alice", "95", "A"],
    ["Bob", "87", "B"],
    ["Charlie", "72", "C"]
]

table = format_table(headers, rows)
print(table)
```
:::

## Exercise 5: Build Log Entries

Create a function that generates log file entries.

```python live
def create_log_entries(events):
    """Create formatted log entries."""
    # Each event is (time, level, message)
    # Format: [TIME] [LEVEL] MESSAGE
    pass

events = [
    ("09:00:00", "INFO", "System started"),
    ("09:00:05", "DEBUG", "Loading modules"),
    ("09:00:10", "INFO", "Ready for connections"),
    ("09:05:30", "WARNING", "High memory usage"),
    ("09:10:00", "ERROR", "Connection timeout")
]

log = create_log_entries(events)
print(log)
```

:::expected_output
[09:00:00] [INFO] System started
[09:00:05] [DEBUG] Loading modules
[09:00:10] [INFO] Ready for connections
[09:05:30] [WARNING] High memory usage
[09:10:00] [ERROR] Connection timeout
:::

:::hint Stuck?
Format each event as `"[" + time + "] [" + level + "] " + message + "\n"`.
:::

:::answer Reveal answer
```python
def create_log_entries(events):
    """Create formatted log entries."""
    # Each event is (time, level, message)
    # Format: [TIME] [LEVEL] MESSAGE
    result = ""
    for time, level, message in events:
        result += "[" + time + "] [" + level + "] " + message + "\n"
    return result

events = [
    ("09:00:00", "INFO", "System started"),
    ("09:00:05", "DEBUG", "Loading modules"),
    ("09:00:10", "INFO", "Ready for connections"),
    ("09:05:30", "WARNING", "High memory usage"),
    ("09:10:00", "ERROR", "Connection timeout")
]

log = create_log_entries(events)
print(log)
```
:::

