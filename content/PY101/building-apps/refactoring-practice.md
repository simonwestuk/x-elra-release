---
title: "Practice: Refactoring Code"
slug: refactoring-practice
description: "Practice improving code quality through refactoring"
course_id: PY101
module: building-apps
module_order: 7
topic: refactoring
topic_order: 5
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - refactoring-lesson
skills:
  - refactoring
  - code-quality
outcomes:
  - "Identify refactoring opportunities"
  - "Apply refactoring techniques"
  - "Write cleaner code"
capstone_relevance: "Clean code is easier to maintain and extend"
---

## Exercise 1: Rename for Clarity

Refactor this code to use meaningful names.

```python live
# BEFORE: Cryptic names
def f(l):
    t = 0
    for i in l:
        t += i
    return t / len(l)

r = f([10, 20, 30, 40, 50])
print(r)

# AFTER: Write a refactored version
def calculate_average(numbers):
    # Your code here
    pass

# Test your refactored version
# result = calculate_average([10, 20, 30, 40, 50])
# print(result)
```

:::expected_output
30.0
:::

:::hint Stuck?
`l` is a list of numbers, `t` is total, `i` is each item. The function calculates average.
:::

:::answer Reveal answer
```python
def calculate_average(numbers):
    total = 0
    for number in numbers:
        total += number
    return total / len(numbers)

# Test your refactored version
result = calculate_average([10, 20, 30, 40, 50])
print(result)
```
:::

## Exercise 2: Extract Functions

Break this long function into smaller, focused functions.

```python live
# BEFORE: One big function
def process_student(name, scores):
    # Calculate average
    total = 0
    for score in scores:
        total += score
    average = total / len(scores) if scores else 0

    # Determine grade
    if average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 60:
        grade = "D"
    else:
        grade = "F"

    # Determine status
    if average >= 70:
        status = "Passing"
    else:
        status = "Needs Improvement"

    # Print report
    print("Student:", name)
    print("Average:", round(average, 2))
    print("Grade:", grade)
    print("Status:", status)

process_student("Alice", [85, 92, 78, 90])

# AFTER: Extract into separate functions
# def calculate_average(scores): ...
# def get_grade(average): ...
# def get_status(average): ...
# def print_student_report(name, average, grade, status): ...
```

:::expected_output
Student: Alice
Average: 86.25
Grade: B
Status: Passing
:::

:::hint Stuck?
Create 4 functions: one for average, one for grade, one for status, one for printing. Then combine in main function.
:::

:::answer Reveal answer
```python
def calculate_average(scores):
    total = 0
    for score in scores:
        total += score
    return total / len(scores) if scores else 0

def get_grade(average):
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"

def get_status(average):
    if average >= 70:
        return "Passing"
    else:
        return "Needs Improvement"

def print_student_report(name, scores):
    average = calculate_average(scores)
    grade = get_grade(average)
    status = get_status(average)
    print("Student:", name)
    print("Average:", round(average, 2))
    print("Grade:", grade)
    print("Status:", status)

print_student_report("Alice", [85, 92, 78, 90])
```
:::

## Exercise 3: Replace Magic Numbers

Replace the magic numbers with named constants.

```python live
# BEFORE: Magic numbers everywhere
def calculate_shipping(weight, distance):
    if weight <= 1:
        base = 5.99
    elif weight <= 5:
        base = 9.99
    elif weight <= 20:
        base = 14.99
    else:
        base = 24.99

    if distance > 500:
        base = base * 1.5

    return round(base, 2)

print(calculate_shipping(3, 600))

# AFTER: Use named constants
# LIGHT_WEIGHT_THRESHOLD = 1
# MEDIUM_WEIGHT_THRESHOLD = 5
# ... etc
```

:::hint Stuck?
Create constants for weight thresholds, price tiers, distance threshold, and the long-distance multiplier.
:::

