---
title: "Challenge: Build a Safe File Manager"
slug: file-modes-challenge
description: "Create a file manager that uses correct modes for each operation"
course_id: PY101
module: file-operations
module_order: 6
topic: file-modes
topic_order: 3
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - file-modes-practice
skills:
  - file-io
  - files
outcomes:
  - "Implement safe file operations"
  - "Use correct modes consistently"
  - "Handle file operation errors"
capstone_relevance: "Safe file handling prevents data loss in applications"
---

## Challenge: Simulated File Manager

Build a file manager class that simulates safe file operations using the correct modes.

### Requirements

Create a `FileManager` class with these methods:

1. **`__init__()`** - Initialize with an empty file system (dictionary)

2. **`read(filename)`** - Read file contents
   - Return contents if file exists
   - Raise FileNotFoundError if not

3. **`write(filename, content)`** - Write/overwrite file
   - Create or overwrite the file

4. **`append(filename, content)`** - Append to file
   - Create file if it doesn't exist
   - Add content to end if it does

5. **`create_new(filename, content)`** - Create new file only
   - Raise FileExistsError if file exists

6. **`exists(filename)`** - Check if file exists

7. **`delete(filename)`** - Delete a file
   - Raise FileNotFoundError if not exists

8. **`list_files()`** - Return list of all filenames

### Your Solution

```python live
class FileManager:
    def __init__(self):
        # Simulated file system
        self.files = {}

    def read(self, filename):
        """Read file contents (mode: r)."""
        # Your code here
        pass

    def write(self, filename, content):
        """Write/overwrite file (mode: w)."""
        # Your code here
        pass

    def append(self, filename, content):
        """Append to file (mode: a)."""
        # Your code here
        pass

    def create_new(self, filename, content):
        """Create new file only (mode: x)."""
        # Your code here
        pass

    def exists(self, filename):
        """Check if file exists."""
        # Your code here
        pass

    def delete(self, filename):
        """Delete a file."""
        # Your code here
        pass

    def list_files(self):
        """List all files."""
        # Your code here
        pass


# Test the FileManager
fm = FileManager()

print("=== Testing FileManager ===\n")

# Test write
print("1. Writing 'hello.txt'...")
fm.write("hello.txt", "Hello, World!")
print("   Files:", fm.list_files())

# Test read
print("\n2. Reading 'hello.txt'...")
print("   Content:", fm.read("hello.txt"))

# Test append
print("\n3. Appending to 'hello.txt'...")
fm.append("hello.txt", "\nNice to meet you!")
print("   Content:", fm.read("hello.txt"))

# Test create_new (should work)
print("\n4. Creating 'new.txt'...")
fm.create_new("new.txt", "Brand new file!")
print("   Files:", fm.list_files())

# Test create_new (should fail)
print("\n5. Trying to create 'hello.txt' again...")
try:
    fm.create_new("hello.txt", "This should fail")
except FileExistsError as e:
    print("   Error:", e)

# Test read missing file
print("\n6. Reading missing file...")
try:
    fm.read("missing.txt")
except FileNotFoundError as e:
    print("   Error:", e)

# Test delete
print("\n7. Deleting 'new.txt'...")
fm.delete("new.txt")
print("   Files:", fm.list_files())

# Test append to new file
print("\n8. Appending to non-existent 'log.txt'...")
fm.append("log.txt", "First entry")
fm.append("log.txt", "\nSecond entry")
print("   Content:", fm.read("log.txt"))
print("   Files:", fm.list_files())

print("\n=== All Tests Complete ===")
```

:::expected_output
=== Testing FileManager ===

1. Writing 'hello.txt'...
   Files: ['hello.txt']

2. Reading 'hello.txt'...
   Content: Hello, World!

3. Appending to 'hello.txt'...
   Content: Hello, World!
Nice to meet you!

4. Creating 'new.txt'...
   Files: ['hello.txt', 'new.txt']

