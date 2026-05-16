import json
import os
from datetime import datetime

class LocalLogger:
    def __init__(self, filename="raw_events.jsonl"):
        """
        Initializes the local logger. 
        Creates a 'logs' directory if it does not already exist.
        """
        self.log_dir = "logs"
        self.filepath = os.path.join(self.log_dir, filename)
        
        # Ensure the log directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def log(self, event):
        """
        Persists the event data locally with a client-side timestamp.
        Stored in JSONL format (one JSON object per line).
        """
        try:
            entry = {
                "client_capture_timestamp": datetime.now().isoformat(),
                "raw_data": event
            }
            # Open in append mode to add new events to the end of the file
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"Local Logger Error: {e}")