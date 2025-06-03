from flask import Flask, redirect, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

CLIENT_ID = os.getenv("ALPACA_CLIENT_ID")
CLIENT_SECRET = os.getenv("ALPACA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("ALPACA_REDIRECT_URI")
BASE_AUTH_URL = "https://app.alpaca.markets/oauth/authorize"
BASE_TOKEN_URL = "https://api.alpaca.markets/oauth/token"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    scopes = "account:write trading"
    auth_url = f"{BASE_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={scopes}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: No code provided", 400

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(BASE_TOKEN_URL, data=data)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
