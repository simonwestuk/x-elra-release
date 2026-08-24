---
title: "Challenge: Build a Log Analyzer"
slug: reading-files-challenge
description: "Create a log file analyzer that extracts insights from log data"
course_id: PY101
module: file-operations
module_order: 6
topic: reading-files
topic_order: 1
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - reading-files-practice
skills:
  - file-io
  - files
outcomes:
  - "Parse complex file formats"
  - "Extract meaningful data from files"
  - "Generate reports from file data"
capstone_relevance: "Log analysis is common in real applications"
---

## Challenge: Log File Analyzer

Build a system to analyze application log files and generate useful reports.

### Log Format

Each log line has the format: `[TIMESTAMP] [LEVEL] Message`

```
[09:15:30] [INFO] Application started
[09:15:31] [DEBUG] Loading configuration
[09:15:32] [INFO] Configuration loaded successfully
[09:15:45] [WARNING] High memory usage detected
[09:16:00] [ERROR] Database connection failed
[09:16:05] [INFO] Retrying database connection
[09:16:10] [INFO] Database connected
[09:17:00] [ERROR] User authentication failed
[09:18:30] [INFO] User login successful
[09:19:00] [WARNING] API rate limit approaching
[09:20:00] [INFO] Application shutdown
```

### Requirements

1. **`parse_log_line(line)`** - Parse a log line and return a dictionary with:
   - `timestamp` - The time string
   - `level` - The log level (INFO, DEBUG, WARNING, ERROR)
   - `message` - The log message

2. **`count_by_level(log_lines)`** - Return a dictionary counting entries by level

3. **`get_errors(log_lines)`** - Return a list of all error messages

4. **`generate_report(log_content)`** - Generate a full analysis report

### Your Solution

```python live
def parse_log_line(line):
    """Parse a single log line into components."""
    # Format: [09:15:30] [INFO] Message
    # Your code here
    pass

def count_by_level(log_lines):
    """Count log entries by level."""
    # Your code here
    pass

def get_errors(log_lines):
    """Get all error messages with timestamps."""
    # Your code here
    pass

def generate_report(log_content):
    """Generate complete analysis report."""
    # Your code here
    pass


# Test data
log_data = """[09:15:30] [INFO] Application started
[09:15:31] [DEBUG] Loading configuration
[09:15:32] [INFO] Configuration loaded successfully
[09:15:45] [WARNING] High memory usage detected
[09:16:00] [ERROR] Database connection failed
[09:16:05] [INFO] Retrying database connection
[09:16:10] [INFO] Database connected
[09:17:00] [ERROR] User authentication failed
[09:18:30] [INFO] User login successful
[09:19:00] [WARNING] API rate limit approaching
[09:20:00] [INFO] Application shutdown"""

# Generate the report
generate_report(log_data)
```

:::expected_output
=== Log Analysis Report ===

Total entries: 11

Entries by level:
  INFO: 6
  DEBUG: 1
  WARNING: 2
  ERROR: 2

Errors found:
  [09:16:00] Database connection failed
  [09:17:00] User authentication failed

=== End Report ===
:::

### Expected Output

```
=== Log Analysis Report ===

Total entries: 11

Entries by level:
  INFO: 6
  DEBUG: 1
  WARNING: 2
  ERROR: 2

Errors found:
  [09:16:00] Database connection failed
  [09:17:00] User authentication failed

=== End Report ===
```

:::hint Parsing Log Lines
Use string methods to extract parts. For `[09:15:30] [INFO] Message`:
- Timestamp is between positions 1-9
- Level can be found by splitting or searching for the second `[`
- Message is everything after the second `]`
:::

:::hint Counting by Level
Create a counts dictionary. Loop through lines, parse each, and increment the count for that level.
:::

:::hint Getting Errors
Loop through parsed lines, check if level is "ERROR", collect timestamp and message.
:::

:::answer Reveal full solution
```python
def parse_log_line(line):
    """Parse a single log line into components."""
    # Format: [09:15:30] [INFO] Message
    timestamp = line[1:9]
    rest = line[11:]  # after "] "
    bracket_end = rest.index("]")
    level = rest[1:bracket_end]
    message = rest[bracket_end + 2:]
    return {"timestamp": timestamp, "level": level, "message": message}

def count_by_level(log_lines):
    """Count log entries by level."""
    counts = {}
    for line in log_lines:
        parsed = parse_log_line(line)
        level = parsed["level"]
        if level in counts:
            counts[level] += 1
        else:
            counts[level] = 1
    return counts

def get_errors(log_lines):
    """Get all error messages with timestamps."""
    errors = []
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed["level"] == "ERROR":
            errors.append(parsed)
    return errors

def generate_report(log_content):
    """Generate complete analysis report."""
    lines = log_content.strip().split("\n")

    print("=== Log Analysis Report ===")
    print()
    print("Total entries:", len(lines))

    counts = count_by_level(lines)
    print()
    print("Entries by level:")
    for level in counts:
        print("  " + level + ": " + str(counts[level]))

    errors = get_errors(lines)
    print()
    print("Errors found:")
    for error in errors:
        print("  [" + error["timestamp"] + "] " + error["message"])

    print()
    print("=== End Report ===")


# Test data
log_data = """[09:15:30] [INFO] Application started
[09:15:31] [DEBUG] Loading configuration
[09:15:32] [INFO] Configuration loaded successfully
[09:15:45] [WARNING] High memory usage detected
[09:16:00] [ERROR] Database connection failed
[09:16:05] [INFO] Retrying database connection
[09:16:10] [INFO] Database connected
[09:17:00] [ERROR] User authentication failed
[09:18:30] [INFO] User login successful
[09:19:00] [WARNING] API rate limit approaching
[09:20:00] [INFO] Application shutdown"""

# Generate the report
generate_report(log_data)
```
:::

