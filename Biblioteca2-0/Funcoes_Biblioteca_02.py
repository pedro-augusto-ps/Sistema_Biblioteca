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
    if buscar_usuario(nome) == None:
        insira_senha() 
        senha = getpass("")
        usuario = Usuario(nome, senha)  #Cria um usuário
        biblioteca_recebida.cadastrar_usuario(usuario)  #Cadastra ele na biblioteca
    else:
        usuario_cadastrado()
        return
    
def escolha3_exibir_informações(biblioteca_recebida):
    usuario = insira_usuario()
    try:
        id_usuario, nome_usuario, senha_usuario = buscar_usuario_completo(usuario)
        usuario = Usuario(nome_usuario, senha_usuario)
        insira_senha()        
        senha = getpass("")
        if usuario.verificar_senha(senha) == True:  #Verifica a senha do usuário
            exibir_informacoes(usuario)#Exibe as informaçoes do usuário
        else:
            senha_invalida()
    except TypeError:
        usuario_nao_encontrado()        

def escolha4_exibir_acervo(bibilioteca_recebida):
    exibir_acervo_estilizado(bibilioteca_recebida)

#----------------------RETIRAR----------------------#
def escolha5_retirar(biblioteca_recebida):
    exibir_acervo_estilizado(biblioteca_recebida)
    usuario = insira_usuario()
    try:
        buscar_usuario(usuario) #Busca o nome do usuario
        id_usuario, nome_usuario, senha_usuario = buscar_usuario_completo(usuario)
        usuario = Usuario(nome_usuario, senha_usuario)
        try:
            item = insira_item()
            biblioteca_recebida.retirar(usuario, item)
        except AttributeError:
            item_nao_encontrado()
    except:
        usuario_nao_encontrado()
#----------------------RETIRAR----------------------#


def escolha6_devolver(biblioteca_recebida):
    usuario = insira_usuario()
    try:
        buscar_usuario(usuario) #Busca o nome do usuario
        id_usuario, nome_usuario, senha_usuario = buscar_usuario_completo(usuario)
        usuario = Usuario(nome_usuario, senha_usuario) #TRANSFORMANDO EM OBJETO, DESFRAGMENTAÇÃO SEM ORM
        print(f"ITENS RETIRADOS: ")                 #LISTAGEM DOS ITENS
        for item in nome_usuario._itens_emprestados:#LISTAGEM DOS ITENS
            print(item)                             #LISTAGEM DOS ITENS
        try:
            item = insira_item()
            biblioteca_recebida.devolver(usuario, item)
        except ValueError:
            item_nao_encontrado()
    except ValueError:
        usuario_nao_encontrado() 



def buscar_usuario(nome):
    try:
        cursor.execute("SELECT nome FROM usuarios WHERE nome = ?", (nome,)) #Executa a busca do nome. vírgula por obrigação do SQLITE
        resultado = cursor.fetchone()[0] #[0] Pois vai retornar STR da tupla encontrada
        return resultado
    except TypeError:
        return None

def buscar_usuario_completo(nome):
    cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    return resultado

def buscar_item_completo(item):
    cursor.execute("SELECT * FROM itens WHERE titulo = ?", (item,))
    resultado = cursor.fetchone()
    return resultado