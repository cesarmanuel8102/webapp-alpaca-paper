from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'alpaca_secret_key'

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
        logs.append(f"[{datetime.datetime.now()}] Modelo cargado: {file.filename}")
        flash(f'Modelo cargado: {file.filename}')
        return redirect(url_for('index'))
    else:
        flash('Solo se permiten archivos .py')
        return redirect(url_for('index'))

@app.route('/log_response', methods=['POST'])
def log_response():
    response = request.form.get('response')
    if response:
        logs.append(f"[{datetime.datetime.now()}] Alpaca API: {response}")
    return '', 204

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)