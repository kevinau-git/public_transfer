import tkinter as tk
import datetime
from typing import TYPE_CHECKING

# Only import for type checking - won't cause runtime errors
if TYPE_CHECKING:
    from GridLayoutApp import GridLayoutApp

class ClickEventHandler:
    def __init__(self, app: 'GridLayoutApp'):
        """Initialize with reference to the main application"""
        self.app = app
        
            
        
    def on_tree_click(self, event):        
        """Handle tree click to toggle checkboxes"""
        region = self.app.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.app.tree.identify_column(event.x)
            if column == "#1":  # Checkbox column
                item = self.app.tree.identify_row(event.y)
                if item:
                    values = list(self.app.tree.item(item)["values"])
                    # Toggle checkbox
                    if values[0] == "☐":
                        values[0] = "☑"
                        self.app.log_to_console(f"Checked: {values[1]}")
                    else:
                        values[0] = "☐"
                        self.app.log_to_console(f"Unchecked: {values[1]}")
                    self.app.tree.item(item, values=values)
    
    def submit_data(self):
        """Submit data to treeview"""
        input_text = self.app.main_entry.get().strip()
        
        if not input_text:
            self.app.log_to_console("Error: Input field is required")
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
        self.app.tree.insert("", "end", values=("☐", name, value, type_val, timestamp))
        
        # Clear input field
        self.app.main_entry.delete(0, tk.END)
        
        self.app.log_to_console(f"Submitted: {name} = {value} ({type_val})")
    
    def clean_data(self):
        """Clean input field"""
        self.app.main_entry.delete(0, tk.END)
        self.app.log_to_console("Input field cleaned")
    
    def execute_delete(self):
        """Print checked items to console"""
        checked_items = []
        
        # Find all checked items
        for item in self.app.tree.get_children():
            values = self.app.tree.item(item)["values"]
            if values and values[0] == "☑":  # If checked
                checked_items.append({
                    "name": values[1],
                    "value": values[2], 
                    "type": values[3],
                    "timestamp": values[4]
                })
        
        if not checked_items:
            self.app.log_to_console("No checked items found")
            return
        
        self.app.log_to_console(f"=== Checked Items ({len(checked_items)}) ===")
        for i, item in enumerate(checked_items, 1):
            self.app.log_to_console(f"{i}. {item['name']} = {item['value']} ({item['type']}) [{item['timestamp']}]")
        self.app.log_to_console("=== End of Checked Items ===")
    
    # Menu option handlers
    def menu_option_1_1(self):
        """Handle File -> Option 1"""
        self.app.log_to_console("Menu: File -> Option 1 selected")
    
    def menu_option_1_2(self):
        """Handle File -> Option 2"""
        self.app.log_to_console("Menu: File -> Option 2 selected")
    
    def menu_option_1_3(self):
        """Handle File -> Option 3"""
        self.app.log_to_console("Menu: File -> Option 3 selected")
    
    def menu_option_2_1(self):
        """Handle Tools -> Settings"""
        self.app.log_to_console("Menu: Tools -> Settings selected")
