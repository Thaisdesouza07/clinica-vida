import os
import sqlite3


# =========================
# FUNÇÕES UTILITÁRIAS
# =========================

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPressione ENTER para continuar...")
    limpar_tela()


# =========================
# BANCO DE DADOS
# =========================

def criar_banco():
    conexao = sqlite3.connect("clinica.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            telefone TEXT
        )
    """)

    conexao.commit()
    conexao.close()


# =========================
# CADASTRAR PACIENTE
# =========================

def cadastrar_paciente():
    print("\n==== CADASTRO DE PACIENTE ====")

    nome = input("Nome do Paciente: ").strip().title()
    if not nome:
        print("Erro: Nome não pode ser vazio.")
        return

    while True:
        try:
            idade = int(input("Idade do Paciente: "))
            if idade <= 0:
                print("Idade inválida.")
                continue
            break
        except ValueError:
            print("Digite um número válido.")

    telefone = input("Telefone: ").strip()

    conexao = sqlite3.connect("clinica.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO pacientes (nome, idade, telefone)
        VALUES (?, ?, ?)
    """, (nome, idade, telefone))

    conexao.commit()
    conexao.close()

    print(f"\n✅ Paciente '{nome}' cadastrado com sucesso!")


# =========================
# LISTAR PACIENTES
# =========================

def listar_todos_pacientes():
    limpar_tela()
    print("\n=== LISTA DE PACIENTES ===")

    conexao = sqlite3.connect("clinica.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome, idade, telefone
        FROM pacientes
        ORDER BY nome
    """)

    pacientes = cursor.fetchall()
    conexao.close()

    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return

    print("-" * 50)
    print(f"{'Nome':<20} | {'Idade':<5} | {'Telefone':<20}")
    print("-" * 50)

    for nome, idade, telefone in pacientes:
        print(f"{nome:<20} | {idade:<5} | {telefone:<20}")

    print("-" * 50)
    print(f"Total de pacientes: {len(pacientes)}")


# =========================
# BUSCAR PACIENTE
# =========================

def buscar_paciente():
    print("\n==== BUSCAR PACIENTE ====")

    termo = input("Digite o nome: ").strip()

    if not termo:
        print("Busca não pode ser vazia.")
        return

    conexao = sqlite3.connect("clinica.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome, idade, telefone
        FROM pacientes
        WHERE nome LIKE ?
    """, (f"%{termo}%",))

    resultados = cursor.fetchall()
    conexao.close()

    if resultados:
        print(f"\n{len(resultados)} paciente(s) encontrado(s):")
        print("-" * 50)
        print(f"{'Nome':<20} | {'Idade':<5} | {'Telefone':<20}")
        print("-" * 50)

        for nome, idade, telefone in resultados:
            print(f"{nome:<20} | {idade:<5} | {telefone:<20}")

        print("-" * 50)
    else:
        print("Paciente não encontrado.")


# =========================
# ESTATÍSTICAS
# =========================

def calcular_estatisticas():
    limpar_tela()
    print("\n==== ESTATÍSTICAS ====")

    conexao = sqlite3.connect("clinica.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM pacientes")
    total = cursor.fetchone()[0]

    if total == 0:
        print("Não há pacientes cadastrados.")
        conexao.close()
        return

    cursor.execute("SELECT AVG(idade) FROM pacientes")
    media = cursor.fetchone()[0]

    cursor.execute("""
        SELECT nome, idade FROM pacientes
        ORDER BY idade ASC LIMIT 1
    """)
    mais_novo = cursor.fetchone()

    cursor.execute("""
        SELECT nome, idade FROM pacientes
        ORDER BY idade DESC LIMIT 1
    """)
    mais_velho = cursor.fetchone()

    conexao.close()

    print(f"Total de pacientes: {total}")
    print(f"Idade média: {media:.2f} anos")
    print(f"Paciente mais novo: {mais_novo[0]} ({mais_novo[1]} anos)")
    print(f"Paciente mais velho: {mais_velho[0]} ({mais_velho[1]} anos)")


# =========================
# MENU
# =========================

def exibir_menu():
    print("\n=== SISTEMA CLÍNICA VIDA+ ===")
    print("=" * 30)
    print("1. Cadastrar paciente")
    print("2. Ver estatísticas")
    print("3. Buscar paciente")
    print("4. Listar pacientes")
    print("5. Sair")
    print("-" * 30)


# =========================
# MAIN
# =========================

def main():
    criar_banco()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            cadastrar_paciente()
            pausar()

        elif opcao == '2':
            calcular_estatisticas()
            pausar()

        elif opcao == '3':
            buscar_paciente()
            pausar()

        elif opcao == '4':
            listar_todos_pacientes()
            pausar()

        elif opcao == '5':
            print("\nSistema encerrado. Obrigado!")
            break

        else:
            print("Opção inválida.")
            pausar()


if __name__ == "__main__":
    main()
