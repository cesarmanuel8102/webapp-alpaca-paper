import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

modelo_actual = {"estado": "Esperando ejecución...", "nombre": "Ninguno", "ordenes": []}

@app.route("/", methods=["GET"])
def index():
    headers = {
        "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_API_SECRET")
    }
    response = requests.get("https://paper-api.alpaca.markets/v2/account", headers=headers)
    account_data = response.json()
    return render_template("index.html", account=account_data, modelo=modelo_actual)

@app.route("/cargar_modelo", methods=["POST"])
def cargar_modelo():
    nombre = request.form.get("modelo")
    modelo_actual["nombre"] = nombre
    modelo_actual["estado"] = "Modelo cargado"
    return jsonify(success=True)

@app.route("/ejecutar_modelo", methods=["POST"])
def ejecutar_modelo():
    modelo_actual["estado"] = "Ejecutando modelo..."
    modelo_actual["ordenes"].append({"ticker": "AAPL", "tipo": "buy", "cantidad": 1, "precio": 192.5})
    return jsonify(success=True)

@app.route("/detener_modelo", methods=["POST"])
def detener_modelo():
    modelo_actual["estado"] = "Modelo detenido"
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)