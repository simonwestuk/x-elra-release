---
title: "Challenge: Build a Data Exporter"
slug: writing-files-challenge
description: "Create a system to export data in multiple formats"
course_id: PY101
module: file-operations
module_order: 6
topic: writing-files
topic_order: 2
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - writing-files-practice
skills:
  - file-io
  - files
outcomes:
  - "Export data in multiple formats"
  - "Create well-formatted output files"
  - "Build a flexible export system"
capstone_relevance: "Data export is essential for application usability"
---

## Challenge: Multi-Format Data Exporter

Build a system that can export data in multiple formats: plain text, CSV, and a formatted report.

### Sample Data

```python
students = [
    {"name": "Alice Johnson", "id": "S001", "grade": 95, "status": "active"},
    {"name": "Bob Smith", "id": "S002", "grade": 87, "status": "active"},
    {"name": "Charlie Brown", "id": "S003", "grade": 72, "status": "probation"},
    {"name": "Diana Ross", "id": "S004", "grade": 91, "status": "active"},
    {"name": "Eve Wilson", "id": "S005", "grade": 68, "status": "probation"}
]
```

### Requirements

1. **`export_as_text(students)`** - Plain text format, one student per line

2. **`export_as_csv(students)`** - CSV format with header row

3. **`export_as_report(students, title)`** - Formatted report with:
   - Title with decorative border
   - Each student's details nicely formatted
   - Summary statistics (count, average grade, count by status)

4. **`export_data(students, format_type)`** - Main function that calls appropriate exporter

### Your Solution

```python live
def export_as_text(students):
    """Export as plain text."""
    # Your code here
    pass

def export_as_csv(students):
    """Export as CSV with headers."""
    # Your code here
    pass

def export_as_report(students, title="Student Report"):
    """Export as formatted report."""
    # Your code here
    pass

def export_data(students, format_type):
    """Export data in specified format."""
    if format_type == "text":
        return export_as_text(students)
    elif format_type == "csv":
        return export_as_csv(students)
    elif format_type == "report":
        return export_as_report(students)
    else:
        return "Error: Unknown format"


# Test data
students = [
    {"name": "Alice Johnson", "id": "S001", "grade": 95, "status": "active"},
    {"name": "Bob Smith", "id": "S002", "grade": 87, "status": "active"},
    {"name": "Charlie Brown", "id": "S003", "grade": 72, "status": "probation"},
    {"name": "Diana Ross", "id": "S004", "grade": 91, "status": "active"},
    {"name": "Eve Wilson", "id": "S005", "grade": 68, "status": "probation"}
]

# Test all formats
print("=== TEXT FORMAT ===")
print(export_data(students, "text"))

print("=== CSV FORMAT ===")
print(export_data(students, "csv"))

print("=== REPORT FORMAT ===")
print(export_data(students, "report"))
```

:::expected_output
=== TEXT FORMAT ===
Alice Johnson (S001): Grade 95, Status: active
Bob Smith (S002): Grade 87, Status: active
Charlie Brown (S003): Grade 72, Status: probation
Diana Ross (S004): Grade 91, Status: active
Eve Wilson (S005): Grade 68, Status: probation
=== CSV FORMAT ===
name,id,grade,status
Alice Johnson,S001,95,active
Bob Smith,S002,87,active
Charlie Brown,S003,72,probation
Diana Ross,S004,91,active
Eve Wilson,S005,68,probation
=== REPORT FORMAT ===
================================
       STUDENT REPORT
================================

Student: Alice Johnson
  ID: S001
  Grade: 95
  Status: active

Student: Bob Smith
  ID: S002
  Grade: 87
  Status: active

Student: Charlie Brown
  ID: S003
  Grade: 72
  Status: probation

Student: Diana Ross
  ID: S004
  Grade: 91
  Status: active

Student: Eve Wilson
  ID: S005
  Grade: 68
  Status: probation

