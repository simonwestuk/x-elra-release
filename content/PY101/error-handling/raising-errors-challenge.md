---
title: "Challenge: Build a Form Validator"
slug: raising-errors-challenge
description: "Create a comprehensive form validation system"
course_id: PY101
module: error-handling
module_order: 5
topic: raising-errors
topic_order: 4
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - raising-errors-practice
skills:
  - errors
  - exceptions
outcomes:
  - "Design validation systems"
  - "Raise appropriate exceptions"
  - "Create helpful error messages"
capstone_relevance: "Data validation is crucial for your capstone application"
---

## Challenge: Registration Form Validator

Build a comprehensive form validator for a user registration system.

### Requirements

Create these validation functions:

1. **`validate_email(email)`**:
   - Must be a string (TypeError if not)
   - Must contain exactly one @ symbol
   - Must have text before and after @
   - Must have at least one . after @

2. **`validate_password(password)`**:
   - Must be at least 8 characters
   - Must contain at least one uppercase letter
   - Must contain at least one lowercase letter
   - Must contain at least one digit

3. **`validate_age(age)`**:
   - Must be an integer (TypeError if not)
   - Must be between 13 and 120

4. **`validate_username(username)`**:
   - Must be 3-20 characters
   - Must start with a letter
   - Can only contain letters, numbers, and underscores

5. **`validate_registration(username, email, password, age)`**:
   - Validates all fields
   - Returns dict with validated data if all pass
   - Raises first validation error encountered

### Your Solution

```python live
def validate_email(email):
    """Validate email format."""
    # Your validation code
    pass

def validate_password(password):
    """Validate password strength."""
    # Your validation code
    pass

def validate_age(age):
    """Validate age range."""
    # Your validation code
    pass

def validate_username(username):
    """Validate username format."""
    # Your validation code
    pass

def validate_registration(username, email, password, age):
    """Validate complete registration."""
    # Call all validators
    pass


# Test the validators
test_cases = [
    # Valid registration
    ("alice_99", "alice@email.com", "Secret123", 25),
    # Invalid email
    ("bob", "invalid-email", "Secret123", 25),
    # Weak password
    ("charlie", "charlie@test.com", "weak", 25),
    # Invalid age
    ("david", "david@test.com", "Strong123", 10),
    # Invalid username
    ("99problems", "user@test.com", "Secret123", 25),
]

print("=== Registration Validator Tests ===\n")
for username, email, password, age in test_cases:
    try:
        result = validate_registration(username, email, password, age)
        print("SUCCESS:", result)
    except (ValueError, TypeError) as e:
        print("FAILED:", e)
    print()
```

:::expected_output
=== Registration Validator Tests ===

SUCCESS: {'username': 'alice_99', 'email': 'alice@email.com', 'age': 25}

FAILED: Email must contain exactly one @ symbol

FAILED: Password must be at least 8 characters

FAILED: Age must be at least 13

FAILED: Username must start with a letter

:::

### Expected Output

```
=== Registration Validator Tests ===

SUCCESS: {'username': 'alice_99', 'email': 'alice@email.com', 'age': 25}

FAILED: Email must contain exactly one @ symbol

FAILED: Password must be at least 8 characters

FAILED: Age must be at least 13

FAILED: Username must start with a letter
```

:::hint Email Validation
Use `email.count("@") == 1` to check for exactly one @. Split by @ and check both parts have content.
:::

:::hint Password Requirements
Use `any(c.isupper() for c in password)` for uppercase check. Similar for lowercase and digit.
:::

:::hint Username Validation
Use `username[0].isalpha()` to check first character. Use `all(c.isalnum() or c == '_' for c in username)` for valid characters.
:::

:::hint Registration Function
Call each validator in order. If any raises, it will bubble up. If all pass, return the data dict.
:::

:::answer Reveal full solution
```python
def validate_email(email):
    """Validate email format."""
    if not isinstance(email, str):
        raise TypeError("Email must be a string")
    if email.count("@") != 1:
        raise ValueError("Email must contain exactly one @ symbol")
    parts = email.split("@")
    if not parts[0] or not parts[1]:
        raise ValueError("Email must have text before and after @")
    if "." not in parts[1]:
        raise ValueError("Email must have at least one . after @")
    return True

def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit")
    return True

def validate_age(age):
    """Validate age range."""
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 13:
        raise ValueError("Age must be at least 13")
    if age > 120:
        raise ValueError("Age must be at most 120")
    return True

def validate_username(username):
    """Validate username format."""
    if len(username) < 3 or len(username) > 20:
        raise ValueError("Username must be 3-20 characters")
    if not username[0].isalpha():
        raise ValueError("Username must start with a letter")
    if not all(c.isalnum() or c == '_' for c in username):
        raise ValueError("Username can only contain letters, numbers, and underscores")
    return True

def validate_registration(username, email, password, age):
    """Validate complete registration."""
    validate_username(username)
    validate_email(email)
    validate_password(password)
    validate_age(age)
    return {"username": username, "email": email, "age": age}


# Test the validators
test_cases = [
    # Valid registration
    ("alice_99", "alice@email.com", "Secret123", 25),
    # Invalid email
    ("bob", "invalid-email", "Secret123", 25),
    # Weak password
    ("charlie", "charlie@test.com", "weak", 25),
    # Invalid age
    ("david", "david@test.com", "Strong123", 10),
    # Invalid username
    ("99problems", "user@test.com", "Secret123", 25),
]

print("=== Registration Validator Tests ===\n")
for username, email, password, age in test_cases:
    try:
        result = validate_registration(username, email, password, age)
        print("SUCCESS:", result)
    except (ValueError, TypeError) as e:
        print("FAILED:", e)
    print()
```
:::

