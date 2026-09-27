---
title: "Practice: CSV Data"
slug: csv-data-practice
description: "Practice parsing and creating CSV data"
course_id: PY101
module: file-operations
module_order: 6
topic: csv-data
topic_order: 5
type: practice
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - csv-data-lesson
skills:
  - file-io
  - csv
  - data-processing
outcomes:
  - "Parse CSV data into usable structures"
  - "Generate CSV from data"
  - "Process CSV data for analysis"
capstone_relevance: "CSV handling is essential for data import/export"
---

## Exercise 1: Parse Simple CSV

Parse this CSV data and print each person's name and age.

```python live
csv_data = """name,age,country
Alice,28,USA
Bob,34,Canada
Carol,42,UK
David,25,Australia"""

# Parse and print each person
# Your code here


# Expected output:
# Alice is 28 years old
# Bob is 34 years old
# Carol is 42 years old
# David is 25 years old
```

:::expected_output
Alice is 28 years old
Bob is 34 years old
Carol is 42 years old
David is 25 years old
:::

:::hint Stuck?
Split by `\n`, skip the header line, then split each data line by `,`.
:::

:::answer Reveal answer
```python
csv_data = """name,age,country
Alice,28,USA
Bob,34,Canada
Carol,42,UK
David,25,Australia"""

# Parse and print each person
lines = csv_data.split("\n")
for line in lines[1:]:  # Skip header
    parts = line.split(",")
    name = parts[0]
    age = parts[1]
    print(name + " is " + age + " years old")
```
:::

## Exercise 2: Convert to Dictionaries

Parse the CSV into a list of dictionaries.

```python live
csv_data = """id,product,price
1,Laptop,999.99
2,Mouse,29.99
3,Keyboard,79.99
4,Monitor,299.99"""

def csv_to_dicts(data):
    """Convert CSV string to list of dictionaries."""
    # Your code here
    pass

products = csv_to_dicts(csv_data)
print("Products:")
for product in products:
    print(product)

# Expected:
# {'id': '1', 'product': 'Laptop', 'price': '999.99'}
# etc.
```

:::expected_output
Products:
{'id': '1', 'product': 'Laptop', 'price': '999.99'}
{'id': '2', 'product': 'Mouse', 'price': '29.99'}
{'id': '3', 'product': 'Keyboard', 'price': '79.99'}
{'id': '4', 'product': 'Monitor', 'price': '299.99'}
:::

:::hint Stuck?
Get headers from first line. For each data line, zip headers with values to create a dict.
:::

:::answer Reveal answer
```python
csv_data = """id,product,price
1,Laptop,999.99
2,Mouse,29.99
3,Keyboard,79.99
4,Monitor,299.99"""

def csv_to_dicts(data):
    """Convert CSV string to list of dictionaries."""
    lines = data.split("\n")
    headers = lines[0].split(",")
    result = []
    for line in lines[1:]:
        values = line.split(",")
        record = {}
        for i in range(len(headers)):
            record[headers[i]] = values[i]
        result.append(record)
    return result

products = csv_to_dicts(csv_data)
print("Products:")
for product in products:
    print(product)
```
:::

## Exercise 3: Calculate Statistics

Parse the CSV and calculate total and average sales.

```python live
sales_csv = """month,sales
January,15000
February,18500
March,22000
April,19500
May,21000
June,24500"""

# Parse the data
# Calculate total sales
# Calculate average sales
# Find the month with highest sales

# Your code here


# Expected output:
# Total Sales: $120500
# Average Sales: $20083.33
# Best Month: June ($24500)
```

:::expected_output
Total Sales: $120500
Average Sales: $20083.33
Best Month: June ($24500)
:::

:::hint Stuck?
Convert sales values to int/float. Use sum() for total, divide by count for average, use max() or loop to find best.
:::

