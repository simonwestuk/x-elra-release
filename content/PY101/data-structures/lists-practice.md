---
title: "Practice: Lists Basics"
slug: lists-practice
description: "Practice creating and working with lists"
course_id: PY101
module: data-structures
module_order: 3
topic: lists
topic_order: 1
type: practice
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - lists-lesson
skills:
  - data-structures
  - lists
outcomes:
  - "Create and modify lists"
  - "Access elements by index"
  - "Add and remove list items"
capstone_relevance: "Work with collections of records"
---

## Exercise 1: Create a List

Create a list of 5 favorite foods and print it:

```python live
# Create a list of 5 foods


```

:::hint Stuck?
Use square brackets: `foods = ["pizza", "sushi", ...]`
:::

:::answer Reveal answer
```python
# Create a list of 5 foods
foods = ["pizza", "sushi", "tacos", "pasta", "salad"]
print(foods)
```
:::

## Exercise 2: Access Elements

Print the first and last elements of this list:

```python live
cities = ["London", "Paris", "Tokyo", "New York", "Sydney"]
# Print first and last


```

:::expected_output
London
Sydney
:::

:::hint Stuck?
Use index 0 for first, -1 for last: `cities[0]` and `cities[-1]`
:::

:::answer Reveal answer
```python
cities = ["London", "Paris", "Tokyo", "New York", "Sydney"]
print(cities[0])
print(cities[-1])
```
:::

## Exercise 3: Modify Element

Change the second element to "updated":

```python live
items = ["first", "second", "third"]
# Change second element
# Print the list


```

:::expected_output
['first', 'updated', 'third']
:::

:::hint Stuck?
Second element is index 1: `items[1] = "updated"`
:::

:::answer Reveal answer
```python
items = ["first", "second", "third"]
items[1] = "updated"
print(items)
```
:::

## Exercise 4: Add Items

Add two items to the list and print the result:

```python live
colors = ["red", "blue"]
# Add "green" and "yellow"
# Print the list


```

:::expected_output
['red', 'blue', 'green', 'yellow']
:::

:::hint Stuck?
Use `append()` twice or extend with a list.
:::

:::answer Reveal answer
```python
colors = ["red", "blue"]
colors.append("green")
colors.append("yellow")
print(colors)
```
:::

## Exercise 5: Remove Item

Remove "banana" from the list:

```python live
fruits = ["apple", "banana", "cherry", "banana"]
# Remove banana
# Print the list


```

:::expected_output
['apple', 'cherry', 'banana']
:::

:::hint Stuck?
Use `remove("banana")` - it removes the first occurrence.
:::

:::answer Reveal answer
```python
fruits = ["apple", "banana", "cherry", "banana"]
fruits.remove("banana")
print(fruits)
```
:::
