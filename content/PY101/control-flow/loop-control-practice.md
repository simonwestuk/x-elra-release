---
title: "Practice: Loop Control"
slug: loop-control-practice
description: "Practice using break and continue in loops"
course_id: PY101
module: control-flow
module_order: 2
topic: loop-control
topic_order: 9
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - loop-control-lesson
skills:
  - control-flow
  - loop-control
outcomes:
  - "Exit loops appropriately with break"
  - "Skip iterations with continue"
  - "Choose the right control statement"
capstone_relevance: "Control flow in menus and data processing"
---

## Exercise 1: Stop at Target

Print numbers 1-10 but stop when you reach 7:

```python live
# Print 1-10, break at 7


```

:::expected_output
1
2
3
4
5
6
:::

:::hint Stuck?
Inside the loop, check if number equals 7, then break.
:::

:::answer Reveal answer
```python
for num in range(1, 11):
    if num == 7:
        break
    print(num)
```
:::

## Exercise 2: Skip Negative

Sum a list but skip negative numbers:

```python live
numbers = [5, -3, 8, -1, 4, -6, 2]
total = 0
# Sum only positive numbers


```

:::expected_output
19
:::

:::hint Stuck?
If number < 0, use continue to skip. Otherwise add to total.
:::

:::answer Reveal answer
```python
numbers = [5, -3, 8, -1, 4, -6, 2]
total = 0
for num in numbers:
    if num < 0:
        continue
    total = total + num
print(total)
```
:::

## Exercise 3: Find First Match

Find the first name starting with 'C':

```python live
names = ["Alice", "Bob", "Charlie", "Carol", "Dave"]
# Find and print first name starting with C


```

:::expected_output
Charlie
:::

:::hint Stuck?
Check if `name.startswith("C")`, print it and break.
:::

:::answer Reveal answer
```python
names = ["Alice", "Bob", "Charlie", "Carol", "Dave"]
for name in names:
    if name.startswith("C"):
        print(name)
        break
```
:::

## Exercise 4: Valid Input Only

Process numbers but skip zeros (can't divide by zero):

```python live
numbers = [4, 0, 2, 5, 0, 3]
# Print 100 divided by each non-zero number


```

:::hint Stuck?
If number == 0, continue. Otherwise print `100 / number`.
:::

:::answer Reveal answer
```python
numbers = [4, 0, 2, 5, 0, 3]
for num in numbers:
    if num == 0:
        continue
    print(100 / num)
```
:::

## Exercise 5: Search with Feedback

Search for 'banana' in list, print "Not found" if not there:

```python live
fruits = ["apple", "cherry", "orange", "grape"]
# Search for banana, use loop else


```

:::expected_output
Not found
:::

:::hint Stuck?
If found, print and break. Use else clause for "Not found" message.
:::

:::answer Reveal answer
```python
fruits = ["apple", "cherry", "orange", "grape"]
for fruit in fruits:
    if fruit == "banana":
        print("Found banana!")
        break
else:
    print("Not found")
```
:::
