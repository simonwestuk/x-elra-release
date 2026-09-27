---
title: "Practice: Variables and Types"
slug: variables-types-practice
description: "Practice creating variables and working with different data types"
course_id: PY101
module: python-foundations
module_order: 1
topic: variables-types
topic_order: 3
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - variables-types-lesson
skills:
  - variables
  - types
outcomes:
  - "Create variables of different types"
  - "Reassign variable values"
  - "Use type() to verify data types"
capstone_relevance: "Every piece of data in your app will be stored in variables"
---

## Exercise 1: Create a String Variable

Create a variable called `city` that stores the name of a city, then print it:

```python live
# Create the city variable and print it


```

:::hint Stuck?
Use the format: `variable_name = "value"` then `print(variable_name)`
:::

:::answer Reveal answer
```python
city = "Paris"
print(city)
```
:::

## Exercise 2: Numeric Variables

Create two variables: `quantity` (an integer) and `price` (a float), then print both:

```python live
# Create quantity as a whole number
# Create price as a decimal number
# Print both


```

:::hint Stuck?
Integers are whole numbers like `5`. Floats have decimals like `4.99`.
:::

:::answer Reveal answer
```python
quantity = 5
price = 4.99
print(quantity)
print(price)
```
:::

## Exercise 3: Check the Type

Create a variable and use `type()` to confirm it's a boolean:

```python live
# Create a boolean variable (True or False)
# Print its type


```

:::hint Stuck?
Boolean values are `True` or `False` (with capital letters). Use `print(type(variable))` to check.
:::

:::answer Reveal answer
```python
is_active = True
print(type(is_active))
```
:::

## Exercise 4: Reassign a Variable

Create a variable, print it, change its value, and print it again:

```python live
# Create a variable with an initial value
# Print it
# Change the variable to a new value
# Print it again


```

:::hint Stuck?
Just use the `=` sign again to give the variable a new value.
:::

:::answer Reveal answer
```python
score = 10
print(score)
score = 20
print(score)
```
:::

## Exercise 5: Product Information

Create variables to store product information, then print them all:
- `product_name` (string)
- `product_price` (float)
- `in_stock` (boolean)
- `quantity_available` (integer)

```python live
# Create all four variables


# Print all the information


```

:::hint Stuck?
Create each variable on its own line, then use print() to display each one.
:::

:::answer Reveal answer
```python
product_name = "Laptop"
product_price = 999.99
in_stock = True
quantity_available = 25

print(product_name)
print(product_price)
print(in_stock)
print(quantity_available)
```
:::
