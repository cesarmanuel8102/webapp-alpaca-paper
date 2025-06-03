from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ejecutar_modelo", methods=["POST"])
def ejecutar_modelo():
    # Aquí se integrará el modelo Alpaca
    resultado = "Modelo Alpaca ejecutado correctamente."
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
