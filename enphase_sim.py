from flask import Flask, request, jsonify
import hashlib
from datetime import datetime
import subprocess

app = Flask(__name__)

# Mock internal state
device_state = {
    "serial_number": "1234567890ENPH",
    "firmware_version": "R5.10.65",
    "model": "Envoy-S Metered",
    "production_kw": 5.3,
    "auth_token": None,
    "username": "admin",
    "password_hash": None,  # Will be derived from serial
    "powerForcedOff": False,
    "inverters": [
        {"serial": "121715003401", "last_report_date": datetime.now().isoformat(), "watt": 270},
        {"serial": "121715003402", "last_report_date": datetime.now().isoformat(), "watt": 265}
    ],
    "firmware_version": "v5.10.65",
    "auth_mode": "strong",  # strong or weak
}

# Utility Functions

def generate_password(serial):
    hash_obj = hashlib.sha256(serial.encode())
    return hash_obj.hexdigest()[:8]

def is_authed(req):
    return req.headers.get("Authorization") == device_state["auth_token"]

# Initialize password from serial
if not device_state["password_hash"]:
    device_state["password_hash"] = generate_password(device_state["serial_number"])

# Public device info endpoint
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "serial_number": device_state["serial_number"],
        "model": device_state["model"],
        "software": device_state["firmware_version"]
    })

# Public production data
@app.route("/api/v1/production", methods=["GET"])
def prod():
    total_watts = sum(inv["watt"] for inv in device_state["inverters"])
    return jsonify({
        "wattHoursToday": 21340,
        "wattHoursSevenDays": 154340,
        "wattHoursLifetime": 11200342,
        "wattsNow": total_watts
    })

# Authenticated inverter stats
@app.route("/api/v1/production/inverters", methods=["GET"])
def get_inverters():
    if not is_authed(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(device_state["inverters"])


# Modify inverter stats
@app.route("/api/v1/production/inverters/<serial>", methods=["POST"])
def update_inverter(serial):
    if not is_authed(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    for inv in device_state["inverters"]:
        if inv["serial"] == serial:
            inv["watt"] = data.get("watt", inv["watt"])
            inv["last_report_date"] = datetime.now().isoformat()
            return jsonify({"message": "Inverter updated."})
    return jsonify({"error": "Inverter not found"}), 404


# Authenticated device list
@app.route("/api/v1/devices", methods=["GET"])
def devices():
    if not is_authed(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify([
        {
            "type": "PCU",
            "serialNumber": inv["serial"],
            "producing": not device_state["powerForcedOff"],
            "lastReportWatts": inv["watt"],
            "lastReportDate": inv["last_report_date"]
        }
        for inv in device_state["inverters"]
    ])

# Simulated insecure login endpoint
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = data.get("username")
    password = data.get("password")
    expected = device_state["password_hash"]
    if user == device_state["username"] and password == expected:
        token = "authtok_" + expected
        device_state["auth_token"] = token
        return jsonify({"token": token})
    return jsonify({"error": "Access denied"}), 403

# Power disable endpoints (unauthenticated for demo purposes)
DEVICE_ID = "603980032"

@app.route(f"/ivp/mod/{DEVICE_ID}/mode/power", methods=["GET"])
def get_power_state():
    return jsonify({
        "powerForcedOff": device_state["powerForcedOff"]
    })

@app.route(f"/ivp/mod/{DEVICE_ID}/mode/power", methods=["POST"])
def set_power_state():
    data = request.json
    forced_off = data.get("powerForcedOff")
    if isinstance(forced_off, bool):
        device_state["powerForcedOff"] = forced_off
        return jsonify({"message": f"Power state updated. Forced off: {forced_off}"})
    return jsonify({"error": "Invalid or missing parameter"}), 400

# Simulate firmware upgrade (vulnerability for LoTL)

@app.route("/installer/upgrade_start", methods=["POST"])
def upgrade_start():
    data = request.get_json()
    firmware_url = data.get("firmware_url", "").lower()

    if "v4.2.11" in firmware_url:
        device_state["firmware_version"] = "v4.2.11"
        device_state["auth_mode"] = "weak"
        return jsonify({
            "status": "Firmware downgraded",
            "version": "v4.2.11",
            "message": "Legacy version enabled weak authentication (e.g., default password)."
        }), 200

    elif "v5.10.65" in firmware_url:
        device_state["firmware_version"] = "v5.10.65"
        device_state["auth_mode"] = "strong"
        return jsonify({
            "status": "Firmware upgraded to latest",
            "version": "v5.10.65",
            "message": "System is secure"
        }), 200

    else:
        return jsonify({"error": "Unsupported or unknown firmware image"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
