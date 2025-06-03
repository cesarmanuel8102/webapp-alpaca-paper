from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'alpaca_secret_key'

# Asegura que la carpeta exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

logs = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', logs=logs)

@app.route('/upload', methods=['POST'])
def upload_model():
    if 'model' not in request.files:
        flash('No se seleccionó ningún archivo.')
        return redirect(url_for('index'))
    file = request.files['model']
    if file.filename == '':
        flash('Nombre de archivo vacío.')
        return redirect(url_for('index'))
    if file and file.filename.endswith('.py'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        logs.append(f"[{datetime.datetime.]()
