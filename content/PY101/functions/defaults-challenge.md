---
title: "Challenge: Build a Logger"
slug: defaults-challenge
description: "Create a flexible logging system using default parameters"
course_id: PY101
module: functions
module_order: 4
topic: defaults
topic_order: 4
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - defaults-practice
skills:
  - functions
  - parameters
outcomes:
  - "Design functions with sensible defaults"
  - "Create flexible, reusable utilities"
  - "Balance required and optional parameters"
capstone_relevance: "Logging is useful for debugging your application"
---

## Challenge: Application Logger

Build a flexible logging system that can format and display messages with different levels and styles.

### Requirements

1. Create `format_timestamp(hour=12, minute=0, second=0)` that returns a timestamp string:
   - Format: "HH:MM:SS" (with leading zeros)
   - Example: format_timestamp(9, 5, 30) returns "09:05:30"

2. Create `log(message, level="INFO", show_timestamp=True, hour=12, minute=0)` that prints:
   - With timestamp: "[HH:MM:00] [LEVEL] message"
   - Without timestamp: "[LEVEL] message"

3. Create `log_error(message, code=500, hour=12, minute=0)` that prints:
   - "[HH:MM:00] [ERROR] (code) message"

4. Create `log_separator(char="-", length=40)` that prints a line of characters.

### Your Solution

```python live
# Define your functions here




# Test the logging system
log_separator("=")
log("Application starting", hour=9, minute=0)
log("Loading configuration", hour=9, minute=1)
log("Config loaded", level="DEBUG", show_timestamp=False)
log_separator()
log_error("Database connection failed", code=503, hour=9, minute=2)
log_error("Retrying...", hour=9, minute=3)
log_separator()
log("Application ready", level="SUCCESS", hour=9, minute=5)
log_separator("=")
```

:::expected_output
========================================
[09:00:00] [INFO] Application starting
[09:01:00] [INFO] Loading configuration
[DEBUG] Config loaded
----------------------------------------
[09:02:00] [ERROR] (503) Database connection failed
[09:03:00] [ERROR] (500) Retrying...
----------------------------------------
[09:05:00] [SUCCESS] Application ready
========================================
:::

### Expected Output

```
========================================
[09:00:00] [INFO] Application starting
[09:01:00] [INFO] Loading configuration
[DEBUG] Config loaded
----------------------------------------
[09:02:00] [ERROR] (503) Database connection failed
[09:03:00] [ERROR] (500) Retrying...
----------------------------------------
[09:05:00] [SUCCESS] Application ready
========================================
```

:::hint Leading Zeros
To add leading zeros: `str(hour).zfill(2)` pads a number to 2 digits. Example: `str(9).zfill(2)` gives "09".
:::

:::hint Building Strings
Build your log string piece by piece, then print it at the end.
:::

:::hint Reuse Functions
`log_error` can call `format_timestamp` and follow a similar pattern to `log`.
:::

:::answer Reveal full solution
```python
def format_timestamp(hour=12, minute=0, second=0):
    return str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)

def log(message, level="INFO", show_timestamp=True, hour=12, minute=0):
    if show_timestamp:
        print("[" + format_timestamp(hour, minute) + "] [" + level + "] " + message)
    else:
        print("[" + level + "] " + message)

def log_error(message, code=500, hour=12, minute=0):
    print("[" + format_timestamp(hour, minute) + "] [ERROR] (" + str(code) + ") " + message)

def log_separator(char="-", length=40):
    print(char * length)

# Test the logging system
log_separator("=")
log("Application starting", hour=9, minute=0)
log("Loading configuration", hour=9, minute=1)
log("Config loaded", level="DEBUG", show_timestamp=False)
log_separator()
log_error("Database connection failed", code=503, hour=9, minute=2)
log_error("Retrying...", hour=9, minute=3)
log_separator()
log("Application ready", level="SUCCESS", hour=9, minute=5)
log_separator("=")
```
:::

