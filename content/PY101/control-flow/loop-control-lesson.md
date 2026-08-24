---
title: "Loop Control: break and continue"
slug: loop-control-lesson
description: "Learn to control loop execution with break and continue"
course_id: PY101
module: control-flow
module_order: 2
topic: loop-control
topic_order: 9
type: lesson
difficulty: beginner
estimated_minutes: 10
prerequisites:
  - for-loops-lesson
  - while-loops-lesson
skills:
  - control-flow
  - loop-control
outcomes:
  - "Exit loops early with break"
  - "Skip iterations with continue"
  - "Use else with loops"
capstone_relevance: "Exit menus and skip invalid records efficiently"
---

## Introduction

Sometimes you need more control over loops than just the main condition. `break` exits the loop entirely, while `continue` skips to the next iteration.

## break - Exit the Loop

`break` immediately exits the loop:

```python live
for i in range(10):
    if i == 5:
        print("Found 5, stopping!")
        break
    print(i)

print("Loop ended")
```

:::expected_output
0
1
2
3
4
Found 5, stopping!
Loop ended
:::

## Try It: Search with break

```python live
names = ["Alice", "Bob", "Charlie", "Diana"]
search = "Charlie"

for name in names:
    print(f"Checking {name}...")
    if name == search:
        print(f"Found {search}!")
        break
```

:::expected_output
Checking Alice...
Checking Bob...
Checking Charlie...
Found Charlie!
:::

## continue - Skip This Iteration

`continue` skips the rest of the current iteration:

```python live
for i in range(6):
    if i == 3:
        print("Skipping 3")
        continue
    print(f"Number: {i}")
```

:::expected_output
Number: 0
Number: 1
Number: 2
Skipping 3
Number: 4
Number: 5
:::

## Practical Example: Skip Invalid Data

```python live
values = [10, -5, 8, -2, 15, 0, 7]
total = 0

for value in values:
    if value <= 0:
        print(f"Skipping invalid value: {value}")
        continue
    total = total + value
    print(f"Added {value}, total: {total}")

print(f"\nFinal total: {total}")
```

:::expected_output
Added 10, total: 10
Skipping invalid value: -5
Added 8, total: 18
Skipping invalid value: -2
Added 15, total: 33
Skipping invalid value: 0
Added 7, total: 40

Final total: 40
:::

## break in While Loops

```python live
while True:
    command = input("Enter command (quit to exit): ")
    if command == "quit":
        print("Goodbye!")
        break
    print(f"Executing: {command}")
```

## continue in While Loops

```python live
count = 0
while count < 5:
    count = count + 1
    if count == 3:
        print("Skipping 3")
        continue
    print(f"Count: {count}")
```

:::expected_output
Count: 1
Count: 2
Skipping 3
Count: 4
Count: 5
:::

## Loop else Clause

Python loops can have an `else` that runs if the loop completes without `break`:

```python live
numbers = [1, 3, 5, 7, 9]

for num in numbers:
    if num == 4:
        print("Found 4!")
        break
else:
    print("4 not found in list")
```

:::expected_output
4 not found in list
:::

## When to Use Each

| Use `break` when... | Use `continue` when... |
|---------------------|------------------------|
| You found what you need | Item is invalid/skip-worthy |
| Error occurred | Special case to ignore |
| User wants to quit | Don't need to process this one |

## Key Points

- `break` exits the entire loop immediately
- `continue` skips to the next iteration
- Both work in for and while loops
- `else` on loops runs if no `break` occurred
- Use sparingly for clearer code

:::hint Common Mistake
Putting code after `break` or `continue` in the same if block - it won't run. These statements immediately change the loop flow.
:::
