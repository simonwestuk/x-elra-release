---
title: "Challenge: Pagination Display"
slug: slicing-challenge
description: "Build a pagination system using slicing"
course_id: PY101
module: data-structures
module_order: 3
topic: slicing
topic_order: 3
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - slicing-lesson
  - slicing-practice
skills:
  - data-structures
  - slicing
outcomes:
  - "Implement pagination logic"
  - "Calculate slice boundaries"
  - "Display paginated data"
capstone_relevance: "Paginate record displays in your application"
---

## The Challenge

Create a pagination system that displays items in pages.

### Requirements

Given a list of 20 items and a page size of 5:
1. Display page 1 (items 1-5)
2. Display page 3 (items 11-15)
3. Display the last page
4. Show "Page X of Y" header for each

### Example Output

```
=== Pagination Demo ===

Page 1 of 4:
1. Item 01
2. Item 02
3. Item 03
4. Item 04
5. Item 05

Page 3 of 4:
1. Item 11
2. Item 12
3. Item 13
4. Item 14
5. Item 15

Page 4 of 4 (Last):
1. Item 16
2. Item 17
3. Item 18
4. Item 19
5. Item 20
```

## Your Solution

```python live
# Generate 20 items
items = [f"Item {i:02d}" for i in range(1, 21)]
page_size = 5

print("=== Pagination Demo ===")
print()

# Calculate total pages


# Display page 1


# Display page 3


# Display last page


```

:::expected_output
=== Pagination Demo ===

Page 1 of 4:
1. Item 01
2. Item 02
3. Item 03
4. Item 04
5. Item 05

Page 3 of 4:
1. Item 11
2. Item 12
3. Item 13
4. Item 14
5. Item 15

Page 4 of 4 (Last):
1. Item 16
2. Item 17
3. Item 18
4. Item 19
5. Item 20
:::

:::hint Approach
Calculate start index: (page - 1) * page_size. Calculate end index: start + page_size. Use slicing to get page items.
:::

:::hint Structure
Create a formula for slice indices. Total pages = (len(items) + page_size - 1) // page_size handles partial pages.
:::

:::answer Reveal full solution
```python
# Generate 20 items
items = [f"Item {i:02d}" for i in range(1, 21)]
page_size = 5

print("=== Pagination Demo ===")
print()

# Calculate total pages
total_pages = (len(items) + page_size - 1) // page_size

# Display page 1
page = 1
start = (page - 1) * page_size
end = start + page_size
print(f"Page {page} of {total_pages}:")
for i, item in enumerate(items[start:end], 1):
    print(f"{i}. {item}")
print()

# Display page 3
page = 3
start = (page - 1) * page_size
end = start + page_size
print(f"Page {page} of {total_pages}:")
for i, item in enumerate(items[start:end], 1):
    print(f"{i}. {item}")
print()

# Display last page
page = total_pages
start = (page - 1) * page_size
end = start + page_size
print(f"Page {page} of {total_pages} (Last):")
for i, item in enumerate(items[start:end], 1):
    print(f"{i}. {item}")
```
:::
