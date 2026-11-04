import pytest
from app import app, db, CalculoFiscal

@pytest.fixture
def client():
    # Configura a aplicação para o modo de testes com um banco em memória temporário
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_rota_login_get(client):
    # Teste unitário: Renderização inicial
    resposta = client.get('/')
    assert resposta.status_code == 200

def test_rota_login_post(client):
    # Teste unitário: Redirecionamento após login
    resposta = client.post('/', data={'email': 'teste@teste.com', 'senha': '123'})
    assert resposta.status_code == 302

def test_rota_dashboard(client):
    # Teste unitário: Renderização do painel
    resposta = client.get('/dashboard')
    assert resposta.status_code == 200

def test_calculo_e_integracao_banco(client):
    # Teste de Integração: Fluxo completo de cálculo e gravação no banco
    resposta = client.post('/calcular', data={
        'data_nota': '2026-11-20',
        'valor': '5000'
    })
    
    assert resposta.status_code == 200
    assert b'20/12/2026' in resposta.data # Verifica a soma de 30 dias no HTML retornado
    
    # Verifica a integridade da persistência no banco de dados de teste
    with app.app_context():
        calculo = CalculoFiscal.query.first()
        assert calculo is not None
        assert calculo.valor == 5000.0
        assert calculo.data_vencimento.strftime('%Y-%m-%d') == '2026-12-20'