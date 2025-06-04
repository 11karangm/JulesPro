import sqlite3

DB_NAME = "todo_list.db"

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Optional: to access columns by name
    return conn

def init_db():
    """Initializes the database and creates the tasks table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'completed'))
    )
    ''')

    conn.commit()
    conn.close()

def add_task(description: str):
    """Adds a new task to the database."""
    if not description.strip():
        # Optional: Basic validation to prevent empty tasks
        print("Task description cannot be empty.")
        return False

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO tasks (task_description) VALUES (?)", (description,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def get_tasks():
    """Retrieves all tasks from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, task_description, status FROM tasks ORDER BY id DESC")
        tasks = cursor.fetchall()
        return tasks # Returns a list of Row objects (or tuples if row_factory is not set)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def update_task_status(task_id: int, status: str):
    """Updates the status of a specific task."""
    if status not in ('pending', 'completed'):
        print(f"Invalid status: {status}. Must be 'pending' or 'completed'.")
        return False

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
        return cursor.rowcount > 0 # Returns True if a row was updated, False otherwise
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def delete_task(task_id: int):
    """Deletes a specific task from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0 # Returns True if a row was deleted, False otherwise
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    print(f"Database '{DB_NAME}' initialized/verified.")

    # Example Usage (optional - for testing database functions directly)
    # print("Attempting to add tasks...")
    # add_task("Buy groceries")
    # add_task("Finish report")
    # add_task("Call mom")

    # print("\nFetching all tasks:")
    # all_tasks = get_tasks()
    # if all_tasks:
    #     for task in all_tasks:
    #         print(f"ID: {task['id']}, Task: {task['task_description']}, Status: {task['status']}")
    # else:
    #     print("No tasks found.")

    # print("\nAttempting to update task 1 to 'completed'...")
    # if all_tasks:
    #     update_task_status(all_tasks[0]['id'], "completed")

    # print("\nFetching tasks again:")
    # for task in get_tasks():
    #     print(f"ID: {task['id']}, Task: {task['task_description']}, Status: {task['status']}")

    # print("\nAttempting to delete a task...")
    # if all_tasks and len(all_tasks) > 1:
    #    delete_task(all_tasks[1]['id'])

    # print("\nFetching tasks after deletion:")
    # for task in get_tasks():
    #     print(f"ID: {task['id']}, Task: {task['task_description']}, Status: {task['status']}")
