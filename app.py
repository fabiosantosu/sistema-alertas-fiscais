from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do ficheiro .env
load_dotenv()

app = Flask(__name__)

# Configuração da ligação ao banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///testes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar a extensão SQLAlchemy
db = SQLAlchemy(app)

# --- MODELO DO BANCO DE DADOS (Tabela) ---
class CalculoFiscal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data_fatura = db.Column(db.Date, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)

# Cria as tabelas automaticamente se não existirem
with app.app_context():
    db.create_all()

# --- ROTAS ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Busca os últimos 5 cálculos registrados, ordenados do mais recente para o mais antigo
    ultimos_calculos = CalculoFiscal.query.order_by(CalculoFiscal.id.desc()).limit(5).all()
    return render_template('dashboard.html', calculos=ultimos_calculos)

@app.route('/calcular', methods=['POST'])
def calcular():
    data_nota_str = request.form.get('data_nota')
    valor_str = request.form.get('valor')
    
    data_nota = datetime.strptime(data_nota_str, '%Y-%m-%d')
    data_vencimento = data_nota + timedelta(days=30)
    data_formatada = data_vencimento.strftime('%d/%m/%Y')
    
    # Salvar o novo cálculo no banco de dados
    novo_calculo = CalculoFiscal(
        valor=float(valor_str),
        data_fatura=data_nota,
        data_vencimento=data_vencimento
    )
    db.session.add(novo_calculo)
    db.session.commit()
    
    return render_template('resultado.html', valor=valor_str, data=data_formatada)

if __name__ == '__main__':
    app.run(debug=True)
