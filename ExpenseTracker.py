"""
Simple Expense Tracker - Works without matplotlib if needed
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date, timedelta
import sys

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available. Charts will be disabled.")

class ExpenseTracker:
    def __init__(self, data_file="expenses.json"):
        self.data_file = data_file
        self.expenses = self.load_expenses()
        self.categories = ["Food", "Transport", "Shopping", "Entertainment", 
                          "Bills", "Healthcare", "Education", "Other"]
    
    def load_expenses(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for expense in data:
                        expense['date'] = datetime.strptime(expense['date'], '%Y-%m-%d').date()
                    return data
            except:
                return []
        return []
    
    def save_expenses(self):
        data_to_save = []
        for expense in self.expenses:
            expense_copy = expense.copy()
            expense_copy['date'] = expense['date'].isoformat()
            data_to_save.append(expense_copy)
        
        with open(self.data_file, 'w') as f:
            json.dump(data_to_save, f, indent=2)
    
    def add_expense(self, category, amount, description=""):
        if amount <= 0:
            return False, "Amount must be positive"
        
        expense = {
            'date': date.today(),
            'category': category,
            'amount': amount,
            'description': description
        }
        
        self.expenses.append(expense)
        self.save_expenses()
        return True, "Expense added successfully"

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - KSh")
        self.root.geometry("1000x600")
        
        self.tracker = ExpenseTracker()
        self.setup_ui()
        self.refresh_display()
    
    def setup_ui(self):
        # Main frames
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel
        left_frame = tk.Frame(main_frame, relief=tk.RAISED, borderwidth=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Title
        tk.Label(left_frame, text="Expense Tracker", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Add expense form
        form_frame = tk.Frame(left_frame)
        form_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(form_frame, text="Category:").pack(anchor='w')
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var,
                                         values=self.tracker.categories)
        self.category_combo.pack(fill=tk.X, pady=(0, 10))
        self.category_combo.set("Food")
        
        tk.Label(form_frame, text="Amount (KSh):").pack(anchor='w')
        self.amount_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.amount_var).pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(form_frame, text="Description:").pack(anchor='w')
        self.desc_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.desc_var).pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(form_frame, text="Add Expense", command=self.add_expense,
                 bg='blue', fg='white').pack(pady=10)
        
        # Statistics
        stats_frame = tk.Frame(left_frame, relief=tk.GROOVE, borderwidth=1)
        stats_frame.pack(pady=20, padx=10, fill=tk.X)
        
        self.stats_label = tk.Label(stats_frame, text="", justify=tk.LEFT)
        self.stats_label.pack(pady=10, padx=10)
        
        # Right panel
        right_frame = tk.Frame(main_frame, relief=tk.RAISED, borderwidth=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Expense list
        tk.Label(right_frame, text="Expenses", font=('Arial', 14, 'bold')).pack(pady=10)
        
        columns = ('Date', 'Category', 'Amount', 'Description')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Buttons
        button_frame = tk.Frame(right_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Delete", command=self.delete_expense,
                 bg='red', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear All", command=self.clear_all,
                 bg='orange', fg='white').pack(side=tk.LEFT, padx=5)
        
        if not MATPLOTLIB_AVAILABLE:
            tk.Label(right_frame, text="\nNote: Install matplotlib for charts:\npip install matplotlib",
                    fg='red', font=('Arial', 10)).pack()
    
    def add_expense(self):
        category = self.category_var.get()
        amount_str = self.amount_var.get()
        description = self.desc_var.get()
        
        if not category:
            messagebox.showerror("Error", "Select category")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be > 0")
                return
        except:
            messagebox.showerror("Error", "Enter valid amount")
            return
        
        success, msg = self.tracker.add_expense(category, amount, description)
        if success:
            messagebox.showinfo("Success", f"Added: {category} - KSh {amount:,.2f}")
            self.amount_var.set("")
            self.desc_var.set("")
            self.refresh_display()
    
    def delete_expense(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        if messagebox.askyesno("Confirm", f"Delete {values[1]} - {values[2]}?"):
            # Simple deletion logic
            date_str, category, amount_str = values[0], values[1], values[2]
            amount = float(amount_str.replace(' KSh', '').replace(',', ''))
            
            for i, exp in enumerate(self.tracker.expenses):
                if (exp['date'].strftime('%Y-%m-%d') == date_str and
                    exp['category'] == category and
                    exp['amount'] == amount):
                    del self.tracker.expenses[i]
                    self.tracker.save_expenses()
                    self.refresh_display()
                    break
    
    def clear_all(self):
        if messagebox.askyesno("Confirm", "Clear ALL expenses?"):
            self.tracker.expenses = []
            self.tracker.save_expenses()
            self.refresh_display()
    
    def refresh_display(self):
        # Update tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for expense in self.tracker.expenses[-50:]:  # Show last 50
            date_str = expense['date'].strftime('%Y-%m-%d')
            amount_str = f"{expense['amount']:,.2f} KSh"
            self.tree.insert('', tk.END, values=(date_str, expense['category'],
                                               amount_str, expense['description']))
        
        # Update stats
        total = sum(exp['amount'] for exp in self.tracker.expenses)
        stats = f"Total Expenses: {len(self.tracker.expenses)}\n"
        stats += f"Total Amount: KSh {total:,.2f}\n\n"
        
        # Category breakdown
        categories = {}
        for exp in self.tracker.expenses:
            categories[exp['category']] = categories.get(exp['category'], 0) + exp['amount']
        
        for cat, amt in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            stats += f"{cat}: KSh {amt:,.2f}\n"
        
        self.stats_label.config(text=stats)

def main():
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()