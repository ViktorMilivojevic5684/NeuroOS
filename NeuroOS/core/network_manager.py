# core/network_manager.py
import requests
import socket
import time
from typing import Dict, List

class NetworkManager:
    def __init__(self):
        self.session = requests.Session()
        self.request_history = []
        
        # Configure session
        self.session.headers.update({
            'User-Agent': 'NeuroOS/1.0',
            'Accept': '*/*'
        })
    
    def check_connectivity(self) -> Dict:
        """Check internet connectivity with multiple tests"""
        try:
            test_urls = [
                "https://www.google.com",
                "https://www.cloudflare.com",
                "https://www.github.com"
            ]
            
            results = []
            for url in test_urls:
                start_time = time.time()
                try:
                    response = self.session.get(url, timeout=5)
                    response_time = round((time.time() - start_time) * 1000, 2)
                    
                    results.append({
                        'url': url,
                        'status': 'SUCCESS',
                        'response_time_ms': response_time,
                        'status_code': response.status_code
                    })
                except Exception as e:
                    results.append({
                        'url': url,
                        'status': 'FAILED',
                        'error': str(e)
                    })
            
            success_count = len([r for r in results if r['status'] == 'SUCCESS'])
            
            return {
                'success': True,
                'connected': success_count > 0,
                'success_rate': f"{success_count}/{len(test_urls)}",
                'tests': results,
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_system_network_info(self) -> Dict:
        """Get system network information"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Get network interfaces (simplified)
            interfaces = []
            try:
                import netifaces
                for interface in netifaces.interfaces():
                    addrs = netifaces.ifaddresses(interface)
                    if netifaces.AF_INET in addrs:
                        for link in addrs[netifaces.AF_INET]:
                            interfaces.append({
                                'interface': interface,
                                'ip_address': link.get('addr', 'Unknown'),
                                'netmask': link.get('netmask', 'Unknown')
                            })
            except ImportError:
                interfaces.append({
                    'interface': 'eth0',
                    'ip_address': local_ip,
                    'netmask': '255.255.255.0'
                })
            
            return {
                'success': True,
                'hostname': hostname,
                'local_ip': local_ip,
                'interfaces': interfaces,
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def web_search(self, query: str, max_results: int = 5) -> Dict:
        """Perform web search using DuckDuckGo API"""
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            
            # Extract information from API response
            if data.get('AbstractText'):
                results.append({
                    'title': data.get('Heading', 'Information'),
                    'url': data.get('AbstractURL', ''),
                    'snippet': data.get('AbstractText', ''),
                    'type': 'abstract'
                })
            
            # Add related topics
            for topic in data.get('RelatedTopics', [])[:max_results]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' ').title(),
                        'url': topic.get('FirstURL', ''),
                        'snippet': topic.get('Text', ''),
                        'type': 'related'
                    })
            
            self.request_history.append({
                'type': 'search',
                'query': query,
                'result_count': len(results),
                'timestamp': time.time()
            })
            
            return {
                'success': True,
                'query': query,
                'results': results[:max_results],
                'total_results': len(results),
                'source': 'DuckDuckGo'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_weather(self, location: str = "London") -> Dict:
        """Get weather information (simulated for now)"""
        try:
            # Simulated weather data - in real implementation, use weather API
            weather_data = {
                'location': location.title(),
                'temperature': 22.5,
                'conditions': 'Partly Cloudy',
                'humidity': 65,
                'wind_speed': 15.2,
                'pressure': 1013,
                'timestamp': time.time()
            }
            
            return {
                'success': True,
                'weather': weather_data,
                'source': 'simulated'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}