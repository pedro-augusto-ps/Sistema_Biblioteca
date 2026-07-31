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
    def __init__(self, titulo, autor, disponibilidade, tipo): #Todo item deve ter: Titulo, Autor, e uma disponibilidade(Bool)
        self.titulo = titulo
        self.autor = autor
        self.disponibilidade = disponibilidade
        self.tipo = tipo

    @abstractmethod         #Método abstrato para forçar a criaçao nas subclasses
    def calcular_multa(self, dias_de_atraso):
        pass

class Livro(Item): 
    """Livro SUBCLASSE de item, com essa classe criamos um item para nossa biblioteca"""
    def __init__(self, titulo, autor, disponibilidade, tipo):
        super().__init__(titulo, autor, disponibilidade, tipo)

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
    def __init__(self, titulo, autor, disponibilidade, tipo):
        super().__init__(titulo, autor, disponibilidade, tipo)

    def calcular_multa(self, dias_de_atraso):
        return dias_de_atraso * 0.50
    
    def __str__(self):
        if self.disponibilidade == True:
            status = "DISPONÍVEL"
        else:
            status = "INDISPONÍVEL"
        return f"REVISTA: {self.titulo} AUTOR: {self.autor} STATUS: {status}"
     
class Usuario:
    """Usuário que irá utilizar do sistema
    ATRIBUTOS: nome(#), senha_usuario(-), emprestimos_realizados(#), itens_emprestados(#)
    MÉTODOS: verificar_senha -> Valida a veracidade da senha e posteriormente permite
    a retirada, exibição de informações, e devolução dos itens.
    NOTA: A senha automaticamente vira um HASH SHA256 para contribuir com a segurança."""
    def __init__(self, nome, senha_usuario):
        self._nome = nome
        self.__senha_usuario = hashlib.sha256(senha_usuario.encode('utf-8')).hexdigest()  #Senha trasnformada em HASH de cara
        self._emprestimos = 0
        
    def verificar_senha(self, senha_fornecida):
        senha_fornecida = hashlib.sha256(senha_fornecida.encode('utf-8')).hexdigest()
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
    """"Esta classe possui apenas os métodos, antigamente na forma de JSON ela possuía atributos também,
    É possível vizualizar as versões anteriores no commit final do meu GITHUB;
    O método retirar e devolver, recebem OBJETOS: (usuario e item)
    Cadastrar Livro e revista, recebem DADOS, o objeto é criado dentro do método
    Essa é a classe "Principal" do código, pois grande parte das alterações
    acontece aqui."""

#----------------------RETIRAR----------------------#
    def retirar(self, usuario, item): 
        conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (usuario.nome,)) #Pega o ID do usuário
        id_usuario = cursor.fetchone()[0]                                         #Pega o ID do usuário
        cursor.execute("SELECT id FROM itens WHERE titulo = ?", (item.titulo,))   #Pega o id do item
        id_item = cursor.fetchone()[0]                                            #Pega o id do item
        cursor.execute("""INSERT INTO emprestimos 
        (id_usuario, id_item) VALUES
        (?, ?)""", (id_usuario, id_item,))  #Cria um empréstimo
        cursor.execute("""UPDATE item
        SET disponibilidade = 0     
        WHERE id = ?""", (id_item,))
        cursor.execute("""UPDATE TABLE usuarios
        SET emprestimos_realizados + 1 
        WHERE id = ?""", (id_usuario,)) 
        conexao.commit()    #Muda a disponibilidade do item no DB
        conexao.close()
        #INÍCIO DA RETIRADA

#----------------------RETIRAR----------------------#

#----------------------DEVOLUÇÃO--------------------#
    def devolver(self, usuario, item):
        conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (usuario.nome,))  #Pega o ID do usuário
        id_usuario = cursor.fetchone()[0]                                          #Pega o ID do usuário
        cursor.execute("SELECT id FROM itens WHERE titulo = ?", (item.titulo,))    #Pega o id do item
        id_item = cursor.fetchone()[0]                                             #Pega o id do item
        cursor.execute("""DELETE FROM emprestimos                                  
        WHERE (id_usuario,id_item) IN ((?, ?))""", (id_usuario, id_item))
         #Deleta a ROW do empréstimo
        cursor.execute("""UPDATE item
        SET disponibilidade = 1
        WHERE id = ?""", (id_item)) #Muda a disponibilidade do item no DB
        cursor.execute("""UPDATE TABLE usuarios
        SET emprestimos_realizados - 1 
        WHERE id = ?""", (id_usuario)) 
        conexao.commit()   
        conexao.close()

#----------------------DEVOLUÇÃO--------------------#

    def cadastrar_livro(self, titulo, autor, disponibilidade, tipo):
        novo_item = Livro(titulo, autor, disponibilidade, tipo)  
        conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
        cursor = conexao.cursor()
        cursor.execute("""INSERT INTO item 
        (titulo, autor, disponibilidade, tipo) VALUES
        (?, ?, ?, ?)""",
        (novo_item.titulo, novo_item.autor, novo_item.disponibilidade, novo_item.tipo))
        conexao.commit()
        conexao.close()

    def cadastrar_revista(self, titulo, autor, disponibilidade, tipo):
        novo_item = Revista(titulo, autor, disponibilidade, tipo)
        conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
        cursor = conexao.cursor()
        cursor.execute("""INSERT INTO item 
        (titulo, autor, disponibilidade, tipo) VALUES
        (?, ?, ?, ?)""",
        (novo_item.titulo, novo_item.autor, novo_item.disponibilidade, novo_item.tipo))
        conexao.commit()
        conexao.close()
        
    def cadastrar_usuario(self, novo_usuario):
        conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
        cursor = conexao.cursor()
        cursor.execute("""INSERT INTO usuarios
        (nome, senha)VALUES
        (?, ?)""",
        (novo_usuario.nome, novo_usuario.checagem_senha))
        conexao.commit()
        conexao.close()

