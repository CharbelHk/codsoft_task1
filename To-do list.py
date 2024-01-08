import tkinter as tk
import json

class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.tasks = []

        self.task_entry = tk.Entry(self.root, width=40, font=('Arial', 12))
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task, font=('Arial', 10, 'bold'))
        self.add_button.pack()

        self.tasks_display = tk.Listbox(self.root, height=10, width=50, font=('Arial', 10))
        self.tasks_display.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task, font=('Arial', 10))
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.complete_button = tk.Button(self.root, text="Mark Complete", command=self.mark_as_complete, font=('Arial', 10))
        self.complete_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task, font=('Arial', 10))
        self.edit_button.pack(side=tk.LEFT, padx=5)

        # Load tasks from the file when the app starts
        self.load_tasks()


    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            new_task = Task(description=task_text)
            self.tasks.append(new_task)
            self.update_tasks_display()
            self.save_tasks()  # Save tasks after adding a new task
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        selected_task_index = self.tasks_display.curselection()
        if selected_task_index:
            index_to_delete = selected_task_index[0]
            del self.tasks[index_to_delete]
            self.update_tasks_display()
            self.save_tasks()  # Save tasks after deleting a task

    def mark_as_complete(self):
        selected_task_index = self.tasks_display.curselection()
        if selected_task_index:
            index_to_mark = selected_task_index[0]
            self.tasks[index_to_mark].completed = True
            self.update_tasks_display()
            self.save_tasks()  # Save tasks after marking a task as complete

    def edit_task(self):
        selected_task_index = self.tasks_display.curselection()
        if selected_task_index:
            index_to_edit = selected_task_index[0]
            new_text = self.task_entry.get()
            if new_text:
                self.tasks[index_to_edit].description = new_text
                self.update_tasks_display()
                self.save_tasks()  # Save tasks after editing a task
                self.task_entry.delete(0, tk.END)

    def update_tasks_display(self):
        self.tasks_display.delete(0, tk.END)
        for task in self.tasks:
            status = "[X]" if task.completed else "[ ]"
            self.tasks_display.insert(tk.END, f"{status} {task.description}")

    def save_tasks(self):
        tasks_data = [{'description': task.description, 'completed': task.completed} for task in self.tasks]
        with open('tasks.json', 'w') as file:
            json.dump(tasks_data, file)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                if isinstance(tasks_data, list):
                    self.tasks = [Task(task.get('description', ''), task.get('completed', False)) for task in tasks_data]
                    self.update_tasks_display()
                else:
                    self.tasks = []
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

def main():
    root = tk.Tk()
    todo_app = ToDoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
