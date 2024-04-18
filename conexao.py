import mysql.connector

class Connection:
    def conectar():
        myBD = mysql.connector.connect(
            host = "projetochat2.mysql.database.azure.com",
            user="equipe",
            password="123456789",
            database="colazap"
        )

        return myBD