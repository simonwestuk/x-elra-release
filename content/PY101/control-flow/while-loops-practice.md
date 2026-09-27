---
title: "Practice: While Loops"
slug: while-loops-practice
description: "Practice repeating code with while loops"
course_id: PY101
module: control-flow
module_order: 2
topic: while-loops
topic_order: 7
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - while-loops-lesson
skills:
  - control-flow
  - while-loops
outcomes:
  - "Write while loops with correct conditions"
  - "Update loop variables properly"
  - "Use while for input validation"
capstone_relevance: "Implement repeating menus in your application"
---

## Exercise 1: Count to 10

Print numbers 1 through 10 using a while loop:

```python live
# Start at 1, print each number, stop after 10


```

:::expected_output
1
2
3
4
5
6
7
8
9
10
:::

:::hint Stuck?
Start with `num = 1`, loop while `num <= 10`, print and increment.
:::

:::answer Reveal answer
```python
num = 1
while num <= 10:
    print(num)
    num = num + 1
```
:::

## Exercise 2: Countdown

Print a countdown from 5 to 1, then "Blast off!":

```python live
# Count down from 5


```

:::expected_output
5
4
3
2
1
Blast off!
:::

:::hint Stuck?
Start at 5, loop while > 0, print and decrement.
:::

:::answer Reveal answer
```python
count = 5
while count > 0:
    print(count)
    count = count - 1
print("Blast off!")
```
:::

## Exercise 3: Sum Until 100

Add numbers (1, 2, 3...) until the sum exceeds 100. Print the final sum:

```python live
total = 0
num = 1
# Keep adding until total > 100


```

:::expected_output
105
:::

:::hint Stuck?
Loop while `total <= 100`, add num to total, increment num.
:::

:::answer Reveal answer
```python
total = 0
num = 1
while total <= 100:
    total = total + num
    num = num + 1
print(total)
```
:::

## Exercise 4: Password Retry

Ask for password until correct (password is "python123"):

```python live
# Keep asking until correct password


```

:::hint Stuck?
Use `while True:` with `break` when correct, or `while password != "python123"`.
:::

:::answer Reveal answer
```python
password = ""
while password != "python123":
    password = input("Enter password: ")
print("Access granted!")
```
:::

## Exercise 5: Double Until Big

Start with 1, keep doubling until value exceeds 1000:

```python live
value = 1
# Double until > 1000, print each step


```

:::expected_output
1
2
4
8
16
32
64
128
256
512
:::

:::hint Stuck?
Loop while `value <= 1000`, print value, then `value = value * 2`.
:::

:::answer Reveal answer
```python
value = 1
while value <= 1000:
    print(value)
    value = value * 2
```
:::
