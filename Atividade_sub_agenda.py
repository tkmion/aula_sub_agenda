import os
import json
from datetime import datetime, timedelta

class Contato:
    def __init__(self, nome, telefone, endereco, aniversario, email):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.aniversario = datetime.strptime(aniversario, "%d/%m/%Y")
        self.email = email

    def idade(self):
        hoje = datetime.today()
        idade = hoje.year - self.aniversario.year - ((hoje.month, hoje.day) < (self.aniversario.month, self.aniversario.day))
        return idade

    def dias_para_aniversario(self):
        hoje = datetime.today()
        proximo_aniversario = self.aniversario.replace(year=hoje.year)
        if proximo_aniversario < hoje:
            proximo_aniversario = proximo_aniversario.replace(year=hoje.year + 1)
        dias = (proximo_aniversario - hoje).days
        return dias

    def to_dict(self):
        return {
            "nome": self.nome,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "aniversario": self.aniversario.strftime("%d/%m/%Y"),
            "email": self.email
        }

class Arquivo:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.dados = []
        self.carregar()

    def salvar(self):
        with open(self.nome_arquivo, 'w') as f:
            json.dump([contato.to_dict() for contato in self.dados], f, ensure_ascii=False, indent=4)

    def carregar(self):
        try:
            with open(self.nome_arquivo, 'r') as f:
                contatos_json = json.load(f)
                self.dados = [Contato(**contato) for contato in contatos_json]
        except FileNotFoundError:
            self.dados = []

class Agenda:
    def __init__(self):
        self.arquivo = Arquivo('contatos.json')
        self.contatos = self.arquivo.dados
        self.limpar_tela()
        self.mostrar_aniversariantes()

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_aniversariantes(self):
        hoje = datetime.today().strftime("%d/%m")
        aniversariantes = [c.nome for c in self.contatos if c.aniversario.strftime("%d/%m") == hoje]
        if aniversariantes:
            print("Aniversariantes de hoje:")
            for nome in aniversariantes:
                print(f"- {nome}")
        else:
            print("Nenhum aniversariante hoje.")

    def adicionar_contato(self):
        try:
            nome = input("Nome completo: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            aniversario = input("Data de aniversário (dd/mm/yyyy): ")
            email = input("Email: ")
            novo_contato = Contato(nome, telefone, endereco, aniversario, email)
            self.contatos.append(novo_contato)
            self.arquivo.dados = self.contatos
            self.arquivo.salvar()
            print("Contato adicionado com sucesso!")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def editar_contato(self):
        nome = input("Digite o nome do contato que deseja editar: ")
        contato = self.buscar_contato(nome)
        if contato:
            try:
                contato.nome = input(f"Nome completo [{contato.nome}]: ") or contato.nome
                contato.telefone = input(f"Telefone [{contato.telefone}]: ") or contato.telefone
                contato.endereco = input(f"Endereço [{contato.endereco}]: ") or contato.endereco
                aniversario = input(f"Data de aniversário [{contato.aniversario.strftime('%d/%m/%Y')}]: ")
                if aniversario:
                    contato.aniversario = datetime.strptime(aniversario, "%d/%m/%Y")
                contato.email = input(f"Email [{contato.email}]: ") or contato.email
                self.arquivo.salvar()
                print("Contato editado com sucesso!")
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
        else:
            print("Contato não encontrado.")

    def apagar_contato(self):
        nome = input("Digite o nome do contato que deseja apagar: ")
        contato = self.buscar_contato(nome)
        if contato:
            self.contatos.remove(contato)
            self.arquivo.dados = self.contatos
            self.arquivo.salvar()
            print("Contato apagado com sucesso!")
        else:
            print("Contato não encontrado.")

    def listar_contatos(self):
        if self.contatos:
            for contato in self.contatos:
                print(f"Nome: {contato.nome}")
                print(f"Telefone: {contato.telefone}")
                print(f"Endereço: {contato.endereco}")
                print(f"Aniversário: {contato.aniversario.strftime('%d/%m/%Y')}")
                print(f"Email: {contato.email}")
                print(f"Idade: {contato.idade()} anos")
                print(f"Dias até o próximo aniversário: {contato.dias_para_aniversario()} dias")
                print("-" * 30)
        else:
            print("Nenhum contato na agenda.")

    def buscar_contatos_semelhantes(self):
        termo = input("Digite o nome a ser buscado: ").lower()
        resultados = [c for c in self.contatos if termo in c.nome.lower()]
        if resultados:
            for contato in resultados:
                print(f"Nome: {contato.nome}")
                print(f"Telefone: {contato.telefone}")
                print(f"Endereço: {contato.endereco}")
                print(f"Aniversário: {contato.aniversario.strftime('%d/%m/%Y')}")
                print(f"Email: {contato.email}")
                print(f"Idade: {contato.idade()} anos")
                print(f"Dias até o próximo aniversário: {contato.dias_para_aniversario()} dias")
                print("-" * 30)
        else:
            print("Nenhum contato encontrado.")

    def buscar_contato(self, nome):
        for contato in self.contatos:
            if contato.nome.lower() == nome.lower():
                return contato
        return None

    def menu(self):
        while True:
            print("\nAgenda Eletrônica")
            print("1. Adicionar contato")
            print("2. Editar contato")
            print("3. Apagar contato")
            print("4. Listar todos os contatos")
            print("5. Buscar contatos por nome")
            print("6. Sair")
            opcao = input("Escolha uma opção: ")
            self.limpar_tela()
            if opcao == '1':
                self.adicionar_contato()
            elif opcao == '2':
                self.editar_contato()
            elif opcao == '3':
                self.apagar_contato()
            elif opcao == '4':
                self.listar_contatos()
            elif opcao == '5':
                self.buscar_contatos_semelhantes()
            elif opcao == '6':
                print("Saindo da agenda...")
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    agenda = Agenda()
    agenda.menu()
