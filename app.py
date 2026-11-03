from flask import Flask

app = Flask(__name__)

@app.route('/')
def login():
    return "<h1>Sistema de Alertas Fiscais</h1><p>O servidor Flask está rodando com sucesso!</p>"

if __name__ == '__main__':
    app.run(debug=True)