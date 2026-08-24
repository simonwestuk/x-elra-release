---
title: "Challenge: Coordinate System"
slug: tuples-challenge
description: "Build a coordinate system using tuples"
course_id: PY101
module: data-structures
module_order: 3
topic: tuples
topic_order: 6
type: challenge
difficulty: beginner
estimated_minutes: 15
prerequisites:
  - tuples-lesson
  - tuples-practice
skills:
  - data-structures
  - tuples
outcomes:
  - "Use tuples for coordinate data"
  - "Calculate with tuple values"
  - "Store tuples as dictionary keys"
capstone_relevance: "Structure fixed data in your application"
---

## The Challenge

Create a simple coordinate system that tracks locations on a grid.

### Requirements

1. Store several points as tuples (x, y)
2. Calculate distance from origin for each point
3. Store location names using point tuples as keys
4. Find the point farthest from origin

Distance formula: sqrt(x² + y²)

### Example Output

```
=== Coordinate System ===

Points:
- Home: (0, 0)
- Work: (3, 4) - Distance: 5.0
- Gym: (6, 8) - Distance: 10.0
- Store: (5, 12) - Distance: 13.0

Farthest from origin: Store at (5, 12)
```

## Your Solution

```python live
# Define points
home = (0, 0)
work = (3, 4)
gym = (6, 8)
store = (5, 12)

# Location names dictionary
locations = {
    home: "Home",
    work: "Work",
    gym: "Gym",
    store: "Store"
}

print("=== Coordinate System ===")
print()

# Process points and find farthest




```

:::expected_output
=== Coordinate System ===

Points:
- Home: (0, 0)
- Work: (3, 4) - Distance: 5.0
- Gym: (6, 8) - Distance: 10.0
- Store: (5, 12) - Distance: 13.0

Farthest from origin: Store at (5, 12)
:::

:::hint Approach
Loop through locations dict. Calculate distance for each using x**2 + y**2, then sqrt. Track the maximum.
:::

:::hint Structure
Unpack each tuple to get x, y. For sqrt, you can use `(x**2 + y**2) ** 0.5`. Keep track of max distance and which point.
:::

:::answer Reveal full solution
```python
# Define points
home = (0, 0)
work = (3, 4)
gym = (6, 8)
store = (5, 12)

# Location names dictionary
locations = {
    home: "Home",
    work: "Work",
    gym: "Gym",
    store: "Store"
}

print("=== Coordinate System ===")
print()

# Process points and find farthest
print("Points:")
max_distance = 0
farthest_point = None
farthest_name = None

for point, name in locations.items():
    x, y = point
    distance = (x**2 + y**2) ** 0.5

    if point == home:
        print(f"- {name}: ({x}, {y})")
    else:
        print(f"- {name}: ({x}, {y}) - Distance: {distance}")

    if distance > max_distance:
        max_distance = distance
        farthest_point = point
        farthest_name = name

print()
print(f"Farthest from origin: {farthest_name} at ({farthest_point[0]}, {farthest_point[1]})")
```
:::
