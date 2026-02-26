import tkinter as tk
from tkinter import ttk
import datetime

class GridLayoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Layout Application")
        self.root.geometry("600x500")
        
        # Configure grid weights for responsive layout
        for i in range(3):
            self.root.columnconfigure(i, weight=1)
        for i in range(5):
            self.root.rowconfigure(i, weight=0)  # Fixed size for input rows
        
        # Row 0 (info) - minimal height
        self.root.rowconfigure(0, weight=0)
        # Row 1 (input) - minimal height  
        self.root.rowconfigure(1, weight=0)
        # Row 2 (buttons) - minimal height
        self.root.rowconfigure(2, weight=0)
        # Row 3 (treeview) should expand most
        self.root.rowconfigure(3, weight=4)
        # Row 4 (console) should expand moderately
        self.root.rowconfigure(4, weight=2)
        
        # Create menu bar
        self.create_menu()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Row 1: Info label (spans 3 columns)
        self.info_label = tk.Label(
            self.root, 
            text="Grid Layout Application - Enter data and manage records", 
            bg="lightblue", 
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        self.info_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=2, pady=2)
        
        # Row 2: Single text input spanning 3 columns
        input_frame = tk.Frame(self.root)
        input_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=2, pady=2)
        input_frame.columnconfigure(0, weight=1)
        tk.Label(input_frame, text="Input:", font=("Arial", 9), anchor="w").grid(row=0, column=0, sticky="nw")
        self.main_entry = tk.Entry(input_frame, font=("Arial", 9))
        self.main_entry.grid(row=1, column=0, sticky="nsew")
        
        # Row 3: Buttons (3 columns)
        self.submit_btn = tk.Button(
            self.root, 
            text="Submit", 
            command=self.submit_data,
            bg="green",
            fg="white",
            font=("Arial", 9, "bold")
        )
        self.submit_btn.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        
        self.clean_btn = tk.Button(
            self.root, 
            text="Clean", 
            command=self.clean_data,
            bg="orange",
            fg="white",
            font=("Arial", 9, "bold")
        )
        self.clean_btn.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
        
        self.execute_del_btn = tk.Button(
            self.root, 
            text="Execute Del", 
            command=self.execute_delete,
            bg="red",
            fg="white",
            font=("Arial", 9, "bold")
        )
        self.execute_del_btn.grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
        
        # Row 4: Treeview (table-like list, spans 3 columns)
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=2, pady=2)
        
        # Configure treeview frame for auto-expansion
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)
        
        # Create treeview with scrollbars and checkbox column
        self.tree = ttk.Treeview(self.tree_frame, columns=("Checked", "Name", "Value", "Type", "Timestamp"), show="headings")
        
        # Define headings
        self.tree.heading("Checked", text="☐")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Value", text="Value")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Timestamp", text="Timestamp")
        
        # Configure column widths
        self.tree.column("Checked", width=30, minwidth=30)
        self.tree.column("Name", width=120)
        self.tree.column("Value", width=120)
        self.tree.column("Type", width=80)
        self.tree.column("Timestamp", width=150)
        
        # Bind click event to toggle checkboxes
        self.tree.bind("<Button-1>", self.on_tree_click)
        
        # Add scrollbars
        tree_scrolly = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        tree_scrollx = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scrolly.set, xscrollcommand=tree_scrollx.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scrolly.grid(row=0, column=1, sticky="ns")
        tree_scrollx.grid(row=1, column=0, sticky="ew")
        
        # Row 5: Console textarea (spans 3 columns)
        self.console_frame = tk.Frame(self.root)
        self.console_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=2, pady=2)
        
        # Configure console frame for auto-expansion
        self.console_frame.columnconfigure(0, weight=1)
        self.console_frame.rowconfigure(1, weight=1)  # Text area row expands
        
        # Console label
        tk.Label(self.console_frame, text="Console Output:", font=("Arial", 9, "bold"), anchor="w").grid(row=0, column=0, sticky="nw")
        
        # Console text area with scrollbar
        self.console_text = tk.Text(
            self.console_frame, 
            height=6, 
            font=("Courier", 8),
            bg="black",
            fg="green",
            wrap=tk.WORD
        )
        console_scrollbar = ttk.Scrollbar(self.console_frame, orient="vertical", command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=console_scrollbar.set)
        
        self.console_text.grid(row=1, column=0, sticky="nsew", pady=(2, 0))
        console_scrollbar.grid(row=1, column=1, sticky="ns", pady=(2, 0))
        
        # No need for additional grid weight configuration as it's already set above
        
        # Add some initial data
        self.add_sample_data()
        self.log_to_console("Application started successfully")
    
    def create_menu(self):
        """Create menu bar with submenus"""
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # First submenu with 3 options
        submenu1 = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=submenu1)
        submenu1.add_command(label="Option 1", command=self.menu_option_1_1)
        submenu1.add_command(label="Option 2", command=self.menu_option_1_2)
        submenu1.add_command(label="Option 3", command=self.menu_option_1_3)
        
        # Second submenu with 1 option
        submenu2 = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=submenu2)
        submenu2.add_command(label="Settings", command=self.menu_option_2_1)
    
    # Menu option handlers
    def menu_option_1_1(self):
        """Handle File -> Option 1"""
        self.log_to_console("Menu: File -> Option 1 selected")
    
    def menu_option_1_2(self):
        """Handle File -> Option 2"""
        self.log_to_console("Menu: File -> Option 2 selected")
    
    def menu_option_1_3(self):
        """Handle File -> Option 3"""
        self.log_to_console("Menu: File -> Option 3 selected")
    
    def menu_option_2_1(self):
        """Handle Tools -> Settings"""
        self.log_to_console("Menu: Tools -> Settings selected")
    
    def on_tree_click(self, event):
        """Handle tree click to toggle checkboxes"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#1":  # Checkbox column
                item = self.tree.identify_row(event.y)
                if item:
                    values = list(self.tree.item(item)["values"])
                    # Toggle checkbox
                    if values[0] == "☐":
                        values[0] = "☑"
                        self.log_to_console(f"Checked: {values[1]}")
                    else:
                        values[0] = "☐"
                        self.log_to_console(f"Unchecked: {values[1]}")
                    self.tree.item(item, values=values)
    
    def submit_data(self):
        """Submit data to treeview"""
        input_text = self.main_entry.get().strip()
        
        if not input_text:
            self.log_to_console("Error: Input field is required")
            return
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Parse input - if contains commas, split into name, value, type
        parts = [part.strip() for part in input_text.split(',')]
        if len(parts) >= 3:
            name, value, type_val = parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            name, value, type_val = parts[0], parts[1], ""
        else:
            name, value, type_val = input_text, "", ""
        
        # Insert into treeview with unchecked checkbox
        self.tree.insert("", "end", values=("☐", name, value, type_val, timestamp))
        
        # Clear input field
        self.main_entry.delete(0, tk.END)
        
        self.log_to_console(f"Submitted: {name} = {value} ({type_val})")
    
    def clean_data(self):
        """Clean input field"""
        self.main_entry.delete(0, tk.END)
        self.log_to_console("Input field cleaned")
    
    def execute_delete(self):
        """Print checked items to console"""
        checked_items = []
        
        # Find all checked items
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            if values and values[0] == "☑":  # If checked
                checked_items.append({
                    "name": values[1],
                    "value": values[2], 
                    "type": values[3],
                    "timestamp": values[4]
                })
        
        if not checked_items:
            self.log_to_console("No checked items found")
            return
        
        self.log_to_console(f"=== Checked Items ({len(checked_items)}) ===")
        for i, item in enumerate(checked_items, 1):
            self.log_to_console(f"{i}. {item['name']} = {item['value']} ({item['type']}) [{item['timestamp']}]")
        self.log_to_console("=== End of Checked Items ===")
    
    def add_sample_data(self):
        """Add some sample data to the treeview"""
        sample_data = [
            ("☐", "Sample1", "Value1", "String", "2026-02-26 10:00:00"),
            ("☐", "Sample2", "Value2", "Number", "2026-02-26 10:01:00"),
            ("☐", "Sample3", "Value3", "Boolean", "2026-02-26 10:02:00")
        ]
        
        for data in sample_data:
            self.tree.insert("", "end", values=data)
    
    def log_to_console(self, message):
        """Log message to console with timestamp"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.console_text.insert(tk.END, formatted_message)
        self.console_text.see(tk.END)  # Auto-scroll to bottom

def main():
    root = tk.Tk()
    app = GridLayoutApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
