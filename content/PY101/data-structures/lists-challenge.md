---
title: "Challenge: Playlist Manager"
slug: lists-challenge
description: "Build a playlist manager using list operations"
course_id: PY101
module: data-structures
module_order: 3
topic: lists
topic_order: 1
type: challenge
difficulty: beginner
estimated_minutes: 18
prerequisites:
  - lists-lesson
  - lists-practice
skills:
  - data-structures
  - lists
outcomes:
  - "Design list-based data management"
  - "Perform common list operations"
  - "Display list contents meaningfully"
capstone_relevance: "Manage collections of data in your application"
---

## The Challenge

Create a simple playlist manager that demonstrates various list operations.

### Requirements

1. Start with a playlist of 5 songs
2. Add 2 new songs to the end
3. Insert a song at position 2
4. Remove one song by name
5. Display the playlist with numbers
6. Show playlist statistics

### Example Output

```
=== Playlist Manager ===

Initial Playlist:
1. Bohemian Rhapsody
2. Stairway to Heaven
3. Hotel California
4. Sweet Child O Mine
5. Comfortably Numb

Adding songs...
Inserting "Imagine" at position 2...
Removing "Hotel California"...

Final Playlist:
1. Bohemian Rhapsody
2. Imagine
3. Stairway to Heaven
4. Sweet Child O Mine
5. Comfortably Numb
6. Purple Rain
7. Back in Black

Statistics:
- Total songs: 7
- First song: Bohemian Rhapsody
- Last song: Back in Black
```

## Your Solution

```python live
# Initial playlist
playlist = [
    "Bohemian Rhapsody",
    "Stairway to Heaven",
    "Hotel California",
    "Sweet Child O Mine",
    "Comfortably Numb"
]

print("=== Playlist Manager ===")
print()

# Display initial playlist


# Perform operations


# Display final playlist


# Show statistics


```

:::expected_output
=== Playlist Manager ===

Initial Playlist:
1. Bohemian Rhapsody
2. Stairway to Heaven
3. Hotel California
4. Sweet Child O Mine
5. Comfortably Numb

Adding songs...
Inserting "Imagine" at position 2...
Removing "Hotel California"...

Final Playlist:
1. Bohemian Rhapsody
2. Imagine
3. Stairway to Heaven
4. Sweet Child O Mine
5. Comfortably Numb
6. Purple Rain
7. Back in Black

Statistics:
- Total songs: 7
- First song: Bohemian Rhapsody
- Last song: Back in Black
:::

:::hint Approach
Use enumerate() for numbered display. Use append(), insert(), and remove() for modifications.
:::

:::hint Structure
Print initial playlist, make changes with appropriate messages, print final playlist, calculate and show statistics.
:::

:::answer Reveal full solution
```python
# Initial playlist
playlist = [
    "Bohemian Rhapsody",
    "Stairway to Heaven",
    "Hotel California",
    "Sweet Child O Mine",
    "Comfortably Numb"
]

print("=== Playlist Manager ===")
print()

# Display initial playlist
print("Initial Playlist:")
for i, song in enumerate(playlist, 1):
    print(f"{i}. {song}")
print()

# Perform operations
print("Adding songs...")
playlist.append("Purple Rain")
playlist.append("Back in Black")

print('Inserting "Imagine" at position 2...')
playlist.insert(1, "Imagine")

print('Removing "Hotel California"...')
playlist.remove("Hotel California")
print()

# Display final playlist
print("Final Playlist:")
for i, song in enumerate(playlist, 1):
    print(f"{i}. {song}")
print()

# Show statistics
print("Statistics:")
print(f"- Total songs: {len(playlist)}")
print(f"- First song: {playlist[0]}")
print(f"- Last song: {playlist[-1]}")
```
:::
