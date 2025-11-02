# core/system_manager.py
import psutil
import time
import threading
from typing import Dict, List

class SystemManager:
    def __init__(self):
        self.system_info = {}
        self.processes = []
        self.monitoring = False
        self.update_interval = 2
        
    def get_system_info(self) -> Dict:
        """Get comprehensive system information"""
        try:
            # CPU Information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory Information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk Information
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network Information
            net_io = psutil.net_io_counters()
            net_connections = len(psutil.net_connections())
            
            # System Information
            boot_time = psutil.boot_time()
            users = len(psutil.users())
            
            self.system_info = {
                'cpu': {
                    'usage_percent': cpu_percent,
                    'core_count': cpu_count,
                    'frequency_mhz': cpu_freq.current if cpu_freq else 0,
                    'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)
                },
                'memory': {
                    'total_gb': round(memory.total / (1024**3), 2),
                    'available_gb': round(memory.available / (1024**3), 2),
                    'used_percent': memory.percent,
                    'used_gb': round(memory.used / (1024**3), 2)
                },
                'disk': {
                    'total_gb': round(disk.total / (1024**3), 2),
                    'used_gb': round(disk.used / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2),
                    'used_percent': disk.percent
                },
                'network': {
                    'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2) if net_io else 0,
                    'bytes_recv_mb': round(net_io.bytes_recv / (1024**2), 2) if net_io else 0,
                    'active_connections': net_connections
                },
                'system': {
                    'boot_time': time.ctime(boot_time),
                    'users_count': users,
                    'timestamp': time.time()
                }
            }
            
            return self.system_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_running_processes(self, limit: int = 20) -> List[Dict]:
        """Get list of running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    process_info = proc.info
                    processes.append(process_info)
                    if len(processes) >= limit:
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            self.processes = processes
            return processes
            
        except Exception as e:
            return [{'error': str(e)}]
    
    def start_real_time_monitoring(self, callback=None):
        """Start real-time system monitoring"""
        self.monitoring = True
        
        def monitor_loop():
            while self.monitoring:
                try:
                    system_info = self.get_system_info()
                    processes = self.get_running_processes()
                    
                    if callback:
                        callback({
                            'system': system_info,
                            'processes': processes,
                            'timestamp': time.time()
                        })
                    
                    time.sleep(self.update_interval)
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(self.update_interval)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring = False
    
    def get_system_health(self) -> Dict:
        """Get system health status"""
        info = self.get_system_info()
        
        health_status = "HEALTHY"
        warnings = []
        
        # Check CPU
        if info.get('cpu', {}).get('usage_percent', 0) > 90:
            health_status = "WARNING"
            warnings.append("High CPU usage")
        
        # Check Memory
        if info.get('memory', {}).get('used_percent', 0) > 90:
            health_status = "CRITICAL"
            warnings.append("High memory usage")
        
        # Check Disk
        if info.get('disk', {}).get('used_percent', 0) > 90:
            health_status = "WARNING"
            warnings.append("Low disk space")
        
        return {
            'status': health_status,
            'warnings': warnings,
            'timestamp': time.time()
        }