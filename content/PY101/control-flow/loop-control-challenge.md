---
title: "Challenge: Data Validator"
slug: loop-control-challenge
description: "Build a data validator using break and continue"
course_id: PY101
module: control-flow
module_order: 2
topic: loop-control
topic_order: 9
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - loop-control-lesson
  - loop-control-practice
skills:
  - control-flow
  - loop-control
outcomes:
  - "Design validation loops"
  - "Use break and continue strategically"
  - "Process data with error handling"
capstone_relevance: "Validate and filter records in your application"
---

## The Challenge

Create a data processor that validates and processes a list of transactions.

### Requirements

Process transactions with these rules:
1. Skip transactions with amount <= 0 (invalid)
2. Stop processing if you encounter "ERROR" status
3. Only sum transactions with "COMPLETE" status
4. Track counts of: processed, skipped, valid

### Test Data

```python
transactions = [
    {"id": 1, "amount": 100, "status": "COMPLETE"},
    {"id": 2, "amount": -50, "status": "COMPLETE"},  # Skip: negative
    {"id": 3, "amount": 75, "status": "PENDING"},    # Skip: not complete
    {"id": 4, "amount": 200, "status": "COMPLETE"},
    {"id": 5, "amount": 0, "status": "COMPLETE"},    # Skip: zero
    {"id": 6, "amount": 150, "status": "ERROR"},     # Stop here
    {"id": 7, "amount": 300, "status": "COMPLETE"},  # Never reached
]
```

### Example Output

```
=== Transaction Processor ===

Processing #1: $100 COMPLETE - Added to total
Processing #2: $-50 COMPLETE - Skipped (invalid amount)
Processing #3: $75 PENDING - Skipped (not complete)
Processing #4: $200 COMPLETE - Added to total
Processing #5: $0 COMPLETE - Skipped (invalid amount)
Processing #6: $150 ERROR - STOPPING

Summary:
- Transactions processed: 6
- Valid transactions: 2
- Invalid/skipped: 3
- Total of valid: $300
```

## Your Solution

```python live
transactions = [
    {"id": 1, "amount": 100, "status": "COMPLETE"},
    {"id": 2, "amount": -50, "status": "COMPLETE"},
    {"id": 3, "amount": 75, "status": "PENDING"},
    {"id": 4, "amount": 200, "status": "COMPLETE"},
    {"id": 5, "amount": 0, "status": "COMPLETE"},
    {"id": 6, "amount": 150, "status": "ERROR"},
    {"id": 7, "amount": 300, "status": "COMPLETE"},
]

# Process transactions




```

:::expected_output
=== Transaction Processor ===

Processing #1: $100 COMPLETE - Added to total
Processing #2: $-50 COMPLETE - Skipped (invalid amount)
Processing #3: $75 PENDING - Skipped (not complete)
Processing #4: $200 COMPLETE - Added to total
Processing #5: $0 COMPLETE - Skipped (invalid amount)
Processing #6: $150 ERROR - STOPPING

Summary:
- Transactions processed: 6
- Valid transactions: 2
- Invalid/skipped: 3
- Total of valid: $300
:::

:::hint Approach
Loop through transactions. Check for ERROR (break), invalid amount (continue), non-COMPLETE status (continue). Otherwise, add to total.
:::

:::hint Structure
Track processed_count, valid_count, skipped_count, and total. Update appropriate counters based on what happens to each transaction.
:::

:::answer Reveal full solution
```python
transactions = [
    {"id": 1, "amount": 100, "status": "COMPLETE"},
    {"id": 2, "amount": -50, "status": "COMPLETE"},
    {"id": 3, "amount": 75, "status": "PENDING"},
    {"id": 4, "amount": 200, "status": "COMPLETE"},
    {"id": 5, "amount": 0, "status": "COMPLETE"},
    {"id": 6, "amount": 150, "status": "ERROR"},
    {"id": 7, "amount": 300, "status": "COMPLETE"},
]

# Process transactions
processed = 0
valid = 0
skipped = 0
total = 0

print("=== Transaction Processor ===")
print()

for t in transactions:
    processed += 1
    print(f"Processing #{t['id']}: ${t['amount']} {t['status']}", end="")

    if t["status"] == "ERROR":
        print(" - STOPPING")
        break

    if t["amount"] <= 0:
        print(" - Skipped (invalid amount)")
        skipped += 1
        continue

    if t["status"] != "COMPLETE":
        print(" - Skipped (not complete)")
        skipped += 1
        continue

    total += t["amount"]
    valid += 1
    print(" - Added to total")

print()
print("Summary:")
print(f"- Transactions processed: {processed}")
print(f"- Valid transactions: {valid}")
print(f"- Invalid/skipped: {skipped}")
print(f"- Total of valid: ${total}")
```
:::
