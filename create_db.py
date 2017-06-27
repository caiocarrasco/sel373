import sqlite3

conn = sqlite3.connect('database.db')
print("Banco de dados aberto")

conn.execute('CREATE TABLE CLIENTS (NAME TEXT, PSWD TEXT)')
print("Tabela de clientes foi criada")

conn.execute('CREATE TABLE PLATES (PLATE TEXT, NAME TEXT, LOG TEXT)')
print("Tabela de placas foi criada")

conn.close()
