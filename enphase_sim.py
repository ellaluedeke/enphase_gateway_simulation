from flask import Flask, request, jsonify
import hashlib
from datetime import datetime

app = Flask(__name__)

# Mock internal state
device_state = {
    "serial_number": "1234567890ENPH",
    "firmware_version": "R5.10.65",
    "model": "Envoy-S Metered",
    "production_kw": 5.3,
    "auth_token": None,
    "inverters": [
        {"serial": "121715003401", "last_report_date": datetime.now().isoformat(), "watt": 270},
        {"serial": "121715003402", "last_report_date": datetime.now().isoformat(), "watt": 265}
    ]
}

# ----------- Utility Functions -----------

def generate_password(serial):
    hash_obj = hashlib.sha256(serial.encode())
    return hash_obj.hexdigest()[:8]

def is_authed(req):
    return req.headers.get("Authorization") == device_state["auth_token"]

# ----------- API Endpoints -----------

# /info (public)
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "serial_number": device_state["serial_number"],
        "model": device_state["model"],
        "software": device_state["firmware_version"]
    })

# /api/v1/production (public)
@app.route("/api/v1/production", methods=["GET"])
def prod():
    return jsonify({
        "wattHoursToday": 21340,
        "wattHoursSevenDays": 154340,
        "wattHoursLifetime": 11200342,
        "wattsNow": int(device_state["production_kw"] * 1000)
    })

# /api/v1/production/inverters (requires auth)
@app.route("/api/v1/production/inverters", methods=["GET"])
def inverter_stats():
    if not is_authed(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(device_state["inverters"])

# /api/v1/devices (requires auth)
@app.route("/api/v1/devices", methods=["GET"])
def devices():
    if not is_authed(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify([
        {
            "type": "PCU",
            "serialNumber": inv["serial"],
            "producing": True,
            "lastReportWatts": inv["watt"],
            "lastReportDate": inv["last_report_date"]
        }
        for inv in device_state["inverters"]
    ])

# /api/login (insecure custom logic)
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = data.get("username")
    password = data.get("password")
    if user == "admin":
        expected = generate_password(device_state["serial_number"])
        if password == expected:
            device_state["auth_token"] = "authtok_" + expected
            return jsonify({"token": device_state["auth_token"]})
    return jsonify({"error": "Access denied"}), 403

# Spoof production (simulates attacker success)
@app.route("/api/spoof", methods=["POST"])
def spoof():
    if not is_authed(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    if "production_kw" in data:
        device_state["production_kw"] = float(data["production_kw"])
        return jsonify({"message": "Production spoofed."})
    return jsonify({"error": "Missing value"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
