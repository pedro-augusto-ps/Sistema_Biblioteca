from Classes_Biblioteca_02 import Biblioteca, Usuario
from Visual import *
from getpass import getpass
from rich import print
import sqlite3

conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
cursor = conexao.cursor()

def escolha1_cadastrar_item(biblioteca_recebida):
    itens_disponiveis()     #Exibe os ITENS disponíveis
    escolha = escolha_item()
    if escolha == 1:
        titulo = insira_titulo()
        autor = insira_autor()
        disponibilidade = True
        biblioteca_recebida.cadastrar_livro(titulo, autor, disponibilidade) #Cria um livro
    elif escolha == 2:
        titulo = insira_nome_revista()
        autor = insira_autor()
        disponibilidade = True
        biblioteca_recebida.cadastrar_revista(titulo, autor, disponibilidade) #Cria uma revista
    else:
        invalido()

def escolha2_cadastrar_usuario(biblioteca_recebida):
    nome = insira_usuario() 
    if nome in buscar_usuario(nome):
        usuario_cadastrado()
        return
    insira_senha() 
    senha = getpass("")
    usuario = Usuario(nome, senha, False)  #Cria um usuário
    biblioteca_recebida.cadastrar_usuario(usuario)  #Cadastra ele na biblioteca

def escolha3_exibir_informações(biblioteca_recebida):
    procurado = insira_usuario()
    usuario = biblioteca_recebida.usuarios.get(procurado)   #Acha o usuário na lista da biblioteca
    try:
        if procurado == usuario.nome:
           insira_senha()        
        senha = getpass("")
        if usuario.verificar_senha(senha) == True:  #Verifica a senha do usuário
            exibir_informacoes(usuario)     #Exibe as informaçoes do usuário
        else:
            senha_invalida()
    except:
            usuario_nao_encontrado()


def escolha4_exibir_acervo(bibilioteca_recebida):
    exibir_acervo_estilizado(bibilioteca_recebida)

def escolha5_retirar(biblioteca_recebida):
    exibir_acervo_estilizado(biblioteca_recebida)
    usuario = insira_usuario()
    try:
        if usuario in biblioteca_recebida.usuarios.keys():  #Confirma se o usuário(STR) está na lista da biblioteca
            item = insira_item()
            biblioteca_recebida.retirar(usuario, item)
        else:
            usuario_nao_encontrado()
    except AttributeError:
        item_nao_encontrado()


def escolha6_devolver(biblioteca_recebida):
    usuario = insira_usuario()
    try:
        if usuario in biblioteca_recebida.usuarios.keys():  #Confirma se o usuário(STR) está na lista da biblioteca
            usuario_objeto = biblioteca_recebida.usuarios.get(usuario)  #Vira objeot
            print(f"ITENS RETIRADOS: ")
            for item in usuario_objeto._itens_emprestados:
                print(item)
            item = insira_item()
            biblioteca_recebida.devolver(usuario, item)
    except:
        usuario_nao_encontrado() 


def buscar_usuario(nome):
    try:
        cursor.execute("SELECT nome FROM usuarios WHERE nome = ?", (nome,)) #Executa a busca do nome. vírgula por obrigação do SQLITE
        resultado = cursor.fetchone()[0] #[0] Pois vai retornar STR da tupla encontrada
        return resultado
    except TypeError:
        return None