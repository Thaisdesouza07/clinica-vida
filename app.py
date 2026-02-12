from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

import os
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", "!Resileincia"),
        database=os.environ.get("MYSQL_DB", "clinica"),
        port=int(os.environ.get("MYSQL_PORT", 3306))
    )


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            idade INT NOT NULL,
            telefone VARCHAR(20) UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            paciente_id INT NOT NULL,
            data DATE NOT NULL,
            horario TIME NOT NULL,
            observacao TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


criar_tabelas()


@app.route("/", methods=["GET", "POST"])
def index():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        telefone = request.form["telefone"]

        try:
            cursor.execute(
                "INSERT INTO pacientes (nome, idade, telefone) VALUES (%s, %s, %s)",
                (nome, idade, telefone)
            )
            conn.commit()
        except mysql.connector.Error:
            cursor.close()
            conn.close()
            return "Paciente já cadastrado."

    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("index.html", pacientes=pacientes)


@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()

    if request.method == "POST":
        paciente_id = request.form["paciente_id"]
        data = request.form["data"]
        horario = request.form["horario"]
        observacao = request.form["observacao"]

        cursor.execute("""
            INSERT INTO consultas (paciente_id, data, horario, observacao)
            VALUES (%s, %s, %s, %s)
        """, (paciente_id, data, horario, observacao))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/consultas")

    cursor.close()
    conn.close()
    return render_template("agendar.html", pacientes=pacientes)


@app.route("/consultas")
def consultas():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT consultas.id, pacientes.nome, consultas.data,
               consultas.horario, consultas.observacao
        FROM consultas
        JOIN pacientes ON consultas.paciente_id = pacientes.id
        ORDER BY consultas.data
    """)

    consultas = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("consultas.html", consultas=consultas)


@app.route("/cancelar/<int:id>")
def cancelar(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM consultas WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect("/consultas")


if __name__ == "__main__":
    app.run(debug=True)
