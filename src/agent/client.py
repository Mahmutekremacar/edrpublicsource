import requests
import time
import socket
from eventscanner import EventCollector
from logger import LocalLogger

def run_agent():
    collector = EventCollector()
    local_logger = LocalLogger()
    client_id = "client_01"
    hostname = socket.gethostname()
    backend_url = f"http://127.0.0.1:8000/api/ingest/json/{client_id}?hostname={hostname}"
    print(f"EDR Agent initialized. Sending data to: {backend_url}")

    while True:

        events = collector.get_recent_events(max_events=500)

        
        if events:
            for event in events:
                local_logger.log(event)
            
            payload = {"source": "windows-sysmon", "messages": events}
            
            try:
                response = requests.post(backend_url, json=payload, timeout=5)
                if response.status_code == 200:
                    print(f"Success: Transmitted batch of {len(events)} events. Newest RecordID: {events[-1]['record_id']}")
                else:
                    print(f"Server Warning: Received status code {response.status_code}")
            except Exception as e:
                print(f"Transmission Error: Unable to reach backend. {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    run_agent()