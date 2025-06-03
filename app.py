from flask import Flask, redirect, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("ALPACA_OAUTH_CLIENT_ID")
REDIRECT_URI = os.getenv("ALPACA_OAUTH_REDIRECT_URI")

@app.route("/")
def home():
    return '''
    <h1>Conectar con Alpaca</h1>
    <a href="/login">Iniciar sesión con Alpaca</a>
    '''

@app.route("/login")
def login():
    auth_url = (
        "https://app.alpaca.markets/oauth/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=account:write%20trading"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    return f"Código recibido: {code}"