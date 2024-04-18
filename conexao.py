import mysql.connector

class Connection:
    def conectar():
        myBD = mysql.connector.connect(
            host = "10.110.140.136",
            user="equipe",
            password="123456789",
            database="colazap"
        )

        return myBD