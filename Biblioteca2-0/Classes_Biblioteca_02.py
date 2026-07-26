from abc import ABC, abstractmethod 
import hashlib
from rich import print,inspect
from getpass import getpass
from Visual import *
import json
import os
import sqlite3



PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))        #Configura para ser DEFINITIVO
CAMINHO_ITENS = os.path.join(PASTA_ATUAL, "itens.json")         #Configura para ser DEFINITIVO
CAMINHO_USUARIOS = os.path.join(PASTA_ATUAL, "usuarios.json")   #Configura para ser DEFINITIVO

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
    def __init__(self, nome, senha_usuario, tem_hash, emprestimos=0):
        self._nome = nome
        self._emprestimos_realizados = emprestimos
        self._itens_emprestados = []

        if tem_hash == True:
            self.__senha_usuario = senha_usuario
        else:
            self.__senha_usuario = hashlib.sha256(senha_usuario.encode('utf-8')).hexdigest()  #Senha trasnformada em HASH de cara

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

    #Esses parâmetros recebem STR, aqui se forem validados tornam-se OBJETOS
    def retirar(self, usuario, item): 
        if usuario in self.usuarios:   #Usuário esta na lista da biblioteca de usuários?
            usuario = self.usuarios.get(usuario) 
            #IMPORTANTE! (usuario) é passado como uma string, usar o método get vai
            #puxar o OBJETO usuario, então (usuario)tornou-se um objeto.

            for item_obj in self.itens:         #Passa cada item na lista de item da biblioteca.
                if item == item_obj.titulo:     #Se o item fornecido existe no item.titulo
                    item = item_obj             #item fornecido vira aquele objeto armazenado
                    break

            insira_senha()         #Função ESTILIZADA
            senha = getpass("")    #GETPASS para omitir a senha

            if usuario.verificar_senha(senha) == True:        #VALIDAÇÃO: Senha correta?
                if item.disponibilidade == True:              #VALIDAÇÃO: Item disponivél?
                    if usuario._emprestimos_realizados < 3:   #VALIDAÇÃO: Usuário tem -3 empréstimos?
                        #INÍCIO DA RETIRADA
                        item.disponibilidade = False          #Item não está mais disponível.
                        usuario._emprestimos_realizados += 1  #Soma um emprestimo no usuário
                        novo_emprestimo = Emprestimo(usuario, item, "11 de Julho", True)  #Cria um Emprestimo, para o "objeto"usuario 
                        self.emprestimos_lista.append(novo_emprestimo)  #Adiciona esse empréstimo na lista da biblioteca
                        usuario._itens_emprestados.append(novo_emprestimo)  #Adiciona esse empréstimo na lista do usuário
                    else:
                        emprestimo_excedente()
                else:
                    item_indisponivel()    
            else:
                senha_invalida()
        else:
            usuario_nao_encontrado()
        self.salvar_itens(CAMINHO_ITENS)
        self.salvar_usuarios(CAMINHO_USUARIOS)

    def devolver(self, usuario, item):
        if usuario in self.usuarios:   #Usuário está na lista de usuários da biblioteca?
            usuario = self.usuarios.get(usuario) #Sim, transforma no objeto usuário
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
        self.salvar_itens(CAMINHO_ITENS)
        self.salvar_usuarios(CAMINHO_USUARIOS)
            
    def cadastrar_livro(self, titulo, autor, disponibilidade):
        novo_item = Livro(titulo, autor, disponibilidade)
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

    def cadastrar_revista(self, titulo, autor, disponibilidade):
        novo_item = Revista(titulo, autor, disponibilidade)
        if novo_item in self.itens:
            item_cadastrado()
        else:
            self.itens.append(novo_item)
        self.salvar_itens(CAMINHO_ITENS)     #Salva o item no módulo JSON

    def cadastrar_usuario(self, novo_usuario, caminho):
        self.usuarios[novo_usuario.nome] = novo_usuario
        self.salvar_itens(CAMINHO_USUARIOS)   #Caminho é fornecido no __main__

    def salvar_usuarios(self, caminho_user):
        lista_usuarios = [] #Lista para adicionar no final
        for usuario in self.usuarios.values():
            titulo_emprestado = [emp.item.titulo for emp in usuario._itens_emprestados if emp.ativo]  
            lista_usuarios.append({ 
                "nome": usuario.nome, #Para o JSON funcionar, precisa estar semelhando ao DICT do python
                "senha": usuario.checagem_senha,    #Transformando em Chave,valor
                "emprestimos_realizados": usuario._emprestimos_realizados,
                "itens_titulo": titulo_emprestado,
            })
        with open(caminho_user, "w", encoding=("utf-8")) as arquivo: #Abre o caminho fornecido, escreve e salva 
            json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)

    def carregar_usuarios(self, caminho_user):
        try:
            with open(caminho_user, "r", encoding=("utf-8")) as arquivo:  #Abre o caminho fornecido, Lê
                lista_dados = json.load(arquivo)    #lista de dados vira o carregamento do JSON

            self.usuarios = {}
            for dados in lista_dados:
                usuario_objeto = Usuario(    #Transformando o usuario em objeto devolta, pois o JSON desfragmenta em DICT
                    nome=dados["nome"],  #Atributo nome = "nome" daquele dado
                    senha_usuario=dados["senha"],  #Atributo semha = "senha" daquele dado
                    tem_hash=True   #Usado para não fazer HASH da HASH
                )
                usuario_objeto._emprestimos_realizados = dados["emprestimos_realizados"]
                if "itens_titulo" in dados:
                    for titulo in dados["itens_titulo"]:
                        for item_objeto in self.itens:
                            if item_objeto.titulo.lower() == titulo.lower():
                                novo_emprestimo = Emprestimo(usuario_objeto, item_objeto, 0, True)
                                self.emprestimos_lista.append(novo_emprestimo)
                                usuario_objeto._itens_emprestados.append(novo_emprestimo)
                                item_objeto.disponibilidade = False
                                break
                self.usuarios[usuario_objeto.nome] = usuario_objeto #O nome do DICT é o nome do objeto
        except FileNotFoundError:
            pass
        except:
            print("ERRO")

    def salvar_itens(self, caminho_item):
        lista_itens = []
        for item in self.itens:
            lista_itens.append({        #Para o JSON funcionar, precisa estar semelhando ao DICT do python
                "tipo": item.tipo,
                "titulo": item.titulo,
                "autor": item.autor,
                "disponibilidade": item.disponibilidade
            })
        with open(caminho_item, "w", encoding=("utf-8")) as arquivo:    #Abre o caminho fornecido, escreve e salva 
            json.dump(lista_itens, arquivo, indent=4, ensure_ascii=False)

    def carregar_itens(self, caminho_item):
        try:
            with open(caminho_item, "r", encoding=("utf-8")) as arquivo: #Abre o arquivo para ler
                lista_dados = json.load(arquivo)    
            self.itens = []
            for dado in lista_dados:
                if dado["tipo"] == "Livro": #Atributo "tipo" é para saber se é um Livro ou Revista
                    item_objeto = Livro(            #Desfragmentamos, transformando DICT em OBJETO novamente
                        titulo = dado["titulo"],
                        autor = dado["autor"],
                        disponibilidade = dado["disponibilidade"],
                    )
                else:
                    item_objeto = Revista(  #Revista dessa vez
                    titulo = dado["titulo"],
                    autor = dado["autor"],
                    disponibilidade = dado["disponibilidade"],
                    )
                self.itens.append(item_objeto)
        except FileNotFoundError:
            pass
        except:
            print("ERRO")