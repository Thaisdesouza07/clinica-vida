import os
import sqlite3

pacientes = []
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

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_paciente():
    print("\n==== CADASTRO DE PACIENTE ====")

    nome = input("Nome do Paciente: ").strip().title()
    if not nome:
        print("Erro: O nome não pode ser vazio.")
        return

    while True:
        try:
            idade_str = input("Idade do Paciente: ").strip()
            idade = int(idade_str)
            if idade <= 0:
                print("Idade inválida.")
                continue
            break
        except ValueError:
            print("Idade deve ser um número inteiro. Tente novamente.")

    telefone = input("Telefone do Paciente (Ex: (11) 99999-9999): ").strip()

    novo_paciente = {
        'nome': nome,
        'idade': idade,
        'telefone': telefone
    }

    def cadastrar_paciente():
        print("\n==== CADASTRO DE PACIENTE ====")

        nome = input("Nome do Paciente: ").strip().title()

        while True:
            try:
                idade = int(input("Idade do Paciente: "))
                break
            except:
                print("Idade inválida")

        telefone = input("Telefone: ")

        conexao = sqlite3.connect("clinica.db")
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO pacientes (nome, idade, telefone)
            VALUES (?, ?, ?)
        """, (nome, idade, telefone))

        conexao.commit()
        conexao.close()

        print("Paciente cadastrado com sucesso!")

    print(f"\n✅ Paciente: '{nome}' cadastrado com sucesso!")


def calcular_estatisticas():
    limpar_tela()
    print("\n==== ESTATÍSTICAS ====")

    num_pacientes = len(pacientes)
    print(f"1. Número de pacientes cadastrados: {num_pacientes}")

    if num_pacientes == 0:
        print("Não há pacientes cadastrados.")
        return

    idades = [p['idade'] for p in pacientes]

    idade_media = sum(idades) / num_pacientes
    print(f"2. Idade média: {idade_media:.2f} anos")

    paciente_mais_novo = min(pacientes, key=lambda p: p['idade'])
    paciente_mais_velho = max(pacientes, key=lambda p: p['idade'])

    print(f"3. Paciente mais novo: {paciente_mais_novo['nome']} ({paciente_mais_novo['idade']} anos)")
    print(f"4. Paciente mais velho: {paciente_mais_velho['nome']} ({paciente_mais_velho['idade']} anos)")


def buscar_paciente():
    print("\n==== BUSCAR PACIENTE ====")
    termo_busca = input("Digite o nome do paciente: ").strip().title()

    if not termo_busca:
        print("ERRO: Busca não pode ser vazia.")
        return

    resultados = [
        p for p in pacientes if termo_busca in p['nome']
    ]

    if resultados:
        print(f"\n {len(resultados)} paciente(s) encontrado(s) para '{termo_busca}':")
        print("-" * 50)
        print(f"{'Nome':<20} | {'Idade':<5} | {'Telefone':<20}")
        print("-" * 50)
        for p in resultados:
            print(f"{p['nome']:<20} | {p['idade']:<5} | {p['telefone']:<20}")
        print("-" * 50)
    else:
        print(f"\n Paciente '{termo_busca}' não cadastrado ")


def listar_todos_pacientes():
    limpar_tela()
    print("\n=== LISTA De PACIENTES CADASTRADOS ===")

    if not pacientes:
        print("Nenhum paciente cadastrado ")
        return

    print("-" * 30)
    print(f"{'Nome':<20} | {'Idade':<5} | {'Telefone':<20}")
    print("-" * 30)

    for p in pacientes:
        print(f"{p['nome']:<20} | {p['idade']:<5} | {p['telefone']:<20}")

    print("-" * 50)
    print(f"Numero Total de pacientes: {len(pacientes)}")


def exibir_menu():
    print("\n" + "=" * 28)


print("=== SISTEMA CLÍNICA VIDA+ ===")
print("=" * 30)
print("1. Cadastrar paciente")
print("2. Ver estatísticas")
print("3. Buscar paciente")
print("4. Listar todos os pacientes")
print("5. Sair")
print("-" * 30)


def main():
     criar_banco()

    while True:
        exibir_menu()

        try:
            opcao = input("Escolha uma Opção: ").strip()

            if opcao == '1':
                cadastrar_paciente()
            elif opcao == '2':
                calcular_estatisticas()
            elif opcao == '3':
                buscar_paciente()
            elif opcao == '4':
                listar_todos_pacientes()
            elif opcao == '5':
                print("\n Sistema Clínica Vida+ Encerrado. Obrigado!")
                break
            else:
                print("\n Opção inválida. Por favor, escolha uma Opção  de 1 a 5.")

        except Exception as erro:
            print(f"Erro inesperado: {erro}")

    if opcao != '5':
            input("\nPressione ENTER ")
            limpar_tela()


if __name__ == "__main__":
    main()