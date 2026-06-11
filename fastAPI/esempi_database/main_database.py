from fastapi import FastAPI
#import uso_database.py
import sqlite3

app = FastAPI()

#controlla l'url ci deve essere /prodotti per vedere i prodotti
#es
#https://obscure-space-spork-9677gq7jr7rj37j4w-8000.app.github.dev --> (risultato) {"detail":"Not Found"}
#https://obscure-space-spork-9677gq7jr7rj37j4w-8000.app.github.dev/prodotti --> (risultato) tabella prodotti
@app.get("/prodotti")
def ottieni_prodotti():
    conn = sqlite3.connect("db_test.db")
    conn.row_factory = sqlite3.Row # Conversione attiva!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    risultato = cursor.fetchall()
    conn.close()
    return risultato

@app.get("/prodotti/ricerca")
def ottieni_prodotti(item: str):
    conn = sqlite3.connect("db_test.db")
    conn.row_factory = sqlite3.Row # Conversione attiva!
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM prodotti WHERE nome LIKE ?",
        (f"%{item}%",)
    )
    risultato = cursor.fetchall()
    conn.close()
    return risultato
#url --> https://obscure-space-spork-9677gq7jr7rj37j4w-8000.app.github.dev/prodotti/ricerca?item=ous
#risultato --> [{"id": 1, "nome": "Mouse Wireless", "prezzo": 25.99}]