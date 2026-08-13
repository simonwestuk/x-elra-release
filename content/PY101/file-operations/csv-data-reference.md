---
title: "Quick Reference: CSV Data"
slug: csv-data-reference
description: "Quick reference for CSV parsing and creation"
course_id: PY101
module: file-operations
module_order: 6
topic: csv-data
topic_order: 5
type: reference
difficulty: beginner
estimated_minutes: 3
prerequisites: []
skills:
  - file-io
  - csv
  - data-processing
outcomes:
  - "Quick lookup for CSV operations"
  - "Review CSV parsing patterns"
capstone_relevance: "CSV reference for data handling"
---

## Quick Reference: CSV Data

### CSV Format

```
header1,header2,header3
value1,value2,value3
value4,value5,value6
```

### Parse CSV String

```python
csv_data = """name,age,city
Alice,25,NYC
Bob,30,LA"""

lines = csv_data.strip().split("\n")
headers = lines[0].split(",")

for line in lines[1:]:
    values = line.split(",")
    # Process values
```

### Parse to Dictionaries

```python
def csv_to_dicts(csv_string):
    lines = csv_string.strip().split("\n")
    headers = lines[0].split(",")
    records = []

    for line in lines[1:]:
        values = line.split(",")
        record = dict(zip(headers, values))
        records.append(record)

    return records
```

### Create CSV from Data

```python
def dicts_to_csv(records):
    if not records:
        return ""

    headers = list(records[0].keys())
    lines = [",".join(headers)]

    for record in records:
        values = [str(record[h]) for h in headers]
        lines.append(",".join(values))

    return "\n".join(lines)
```

### Type Conversion

```python
# String to number
quantity = int(row[1])
price = float(row[2])

# In parsing
record = {
    "name": values[0],
    "age": int(values[1]),
    "salary": float(values[2])
}
```

### Handle Special Values

```python
# Values with commas (quote them)
def escape_value(val):
    if "," in str(val):
        return '"' + str(val) + '"'
    return str(val)

# Empty values
value = row[i] if row[i] else "N/A"
```

### Common Operations

```python
# Filter rows
filtered = [r for r in records if r["status"] == "active"]

# Calculate sum
total = sum(int(r["amount"]) for r in records)

# Group by field
from collections import defaultdict
groups = defaultdict(list)
for r in records:
    groups[r["category"]].append(r)

# Sort records
sorted_records = sorted(records, key=lambda r: r["name"])
```

### Read CSV File

```python
with open("data.csv", "r") as f:
    lines = f.readlines()

headers = lines[0].strip().split(",")
for line in lines[1:]:
    values = line.strip().split(",")
    # process
```

### Write CSV File

```python
with open("output.csv", "w") as f:
    f.write("name,age,city\n")
    for record in data:
        line = ",".join([
            record["name"],
            str(record["age"]),
            record["city"]
        ])
        f.write(line + "\n")
```

### Quick Patterns

| Task | Code |
|------|------|
| Split line | `values = line.split(",")` |
| Get header | `headers = lines[0].split(",")` |
| Make dict | `dict(zip(headers, values))` |
| Join values | `",".join(values)` |
| Skip header | `for line in lines[1:]:` |

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| IndexError | Uneven columns | Check data consistency |
| ValueError | Type conversion | Validate before converting |
| Wrong values | Extra whitespace | Use `.strip()` |

### See Also

- [Reading Files](reading-files-lesson.html) - File reading basics
- [Writing Files](writing-files-lesson.html) - File writing basics
- [Dictionaries](dicts-lesson.html) - Dict operations

