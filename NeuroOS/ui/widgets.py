# ui/widgets.py
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable, Any

class ModernButton(tk.Button):
    """Modern styled button with hover effects"""
    def __init__(self, master, **kwargs):
        # Default style for modern button
        default_kwargs = {
            'bg': '#0078d7',
            'fg': 'white',
            'font': ('Arial', 10),
            'relief': 'flat',
            'bd': 0,
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2'
        }
        default_kwargs.update(kwargs)
        
        super().__init__(master, **default_kwargs)
        
        # Bind hover events
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        """Button hover effect"""
        self.config(bg='#106ebe')
    
    def _on_leave(self, event):
        """Button leave effect"""
        self.config(bg='#0078d7')

class SystemCard(tk.Frame):
    """System monitoring card widget"""
    def __init__(self, master, title: str, value: str = "0%", color: str = "#0078d7", **kwargs):
        super().__init__(master, bg='#252526', relief='flat', bd=1, **kwargs)
        
        # Title label
        self.title_label = tk.Label(self, text=title, font=("Arial", 10, "bold"),
                                  bg='#252526', fg='#888888')
        self.title_label.pack(anchor='w', padx=15, pady=(15, 5))
        
        # Value label
        self.value_label = tk.Label(self, text=value, font=("Arial", 18, "bold"),
                                  bg='#252526', fg=color)
        self.value_label.pack(expand=True)
        
        # Progress bar (optional)
        self.progress_bar = None
    
    def update_value(self, new_value: str, color: str = None):
        """Update the card value"""
        self.value_label.config(text=new_value)
        if color:
            self.value_label.config(fg=color)

class ConsoleOutput(scrolledtext.ScrolledText):
    """Enhanced console output widget"""
    def __init__(self, master, **kwargs):
        default_kwargs = {
            'bg': '#1e1e1e',
            'fg': '#cccccc',
            'insertbackground': 'white',
            'font': ('Consolas', 10),
            'wrap': tk.WORD,
            'state': 'disabled'
        }
        default_kwargs.update(kwargs)
        
        super().__init__(master, **default_kwargs)
    
    def write(self, text: str, tag: str = None):
        """Write text to console with optional formatting"""
        self.config(state='normal')
        
        if tag:
            self.insert('end', text, tag)
        else:
            self.insert('end', text)
        
        self.see('end')
        self.config(state='disabled')
    
    def clear(self):
        """Clear console content"""
        self.config(state='normal')
        self.delete('1.0', 'end')
        self.config(state='disabled')

class StatusIndicator(tk.Frame):
    """System status indicator widget"""
    def __init__(self, master, text: str = "STATUS", **kwargs):
        super().__init__(master, bg=master.cget('bg'), **kwargs)
        
        # Status indicator circle
        self.indicator = tk.Label(self, text="O", font=("Arial", 12),
                                bg=master.cget('bg'), fg='#4caf50')
        self.indicator.pack(side='left', padx=(0, 5))
        
        # Status text
        self.text_label = tk.Label(self, text=text, font=("Arial", 9, "bold"),
                                 bg=master.cget('bg'), fg='white')
        self.text_label.pack(side='left')
    
    def set_status(self, status: str, color: str = "#4caf50"):
        """Update status indicator"""
        self.text_label.config(text=status)
        self.indicator.config(fg=color)

class NavigationPanel(tk.Frame):
    """Side navigation panel"""
    def __init__(self, master, items: list, **kwargs):
        super().__init__(master, bg='#252526', **kwargs)
        
        self.items = items
        self.buttons = []
        self.current_selection = 0
        
        self.create_navigation()
    
    def create_navigation(self):
        """Create navigation buttons"""
        for i, (text, command) in enumerate(self.items):
            btn = tk.Button(self, text=text, font=("Arial", 10),
                          bg='#2d2d30', fg='#cccccc',
                          activebackground='#3e3e42', activeforeground='white',
                          relief='flat', height=2, anchor='w',
                          command=lambda cmd=command, idx=i: self.on_item_click(cmd, idx))
            btn.pack(fill='x', padx=10, pady=5)
            self.buttons.append(btn)
        
        # Highlight first item
        if self.buttons:
            self.buttons[0].config(bg='#0078d7', fg='white')
    
    def on_item_click(self, command: Callable, index: int):
        """Handle navigation item click"""
        # Reset all buttons
        for btn in self.buttons:
            btn.config(bg='#2d2d30', fg='#cccccc')
        
        # Highlight selected button
        self.buttons[index].config(bg='#0078d7', fg='white')
        self.current_selection = index
        
        # Execute command
        if command:
            command()

