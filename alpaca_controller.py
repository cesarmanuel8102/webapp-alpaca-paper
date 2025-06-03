import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    headers = {
        "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_API_SECRET")
    }
    # Se usa la URL fija de Alpaca (modo paper)
    response = requests.get("https://paper-api.alpaca.markets/v2/account", headers=headers)
    account_data = response.json()
    return render_template("index.html", account=account_data)

if __name__ == "__main__":
    app.run(debug=True)
