import requests
import base64
import json
import subprocess
import time
from typing import Optional, Dict, Any

class CaptchaBridge:
    def __init__(self):
        self.go_server_url = "http://localhost:8080"
        self.go_process = None
        self.start_go_server()
    
    def start_go_server(self):
        """Start the Go captcha solver server"""
        try:
            self.go_process = subprocess.Popen(
                ["go", "run", "captcha_solver.go"],
                cwd=".",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(2)  # Wait for server to start
        except Exception as e:
            print(f"Failed to start Go server: {e}")
    
    def solve_captcha(self, image_data: bytes, captcha_type: str = "image") -> Optional[str]:
        """Solve captcha using Go backend"""
        try:
            # Convert image to base64
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            
            # Send to Go server
            response = requests.post(
                f"{self.go_server_url}/solve",
                json={
                    "image": image_b64,
                    "type": captcha_type
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result.get("text")
            
            return None
            
        except Exception as e:
            print(f"Captcha solving error: {e}")
            return None
    
    def __del__(self):
        if self.go_process:
            self.go_process.terminate()