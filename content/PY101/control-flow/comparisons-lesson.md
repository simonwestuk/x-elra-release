---
title: "Comparison Operators"
slug: comparisons-lesson
description: "Learn to compare values using Python's comparison operators"
course_id: PY101
module: control-flow
module_order: 2
topic: comparisons
topic_order: 1
type: lesson
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - variables-types-lesson
skills:
  - control-flow
  - comparisons
outcomes:
  - "Use all six comparison operators"
  - "Compare numbers and strings"
  - "Understand comparison results (True/False)"
capstone_relevance: "Compare record values for filtering and validation"
---

## Introduction

Comparison operators let you compare two values. They always return a boolean: `True` or `False`. These are the foundation of making decisions in your programs.

## The Six Comparison Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `<` | Less than | `3 < 5` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<=` | Less than or equal | `5 <= 5` | `True` |
| `>=` | Greater than or equal | `5 >= 3` | `True` |

## Try It: Basic Comparisons

```python live
print(10 == 10)   # Equal?
print(10 != 5)    # Not equal?
print(3 < 7)      # Less than?
print(8 > 4)      # Greater than?
```

:::expected_output
True
True
True
True
:::

## Comparing Variables

```python live
age = 25
minimum_age = 18

print(age >= minimum_age)
print(age == minimum_age)
print(age < minimum_age)
```

:::expected_output
True
False
False
:::

## Equal vs Assignment

Be careful: `==` compares, `=` assigns!

```python live
x = 5        # Assignment (x becomes 5)
print(x == 5)  # Comparison (is x equal to 5?)
print(x == 3)  # Comparison (is x equal to 3?)
```

:::expected_output
True
False
:::

## Comparing Strings

Strings compare alphabetically (case-sensitive):

```python live
print("apple" == "apple")   # True
print("Apple" == "apple")   # False (different case!)
print("apple" < "banana")   # True (a comes before b)
print("a" < "b")           # True
```

:::expected_output
True
False
True
True
:::

## Case-Insensitive Comparison

Convert to same case first:

```python live
name1 = "Alice"
name2 = "ALICE"

print(name1 == name2)                    # False
print(name1.lower() == name2.lower())   # True
```

:::expected_output
False
True
:::

## Comparing Different Types

Be careful comparing different types:

```python live
print(5 == 5.0)       # True (int and float can compare)
print("5" == 5)       # False (string and int are different)
print(5 == "5")       # False
```

:::expected_output
True
False
False
:::

## Storing Comparison Results

Comparisons return booleans that you can store:

```python live
score = 85
passing_grade = 70

is_passing = score >= passing_grade
print(f"Score: {score}")
print(f"Passing: {is_passing}")
```

:::expected_output
Score: 85
Passing: True
:::

## Chained Comparisons

Python allows chained comparisons:

```python live
age = 25
print(18 <= age <= 65)  # True (age is between 18 and 65)

temperature = 72
print(60 < temperature < 80)  # True (comfortable range)
```

:::expected_output
True
True
:::

## Key Points

- Six operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Comparisons always return `True` or `False`
- `==` compares, `=` assigns (don't confuse them!)
- String comparisons are case-sensitive
- Comparison results can be stored in variables

:::hint Common Mistake
Using `=` instead of `==` for comparison. `if x = 5` is wrong, use `if x == 5`.
:::