:::answer Reveal answer
```python
# Named constants
LIGHT_WEIGHT_THRESHOLD = 1
MEDIUM_WEIGHT_THRESHOLD = 5
HEAVY_WEIGHT_THRESHOLD = 20

LIGHT_RATE = 5.99
MEDIUM_RATE = 9.99
HEAVY_RATE = 14.99
EXTRA_HEAVY_RATE = 24.99

LONG_DISTANCE_THRESHOLD = 500
LONG_DISTANCE_MULTIPLIER = 1.5

def calculate_shipping(weight, distance):
    if weight <= LIGHT_WEIGHT_THRESHOLD:
        base = LIGHT_RATE
    elif weight <= MEDIUM_WEIGHT_THRESHOLD:
        base = MEDIUM_RATE
    elif weight <= HEAVY_WEIGHT_THRESHOLD:
        base = HEAVY_RATE
    else:
        base = EXTRA_HEAVY_RATE

    if distance > LONG_DISTANCE_THRESHOLD:
        base = base * LONG_DISTANCE_MULTIPLIER

    return round(base, 2)

print(calculate_shipping(3, 600))
```
:::

## Exercise 4: Simplify Conditionals

Simplify this nested conditional mess.

```python live
# BEFORE: Deeply nested
def get_discount(customer):
    discount = 0
    if customer.get("is_member"):
        if customer.get("years") >= 5:
            if customer.get("total_purchases") > 1000:
                discount = 25
            else:
                discount = 15
        else:
            if customer.get("total_purchases") > 500:
                discount = 10
            else:
                discount = 5
    else:
        if customer.get("total_purchases") > 500:
            discount = 5
    return discount

# Test
customer = {"is_member": True, "years": 6, "total_purchases": 1500}
print("Discount:", get_discount(customer), "%")

# AFTER: Use early returns and simpler logic
def get_discount_better(customer):
    # Your refactored code here
    pass
```

:::expected_output
Discount: 25 %
:::

:::hint Stuck?
Use early returns: check non-member first, then check member conditions. Can use intermediate variables like `is_loyal` for years >= 5.
:::

:::answer Reveal answer
```python
def get_discount_better(customer):
    # Non-members
    if not customer.get("is_member"):
        if customer.get("total_purchases") > 500:
            return 5
        return 0

    # Members
    is_loyal = customer.get("years", 0) >= 5
    high_spender = customer.get("total_purchases", 0) > 1000
    mid_spender = customer.get("total_purchases", 0) > 500

    if is_loyal and high_spender:
        return 25
    if is_loyal:
        return 15
    if mid_spender:
        return 10
    return 5

# Test
customer = {"is_member": True, "years": 6, "total_purchases": 1500}
print("Discount:", get_discount_better(customer), "%")
```
:::

## Exercise 5: Remove Duplication

Identify and remove the duplicated code.

```python live
# BEFORE: Lots of duplication
def create_error_response(message):
    response = {}
    response["status"] = "error"
    response["message"] = message
    response["code"] = 400
    return response

def create_success_response(data):
    response = {}
    response["status"] = "success"
    response["data"] = data
    response["code"] = 200
    return response

def create_not_found_response(resource):
    response = {}
    response["status"] = "error"
    response["message"] = resource + " not found"
    response["code"] = 404
    return response

# AFTER: Create a general response function
def create_response(status, code, **kwargs):
    # Your code here - single function that handles all cases
    pass

# Then create specific helpers that use it
# def error_response(message): return create_response(...)
# def success_response(data): return create_response(...)
# def not_found_response(resource): return create_response(...)
```

:::hint Stuck?
Create one `create_response(status, code, **kwargs)` that builds the base dict and adds any extra kwargs. Then the specific functions call this with their specific values.
:::

:::answer Reveal answer
```python
def create_response(status, code, **kwargs):
    response = {"status": status, "code": code}
    for key, value in kwargs.items():
        response[key] = value
    return response

def error_response(message):
    return create_response("error", 400, message=message)

def success_response(data):
    return create_response("success", 200, data=data)

def not_found_response(resource):
    return create_response("error", 404, message=resource + " not found")

# Test
print(error_response("Invalid input"))
print(success_response({"id": 1, "name": "Alice"}))
print(not_found_response("User"))
```
:::

