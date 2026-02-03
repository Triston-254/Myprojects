import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✅ To-Do List Manager")
        self.root.geometry("600x500")
        self.root.configure(bg='#f5f7fa')
        
        self.tasks = []
        self.filename = "tasks.json"
        
        # Load existing tasks
        self.load_tasks()
        
        # Colors
        self.colors = {
            'bg': '#f5f7fa',
            'card': '#ffffff',
            'primary': '#4a6fa5',
            'secondary': '#166088',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'text': '#2c3e50'
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            header_frame,
            text="📋 To-Do List Manager",
            font=('Arial', 20, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=10)
        
        # Date display
        date_str = datetime.now().strftime("%A, %B %d, %Y")
        tk.Label(
            header_frame,
            text=date_str,
            font=('Arial', 10),
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=(0, 10))
        
        # Task input section
        input_frame = tk.Frame(self.root, bg=self.colors['card'])
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            input_frame,
            text="New Task:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        # Task entry
        self.task_var = tk.StringVar()
        self.task_entry = tk.Entry(
            input_frame,
            textvariable=self.task_var,
            font=('Arial', 11),
            bg='white',
            fg=self.colors['text'],
            relief='flat',
            width=40
        )
        self.task_entry.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Priority combobox
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=["Low", "Medium", "High"],
            state="readonly",
            width=10
        )
        priority_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="➕ Add Task",
            command=self.add_task,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=15,
            pady=5
        )
        add_btn.pack(side=tk.LEFT, pady=5)
        
        # Task list frame
        list_frame = tk.Frame(self.root, bg=self.colors['bg'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 11),
            bg='white',
            fg=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief='flat',
            height=15,
            yscrollcommand=scrollbar.set
        )
        self.task_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Action buttons frame
        action_frame = tk.Frame(self.root, bg=self.colors['bg'])
        action_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        buttons = [
            ("✅ Complete", self.colors['success'], self.complete_task),
            ("✏️ Edit", self.colors['warning'], self.edit_task),
            ("🗑️ Delete", self.colors['danger'], self.delete_task),
            ("📊 Stats", self.colors['secondary'], self.show_stats),
            ("💾 Save", '#27ae60', self.save_tasks)
        ]
        
        for text, color, command in buttons:
            btn = tk.Button(
                action_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Arial', 10),
                relief='flat',
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value=f"Tasks: {len(self.tasks)}")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=('Arial', 9),
            bg=self.colors['primary'],
            fg='white',
            anchor='w',
            relief='sunken'
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Load tasks into listbox
        self.update_listbox()
    
    def add_task(self):
        """Add a new task"""
        task_text = self.task_var.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
        priority = self.priority_var.get()
        task = {
            'id': len(self.tasks) + 1,
            'text': task_text,
            'priority': priority,
            'completed': False,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.task_var.set("")
        self.update_listbox()
        self.save_tasks()
        messagebox.showinfo("Success", "Task added successfully!")
    
    def update_listbox(self):
        """Update the task listbox"""
        self.task_listbox.delete(0, tk.END)
        
        for task in self.tasks:
            status = "✓" if task['completed'] else "○"
            priority_color = {
                'High': '🔴',
                'Medium': '🟡',
                'Low': '🟢'
            }
            display_text = f"{status} {priority_color[task['priority']]} {task['text']}"
            
            if task['completed']:
                self.task_listbox.insert(tk.END, display_text)
                self.task_listbox.itemconfig(tk.END, {'fg': 'gray'})
            else:
                self.task_listbox.insert(tk.END, display_text)
        
        self.status_var.set(f"Tasks: {len(self.tasks)} | Completed: {sum(1 for t in self.tasks if t['completed'])}")
    
    def complete_task(self):
        """Mark selected task as complete"""
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks[index]['completed'] = True
            self.update_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def edit_task(self):
        """Edit selected task"""
        try:
            index = self.task_listbox.curselection()[0]
            task = self.tasks[index]
            
            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("400x200")
            edit_window.configure(bg=self.colors['bg'])
            
            tk.Label(
                edit_window,
                text="Edit Task:",
                font=('Arial', 12, 'bold'),
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(pady=10)
            
            edit_var = tk.StringVar(value=task['text'])
            edit_entry = tk.Entry(
                edit_window,
                textvariable=edit_var,
                font=('Arial', 11),
                width=40
            )
            edit_entry.pack(pady=10, padx=20)
            
            # Update button
            def update_task():
                task['text'] = edit_var.get().strip()
                if task['text']:
                    self.update_listbox()
                    self.save_tasks()
                    edit_window.destroy()
                    messagebox.showinfo("Success", "Task updated!")
                else:
                    messagebox.showwarning("Warning", "Task cannot be empty!")
            
            update_btn = tk.Button(
                edit_window,
                text="Update Task",
                command=update_task,
                bg=self.colors['primary'],
                fg='white',
                font=('Arial', 10, 'bold'),
                padx=15,
                pady=5
            )
            update_btn.pack(pady=10)
            
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit!")
    
    def delete_task(self):
        """Delete selected task"""
        try:
            index = self.task_listbox.curselection()[0]
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
                del self.tasks[index]
                self.update_listbox()
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def show_stats(self):
        """Show task statistics"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        
        stats_text = f"""
        📊 Task Statistics
        
        Total Tasks: {total}
        Completed: {completed}
        Pending: {pending}
        
        Completion Rate: {(completed/total*100):.1f}%""" if total > 0 else "No tasks yet!"
        
        messagebox.showinfo("Task Statistics", stats_text)
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()