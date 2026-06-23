from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

# Modello per i dati di input
class ProdottoIn(BaseModel):
    nome: str
    prezzo: float

#Creiamo il mini-gestore delle rotte
router = APIRouter()

@router.get("/prodotti")
def lista_prodotti():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    risultato = cursor.fetchall()
    conn.close()
    return risultato


@router.get("/prodotti/{id_prodotto}")
def lista_prodotto_singolo(id_prodotto: int):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti WHERE id = ?", (id_prodotto,))
    risultato = cursor.fetchone() # fetchone() restituisce None se vuoto
    conn.close()
    
    if risultato is None:
        raise HTTPException(status_code=404, detail="Prodotto non trovato")
    return risultato



# Espongo la chiamata per inserire un nuovo prodotto
@router.post("/prodotti", status_code=201)
def crea_prodotto(dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)", (dati.nome, dati.prezzo))
    conn.commit()
    conn.close()
    return {"status": "Prodotto registrato con successo"}

# Espongo la chiamata per modificare un prodotto
@router.put("/prodotti/{id_prodotto}") 
def aggiorna_prodotto(id_prodotto: int, dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Verifico se il prodotto richiesto esiste
    cursor.execute("SELECT * FROM prodotti WHERE id = ?", (id_prodotto,))
    risultato = cursor.fetchone()
    if risultato is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato")
    
    cursor.execute("UPDATE prodotti SET nome = ?, prezzo = ? WHERE id = ?", (dati.nome, dati.prezzo, id_prodotto))
    conn.commit()
    conn.close()
    return {"status": "Modifica salvata"}

# Espongo la chiamata per cancellare un prodotto
@router.delete("/prodotti/{id_prodotto}")
def elimina(id_prodotto: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Verifico se il prodotto richiesto esiste
    cursor.execute("SELECT * FROM prodotti WHERE id = ?", (id_prodotto,))
    risultato = cursor.fetchone()
    if risultato is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato")
    
    cursor.execute("DELETE FROM prodotti WHERE id=?", (id_prodotto,))
    conn.commit()
    conn.close()
    return {"status": "Cancellato"}

    
    cursor.execute("DELETE FROM prodotti WHERE id=?", (id_prodotto,))
    conn.commit()
    conn.close()
    return {"status": "Cancellato"}