import sqlite3
import json
import os

def save_data(data):
    os.makedirs('database', exist_ok=True)

    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect('database/central.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            depends_on TEXT,
            agent TEXT NOT NULL,
            resolved BOOLEAN DEFAULT 0
        )
    ''')

    # Insert data
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
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()

    print("\nVerification - Data in database:")
    for row in rows:
        task_id, desc, deps, agent, resolved = row
        print(f"  {task_id}: {desc[:50]}... (depends on: {deps}, agent: {agent}, resolved: {resolved})")

    conn.close()