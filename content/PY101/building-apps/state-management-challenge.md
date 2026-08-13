---
title: "Challenge: Build a Task Manager"
slug: state-management-challenge
description: "Create a complete task manager with state management"
course_id: PY101
module: building-apps
module_order: 7
topic: state-management
topic_order: 4
type: challenge
difficulty: beginner
estimated_minutes: 25
prerequisites:
  - state-management-practice
skills:
  - state-management
  - data-structures
outcomes:
  - "Design complete application state"
  - "Implement CRUD operations on state"
  - "Build a working mini-application"
capstone_relevance: "This mirrors the structure of your capstone project"
---

## Challenge: Task Manager Application

Build a complete task manager with multiple users, projects, and tasks.

### State Structure

```python
app_state = {
    "users": [],
    "projects": [],
    "tasks": [],
    "current_user": None,
    "counters": {
        "user_id": 0,
        "project_id": 0,
        "task_id": 0
    }
}
```

### Requirements

**User Management:**
- `create_user(name)` - Create and return user
- `login(user_id)` - Set current user
- `logout()` - Clear current user
- `get_current_user()` - Return current user or None

**Project Management:**
- `create_project(name)` - Create project for current user
- `get_user_projects()` - Get current user's projects
- `delete_project(project_id)` - Delete project and its tasks

**Task Management:**
- `create_task(project_id, title, priority="medium")` - Create task in project
- `complete_task(task_id)` - Mark task as complete
- `get_project_tasks(project_id)` - Get tasks for a project
- `get_task_stats(project_id)` - Return completed/total counts

### Your Solution

```python live
# ============ STATE ============
app_state = {
    "users": [],
    "projects": [],
    "tasks": [],
    "current_user": None,
    "counters": {
        "user_id": 0,
        "project_id": 0,
        "task_id": 0
    }
}

# ============ HELPERS ============
def get_next_id(id_type):
    """Generate next ID for user, project, or task."""
    app_state["counters"][id_type] += 1
    return app_state["counters"][id_type]

# ============ USER MANAGEMENT ============
def create_user(name):
    """Create and return a new user."""
    # Your code here
    pass

def login(user_id):
    """Set current user by ID."""
    # Your code here
    pass

def logout():
    """Clear current user."""
    # Your code here
    pass

def get_current_user():
    """Return current user or None."""
    # Your code here
    pass

# ============ PROJECT MANAGEMENT ============
def create_project(name):
    """Create project for current user."""
    # Your code here
    pass

def get_user_projects():
    """Get current user's projects."""
    # Your code here
    pass

def delete_project(project_id):
    """Delete project and its tasks."""
    # Your code here
    pass

# ============ TASK MANAGEMENT ============
def create_task(project_id, title, priority="medium"):
    """Create task in project."""
    # Your code here
    pass

def complete_task(task_id):
    """Mark task as complete."""
    # Your code here
    pass

def get_project_tasks(project_id):
    """Get tasks for a project."""
    # Your code here
    pass

def get_task_stats(project_id):
    """Return dict with completed and total counts."""
    # Your code here
    pass

# ============ DISPLAY ============
def display_dashboard():
    """Display current user's dashboard."""
    user = get_current_user()
    if not user:
        print("Not logged in")
        return

    print("\n" + "=" * 40)
    print("  Dashboard: " + user["name"])
    print("=" * 40)

    projects = get_user_projects()
    if not projects:
        print("\nNo projects yet.")
        return

    for project in projects:
        print("\n📁 " + project["name"])
        tasks = get_project_tasks(project["id"])
        stats = get_task_stats(project["id"])

        if not tasks:
            print("   No tasks")
        else:
            for task in tasks:
                status = "✓" if task["completed"] else "○"
                print("   " + status + " " + task["title"] + " [" + task["priority"] + "]")

        print("   Progress: " + str(stats["completed"]) + "/" + str(stats["total"]))

    print("\n" + "=" * 40)


# ============ TEST ============
print("=== Task Manager Test ===\n")

# Create users
alice = create_user("Alice")
bob = create_user("Bob")
print("Created users:", alice, bob)

# Login as Alice
login(1)
print("Logged in as:", get_current_user()["name"] if get_current_user() else "None")

# Create projects
work = create_project("Work Tasks")
personal = create_project("Personal")
print("Created projects for Alice")

# Add tasks
create_task(work["id"], "Finish report", "high")
create_task(work["id"], "Email client", "medium")
create_task(work["id"], "Team meeting", "low")

create_task(personal["id"], "Buy groceries", "medium")
create_task(personal["id"], "Exercise", "high")

# Complete some tasks
complete_task(1)
complete_task(4)

# Display dashboard
display_dashboard()

# Switch to Bob
logout()
login(2)
study = create_project("Study")
create_task(study["id"], "Read chapter 5", "high")

display_dashboard()

print("\n=== Test Complete ===")
```

:::expected_output
=== Task Manager Test ===

Created users: {'id': 1, 'name': 'Alice'} {'id': 2, 'name': 'Bob'}
Logged in as: Alice
Created projects for Alice

========================================
  Dashboard: Alice
========================================

📁 Work Tasks
   ✓ Finish report [high]
   ○ Email client [medium]
   ○ Team meeting [low]
   Progress: 1/3

📁 Personal
   ✓ Buy groceries [medium]
   ○ Exercise [high]
   Progress: 1/2

========================================

========================================
  Dashboard: Bob
========================================

📁 Study
   ○ Read chapter 5 [high]
   Progress: 0/1

