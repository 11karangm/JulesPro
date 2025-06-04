import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database
import sv_ttk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")

        self.current_theme = "light"
        sv_ttk.set_theme(self.current_theme)

        self.root.geometry("450x650")

        database.init_db()

        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)

        self.task_entry = ttk.Entry(input_frame, width=35, font=('Arial', 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", self.add_task_event)

        self.add_task_button = ttk.Button(input_frame, text="Add Task", command=self.add_task_event)
        self.add_task_button.pack(side=tk.LEFT)

        list_frame = ttk.Frame(self.root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(list_frame, width=50, height=15, font=('Arial', 12), activestyle='none', borderwidth=0)
        # selectbackground is set in update_listbox_theme
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0))

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        action_buttons_frame = ttk.Frame(self.root)
        action_buttons_frame.pack(pady=(5,0))

        self.mark_complete_button = ttk.Button(action_buttons_frame, text="Mark as Complete", command=self.mark_task_complete_event)
        self.mark_complete_button.pack(side=tk.LEFT, padx=5)

        self.delete_task_button = ttk.Button(action_buttons_frame, text="Delete Task", command=self.delete_task_event)
        self.delete_task_button.pack(side=tk.LEFT, padx=5)

        theme_frame = ttk.Frame(self.root)
        theme_frame.pack(pady=(5,10))

        self.theme_toggle_button = ttk.Button(theme_frame, text="Switch to Dark Mode", command=self.toggle_theme)
        self.theme_toggle_button.pack(pady=5)

        # Initial setup of listbox theme and loading tasks
        self.update_listbox_theme() # This will also call load_tasks

    def toggle_theme(self):
        if self.current_theme == "light":
            sv_ttk.set_theme("dark")
            self.current_theme = "dark"
            self.theme_toggle_button.configure(text="Switch to Light Mode")
        else:
            sv_ttk.set_theme("light")
            self.current_theme = "light"
            self.theme_toggle_button.configure(text="Switch to Dark Mode")

        self.update_listbox_theme() # Apply new theme to listbox and reload tasks

    def update_listbox_theme(self):
        listbox_themes = {
            "light": {
                "bg": "white",
                "fg": "black",
                "selectbg": "#0078D4",
                "selectfg": "white"
            },
            "dark": {
                "bg": "#2b2b2b",
                "fg": "#cccccc",
                "selectbg": "#0078D4",
                "selectfg": "white"
            }
        }

        current_colors = listbox_themes.get(self.current_theme, listbox_themes["light"])

        self.task_listbox.configure(
            background=current_colors["bg"],
            foreground=current_colors["fg"], # Default text color for items
            selectbackground=current_colors["selectbg"],
            selectforeground=current_colors["selectfg"]
        )

        self.load_tasks() # Reload tasks to apply item-specific styling

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = database.get_tasks()

        if self.current_theme == "dark":
            pending_fg = "#cccccc"  # Light gray for pending tasks in dark mode
            completed_fg = "#777777" # Darker gray for completed tasks in dark mode
        else: # Light mode
            pending_fg = "black"    # Default text color from listbox config
            completed_fg = "gray"   # Standard gray for completed in light mode

        if tasks:
            for i, task_data in enumerate(tasks):
                task_description = task_data['task_description']
                task_status = task_data['status']
                task_id = task_data['id']

                visible_text = task_description

                current_item_fg = pending_fg
                if task_status == 'completed':
                    visible_text += " [DONE]"
                    current_item_fg = completed_fg

                full_display_text = f"{visible_text} (ID: {task_id}, Status: {task_status})"

                self.task_listbox.insert(tk.END, full_display_text)
                # Only set item-specific foreground if it differs from the Listbox's default foreground
                # or if it's a completed task that needs graying out.
                if task_status == 'completed' or current_item_fg != self.task_listbox.cget("foreground"):
                    self.task_listbox.itemconfig(i, {'fg': current_item_fg})

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
            selected_task_full_text = self.task_listbox.get(selected_index)

            id_part = selected_task_full_text.split(" (ID: ")[1]
            task_id = int(id_part.split(",")[0])
            return task_id
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task from the list.")
            return None
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", f"Could not retrieve task ID from selected item: '{selected_task_full_text}'. Please ensure tasks are loaded correctly.")
            return None

    def mark_task_complete_event(self):
        task_id = self.get_selected_task_id()
        if task_id is not None:
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


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
