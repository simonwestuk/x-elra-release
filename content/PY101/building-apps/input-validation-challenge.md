---
title: "Challenge: Build a Form Validation System"
slug: input-validation-challenge
description: "Create a complete form validation system"
course_id: PY101
module: building-apps
module_order: 7
topic: input-validation
topic_order: 3
type: challenge
difficulty: beginner
estimated_minutes: 25
prerequisites:
  - input-validation-practice
skills:
  - validation
  - error-handling
outcomes:
  - "Build comprehensive validation"
  - "Create reusable validators"
  - "Handle complex validation rules"
capstone_relevance: "Form validation is core to CRUD applications"
---

## Challenge: Order Form Validator

Build a complete validation system for an e-commerce order form.

### Order Data Structure

```python
order = {
    "customer": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "555-123-4567"
    },
    "items": [
        {"product_id": "P001", "quantity": 2, "price": 29.99},
        {"product_id": "P002", "quantity": 1, "price": 49.99}
    ],
    "shipping": {
        "address": "123 Main St",
        "city": "New York",
        "zip": "10001"
    },
    "payment": {
        "method": "credit_card",
        "card_last4": "1234"
    }
}
```

### Validation Rules

**Customer:**
- name: required, 2-100 characters
- email: required, must contain @ and .
- phone: optional, if provided must be 10+ characters

**Items:**
- Must have at least 1 item
- Each item: product_id (required), quantity (int > 0), price (number > 0)

**Shipping:**
- address: required, 5-200 characters
- city: required, 2-100 characters
- zip: required, 5-10 characters, only digits/letters/hyphens

**Payment:**
- method: required, one of ["credit_card", "debit_card", "paypal"]
- card_last4: required if method is card, must be 4 digits

### Your Solution

```python live
# ============ VALIDATORS ============
def validate_customer(customer):
    """Validate customer data."""
    errors = []
    # Your code here
    return errors

def validate_items(items):
    """Validate order items."""
    errors = []
    # Your code here
    return errors

def validate_shipping(shipping):
    """Validate shipping data."""
    errors = []
    # Your code here
    return errors

def validate_payment(payment):
    """Validate payment data."""
    errors = []
    # Your code here
    return errors

def validate_order(order):
    """Validate complete order."""
    all_errors = {
        "customer": [],
        "items": [],
        "shipping": [],
        "payment": []
    }

    # Validate each section
    if "customer" in order:
        all_errors["customer"] = validate_customer(order["customer"])
    else:
        all_errors["customer"] = ["Customer information is required"]

    if "items" in order:
        all_errors["items"] = validate_items(order["items"])
    else:
        all_errors["items"] = ["Order items are required"]

    if "shipping" in order:
        all_errors["shipping"] = validate_shipping(order["shipping"])
    else:
        all_errors["shipping"] = ["Shipping information is required"]

    if "payment" in order:
        all_errors["payment"] = validate_payment(order["payment"])
    else:
        all_errors["payment"] = ["Payment information is required"]

    # Check if any errors
    has_errors = any(errors for errors in all_errors.values())
    return not has_errors, all_errors

def display_validation_result(is_valid, errors):
    """Display validation results."""
    if is_valid:
        print("✓ Order is valid!")
    else:
        print("✗ Order has errors:")
        for section, section_errors in errors.items():
            if section_errors:
                print("\n  " + section.upper() + ":")
                for error in section_errors:
                    print("    - " + error)


# ============ TEST ============
# Valid order
valid_order = {
    "customer": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "555-123-4567"
    },
    "items": [
        {"product_id": "P001", "quantity": 2, "price": 29.99}
    ],
    "shipping": {
        "address": "123 Main Street",
        "city": "New York",
        "zip": "10001"
    },
    "payment": {
        "method": "credit_card",
        "card_last4": "1234"
    }
}

print("=== Testing Valid Order ===")
is_valid, errors = validate_order(valid_order)
display_validation_result(is_valid, errors)

# Invalid order
invalid_order = {
    "customer": {
        "name": "J",           # Too short
        "email": "invalid",    # No @ or .
        "phone": "123"         # Too short
    },
    "items": [],               # Empty
    "shipping": {
        "address": "123",      # Too short
        "city": "X",           # Too short
        "zip": "!!!"           # Invalid characters
    },
    "payment": {
        "method": "bitcoin",   # Invalid method
        "card_last4": "12"     # Not 4 digits
    }
}

print("\n=== Testing Invalid Order ===")
is_valid, errors = validate_order(invalid_order)
display_validation_result(is_valid, errors)
```

:::expected_output
=== Testing Valid Order ===
✓ Order is valid!

=== Testing Invalid Order ===
✗ Order has errors:

  CUSTOMER:
    - Name must be at least 2 characters
    - Email must contain @ and .
    - Phone must be at least 10 characters

  ITEMS:
    - Order must have at least one item

  SHIPPING:
    - Address must be at least 5 characters
    - City must be at least 2 characters
    - Zip must be 5-10 characters

  PAYMENT:
    - Payment method must be credit_card, debit_card, or paypal
:::

### Expected Output

```
=== Testing Valid Order ===
✓ Order is valid!

=== Testing Invalid Order ===
✗ Order has errors:

  CUSTOMER:
    - Name must be at least 2 characters
    - Email must contain @ and .
    - Phone must be at least 10 characters

  ITEMS:
    - Order must have at least one item

  SHIPPING:
    - Address must be at least 5 characters
    - City must be at least 2 characters
    - Zip contains invalid characters

  PAYMENT:
    - Payment method must be credit_card, debit_card, or paypal
    - Card last 4 digits must be exactly 4 digits
```

