# main.py
import os
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import time

def setup_environment():
    """Set up Python environment and paths"""
    try:
        # Get the project root directory
        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        
        # Add all module directories to Python path
        module_paths = [
            PROJECT_ROOT,
            os.path.join(PROJECT_ROOT, "core"),
            os.path.join(PROJECT_ROOT, "ai"), 
            os.path.join(PROJECT_ROOT, "ui"),
            os.path.join(PROJECT_ROOT, "apps")
        ]
        
        for path in module_paths:
            if path not in sys.path:
                sys.path.insert(0, path)
        
        # Set working directory to project root
        os.chdir(PROJECT_ROOT)
        
        print(f"NeuroOS Environment Setup Complete")
        print(f"Project Root: {PROJECT_ROOT}")
        print(f"Python Path: {sys.path}")
        
        return True
        
    except Exception as e:
        print(f"Environment setup failed: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    required_modules = [
        'psutil',      # System monitoring
        'PIL',         # Image processing (Pillow)
        'requests',    # HTTP requests
    ]
    
    for module in required_modules:
        try:
            if module == 'PIL':
                __import__('PIL.Image')
            else:
                __import__(module)
        except ImportError:
            missing_deps.append(module)
    
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        
        # Auto-install missing dependencies
        try:
            import subprocess
            import sys
            
            for dep in missing_deps:
                package_name = 'Pillow' if dep == 'PIL' else dep
                print(f"Installing {package_name}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            
            print("All dependencies installed successfully")
            return True
            
        except Exception as e:
            print(f"Failed to auto-install dependencies: {e}")
            return False
    
    print("All dependencies available")
    return True

def show_splash_screen():
    """Show a simple splash screen during startup"""
    splash = tk.Tk()
    splash.title("NeuroOS")
    splash.geometry("400x200")
    splash.configure(bg='#1e1e1e')
    
    # Center the splash screen
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (400 // 2)
    y = (splash.winfo_screenheight() // 2) - (200 // 2)
    splash.geometry(f"400x200+{x}+{y}")
    
    # Splash content
    title_label = tk.Label(splash, text="NeuroOS", font=("Arial", 24, "bold"), 
                          bg='#1e1e1e', fg='#0078d7')
    title_label.pack(pady=20)
    
    subtitle_label = tk.Label(splash, text="AI Operating System", 
                             font=("Arial", 12), bg='#1e1e1e', fg='#cccccc')
    subtitle_label.pack(pady=5)
    
    progress_label = tk.Label(splash, text="Initializing...", 
                             font=("Arial", 10), bg='#1e1e1e', fg='#888888')
    progress_label.pack(pady=20)
    
    # Progress bar
    progress_frame = tk.Frame(splash, bg='#1e1e1e')
    progress_frame.pack(pady=10)
    
    progress_bar = tk.Frame(progress_frame, bg='#0078d7', height=4, width=0)
    progress_bar.pack(fill='x')
    
    splash.update()
    return splash, progress_bar, progress_label

def initialize_system(splash, progress_bar, progress_label):
    """Initialize system components with progress updates"""
    stages = [
        ("Setting up environment...", 20),
        ("Checking dependencies...", 40),
        ("Loading core modules...", 60),
        ("Initializing AI system...", 80),
        ("Starting user interface...", 100)
    ]
    
    for stage_text, progress in stages:
        progress_label.config(text=stage_text)
        progress_bar.config(width=progress * 3)  # Scale to 300px
        splash.update()
        time.sleep(0.5)  # Simulate loading time
    
    time.sleep(0.5)
    splash.destroy()

def main():
    """Main application entry point"""
    print("=" * 50)
    print("Starting NeuroOS AI Operating System")
    print("=" * 50)
    
    # Show splash screen
    splash, progress_bar, progress_label = show_splash_screen()
    
    try:
        # Initialize system with progress
        initialize_system(splash, progress_bar, progress_label)
        
        # Final environment setup
        if not setup_environment():
            messagebox.showerror("Startup Error", "Failed to set up environment")
            return
        
        if not check_dependencies():
            messagebox.showerror("Dependency Error", 
                               "Some required packages are missing.\n\n"
                               "Please install: psutil, Pillow, requests")
            return
        
        # Import and start the main application
        from ui.desktop import NeuroOSDesktop
        
        print("Launching NeuroOS Desktop...")
        app = NeuroOSDesktop()
        
        print("NeuroOS is now running")
        print("=" * 50)
        
        # Start the application
        app.run()
        
    except ImportError as e:
        error_msg = f"Failed to import required module: {e}"
        print(error_msg)
        messagebox.showerror("Import Error", error_msg)
        
    except Exception as e:
        error_msg = f"Failed to start NeuroOS: {e}"
        print(error_msg)
        messagebox.showerror("Startup Error", error_msg)
        
    finally:
        print("NeuroOS shutdown complete")
        print("=" * 50)

if __name__ == "__main__":
    main()