5. Trying to create 'hello.txt' again...
   Error: File already exists: hello.txt

6. Reading missing file...
   Error: File not found: missing.txt

7. Deleting 'new.txt'...
   Files: ['hello.txt']

8. Appending to non-existent 'log.txt'...
   Content: First entry
Second entry
   Files: ['hello.txt', 'log.txt']

=== All Tests Complete ===
:::

### Expected Output

```
=== Testing FileManager ===

1. Writing 'hello.txt'...
   Files: ['hello.txt']

2. Reading 'hello.txt'...
   Content: Hello, World!

3. Appending to 'hello.txt'...
   Content: Hello, World!
Nice to meet you!

4. Creating 'new.txt'...
   Files: ['hello.txt', 'new.txt']

5. Trying to create 'hello.txt' again...
   Error: File already exists: hello.txt

6. Reading missing file...
   Error: File not found: missing.txt

7. Deleting 'new.txt'...
   Files: ['hello.txt']

8. Appending to non-existent 'log.txt'...
   Content: First entry
Second entry
   Files: ['hello.txt', 'log.txt']

=== All Tests Complete ===
```

:::hint Read Mode
Check if file exists in `self.files`. If not, raise `FileNotFoundError`.
:::

:::hint Append Mode
If file exists, add to existing content. If not, create it.
:::

:::hint Create New Mode
If file exists, raise `FileExistsError`. Otherwise, create it.
:::

:::answer Reveal full solution
```python
class FileManager:
    def __init__(self):
        # Simulated file system
        self.files = {}

    def read(self, filename):
        """Read file contents (mode: r)."""
        if filename not in self.files:
            raise FileNotFoundError("File not found: " + filename)
        return self.files[filename]

    def write(self, filename, content):
        """Write/overwrite file (mode: w)."""
        self.files[filename] = content

    def append(self, filename, content):
        """Append to file (mode: a)."""
        if filename in self.files:
            self.files[filename] += content
        else:
            self.files[filename] = content

    def create_new(self, filename, content):
        """Create new file only (mode: x)."""
        if filename in self.files:
            raise FileExistsError("File already exists: " + filename)
        self.files[filename] = content

    def exists(self, filename):
        """Check if file exists."""
        return filename in self.files

    def delete(self, filename):
        """Delete a file."""
        if filename not in self.files:
            raise FileNotFoundError("File not found: " + filename)
        del self.files[filename]

    def list_files(self):
        """List all files."""
        return list(self.files.keys())


# Test the FileManager
fm = FileManager()

print("=== Testing FileManager ===\n")

# Test write
print("1. Writing 'hello.txt'...")
fm.write("hello.txt", "Hello, World!")
print("   Files:", fm.list_files())

# Test read
print("\n2. Reading 'hello.txt'...")
print("   Content:", fm.read("hello.txt"))

# Test append
print("\n3. Appending to 'hello.txt'...")
fm.append("hello.txt", "\nNice to meet you!")
print("   Content:", fm.read("hello.txt"))

# Test create_new (should work)
print("\n4. Creating 'new.txt'...")
fm.create_new("new.txt", "Brand new file!")
print("   Files:", fm.list_files())

# Test create_new (should fail)
print("\n5. Trying to create 'hello.txt' again...")
try:
    fm.create_new("hello.txt", "This should fail")
except FileExistsError as e:
    print("   Error:", e)

# Test read missing file
print("\n6. Reading missing file...")
try:
    fm.read("missing.txt")
except FileNotFoundError as e:
    print("   Error:", e)

# Test delete
print("\n7. Deleting 'new.txt'...")
fm.delete("new.txt")
print("   Files:", fm.list_files())

# Test append to new file
print("\n8. Appending to non-existent 'log.txt'...")
fm.append("log.txt", "First entry")
fm.append("log.txt", "\nSecond entry")
print("   Content:", fm.read("log.txt"))
print("   Files:", fm.list_files())

print("\n=== All Tests Complete ===")
```
:::

