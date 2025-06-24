from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Simulated device state
device_state = {
    "serial_number": "1234567890ENPH",
    "auth_token": None,
    "production_kw": 5.0,
    "config": {
        "max_output_kw": 6.0,
        "firmware_version": "v1.2.3"
    }
}

# Insecure password derived from serial number
def generate_password(serial):
    hash_obj = hashlib.sha256(serial.encode())
    return hash_obj.hexdigest()[:8]

# Leak serial number publicly
@app.route("/api/device_info", methods=["GET"])
def get_device_info():
    return jsonify({
        "serial_number": device_state["serial_number"]
    })

# Login using custom password logic
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

# Changing OS password does nothing (simulated)
@app.route("/api/changepass", methods=["POST"])
def change_password():
    return jsonify({"message": "Root password changed (but ignored by system auth)."}), 200

# Spoof production data (requires token)
@app.route("/api/fake_production", methods=["POST"])
def fake_prod():
    token = request.headers.get("Authorization")
    if token != device_state["auth_token"]:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    if "production_kw" in data:
        device_state["production_kw"] = data["production_kw"]
        return jsonify({"message": "Production spoofed."})
    return jsonify({"error": "Missing data"}), 400

# Get current state
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "production_kw": device_state["production_kw"],
        "config": device_state["config"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
