---
title: "Challenge: Status Dashboard"
slug: booleans-challenge
description: "Build a status dashboard using boolean flags"
course_id: PY101
module: control-flow
module_order: 2
topic: booleans
topic_order: 2
type: challenge
difficulty: beginner
estimated_minutes: 12
prerequisites:
  - booleans-lesson
  - booleans-practice
skills:
  - control-flow
  - booleans
outcomes:
  - "Design a system with multiple boolean states"
  - "Display status information clearly"
  - "Apply truthiness checks"
capstone_relevance: "Track and display record statuses in your application"
---

## The Challenge

Create a system status dashboard that shows the state of various services.

### Requirements

Display the status of:
1. Database connection (True)
2. API server (True)
3. Cache service (False)
4. Email service (True)
5. Background jobs (False)

Calculate and show:
- Total services
- Services online (count of True values)
- Services offline (count of False values)
- Overall system health (True if all are online)

### Example Output

```
=== System Status Dashboard ===

Service Status:
- Database: Online
- API Server: Online
- Cache: Offline
- Email: Online
- Background Jobs: Offline

Summary:
- Total Services: 5
- Online: 3
- Offline: 2
- System Healthy: False
```

## Your Solution

```python live
# Service statuses
database = True
api_server = True
cache = False
email = True
background_jobs = False

# Build and display the dashboard




```

:::expected_output
=== System Status Dashboard ===

Service Status:
- Database: Online
- API Server: Online
- Cache: Offline
- Email: Online
- Background Jobs: Offline

Summary:
- Total Services: 5
- Online: 3
- Offline: 2
- System Healthy: False
:::

:::hint Approach
Convert boolean to "Online"/"Offline" for display. Count True/False values for summary.
:::

:::hint Structure
Display each service status, then calculate the summary stats. For "Online"/"Offline", you can use: `"Online" if status else "Offline"`
:::

:::answer Reveal full solution
```python
# Service statuses
database = True
api_server = True
cache = False
email = True
background_jobs = False

# Build and display the dashboard
print("=== System Status Dashboard ===")
print()
print("Service Status:")
print(f"- Database: {'Online' if database else 'Offline'}")
print(f"- API Server: {'Online' if api_server else 'Offline'}")
print(f"- Cache: {'Online' if cache else 'Offline'}")
print(f"- Email: {'Online' if email else 'Offline'}")
print(f"- Background Jobs: {'Online' if background_jobs else 'Offline'}")

services = [database, api_server, cache, email, background_jobs]
total = len(services)
online = sum(services)
offline = total - online
healthy = all(services)

print()
print("Summary:")
print(f"- Total Services: {total}")
print(f"- Online: {online}")
print(f"- Offline: {offline}")
print(f"- System Healthy: {healthy}")
```
:::
