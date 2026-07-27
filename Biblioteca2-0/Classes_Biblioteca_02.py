from abc import ABC, abstractmethod 
import hashlib
from rich import print
from getpass import getpass
from Visual import *
import sqlite3


class Item(ABC):
    """Clase ITEM, abstrata e serve para criação das SUBCLASSES livro e Revista
    Possuí um método abstrato para ser implantado em ambas.
    """
    def __init__(self, titulo, autor, disponibilidade): #Todo item deve ter: Titulo, Autor, e uma disponibilidade(Bool)
        self.titulo = titulo
        self.autor = autor
        self.disponibilidade = disponibilidade

    @abstractmethod         #Método abstrato para forçar a criaçao nas subclasses
    def calcular_multa(self, dias_de_atraso):
        pass

class Livro(Item): 
    """Livro SUBCLASSE de item, com essa classe criamos um item para nossa biblioteca"""
    def __init__(self, titulo, autor, disponibilidade):
        super().__init__(titulo, autor, disponibilidade)
        self.tipo = "Livro"

    def calcular_multa(self, dias_de_atraso):
        return dias_de_atraso * 1

    def __str__(self):
        if self.disponibilidade == True:
            status = "DISPONÍVEL"
        else:
            status = "INDISPONÍVEL"
        return f"LIVRO: {self.titulo} AUTOR: {self.autor} STATUS: {status}"
     
class Revista(Item):
    """Revista SUBCLASSE de item, com essa classe criamos um item para nossa biblioteca"""
    def __init__(self, titulo, autor, disponibilidade):
        super().__init__(titulo, autor, disponibilidade)
        self.tipo = "Revista"

    def calcular_multa(self, dias_de_atraso):
        return dias_de_atraso * 0.50
    
    def __str__(self):
        if self.disponibilidade == True:
            status = "DISPONÍVEL"
        else:
            status = "INDISPONÍVEL"
        return f"REVISTA: {self.titulo} AUTOR: {self.autor} STATUS: {status}"
     

class Emprestimo:
    """Nesta CLASSE, os atributos: (usuario) e (item) seram CLASSES!
    (usuario)será utilizado para verificar a quantia de emprestimos que esse usuario já tem
    (item)é usado para ver se o item está True, ou False"""
    def __init__(self, usuario, item, data_do_emprestimo, ativo):
        self.usuario = usuario  #O usuario fornecido será o usuario PASSADO no MÉTODO RETIRAR da CLASSE BIBLIOTECA
        self.item = item        #O Item fornecido será um OBJETO, um livro ou uma revista
        self.data_do_emprestimo = data_do_emprestimo
        self.ativo = ativo

    def finalizar(self):
        """Quando um item precisa ser devolvido, o empréstimo é finalizado por meio
        deste método"""
        
        self.item.disponibilidade = True  #O item volta a estar disponível.      
        self.usuario._emprestimos_realizados -= 1  #O Usuario obtem -1 empréstimo.
        self.ativo = False  #Empréstimo não está mais ativo

    def __str__(self):
        return f"{self.item}"
    
class Usuario:
    """Usuário que irá utilizar do sistema
    ATRIBUTOS: nome(#), senha_usuario(-), emprestimos_realizados(#), itens_emprestados(#)
    MÉTODOS: verificar_senha -> Valida a veracidade da senha e posteriormente permite
    a retirada, exibição de informações, e devolução dos itens.
    NOTA: A senha automaticamente vira um HASH SHA256 para contribuir com a segurança."""
    def __init__(self, nome, senha_usuario, emprestimos=0):
        self._nome = nome
        self.__senha_usuario = hashlib.sha256(senha_usuario.encode('utf-8')).hexdigest()  #Senha trasnformada em HASH de cara
        self._emprestimos_realizados = emprestimos
        self._itens_emprestados = []
        

    def verificar_senha(self, senha_fornecida):
        return senha_fornecida == self.__senha_usuario

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        if novo_nome == self._nome:
           raise ValueError("O novo nome não pode ser igual o antigo")
        else:
            self._nome = novo_nome

    @property
    def checagem_senha(self):
        return self.__senha_usuario

    @checagem_senha.setter
    def checagem_senha(self, nova_senha):
        insira_senha()              #Função ESTILIZADA
        senha = str(input(""))
        if hashlib.sha256(senha.encode('utf-8')).hexdigest() != self.__senha_usuario:
            return senha_invalida()
        else:
            insira_senha()
            nova_senha = getpass("")
            self.__senha_usuario = hashlib.sha256(nova_senha.encode('utf-8')).hexdigest()
         
