import os
from flask import Flask, redirect, request, jsonify
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("ALPACA_OAUTH_CLIENT_ID")
CLIENT_SECRET = os.getenv("ALPACA_OAUTH_CLIENT_SECRET")
REDIRECT_URI = os.getenv("ALPACA_OAUTH_REDIRECT_URI")

@app.route("/")
def home():
    return "✅ WebApp Alpaca OAuth2 está activa."

@app.route("/login")
def login():
    auth_url = (
        "https://app.alpaca.markets/oauth/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=account:write+trading"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url = "https://api.alpaca.markets/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(token_url, json=data)
    return jsonify(response.json())