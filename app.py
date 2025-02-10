from flask import Flask, request, render_template, redirect, url_for
from bd import db, Usuario  # Importa o banco e o modelo

app = Flask(__name__)

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jujuBA007.@localhost/python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa o banco com o Flask

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    telefone = request.form.get("telefone")

    if not nome or not email or not senha or not telefone:
        return "Todos os campos são obrigatórios!", 400

    novo_usuario = Usuario(nome=nome, email=email, senha=senha, telefone=telefone)
    
    try:
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for("home"))
    except Exception as e:
        db.session.rollback()
        return f"Erro ao cadastrar: {e}", 500

# Criar tabelas no banco ao iniciar
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)