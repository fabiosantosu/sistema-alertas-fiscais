from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        # Mais tarde adicionar o hash seguro aqui
        return f"<h3>Sucesso!</h3><p>Autenticação simulada para: {email}</p>"
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)