:::hint Customer Validation
Check if keys exist, then validate each field's length and format.
:::

:::hint Items Validation
Check if list is empty first. Then loop through items validating each.
:::

:::hint Zip Validation
Use `all(c.isalnum() or c == '-' for c in zip_code)` to check characters.
:::

:::hint Payment Validation
Check method is in valid list. If card method, validate card_last4 is 4 digits.
:::

:::answer Reveal full solution
```python
# ============ VALIDATORS ============
def validate_customer(customer):
    """Validate customer data."""
    errors = []
    # Validate name
    name = customer.get("name", "")
    if len(name) < 2:
        errors.append("Name must be at least 2 characters")
    elif len(name) > 100:
        errors.append("Name must be at most 100 characters")

    # Validate email
    email = customer.get("email", "")
    if "@" not in email or "." not in email:
        errors.append("Email must contain @ and .")

    # Validate phone (optional)
    phone = customer.get("phone", "")
    if phone and len(phone) < 10:
        errors.append("Phone must be at least 10 characters")

    return errors

def validate_items(items):
    """Validate order items."""
    errors = []
    if not items:
        errors.append("Order must have at least one item")
        return errors

    for i, item in enumerate(items):
        if not item.get("product_id"):
            errors.append("Item " + str(i + 1) + ": product_id is required")
        if not isinstance(item.get("quantity"), int) or item.get("quantity", 0) <= 0:
            errors.append("Item " + str(i + 1) + ": quantity must be a positive integer")
        if not isinstance(item.get("price"), (int, float)) or item.get("price", 0) <= 0:
            errors.append("Item " + str(i + 1) + ": price must be a positive number")

    return errors

def validate_shipping(shipping):
    """Validate shipping data."""
    errors = []
    address = shipping.get("address", "")
    if len(address) < 5:
        errors.append("Address must be at least 5 characters")
    elif len(address) > 200:
        errors.append("Address must be at most 200 characters")

    city = shipping.get("city", "")
    if len(city) < 2:
        errors.append("City must be at least 2 characters")
    elif len(city) > 100:
        errors.append("City must be at most 100 characters")

    zip_code = shipping.get("zip", "")
    if len(zip_code) < 5 or len(zip_code) > 10:
        errors.append("Zip must be 5-10 characters")
    elif not all(c.isalnum() or c == '-' for c in zip_code):
        errors.append("Zip contains invalid characters")

    return errors

def validate_payment(payment):
    """Validate payment data."""
    errors = []
    valid_methods = ["credit_card", "debit_card", "paypal"]
    method = payment.get("method", "")

    if method not in valid_methods:
        errors.append("Payment method must be credit_card, debit_card, or paypal")

    if method in ["credit_card", "debit_card"]:
        card_last4 = payment.get("card_last4", "")
        if len(card_last4) != 4 or not card_last4.isdigit():
            errors.append("Card last 4 digits must be exactly 4 digits")

    return errors

def validate_order(order):
    """Validate complete order."""
    all_errors = {
        "customer": [],
        "items": [],
        "shipping": [],
        "payment": []
    }

    # Validate each section
    if "customer" in order:
        all_errors["customer"] = validate_customer(order["customer"])
    else:
        all_errors["customer"] = ["Customer information is required"]

    if "items" in order:
        all_errors["items"] = validate_items(order["items"])
    else:
        all_errors["items"] = ["Order items are required"]

    if "shipping" in order:
        all_errors["shipping"] = validate_shipping(order["shipping"])
    else:
        all_errors["shipping"] = ["Shipping information is required"]

    if "payment" in order:
        all_errors["payment"] = validate_payment(order["payment"])
    else:
        all_errors["payment"] = ["Payment information is required"]

    # Check if any errors
    has_errors = any(errors for errors in all_errors.values())
    return not has_errors, all_errors

def display_validation_result(is_valid, errors):
    """Display validation results."""
    if is_valid:
        print("✓ Order is valid!")
    else:
        print("✗ Order has errors:")
        for section, section_errors in errors.items():
            if section_errors:
                print("\n  " + section.upper() + ":")
                for error in section_errors:
                    print("    - " + error)


# ============ TEST ============
# Valid order
valid_order = {
    "customer": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "555-123-4567"
    },
    "items": [
        {"product_id": "P001", "quantity": 2, "price": 29.99}
    ],
    "shipping": {
        "address": "123 Main Street",
        "city": "New York",
        "zip": "10001"
    },
    "payment": {
        "method": "credit_card",
        "card_last4": "1234"
    }
}

print("=== Testing Valid Order ===")
is_valid, errors = validate_order(valid_order)
display_validation_result(is_valid, errors)

# Invalid order
invalid_order = {
    "customer": {
        "name": "J",           # Too short
        "email": "invalid",    # No @ or .
        "phone": "123"         # Too short
    },
    "items": [],               # Empty
    "shipping": {
        "address": "123",      # Too short
        "city": "X",           # Too short
        "zip": "!!!"           # Invalid characters
    },
    "payment": {
        "method": "bitcoin",   # Invalid method
        "card_last4": "12"     # Not 4 digits
    }
}

print("\n=== Testing Invalid Order ===")
is_valid, errors = validate_order(invalid_order)
display_validation_result(is_valid, errors)
```
:::

