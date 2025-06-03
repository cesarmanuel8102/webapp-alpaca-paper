from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Simulación de ordenes y lógica Alpaca (placeholder realista)
@app.route("/simular")
def simular_orden():
    return "Simulación de orden ejecutada en entorno Alpaca (paper trading)"
