import sqlite3

conn = sqlite3.connect("db_test.db")
cursor = conn.cursor()

#i tre doppi apici indicano che tutto ciò che sta al suo interno è tutta una variabile strigna
cursor.execute("""
    CREATE TABLE IF NOT EXISTS prodotti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        prezzo REAL
    )
""")

#fondamentale quando si va a manipolare i dati altrimenti il comando rimane in memoria ma non viene eseguito 
#e al prossio avvio la query si cancellerebbe
conn.commit()

#
#
#
#
#1.preparazione in RAM
cursor.execute(
    "INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)", 
    ("prodotto1", 10.99)
)

#2.scrittura su file(Hard Disk)
conn.commit()

#inserimento di più prodotti

lista_prodotti = [
    ("Mouse Wireless", 25.99),
    ("Tastiera Meccanica", 79.99),
    ("Monitor 24 pollici", 149.99),
    ("Cuffie Gaming", 59.99),
    ("Tappetino XL", 39.99)
]

cursor.executemany(
    "INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)", 
    lista_prodotti
    #"DELETE FROM prodotti WHERE nome = ? AND prezzo = ?",
    #lista_prodotti
)
conn.commit()


# Creazione di una tupla
prodotto_tupla = (1, "Mouse Wireless", 25.50)
# Accesso per indice numerico
print(prodotto_tupla[1]) # Mouse Wireless


conn.close()