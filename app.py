
from flask import Flask, render_template, request, jsonify
import requests
import os
import datetime

app = Flask(__name__)

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY,
    "Content-Type": "application/json"
}

modelo_actual = {"nombre": "Modelo Oficial", "activo": False, "resultado": ""}

@app.route("/")
def index():
    return render_template("index.html", modelo=modelo_actual)

@app.route("/ejecutar_modelo", methods=["POST"])
def ejecutar_modelo():
    now = datetime.datetime.now().time()
    hora_actual = now.strftime("%H:%M:%S")
    resultado = ""

    if not (datetime.time(10,30) <= now <= datetime.time(11,15)):
        resultado = f"⛔ Orden bloqueada: fuera de horario permitido (hora actual: {hora_actual})."
        modelo_actual["resultado"] = resultado
        return jsonify({"status": "fuera_horario", "detalle": resultado})

    orden = {
        "symbol": "AAPL",
        "qty": 1,
        "side": "buy",
        "type": "market",
        "time_in_force": "gtc"
    }

    url = f"{ALPACA_BASE_URL}/v2/orders"
    response = requests.post(url, headers=HEADERS, json=orden)

    resultado = f"✅ Orden enviada. Código: {response.status_code}, Respuesta: {response.text}"
    modelo_actual["resultado"] = resultado
    return jsonify({"status": "orden_enviada", "detalle": resultado})

@app.route("/detener_modelo", methods=["POST"])
def detener_modelo():
    modelo_actual["activo"] = False
    modelo_actual["resultado"] = "⏹ Modelo detenido manualmente."
    return jsonify({"status": "modelo_detenido"})

@app.route("/estado_modelo")
def estado_modelo():
    return jsonify(modelo_actual)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
