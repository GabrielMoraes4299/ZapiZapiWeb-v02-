from flask import Flask, render_template, request, redirect, session, jsonify
from usuario import Usuario
from chat import Chat
from contato import Contato

app = Flask(__name__)

app.secret_key = "capivara"

@app.route("/")
def pg_inicial():
    return render_template("index.html", campo_usuario = False)

@app.route("/cadastrar")
def pg_cadasatrar_form():
    return render_template("cadastrar.html")

@app.route("/cadastrar", methods=["POST"])
def pg_cadastro():
    if session.get("usuario","erro") == "Autenticado":
        return render_template("cadastrar.html")
    else:
        dados = request.get_json()
        nome = dados["nome"]
        telefone = dados["telefone"]
        senha = dados["senha"]

        usuario = Usuario()

        if usuario.cadastrar(nome, telefone, senha):
            session["usuario"] = {"nome":nome,"telefone":telefone}
            return jsonify({'mensagem':'Cadastro OK'}), 200, redirect("/chat")
        else:
            return {'mensagem':'ERRO'}, 500

@app.route("/login", methods=["GET", "POST"])
def pg_login():
    usuario = Usuario()
    if request.method == "GET":
        if session.get("usuario","erro") == "Autenticado":   
            return render_template("chat.html")
        else:
            return render_template("login.html")
    else:
        telefone = request.form["telefone"]
        senha = request.form["senha"]

        usuario.logar(telefone, senha)

        if usuario.logado:
            session["usuario"] = {"nome":usuario.nome, "telefone":telefone}
            return redirect("/chat")
        else:
            session.clear()
            return redirect("/login")

@app.route("/chat")
def pg_chat():
    if "usuario" in session:
        return render_template("chat.html", campo_usuario = True, campo_nome = "Gabriel")
    else:
        return render_template("cadastrar.html")

@app.route("/retorna_usuarios")
def retorna_usuarios():
    nome_usuario = session["usuario"]["nome"]
    telefone_usuario = session["usuario"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)
    contatos = chat.retornar_contatos()
    return jsonify(contatos), 200

@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
    dados = request.get_json()
    conteudo_mensagem = dados["conteudo"]
    telefone = dados["telefone"]

    contato = Contato("", telefone)

    nome_usuario = session["usuario"]["nome"]
    telefone_usuario = session["usuario"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    chat.enviar_mensagem(conteudo_mensagem, contato)

    return jsonify({}), 200

@app.route("/get/mensagens/<tel_destinatario>")
def api_verificar_mensagem(tel_destinatario):
    nome_usuario = session["usuario"]["nome"]
    telefone_usuario = session["usuario"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    contato = Contato("", tel_destinatario)
    mensagens = chat.verificar_mensagem(0, contato)

    return jsonify(mensagens), 200

@app.route("/logoff")
def pagina_logoff():
    session.clear()
    return redirect("/")

app.run(host='0.0.0.0',port='8080')