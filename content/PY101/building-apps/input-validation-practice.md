---
title: "Practice: Input Validation"
slug: input-validation-practice
description: "Practice validating user input"
course_id: PY101
module: building-apps
module_order: 7
topic: input-validation
topic_order: 3
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - input-validation-lesson
skills:
  - validation
  - error-handling
outcomes:
  - "Create validation functions"
  - "Handle various input types"
  - "Return meaningful error messages"
capstone_relevance: "Validation protects your application from bad data"
---

## Exercise 1: Validate Positive Number

Create a function that validates a positive number.

```python live
def validate_positive(value, field_name="number"):
    """
    Validate that value is a positive number.
    Return (True, None) if valid.
    Return (False, error_message) if invalid.
    """
    # Your code here
    pass

# Test
print(validate_positive(10))        # (True, None)
print(validate_positive(0))         # (False, "...")
print(validate_positive(-5))        # (False, "...")
print(validate_positive("ten"))     # (False, "...")
```

:::expected_output
(True, None)
(False, 'number must be positive')
(False, 'number must be positive')
(False, 'number must be a number')
:::

:::hint Stuck?
Check `isinstance(value, (int, float))` first, then check if value > 0.
:::

:::answer Reveal answer
```python
def validate_positive(value, field_name="number"):
    """
    Validate that value is a positive number.
    Return (True, None) if valid.
    Return (False, error_message) if invalid.
    """
    if not isinstance(value, (int, float)):
        return (False, field_name + " must be a number")
    if value <= 0:
        return (False, field_name + " must be positive")
    return (True, None)

# Test
print(validate_positive(10))        # (True, None)
print(validate_positive(0))         # (False, "...")
print(validate_positive(-5))        # (False, "...")
print(validate_positive("ten"))     # (False, "...")
```
:::

## Exercise 2: Validate Username

Create a function to validate usernames with these rules:
- Must be a string
- 3-20 characters long
- Only letters, numbers, and underscores

```python live
def validate_username(username):
    """Validate username format."""
    # Your code here
    pass

# Test
print(validate_username("alice_123"))   # (True, None)
print(validate_username("ab"))          # Too short
print(validate_username("user@name"))   # Invalid character
print(validate_username(123))           # Not a string
```

:::expected_output
(True, None)
(False, 'Username must be at least 3 characters')
(False, 'Username can only contain letters, numbers, and underscores')
(False, 'Username must be a string')
:::

:::hint Stuck?
Check type with isinstance, length with len, and characters with `all(c.isalnum() or c == '_' for c in username)`.
:::

:::answer Reveal answer
```python
def validate_username(username):
    """Validate username format."""
    if not isinstance(username, str):
        return (False, "Username must be a string")
    if len(username) < 3:
        return (False, "Username must be at least 3 characters")
    if len(username) > 20:
        return (False, "Username must be at most 20 characters")
    if not all(c.isalnum() or c == '_' for c in username):
        return (False, "Username can only contain letters, numbers, and underscores")
    return (True, None)

# Test
print(validate_username("alice_123"))   # (True, None)
print(validate_username("ab"))          # Too short
print(validate_username("user@name"))   # Invalid character
print(validate_username(123))           # Not a string
```
:::

## Exercise 3: Validate Date String

Validate a date in YYYY-MM-DD format.

```python live
def validate_date_string(date_str):
    """Validate date format YYYY-MM-DD."""
    # Check: string type, length 10, correct format
    # Check: year 1900-2100, month 1-12, day 1-31
    # Your code here
    pass

# Test
print(validate_date_string("2024-01-15"))  # Valid
print(validate_date_string("2024-13-01"))  # Invalid month
print(validate_date_string("2024/01/15"))  # Wrong format
print(validate_date_string("24-01-15"))    # Wrong year format
```

:::expected_output
(True, None)
(False, 'Month must be between 1 and 12')
(False, 'Date must be in YYYY-MM-DD format')
(False, 'Date must be in YYYY-MM-DD format')
:::

:::hint Stuck?
Split by "-", check you get 3 parts, convert to int, validate ranges.
:::

:::answer Reveal answer
```python
def validate_date_string(date_str):
    """Validate date format YYYY-MM-DD."""
    if not isinstance(date_str, str):
        return (False, "Date must be a string")
    if len(date_str) != 10:
        return (False, "Date must be in YYYY-MM-DD format")
    parts = date_str.split("-")
    if len(parts) != 3:
        return (False, "Date must be in YYYY-MM-DD format")
    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
    except ValueError:
        return (False, "Date parts must be numbers")
    if len(parts[0]) != 4:
        return (False, "Year must be 4 digits")
    if year < 1900 or year > 2100:
        return (False, "Year must be between 1900 and 2100")
    if month < 1 or month > 12:
        return (False, "Month must be between 1 and 12")
    if day < 1 or day > 31:
        return (False, "Day must be between 1 and 31")
    return (True, None)

# Test
print(validate_date_string("2024-01-15"))  # Valid
print(validate_date_string("2024-13-01"))  # Invalid month
print(validate_date_string("2024/01/15"))  # Wrong format
print(validate_date_string("24-01-15"))    # Wrong year format
```
:::

