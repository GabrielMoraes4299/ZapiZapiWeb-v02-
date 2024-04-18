from conexao import Connection
from hashlib import sha256

class Usuario:
    def __init__(self) -> None:
        self.nome = None
        self.telefone = None
        self.senha = None
        self.logado = False

    def cadastrar(self, nome, telefone, senha):
        try:

            myBD = Connection.conectar()

            mycursor = myBD.cursor()

            self.nome = nome
            self.telefone = telefone
            self.senha = senha
            self.logado = True
            senha_criptografada = sha256(self.senha.encode()).hexdigest()

            mycursor.execute(f"INSERT INTO tb_usuario (nome, tel, senha) VALUES ('{nome}', '{telefone}', '{senha_criptografada}');")

            myBD.commit()

            myBD.close()

            return True
        except:
            return False

    def logar(self, telefone, senha):
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        self.senha = senha
        senha_criptografada = sha256(self.senha.encode()).hexdigest()

        mycursor.execute(f"SELECT nome, tel, senha FROM tb_usuario WHERE tel = '{telefone}' AND BINARY senha = '{senha_criptografada}';")

        resultado = mycursor.fetchone()

        if resultado != None:
            self.logado = True
            self.nome = resultado[0]
            self.telefone = resultado[1]
            self.senha = resultado[2]
        else:
            self.logado = False
    
        myBD.close()

    def listar_contatos(self):
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        mycursor.execute(f"SELECT nome, tel FROM tb_usuario")

        resultado = mycursor.fetchall()

        for x in resultado:
            print("--------------------")
            print(f"| {x[0]} | {x[1]} |")
            print("--------------------")

        myBD.close()