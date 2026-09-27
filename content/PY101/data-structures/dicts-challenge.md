---
title: "Challenge: Contact Book"
slug: dicts-challenge
description: "Build a contact book using dictionaries"
course_id: PY101
module: data-structures
module_order: 3
topic: dicts
topic_order: 7
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - dicts-lesson
  - dicts-practice
skills:
  - data-structures
  - dicts
outcomes:
  - "Design dictionary structures"
  - "Work with nested data"
  - "Build data management solutions"
capstone_relevance: "Structure and manage your application records"
---

## The Challenge

Create a contact book that stores and displays contact information.

### Requirements

1. Create 3 contacts with: name, phone, email, and city
2. Display all contacts formatted nicely
3. Search for a contact by name
4. Show contact count by city

### Example Output

```
=== Contact Book ===

All Contacts:
---
Name: Alice Johnson
Phone: 555-1234
Email: alice@email.com
City: New York
---
Name: Bob Smith
Phone: 555-5678
Email: bob@email.com
City: Los Angeles
---
Name: Carol Davis
Phone: 555-9012
Email: carol@email.com
City: New York
---

Search for "Bob Smith":
Found! Phone: 555-5678, Email: bob@email.com

Contacts by City:
- New York: 2
- Los Angeles: 1
```

## Your Solution

```python live
# Create contacts as list of dictionaries
contacts = [
    {
        "name": "Alice Johnson",
        "phone": "555-1234",
        "email": "alice@email.com",
        "city": "New York"
    },
    # Add more contacts...
]

print("=== Contact Book ===")
print()

# Display all contacts


# Search for a contact


# Count by city


```

:::expected_output
=== Contact Book ===

All Contacts:
---
Name: Alice Johnson
Phone: 555-1234
Email: alice@email.com
City: New York
---
Name: Bob Smith
Phone: 555-5678
Email: bob@email.com
City: Los Angeles
---
Name: Carol Davis
Phone: 555-9012
Email: carol@email.com
City: New York
---

Search for "Bob Smith":
Found! Phone: 555-5678, Email: bob@email.com

Contacts by City:
- New York: 2
- Los Angeles: 1
:::

:::hint Approach
Use a list of dictionaries for contacts. Loop to display. Loop with condition to search. Use another dict to count cities.
:::

:::hint Structure
For city counting, create an empty dict and use `city_counts[city] = city_counts.get(city, 0) + 1` pattern.
:::

:::answer Reveal full solution
```python
# Create contacts as list of dictionaries
contacts = [
    {
        "name": "Alice Johnson",
        "phone": "555-1234",
        "email": "alice@email.com",
        "city": "New York"
    },
    {
        "name": "Bob Smith",
        "phone": "555-5678",
        "email": "bob@email.com",
        "city": "Los Angeles"
    },
    {
        "name": "Carol Davis",
        "phone": "555-9012",
        "email": "carol@email.com",
        "city": "New York"
    },
]

print("=== Contact Book ===")
print()

# Display all contacts
print("All Contacts:")
for contact in contacts:
    print("---")
    print(f"Name: {contact['name']}")
    print(f"Phone: {contact['phone']}")
    print(f"Email: {contact['email']}")
    print(f"City: {contact['city']}")
print("---")
print()

# Search for a contact
search_name = "Bob Smith"
print(f'Search for "{search_name}":')
for contact in contacts:
    if contact["name"] == search_name:
        print(f"Found! Phone: {contact['phone']}, Email: {contact['email']}")
        break
print()

# Count by city
city_counts = {}
for contact in contacts:
    city = contact["city"]
    city_counts[city] = city_counts.get(city, 0) + 1

print("Contacts by City:")
for city, count in city_counts.items():
    print(f"- {city}: {count}")
```
:::
