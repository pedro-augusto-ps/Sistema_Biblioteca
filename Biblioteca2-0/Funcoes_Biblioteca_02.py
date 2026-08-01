from Classes_Biblioteca_02 import Biblioteca, Usuario, Livro, Revista
from Visual import *
from getpass import getpass
from rich import print
import sqlite3

conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
cursor = conexao.cursor()

# cursor.execute("DELETE FROM emprestimos")
# cursor.execute("DELETE FROM usuarios")
# cursor.execute("DELETE FROM item")
# cursor.execute("DELETE FROM sqlite_sequence")
# conexao.commit()
def escolha1_cadastrar_item(biblioteca_recebida):
    itens_disponiveis()   
    escolha = escolha_item()
    if escolha == 1:
        titulo = insira_titulo()
        if buscar_item_completo(titulo) == None:    #Se é "None" então não existe item com este nome
            autor = insira_autor()                  
            disponibilidade = True
            biblioteca_recebida.cadastrar_livro(titulo, autor, disponibilidade, "Livro") #Passa os dados, objeto ainda não foi criado
    elif escolha == 2:
        titulo = insira_nome_revista()
        if buscar_item_completo(titulo) == None:    #Se é "None" então não existe item com este nome
            autor = insira_autor()
            disponibilidade = True
            biblioteca_recebida.cadastrar_revista(titulo, autor, disponibilidade, "Revista") #Passa os dados, objeto ainda não foi criado
    else:
        invalido()
        return
    
def escolha2_cadastrar_usuario(biblioteca_recebida):
    nome = insira_usuario() 
    if buscar_usuario(nome) == None:  #Se é "None" então não existe usuário com este nome
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
        id_usuario, nome_usuario, senha_usuario, emprestimos_realizados = buscar_usuario_completo(usuario)
        cursor.execute("""SELECT titulo, autor, disponibilidade, tipo
        FROM item
        INNER JOIN emprestimos ON emprestimos.id_item = item.id_item
        WHERE emprestimos.id_usuario = ?""", (id_usuario,))
        itens_emprestados = cursor.fetchall()
        usuario = Usuario(nome_usuario, senha_usuario, tem_hash=True)
        insira_senha()        
        senha = getpass("")
        if usuario.verificar_senha(senha) == True:  #Verifica a senha do usuário
            exibir_informacoes(usuario, itens_emprestados)             #Exibe as informaçoes do usuário
        else:
            senha_invalida()
    except TypeError:
        usuario_nao_encontrado()        

def escolha4_exibir_acervo(bibilioteca_recebida):
    exibir_acervo_estilizado(bibilioteca_recebida)

#----------------------RETIRAR----------------------#
#FUNÇÕES DEVEM VALIDAR TUDO
def escolha5_retirar(biblioteca_recebida):
    # exibir_acervo_estilizado(biblioteca_recebida)
    usuario = insira_usuario()
    try:
        buscar_usuario(usuario) #Busca o nome do usuário no DB, como não pode ter nomes iguais na criação, não tem conflito
        id_usuario, nome_usuario, senha_usuario, emprestimos_realizados = buscar_usuario_completo(usuario) #Em ordem, pega as informações do usuário
        usuario = Usuario(nome_usuario, senha_usuario, tem_hash=True) #Cria o objeto usuario,
        insira_senha()
        senha = getpass("")
        if usuario.verificar_senha(senha) == True: #Senha correta, então continue
            try:
                item = insira_item()
                id_item, titulo, autor, disponibilidade, tipo = buscar_item_completo(item)
                if item_disponivel(id_item) == True:
                    if tipo == "Livro":  #Para não criar um objeto item, pensei em usar um IF para verificar o tipo antes de criar
                        item = Livro(titulo, autor, disponibilidade, tipo)  
                    else:
                        item = Revista(titulo, autor, disponibilidade, tipo)
                    biblioteca_recebida.retirar(usuario, item) #Passando OBJETOS
                else:
                    print("Item indisponivel")
            except AttributeError:
                item_nao_encontrado()
        else:
            senha_invalida()
    except:
        usuario_nao_encontrado()
#----------------------RETIRAR----------------------#

#----------------------DEVOLUÇÃO--------------------#
def escolha6_devolver(biblioteca_recebida):
    usuario = insira_usuario()
    try:
        buscar_usuario(usuario) #Busca o nome do usuário no DB, como não pode ter nomes iguais na criação, não tem conflito
        id_usuario, nome_usuario, senha_usuario, emprestimos_realizados = buscar_usuario_completo(usuario,) 
        usuario = Usuario(nome_usuario, senha_usuario, tem_hash=True) #Cria o objeto usuario,
        insira_senha()
        senha = getpass("")
        if usuario.verificar_senha(senha) == True:   #Senha correta, então continue
            item = insira_item()
            id_item, titulo, autor, disponibilidade, tipo = buscar_item_completo(item,)
            if item_disponivel(id_item) == False:
                if tipo == "Livro":  #Para não criar um objeto item, pensei em usar um IF para verificar o tipo antes de criar
                    item = Livro(titulo, autor, disponibilidade, tipo)  
                else:
                    item = Revista(titulo, autor, disponibilidade, tipo)
                biblioteca_recebida.devolver(usuario, item) #Passando OBJETOS 
            else:
                item_indisponivel()
        else:
            senha_invalida()
    except:
        usuario_nao_encontrado()
#----------------------DEVOLUÇÃO--------------------#

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
    try:
        cursor.execute("SELECT * FROM item WHERE titulo = ?", (item,))
        resultado = cursor.fetchone()
        return resultado
    except TypeError:
        return None

def item_disponivel(id_item):
    cursor.execute("""SELECT disponibilidade FROM item WHERE id_item = ?""", (id_item,))
    resultado = cursor.fetchone()[0]
    if resultado == 1: #0 = Não foi retirado
        return True
    else:
        return False
