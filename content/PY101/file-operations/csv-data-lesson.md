---
title: "Working with CSV Data"
slug: csv-data-lesson
description: "Learn to read and write CSV (comma-separated values) data"
course_id: PY101
module: file-operations
module_order: 6
topic: csv-data
topic_order: 5
type: lesson
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - reading-files-lesson
  - writing-files-lesson
skills:
  - file-io
  - csv
  - data-processing
outcomes:
  - "Parse CSV data manually"
  - "Create CSV formatted output"
  - "Handle CSV data with headers"
capstone_relevance: "CSV is a common format for data storage and export"
---

## Introduction

**CSV** (Comma-Separated Values) is a simple text format for storing tabular data. Each line is a row, and values in each row are separated by commas. CSV is widely used for data exchange between applications.

## CSV Format

```
name,age,city
Alice,25,New York
Bob,30,Los Angeles
Charlie,35,Chicago
```

- First row is often headers (column names)
- Each row has the same number of values
- Values separated by commas

## Reading CSV Data

```python live
# Sample CSV data
csv_data = """name,age,city
Alice,25,New York
Bob,30,Los Angeles
Charlie,35,Chicago"""

# Split into lines
lines = csv_data.split("\n")

# First line is headers
headers = lines[0].split(",")
print("Headers:", headers)

# Rest are data rows
print("\nData rows:")
for line in lines[1:]:
    values = line.split(",")
    print(values)
```

:::expected_output
Headers: ['name', 'age', 'city']

Data rows:
['Alice', '25', 'New York']
['Bob', '30', 'Los Angeles']
['Charlie', '35', 'Chicago']
:::

## Parsing CSV into Dictionaries

```python live
csv_data = """name,age,city
Alice,25,New York
Bob,30,Los Angeles
Charlie,35,Chicago"""

def parse_csv(data):
    """Parse CSV data into list of dictionaries."""
    lines = data.strip().split("\n")
    headers = lines[0].split(",")
    records = []

    for line in lines[1:]:
        values = line.split(",")
        record = {}
        for i, header in enumerate(headers):
            record[header] = values[i]
        records.append(record)

    return records

people = parse_csv(csv_data)
for person in people:
    print(person)
```

:::expected_output
{'name': 'Alice', 'age': '25', 'city': 'New York'}
{'name': 'Bob', 'age': '30', 'city': 'Los Angeles'}
{'name': 'Charlie', 'age': '35', 'city': 'Chicago'}
:::

## Accessing Parsed Data

```python live
csv_data = """name,age,city
Alice,25,New York
Bob,30,Los Angeles
Charlie,35,Chicago"""

# Parse the data
lines = csv_data.strip().split("\n")
headers = lines[0].split(",")
records = []

for line in lines[1:]:
    values = line.split(",")
    record = dict(zip(headers, values))
    records.append(record)

# Now access data by field name
print("Names:")
for person in records:
    print(" -", person["name"])

print("\nPeople in New York:")
for person in records:
    if person["city"] == "New York":
        print(" -", person["name"])

print("\nPeople over 28:")
for person in records:
    if int(person["age"]) > 28:
        print(" -", person["name"], "is", person["age"])
```

:::expected_output
Names:
 - Alice
 - Bob
 - Charlie

People in New York:
 - Alice

People over 28:
 - Bob is 30
 - Charlie is 35
:::

## Creating CSV Data

```python live
# Data as list of dictionaries
people = [
    {"name": "Alice", "age": 25, "city": "New York"},
    {"name": "Bob", "age": 30, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]

def to_csv(records):
    """Convert list of dictionaries to CSV string."""
    if not records:
        return ""

    # Get headers from first record
    headers = list(records[0].keys())
    lines = [",".join(headers)]

    # Add data rows
    for record in records:
        values = [str(record[h]) for h in headers]
        lines.append(",".join(values))

    return "\n".join(lines)

csv_output = to_csv(people)
print("Generated CSV:")
print(csv_output)
```

:::expected_output
Generated CSV:
name,age,city
Alice,25,New York
Bob,30,Los Angeles
Charlie,35,Chicago
:::

## Handling Special Cases

### Values with Commas

If a value contains a comma, wrap it in quotes:

```python live
# Handling values with commas
data = [
    {"name": "Smith, John", "city": "New York"},
    {"name": "Doe, Jane", "city": "Los Angeles"}
]

def escape_csv_value(value):
    """Escape value if it contains comma."""
    if "," in str(value):
        return '"' + str(value) + '"'
    return str(value)

# Build CSV with escaping
lines = ["name,city"]
for record in data:
    name = escape_csv_value(record["name"])
    city = escape_csv_value(record["city"])
    lines.append(name + "," + city)

print("\n".join(lines))
```

:::expected_output
name,city
"Smith, John",New York
"Doe, Jane",Los Angeles
:::

### Empty Values

```python live
csv_with_empty = """name,email,phone
Alice,alice@email.com,555-1234
Bob,,555-5678
Charlie,charlie@email.com,"""

lines = csv_with_empty.split("\n")
headers = lines[0].split(",")

for line in lines[1:]:
    values = line.split(",")
    record = dict(zip(headers, values))
    print(record)
    # Empty values become empty strings
```

:::expected_output
{'name': 'Alice', 'email': 'alice@email.com', 'phone': '555-1234'}
{'name': 'Bob', 'email': '', 'phone': '555-5678'}
{'name': 'Charlie', 'email': 'charlie@email.com', 'phone': ''}
:::

## Processing Numeric Data

```python live
# Sales data
sales_csv = """product,quantity,price
Widget,100,9.99
Gadget,50,19.99
Gizmo,75,14.99"""

lines = sales_csv.split("\n")
headers = lines[0].split(",")

total_revenue = 0
print("Sales Report:")
print("-" * 40)

for line in lines[1:]:
    values = line.split(",")
    product = values[0]
    quantity = int(values[1])
    price = float(values[2])
    revenue = quantity * price
    total_revenue += revenue
    print(product + ": " + str(quantity) + " x $" + str(price) + " = $" + str(revenue))

print("-" * 40)
print("Total Revenue: $" + str(round(total_revenue, 2)))
```

## Key Points

- CSV is a simple text format for tabular data
- Split lines by `\n`, split values by `,`
- First row is usually headers
- Convert strings to numbers when needed
- Quote values that contain commas
- CSV is great for data exchange and backups

:::hint Note
Python has a built-in `csv` module for more robust CSV handling, but understanding manual parsing helps you work with any delimited format.
:::

