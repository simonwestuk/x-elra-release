---
title: "Practice: File Modes"
slug: file-modes-practice
description: "Practice choosing and using file modes"
course_id: PY101
module: file-operations
module_order: 6
topic: file-modes
topic_order: 3
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - file-modes-lesson
skills:
  - file-io
  - files
outcomes:
  - "Choose correct file modes"
  - "Understand mode behaviors"
  - "Avoid common mode mistakes"
capstone_relevance: "Correct mode selection prevents data loss"
---

## Exercise 1: Mode Selection

For each scenario, choose the correct file mode.

```python live
def get_mode(scenario):
    """Return the best mode for the scenario."""
    # Fill in the correct modes
    modes = {
        "read_existing": "?",      # Read an existing config file
        "create_new": "?",         # Create a new file, error if exists
        "overwrite": "?",          # Replace file contents completely
        "append_log": "?",         # Add entries to a log file
        "update_file": "?",        # Read and modify existing file
    }
    return modes.get(scenario, "unknown")

# Test your answers
scenarios = [
    ("read_existing", "r"),
    ("create_new", "x"),
    ("overwrite", "w"),
    ("append_log", "a"),
    ("update_file", "r+")
]

print("Scenario         | Your Answer | Correct")
print("-" * 45)
for scenario, correct in scenarios:
    your_answer = get_mode(scenario)
    match = "✓" if your_answer == correct else "✗"
    print(scenario.ljust(16) + " | " + your_answer.ljust(11) + " | " + correct + " " + match)
```

:::expected_output
Scenario         | Your Answer | Correct
---------------------------------------------
read_existing    | r           | r ✓
create_new       | x           | x ✓
overwrite        | w           | w ✓
append_log       | a           | a ✓
update_file      | r+          | r+ ✓
:::

:::hint Stuck?
- Read existing: `"r"`
- Create new (fail if exists): `"x"`
- Overwrite: `"w"`
- Append: `"a"`
- Update (read + write): `"r+"`
:::

:::answer Reveal answer
```python
def get_mode(scenario):
    """Return the best mode for the scenario."""
    # Fill in the correct modes
    modes = {
        "read_existing": "r",      # Read an existing config file
        "create_new": "x",         # Create a new file, error if exists
        "overwrite": "w",          # Replace file contents completely
        "append_log": "a",         # Add entries to a log file
        "update_file": "r+",       # Read and modify existing file
    }
    return modes.get(scenario, "unknown")

# Test your answers
scenarios = [
    ("read_existing", "r"),
    ("create_new", "x"),
    ("overwrite", "w"),
    ("append_log", "a"),
    ("update_file", "r+")
]

print("Scenario         | Your Answer | Correct")
print("-" * 45)
for scenario, correct in scenarios:
    your_answer = get_mode(scenario)
    match = "✓" if your_answer == correct else "✗"
    print(scenario.ljust(16) + " | " + your_answer.ljust(11) + " | " + correct + " " + match)
```
:::

## Exercise 2: Mode Behavior Prediction

Predict what each mode does in these situations.

```python live
def predict_behavior(mode, file_exists):
    """Predict what happens when opening with given mode."""
    # Complete this function
    # Return: "success", "error_not_found", "error_exists",
    #         "creates_new", "erases_content"
    pass

test_cases = [
    ("r", True, "success"),           # Read existing file
    ("r", False, "error_not_found"),  # Read missing file
    ("w", True, "erases_content"),    # Write existing file
    ("w", False, "creates_new"),      # Write missing file
    ("a", True, "success"),           # Append existing file
    ("a", False, "creates_new"),      # Append missing file
    ("x", True, "error_exists"),      # Exclusive existing file
    ("x", False, "creates_new"),      # Exclusive missing file
]

print("Mode | Exists | Expected Result")
print("-" * 35)
for mode, exists, expected in test_cases:
    exists_str = "Yes" if exists else "No "
    print(mode.ljust(4) + " | " + exists_str + "    | " + expected)
```

