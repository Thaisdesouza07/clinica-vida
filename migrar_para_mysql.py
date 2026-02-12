import sqlite3
import mysql.connector

# Conectar SQLite
sqlite_conn = sqlite3.connect("clinica.db")
sqlite_cursor = sqlite_conn.cursor()

sqlite_cursor.execute("SELECT nome, idade, telefone FROM pacientes")
dados = sqlite_cursor.fetchall()


# Conectar MySQL
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="!Resiliencia",
    database="clinica"
)

mysql_cursor = mysql_conn.cursor()


# Inserir dados no MySQL
for paciente in dados:
    mysql_cursor.execute("""
        INSERT INTO pacientes (nome, idade, telefone)
        VALUES (%s, %s, %s)
    """, paciente)

mysql_conn.commit()

print("Dados migrados com sucesso!")

sqlite_conn.close()
mysql_conn.close()
