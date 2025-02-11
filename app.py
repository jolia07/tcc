from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from bd import db, Usuario  # Importa o banco e o modelo

app = Flask(__name__)

eventos = {}

app.config['SECRET_KEY'] = 'seuSegredoAqui'
# Configuração de cookies da sessão
app.config['SESSION_COOKIE_SECURE'] = False  # True se estiver usando HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = 24 * 60 * 60  # 24 horas

@app.route('/set_session')
def set_session():
    session['usuario'] = "{usuario}"
    return "Sessão criada!"

@app.route('/get_session')
def get_session():
    usuario = session.get('usuario', 'Usuário não logado')
    return f"Usuário na sessão: {usuario}"

@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Remove o usuário da sessão
    return "Sessão encerrada!"

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
    
    senha_hash = generate_password_hash(senha)  

    novo_usuario = Usuario(nome=nome, email=email, senha=senha, telefone=telefone)
    
    try:
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for("home"))
    except Exception as e:
        db.session.rollback()
        return f"Erro ao cadastrar: {e}", 500
    
# Rota para login de usuário
@app.route("/logar", methods=["POST"])
def logar():
    email = request.form.get("email")
    senha = request.form.get("senha")

    # Verifica se o usuário existe no banco
    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario.senha == senha:  # Aqui seria ideal usar hash para senhas!
        session["usuario_id"] = usuario.id  # Guarda o ID do usuário na sessão
        session["usuario_nome"] = usuario.nome
        return redirect(url_for("calendario"))  # Redireciona para o calendário
    else:
        return "Email ou senha inválidos!", 401

# Criar tabelas no banco ao iniciar
with app.app_context():
    db.create_all()

#Rota do calendário
@app.route("/add_event", methods=["POST"])
def add_event():
    data = request.json
    date = data["date"]
    event = data["event"]
    
    if date in eventos:
        eventos[date].append(event)
    else:
        eventos[date] = [event]
    
    return jsonify({"message": "Evento adicionado!"})

# Rota para obter eventos de uma data específica
@app.route("/get_events/<date>")
def get_events(date):
    if "usuario_id" not in session:
        return jsonify({"error": "Acesso negado! Faça login primeiro."}), 403

    return jsonify({"events": eventos.get(date, [])})

if __name__ == "__main__":
    app.run(debug=True)