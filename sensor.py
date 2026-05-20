import time
from client import BackendClient
from eventscanner import EventScanner

print("[*] Initializing EDR Sensor...")
client = BackendClient()
scanner = EventScanner()

# Start subscribing to the Windows Event Channels
scanner.scanner() 

print("[*] Starting REAL EDR sensor. Listening for events...")

# The infinite heartbeat loop
while True:
    try:
        # Check the scanner for any new logs it scooped up
        events = scanner.get_backlog()
        
        if events:
            print(f"[*] Found {len(events)} new logs! Firing them to the server...")
            for event in events:
                client.send_log(event)
        
        # Rest for 2 seconds before checking again
        time.sleep(2)
        
    except KeyboardInterrupt:
        print("Shutting down sensor...")
        break
    except Exception as e:
        print(f"[-] Loop error: {e}")
        time.sleep(2)
