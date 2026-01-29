import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar Generator")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.current_year = datetime.now().year
        self.year_var = tk.StringVar(value=str(self.current_year))
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
        # Generate initial calendar
        self.generate_calendar()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Year.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Month.TLabel', font=('Arial', 14, 'bold'), foreground='#2c3e50')
        style.configure('Weekday.TLabel', font=('Arial', 10, 'bold'), foreground='#34495e')
        style.configure('Day.TLabel', font=('Arial', 10))
        style.configure('Today.TLabel', font=('Arial', 10, 'bold'), foreground='#e74c3c')
        
        # Configure button style
        style.configure('Generate.TButton', font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="📅 Calendar Generator", 
            font=('Arial', 24, 'bold'),
            foreground='#2c3e50'
        )
        title_label.pack(side=tk.LEFT)
        
        # Year selection frame
        year_frame = ttk.Frame(header_frame)
        year_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(year_frame, text="Enter Year:", font=('Arial', 11)).pack(side=tk.LEFT, padx=(0, 5))
        
        year_entry = ttk.Entry(
            year_frame, 
            textvariable=self.year_var, 
            width=8, 
            font=('Arial', 11),
            justify='center'
        )
        year_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Generate button
        generate_btn = ttk.Button(
            year_frame,
            text="Generate Calendar",
            style='Generate.TButton',
            command=self.generate_calendar
        )
        generate_btn.pack(side=tk.LEFT)
        
        # Today button
        today_btn = ttk.Button(
            year_frame,
            text="Today",
            command=self.show_current_year
        )
        today_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Separator
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Calendar display frame with scrollbar
        self.calendar_frame_container = ttk.Frame(main_frame)
        self.calendar_frame_container.pack(fill=tk.BOTH, expand=True)
        
        # Add canvas for scrolling
        self.canvas = tk.Canvas(self.calendar_frame_container, bg='white')
        scrollbar = ttk.Scrollbar(self.calendar_frame_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def show_current_year(self):
        """Show calendar for current year"""
        self.year_var.set(str(self.current_year))
        self.generate_calendar()
    
    def generate_calendar(self):
        """Generate and display calendar for the selected year"""
        try:
            year = int(self.year_var.get())
            if year < 1 or year > 9999:
                messagebox.showerror("Invalid Year", "Please enter a year between 1 and 9999")
                return
            
            # Clear previous calendar
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            # Create months grid (4 rows x 3 columns)
            months_frame = ttk.Frame(self.scrollable_frame)
            months_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Year header
            year_label = ttk.Label(
                months_frame,
                text=f"📅 {year}",
                style='Year.TLabel',
                anchor='center'
            )
            year_label.grid(row=0, column=0, columnspan=3, pady=(0, 30))
            
            month_names = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            
            # Create each month's calendar
            for month_idx in range(12):
                row = (month_idx // 3) + 1  # +1 for year label row
                col = month_idx % 3
                
                # Month container
                month_container = ttk.Frame(
                    months_frame, 
                    relief='solid', 
                    borderwidth=1,
                    padding=10
                )
                month_container.grid(
                    row=row, 
                    column=col, 
                    padx=15, 
                    pady=15, 
                    sticky='nsew'
                )
                
                # Make the grid expandable
                months_frame.grid_rowconfigure(row, weight=1)
                months_frame.grid_columnconfigure(col, weight=1)
                
                # Month name
                month_label = ttk.Label(
                    month_container,
                    text=month_names[month_idx],
                    style='Month.TLabel'
                )
                month_label.pack(pady=(0, 10))
                
                # Weekday headers
                weekdays_frame = ttk.Frame(month_container)
                weekdays_frame.pack()
                
                weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
                for i, day in enumerate(weekdays):
                    day_label = ttk.Label(
                        weekdays_frame,
                        text=day,
                        style='Weekday.TLabel',
                        width=3,
                        anchor='center'
                    )
                    day_label.grid(row=0, column=i, padx=1, pady=1)
                
                # Get calendar matrix
                cal = calendar.monthcalendar(year, month_idx + 1)
                
                # Create days grid
                days_frame = ttk.Frame(month_container)
                days_frame.pack()
                
                today = datetime.now()
                is_current_month = (year == today.year and month_idx + 1 == today.month)
                
                # Display days
                for week_idx, week in enumerate(cal):
                    for day_idx, day in enumerate(week):
                        if day == 0:
                            # Empty cell for days outside the month
                            day_label = ttk.Label(
                                days_frame,
                                text="",
                                width=3
                            )
                        else:
                            # Check if this is today
                            is_today = (is_current_month and day == today.day)
                            
                            # Create day label with appropriate style
                            if is_today:
                                day_label = ttk.Label(
                                    days_frame,
                                    text=str(day),
                                    style='Today.TLabel',
                                    width=3,
                                    anchor='center',
                                    relief='solid',
                                    borderwidth=1,
                                    background='#ffebee'
                                )
                            else:
                                day_label = ttk.Label(
                                    days_frame,
                                    text=str(day),
                                    style='Day.TLabel',
                                    width=3,
                                    anchor='center'
                                )
                            
                            # Highlight weekends
                            if day_idx >= 5:  # Saturday or Sunday
                                if not is_today:
                                    day_label.configure(foreground='#7f8c8d')
                        
                        day_label.grid(row=week_idx + 1, column=day_idx, padx=1, pady=1)
            
            # Add footer with info
            footer_frame = ttk.Frame(self.scrollable_frame)
            footer_frame.pack(fill=tk.X, pady=(20, 10))
            
            info_text = f"• Calendar for year {year} • Today is highlighted in red"
            if calendar.isleap(year):
                info_text += f" • {year} is a leap year"
            
            footer_label = ttk.Label(
                footer_frame,
                text=info_text,
                font=('Arial', 10, 'italic'),
                foreground='#7f8c8d',
                anchor='center'
            )
            footer_label.pack()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid year (numeric value)")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()