class Biblioteca:
    """Nesta classe é gerenciado grande parte do sistema, abaixo
    explicação dos atributos e suas funcionalidades:
    ATRIBUTOS: usuarios -> esse atributo armazena todo OBJETO usuário em 
    um dicionário, onde nome é a chave(KEY).
    item -> Aqui é armazenado todo livro/revista e seus respectivos 
    atributos, o método cadastrar_livro e cadastrar_revista armazenam aqui
    emprestimos_lista -> Quando um usuário retira um livro por meio do método
    retirar, é criado um OBJETO empréstimo, e eles ficam armazenados nesta lista"""
    def __init__(self):
        self.usuarios = {}
        self.itens = []
        self.emprestimos_lista = []

    def retirar(self, usuario, item): 
        conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
        cursor = conexao.cursor()
        try:
            insira_senha()         
            senha = getpass("")    
            if usuario.verificar_senha(senha) == True:        #VALIDAÇÃO: Senha correta?
                if item.disponibilidade == True:              #VALIDAÇÃO: Item disponivél?
                    if usuario._emprestimos_realizados < 3:   #VALIDAÇÃO: Usuário tem -3 empréstimos?
                        cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (usuario.nome,))
                        id_usuario = cursor.fetchone()[0]
                        cursor.execute("SELECT id FROM itens WHERE titulo = ?", (item.titulo,))
                        id_item = cursor.fetchone()[0]
                        #INÍCIO DA RETIRADA
                        item.disponibilidade = False          #Item não está mais disponível.
                        usuario._emprestimos_realizados += 1  #Soma um emprestimo no usuário
                        cursor.execute("""INSERT INTO emprestimos
                        (usuario_ID, itens_ID) VALUES
                        (?, ?)""", (id_usuario, id_item,))
                        conexao.commit()
                    else:
                        emprestimo_excedente()
                else:
                    item_indisponivel()    
            else:
                senha_invalida()
        except ValueError:
            usuario_nao_encontrado()

    def devolver(self, usuario, item):
        if usuario.nome in self.usuarios['nome']:   #Usuário está na lista de usuários da biblioteca?
            insira_senha()          
            senha = getpass("")
            if usuario.verificar_senha(senha) == False:
                senha_invalida()    
            else:
                emprestimo_encontrado = None   #Variável de apoio
                for emprestimo in usuario._itens_emprestados: #Para cada emprestimo, na lista de empréstimos do usuário
                    if emprestimo.item.titulo == item:  #Se o titúlo de um empréstimo condiz com meu item
                        emprestimo_encontrado = emprestimo 
                if emprestimo_encontrado != None:
                    self.emprestimos_lista.remove(emprestimo_encontrado)        #Removo este empréstimo da biblioteca
                    usuario._itens_emprestados.remove(emprestimo_encontrado)    #Removo este empréstimo do usuário
                    emprestimo_encontrado.finalizar()                           #Finalizo o empréstimo,item volta a ser TRUE...
                else:
                    emprestimo_nao_encontrado()          
            
    def cadastrar_livro(self, titulo, autor, disponibilidade):
        novo_item = Livro(titulo, autor, disponibilidade)
        if novo_item in self.itens:
            item_cadastrado()
        else:   
            conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
            cursor = conexao.cursor()
            cursor.execute("""INSERT INTO itens 
            (titulo, autor, disponibilidade) VALUES
            (?, ?, ?)""",
            (novo_item.titulo, novo_item.autor, novo_item.disponibilidade))
            self.itens.append(novo_item)
            conexao.commit()

    def cadastrar_revista(self, titulo, autor, disponibilidade):
        novo_item = Revista(titulo, autor, disponibilidade)
        if novo_item in self.itens:
            item_cadastrado()
        else:
            conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
            cursor = conexao.cursor()
            self.itens.append(novo_item)
            cursor.execute("""INSERT INTO itens 
            (titulo, autor, disponibilidade) VALUES
            (?, ?, ?)""",
            (novo_item.titulo, novo_item.autor, novo_item.disponibilidade))
            conexao.commit()

    def cadastrar_usuario(self, novo_usuario):
        conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
        cursor = conexao.cursor()
        cursor.execute("""INSERT INTO usuarios
        (nome, senha)VALUES
        (?, ?)""",
        (novo_usuario.nome, novo_usuario.checagem_senha))
        conexao.commit()
        self.usuarios[novo_usuario.nome] = novo_usuario


def buscar_usuario_completo(nome):
    cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    return resultado

def buscar_item_completo(item):
    cursor.execute("SELECT * FROM itens WHERE titulo = ?", (item,))
    resultado = cursor.fetchone()
    return resultado