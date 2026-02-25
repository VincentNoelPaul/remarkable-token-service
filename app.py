from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

RM_URL = "https://webapp-production-dot-remarkable-production.appspot.com/token/json/2/device/new"

# Accept both /token and /token/ to avoid 404 issues
@app.route("/token", methods=["POST"])
@app.route("/token/", methods=["POST"])
def token():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "").strip()

    if not code or len(code) != 8:
        return jsonify({"error": "Invalid code"}), 400

    payload = {
        "code": code,
        "deviceDesc": "mobile-browser",
        "deviceID": "mydeviceid123"
    }

    try:
        resp = requests.post(RM_URL, json=payload)
        return resp.text, resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Optional: a simple health check
@app.get("/health")
def health():
    return "OK", 200
