---
title: "Logical Operators"
slug: logical-operators-lesson
description: "Combine conditions with and, or, and not"
course_id: PY101
module: control-flow
module_order: 2
topic: logical-operators
topic_order: 5
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - comparisons-lesson
  - if-statements-lesson
skills:
  - control-flow
  - logic
outcomes:
  - "Combine conditions with and"
  - "Provide alternatives with or"
  - "Negate conditions with not"
capstone_relevance: "Build complex validation rules and search filters"
---

## Introduction

Logical operators let you combine multiple conditions. Instead of nested if statements, you can express complex logic clearly on a single line.

## The Three Logical Operators

| Operator | Meaning | True when... |
|----------|---------|--------------|
| `and` | Both | Both conditions are True |
| `or` | Either | At least one is True |
| `not` | Negation | Condition is False |

## The `and` Operator

Both conditions must be True:

```python live
age = 25
has_license = True

if age >= 18 and has_license:
    print("You can drive")

# Truth table
print(True and True)   # True
print(True and False)  # False
print(False and True)  # False
print(False and False) # False
```

:::expected_output
You can drive
True
False
False
False
:::

## The `or` Operator

At least one condition must be True:

```python live
is_student = True
is_senior = False

if is_student or is_senior:
    print("You get a discount!")

# Truth table
print(True or True)   # True
print(True or False)  # True
print(False or True)  # True
print(False or False) # False
```

:::expected_output
You get a discount!
True
True
True
False
:::

## The `not` Operator

Flips True to False and vice versa:

```python live
logged_in = False

if not logged_in:
    print("Please log in")

print(not True)   # False
print(not False)  # True
```

:::expected_output
Please log in
False
True
:::

## Combining Multiple Conditions

```python live
age = 20
has_ticket = True
is_vip = False

# Can enter if: (adult with ticket) OR VIP
if (age >= 18 and has_ticket) or is_vip:
    print("Welcome to the event!")
```

:::expected_output
Welcome to the event!
:::

## Practical Example: Form Validation

```python live
username = "alice"
password = "secret123"
agreed_to_terms = True

# All three must be valid
if username and password and agreed_to_terms:
    print("Form submitted successfully!")
else:
    print("Please complete all fields")
```

:::expected_output
Form submitted successfully!
:::

## Range Checking

```python live
score = 85

# Check if score is in valid range
if score >= 0 and score <= 100:
    print("Valid score")

# Same thing using chained comparison
if 0 <= score <= 100:
    print("Also valid!")
```

:::expected_output
Valid score
Also valid!
:::

## Checking Against Multiple Values

```python live
day = "Saturday"

if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")

# Alternative with 'in'
if day in ["Saturday", "Sunday"]:
    print("Weekend (using 'in')!")
```

:::expected_output
It's the weekend!
Weekend (using 'in')!
:::

## Short-Circuit Evaluation

Python stops evaluating as soon as it knows the result:

```python live
# With 'and': stops at first False
value = 0
if value != 0 and 10/value > 1:  # Second part never runs
    print("OK")

# With 'or': stops at first True
name = "Alice"
if name or "Default":  # Second part skipped if name is truthy
    print(f"Hello, {name}")
```

:::expected_output
Hello, Alice
:::

## Key Points

- `and`: Both must be True
- `or`: At least one must be True
- `not`: Flips the boolean
- Use parentheses for clarity with complex conditions
- Python uses short-circuit evaluation

:::hint Common Mistake
Using `&` and `|` instead of `and` and `or`. Those are bitwise operators. For boolean logic, always use the words.
:::
