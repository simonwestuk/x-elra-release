---
title: "Challenge: Build a CSV Data Analyzer"
slug: csv-data-challenge
description: "Create a tool to analyze and report on CSV data"
course_id: PY101
module: file-operations
module_order: 6
topic: csv-data
topic_order: 5
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - csv-data-practice
skills:
  - file-io
  - csv
  - data-processing
outcomes:
  - "Build complete CSV processing tools"
  - "Generate reports from CSV data"
  - "Transform and export data"
capstone_relevance: "Data analysis is a key application skill"
---

## Challenge: Sales Data Analyzer

Build a comprehensive sales data analysis tool that can parse, analyze, and report on sales data.

### Sample Data

```
date,product,category,quantity,unit_price
2024-01-05,Laptop,Electronics,3,999.99
2024-01-05,Mouse,Electronics,10,29.99
2024-01-06,Desk Chair,Furniture,2,249.99
2024-01-06,Keyboard,Electronics,8,79.99
2024-01-07,Monitor,Electronics,4,299.99
2024-01-07,Desk Lamp,Furniture,6,45.99
2024-01-08,Headphones,Electronics,5,149.99
2024-01-08,Bookshelf,Furniture,1,189.99
2024-01-09,Webcam,Electronics,7,89.99
2024-01-09,Office Chair,Furniture,3,199.99
```

### Requirements

1. **`parse_sales_data(csv_string)`** - Parse CSV into list of records with proper types

2. **`calculate_revenue(records)`** - Return total revenue (quantity × price)

3. **`revenue_by_category(records)`** - Return dict of revenue per category

4. **`top_products(records, n=3)`** - Return top N products by revenue

5. **`daily_summary(records)`** - Return dict of daily totals

6. **`generate_report(csv_string)`** - Generate complete analysis report

### Your Solution

```python live
def parse_sales_data(csv_string):
    """Parse CSV into list of records with proper types."""
    # Convert quantity to int, unit_price to float
    # Your code here
    pass

def calculate_revenue(records):
    """Calculate total revenue."""
    # Your code here
    pass

def revenue_by_category(records):
    """Calculate revenue by category."""
    # Your code here
    pass

def top_products(records, n=3):
    """Get top N products by revenue."""
    # Your code here
    pass

def daily_summary(records):
    """Calculate daily totals."""
    # Your code here
    pass

def generate_report(csv_string):
    """Generate complete analysis report."""
    # Your code here
    pass


# Test Data
sales_data = """date,product,category,quantity,unit_price
2024-01-05,Laptop,Electronics,3,999.99
2024-01-05,Mouse,Electronics,10,29.99
2024-01-06,Desk Chair,Furniture,2,249.99
2024-01-06,Keyboard,Electronics,8,79.99
2024-01-07,Monitor,Electronics,4,299.99
2024-01-07,Desk Lamp,Furniture,6,45.99
2024-01-08,Headphones,Electronics,5,149.99
2024-01-08,Bookshelf,Furniture,1,189.99
2024-01-09,Webcam,Electronics,7,89.99
2024-01-09,Office Chair,Furniture,3,199.99"""

# Generate the report
generate_report(sales_data)
```

:::expected_output
=======================================
         SALES ANALYSIS REPORT
=======================================

Total Revenue: $8,085.51

Revenue by Category:
  Electronics: $6,519.63
  Furniture: $1,565.88

Top 3 Products by Revenue:
  1. Laptop: $2,999.97
  2. Monitor: $1,199.96
  3. Headphones: $749.95

Daily Summary:
  2024-01-05: $3,299.87
  2024-01-06: $1,139.90
  2024-01-07: $1,475.90
  2024-01-08: $939.94
  2024-01-09: $1,229.90

=======================================
:::

### Expected Output

```
=======================================
         SALES ANALYSIS REPORT
=======================================

Total Revenue: $6,997.79

Revenue by Category:
  Electronics: $5,393.84
  Furniture: $1,603.95

Top 3 Products by Revenue:
  1. Laptop: $2,999.97
  2. Monitor: $1,199.96
  3. Headphones: $749.95

Daily Summary:
  2024-01-05: $3,299.87
  2024-01-06: $1,139.90
  2024-01-07: $1,475.90
  2024-01-08: $939.94
  2024-01-09: $1,229.90

=======================================
```