:::answer Reveal answer
```python
sales_csv = """month,sales
January,15000
February,18500
March,22000
April,19500
May,21000
June,24500"""

# Parse the data
lines = sales_csv.split("\n")
months = []
sales = []
for line in lines[1:]:  # Skip header
    parts = line.split(",")
    months.append(parts[0])
    sales.append(int(parts[1]))

# Calculate total sales
total = sum(sales)

# Calculate average sales
average = total / len(sales)

# Find the month with highest sales
best_index = sales.index(max(sales))
best_month = months[best_index]
best_sales = sales[best_index]

print("Total Sales: $" + str(total))
print("Average Sales: $" + str(round(average, 2)))
print("Best Month: " + best_month + " ($" + str(best_sales) + ")")
```
:::

## Exercise 4: Create CSV from Data

Convert this list of dictionaries to CSV format.

```python live
students = [
    {"name": "Alice", "grade": "A", "score": 95},
    {"name": "Bob", "grade": "B", "score": 85},
    {"name": "Carol", "grade": "A", "score": 92},
    {"name": "David", "grade": "C", "score": 78}
]

def dicts_to_csv(records):
    """Convert list of dictionaries to CSV string."""
    # Your code here
    pass

csv_output = dicts_to_csv(students)
print(csv_output)

# Expected output:
# name,grade,score
# Alice,A,95
# Bob,B,85
# Carol,A,92
# David,C,78
```

:::expected_output
name,grade,score
Alice,A,95
Bob,B,85
Carol,A,92
David,C,78
:::

:::hint Stuck?
Get headers from keys of first record. Build header line with join. Build each data line similarly.
:::

:::answer Reveal answer
```python
students = [
    {"name": "Alice", "grade": "A", "score": 95},
    {"name": "Bob", "grade": "B", "score": 85},
    {"name": "Carol", "grade": "A", "score": 92},
    {"name": "David", "grade": "C", "score": 78}
]

def dicts_to_csv(records):
    """Convert list of dictionaries to CSV string."""
    if not records:
        return ""
    headers = list(records[0].keys())
    lines = [",".join(headers)]
    for record in records:
        values = [str(record[h]) for h in headers]
        lines.append(",".join(values))
    return "\n".join(lines)

csv_output = dicts_to_csv(students)
print(csv_output)
```
:::

## Exercise 5: Filter and Export

Parse the CSV, filter records, and create new CSV with filtered data.

```python live
employee_csv = """name,department,salary
Alice,Engineering,75000
Bob,Marketing,55000
Carol,Engineering,82000
David,Sales,48000
Eve,Engineering,90000
Frank,Marketing,52000"""

def filter_by_department(csv_data, dept):
    """Return CSV of employees in specified department."""
    # Your code here
    pass

# Get all Engineering employees
result = filter_by_department(employee_csv, "Engineering")
print("Engineering Department:")
print(result)

# Expected output:
# name,department,salary
# Alice,Engineering,75000
# Carol,Engineering,82000
# Eve,Engineering,90000
```

:::expected_output
Engineering Department:
name,department,salary
Alice,Engineering,75000
Carol,Engineering,82000
Eve,Engineering,90000
:::

:::hint Stuck?
Parse the CSV, loop through records keeping only those where department matches, rebuild CSV from filtered list.
:::

:::answer Reveal answer
```python
employee_csv = """name,department,salary
Alice,Engineering,75000
Bob,Marketing,55000
Carol,Engineering,82000
David,Sales,48000
Eve,Engineering,90000
Frank,Marketing,52000"""

def filter_by_department(csv_data, dept):
    """Return CSV of employees in specified department."""
    lines = csv_data.split("\n")
    header = lines[0]
    filtered = [header]
    for line in lines[1:]:
        parts = line.split(",")
        if parts[1] == dept:
            filtered.append(line)
    return "\n".join(filtered)

# Get all Engineering employees
result = filter_by_department(employee_csv, "Engineering")
print("Engineering Department:")
print(result)
```
:::

