import os
import webbrowser
from flask import Flask, request
from dotenv import load_dotenv

# 👇 Cargar el archivo de entorno correcto
load_dotenv(dotenv_path=".env.alpaca-oauth")

app = Flask(__name__)

CLIENT_ID = os.getenv("ALPACA_OAUTH_CLIENT_ID")
CLIENT_SECRET = os.getenv("ALPACA_OAUTH_CLIENT_SECRET")
REDIRECT_URI = os.getenv("ALPACA_OAUTH_REDIRECT_URI")

auth_url = (
    f"https://app.alpaca.markets/oauth/authorize"
    f"?response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope=account:write+trading"
)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    return f"✅ Código recibido: {code}"

if __name__ == "__main__":
    print(f"🌐 Abriendo navegador para autorizar con client_id={CLIENT_ID} ...")
    webbrowser.open(auth_url)
    app.run(port=8080)