--- Summary ---
Total Students: 5
Average Grade: 82.6
Active: 3
Probation: 2
================================
:::

### Expected Output

```
=== TEXT FORMAT ===
Alice Johnson (S001): Grade 95, Status: active
Bob Smith (S002): Grade 87, Status: active
Charlie Brown (S003): Grade 72, Status: probation
Diana Ross (S004): Grade 91, Status: active
Eve Wilson (S005): Grade 68, Status: probation

=== CSV FORMAT ===
name,id,grade,status
Alice Johnson,S001,95,active
Bob Smith,S002,87,active
Charlie Brown,S003,72,probation
Diana Ross,S004,91,active
Eve Wilson,S005,68,probation

=== REPORT FORMAT ===
================================
       STUDENT REPORT
================================

Student: Alice Johnson
  ID: S001
  Grade: 95
  Status: active

Student: Bob Smith
  ID: S002
  Grade: 87
  Status: active

[... more students ...]

--- Summary ---
Total Students: 5
Average Grade: 82.6
Active: 3
Probation: 2
================================
```

:::hint Text Format
Loop through students: `name + " (" + id + "): Grade " + str(grade) + ...`
:::

:::hint CSV Format
First add header line: "name,id,grade,status\n", then add each student's data.
:::

:::hint Report Statistics
Calculate average: `sum(grades) / len(grades)`. Count status with a dictionary or counting loop.
:::

:::answer Reveal full solution
```python
def export_as_text(students):
    """Export as plain text."""
    lines = []
    for s in students:
        line = s["name"] + " (" + s["id"] + "): Grade " + str(s["grade"]) + ", Status: " + s["status"]
        lines.append(line)
    return "\n".join(lines)

def export_as_csv(students):
    """Export as CSV with headers."""
    lines = ["name,id,grade,status"]
    for s in students:
        line = s["name"] + "," + s["id"] + "," + str(s["grade"]) + "," + s["status"]
        lines.append(line)
    return "\n".join(lines)

def export_as_report(students, title="Student Report"):
    """Export as formatted report."""
    lines = []
    lines.append("=" * 32)
    lines.append("       STUDENT REPORT")
    lines.append("=" * 32)

    for s in students:
        lines.append("")
        lines.append("Student: " + s["name"])
        lines.append("  ID: " + s["id"])
        lines.append("  Grade: " + str(s["grade"]))
        lines.append("  Status: " + s["status"])

    # Summary statistics
    grades = [s["grade"] for s in students]
    avg = sum(grades) / len(grades)
    active = 0
    probation = 0
    for s in students:
        if s["status"] == "active":
            active += 1
        elif s["status"] == "probation":
            probation += 1

    lines.append("")
    lines.append("--- Summary ---")
    lines.append("Total Students: " + str(len(students)))
    lines.append("Average Grade: " + str(avg))
    lines.append("Active: " + str(active))
    lines.append("Probation: " + str(probation))
    lines.append("=" * 32)

    return "\n".join(lines)

def export_data(students, format_type):
    """Export data in specified format."""
    if format_type == "text":
        return export_as_text(students)
    elif format_type == "csv":
        return export_as_csv(students)
    elif format_type == "report":
        return export_as_report(students)
    else:
        return "Error: Unknown format"


# Test data
students = [
    {"name": "Alice Johnson", "id": "S001", "grade": 95, "status": "active"},
    {"name": "Bob Smith", "id": "S002", "grade": 87, "status": "active"},
    {"name": "Charlie Brown", "id": "S003", "grade": 72, "status": "probation"},
    {"name": "Diana Ross", "id": "S004", "grade": 91, "status": "active"},
    {"name": "Eve Wilson", "id": "S005", "grade": 68, "status": "probation"}
]

# Test all formats
print("=== TEXT FORMAT ===")
print(export_data(students, "text"))

print("=== CSV FORMAT ===")
print(export_data(students, "csv"))

print("=== REPORT FORMAT ===")
print(export_data(students, "report"))
```
:::

