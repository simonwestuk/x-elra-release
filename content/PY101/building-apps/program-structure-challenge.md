---
title: "Challenge: Build a Structured Application"
slug: program-structure-challenge
description: "Create a well-structured mini application"
course_id: PY101
module: building-apps
module_order: 7
topic: program-structure
topic_order: 1
type: challenge
difficulty: beginner
estimated_minutes: 25
prerequisites:
  - program-structure-practice
skills:
  - program-design
  - code-organization
outcomes:
  - "Build a complete structured application"
  - "Apply all organization principles"
  - "Create maintainable code"
capstone_relevance: "This structure mirrors your capstone project"
---

## Challenge: Contact Manager

Build a well-structured contact management application.

### Requirements

Create a program with these sections:

1. **CONSTANTS** - App settings
2. **DATA LAYER** - Contact CRUD operations
3. **BUSINESS LOGIC** - Search, validation, etc.
4. **PRESENTATION** - Display functions
5. **MAIN** - Program flow

### Features to Implement

1. Store contacts with name, email, and phone
2. Add new contacts (with validation)
3. List all contacts
4. Search contacts by name
5. Delete contacts
6. Show contact count

### Your Solution

```python live
# ============================================
# CONSTANTS
# ============================================
APP_NAME = "Contact Manager"
VERSION = "1.0"

# ============================================
# DATA LAYER
# ============================================
# Storage
contacts = []

def create_contact(name, email, phone):
    """Create a new contact dict."""
    # Your code here
    pass

def add_contact(contact):
    """Add contact to storage."""
    # Your code here
    pass

def get_all_contacts():
    """Return all contacts."""
    # Your code here
    pass

def delete_contact_by_name(name):
    """Delete contact by name. Return True if deleted."""
    # Your code here
    pass

# ============================================
# BUSINESS LOGIC
# ============================================
def validate_email(email):
    """Check if email is valid."""
    # Your code here
    pass

def validate_phone(phone):
    """Check if phone is valid (has digits)."""
    # Your code here
    pass

def search_contacts(query):
    """Search contacts by name (case-insensitive)."""
    # Your code here
    pass

def get_contact_count():
    """Return number of contacts."""
    # Your code here
    pass

# ============================================
# PRESENTATION
# ============================================
def display_header():
    """Show app header."""
    print("=" * 40)
    print("  " + APP_NAME + " v" + VERSION)
    print("=" * 40)

def display_contact(contact):
    """Display a single contact."""
    # Your code here
    pass

def display_all_contacts():
    """Display all contacts."""
    # Your code here
    pass

def display_message(message):
    """Display a status message."""
    print(">>> " + message)

def display_error(message):
    """Display an error message."""
    print("ERROR: " + message)

# ============================================
# MAIN
# ============================================
def main():
    """Main program entry point."""
    display_header()

    # Add some contacts
    display_message("Adding contacts...")

    # Contact 1 - valid
    if validate_email("alice@email.com"):
        contact = create_contact("Alice Smith", "alice@email.com", "555-1234")
        add_contact(contact)
        display_message("Added Alice Smith")

    # Contact 2 - valid
    if validate_email("bob@email.com"):
        contact = create_contact("Bob Jones", "bob@email.com", "555-5678")
        add_contact(contact)
        display_message("Added Bob Jones")

    # Contact 3 - invalid email (should fail)
    if validate_email("invalid-email"):
        contact = create_contact("Invalid", "invalid-email", "555-0000")
        add_contact(contact)
    else:
        display_error("Invalid email for contact")

    # Contact 4 - valid
    contact = create_contact("Carol White", "carol@email.com", "555-9999")
    add_contact(contact)

    print()
    display_message("Contact count: " + str(get_contact_count()))

    print()
    display_message("All contacts:")
    display_all_contacts()

    print()
    display_message("Searching for 'bob':")
    results = search_contacts("bob")
    for contact in results:
        display_contact(contact)

    print()
    display_message("Deleting Bob Jones...")
    if delete_contact_by_name("Bob Jones"):
        display_message("Deleted successfully")
    else:
        display_error("Contact not found")

    print()
    display_message("Final contact list:")
    display_all_contacts()

    print()
    print("=" * 40)
    display_message("Goodbye!")


# Run the program
if __name__ == "__main__":
    main()
```

:::expected_output
========================================
  Contact Manager v1.0
========================================
>>> Adding contacts...
>>> Added Alice Smith
>>> Added Bob Jones
ERROR: Invalid email for contact

>>> Contact count: 3

>>> All contacts:
  Name: Alice Smith
  Email: alice@email.com
  Phone: 555-1234
  ---
  Name: Bob Jones
  Email: bob@email.com
  Phone: 555-5678
  ---
  Name: Carol White
  Email: carol@email.com
  Phone: 555-9999
  ---

>>> Searching for 'bob':
  Name: Bob Jones
  Email: bob@email.com
  Phone: 555-5678
  ---

>>> Deleting Bob Jones...
>>> Deleted successfully

