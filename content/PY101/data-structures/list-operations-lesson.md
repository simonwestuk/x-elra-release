---
title: "List Operations"
slug: list-operations-lesson
description: "Learn common list methods for sorting, copying, and combining"
course_id: PY101
module: data-structures
module_order: 3
topic: list-operations
topic_order: 2
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - lists-lesson
skills:
  - data-structures
  - list-operations
outcomes:
  - "Sort lists in ascending and descending order"
  - "Reverse and copy lists"
  - "Combine and compare lists"
capstone_relevance: "Sort and organize your records for display"
---

## Introduction

Python lists come with powerful built-in methods for sorting, reversing, copying, and combining data. These operations are essential for organizing and presenting your data.

## Sorting Lists

`sort()` modifies the list in place:

```python live
numbers = [5, 2, 8, 1, 9]
print("Before:", numbers)

numbers.sort()
print("After sort:", numbers)

numbers.sort(reverse=True)
print("Descending:", numbers)
```

:::expected_output
Before: [5, 2, 8, 1, 9]
After sort: [1, 2, 5, 8, 9]
Descending: [9, 8, 5, 2, 1]
:::

## sorted() Function

Creates a new sorted list (original unchanged):

```python live
original = [5, 2, 8, 1, 9]
ascending = sorted(original)
descending = sorted(original, reverse=True)

print("Original:", original)
print("Ascending:", ascending)
print("Descending:", descending)
```

:::expected_output
Original: [5, 2, 8, 1, 9]
Ascending: [1, 2, 5, 8, 9]
Descending: [9, 8, 5, 2, 1]
:::

## Sorting Strings

```python live
names = ["Charlie", "Alice", "Bob", "Diana"]
names.sort()
print("Alphabetical:", names)

# Case-insensitive
mixed = ["banana", "Apple", "cherry"]
mixed.sort(key=str.lower)
print("Case-insensitive:", mixed)
```

:::expected_output
Alphabetical: ['Alice', 'Bob', 'Charlie', 'Diana']
Case-insensitive: ['Apple', 'banana', 'cherry']
:::

## Reversing Lists

```python live
items = [1, 2, 3, 4, 5]
print("Before:", items)

items.reverse()
print("Reversed:", items)

# Or create new reversed list
original = [1, 2, 3]
backwards = list(reversed(original))
print("New reversed:", backwards)
```

:::expected_output
Before: [1, 2, 3, 4, 5]
Reversed: [5, 4, 3, 2, 1]
New reversed: [3, 2, 1]
:::

## Copying Lists

```python live
# Simple copy
original = [1, 2, 3]
copy1 = original.copy()
copy2 = original[:]
copy3 = list(original)

# Modify copy, original unchanged
copy1.append(99)
print("Original:", original)
print("Modified copy:", copy1)
```

:::expected_output
Original: [1, 2, 3]
Modified copy: [1, 2, 3, 99]
:::

## Warning: Assignment vs Copy

```python live
# This creates a reference, not a copy!
list_a = [1, 2, 3]
list_b = list_a  # Both point to same list

list_b.append(4)
print("list_a:", list_a)  # Also changed!
print("list_b:", list_b)

# Use .copy() for independent copy
list_c = [1, 2, 3]
list_d = list_c.copy()
list_d.append(4)
print("list_c:", list_c)  # Unchanged
print("list_d:", list_d)
```

:::expected_output
list_a: [1, 2, 3, 4]
list_b: [1, 2, 3, 4]
list_c: [1, 2, 3]
list_d: [1, 2, 3, 4]
:::

## Combining Lists

```python live
list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Concatenation (new list)
combined = list1 + list2
print("Combined:", combined)

# Extend (modifies first list)
list1.extend(list2)
print("Extended list1:", list1)
```

:::expected_output
Combined: [1, 2, 3, 4, 5, 6]
Extended list1: [1, 2, 3, 4, 5, 6]
:::

## Finding Min and Max

```python live
scores = [85, 92, 78, 95, 88]

print(f"Highest: {max(scores)}")
print(f"Lowest: {min(scores)}")
print(f"Sum: {sum(scores)}")
print(f"Average: {sum(scores) / len(scores):.1f}")
```

:::expected_output
Highest: 95
Lowest: 78
Sum: 438
Average: 87.6
:::

## Key Points

- `sort()` modifies in place, `sorted()` returns new list
- Use `reverse=True` for descending order
- Always use `.copy()` to avoid shared references
- `+` combines lists, `extend()` adds to existing list
- `min()`, `max()`, `sum()` work on numeric lists

:::hint Common Mistake
Assigning a list creates a reference, not a copy. Changes to one affect both. Use `.copy()` for an independent copy.
:::
