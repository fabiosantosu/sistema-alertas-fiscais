from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data_nota_str = request.form.get('data_nota')
    valor = request.form.get('valor')
    
    data_nota = datetime.strptime(data_nota_str, '%Y-%m-%d')
    data_vencimento = data_nota + timedelta(days=30)
    data_formatada = data_vencimento.strftime('%d/%m/%Y')
    
    # Aqui está a refatoração: enviamos as variáveis para o novo template
    return render_template('resultado.html', valor=valor, data=data_formatada)

if __name__ == '__main__':
    app.run(debug=True)