import requests

class BackendClient:
    def __init__(self, base_url="http://192.168.100.88:8000/api/ingest/json/Client_84"):
        self.base_url = base_url

    def send_log(self, event_dict: dict):
        """Blind-fires the raw log dictionary to the server"""
        try:
            response = requests.post(self.base_url, json=event_dict, timeout=3)
            print(f"[+] Log sent! Server replied: {response.status_code}")
        except Exception as e:
            print(f"[-] Failed to route to backend: {e}")
