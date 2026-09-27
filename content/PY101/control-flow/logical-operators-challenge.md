---
title: "Challenge: Access Control System"
slug: logical-operators-challenge
description: "Build an access control system with multiple rules"
course_id: PY101
module: control-flow
module_order: 2
topic: logical-operators
topic_order: 5
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - logical-operators-lesson
  - logical-operators-practice
skills:
  - control-flow
  - logic
outcomes:
  - "Design complex access rules"
  - "Combine multiple logical conditions"
  - "Provide clear feedback on rule violations"
capstone_relevance: "Implement authorization rules in your application"
---

## The Challenge

Create an access control system for a secure building.

### Access Rules

Access is granted if ANY of these conditions are met:
1. User is an employee AND has valid badge AND current time is work hours (9-17)
2. User is a visitor AND is escorted AND has signed in
3. User is security personnel (always allowed)

Display which rule granted access, or list all failed conditions.

### Test Data

```python
is_employee = True
has_badge = True
hour = 14  # 24-hour format
is_visitor = False
is_escorted = False
signed_in = False
is_security = False
```

### Example Output (Access Granted)

```
=== Access Control Check ===

Checking credentials...
- Employee with badge during work hours: PASS

ACCESS GRANTED via: Employee access
```

### Example Output (Access Denied)

```
=== Access Control Check ===

Checking credentials...
- Employee with badge during work hours: FAIL (outside hours)
- Visitor with escort and sign-in: FAIL (not a visitor)
- Security personnel: FAIL (not security)

ACCESS DENIED
```

## Your Solution

```python live
# User credentials
is_employee = True
has_badge = True
hour = 14
is_visitor = False
is_escorted = False
signed_in = False
is_security = False

# Check access rules




```

:::expected_output
=== Access Control Check ===

Checking credentials...
- Employee with badge during work hours: PASS

ACCESS GRANTED via: Employee access
:::

:::hint Approach
Define each access rule using logical operators. Check each rule and track which ones pass or fail.
:::

:::hint Structure
Create boolean variables for each rule check, then use those to determine overall access and provide feedback.
:::

:::answer Reveal full solution
```python
# User credentials
is_employee = True
has_badge = True
hour = 14
is_visitor = False
is_escorted = False
signed_in = False
is_security = False

# Check access rules
print("=== Access Control Check ===")
print()
print("Checking credentials...")

work_hours = 9 <= hour <= 17
employee_access = is_employee and has_badge and work_hours
visitor_access = is_visitor and is_escorted and signed_in
security_access = is_security

access_granted = False
access_method = ""

if employee_access:
    print("- Employee with badge during work hours: PASS")
    access_granted = True
    access_method = "Employee access"
else:
    if is_employee:
        if not has_badge:
            print("- Employee with badge during work hours: FAIL (no badge)")
        elif not work_hours:
            print("- Employee with badge during work hours: FAIL (outside hours)")
    else:
        print("- Employee with badge during work hours: FAIL (not an employee)")

if not access_granted and visitor_access:
    print("- Visitor with escort and sign-in: PASS")
    access_granted = True
    access_method = "Visitor access"
elif not access_granted:
    if not is_visitor:
        print("- Visitor with escort and sign-in: FAIL (not a visitor)")
    elif not is_escorted:
        print("- Visitor with escort and sign-in: FAIL (no escort)")
    elif not signed_in:
        print("- Visitor with escort and sign-in: FAIL (not signed in)")

if not access_granted and security_access:
    print("- Security personnel: PASS")
    access_granted = True
    access_method = "Security access"
elif not access_granted:
    print("- Security personnel: FAIL (not security)")

print()
if access_granted:
    print(f"ACCESS GRANTED via: {access_method}")
else:
    print("ACCESS DENIED")
```
:::