========================================

=== Test Complete ===
:::

### Expected Output

```
=== Task Manager Test ===

Created users: {'id': 1, 'name': 'Alice'} {'id': 2, 'name': 'Bob'}
Logged in as: Alice
Created projects for Alice

========================================
  Dashboard: Alice
========================================

📁 Work Tasks
   ✓ Finish report [high]
   ○ Email client [medium]
   ○ Team meeting [low]
   Progress: 1/3

📁 Personal
   ✓ Buy groceries [medium]
   ○ Exercise [high]
   Progress: 1/2

========================================

========================================
  Dashboard: Bob
========================================

📁 Study
   ○ Read chapter 5 [high]
   Progress: 0/1

========================================

=== Test Complete ===
```

:::hint User Management
Store user as `{"id": id, "name": name}`. Login finds user by id in users list.
:::

:::hint Project Management
Store project as `{"id": id, "name": name, "user_id": current_user_id}`. Filter by user_id for get_user_projects.
:::

:::hint Task Management
Store task with `{"id": id, "project_id": project_id, "title": title, "priority": priority, "completed": False}`.
:::

:::answer Reveal full solution
```python
# ============ STATE ============
app_state = {
    "users": [],
    "projects": [],
    "tasks": [],
    "current_user": None,
    "counters": {
        "user_id": 0,
        "project_id": 0,
        "task_id": 0
    }
}

# ============ HELPERS ============
def get_next_id(id_type):
    """Generate next ID for user, project, or task."""
    app_state["counters"][id_type] += 1
    return app_state["counters"][id_type]

# ============ USER MANAGEMENT ============
def create_user(name):
    """Create and return a new user."""
    user = {"id": get_next_id("user_id"), "name": name}
    app_state["users"].append(user)
    return user

def login(user_id):
    """Set current user by ID."""
    for user in app_state["users"]:
        if user["id"] == user_id:
            app_state["current_user"] = user
            return True
    return False

def logout():
    """Clear current user."""
    app_state["current_user"] = None

def get_current_user():
    """Return current user or None."""
    return app_state["current_user"]

# ============ PROJECT MANAGEMENT ============
def create_project(name):
    """Create project for current user."""
    user = get_current_user()
    if not user:
        return None
    project = {
        "id": get_next_id("project_id"),
        "name": name,
        "user_id": user["id"]
    }
    app_state["projects"].append(project)
    return project

def get_user_projects():
    """Get current user's projects."""
    user = get_current_user()
    if not user:
        return []
    return [p for p in app_state["projects"] if p["user_id"] == user["id"]]

def delete_project(project_id):
    """Delete project and its tasks."""
    app_state["projects"] = [p for p in app_state["projects"] if p["id"] != project_id]
    app_state["tasks"] = [t for t in app_state["tasks"] if t["project_id"] != project_id]

# ============ TASK MANAGEMENT ============
def create_task(project_id, title, priority="medium"):
    """Create task in project."""
    task = {
        "id": get_next_id("task_id"),
        "project_id": project_id,
        "title": title,
        "priority": priority,
        "completed": False
    }
    app_state["tasks"].append(task)
    return task

def complete_task(task_id):
    """Mark task as complete."""
    for task in app_state["tasks"]:
        if task["id"] == task_id:
            task["completed"] = True
            return True
    return False

def get_project_tasks(project_id):
    """Get tasks for a project."""
    return [t for t in app_state["tasks"] if t["project_id"] == project_id]

def get_task_stats(project_id):
    """Return dict with completed and total counts."""
    tasks = get_project_tasks(project_id)
    completed = len([t for t in tasks if t["completed"]])
    return {"completed": completed, "total": len(tasks)}

# ============ DISPLAY ============
def display_dashboard():
    """Display current user's dashboard."""
    user = get_current_user()
    if not user:
        print("Not logged in")
        return

    print("\n" + "=" * 40)
    print("  Dashboard: " + user["name"])
    print("=" * 40)

    projects = get_user_projects()
    if not projects:
        print("\nNo projects yet.")
        return

    for project in projects:
        print("\n📁 " + project["name"])
        tasks = get_project_tasks(project["id"])
        stats = get_task_stats(project["id"])

        if not tasks:
            print("   No tasks")
        else:
            for task in tasks:
                status = "✓" if task["completed"] else "○"
                print("   " + status + " " + task["title"] + " [" + task["priority"] + "]")

        print("   Progress: " + str(stats["completed"]) + "/" + str(stats["total"]))

    print("\n" + "=" * 40)


# ============ TEST ============
print("=== Task Manager Test ===\n")

# Create users
alice = create_user("Alice")
bob = create_user("Bob")
print("Created users:", alice, bob)

# Login as Alice
login(1)
print("Logged in as:", get_current_user()["name"] if get_current_user() else "None")

# Create projects
work = create_project("Work Tasks")
personal = create_project("Personal")
print("Created projects for Alice")

# Add tasks
create_task(work["id"], "Finish report", "high")
create_task(work["id"], "Email client", "medium")
create_task(work["id"], "Team meeting", "low")

create_task(personal["id"], "Buy groceries", "medium")
create_task(personal["id"], "Exercise", "high")

# Complete some tasks
complete_task(1)
complete_task(4)

# Display dashboard
display_dashboard()

# Switch to Bob
logout()
login(2)
study = create_project("Study")
create_task(study["id"], "Read chapter 5", "high")

display_dashboard()

print("\n=== Test Complete ===")
```
:::

