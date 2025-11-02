# ai/voice_interface.py
from typing import Dict

class VoiceInterface:
    def __init__(self):
        self.command_history = []
        self.context = []
    
    def process_command(self, text: str) -> Dict:
        """Process natural language command"""
        text_lower = text.lower()
        
        # Determine intent
        intent = self._classify_intent(text_lower)
        
        # Create execution plan
        execution_plan = self._create_execution_plan(intent)
        
        # Store in history
        self.command_history.append({
            'text': text,
            'intent': intent,
            'timestamp': time.time()
        })
        
        return {
            'original_text': text,
            'detected_intent': intent,
            'execution_plan': execution_plan,
            'confidence': 0.85
        }
    
    def _classify_intent(self, text: str) -> str:
        """Classify command intent"""
        # File operations
        file_keywords = ['file', 'folder', 'directory', 'list', 'ls', 'read', 'create', 'delete']
        if any(keyword in text for keyword in file_keywords):
            return 'file_operation'
        
        # Network operations
        network_keywords = ['search', 'find', 'weather', 'internet', 'connectivity', 'network']
        if any(keyword in text for keyword in network_keywords):
            return 'network_operation'
        
        # System operations
        system_keywords = ['system', 'status', 'process', 'cpu', 'memory', 'health']
        if any(keyword in text for keyword in system_keywords):
            return 'system_operation'
        
        return 'general'
    
    def _create_execution_plan(self, intent: str) -> str:
        """Create execution plan based on intent"""
        plans = {
            'file_operation': "1. Analyze file operation request\n2. Check permissions\n3. Execute file operation\n4. Return results",
            'network_operation': "1. Analyze network request\n2. Check connectivity\n3. Execute network operation\n4. Process response",
            'system_operation': "1. Analyze system request\n2. Gather system data\n3. Generate report\n4. Display information",
            'general': "1. Process general command\n2. Execute appropriate action\n3. Return response"
        }
        
        return plans.get(intent, "Standard execution plan")
    
    def get_command_history(self, limit: int = 10) -> list:
        """Get command history"""
        return self.command_history[-limit:]

# Import time
import time