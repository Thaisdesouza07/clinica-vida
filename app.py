from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def conectar():
    return sqlite3.connect("clinica.db")


@app.route("/", methods=["GET", "POST"])
def index():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            telefone TEXT
        )
    """)

    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        telefone = request.form["telefone"]

        cursor.execute(
            "INSERT INTO pacientes (nome, idade, telefone) VALUES (?, ?, ?)",
            (nome, idade, telefone)
        )
        conn.commit()

    cursor.execute("SELECT nome, idade, telefone FROM pacientes")
    pacientes = cursor.fetchall()

    conn.close()

    return render_template("index.html", pacientes=[
        {"nome": p[0], "idade": p[1], "telefone": p[2]}
        for p in pacientes
    ])


if __name__ == "__main__":
    app.run()

