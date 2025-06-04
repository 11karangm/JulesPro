import tkinter as tk
from tkinter import messagebox
import database

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")
        self.root.geometry("450x600")

        database.init_db()

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, width=35, font=('Arial', 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", self.add_task_event)

        self.add_task_button = tk.Button(input_frame, text="Add Task", command=self.add_task_event, font=('Arial', 10))
        self.add_task_button.pack(side=tk.LEFT)

        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(list_frame, width=50, height=15, font=('Arial', 12), selectbackground="#a6a6a6", activestyle='none')
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0))

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        action_buttons_frame = tk.Frame(self.root)
        action_buttons_frame.pack(pady=10)

        self.mark_complete_button = tk.Button(action_buttons_frame, text="Mark as Complete", command=self.mark_task_complete_event, font=('Arial', 10))
        self.mark_complete_button.pack(side=tk.LEFT, padx=5)

        self.delete_task_button = tk.Button(action_buttons_frame, text="Delete Task", command=self.delete_task_event, font=('Arial', 10))
        self.delete_task_button.pack(side=tk.LEFT, padx=5)

        self.load_tasks()

    def add_task_event(self, event=None):
        task_description = self.task_entry.get().strip()
        if task_description:
            if database.add_task(task_description):
                self.load_tasks()
                self.task_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Database Error", "Failed to add task to the database.")
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty.")

    def get_selected_task_id(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            # The string stored in the listbox IS the full_display_text defined in load_tasks
            selected_task_full_text = self.task_listbox.get(selected_index)

            id_part = selected_task_full_text.split(" (ID: ")[1] # This expects " (ID: " to be present
            task_id = int(id_part.split(",")[0])
            return task_id
        except IndexError: # No selection
            messagebox.showwarning("Selection Error", "Please select a task from the list.")
            return None
        except (ValueError, IndexError) as e: # Parsing issue or other problem
             # Catch if " (ID: " is not found or int conversion fails
            messagebox.showerror("Error", f"Could not retrieve task ID from selected item: '{selected_task_full_text}'. Please ensure tasks are loaded correctly.")
            return None

    def mark_task_complete_event(self):
        task_id = self.get_selected_task_id()
        if task_id is not None:
            # For now, we just set to "completed".
            # A more advanced version could check current status to toggle or prevent re-marking.
            if database.update_task_status(task_id, "completed"):
                self.load_tasks()
            else:
                messagebox.showerror("Database Error", f"Failed to update task (ID: {task_id}) status.")

    def delete_task_event(self):
        task_id = self.get_selected_task_id()
        if task_id is not None:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this task?\n(ID: {task_id})")
            if confirm:
                if database.delete_task(task_id):
                    self.load_tasks()
                else:
                    messagebox.showerror("Database Error", f"Failed to delete task (ID: {task_id}).")

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = database.get_tasks() # This returns list of dicts/Rows
        if tasks:
            for i, task_data in enumerate(tasks): # task_data is a dict-like object from sqlite3.Row
                task_description = task_data['task_description']
                task_status = task_data['status']
                task_id = task_data['id']

                # User-visible part of the string
                visible_text = task_description
                if task_status == 'completed':
                    visible_text += " [DONE]"

                # String actually stored in the listbox, including metadata for parsing
                # This is what get_selected_task_id() will parse.
                # Format: "User visible text (ID: id, Status: status)"
                full_display_text = f"{visible_text} (ID: {task_id}, Status: {task_status})"

                self.task_listbox.insert(tk.END, full_display_text)
                if task_status == 'completed':
                    self.task_listbox.itemconfig(i, {'fg': 'gray'})
                else:
                    # Ensure pending tasks are not gray (use default text color)
                    self.task_listbox.itemconfig(i, {'fg': 'black'}) # Adjust 'black' if your default is different


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
