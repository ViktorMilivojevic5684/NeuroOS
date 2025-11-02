# core/file_manager.py
import os
import shutil
import time
from pathlib import Path
from typing import Dict, List

class FileManager:
    def __init__(self):
        self.current_path = os.getcwd()
        self.history = []
        self.bookmarks = []
    
    def list_directory(self, path: str = None) -> Dict:
        """List directory contents with detailed information"""
        try:
            target_path = path if path else self.current_path
            
            if not os.path.exists(target_path):
                return {'success': False, 'error': 'Path does not exist'}
            
            items = []
            total_size = 0
            file_count = 0
            dir_count = 0
            
            for item_name in os.listdir(target_path):
                item_path = os.path.join(target_path, item_name)
                
                try:
                    stat = os.stat(item_path)
                    is_dir = os.path.isdir(item_path)
                    size = stat.st_size if not is_dir else 0
                    
                    item_info = {
                        'name': item_name,
                        'path': item_path,
                        'is_directory': is_dir,
                        'is_file': not is_dir,
                        'size_bytes': size,
                        'size_human': self._bytes_to_human(size),
                        'modified': time.ctime(stat.st_mtime),
                        'permissions': oct(stat.st_mode)[-3:],
                        'owner': stat.st_uid
                    }
                    
                    items.append(item_info)
                    total_size += size
                    
                    if is_dir:
                        dir_count += 1
                    else:
                        file_count += 1
                        
                except OSError:
                    continue
            
            # Sort: directories first, then files
            items.sort(key=lambda x: (not x['is_directory'], x['name'].lower()))
            
            return {
                'success': True,
                'path': target_path,
                'items': items,
                'summary': {
                    'total_items': len(items),
                    'file_count': file_count,
                    'directory_count': dir_count,
                    'total_size_bytes': total_size,
                    'total_size_human': self._bytes_to_human(total_size)
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def read_file(self, file_path: str) -> Dict:
        """Read file content safely"""
        try:
            if not os.path.exists(file_path):
                return {'success': False, 'error': 'File does not exist'}
            
            if os.path.isdir(file_path):
                return {'success': False, 'error': 'Path is a directory'}
            
            # Check file size (limit to 1MB for safety)
            file_size = os.path.getsize(file_path)
            if file_size > 1024 * 1024:  # 1MB
                return {'success': False, 'error': 'File too large to read'}
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            
            return {
                'success': True,
                'content': content,
                'size': file_size,
                'encoding': 'utf-8'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_file(self, file_path: str, content: str = "") -> Dict:
        """Create a new file"""
        try:
            if os.path.exists(file_path):
                return {'success': False, 'error': 'File already exists'}
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return {'success': True, 'message': f'File created: {file_path}'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_path(self, path: str) -> Dict:
        """Delete file or directory"""
        try:
            if not os.path.exists(path):
                return {'success': False, 'error': 'Path does not exist'}
            
            if os.path.isdir(path):
                shutil.rmtree(path)
                message = f'Directory deleted: {path}'
            else:
                os.remove(path)
                message = f'File deleted: {path}'
            
            return {'success': True, 'message': message}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_disk_usage(self) -> Dict:
        """Get disk usage information"""
        try:
            usage = shutil.disk_usage(self.current_path)
            
            return {
                'success': True,
                'total_gb': round(usage.total / (1024**3), 2),
                'used_gb': round(usage.used / (1024**3), 2),
                'free_gb': round(usage.free / (1024**3), 2),
                'used_percent': round((usage.used / usage.total) * 100, 2)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _bytes_to_human(self, size_bytes: int) -> str:
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"
    
    def change_directory(self, new_path: str) -> Dict:
        """Change current directory"""
        try:
            if not os.path.exists(new_path):
                return {'success': False, 'error': 'Path does not exist'}
            
            if not os.path.isdir(new_path):
                return {'success': False, 'error': 'Path is not a directory'}
            
            self.history.append(self.current_path)
            self.current_path = new_path
            
            return {'success': True, 'message': f'Changed to: {new_path}'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