:::hint Parsing
Convert fields: `int(quantity)` and `float(unit_price)`. Calculate revenue for each record as `quantity * unit_price`.
:::

:::hint Revenue by Category
Create a dict. Loop through records, add revenue to `totals[category]`.
:::

:::hint Top Products
Create dict of product → revenue. Sort by value. Take first N.
:::

:::hint Daily Summary
Similar to category - group by date and sum revenues.
:::

:::hint Formatting
Use `round(value, 2)` for currency. Format with `${:,.2f}` if using f-strings, or manual formatting.
:::

:::answer Reveal full solution
```python
def parse_sales_data(csv_string):
    """Parse CSV into list of records with proper types."""
    lines = csv_string.strip().split("\n")
    headers = lines[0].split(",")
    records = []
    for line in lines[1:]:
        values = line.split(",")
        record = {
            "date": values[0],
            "product": values[1],
            "category": values[2],
            "quantity": int(values[3]),
            "unit_price": float(values[4])
        }
        record["revenue"] = record["quantity"] * record["unit_price"]
        records.append(record)
    return records

def calculate_revenue(records):
    """Calculate total revenue."""
    total = 0
    for record in records:
        total += record["revenue"]
    return round(total, 2)

def revenue_by_category(records):
    """Calculate revenue by category."""
    categories = {}
    for record in records:
        cat = record["category"]
        if cat in categories:
            categories[cat] += record["revenue"]
        else:
            categories[cat] = record["revenue"]
    # Round values
    for cat in categories:
        categories[cat] = round(categories[cat], 2)
    return categories

def top_products(records, n=3):
    """Get top N products by revenue."""
    products = {}
    for record in records:
        name = record["product"]
        if name in products:
            products[name] += record["revenue"]
        else:
            products[name] = record["revenue"]
    # Sort by revenue descending
    sorted_products = sorted(products.items(), key=lambda x: x[1], reverse=True)
    return sorted_products[:n]

def daily_summary(records):
    """Calculate daily totals."""
    days = {}
    for record in records:
        date = record["date"]
        if date in days:
            days[date] += record["revenue"]
        else:
            days[date] = record["revenue"]
    # Round values
    for date in days:
        days[date] = round(days[date], 2)
    return days

def format_currency(amount):
    """Format a number as currency string."""
    return "${:,.2f}".format(amount)

def generate_report(csv_string):
    """Generate complete analysis report."""
    records = parse_sales_data(csv_string)

    print("=" * 39)
    print("         SALES ANALYSIS REPORT")
    print("=" * 39)

    total = calculate_revenue(records)
    print()
    print("Total Revenue:", format_currency(total))

    cat_revenue = revenue_by_category(records)
    print()
    print("Revenue by Category:")
    for cat, rev in cat_revenue.items():
        print("  " + cat + ": " + format_currency(rev))

    top = top_products(records, 3)
    print()
    print("Top 3 Products by Revenue:")
    for i, (product, rev) in enumerate(top):
        print("  " + str(i + 1) + ". " + product + ": " + format_currency(round(rev, 2)))

    daily = daily_summary(records)
    print()
    print("Daily Summary:")
    for date, rev in daily.items():
        print("  " + date + ": " + format_currency(rev))

    print()
    print("=" * 39)


# Test Data
sales_data = """date,product,category,quantity,unit_price
2024-01-05,Laptop,Electronics,3,999.99
2024-01-05,Mouse,Electronics,10,29.99
2024-01-06,Desk Chair,Furniture,2,249.99
2024-01-06,Keyboard,Electronics,8,79.99
2024-01-07,Monitor,Electronics,4,299.99
2024-01-07,Desk Lamp,Furniture,6,45.99
2024-01-08,Headphones,Electronics,5,149.99
2024-01-08,Bookshelf,Furniture,1,189.99
2024-01-09,Webcam,Electronics,7,89.99
2024-01-09,Office Chair,Furniture,3,199.99"""

# Generate the report
generate_report(sales_data)
```
:::

