# The Mock Client Sensor

import requests
import time
import random

BACKEND_URL = "http://169.254.197.25:8000/api/logs"


def generate_mock_data():
    """Generates random telemetry, occasionally injecting poisoned data."""

    # 15% chance to generate an anomaly (Honeypot scenario)
    is_anomaly = random.random() < 0.15

    # Randomly pick event type
    if random.choice(["network", "system"]) == "network":
        return {
            "event_type": "network",
            "source_ip": f"192.168.1.{random.randint(2, 254)}",
            "dest_ip": f"10.0.0.{random.randint(1, 100)}",
            "source_port": random.randint(1024, 65535),
            # Inject port 4444 if anomaly, otherwise normal HTTP/HTTPS ports
            "dest_port": 4444 if is_anomaly else random.choice([80, 443, 8080]),
            "protocol": "TCP"
        }
    else:
        return {
            "event_type": "system",
            "process_name": random.choice(["chrome", "svchost", "explorer", "cmd", "unknown_process"]),
            # Inject > 500MB if anomaly, otherwise 50-200MB
            "memory_usage_mb": round(random.uniform(550.0, 900.0) if is_anomaly else random.uniform(50.0, 200.0), 2)
        }


def run_sensor():
    """Continuous loop to simulate 24/7 endpoint monitoring."""
    print("Starting mock EDR sensor. Press Ctrl+C to stop.")

    while True:
        payload = generate_mock_data()

        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=2)

            if response.status_code == 200:
                result = response.json()
                if result.get("alert_triggered"):
                    print(f"[-] Sent anomaly! Backend caught it: {payload}")
                else:
                    print(f"[+] Sent normal {payload['event_type']} event.")
            else:
                print(f"[!] Server returned error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("[!] Connection failed. Is the FastAPI backend running?")

        # Wait 1-3 seconds before sending the next log
        time.sleep(random.uniform(1, 3))


if __name__ == "__main__":
    run_sensor()