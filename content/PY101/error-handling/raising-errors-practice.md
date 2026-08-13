---
title: "Practice: Raising Exceptions"
slug: raising-errors-practice
description: "Practice raising your own exceptions"
course_id: PY101
module: error-handling
module_order: 5
topic: raising-errors
topic_order: 4
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - raising-errors-lesson
skills:
  - errors
  - exceptions
outcomes:
  - "Raise appropriate exceptions"
  - "Write meaningful error messages"
  - "Implement input validation"
capstone_relevance: "Input validation is essential for robust applications"
---

## Exercise 1: Validate Positive Number

Create a function `require_positive` that raises a `ValueError` if the number is not positive.

```python live
def require_positive(n):
    # Raise ValueError if n is not positive
    pass
    return n

# Test
print(require_positive(5))    # Should return 5

try:
    require_positive(-3)      # Should raise ValueError
except ValueError as e:
    print("Error:", e)
```

:::expected_output
5
Error: Number must be positive
:::

:::hint Stuck?
Check `if n <= 0:` and then `raise ValueError("Number must be positive")`.
:::

:::answer Reveal answer
```python
def require_positive(n):
    # Raise ValueError if n is not positive
    if n <= 0:
        raise ValueError("Number must be positive")
    return n

# Test
print(require_positive(5))    # Should return 5

try:
    require_positive(-3)      # Should raise ValueError
except ValueError as e:
    print("Error:", e)
```
:::

## Exercise 2: Validate String Length

Create a function `validate_username` that:
- Raises `TypeError` if username is not a string
- Raises `ValueError` if username is shorter than 3 characters

```python live
def validate_username(username):
    # Add type and length validation
    pass
    return username

# Test
print(validate_username("alice"))  # Should return "alice"

try:
    validate_username("ab")        # Should raise ValueError
except ValueError as e:
    print("Error:", e)

try:
    validate_username(123)         # Should raise TypeError
except TypeError as e:
    print("Error:", e)
```

:::expected_output
alice
Error: Username must be at least 3 characters
Error: Username must be a string
:::

:::hint Stuck?
Use `isinstance(username, str)` to check the type. Use `len(username) < 3` for length.
:::

:::answer Reveal answer
```python
def validate_username(username):
    # Add type and length validation
    if not isinstance(username, str):
        raise TypeError("Username must be a string")
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters")
    return username

# Test
print(validate_username("alice"))  # Should return "alice"

try:
    validate_username("ab")        # Should raise ValueError
except ValueError as e:
    print("Error:", e)

try:
    validate_username(123)         # Should raise TypeError
except TypeError as e:
    print("Error:", e)
```
:::

## Exercise 3: Range Validation

Create a function `validate_percentage` that raises `ValueError` if the value is not between 0 and 100 (inclusive).

```python live
def validate_percentage(value):
    # Validate that value is between 0 and 100
    pass
    return value

# Test
print(validate_percentage(75))   # Should return 75
print(validate_percentage(0))    # Should return 0
print(validate_percentage(100))  # Should return 100

try:
    validate_percentage(150)     # Should raise ValueError
except ValueError as e:
    print("Error:", e)
```

:::expected_output
75
0
100
Error: Percentage must be between 0 and 100
:::

:::hint Stuck?
Check `if value < 0 or value > 100:` and raise with a message like "Percentage must be between 0 and 100".
:::

:::answer Reveal answer
```python
def validate_percentage(value):
    # Validate that value is between 0 and 100
    if value < 0 or value > 100:
        raise ValueError("Percentage must be between 0 and 100")
    return value

# Test
print(validate_percentage(75))   # Should return 75
print(validate_percentage(0))    # Should return 0
print(validate_percentage(100))  # Should return 100

try:
    validate_percentage(150)     # Should raise ValueError
except ValueError as e:
    print("Error:", e)
```
:::

## Exercise 4: Password Validator

Create a function `validate_password` that checks:
- At least 8 characters (raise ValueError if not)
- Contains at least one digit (raise ValueError if not)

```python live
def validate_password(password):
    # Check length and digit requirement
    pass
    return "Password is valid"

# Test
print(validate_password("secret123"))  # Valid

try:
    validate_password("short1")        # Too short
except ValueError as e:
    print("Error:", e)

try:
    validate_password("nodigitshere")  # No digit
except ValueError as e:
    print("Error:", e)
```

:::expected_output
Password is valid
Error: Password must be at least 8 characters
Error: Password must contain at least one digit
:::

:::hint Check for Digit
Use `any(char.isdigit() for char in password)` to check if any character is a digit.
:::

:::answer Reveal answer
```python
def validate_password(password):
    # Check length and digit requirement
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    return "Password is valid"

# Test
print(validate_password("secret123"))  # Valid

try:
    validate_password("short1")        # Too short
except ValueError as e:
    print("Error:", e)

try:
    validate_password("nodigitshere")  # No digit
except ValueError as e:
    print("Error:", e)
```
:::

## Exercise 5: Build a Validator Function

Create a function `validate_product` that validates product data with multiple checks:

```python live
def validate_product(name, price, quantity):
    """
    Validate product data.
    - name must be non-empty string
    - price must be positive number
    - quantity must be non-negative integer
    """
    # Add all validations
    pass
    return {"name": name, "price": price, "quantity": quantity}

# Test valid product
print(validate_product("Widget", 9.99, 100))

# Test invalid products
tests = [
    ("", 9.99, 100, "empty name"),
    ("Widget", -5, 100, "negative price"),
    ("Widget", 9.99, -10, "negative quantity"),
    ("Widget", 9.99, 3.5, "non-integer quantity"),
]

for name, price, qty, description in tests:
    try:
        validate_product(name, price, qty)
    except (ValueError, TypeError) as e:
        print(description + ":", e)
```

:::expected_output
{'name': 'Widget', 'price': 9.99, 'quantity': 100}
empty name: Name must be a non-empty string
negative price: Price must be positive
negative quantity: Quantity must be non-negative
non-integer quantity: Quantity must be an integer
:::

:::hint Stuck?
Validate each field separately. Check if name is empty, if price <= 0, if quantity < 0, and if quantity is an integer using `isinstance(quantity, int)`.
:::

:::answer Reveal answer
```python
def validate_product(name, price, quantity):
    """
    Validate product data.
    - name must be non-empty string
    - price must be positive number
    - quantity must be non-negative integer
    """
    # Add all validations
    if not isinstance(name, str) or len(name) == 0:
        raise ValueError("Name must be a non-empty string")
    if price <= 0:
        raise ValueError("Price must be positive")
    if not isinstance(quantity, int):
        raise TypeError("Quantity must be an integer")
    if quantity < 0:
        raise ValueError("Quantity must be non-negative")
    return {"name": name, "price": price, "quantity": quantity}

# Test valid product
print(validate_product("Widget", 9.99, 100))

# Test invalid products
tests = [
    ("", 9.99, 100, "empty name"),
    ("Widget", -5, 100, "negative price"),
    ("Widget", 9.99, -10, "negative quantity"),
    ("Widget", 9.99, 3.5, "non-integer quantity"),
]

for name, price, qty, description in tests:
    try:
        validate_product(name, price, qty)
    except (ValueError, TypeError) as e:
        print(description + ":", e)
```
:::

