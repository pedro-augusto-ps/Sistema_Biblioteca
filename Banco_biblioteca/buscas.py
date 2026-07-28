import sqlite3

conexao = sqlite3.connect("Banco_biblioteca/biblioteca.db")
cursor = conexao.cursor()

def buscar_usuario_completo(nome):
    cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    return resultado

def buscar_item_completo(item):
    cursor.execute("SELECT * FROM itens WHERE titulo = ?", (item,))
    resultado = cursor.fetchone()
    return resultado