## Exercise 4: Validate Product Data

Create a function to validate product data.

```python live
def validate_product(product):
    """
    Validate product dictionary.
    Required: name (string, 1-100 chars), price (number > 0)
    Optional: quantity (integer >= 0)
    """
    errors = []

    # Validate name
    # Your code here

    # Validate price
    # Your code here

    # Validate quantity (if present)
    # Your code here

    return len(errors) == 0, errors

# Test
valid = {"name": "Laptop", "price": 999.99, "quantity": 5}
print("Valid product:", validate_product(valid))

invalid = {"name": "", "price": -50, "quantity": -1}
print("Invalid product:", validate_product(invalid))

missing = {"price": 100}
print("Missing name:", validate_product(missing))
```

:::expected_output
Valid product: (True, [])
Invalid product: (False, ['Name must be a non-empty string', 'Price must be greater than 0', 'Quantity must be 0 or greater'])
Missing name: (False, ['Name is required'])
:::

:::hint Stuck?
Check if key exists with `"key" in product`, then validate the value.
:::

:::answer Reveal answer
```python
def validate_product(product):
    """
    Validate product dictionary.
    Required: name (string, 1-100 chars), price (number > 0)
    Optional: quantity (integer >= 0)
    """
    errors = []

    # Validate name
    if "name" not in product:
        errors.append("Name is required")
    elif not isinstance(product["name"], str) or len(product["name"]) < 1:
        errors.append("Name must be a non-empty string")
    elif len(product["name"]) > 100:
        errors.append("Name must be 100 characters or less")

    # Validate price
    if "price" not in product:
        errors.append("Price is required")
    elif not isinstance(product["price"], (int, float)):
        errors.append("Price must be a number")
    elif product["price"] <= 0:
        errors.append("Price must be greater than 0")

    # Validate quantity (if present)
    if "quantity" in product:
        if not isinstance(product["quantity"], int):
            errors.append("Quantity must be an integer")
        elif product["quantity"] < 0:
            errors.append("Quantity must be 0 or greater")

    return len(errors) == 0, errors

# Test
valid = {"name": "Laptop", "price": 999.99, "quantity": 5}
print("Valid product:", validate_product(valid))

invalid = {"name": "", "price": -50, "quantity": -1}
print("Invalid product:", validate_product(invalid))

missing = {"price": 100}
print("Missing name:", validate_product(missing))
```
:::

## Exercise 5: Create Input Loop

Create a function that keeps asking for input until valid.

```python live
def get_valid_score():
    """
    Get a valid score (0-100) from user.
    Simulated with test inputs.
    """
    # Simulated inputs (in real app, would use input())
    test_inputs = ["abc", "-5", "150", "85"]
    input_index = [0]  # Mutable to track position

    def get_input(prompt):
        result = test_inputs[input_index[0]]
        print(prompt + result)
        input_index[0] += 1
        return result

    while True:
        user_input = get_input("Enter score (0-100): ")

        # Validate the input
        try:
            score = int(user_input)
            if 0 <= score <= 100:
                return score
            else:
                print("Score must be between 0 and 100")
        except ValueError:
            print("Please enter a valid number")

        if input_index[0] >= len(test_inputs):
            break

    return None

result = get_valid_score()
print("Valid score received:", result)
```

:::expected_output
Enter score (0-100): abc
Please enter a valid number
Enter score (0-100): -5
Score must be between 0 and 100
Enter score (0-100): 150
Score must be between 0 and 100
Enter score (0-100): 85
Valid score received: 85
:::

:::hint Pattern
Use a while True loop, try to parse/validate, return if valid, print error and continue if not.
:::

:::answer Reveal answer
```python
def get_valid_score():
    """
    Get a valid score (0-100) from user.
    Simulated with test inputs.
    """
    # Simulated inputs (in real app, would use input())
    test_inputs = ["abc", "-5", "150", "85"]
    input_index = [0]  # Mutable to track position

    def get_input(prompt):
        result = test_inputs[input_index[0]]
        print(prompt + result)
        input_index[0] += 1
        return result

    while True:
        user_input = get_input("Enter score (0-100): ")

        # Validate the input
        try:
            score = int(user_input)
            if 0 <= score <= 100:
                return score
            else:
                print("Score must be between 0 and 100")
        except ValueError:
            print("Please enter a valid number")

        if input_index[0] >= len(test_inputs):
            break

    return None

result = get_valid_score()
print("Valid score received:", result)
```
:::

