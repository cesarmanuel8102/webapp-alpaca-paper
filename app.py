
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import alpaca_trade_api as tradeapi

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("BASE_URL")

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ejecutar", methods=["POST"])
def ejecutar():
    try:
        # Ejemplo: obtener cuenta
        account = api.get_account()
        return f"Cuenta: {account.status}"
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
