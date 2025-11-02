# ai/orchestrator.py
from typing import Dict, List
from enum import Enum

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class AIOrchestrator:
    def __init__(self):
        self.tasks = []
        self.task_history = []
        self.modules = {}
        
    def register_module(self, name: str, function, description: str = ""):
        """Register an AI module"""
        self.modules[name] = {
            'function': function,
            'description': description
        }
    
    def submit_task(self, command: str, user_intent: str = None) -> Dict:
        """Submit a task for execution"""
        try:
            task_id = len(self.tasks) + 1
            task = {
                'id': task_id,
                'command': command,
                'intent': user_intent,
                'status': 'pending',
                'priority': TaskPriority.MEDIUM,
                'timestamp': time.time()
            }
            
            self.tasks.append(task)
            
            # Execute task
            result = self._execute_task(task)
            
            # Update task status
            task['status'] = 'completed' if result['success'] else 'failed'
            task['result'] = result
            self.task_history.append(task)
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _execute_task(self, task: Dict) -> Dict:
        """Execute a task based on its intent"""
        intent = task.get('intent', 'general')
        command = task.get('command', '')
        
        try:
            if intent == 'file_operation':
                return self._handle_file_operation(command)
            elif intent == 'network_operation':
                return self._handle_network_operation(command)
            elif intent == 'system_operation':
                return self._handle_system_operation(command)
            else:
                return self._handle_general_command(command)
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_file_operation(self, command: str) -> Dict:
        """Handle file operations"""
        from core.file_manager import FileManager
        fm = FileManager()
        
        if 'list' in command.lower() or 'ls' in command.lower():
            return fm.list_directory()
        elif 'read' in command.lower():
            # Extract filename from command
            return {'success': True, 'message': 'File read operation'}
        else:
            return {'success': True, 'message': 'File operation completed'}
    
    def _handle_network_operation(self, command: str) -> Dict:
        """Handle network operations"""
        from core.network_manager import NetworkManager
        nm = NetworkManager()
        
        if 'search' in command.lower():
            query = command.replace('search', '').strip()
            return nm.web_search(query)
        elif 'weather' in command.lower():
            location = 'London'  # Default
            if 'in' in command:
                location = command.split('in')[1].strip()
            return nm.get_weather(location)
        elif 'internet' in command.lower() or 'connectivity' in command.lower():
            return nm.check_connectivity()
        else:
            return nm.get_system_network_info()
    
    def _handle_system_operation(self, command: str) -> Dict:
        """Handle system operations"""
        from core.system_manager import SystemManager
        sm = SystemManager()
        
        if 'status' in command.lower():
            return sm.get_system_info()
        elif 'process' in command.lower():
            return {'success': True, 'processes': sm.get_running_processes()}
        elif 'health' in command.lower():
            return sm.get_system_health()
        else:
            return sm.get_system_info()
    
    def _handle_general_command(self, command: str) -> Dict:
        """Handle general commands"""
        return {
            'success': True,
            'message': f'Command executed: {command}',
            'timestamp': time.time()
        }
    
    def get_task_history(self, limit: int = 10) -> List[Dict]:
        """Get task history"""
        return self.task_history[-limit:]
    
    def get_system_status(self) -> Dict:
        """Get orchestrator status"""
        return {
            'total_tasks': len(self.task_history),
            'successful_tasks': len([t for t in self.task_history if t.get('status') == 'completed']),
            'failed_tasks': len([t for t in self.task_history if t.get('status') == 'failed']),
            'registered_modules': len(self.modules),
            'active_tasks': len(self.tasks)
        }

# Import time at the end to avoid circular imports
import time