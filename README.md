# Python GUI Todo List Application

A simple graphical Todo List application built with Python, using Tkinter for the GUI and SQLite for data storage. It features themed widgets using the `sv_ttk` library for a modern look and feel, including light and dark modes.

## Features

- Add new tasks with a text description.
- View all tasks in a scrollable list.
- Mark tasks as "completed" (visually distinguished in the list).
- Delete tasks from the list (with a confirmation dialog).
- Switch between light and dark themes for the application interface.
- Tasks are persisted in an SQLite database (`todo_list.db`), so they remain available between application sessions.

## Files

- `todo_app.py`: Manages the Tkinter GUI, event handling, user interactions, and theme switching.
- `database.py`: Handles all database operations, including table creation and CRUD (Create, Read, Update, Delete) functions for tasks.
- `todo_list.db`: (Generated on first run) The SQLite database file where tasks are stored.

## Prerequisites

- **Python 3.x:** Ensure Python 3 is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **sv_ttk Library:** This application uses the `sv_ttk` library for modern theming (including dark/light modes).

You can install `sv_ttk` using pip:
```bash
pip install sv_ttk
```
If you are using a virtual environment, activate it before running the pip install command.

The application also uses `tkinter` and `sqlite3`, which are part of the Python standard library, so no additional package installations are typically required for these.

## How to Run the Application

1.  **Get the Code:**
    *   Ensure you have the following files in the same folder (directory) on your computer:
        *   `todo_app.py`
        *   `database.py`

2.  **Install Dependencies:**
    *   Open your computer's terminal (Command Prompt, PowerShell, Terminal on macOS/Linux).
    *   Navigate to the folder where you saved the files.
    *   Install the `sv_ttk` library by running:
        ```bash
        pip install sv_ttk
        ```

3.  **Open Your Computer's Terminal (Command Line):** (If not already open)
    *   **Windows:** Search for "Command Prompt" or "PowerShell".
    *   **macOS:** Search for "Terminal" (usually in Applications > Utilities).
    *   **Linux:** Typically Ctrl+Alt+T or search for "Terminal".

4.  **Navigate to the Application Folder:** (If not already there)
    *   In the terminal, use the `cd` (change directory) command to go into the folder where you saved the Python files.
    *   For example, if you saved the files in a folder named `PythonTodoApp` on your Desktop:
        ```bash
        cd Desktop/PythonTodoApp
        ```
    *   *Tip:* After typing `cd ` (note the space), you can often drag the folder from your file explorer directly into the terminal window, and it will paste the correct path for you.

5.  **Run the Application:**
    *   Once your terminal is "inside" the correct folder (you should see the folder name in the terminal's prompt), type the following command and press Enter:
        ```bash
        python todo_app.py
        ```
    *   *Note:* If you have multiple Python versions installed, or if the `python` command doesn't point to Python 3, you might need to use `python3` instead:
        ```bash
        python3 todo_app.py
        ```

**Using the Application:**

*   Upon running, a window titled "Todo List App" will appear.
*   The first time you run the application, a file named `todo_list.db` will also be created in the same directory. This file stores your tasks. Do not delete it if you wish to keep your task data.
*   Use the "Switch to Dark Mode" / "Switch to Light Mode" button to change the application's theme.

```
