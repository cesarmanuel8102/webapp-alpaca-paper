from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "WebApp Alpaca PaperTrading Activa"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Render necesita que se use este puerto
    app.run(host='0.0.0.0', port=port)