from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Após clicar em Entrar, redireciona para o dashboard
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data_nota_str = request.form.get('data_nota')
    valor = request.form.get('valor')
    
    # Lógica central: Converte o texto em data e soma 30 dias
    data_nota = datetime.strptime(data_nota_str, '%Y-%m-%d')
    data_vencimento = data_nota + timedelta(days=30)
    
    return f"""
    <div style="font-family: Arial; padding: 20px;">
        <h3>Cálculo Realizado com Sucesso</h3>
        <p>Valor Registado: <b>R$ {valor}</b></p>
        <p>Data Limite de Pagamento: <b style="color: red;">{data_vencimento.strftime('%d/%m/%Y')}</b></p>
        <br><a href='/dashboard'>Voltar ao formulário</a>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)