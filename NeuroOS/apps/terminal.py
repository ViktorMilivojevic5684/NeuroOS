# apps/terminal.py
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import os

class TerminalEmulator:
    """Basic terminal emulator for NeuroOS"""
    def __init__(self, master):
        self.master = master
        self.current_directory = os.getcwd()
        self.command_history = []
        self.history_index = 0
        
        self.setup_terminal()
    
    def setup_terminal(self):
        """Setup terminal interface"""
        # Terminal output area
        self.output_area = scrolledtext.ScrolledText(
            self.master, 
            bg='#1e1e1e', 
            fg='#00ff00',
            font=('Consolas', 11),
            wrap=tk.WORD,
            state='disabled'
        )
        self.output_area.pack(fill='both', expand=True)
        
        # Command input area
        input_frame = tk.Frame(self.master, bg='#1e1e1e')
        input_frame.pack(fill='x', padx=5, pady=5)
        
        self.prompt_label = tk.Label(input_frame, text="$", 
                                   bg='#1e1e1e', fg='#00ff00',
                                   font=('Consolas', 11))
        self.prompt_label.pack(side='left')
        
        self.command_entry = tk.Entry(input_frame, bg='#1e1e1e', fg='#00ff00',
                                    insertbackground='#00ff00',
                                    font=('Consolas', 11),
                                    relief='flat')
        self.command_entry.pack(side='left', fill='x', expand=True, padx=(5, 0))
        self.command_entry.bind('<Return>', self.execute_command)
        self.command_entry.bind('<Up>', self.previous_command)
        self.command_entry.bind('<Down>', self.next_command)
        self.command_entry.focus()
        
        # Welcome message
        self.write_output("NeuroOS Terminal v1.0\nType 'help' for available commands\n\n")
    
    def write_output(self, text: str):
        """Write text to terminal output"""
        self.output_area.config(state='normal')
        self.output_area.insert('end', text)
        self.output_area.see('end')
        self.output_area.config(state='disabled')
    
    def execute_command(self, event=None):
        """Execute terminal command"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Show command in output
        self.write_output(f"$ {command}\n")
        
        # Clear input
        self.command_entry.delete(0, 'end')
        
        # Execute command in thread
        threading.Thread(target=self._execute_command, args=(command,), daemon=True).start()
    
    def _execute_command(self, command: str):
        """Execute command in background"""
        try:
            if command == 'help':
                help_text = """
Available Commands:
- help: Show this help message
- clear: Clear terminal
- ls, dir: List directory
- pwd: Show current directory
- System commands will be integrated soon
"""
                self.write_output(help_text)
            
            elif command == 'clear':
                self.output_area.config(state='normal')
                self.output_area.delete('1.0', 'end')
                self.output_area.config(state='disabled')
            
            elif command in ['ls', 'dir']:
                # Simple directory listing
                files = os.listdir('.')
                for file in files:
                    self.write_output(f"{file}\n")
            
            elif command == 'pwd':
                self.write_output(f"{os.getcwd()}\n")
            
            else:
                self.write_output(f"Command not found: {command}\n")
                
        except Exception as e:
            self.write_output(f"Error: {str(e)}\n")
    
    def previous_command(self, event):
        """Navigate to previous command in history"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.command_entry.delete(0, 'end')
            self.command_entry.insert(0, self.command_history[self.history_index])
    
    def next_command(self, event):
        """Navigate to next command in history"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_entry.delete(0, 'end')
            self.command_entry.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
            self.command_entry.delete(0, 'end')