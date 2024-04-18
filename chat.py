from usuario import Usuario
from mensagem import Mensagem
from conexao import Connection
from contato import Contato

class Chat:
    def __init__(self, nome_usuario:str, telefone_usuario: str):
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario
    
    def enviar_mensagem(self, conteudo: str, destinatario:Contato) -> bool:
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        self.conteudo = conteudo
        self.destinatario = destinatario
        tel_remetente = self.telefone_usuario
        tel_destinatario = destinatario.telefone
        mensagem = conteudo

        mycursor.execute(f"INSERT INTO tb_mensagem (tel_remetente, tel_destinatario, mensagem) VALUES ('{tel_remetente}', '{tel_destinatario}', '{mensagem}');")

        myBD.commit()
        myBD.close()
        return True

    def verificar_mensagem(self, quantidade: int, destinatario:Contato):
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        self.destinatario = destinatario

        mycursor.execute(f"SELECT nome, mensagem FROM tb_usuario u , tb_mensagem m WHERE (m.tel_remetente = u.tel) AND (tel_remetente = '{self.telefone_usuario}' AND tel_destinatario = '{destinatario.telefone}' OR tel_remetente = '{destinatario.telefone}' AND tel_destinatario = '{self.telefone_usuario}') ORDER BY id_mensagem")

        resultado = mycursor.fetchall()

        lista_mensagens = []

        for x in resultado:
            # Tudo em uma linha só
            # lista_mensagem.append(Mensagem(x[0], x[1]))

            mensagem = Mensagem(x[0], x[1])
            lista_mensagens.append({"nome":mensagem.remetente, "conteudo":mensagem.conteudo})

        myBD.close()
        return (lista_mensagens)
    
    def retornar_contatos(self):
        myBD = Connection.conectar()

        mycursor = myBD.cursor()

        mycursor.execute("SELECT nome, tel FROM tb_usuario ORDER BY nome")

        resultado = mycursor.fetchall()

        lista_contatos = []

        lista_contatos.append({"nome":"TODOS", "telefone":""})

        for x  in resultado:
            lista_contatos.append({"nome":x[0], "telefone":x[1]})
        myBD.close()
        return (lista_contatos)