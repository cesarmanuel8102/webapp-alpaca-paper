from flask import Flask, render_template, request, redirect, url_for
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_PAPER_BASE_URL")

@app.route("/")
def index():
    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY
    }
    response = requests.get(f"{BASE_URL}/v2/account", headers=headers)
    if response.status_code == 200:
        account_info = response.json()
        return render_template("panel.html", account=account_info)
    else:
        return f"Error al conectar con Alpaca: {response.text}", 500

@app.route("/ejecutar_modelo", methods=["POST"])
def ejecutar_modelo():
    # Aquí se puede integrar lógica de operaciones reales de compra/venta
    return "Modelo ejecutado correctamente."

if __name__ == "__main__":
    app.run(debug=True)
