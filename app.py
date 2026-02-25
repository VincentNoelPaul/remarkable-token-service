from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

RM_URL = "https://webapp-production-dot-remarkable-production.appspot.com/token/json/2/device/new"

@app.route("/", methods=["GET"])
def home():
    return """<html>
<body>
<h2>reMarkable Token Generator</h2>
<p>Paste your 8-letter code below:</p>
<input id="code" placeholder="ABCDEFGH" />
<button onclick="go()">Get Token</button>
<pre id="out"></pre>

<script>
async function go() {
  const code = document.getElementById("code").value.trim();
  const res = await fetch("/token", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code })
  });
  document.getElementById("out").textContent = await res.text();
}
</script>
</body>
</html>"""
