from flask import Flask, redirect, request, session, url_for, jsonify
import os
import requests
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "test_secret")

CLIENT_ID = os.getenv("ALPACA_CLIENT_ID")
CLIENT_SECRET = os.getenv("ALPACA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
BASE_URL = os.getenv("BASE_URL")

@app.route("/")
def home():
    return '<a href="/login">Iniciar sesión con Alpaca</a>'

@app.route("/login")
def login():
    query = urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "account:write trading",
    })
    return redirect(f"https://app.alpaca.markets/oauth/authorize?{query}")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Código no proporcionado", 400

    token_url = "https://api.alpaca.markets/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(token_url, json=payload)
    if response.status_code == 200:
        token_data = response.json()
        return jsonify(token_data)
    else:
        return f"Error al obtener token: {response.text}", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
