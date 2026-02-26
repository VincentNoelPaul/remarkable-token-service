from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

RM_URL = "https://webapp-production-dot-remarkable-production.appspot.com/token/json/2/device/new"

# Homepage (your UI)
@app.get("/")
def home():
    return """
    <html>
    <body>
    <h2>reMarkable Token Generator</h2>
    <p>Paste your 8-letter code below:</p>
    <input id="code" placeholder="ABCDEFGH" />
    <button onclick="go()">Get Token</button>
    <pre id="out"></pre>

    <script>
    async function go() {
      const code = document.getElementById("code").value.trim();
      const res = await fetch(window.location.origin + "/token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
      });
      document.getElementById("out").textContent = await res.text();
    }
    </script>
    </body>
    </html>
    """

@app.route("/token", methods=["POST"])
@app.route("/token/", methods=["POST"])
def token():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "").strip()

    if not code or len(code) != 8:
        return jsonify({"error": "Invalid code"}), 400

    payload = {
        "code": code,
        "deviceDesc": "desktop-windows",
        "deviceID": str(uuid.uuid4())
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(RM_URL, json=payload, headers=headers, timeout=10)
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to reach reMarkable API: {e}"}), 502

    if resp.ok:
        return resp.text, resp.status_code

    # The API returns HTML error pages on failure — return a clean JSON error instead
    try:
        error_body = resp.json()
    except (ValueError, requests.exceptions.JSONDecodeError):
        error_body = {"error": f"reMarkable API returned status {resp.status_code}"}
    return jsonify(error_body), resp.status_code


# Health check
@app.get("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
