---
title: "Input Validation"
slug: input-validation-lesson
description: "Learn to validate and sanitize user input"
course_id: PY101
module: building-apps
module_order: 7
topic: input-validation
topic_order: 3
type: lesson
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - try-except-lesson
  - raising-errors-lesson
skills:
  - validation
  - error-handling
outcomes:
  - "Validate user input before processing"
  - "Handle invalid input gracefully"
  - "Create robust input functions"
capstone_relevance: "Input validation is critical for user-facing applications"
---

## Introduction

Never trust user input! **Input validation** checks that data meets your requirements before using it. This prevents errors, crashes, and security issues.

## Why Validate?

```python live
# Without validation - crash waiting to happen!
def dangerous_divide(a, b):
    return a / b  # What if b is 0? Or not a number?

# With validation - safe and informative
def safe_divide(a, b):
    if not isinstance(a, (int, float)):
        return "Error: First value must be a number"
    if not isinstance(b, (int, float)):
        return "Error: Second value must be a number"
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))
```

:::expected_output
5.0
Error: Cannot divide by zero
Error: First value must be a number
:::

## Validation Types

### Type Validation

```python live
def validate_type(value, expected_type, field_name):
    """Check if value is the expected type."""
    if not isinstance(value, expected_type):
        return False, field_name + " must be " + expected_type.__name__
    return True, None

# Test
print(validate_type(25, int, "age"))
print(validate_type("25", int, "age"))
print(validate_type("hello", str, "name"))
```

:::expected_output
(True, None)
(False, 'age must be int')
(True, None)
:::

### Range Validation

```python live
def validate_range(value, min_val, max_val, field_name):
    """Check if value is within range."""
    if value < min_val or value > max_val:
        return False, field_name + " must be between " + str(min_val) + " and " + str(max_val)
    return True, None

# Test
print(validate_range(25, 18, 65, "age"))
print(validate_range(10, 18, 65, "age"))
print(validate_range(100, 0, 100, "percentage"))
```

:::expected_output
(True, None)
(False, 'age must be between 18 and 65')
(True, None)
:::

### String Validation

```python live
def validate_string(value, min_len=1, max_len=100, field_name="field"):
    """Validate string length."""
    if not isinstance(value, str):
        return False, field_name + " must be a string"
    if len(value) < min_len:
        return False, field_name + " must be at least " + str(min_len) + " characters"
    if len(value) > max_len:
        return False, field_name + " must be at most " + str(max_len) + " characters"
    return True, None

# Test
print(validate_string("Alice", 2, 50, "name"))
print(validate_string("A", 2, 50, "name"))
print(validate_string("", 1, 50, "name"))
```

:::expected_output
(True, None)
(False, 'name must be at least 2 characters')
(False, 'name must be at least 1 characters')
:::

## Email Validation

```python live
def validate_email(email):
    """Basic email validation."""
    errors = []

    if not isinstance(email, str):
        return False, ["Email must be a string"]

    if not email:
        return False, ["Email is required"]

    if "@" not in email:
        errors.append("Email must contain @")

    if "." not in email:
        errors.append("Email must contain a domain")

    parts = email.split("@")
    if len(parts) != 2:
        errors.append("Email must have exactly one @")
    elif not parts[0]:
        errors.append("Email must have text before @")
    elif not parts[1]:
        errors.append("Email must have domain after @")

    return len(errors) == 0, errors

# Test
print(validate_email("alice@example.com"))
print(validate_email("invalid"))
print(validate_email("@nodomain.com"))
print(validate_email("no.at.sign.com"))
```

:::expected_output
(True, [])
(False, ['Email must contain @', 'Email must contain a domain', 'Email must have exactly one @'])
(False, ['Email must have text before @'])
(False, ['Email must contain @', 'Email must have exactly one @'])
:::

## Creating a Validator Function

```python live
def validate_user_data(data):
    """Validate complete user data."""
    errors = []

    # Name validation
    if "name" not in data:
        errors.append("Name is required")
    elif not isinstance(data["name"], str):
        errors.append("Name must be a string")
    elif len(data["name"]) < 2:
        errors.append("Name must be at least 2 characters")

    # Age validation
    if "age" not in data:
        errors.append("Age is required")
    elif not isinstance(data["age"], int):
        errors.append("Age must be an integer")
    elif data["age"] < 0 or data["age"] > 150:
        errors.append("Age must be between 0 and 150")

    # Email validation
    if "email" in data and data["email"]:
        if "@" not in data["email"]:
            errors.append("Invalid email format")

    return len(errors) == 0, errors

# Test with valid data
valid_data = {"name": "Alice", "age": 25, "email": "alice@example.com"}
is_valid, errors = validate_user_data(valid_data)
print("Valid data:", is_valid, errors)

# Test with invalid data
invalid_data = {"name": "A", "age": -5, "email": "invalid"}
is_valid, errors = validate_user_data(invalid_data)
print("Invalid data:", is_valid, errors)
```

:::expected_output
Valid data: True []
Invalid data: False ['Name must be at least 2 characters', 'Age must be between 0 and 150', 'Invalid email format']
:::

## Sanitizing Input

```python live
def sanitize_string(value):
    """Clean up string input."""
    if not isinstance(value, str):
        return str(value)

    # Remove leading/trailing whitespace
    value = value.strip()

    # Remove extra internal whitespace
    value = " ".join(value.split())

    return value

def sanitize_number(value):
    """Convert to number, return None if invalid."""
    try:
        # Try integer first
        if isinstance(value, str) and "." not in value:
            return int(value)
        return float(value)
    except (ValueError, TypeError):
        return None

# Test
print("Sanitized string:", repr(sanitize_string("  Hello   World  ")))
print("Sanitized number:", sanitize_number("42"))
print("Sanitized float:", sanitize_number("3.14"))
print("Invalid number:", sanitize_number("abc"))
```

:::expected_output
Sanitized string: 'Hello World'
Sanitized number: 42
Sanitized float: 3.14
Invalid number: None
:::

## Combined Validation Pattern

```python live
def get_validated_age(input_value):
    """Get and validate age from user input."""
    # Step 1: Sanitize
    cleaned = sanitize_number(input_value) if 'sanitize_number' in dir() else None

    # Simple implementation
    try:
        age = int(input_value)
    except (ValueError, TypeError):
        return None, "Please enter a valid number"

    # Step 2: Validate range
    if age < 0:
        return None, "Age cannot be negative"
    if age > 150:
        return None, "Please enter a realistic age"

    return age, None

# Test
print(get_validated_age("25"))
print(get_validated_age("-5"))
print(get_validated_age("abc"))
print(get_validated_age("200"))
```

:::expected_output
(25, None)
(None, 'Age cannot be negative')
(None, 'Please enter a valid number')
(None, 'Please enter a realistic age')
:::

## Key Points

- Always validate input before using it
- Check type, format, and range
- Return helpful error messages
- Sanitize input (trim whitespace, etc.)
- Validate early, fail fast
- Consider all edge cases

:::hint Remember
It's better to reject valid input occasionally than to accept invalid input that crashes your program or corrupts your data!
:::

