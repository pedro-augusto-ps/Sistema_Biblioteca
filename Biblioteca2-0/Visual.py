from rich import print
from rich.table import Table
from rich.panel import Panel  
import sqlite3

def menu_principal():
    texto = ("[bold white][1][/] Cadastrar [bold #F9DC5C]ITEM[/]\n"
    "[bold white][2][/] Cadastrar [#3185FC bold]USUÁRIO[/]\n"
    "[bold white][3][/] Exibir [#3185FC bold]INFORMAÇÕES USUÁRIO[/]\n"
    "[bold white][4][/] Exibir [#E6E1C5]ACERVO[/]\n"
    "[bold white][5][/] [#283618]RETIRAR[/]\n"
    "[bold white][6][/] [#283618]DEVOLVER[/]"
    )
    menu = Panel(texto, title="[bold green]MENU[/]")
    print(menu)

def exibir_acervo_estilizado(biblioteca_recebida):
    conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT titulo, autor, disponibilidade, tipo FROM item")
    resultado = cursor.fetchall()
    tabela = Table(title="[white]ACERVO[/]")
    tabela.add_column("ITEM")
    tabela.add_column("AUTOR")
    tabela.add_column("DISPONIBILIDADE")
    tabela.add_column("TIPO")
    for informacao in resultado:
        titulo, autor, disponibilidade, tipo = informacao
        titulo = f"[white bold]{titulo}[/]"
        autor = f"[white bold]{autor}[/]"
        tipo = f"[white bold]{tipo}[/]"
        status = "[green]DISPONÍVEL[/]" if disponibilidade ==1 else "[red]INDISPONÍVEL[/]"
        tabela.add_row(titulo, autor, status, tipo)

    print(tabela)
    conexao.close()


def itens_disponiveis():
    print(f"[#F9DC5C bold]ITENS[/] disponíveis: ")
    print(f"[white bold][1] LIVRO[/]")
    print(f"[white bold][2] REVISTA[/]")

def insira_titulo():
    print(f"[green]Insira o [/][#F9DC5C bold]TÍTULO[/]: ")
    titulo = input("")
    return titulo

def insira_autor():
    print(f"[green]Insira o [/][#F9DC5C bold]AUTOR[/]: ")
    autor = input("")
    return autor


#SENHAS
def senha_invalida():
    print(f"[#FF0000]Senha [bold]INVÁLIDA[/]")

def insira_senha():
    print(f"[#F3A712]Insira a [bold]SENHA:[/]")
#SENHAS

#CADASTRO DE ITENS/QUAL ITEM FORNECER
def insira_item():
    print(f"[white]Insira o [/][#F9DC5C bold]ITEM[/]: ")
    item = input("")
    return item

def insira_nome_revista():
    print(f"[green]Insira o [/][#F9DC5C bold]NOME DA REVISTA[/]: ")
    nome = input("")
    return nome

def escolha_item():
    print(f"[white]Escolha o [/][#F9DC5C bold]ITEM[/]: ")
    item = int(input(""))
    return item

#CADASTRO DE ITENS/QUAL ITEM FORNECER


def invalido():
    print(f"[#FF0000]OPÇÃO [bold]INVÁLIDA[/]")


#USUÁRIO
def insira_usuario():
    print(f"[white]Insira o[/] [#2EC4B6 bold]NOME do USUÁRIO:[/] ")
    usuario = str(input(""))
    return usuario

def usuario_nao_encontrado():
    print(f"[#2EC4B6 bold]USUÁRIO[/] [#2EC4B6]não encontrado[/]")

def usuario_cadastrado():
    print(f"[#2EC4B6 bold]USUÁRIO[/] [#2EC4B6]já cadastrado[/]")

def exibir_informacoes(usuario):
    print(f"EXIBINDO INFORMAÇÕES DE(A):")
    print(f"[#2EC4B6 bold]NOME: {usuario.nome}[/]")
    print(f"[#2EC4B6 bold]EMPRÉSTIMOS ATUAIS: {usuario._emprestimos_realizados}[/]")
    tabela = Table(title="[white]ITENS RETIRADOS[/]")
    tabela.add_column("ITEM")
    tabela.add_column("AUTOR")
    tabela.add_column("DISPONIBILIDADE")
    for item in usuario._itens_emprestados:
        if item.item.disponibilidade == True:
            status = "[green bold]DISPONÍVEL[/]"
        else:
            status = "[red bold]INDISPONÍVEL[/]"
        tabela.add_row(item.item.titulo, item.item.autor, status) #item. -> emprestimo, item.item -> nome do item
    print(tabela)
#USUÁRIO

#EMPRESTIMO

def emprestimo_excedente():
    print(f"[#FF0000 bold]Limite de EMPRÉSTIMOS[/] [#FF0000]atingido[/]")

def emprestimo_nao_encontrado():
    print(f"[#FF0000 bold]EMPRÉSTIMO[/] [#FF0000]não encontrado[/]")
#EMPRESTIMO

def item_cadastrado():
    print(f"[#F9DC5C bold]ITEM[/] já cadastrado")

def item_indisponivel():
    print(f"[#F9DC5C bold]ITEM[/] [#FF0000]indisponível[/]")

def item_nao_encontrado():
    print(f"[#2EC4B6 bold]ITEM[/] [#2EC4B6]não encontrado[/]")