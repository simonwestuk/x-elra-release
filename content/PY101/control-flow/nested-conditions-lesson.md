---
title: "Nested Conditions"
slug: nested-conditions-lesson
description: "Learn to structure complex decision logic with nested if statements"
course_id: PY101
module: control-flow
module_order: 2
topic: nested-conditions
topic_order: 6
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - if-statements-lesson
  - else-elif-lesson
skills:
  - control-flow
  - nested-conditions
outcomes:
  - "Write nested if statements"
  - "Understand indentation levels"
  - "Choose between nesting and logical operators"
capstone_relevance: "Structure complex menu navigation and validation hierarchies"
---

## Introduction

Sometimes you need to check one condition, and then check another condition only if the first was True. This is called nesting - putting an if statement inside another if statement.

## Basic Nested If

```python live
has_account = True
is_verified = True

if has_account:
    print("Account found")
    if is_verified:
        print("Account verified - access granted")
```

:::expected_output
Account found
Account verified - access granted
:::

## Multiple Nesting Levels

```python live
age = 25
has_license = True
has_insurance = True

if age >= 18:
    print("Old enough to drive")
    if has_license:
        print("Has valid license")
        if has_insurance:
            print("Fully authorized to drive!")
```

:::expected_output
Old enough to drive
Has valid license
Fully authorized to drive!
:::

## Nested If-Else

```python live
member_type = "premium"
years_member = 3

if member_type == "premium":
    print("Premium member")
    if years_member >= 5:
        print("Loyalty bonus: 20% off")
    else:
        print("Loyalty bonus: 10% off")
else:
    print("Standard member - no loyalty bonus")
```

:::expected_output
Premium member
Loyalty bonus: 10% off
:::

## Practical Example: Login Flow

```python live
username = "alice"
password = "secret123"
is_active = True

if username:
    print("Username provided")
    if password:
        print("Password provided")
        if is_active:
            print("Login successful!")
        else:
            print("Account is deactivated")
    else:
        print("Password required")
else:
    print("Username required")
```

:::expected_output
Username provided
Password provided
Login successful!
:::

## Nested vs Logical Operators

Sometimes nesting is clearer, sometimes combining conditions is better:

```python live
age = 25
has_id = True

# Nested approach
if age >= 21:
    if has_id:
        print("Can purchase (nested)")

# Combined approach
if age >= 21 and has_id:
    print("Can purchase (combined)")
```

:::expected_output
Can purchase (nested)
Can purchase (combined)
:::

Choose based on readability and whether you need different actions at each level.

## When to Use Nesting

Use nesting when:
- You need different messages at each check level
- The second check only makes sense if the first passes
- You have different else actions at each level

```python live
balance = 150
amount = 100

if amount > 0:
    # Only check balance if amount is valid
    if balance >= amount:
        balance -= amount
        print(f"Withdrawn ${amount}")
    else:
        print("Insufficient funds")
else:
    print("Invalid amount")
```

:::expected_output
Withdrawn $100
:::

## Key Points

- Nested ifs go inside other if blocks
- Each level adds one more indent
- Use nesting when checks depend on previous checks
- Consider logical operators for simpler cases
- Keep nesting shallow (2-3 levels max) for readability

:::hint Common Mistake
Incorrect indentation in nested blocks. Each nested if needs its own indentation level. Python will error if indentation is inconsistent.
:::
