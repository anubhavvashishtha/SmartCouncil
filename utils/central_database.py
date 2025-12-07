import sqlite3
import json
import os

def save_data(data):
    os.makedirs('database', exist_ok=True)

    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect('database/central.db')
    cursor = conn.cursor()

    # Create tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            depends_on TEXT,
            agent TEXT NOT NULL,
            resolved BOOLEAN DEFAULT 0
        )
    ''')

    # Create completed_tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_tasks (
            done_task TEXT PRIMARY KEY,
            responses TEXT
        )
    ''')

    # Insert data into tasks table
    for task in data:
        cursor.execute('''
            INSERT OR REPLACE INTO tasks (id, description, depends_on, agent, resolved)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            task['id'],
            task['description'],
            json.dumps(task['depends_on']),  # Store list as JSON string
            task['agent'],
            False  # Set resolved to False
        ))

    # Commit and close
    conn.commit()
    conn.close()

    print("✓ Database created successfully at: database/central.db")
    print(f"✓ Inserted {len(data)} tasks")

    # Verify by reading back
    conn = sqlite3.connect('database/central.db')
    cursor = conn.cursor()
    
    # Check tasks table
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()

    print("\nVerification - Data in tasks table:")
    for row in rows:
        task_id, desc, deps, agent, resolved = row
        print(f"  {task_id}: {desc[:50]}... (depends on: {deps}, agent: {agent}, resolved: {resolved})")

    # Check completed_tasks table
    cursor.execute('SELECT * FROM completed_tasks')
    completed_rows = cursor.fetchall()
    
    print(f"\nVerification - Data in completed_tasks table:")
    if completed_rows:
        for row in completed_rows:
            done_task, responses = row
            print(f"  {done_task}: {responses}")
    else:
        print("  (empty - no tasks completed yet)")

    conn.close()

def get_ready_tasks():
    """Smart fetch: returns tasks ready for execution based on completed tasks."""
    conn = sqlite3.connect('database/central.db')
    cursor = conn.cursor()

    # Fetch completed tasks
    cursor.execute("SELECT done_task FROM completed_tasks")
    completed_rows = cursor.fetchall()

    completed_tasks = [row[0] for row in completed_rows]   # flatten

    # If no tasks are completed yet → return tasks with no dependencies
    if len(completed_tasks) == 0:
        cursor.execute('''
            SELECT id, description, depends_on, agent
            FROM tasks
            WHERE resolved = 0
        ''')
        
        rows = cursor.fetchall()
        conn.close()

        ready = []
        for task_id, desc, deps_json, agent in rows:
            deps = json.loads(deps_json) if deps_json else []
            if len(deps) == 0:   # only dependency-free tasks
                ready.append({
                    "id": task_id,
                    "description": desc,
                    "depends_on": deps,
                    "agent": agent
                })
        
        return ready

    # Otherwise → check dependency subset logic
    cursor.execute('''
        SELECT id, description, depends_on, agent
        FROM tasks
        WHERE resolved = 0
    ''')

    rows = cursor.fetchall()
    conn.close()

    ready_tasks = []

    for task_id, desc, deps_json, agent in rows:
        deps = json.loads(deps_json) if deps_json else []

        # If dependencies list ⊆ completed tasks → task is ready
        if set(deps).issubset(set(completed_tasks)):
            ready_tasks.append({
                "id": task_id,
                "description": desc,
                "depends_on": deps,
                "agent": agent
            })

    return ready_tasks

def resolve_tasks(task_ids):
    """Mark a list of task IDs as resolved=True in the database."""
    if not task_ids:
        return 0  # Nothing to update

    conn = sqlite3.connect('database/central.db')
    cursor = conn.cursor()

    # Use SQL IN clause to update multiple tasks at once
    placeholders = ",".join("?" for _ in task_ids)

    query = f'''
        UPDATE tasks
        SET resolved = 1
        WHERE id IN ({placeholders})
    '''

    cursor.execute(query, task_ids)

    conn.commit()
    conn.close()

    return cursor.rowcount  # number of tasks updated

def save_completed_tasks(results):
    """
    Save completed task results into completed_tasks table.
    Expects list of dicts like:
    [
        {
            "id": 1,
            "agent": "Exercise",
            "port": "8001",
            "status": 200,
            "response": {
                "success": True,
                "response": "...",
                "task_id": "t1",
                ...
            }
        }
    ]
    """
    db_path = "database/central.db"
    
    if not os.path.exists("database"):
        os.makedirs("database")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_tasks (
            done_task TEXT PRIMARY KEY,
            responses TEXT
        )
    ''')

    for item in results:
        try:
            resp = item.get("response", {})
            
            # Only save successful responses with a task_id
            if resp.get("success") and "task_id" in resp:
                task_id = resp["task_id"]
                response_text = resp["response"]   # only save the actual response string

                cursor.execute('''
                    INSERT OR REPLACE INTO completed_tasks (done_task, responses)
                    VALUES (?, ?)
                ''', (task_id, response_text))

        except Exception as e:
            print(f"⚠ Error saving a task: {e}")

    conn.commit()
    conn.close()

    print("✓ Completed tasks saved successfully.")

def get_completed_task_responses(task_ids):
    """
    Given a list of task IDs, return their saved responses from the completed_tasks table.
    
    Example input:
        ["t1", "t3", "t7"]

    Returns:
        [
            {"task_id": "t1", "response": "..."},
            {"task_id": "t3", "response": "..."},
        ]
    (Only returns tasks that exist in DB)
    """

    db_path = "database/central.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    results = []

    for task_id in task_ids:
        cursor.execute(
            "SELECT responses FROM completed_tasks WHERE done_task = ?",
            (task_id,)
        )
        row = cursor.fetchone()

        if row:  # Only append if found
            results.append({
                "task_id": task_id,
                "response": row[0]
            })

    conn.close()
    return results
