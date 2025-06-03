
import os
import importlib.util
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import traceback

load_dotenv()

APCA_API_KEY_ID = os.getenv("APCA_API_KEY_ID")
APCA_API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("BASE_URL")

app = Flask(__name__)
LOGS = []
ORDERS = []

# Cargar el modelo dinámicamente
def cargar_modelo():
    try:
        spec = importlib.util.spec_from_file_location("modelo_cargado", "modelo_cargado.py")
        modelo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modelo)
        return modelo
    except Exception as e:
        LOGS.append(f"❌ Error al cargar modelo: {e}")
        return None

@app.route("/")
def index():
    return render_template("index.html", logs=LOGS, orders=ORDERS)

@app.route("/iniciar", methods=["POST"])
def iniciar():
    LOGS.clear()
    ORDERS.clear()
    modelo = cargar_modelo()
    if modelo:
        try:
            resultado = modelo.main() if hasattr(modelo, 'main') else "Modelo no tiene función main()"
            LOGS.append(f"✅ Resultado ejecución: {resultado}")
        except Exception as e:
            LOGS.append(f"❌ Error ejecutando modelo: {e}")
            LOGS.append(traceback.format_exc())
    return redirect(url_for("index"))

@app.route("/ordenes", methods=["GET"])
def ordenes():
    try:
        api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, BASE_URL)
        alpaca_orders = api.list_orders(status='all', limit=10)
        ORDERS.clear()
        for o in alpaca_orders:
            ORDERS.append({
                "ticker": o.symbol,
                "asset_class": o.asset_class,
                "order_type": o.order_type,
                "side": o.side,
                "qty": o.qty,
                "filled_qty": o.filled_qty,
                "avg_fill_price": o.filled_avg_price,
                "status": o.status,
                "source": o.client_order_id,
                "submitted_at": str(o.submitted_at),
                "filled_at": str(o.filled_at),
                "expires_at": str(o.expired_at)
            })
        LOGS.append("✅ Órdenes recuperadas correctamente de Alpaca.")
    except Exception as e:
        LOGS.append(f"❌ Error recuperando órdenes: {e}")
        LOGS.append(traceback.format_exc())
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