class ProgressBar(tk.Frame):
    """Custom progress bar widget"""
    def __init__(self, master, width=200, height=20, **kwargs):
        super().__init__(master, **kwargs)
        
        self.width = width
        self.height = height
        self.value = 0
        self.max_value = 100
        
        # Background frame
        self.bg_frame = tk.Frame(self, bg='#2d2d30', width=width, height=height)
        self.bg_frame.pack()
        self.bg_frame.pack_propagate(False)
        
        # Progress frame
        self.progress_frame = tk.Frame(self.bg_frame, bg='#0078d7', height=height)
        self.progress_frame.place(x=0, y=0, width=0)
        
        # Percentage label
        self.label = tk.Label(self.bg_frame, text="0%", font=("Arial", 8),
                            bg='#2d2d30', fg='white')
        self.label.place(relx=0.5, rely=0.5, anchor='center')
    
    def set_value(self, value: int):
        """Set progress bar value"""
        self.value = max(0, min(value, self.max_value))
        progress_width = (self.value / self.max_value) * self.width
        
        self.progress_frame.config(width=progress_width)
        self.label.config(text=f"{self.value}%")
        
        # Change color based on value
        if self.value > 80:
            self.progress_frame.config(bg='#ff5252')
        elif self.value > 60:
            self.progress_frame.config(bg='#ff9800')
        else:
            self.progress_frame.config(bg='#0078d7')

class SystemMetrics(tk.Frame):
    """System metrics display widget"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg='#252526', **kwargs)
        
        self.metrics = {}
        self.setup_metrics()
    
    def setup_metrics(self):
        """Setup metrics display"""
        metrics_config = [
            ("CPU", "cpu", "#ff5252"),
            ("Memory", "memory", "#4caf50"),
            ("Disk", "disk", "#2196f3"),
            ("Network", "network", "#ff9800")
        ]
        
        for i, (title, key, color) in enumerate(metrics_config):
            metric_frame = tk.Frame(self, bg='#252526')
            metric_frame.grid(row=0, column=i, padx=10, pady=5, sticky='nsew')
            
            # Title
            title_label = tk.Label(metric_frame, text=title, font=("Arial", 9),
                                 bg='#252526', fg='#888888')
            title_label.pack()
            
            # Value
            value_label = tk.Label(metric_frame, text="--%", font=("Arial", 12, "bold"),
                                 bg='#252526', fg=color)
            value_label.pack()
            
            self.metrics[key] = value_label
            
            self.columnconfigure(i, weight=1)
    
    def update_metric(self, key: str, value: str, color: str = None):
        """Update a specific metric"""
        if key in self.metrics:
            self.metrics[key].config(text=value)
            if color:
                self.metrics[key].config(fg=color)

class CommandHistory(tk.Frame):
    """Command history widget"""
    def __init__(self, master, max_history=50, **kwargs):
        super().__init__(master, **kwargs)
        
        self.max_history = max_history
        self.history = []
        self.current_index = -1
        
        self.setup_widgets()
    
    def setup_widgets(self):
        """Setup history widgets"""
        # History listbox
        self.listbox = tk.Listbox(self, bg='#1e1e1e', fg='#cccccc',
                                selectbackground='#0078d7', font=("Consolas", 9),
                                height=8)
        self.listbox.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.listbox)
        scrollbar.pack(side='right', fill='y')
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
    
    def add_command(self, command: str):
        """Add command to history"""
        self.history.append(command)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        self.listbox.insert('end', command)
        self.listbox.see('end')
        self.current_index = len(self.history) - 1
    
    def get_previous(self) -> str:
        """Get previous command from history"""
        if not self.history:
            return ""
        
        if self.current_index > 0:
            self.current_index -= 1
        return self.history[self.current_index]
    
    def get_next(self) -> str:
        """Get next command from history"""
        if not self.history:
            return ""
        
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]
        else:
            self.current_index = len(self.history)
            return ""

class NotificationBar(tk.Frame):
    """Notification bar for system messages"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg='#0078d7', height=30, **kwargs)
        self.pack_propagate(False)
        
        self.message_label = tk.Label(self, text="System ready", font=("Arial", 9),
                                    bg='#0078d7', fg='white')
        self.message_label.pack(side='left', padx=10)
        
        self.notifications = []
    
    def show_message(self, message: str, message_type: str = "info"):
        """Show a notification message"""
        colors = {
            "info": "#0078d7",
            "warning": "#ff9800",
            "error": "#ff5252",
            "success": "#4caf50"
        }
        
        color = colors.get(message_type, "#0078d7")
        self.config(bg=color)
        self.message_label.config(bg=color, text=message)
        
        # Auto-clear after 5 seconds
        self.after(5000, self.clear_message)
    
    def clear_message(self):
        """Clear the current message"""
        self.config(bg='#0078d7')
        self.message_label.config(bg='#0078d7', text="System ready")