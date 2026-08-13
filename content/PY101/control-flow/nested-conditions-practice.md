---
title: "Practice: Nested Conditions"
slug: nested-conditions-practice
description: "Practice structuring complex logic with nested if statements"
course_id: PY101
module: control-flow
module_order: 2
topic: nested-conditions
topic_order: 6
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - nested-conditions-lesson
skills:
  - control-flow
  - nested-conditions
outcomes:
  - "Structure nested conditions correctly"
  - "Handle multiple decision levels"
  - "Provide appropriate feedback at each level"
capstone_relevance: "Build hierarchical menus and validation in your application"
---

## Exercise 1: Two-Level Check

If user exists, check if they're verified:

```python live
user_exists = True
is_verified = False
# Nested check with appropriate messages


```

:::expected_output
Please verify your account.
:::

:::hint Stuck?
First if checks user_exists, nested if checks is_verified. Print different messages at each level.
:::

:::answer Reveal answer
```python
user_exists = True
is_verified = False
if user_exists:
    if is_verified:
        print("Welcome! You are verified.")
    else:
        print("Please verify your account.")
else:
    print("User not found.")
```
:::

## Exercise 2: Withdrawal Logic

Check if amount > 0, then check if balance is sufficient:

```python live
balance = 100
amount = 75
# Only process if amount is valid and balance sufficient


```

:::expected_output
Withdrawal successful. New balance: 25
:::

:::hint Stuck?
Outer if checks `amount > 0`, inner if checks `balance >= amount`.
:::

:::answer Reveal answer
```python
balance = 100
amount = 75
if amount > 0:
    if balance >= amount:
        balance = balance - amount
        print(f"Withdrawal successful. New balance: {balance}")
    else:
        print("Insufficient balance.")
else:
    print("Invalid amount.")
```
:::

## Exercise 3: Age Restriction

If age >= 18, check if they have ID. Print appropriate message at each stage:

```python live
age = 22
has_id = True
# Check age first, then ID


```

:::expected_output
Age requirement met.
ID verified. Access granted.
:::

:::hint Stuck?
First check age, print age status, then check ID inside and print ID status.
:::

:::answer Reveal answer
```python
age = 22
has_id = True
if age >= 18:
    print("Age requirement met.")
    if has_id:
        print("ID verified. Access granted.")
    else:
        print("Please provide your ID.")
else:
    print("You must be 18 or older.")
```
:::

## Exercise 4: Shipping Eligibility

Check if item is in stock, then check if it ships to customer's country:

```python live
in_stock = True
ships_to_country = False
# Nested check for shipping eligibility


```

:::expected_output
Sorry, we don't ship to your country.
:::

:::hint Stuck?
Outer: in_stock check. Inner: ships_to_country check. Different messages for each failure.
:::

:::answer Reveal answer
```python
in_stock = True
ships_to_country = False
if in_stock:
    if ships_to_country:
        print("Order can be placed!")
    else:
        print("Sorry, we don't ship to your country.")
else:
    print("Item is out of stock.")
```
:::

## Exercise 5: Login with Role

Check credentials, then check user role for admin access:

```python live
valid_credentials = True
role = "admin"
# Check login, then check if admin


```

:::expected_output
Login successful.
Welcome, Admin! You have full access.
:::

:::hint Stuck?
First verify credentials, then check if role equals "admin" for special admin message.
:::

:::answer Reveal answer
```python
valid_credentials = True
role = "admin"
if valid_credentials:
    print("Login successful.")
    if role == "admin":
        print("Welcome, Admin! You have full access.")
    else:
        print("Welcome! You have standard access.")
else:
    print("Invalid credentials.")
```
:::
