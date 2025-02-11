from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from bd import db, Usuario, Evento  # Importa o banco, o modelo e o evento(calendario)

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
    print(session) #terminal
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

@app.route("/calendario")
def calendario():
    return render_template("calendario.html")

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    telefone = request.form.get("telefone")

    if not nome or not email or not senha or not telefone:
        return "Todos os campos são obrigatórios!", 400
    
    senha_hash = generate_password_hash(senha)  

    novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash, telefone=telefone)
    
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

    if usuario and check_password_hash(usuario.senha, senha):  # Aqui seria ideal usar hash para senhas!
        session["usuario_id"] = usuario.id  # Guarda o ID do usuário na sessão
        session["usuario_nome"] = usuario.nome

        # Exibe a sessão no terminal para depuração
        print("Sessão criada:", session)
        
        return redirect(url_for("calendario"))  # Redireciona para o calendário
    else:
        return "Email ou senha inválidos!", 401

# Criar tabelas no banco ao iniciar
with app.app_context():
    db.create_all()

# Rota para adicionar evento ao banco
@app.route("/add_event", methods=["POST"])
def add_event():
    if "usuario_id" not in session:
        return jsonify({"error": "Acesso negado! Faça login primeiro."}), 403
    
    data = request.json
    novo_evento = Evento(
        titulo=data["event"],
        data=data["date"],
        usuario_id=session["usuario_id"]
    )

    db.session.add(novo_evento)
    db.session.commit()
    
    return jsonify({"message": "Evento adicionado!"})

# Rota para obter eventos do usuário logado
@app.route("/get_events")
def get_events():
    if "usuario_id" not in session:
        return jsonify({"error": "Acesso negado! Faça login primeiro."}), 403

    eventos = Evento.query.filter_by(usuario_id=session["usuario_id"]).all()
    eventos_json = [{"id": e.id, "title": e.titulo, "start": e.data} for e in eventos]

    return jsonify(eventos_json)

# Rota para excluir evento
@app.route("/delete_event", methods=["POST"])
def delete_event():
    if "usuario_id" not in session:
        return jsonify({"error": "Acesso negado! Faça login primeiro."}), 403

    data = request.json
    evento = Evento.query.filter_by(id=data["event_id"], usuario_id=session["usuario_id"]).first()

    if not evento:
        return jsonify({"error": "Evento não encontrado!"}), 404

    db.session.delete(evento)
    db.session.commit()

    return jsonify({"message": "Evento removido!"})

if __name__ == "__main__":
    app.run(debug=True)