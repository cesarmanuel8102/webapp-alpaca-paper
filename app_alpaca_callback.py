
from flask import Flask, request, redirect, jsonify
import requests
import os

app = Flask(__name__)

# Carga de configuración segura desde variables de entorno
CLIENT_ID = os.getenv("ALPACA_CLIENT_ID")
CLIENT_SECRET = os.getenv("ALPACA_CLIENT_SECRET")
REDIRECT_URI = "https://webapp-alpaca-paper.onrender.com/callback"
TOKEN_URL = "https://api.alpaca.markets/oauth/token"

@app.route("/callback")
def oauth_callback():
    code = request.args.get("code")
    if not code:
        return "❌ No authorization code provided.", 400

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code == 200:
        return jsonify({"✅ Access Token Response": response.json()})
    else:
        return jsonify({"❌ Error": response.text, "status_code": response.status_code}), 400

@app.route("/")
def home():
    return "WebApp Alpaca Callback Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