:::expected_output
Mode | Exists | Expected Result
-----------------------------------
r    | Yes    | success
r    | No     | error_not_found
w    | Yes    | erases_content
w    | No     | creates_new
a    | Yes    | success
a    | No     | creates_new
x    | Yes    | error_exists
x    | No     | creates_new
:::

:::hint Modes Summary
- `"r"`: Must exist, read only
- `"w"`: Creates or erases, write only
- `"a"`: Creates or appends, write only
- `"x"`: Must NOT exist, creates new
:::

:::answer Reveal answer
```python
def predict_behavior(mode, file_exists):
    """Predict what happens when opening with given mode."""
    # Return: "success", "error_not_found", "error_exists",
    #         "creates_new", "erases_content"
    if mode == "r":
        if file_exists:
            return "success"
        else:
            return "error_not_found"
    elif mode == "w":
        if file_exists:
            return "erases_content"
        else:
            return "creates_new"
    elif mode == "a":
        if file_exists:
            return "success"
        else:
            return "creates_new"
    elif mode == "x":
        if file_exists:
            return "error_exists"
        else:
            return "creates_new"

test_cases = [
    ("r", True, "success"),           # Read existing file
    ("r", False, "error_not_found"),  # Read missing file
    ("w", True, "erases_content"),    # Write existing file
    ("w", False, "creates_new"),      # Write missing file
    ("a", True, "success"),           # Append existing file
    ("a", False, "creates_new"),      # Append missing file
    ("x", True, "error_exists"),      # Exclusive existing file
    ("x", False, "creates_new"),      # Exclusive missing file
]

print("Mode | Exists | Expected Result")
print("-" * 35)
for mode, exists, expected in test_cases:
    exists_str = "Yes" if exists else "No "
    print(mode.ljust(4) + " | " + exists_str + "    | " + expected)
```
:::

## Exercise 3: Safe File Operations

Create functions that use the correct modes safely.

```python live
def read_config(filename):
    """Read a config file. Return None if not found."""
    # Which mode should you use?
    # Handle FileNotFoundError
    pass

def save_config(filename, config):
    """Save config to file, overwriting existing."""
    # Which mode?
    pass

def add_log_entry(filename, entry):
    """Add an entry to a log file (don't erase existing)."""
    # Which mode?
    pass

def create_new_file(filename, content):
    """Create a new file, but fail if it already exists."""
    # Which mode?
    pass

# Describe the modes you would use:
print("Function          | Mode | Why")
print("-" * 50)
print("read_config       | r    | Only reading, file must exist")
print("save_config       | w    | Overwrite with new content")
print("add_log_entry     | a    | Add without erasing")
print("create_new_file   | x    | Fail if already exists")
```

:::expected_output
Function          | Mode | Why
--------------------------------------------------
read_config       | r    | Only reading, file must exist
save_config       | w    | Overwrite with new content
add_log_entry     | a    | Add without erasing
create_new_file   | x    | Fail if already exists
:::

:::answer Reveal answer
```python
def read_config(filename):
    """Read a config file. Return None if not found."""
    try:
        file = open(filename, "r")
        content = file.read()
        file.close()
        return content
    except FileNotFoundError:
        return None

def save_config(filename, config):
    """Save config to file, overwriting existing."""
    file = open(filename, "w")
    file.write(config)
    file.close()

def add_log_entry(filename, entry):
    """Add an entry to a log file (don't erase existing)."""
    file = open(filename, "a")
    file.write(entry + "\n")
    file.close()

def create_new_file(filename, content):
    """Create a new file, but fail if it already exists."""
    file = open(filename, "x")
    file.write(content)
    file.close()

# Describe the modes you would use:
print("Function          | Mode | Why")
print("-" * 50)
print("read_config       | r    | Only reading, file must exist")
print("save_config       | w    | Overwrite with new content")
print("add_log_entry     | a    | Add without erasing")
print("create_new_file   | x    | Fail if already exists")
```
:::

## Exercise 4: Mode Dangers

Identify the problem in each code snippet.

