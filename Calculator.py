#!/usr/bin/env python3
"""
Complete Calculator Application
Includes both GUI and command-line interfaces
"""

import sys
import math
import re
from typing import Optional, Tuple

# ============================================================================
# Part 1: Core Calculator Engine
# ============================================================================

class CalculatorEngine:
    """Handles all mathematical operations and calculations"""
    
    def __init__(self):
        self.current_value = 0.0
        self.memory = 0.0
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        """Addition: a + b"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtraction: a - b"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplication: a * b"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Division: a / b"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, a: float, b: float) -> float:
        """Power: a ^ b"""
        return a ** b
    
    def square_root(self, a: float) -> float:
        """Square root: √a"""
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(a)
    
    def factorial(self, a: float) -> int:
        """Factorial: a!"""
        if a < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if not isinstance(a, int):
            a = int(a)
        return math.factorial(a)
    
    def sin(self, a: float, degrees: bool = False) -> float:
        """Sine function"""
        if degrees:
            a = math.radians(a)
        return math.sin(a)
    
    def cos(self, a: float, degrees: bool = False) -> float:
        """Cosine function"""
        if degrees:
            a = math.radians(a)
        return math.cos(a)
    
    def tan(self, a: float, degrees: bool = False) -> float:
        """Tangent function"""
        if degrees:
            a = math.radians(a)
        return math.tan(a)
    
    def log(self, a: float, base: float = 10) -> float:
        """Logarithm"""
        if a <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        if base == 10:
            return math.log10(a)
        elif base == 2:
            return math.log2(a)
        else:
            return math.log(a, base)
    
    def ln(self, a: float) -> float:
        """Natural logarithm"""
        if a <= 0:
            raise ValueError("Natural logarithm undefined for non-positive numbers")
        return math.log(a)
    
    def percent(self, a: float) -> float:
        """Convert to percentage"""
        return a / 100
    
    def memory_store(self, value: float):
        """Store value in memory"""
        self.memory = value
    
    def memory_recall(self) -> float:
        """Recall value from memory"""
        return self.memory
    
    def memory_add(self, value: float):
        """Add to memory"""
        self.memory += value
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0.0
    
    def add_to_history(self, operation: str, result: float):
        """Add calculation to history"""
        self.history.append(f"{operation} = {result}")
        if len(self.history) > 10:
            self.history.pop(0)
    
    def clear_history(self):
        """Clear calculation history"""
        self.history.clear()
    
    def get_history(self) -> list:
        """Get calculation history"""
        return self.history.copy()

# ============================================================================
# Part 2: Command-Line Interface (CLI)
# ============================================================================

class CommandLineCalculator:
    """Command-line calculator interface"""
    
    def __init__(self):
        self.calc = CalculatorEngine()
        self.running = True
    
    def display_menu(self):
        """Display calculator menu"""
        print("\n" + "="*50)
        print("COMMAND LINE CALCULATOR")
        print("="*50)
        print("Basic Operations:")
        print("  + : Addition")
        print("  - : Subtraction")
        print("  * : Multiplication")
        print("  / : Division")
        print("  ^ : Power")
        print("  √ : Square Root")
        print("  ! : Factorial")
        print("\nScientific Functions:")
        print("  sin : Sine")
        print("  cos : Cosine")
        print("  tan : Tangent")
        print("  log : Logarithm (base 10)")
        print("  ln  : Natural Logarithm")
        print("\nMemory Operations:")
        print("  ms  : Memory Store")
        print("  mr  : Memory Recall")
        print("  m+  : Memory Add")
        print("  mc  : Memory Clear")
        print("\nOther Commands:")
        print("  h   : History")
        print("  c   : Clear History")
        print("  m   : Menu")
        print("  q   : Quit")
        print("="*50)
    
    def get_number(self, prompt: str) -> Optional[float]:
        """Get a number from user input"""
        while True:
            try:
                value = input(prompt)
                if value.lower() == 'q':
                    return None
                return float(value)
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def handle_basic_operation(self, operation: str):
        """Handle basic arithmetic operations"""
        try:
            a = self.get_number("Enter first number: ")
            if a is None:
                return
            
            b = self.get_number("Enter second number: ")
            if b is None:
                return
            
            result = 0
            
            if operation == '+':
                result = self.calc.add(a, b)
                operation_str = f"{a} + {b}"
            elif operation == '-':
                result = self.calc.subtract(a, b)
                operation_str = f"{a} - {b}"
            elif operation == '*':
                result = self.calc.multiply(a, b)
                operation_str = f"{a} × {b}"
            elif operation == '/':
                result = self.calc.divide(a, b)
                operation_str = f"{a} ÷ {b}"
            elif operation == '^':
                result = self.calc.power(a, b)
                operation_str = f"{a} ^ {b}"
            
            print(f"\nResult: {operation_str} = {result}")
            self.calc.add_to_history(operation_str, result)
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def handle_function(self, func: str):
        """Handle scientific functions"""
        try:
            a = self.get_number("Enter number: ")
            if a is None:
                return
            
            result = 0
            operation_str = ""
            
            if func == 'sqrt':
                result = self.calc.square_root(a)
                operation_str = f"√{a}"
            elif func == 'fact':
                result = self.calc.factorial(a)
                operation_str = f"{a}!"
            elif func == 'sin':
                result = self.calc.sin(a, degrees=True)
                operation_str = f"sin({a}°)"
            elif func == 'cos':
                result = self.calc.cos(a, degrees=True)
                operation_str = f"cos({a}°)"
            elif func == 'tan':
                result = self.calc.tan(a, degrees=True)
                operation_str = f"tan({a}°)"
            elif func == 'log':
                result = self.calc.log(a)
                operation_str = f"log({a})"
            elif func == 'ln':
                result = self.calc.ln(a)
                operation_str = f"ln({a})"
            elif func == '%':
                result = self.calc.percent(a)
                operation_str = f"{a}%"
            
            print(f"\nResult: {operation_str} = {result}")
            self.calc.add_to_history(operation_str, result)
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def handle_memory(self, command: str):
        """Handle memory operations"""
        if command == 'ms':
            value = self.get_number("Enter value to store: ")
            if value is not None:
                self.calc.memory_store(value)
                print(f"Stored {value} in memory")
        elif command == 'mr':
            value = self.calc.memory_recall()
            print(f"Memory recall: {value}")
        elif command == 'm+':
            value = self.get_number("Enter value to add to memory: ")
            if value is not None:
                self.calc.memory_add(value)
                print(f"Added {value} to memory")
        elif command == 'mc':
            self.calc.memory_clear()
            print("Memory cleared")
    
    def run(self):
        """Run the command-line calculator"""
        self.display_menu()
        
        while self.running:
            print("\nEnter operation or command (m for menu): ", end="")
            command = input().strip().lower()
            
            if command == 'q':
                print("Goodbye!")
                self.running = False
            elif command == 'm':
                self.display_menu()
            elif command == 'h':
                history = self.calc.get_history()
                if history:
                    print("\nCalculation History:")
                    for i, calc in enumerate(history, 1):
                        print(f"  {i}. {calc}")
                else:
                    print("No history available")
            elif command == 'c':
                self.calc.clear_history()
                print("History cleared")
            elif command in ['+', '-', '*', '/', '^']:
                self.handle_basic_operation(command)
            elif command in ['sqrt', 'fact', 'sin', 'cos', 'tan', 'log', 'ln', '%']:
                self.handle_function(command)
            elif command in ['ms', 'mr', 'm+', 'mc']:
                self.handle_memory(command)
            else:
                print("Invalid command. Type 'm' to see the menu.")

# ============================================================================
# Part 3: Graphical User Interface (GUI)
# ============================================================================

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

if GUI_AVAILABLE:
    class GraphicalCalculator:
        """Graphical calculator interface using Tkinter"""
        
        def __init__(self, root):
            self.root = root
            self.root.title("Python Calculator")
            self.root.geometry("500x700")
            self.root.resizable(True, True)
            
            # Initialize calculator engine
            self.calc = CalculatorEngine()
            
            # Variables
            self.display_text = tk.StringVar(value="0")
            self.expression_text = tk.StringVar(value="")
            self.current_input = ""
            self.last_operation = ""
            self.reset_display = False
            
            # Configure colors
            self.setup_styles()
            
            # Build the interface
            self.setup_ui()
            
            # Bind keyboard
            self.root.bind('<Key>', self.on_key_press)
        
        def setup_styles(self):
            """Setup color scheme and styles"""
            self.bg_color = "#1e1e1e"
            self.display_bg = "#2d2d2d"
            self.display_fg = "#ffffff"
            self.button_bg = "#3c3c3c"
            self.button_fg = "#ffffff"
            self.operator_bg = "#ff9500"
            self.special_bg = "#a6a6a6"
            self.history_bg = "#252525"
            self.history_fg = "#cccccc"
            
            self.root.configure(bg=self.bg_color)
        
        def setup_ui(self):
            """Setup the user interface"""
            # Main container
            main_frame = tk.Frame(self.root, bg=self.bg_color)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Display section
            display_frame = tk.Frame(main_frame, bg=self.display_bg, height=120)
            display_frame.pack(fill=tk.X, pady=(0, 10))
            display_frame.pack_propagate(False)
            
            # Expression display (smaller, shows full expression)
            expression_label = tk.Label(
                display_frame,
                textvariable=self.expression_text,
                bg=self.display_bg,
                fg="#888888",
                font=("Arial", 12),
                anchor=tk.E,
                padx=20
            )
            expression_label.pack(fill=tk.X, pady=(10, 5))
            
            # Main display
            display_label = tk.Label(
                display_frame,
                textvariable=self.display_text,
                bg=self.display_bg,
                fg=self.display_fg,
                font=("Arial", 36, "bold"),
                anchor=tk.E,
                padx=20
            )
            display_label.pack(fill=tk.BOTH, expand=True)
            
            # History display
            history_frame = tk.Frame(main_frame, bg=self.history_bg)
            history_frame.pack(fill=tk.X, pady=(0, 10))
            
            history_label = tk.Label(
                history_frame,
                text="History",
                bg=self.history_bg,
                fg=self.history_fg,
                font=("Arial", 10, "bold")
            )
            history_label.pack(anchor=tk.W, padx=10, pady=(5, 0))
            
            self.history_text = scrolledtext.ScrolledText(
                history_frame,
                height=4,
                bg=self.history_bg,
                fg=self.history_fg,
                font=("Courier", 9),
                relief=tk.FLAT,
                borderwidth=0
            )
            self.history_text.pack(fill=tk.X, padx=10, pady=(0, 5))
            self.history_text.configure(state='disabled')
            
            # Button frames
            buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
            buttons_frame.pack(fill=tk.BOTH, expand=True)
            
            # First row - Memory and special buttons
            mem_frame = tk.Frame(buttons_frame, bg=self.bg_color)
            mem_frame.pack(fill=tk.X)
            
            mem_buttons = [
                ("MC", self.memory_clear),
                ("MR", self.memory_recall),
                ("M+", self.memory_add),
                ("MS", self.memory_store),
                ("C", self.clear_all),
                ("⌫", self.backspace)
            ]
            
            for text, command in mem_buttons:
                btn = tk.Button(
                    mem_frame,
                    text=text,
                    font=("Arial", 12),
                    bg=self.special_bg,
                    fg=self.button_fg,
                    relief=tk.FLAT,
                    command=command
                )
                btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2)
            
            # Scientific buttons
            sci_frame = tk.Frame(buttons_frame, bg=self.bg_color)
            sci_frame.pack(fill=tk.X)
            
            sci_buttons = [
                ("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
                ("log", "log("), ("ln", "ln("), ("√", "√"),
                ("x²", "²"), ("x³", "³"), ("10ˣ", "10^"),
                ("π", "π"), ("e", "e"), ("n!", "!"),
                ("(", "("), (")", ")"), ("%", "%"), (".", ".")
            ]
            
            cols = 5
            for i, (text, value) in enumerate(sci_buttons):
                row = i // cols
                col = i % cols
                
                if row == 0:
                    frame = sci_frame
                else:
                    if col == 0:
                        frame = tk.Frame(sci_frame, bg=self.bg_color)
                        frame.pack(fill=tk.X)
                
                btn = tk.Button(
                    frame,
                    text=text,
                    font=("Arial", 12),
                    bg=self.button_bg,
                    fg=self.button_fg,
                    relief=tk.FLAT,
                    command=lambda v=value: self.add_to_expression(v)
                )
                btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=2)
            
            # Main calculator buttons
            main_buttons = [
                [
                    ("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/"),
                ],
                [
                    ("4", "4"), ("5", "5"), ("6", "6"), ("×", "*"),
                ],
                [
                    ("1", "1"), ("2", "2"), ("3", "3"), ("−", "-"),
                ],
                [
                    ("0", "0"), (".", "."), ("=", "="), ("+", "+"),
                ]
            ]
            
            for row_buttons in main_buttons:
                frame = tk.Frame(buttons_frame, bg=self.bg_color)
                frame.pack(fill=tk.BOTH, expand=True)
                
                for text, value in row_buttons:
                    if text == "=":
                        bg = self.operator_bg
                        cmd = self.calculate
                    elif text in ["÷", "×", "−", "+"]:
                        bg = self.operator_bg
                        cmd = lambda v=value: self.add_to_expression(v)
                    elif text == "0":
                        bg = self.button_bg
                        cmd = lambda v=value: self.add_to_expression(v)
                    else:
                        bg = self.button_bg
                        cmd = lambda v=value: self.add_to_expression(v)
                    
                    btn = tk.Button(
                        frame,
                        text=text,
                        font=("Arial", 18),
                        bg=bg,
                        fg=self.button_fg,
                        relief=tk.FLAT,
                        command=cmd
                    )
                    btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2, pady=2)
        
        def add_to_expression(self, value):
            """Add value to current expression"""
            if self.reset_display:
                self.current_input = ""
                self.reset_display = False
            
            if value == "=":
                self.calculate()
                return
            
            # Handle special cases
            if value == "²":
                self.current_input += "**2"
            elif value == "³":
                self.current_input += "**3"
            elif value == "√":
                self.current_input += "math.sqrt("
            elif value in ["sin(", "cos(", "tan(", "log(", "ln("]:
                self.current_input += value
            else:
                self.current_input += value
            
            self.update_display()
        
        def update_display(self):
            """Update the display with current input"""
            display = self.current_input if self.current_input else "0"
            self.display_text.set(display)
        
        def calculate(self):
            """Calculate the current expression"""
            if not self.current_input:
                return
            
            try:
                # Prepare expression for evaluation
                expr = self.current_input
                
                # Replace display symbols with Python math symbols
                expr = expr.replace("×", "*")
                expr = expr.replace("÷", "/")
                expr = expr.replace("−", "-")
                expr = expr.replace("^", "**")
                
                # Handle percentage
                if "%" in expr:
                    expr = expr.replace("%", "/100")
                
                # Handle factorial
                import re
                expr = re.sub(r'(\d+)!', r'math.factorial(\1)', expr)
                
                # Safe evaluation
                allowed_names = {
                    k: v for k, v in math.__dict__.items() 
                    if not k.startswith("__")
                }
                
                result = eval(expr, {"__builtins__": {}}, allowed_names)
                
                # Update expression display
                self.expression_text.set(f"{self.current_input} =")
                
                # Update current input with result
                self.current_input = str(result)
                self.update_display()
                
                # Add to history
                history_entry = f"{self.current_input} = {result}"
                self.calc.add_to_history(history_entry, result)
                self.update_history()
                
                # Set flag to reset on next input
                self.reset_display = True
                
            except Exception as e:
                messagebox.showerror("Calculation Error", f"Error: {str(e)}")
        
        def clear_all(self):
            """Clear all inputs and display"""
            self.current_input = ""
            self.expression_text.set("")
            self.display_text.set("0")
            self.reset_display = False
        
        def backspace(self):
            """Remove last character from input"""
            if self.current_input:
                self.current_input = self.current_input[:-1]
                self.update_display()
        
        def memory_store(self):
            """Store current value in memory"""
            try:
                value = float(self.display_text.get())
                self.calc.memory_store(value)
                messagebox.showinfo("Memory", f"Stored {value} in memory")
            except:
                messagebox.showerror("Error", "Invalid value for memory storage")
        
        def memory_recall(self):
            """Recall value from memory"""
            value = self.calc.memory_recall()
            self.current_input = str(value)
            self.update_display()
        
        def memory_add(self):
            """Add current value to memory"""
            try:
                value = float(self.display_text.get())
                self.calc.memory_add(value)
                messagebox.showinfo("Memory", f"Added {value} to memory")
            except:
                messagebox.showerror("Error", "Invalid value for memory operation")
        
        def memory_clear(self):
            """Clear memory"""
            self.calc.memory_clear()
            messagebox.showinfo("Memory", "Memory cleared")
        
        def update_history(self):
            """Update history display"""
            history = self.calc.get_history()
            self.history_text.configure(state='normal')
            self.history_text.delete(1.0, tk.END)
            
            for entry in reversed(history):
                self.history_text.insert(tk.END, entry + "\n")
            
            self.history_text.configure(state='disabled')
            self.history_text.see(tk.END)
        
        def on_key_press(self, event):
            """Handle keyboard input"""
            key = event.char
            
            if key.isdigit() or key in '+-*/.()':
                self.add_to_expression(key)
            elif key == '\r':  # Enter key
                self.calculate()
            elif key == '\x08':  # Backspace key
                self.backspace()
            elif key == '\x1b':  # Escape key
                self.clear_all()
            elif key.lower() == 'c':
                self.clear_all()

# ============================================================================
# Part 4: Main Application Controller
# ============================================================================

def main():
    """Main function to run the calculator application"""
    print("="*60)
    print("PYTHON CALCULATOR APPLICATION")
    print("="*60)
    print("\nAvailable interfaces:")
    print("1. Command Line Interface (CLI)")
    
    if GUI_AVAILABLE:
        print("2. Graphical User Interface (GUI)")
        print("3. Exit")
    else:
        print("2. Exit (GUI not available - tkinter missing)")
    
    print("\n" + "="*60)
    
    while True:
        try:
            if GUI_AVAILABLE:
                choice = input("Choose interface (1-3): ").strip()
                valid_choices = ['1', '2', '3']
            else:
                choice = input("Choose interface (1-2): ").strip()
                valid_choices = ['1', '2']
            
            if choice not in valid_choices:
                print("Invalid choice. Please try again.")
                continue
            
            if choice == '1':
                # Run CLI calculator
                cli_calc = CommandLineCalculator()
                cli_calc.run()
                break
            
            elif choice == '2' and GUI_AVAILABLE:
                # Run GUI calculator
                root = tk.Tk()
                app = GraphicalCalculator(root)
                root.mainloop()
                break
            
            elif choice == '2' and not GUI_AVAILABLE:
                print("Goodbye!")
                break
            
            elif choice == '3':
                print("Goodbye!")
                break
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

# ============================================================================
# Part 5: Expression Parser (Advanced Feature)
# ============================================================================

class ExpressionParser:
    """Advanced mathematical expression parser"""
    
    @staticmethod
    def parse_expression(expr: str) -> float:
        """Parse and evaluate a mathematical expression"""
        # Remove whitespace
        expr = expr.strip()
        
        if not expr:
            raise ValueError("Empty expression")
        
        # Check for invalid characters
        valid_pattern = r'^[0-9+\-*/().\s^!√πe\sincostanlog]+$'
        if not re.match(valid_pattern, expr.replace(" ", "")):
            raise ValueError("Invalid characters in expression")
        
        # Replace symbols
        expr = expr.replace("^", "**")
        expr = expr.replace("√", "math.sqrt")
        expr = expr.replace("π", str(math.pi))
        expr = expr.replace("e", str(math.e))
        
        # Handle functions
        expr = re.sub(r'sin\(', 'math.sin(math.radians(', expr)
        expr = re.sub(r'cos\(', 'math.cos(math.radians(', expr)
        expr = re.sub(r'tan\(', 'math.tan(math.radians(', expr)
        expr = re.sub(r'log\(', 'math.log10(', expr)
        expr = re.sub(r'ln\(', 'math.log(', expr)
        
        # Handle factorial
        expr = re.sub(r'(\d+)!', r'math.factorial(\1)', expr)
        
        # Safe evaluation
        allowed_names = {k: v for k, v in math.__dict__.items() 
                        if not k.startswith("__")}
        
        try:
            result = eval(expr, {"__builtins__": {}}, allowed_names)
            return result
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")

# ============================================================================
# Run the application
# ============================================================================

if __name__ == "__main__":
    main()