from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def conectar():
    conn = sqlite3.connect("clinica.db")
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data TEXT,
            horario TEXT,
            observacao TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    criar_tabelas()

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        telefone = request.form["telefone"]

        cursor.execute(
            "INSERT INTO pacientes (nome, idade, telefone) VALUES (?, ?, ?)",
            (nome, idade, telefone)
        )
        conn.commit()

    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()

    conn.close()

    return render_template("index.html", pacientes=pacientes)


@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()

    if request.method == "POST":
        paciente_id = request.form["paciente_id"]
        data = request.form["data"]
        horario = request.form["horario"]
        observacao = request.form["observacao"]

        cursor.execute("""
            INSERT INTO consultas (paciente_id, data, horario, observacao)
            VALUES (?, ?, ?, ?)
        """, (paciente_id, data, horario, observacao))

        conn.commit()
        conn.close()
        return redirect("/consultas")

    conn.close()
    return render_template("agendar.html", pacientes=pacientes)


@app.route("/consultas")
def consultas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT consultas.id, pacientes.nome, consultas.data,
               consultas.horario, consultas.observacao
        FROM consultas
        JOIN pacientes ON consultas.paciente_id = pacientes.id
        ORDER BY consultas.data
    """)

    consultas = cursor.fetchall()
    conn.close()

    return render_template("consultas.html", consultas=consultas)


@app.route("/cancelar/<int:id>")
def cancelar(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM consultas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/consultas")


if __name__ == "__main__":
    app.run(debug=True)