```python live
# Problem 1: What's wrong here?
# def add_score(filename, score):
#     file = open(filename, "w")  # Problem!
#     file.write(str(score) + "\n")
#     file.close()

print("Problem 1: Using 'w' mode erases existing scores!")
print("Fix: Use 'a' mode to append")
print()

# Problem 2: What's wrong here?
# def read_data(filename):
#     file = open(filename, "r")
#     data = file.read()
#     file.close()
#     return data

print("Problem 2: No error handling for missing file!")
print("Fix: Use try/except for FileNotFoundError")
print()

# Problem 3: What's wrong here?
# def backup_and_update(filename):
#     file = open(filename, "w")  # Problem!
#     backup = file.read()  # Can't read in 'w' mode!

print("Problem 3: Can't read in 'w' mode!")
print("Fix: Use 'r+' to read and write")
```

:::expected_output
Problem 1: Using 'w' mode erases existing scores!
Fix: Use 'a' mode to append

Problem 2: No error handling for missing file!
Fix: Use try/except for FileNotFoundError

Problem 3: Can't read in 'w' mode!
Fix: Use 'r+' to read and write
:::

:::answer Reveal answer
```python
# Problem 1: What's wrong here?
# Using "w" mode erases all existing scores every time!
# Fix: Use "a" mode to append new scores
def add_score(filename, score):
    file = open(filename, "a")  # Fixed: "a" instead of "w"
    file.write(str(score) + "\n")
    file.close()

# Problem 2: What's wrong here?
# No error handling if the file doesn't exist!
# Fix: Use try/except for FileNotFoundError
def read_data(filename):
    try:
        file = open(filename, "r")
        data = file.read()
        file.close()
        return data
    except FileNotFoundError:
        return None

# Problem 3: What's wrong here?
# Can't read in "w" mode, and "w" erases the file!
# Fix: Use "r+" to read and write
def backup_and_update(filename):
    file = open(filename, "r+")  # Fixed: "r+" instead of "w"
    backup = file.read()
    # Now you can write updates
    file.close()

print("Problem 1: Using 'w' mode erases existing scores!")
print("Fix: Use 'a' mode to append")
print()
print("Problem 2: No error handling for missing file!")
print("Fix: Use try/except for FileNotFoundError")
print()
print("Problem 3: Can't read in 'w' mode!")
print("Fix: Use 'r+' to read and write")
```
:::

## Exercise 5: Complete the Function

Write a function that safely updates a counter file.

```python live
def update_counter(filename):
    """
    Read counter from file, increment, and save back.
    If file doesn't exist, start at 0.
    Return the new counter value.
    """
    # Step 1: Try to read existing value
    # Step 2: Increment
    # Step 3: Write back
    # Consider: What modes do you need?
    pass

# Simulate the behavior
def demo_counter():
    counter = 0  # Simulating file content

    # First call - file doesn't exist (counter = 0)
    counter = 1
    print("Call 1: Counter is now", counter)

    # Second call
    counter = 2
    print("Call 2: Counter is now", counter)

    # Third call
    counter = 3
    print("Call 3: Counter is now", counter)

demo_counter()
```

:::expected_output
Call 1: Counter is now 1
Call 2: Counter is now 2
Call 3: Counter is now 3
:::

:::hint Counter Logic
1. Try to read with `"r"` mode (might not exist)
2. If file not found, start at 0
3. Increment the value
4. Write with `"w"` mode (overwrite with new value)
:::

:::answer Reveal answer
```python
def update_counter(filename):
    """
    Read counter from file, increment, and save back.
    If file doesn't exist, start at 0.
    Return the new counter value.
    """
    # Step 1: Try to read existing value
    try:
        file = open(filename, "r")
        counter = int(file.read().strip())
        file.close()
    except FileNotFoundError:
        counter = 0

    # Step 2: Increment
    counter += 1

    # Step 3: Write back
    file = open(filename, "w")
    file.write(str(counter))
    file.close()

    return counter

# Simulate the behavior
def demo_counter():
    counter = 0  # Simulating file content

    # First call - file doesn't exist (counter = 0)
    counter = 1
    print("Call 1: Counter is now", counter)

    # Second call
    counter = 2
    print("Call 2: Counter is now", counter)

    # Third call
    counter = 3
    print("Call 3: Counter is now", counter)

demo_counter()
```
:::

