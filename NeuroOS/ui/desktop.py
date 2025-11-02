# ui/desktop.py
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, messagebox
import threading
import time
import os
import sys

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.system_manager import SystemManager
from core.file_manager import FileManager
from core.network_manager import NetworkManager
from ai.orchestrator import AIOrchestrator
from ai.voice_interface import VoiceInterface

class NeuroOSDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_core_systems()
        self.setup_window()
        self.setup_variables()
        self.setup_gui()
        self.start_system_services()
        
    def setup_core_systems(self):
        """Initialize all core systems"""
        try:
            self.system_manager = SystemManager()
            self.file_manager = FileManager()
            self.network_manager = NetworkManager()
            self.ai_orchestrator = AIOrchestrator()
            self.voice_interface = VoiceInterface()
            
            print("Core systems initialized successfully")
        except Exception as e:
            print(f"System initialization error: {e}")
    
    def setup_window(self):
        """Configure main window"""
        self.root.title("NeuroOS - AI Operating System")
        self.root.geometry("1300x850")
        self.root.configure(bg='#1e1e1e')
        self.root.minsize(1100, 700)
        
        # Center window on screen
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1300) // 2
        y = (screen_height - 850) // 2
        self.root.geometry(f"1300x850+{x}+{y}")
        
        # Set window icon (placeholder)
        try:
            self.root.iconbitmap(default='')
        except:
            pass
    
    def setup_variables(self):
        """Initialize application variables"""
        self.dark_mode = True
        self.current_view = "dashboard"
        self.system_data = {}
        self.monitoring_active = True
        
    def setup_gui(self):
        """Setup complete GUI"""
        self.create_menu_bar()
        self.create_header()
        self.create_main_area()
        self.create_status_bar()
        self.apply_dark_theme()
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = Menu(self.root, bg='#2d2d30', fg='#cccccc', 
                      activebackground='#3e3e42', activeforeground='#ffffff')
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = Menu(menubar, tearoff=0, bg='#2d2d30', fg='#cccccc')
        menubar.add_cascade(label="System", menu=file_menu)
        file_menu.add_command(label="System Info", command=self.show_system_info)
        file_menu.add_command(label="Process Manager", command=self.show_process_manager)
        file_menu.add_separator()
        file_menu.add_command(label="Exit NeuroOS", command=self.safe_shutdown)
        
        # View Menu
        view_menu = Menu(menubar, tearoff=0, bg='#2d2d30', fg='#cccccc')
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Dashboard", command=self.show_dashboard)
        view_menu.add_command(label="AI Control", command=self.show_ai_control)
        view_menu.add_command(label="File Explorer", command=self.show_file_explorer)
        view_menu.add_command(label="Network Tools", command=self.show_network_tools)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        
        # Tools Menu
        tools_menu = Menu(menubar, tearoff=0, bg='#2d2d30', fg='#cccccc')
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="System Monitor", command=self.show_system_monitor)
        tools_menu.add_command(label="Network Diagnostics", command=self.show_network_diagnostics)
        tools_menu.add_command(label="AI Command Console", command=self.show_ai_console)
        
        # Help Menu
        help_menu = Menu(menubar, tearoff=0, bg='#2d2d30', fg='#cccccc')
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About NeuroOS", command=self.show_about)
        help_menu.add_command(label="System Documentation", command=self.show_documentation)
    
    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg='#0078d7', height=70)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Logo and Title Area
        title_frame = tk.Frame(header_frame, bg='#0078d7')
        title_frame.pack(side='left', padx=20, pady=15)
        
        # NeuroOS Logo (Text-based)
        logo_label = tk.Label(title_frame, text="N", font=("Arial", 24, "bold"), 
                             bg='#0078d7', fg='white')
        logo_label.pack(side='left')
        
        title_label = tk.Label(title_frame, text="NeuroOS", font=("Arial", 20, "bold"), 
                              bg='#0078d7', fg='white')
        title_label.pack(side='left', padx=(12, 0))
        
        subtitle_label = tk.Label(title_frame, text="AI Operating System", 
                                 font=("Arial", 11), bg='#0078d7', fg='#e1f5fe')
        subtitle_label.pack(side='left', padx=(15, 0))
        
        # System Status Area
        status_frame = tk.Frame(header_frame, bg='#0078d7')
        status_frame.pack(side='right', padx=20, pady=15)
        
        self.status_indicator = tk.Label(status_frame, text="O", font=("Arial", 16), 
                                        bg='#0078d7', fg='#4caf50')
        self.status_indicator.pack(side='right', padx=(10, 0))
        
        self.status_text = tk.Label(status_frame, text="SYSTEM: OPERATIONAL", 
                                   font=("Arial", 10, "bold"), bg='#0078d7', fg='white')
        self.status_text.pack(side='right')
    
    def create_main_area(self):
        """Create main content area with tabs"""
        main_container = tk.Frame(self.root, bg='#1e1e1e')
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Configure ttk style for modern look
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook style (Tabs)
        style.configure('TNotebook', background='#1e1e1e', borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#2d2d30', 
                       foreground='#cccccc',
                       padding=[20, 8],
                       font=('Arial', 10))
        style.map('TNotebook.Tab', 
                 background=[('selected', '#0078d7')],
                 foreground=[('selected', 'white')])
        
        # Create notebook (tab container)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.setup_dashboard_tab()
        self.setup_ai_control_tab()
        self.setup_file_explorer_tab()
        self.setup_system_monitor_tab()
        self.setup_network_tools_tab()
        
        # Set default tab
        self.notebook.select(0)
    
    def setup_dashboard_tab(self):
        """Setup main dashboard tab"""
        self.dashboard_tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.dashboard_tab, text="   Dashboard   ")
        
        # Main content frame
        content_frame = tk.Frame(self.dashboard_tab, bg='#1e1e1e')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left sidebar - Quick Actions
        sidebar_frame = tk.Frame(content_frame, bg='#252526', width=280)
        sidebar_frame.pack(side='left', fill='y', padx=(0, 15))
        sidebar_frame.pack_propagate(False)
        
        # Quick Actions Title
        actions_title = tk.Label(sidebar_frame, text="QUICK ACTIONS", 
                                font=("Arial", 12, "bold"), bg='#252526', fg='#0078d7',
                                anchor='w')
        actions_title.pack(fill='x', padx=20, pady=(20, 10))
        
        # Quick Action Buttons
        actions = [
            ("System Information", self.quick_system_info),
            ("File Explorer", self.quick_file_explorer),
            ("Network Check", self.quick_network_check),
            ("AI Command", self.quick_ai_command),
            ("Process Monitor", self.quick_process_monitor),
            ("Security Scan", self.quick_security_scan)
        ]
        
        for text, command in actions:
            btn = tk.Button(sidebar_frame, text=text, font=("Arial", 10), 
                          bg='#2d2d30', fg='#cccccc', 
                          activebackground='#3e3e42', activeforeground='white',
                          relief='flat', height=2, width=20,
                          command=command, anchor='w', padx=15)
            btn.pack(fill='x', padx=10, pady=5)
        
        # Right content area
        right_frame = tk.Frame(content_frame, bg='#1e1e1e')
        right_frame.pack(side='left', fill='both', expand=True)
        
        # Welcome Section
        welcome_frame = tk.Frame(right_frame, bg='#252526', relief='flat', bd=1)
        welcome_frame.pack(fill='x', pady=(0, 15))
        
        welcome_label = tk.Label(welcome_frame, text="Welcome to NeuroOS", 
                               font=("Arial", 16, "bold"), bg='#252526', fg='#0078d7')
        welcome_label.pack(anchor='w', padx=20, pady=15)
        
        welcome_text = tk.Label(welcome_frame, 
                              text="Advanced AI-powered operating system with real-time monitoring, intelligent automation, and comprehensive system management capabilities.",
                              font=("Arial", 10), bg='#252526', fg='#cccccc', 
                              justify='left', wraplength=800)
        welcome_text.pack(anchor='w', padx=20, pady=(0, 15))
        
        # System Status Cards
        cards_frame = tk.Frame(right_frame, bg='#1e1e1e')
        cards_frame.pack(fill='x', pady=10)
        
        # System metrics cards
        self.system_cards = {}
        card_configs = [
            ("CPU Usage", "cpu", "#ff5252"),
            ("Memory", "memory", "#4caf50"),
            ("Disk Space", "disk", "#2196f3"),
            ("Network", "network", "#ff9800")
        ]
        
        for i, (title, key, color) in enumerate(card_configs):
            card = tk.Frame(cards_frame, bg='#252526', relief='flat', bd=1, 
                           width=180, height=100)
            card.grid(row=0, column=i, padx=8, sticky='nsew')
            card.grid_propagate(False)
            
            # Card title
            title_label = tk.Label(card, text=title, font=("Arial", 10, "bold"), 
                                 bg='#252526', fg='#888888')
            title_label.pack(anchor='w', padx=15, pady=(15, 5))
            
            # Card value
            value_label = tk.Label(card, text="Loading...", font=("Arial", 18, "bold"), 
                                 bg='#252526', fg=color)
            value_label.pack(expand=True)
            
            self.system_cards[key] = value_label
            
            cards_frame.columnconfigure(i, weight=1)
        
        # Recent Activity Section
        activity_frame = tk.Frame(right_frame, bg='#252526', relief='flat', bd=1)
        activity_frame.pack(fill='both', expand=True, pady=(15, 0))
        
        activity_title = tk.Label(activity_frame, text="RECENT SYSTEM ACTIVITY", 
                                font=("Arial", 12, "bold"), bg='#252526', fg='#0078d7')
        activity_title.pack(anchor='w', padx=20, pady=15)
        
        self.activity_log = scrolledtext.ScrolledText(activity_frame, 
                                                     bg='#1e1e1e', fg='#cccccc',
                                                     insertbackground='white',
                                                     font=("Consolas", 9),
                                                     wrap=tk.WORD)
        self.activity_log.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        self.activity_log.config(state='disabled')
        
        # Add initial activity messages
        self.log_activity("System initialized successfully")
        self.log_activity("Core services started")
        self.log_activity("AI modules loaded and ready")
        self.log_activity("Network services active")
    
    def setup_ai_control_tab(self):
        """Setup AI control tab"""
        self.ai_tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.ai_tab, text="   AI Control   ")
        
        main_frame = tk.Frame(self.ai_tab, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Command Input Section
        input_frame = tk.Frame(main_frame, bg='#252526', relief='flat', bd=1)
        input_frame.pack(fill='x', pady=(0, 15))
        
        input_title = tk.Label(input_frame, text="AI COMMAND INTERFACE", 
                              font=("Arial", 12, "bold"), bg='#252526', fg='#0078d7')
        input_title.pack(anchor='w', padx=20, pady=15)
        
        # Command input area
        command_container = tk.Frame(input_frame, bg='#252526')
        command_container.pack(fill='x', padx=20, pady=(0, 20))
        
        # Command entry with label
        command_label = tk.Label(command_container, text="Enter Command:", 
                                font=("Arial", 10), bg='#252526', fg='#cccccc')
        command_label.pack(anchor='w', pady=(0, 8))
        
        self.command_entry = tk.Entry(command_container, font=("Arial", 12), 
                                    bg='#1e1e1e', fg='white', insertbackground='white',
                                    width=60, relief='sunken', bd=2)
        self.command_entry.pack(side='left', fill='x', expand=True, padx=(0, 15))
        self.command_entry.bind('<Return>', self.execute_ai_command)
        self.command_entry.focus()
        
        # Execute button
        execute_btn = tk.Button(command_container, text="Execute", 
                               font=("Arial", 10, "bold"),
                               bg='#0078d7', fg='white', 
                               activebackground='#005a9e', activeforeground='white',
                               command=self.execute_ai_command, relief='raised', bd=2,
                               padx=20)
        execute_btn.pack(side='right')
        
        # AI Response Area
        response_frame = tk.Frame(main_frame, bg='#252526', relief='flat', bd=1)
        response_frame.pack(fill='both', expand=True)
        
        response_title = tk.Label(response_frame, text="AI RESPONSE & OUTPUT", 
                                font=("Arial", 12, "bold"), bg='#252526', fg='#0078d7')
        response_title.pack(anchor='w', padx=20, pady=15)
        
        self.ai_response = scrolledtext.ScrolledText(response_frame, 
                                                   bg='#1e1e1e', fg='#cccccc',
                                                   insertbackground='white',
                                                   font=("Consolas", 10),
                                                   wrap=tk.WORD)
        self.ai_response.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Add welcome message
        welcome_msg = """NeuroOS AI System Ready

Available Commands:
- System: 'system status', 'show processes', 'system health'
- Files: 'list files', 'show disk usage'
- Network: 'check internet', 'search python', 'weather london'
- General: Any natural language command

Enter a command above to begin."""
        
        self.ai_response.insert('1.0', welcome_msg)
        self.ai_response.config(state='disabled')
    
    def setup_file_explorer_tab(self):
        """Setup file explorer tab"""
        self.file_tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.file_tab, text="   File Explorer   ")
        
        main_frame = tk.Frame(self.file_tab, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # File explorer content
        explorer_label = tk.Label(main_frame, text="File Explorer - Under Development", 
                                 font=("Arial", 16), bg='#1e1e1e', fg='#cccccc')
        explorer_label.pack(expand=True)
        
        info_text = tk.Label(main_frame, 
                           text="Full file explorer with directory navigation,\nfile operations, and search functionality\nwill be implemented in the next version.",
                           font=("Arial", 12), bg='#1e1e1e', fg='#888888')
        info_text.pack(pady=20)
    
    def setup_system_monitor_tab(self):
        """Setup system monitor tab"""
        self.monitor_tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.monitor_tab, text="   System Monitor   ")
        
        main_frame = tk.Frame(self.monitor_tab, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # System monitor content
        monitor_label = tk.Label(main_frame, text="System Monitor - Under Development", 
                                font=("Arial", 16), bg='#1e1e1e', fg='#cccccc')
        monitor_label.pack(expand=True)
        
        info_text = tk.Label(main_frame, 
                           text="Advanced system monitoring with real-time charts,\nprocess management, and performance analytics\nwill be implemented in the next version.",
                           font=("Arial", 12), bg='#1e1e1e', fg='#888888')
        info_text.pack(pady=20)
    
    def setup_network_tools_tab(self):
        """Setup network tools tab"""
        self.network_tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.network_tab, text="   Network Tools   ")
        
        main_frame = tk.Frame(self.network_tab, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Network tools content
        network_label = tk.Label(main_frame, text="Network Tools - Under Development", 
                                font=("Arial", 16), bg='#1e1e1e', fg='#cccccc')
        network_label.pack(expand=True)
        
        info_text = tk.Label(main_frame, 
                           text="Network diagnostics, speed tests, port scanning,\nand advanced networking tools will be implemented\nin the next version.",
                           font=("Arial", 12), bg='#1e1e1e', fg='#888888')
        info_text.pack(pady=20)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = tk.Frame(self.root, bg='#0078d7', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        # Left status items
        left_status = tk.Frame(status_frame, bg='#0078d7')
        left_status.pack(side='left', padx=15)
        
        self.cpu_status = tk.Label(left_status, text="CPU: --%", font=("Arial", 9), 
                                  bg='#0078d7', fg='white')
        self.cpu_status.pack(side='left', padx=(0, 20))
        
        self.memory_status = tk.Label(left_status, text="RAM: --%", font=("Arial", 9),
                                     bg='#0078d7', fg='white')
        self.memory_status.pack(side='left', padx=(0, 20))
        
        self.disk_status = tk.Label(left_status, text="Disk: --%", font=("Arial", 9),
                                   bg='#0078d7', fg='white')
        self.disk_status.pack(side='left')
        
        # Right status items
        right_status = tk.Frame(status_frame, bg='#0078d7')
        right_status.pack(side='right', padx=15)
        
        self.time_status = tk.Label(right_status, text="", font=("Arial", 9),
                                   bg='#0078d7', fg='white')
        self.time_status.pack(side='right')
    
    def apply_dark_theme(self):
        """Apply dark theme to all widgets"""
        # This method would configure all widget colors for dark theme
        pass
    
    def start_system_services(self):
        """Start background system services"""
        self.start_system_monitoring()
        self.start_time_updater()
        
    def start_system_monitoring(self):
        """Start real-time system monitoring"""
        def monitor_loop():
            while self.monitoring_active:
                try:
                    # Get system information
                    system_info = self.system_manager.get_system_info()
                    
                    # Update status bar
                    cpu_usage = system_info.get('cpu', {}).get('usage_percent', 0)
                    memory_usage = system_info.get('memory', {}).get('used_percent', 0)
                    disk_usage = system_info.get('disk', {}).get('used_percent', 0)
                    
                    self.cpu_status.config(text=f"CPU: {cpu_usage:.1f}%")
                    self.memory_status.config(text=f"RAM: {memory_usage:.1f}%")
                    self.disk_status.config(text=f"Disk: {disk_usage:.1f}%")
                    
                    # Update system cards on dashboard
                    if hasattr(self, 'system_cards'):
                        self.system_cards['cpu'].config(text=f"{cpu_usage:.1f}%")
                        self.system_cards['memory'].config(text=f"{memory_usage:.1f}%")
                        self.system_cards['disk'].config(text=f"{disk_usage:.1f}%")
                        self.system_cards['network'].config(text="Online")
                    
                    # Update system status
                    if cpu_usage > 90 or memory_usage > 90:
                        self.update_system_status("High Load", "red")
                    else:
                        self.update_system_status("Operational", "#4caf50")
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(5)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def start_time_updater(self):
        """Start time updater"""
        def update_time():
            while True:
                try:
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    self.time_status.config(text=current_time)
                    time.sleep(1)
                except:
                    time.sleep(5)
        
        time_thread = threading.Thread(target=update_time, daemon=True)
        time_thread.start()
    
    def update_system_status(self, status, color):
        """Update system status display"""
        self.status_text.config(text=f"SYSTEM: {status}")
        self.status_indicator.config(fg=color)
    
    def log_activity(self, message):
        """Log activity to dashboard"""
        timestamp = time.strftime("%H:%M:%S")
        self.activity_log.config(state='normal')
        self.activity_log.insert('end', f"[{timestamp}] {message}\n")
        self.activity_log.see('end')
        self.activity_log.config(state='disabled')
    
    def execute_ai_command(self, event=None):
        """Execute AI command"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        self.command_entry.delete(0, 'end')
        self.log_activity(f"AI Command: {command}")
        
        def run_command():
            try:
                # Process command through voice interface
                processed = self.voice_interface.process_command(command)
                
                # Update AI response area
                self.ai_response.config(state='normal')
                self.ai_response.delete('1.0', 'end')
                
                self.ai_response.insert('end', f"Command: {command}\n")
                self.ai_response.insert('end', f"Intent: {processed['detected_intent']}\n")
                self.ai_response.insert('end', f"Execution Plan:\n{processed['execution_plan']}\n")
                self.ai_response.insert('end', "\n" + "="*60 + "\n\n")
                
                # Execute command through orchestrator
                result = self.ai_orchestrator.submit_task(command, processed['detected_intent'])
                
                # Display results
                if result.get('success'):
                    self.ai_response.insert('end', "RESULT: SUCCESS\n\n")
                    
                    # Display specific result data
                    if 'message' in result:
                        self.ai_response.insert('end', f"{result['message']}\n")
                    
                    if 'results' in result:
                        for item in result['results']:
                            self.ai_response.insert('end', f"- {item.get('title', 'Item')}\n")
                            if 'snippet' in item:
                                self.ai_response.insert('end', f"  {item['snippet'][:100]}...\n")
                            self.ai_response.insert('end', "\n")
                    
                    if 'system' in result:
                        sys_info = result['system']
                        self.ai_response.insert('end', "System Information:\n")
                        for key, value in sys_info.items():
                            if isinstance(value, dict):
                                self.ai_response.insert('end', f"  {key}:\n")
                                for k, v in value.items():
                                    self.ai_response.insert('end', f"    {k}: {v}\n")
                            else:
                                self.ai_response.insert('end', f"  {key}: {value}\n")
                    
                    self.log_activity("AI command executed successfully")
                    
                else:
                    self.ai_response.insert('end', f"RESULT: FAILED\n")
                    self.ai_response.insert('end', f"Error: {result.get('error', 'Unknown error')}\n")
                    self.log_activity("AI command failed")
                
                self.ai_response.see('end')
                self.ai_response.config(state='disabled')
                
            except Exception as e:
                self.ai_response.config(state='normal')
                self.ai_response.insert('end', f"ERROR: {str(e)}\n")
                self.ai_response.config(state='disabled')
                self.log_activity(f"Command error: {e}")
        
        # Run command in separate thread to avoid GUI freezing
        command_thread = threading.Thread(target=run_command, daemon=True)
        command_thread.start()
    
    # Quick Action Methods
    def quick_system_info(self):
        self.notebook.select(0)
        self.log_activity("Quick action: System information")
    
    def quick_file_explorer(self):
        self.notebook.select(2)
        self.log_activity("Quick action: File explorer")
    
    def quick_network_check(self):
        self.command_entry.insert(0, "check internet connectivity")
        self.execute_ai_command()
        self.notebook.select(1)
    
    def quick_ai_command(self):
        self.notebook.select(1)
        self.command_entry.focus()
        self.log_activity("Quick action: AI command")
    
    def quick_process_monitor(self):
        self.notebook.select(3)
        self.log_activity("Quick action: Process monitor")
    
    def quick_security_scan(self):
        self.command_entry.insert(0, "system health check")
        self.execute_ai_command()
        self.notebook.select(1)
    
    # Menu Action Methods
    def show_system_info(self):
        self.notebook.select(0)
        self.log_activity("Menu: System information")
    
    def show_process_manager(self):
        self.notebook.select(3)
        self.log_activity("Menu: Process manager")
    
    def show_dashboard(self):
        self.notebook.select(0)
        self.log_activity("Menu: Dashboard")
    
    def show_ai_control(self):
        self.notebook.select(1)
        self.log_activity("Menu: AI control")
    
    def show_file_explorer(self):
        self.notebook.select(2)
        self.log_activity("Menu: File explorer")
    
    def show_network_tools(self):
        self.notebook.select(4)
        self.log_activity("Menu: Network tools")
    
    def show_system_monitor(self):
        self.notebook.select(3)
        self.log_activity("Menu: System monitor")
    
    def show_network_diagnostics(self):
        self.command_entry.insert(0, "network diagnostics")
        self.execute_ai_command()
        self.notebook.select(1)
    
    def show_ai_console(self):
        self.notebook.select(1)
        self.command_entry.focus()
        self.log_activity("Menu: AI console")
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        theme = "Dark" if self.dark_mode else "Light"
        self.log_activity(f"Theme toggled: {theme} mode")
    
    def show_about(self):
        about_text = """NeuroOS - AI Operating System
Version 1.0
Developed with Advanced AI Integration

Features:
- Real-time System Monitoring
- AI-Powered Command Interface
- File Management System
- Network Diagnostics
- Process Management
- Intelligent Automation

Copyright 2024 NeuroOS Project"""
        messagebox.showinfo("About NeuroOS", about_text)
        self.log_activity("Menu: About dialog")
    
    def show_documentation(self):
        self.log_activity("Menu: Documentation")
    
    def safe_shutdown(self):
        """Safely shutdown the application"""
        self.monitoring_active = False
        self.log_activity("System shutdown initiated")
        time.sleep(1)
        self.root.quit()
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {e}")
        finally:
            self.monitoring_active = False