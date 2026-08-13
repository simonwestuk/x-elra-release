---
title: "Challenge: Build a Game Score Tracker"
slug: scope-challenge
description: "Create a score tracking system using appropriate scope"
course_id: PY101
module: functions
module_order: 4
topic: scope
topic_order: 5
type: challenge
difficulty: beginner
estimated_minutes: 20
prerequisites:
  - scope-practice
skills:
  - functions
  - scope
outcomes:
  - "Design programs with proper scope"
  - "Use global variables appropriately"
  - "Create modular, maintainable code"
capstone_relevance: "State management is crucial for applications"
---

## Challenge: Game Score Tracker

Build a score tracking system for a simple game with multiple players.

### Requirements

**Global State:**
- `player1_score` - starts at 0
- `player2_score` - starts at 0
- `round_number` - starts at 1

**Functions:**

1. `add_points(player, points)` - Adds points to the specified player (1 or 2)

2. `get_score(player)` - Returns the current score for player 1 or 2

3. `get_leader()` - Returns "Player 1", "Player 2", or "Tie"

4. `next_round()` - Increments the round number and prints "Starting Round X"

5. `display_scores()` - Prints the current scores in a nice format:
```
=== Round X ===
Player 1: XX points
Player 2: XX points
Leader: [leader]
===============
```

6. `reset_game()` - Resets all scores to 0 and round to 1

### Your Solution

```python live
# Global state
player1_score = 0
player2_score = 0
round_number = 1

# Define your functions here




# Simulate a game
display_scores()

# Round 1
add_points(1, 10)
add_points(2, 15)
display_scores()

# Round 2
next_round()
add_points(1, 20)
add_points(2, 5)
display_scores()

# Round 3
next_round()
add_points(1, 5)
add_points(2, 10)
display_scores()

print("\nFinal Leader:", get_leader())

# Reset for new game
reset_game()
print("\nAfter reset:")
display_scores()
```

:::expected_output
=== Round 1 ===
Player 1: 0 points
Player 2: 0 points
Leader: Tie
===============
=== Round 1 ===
Player 1: 10 points
Player 2: 15 points
Leader: Player 2
===============
Starting Round 2
=== Round 2 ===
Player 1: 30 points
Player 2: 20 points
Leader: Player 1
===============
Starting Round 3
=== Round 3 ===
Player 1: 35 points
Player 2: 30 points
Leader: Player 1
===============

Final Leader: Player 1

After reset:
=== Round 1 ===
Player 1: 0 points
Player 2: 0 points
Leader: Tie
===============
:::

### Expected Output

```
=== Round 1 ===
Player 1: 0 points
Player 2: 0 points
Leader: Tie
===============
=== Round 1 ===
Player 1: 10 points
Player 2: 15 points
Leader: Player 2
===============
Starting Round 2
=== Round 2 ===
Player 1: 30 points
Player 2: 20 points
Leader: Player 1
===============
Starting Round 3
=== Round 3 ===
Player 1: 35 points
Player 2: 30 points
Leader: Player 1
===============

Final Leader: Player 1

After reset:
=== Round 1 ===
Player 1: 0 points
Player 2: 0 points
Leader: Tie
===============
```

:::hint Modifying Globals
Remember to use `global variable_name` at the start of any function that *modifies* a global variable.
:::

:::hint Player Check
Use if/elif to check which player: `if player == 1:` modify player1_score, `elif player == 2:` modify player2_score.
:::

:::hint Get Leader Logic
Compare scores: if equal → "Tie", if player1 > player2 → "Player 1", else → "Player 2".
:::

:::answer Reveal full solution
```python
# Global state
player1_score = 0
player2_score = 0
round_number = 1

def add_points(player, points):
    global player1_score, player2_score
    if player == 1:
        player1_score = player1_score + points
    elif player == 2:
        player2_score = player2_score + points

def get_score(player):
    if player == 1:
        return player1_score
    elif player == 2:
        return player2_score

def get_leader():
    if player1_score > player2_score:
        return "Player 1"
    elif player2_score > player1_score:
        return "Player 2"
    else:
        return "Tie"

def next_round():
    global round_number
    round_number = round_number + 1
    print("Starting Round " + str(round_number))

def display_scores():
    print("=== Round " + str(round_number) + " ===")
    print("Player 1: " + str(player1_score) + " points")
    print("Player 2: " + str(player2_score) + " points")
    print("Leader: " + get_leader())
    print("===============")

def reset_game():
    global player1_score, player2_score, round_number
    player1_score = 0
    player2_score = 0
    round_number = 1

# Simulate a game
display_scores()

# Round 1
add_points(1, 10)
add_points(2, 15)
display_scores()

# Round 2
next_round()
add_points(1, 20)
add_points(2, 5)
display_scores()

# Round 3
next_round()
add_points(1, 5)
add_points(2, 10)
display_scores()

print("\nFinal Leader:", get_leader())

# Reset for new game
reset_game()
print("\nAfter reset:")
display_scores()
```
:::

