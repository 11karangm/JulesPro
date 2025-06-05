import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database
import sv_ttk

# Color Palette Constants
COLOR_WHITE = "#FFFFFF"
COLOR_BLACK = "#000000"
COLOR_RED = "#FF0000"
COLOR_DARK_RED = "#C00000"
COLOR_GRAY = "#808080"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App - Red/White/Black Theme")

        self.current_theme = "light" # Base for sv_ttk, our custom scheme is light-based
        sv_ttk.set_theme(self.current_theme)

        style = ttk.Style()

        try:
            style.map("TEntry",
                      # fieldbackground=[("focus", COLOR_WHITE)], # sv_ttk handles this
                      # bordercolor=[("focus", COLOR_RED)], # sv_ttk handles this
                     )
        except tk.TclError:
            print("Note: Could not apply some TEntry focus style settings, possibly due to theme constraints.")

        style.configure("Accent.TButton",
                        foreground=COLOR_DARK_RED,
                       )

        self.root.geometry("450x600")

        database.init_db()

        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)

        self.task_entry = ttk.Entry(input_frame, width=35, font=('Arial', 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", self.add_task_event)

        self.add_task_button = ttk.Button(input_frame, text="Add Task", command=self.add_task_event, style="Accent.TButton")
        self.add_task_button.pack(side=tk.LEFT)

        list_frame = ttk.Frame(self.root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(list_frame, width=50, height=15, font=('Arial', 12), activestyle='none', borderwidth=0)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0))

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        action_buttons_frame = ttk.Frame(self.root)
        action_buttons_frame.pack(pady=10)

        self.mark_complete_button = ttk.Button(action_buttons_frame, text="Mark as Complete", command=self.mark_task_complete_event)
        self.mark_complete_button.pack(side=tk.LEFT, padx=5)

        self.delete_task_button = ttk.Button(action_buttons_frame, text="Delete Task", command=self.delete_task_event)
        self.delete_task_button.pack(side=tk.LEFT, padx=5)

        # Ensure theme toggle button and its frame are commented out or removed.
        # self.theme_frame = ttk.Frame(self.root)
        # self.theme_frame.pack(pady=(0,10))
        # self.theme_toggle_button = ttk.Button(self.theme_frame, text="Switch Theme", command=self.toggle_theme)
        # self.theme_toggle_button.pack(pady=5)

        self._apply_listbox_theme_colors()
        self.load_tasks()

    def _apply_listbox_theme_colors(self):
        self.task_listbox.configure(
            background=COLOR_WHITE,
            foreground=COLOR_BLACK,
            selectbackground=COLOR_RED,
            selectforeground=COLOR_WHITE,
            highlightthickness=1,
            highlightbackground=COLOR_BLACK,
            highlightcolor=COLOR_RED
        )

    # Ensure the toggle_theme method is commented out or removed.
    # def toggle_theme(self):
    #     # This method is not used as the theme is fixed to the custom red/white/black scheme.
    #     # if self.current_theme == "light":
    #     #     sv_ttk.set_theme("dark")
    #     #     self.current_theme = "dark"
    #     # else:
    #     #     sv_ttk.set_theme("light")
    #     #     self.current_theme = "light"
    #     # self._apply_listbox_theme_colors()
    #     # self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = database.get_tasks()

        pending_fg = COLOR_BLACK
        completed_fg = COLOR_GRAY

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
