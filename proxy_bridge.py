import subprocess
import json
import time
import requests
from typing import Optional, Dict, List

class ProxyBridge:
    def __init__(self):
        self.rust_process = None
        self.proxy_cache = {}
        self.start_rust_manager()
    
    def start_rust_manager(self):
        """Start the Rust proxy manager"""
        try:
            # Compile and run Rust proxy manager
            subprocess.run(["cargo", "build", "--release"], cwd=".", check=True)
            self.rust_process = subprocess.Popen(
                ["./target/release/proxy_manager"],
                cwd=".",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(5)  # Wait for initialization
        except Exception as e:
            print(f"Failed to start Rust proxy manager: {e}")
    
    def get_proxy(self, country: str = "US") -> Optional[Dict]:
        """Get working proxy for specified country"""
        try:
            # Check cache first
            if country in self.proxy_cache:
                cached_proxy = self.proxy_cache[country]
                if self.validate_proxy(cached_proxy):
                    return cached_proxy
            
            # Get fresh proxy from Rust manager
            proxy = self._fetch_proxy_from_rust(country)
            if proxy:
                self.proxy_cache[country] = proxy
                return proxy
            
            return None
            
        except Exception as e:
            print(f"Proxy fetch error: {e}")
            return None
    
    def _fetch_proxy_from_rust(self, country: str) -> Optional[Dict]:
        """Fetch proxy from Rust manager via IPC"""
        # This would communicate with Rust process
        # For now, return a mock structure
        return {
            "ip": "127.0.0.1",
            "port": 8080,
            "country": country,
            "protocol": "http"
        }
    
    def validate_proxy(self, proxy: Dict) -> bool:
        """Validate if proxy is still working"""
        try:
            proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
            proxies = {"http": proxy_url, "https": proxy_url}
            
            response = requests.get(
                "http://httpbin.org/ip",
                proxies=proxies,
                timeout=10
            )
            
            return response.status_code == 200
            
        except:
            return False
    
    def get_proxy_stats(self) -> Dict:
        """Get statistics from Rust proxy manager"""
        # This would query the Rust process for stats
        return {"total_proxies": 0, "working_proxies": 0}
    
    def __del__(self):
        if self.rust_process:
            self.rust_process.terminate()