>>> Final contact list:
  Name: Alice Smith
  Email: alice@email.com
  Phone: 555-1234
  ---
  Name: Carol White
  Email: carol@email.com
  Phone: 555-9999
  ---

========================================
>>> Goodbye!
:::

### Expected Output

```
========================================
  Contact Manager v1.0
========================================
>>> Adding contacts...
>>> Added Alice Smith
>>> Added Bob Jones
ERROR: Invalid email for contact

>>> Contact count: 3

>>> All contacts:
  Name: Alice Smith
  Email: alice@email.com
  Phone: 555-1234
  ---
  Name: Bob Jones
  Email: bob@email.com
  Phone: 555-5678
  ---
  Name: Carol White
  Email: carol@email.com
  Phone: 555-9999
  ---

>>> Searching for 'bob':
  Name: Bob Jones
  Email: bob@email.com
  Phone: 555-5678
  ---

>>> Deleting Bob Jones...
>>> Deleted successfully

>>> Final contact list:
  Name: Alice Smith
  Email: alice@email.com
  Phone: 555-1234
  ---
  Name: Carol White
  Email: carol@email.com
  Phone: 555-9999
  ---

========================================
>>> Goodbye!
```

:::hint Data Layer
`create_contact` returns a dict. `add_contact` appends to the `contacts` list. `get_all_contacts` returns the list.
:::

:::hint Business Logic
`validate_email` checks for @ and . in the email. `search_contacts` loops through contacts checking if query is in name (use .lower() for case-insensitive).
:::

:::hint Delete Function
Loop through contacts, find matching name, remove with `contacts.remove(contact)` or rebuild list without that contact.
:::

:::answer Reveal full solution
```python
# ============================================
# CONSTANTS
# ============================================
APP_NAME = "Contact Manager"
VERSION = "1.0"

# ============================================
# DATA LAYER
# ============================================
# Storage
contacts = []

def create_contact(name, email, phone):
    """Create a new contact dict."""
    return {"name": name, "email": email, "phone": phone}

def add_contact(contact):
    """Add contact to storage."""
    contacts.append(contact)

def get_all_contacts():
    """Return all contacts."""
    return contacts

def delete_contact_by_name(name):
    """Delete contact by name. Return True if deleted."""
    for contact in contacts:
        if contact["name"] == name:
            contacts.remove(contact)
            return True
    return False

# ============================================
# BUSINESS LOGIC
# ============================================
def validate_email(email):
    """Check if email is valid."""
    return "@" in email and "." in email

def validate_phone(phone):
    """Check if phone is valid (has digits)."""
    return any(c.isdigit() for c in phone)

def search_contacts(query):
    """Search contacts by name (case-insensitive)."""
    results = []
    for contact in contacts:
        if query.lower() in contact["name"].lower():
            results.append(contact)
    return results

def get_contact_count():
    """Return number of contacts."""
    return len(contacts)

# ============================================
# PRESENTATION
# ============================================
def display_header():
    """Show app header."""
    print("=" * 40)
    print("  " + APP_NAME + " v" + VERSION)
    print("=" * 40)

def display_contact(contact):
    """Display a single contact."""
    print("  Name: " + contact["name"])
    print("  Email: " + contact["email"])
    print("  Phone: " + contact["phone"])
    print("  ---")

def display_all_contacts():
    """Display all contacts."""
    for contact in contacts:
        display_contact(contact)

def display_message(message):
    """Display a status message."""
    print(">>> " + message)

def display_error(message):
    """Display an error message."""
    print("ERROR: " + message)

# ============================================
# MAIN
# ============================================
def main():
    """Main program entry point."""
    display_header()

    # Add some contacts
    display_message("Adding contacts...")

    # Contact 1 - valid
    if validate_email("alice@email.com"):
        contact = create_contact("Alice Smith", "alice@email.com", "555-1234")
        add_contact(contact)
        display_message("Added Alice Smith")

    # Contact 2 - valid
    if validate_email("bob@email.com"):
        contact = create_contact("Bob Jones", "bob@email.com", "555-5678")
        add_contact(contact)
        display_message("Added Bob Jones")

    # Contact 3 - invalid email (should fail)
    if validate_email("invalid-email"):
        contact = create_contact("Invalid", "invalid-email", "555-0000")
        add_contact(contact)
    else:
        display_error("Invalid email for contact")

    # Contact 4 - valid
    contact = create_contact("Carol White", "carol@email.com", "555-9999")
    add_contact(contact)

    print()
    display_message("Contact count: " + str(get_contact_count()))

    print()
    display_message("All contacts:")
    display_all_contacts()

    print()
    display_message("Searching for 'bob':")
    results = search_contacts("bob")
    for contact in results:
        display_contact(contact)

    print()
    display_message("Deleting Bob Jones...")
    if delete_contact_by_name("Bob Jones"):
        display_message("Deleted successfully")
    else:
        display_error("Contact not found")

    print()
    display_message("Final contact list:")
    display_all_contacts()

    print()
    print("=" * 40)
    display_message("Goodbye!")


# Run the program
if __name__ == "__main__":
    main()
```
:::

