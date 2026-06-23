from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

# Modello per i dati di input
class UtenteAuth(BaseModel):
    username: str
    password: str

#Creiamo il mini-gestore delle rotte
router = APIRouter()

import hashlib
import secrets

#funzione per hashare le credenziali
def calcola_hash(password_chiaro: str ) -> str:
    
    # Trasforma il testo in impronta digitale esadecimale illeggibile
    hash_risultato = hashlib.sha256(password_chiaro.encode('utf-8')).hexdigest()

    # Genera una stringa casuale esadecimale di 32 caratteri da usare come pass
    #nuovo_token = secrets.token_hex(16)
    
    return hash_risultato

#def calcola_hash(password_chiaro: str ) -> str:
#    password_bytes = password_chiaro.encode('utf-8')
#    new_token = secrets.token_hex(16)  
#    return hashlib.sha256(password_bytes).hexdigest()


@router.get("/utenti")
def lista_utenti():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utenti")
    risultato = cursor.fetchall()
    conn.close()
    return risultato

@router.get("/utenti/{id_utente}")
def lista_utente_singolo(id_utente: int):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utenti WHERE id = ?", (id_utente,))
    risultato = cursor.fetchone() # fetchone() restituisce None se vuoto
    conn.close()
    
    if risultato is None:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return risultato

# Espongo la chiamata per inserire un nuovo utente

@router.post("/register_utente")
def add_user(dati: UtenteAuth):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Inserisco l'utente nel database con la password hashata
        cursor.execute(
            "INSERT INTO utenti (username, password) VALUES (?, ?)",
            (dati.username, calcola_hash(dati.password))
        )

        conn.commit()

        return {"status": "Utente registrato con successo"}
    
    except sqlite3.IntegrityError:
        # Se l'username è già presente nel database, solleva un'eccezione
        raise HTTPException(
            status_code=400,
            detail="Username già in uso"
        )
    #chiude a prescindere da tutto la connesione al db
    finally:
        conn.close()


@router.post("/login_utente")
def login_user(dati: UtenteAuth):
    hash_da_verificare = calcola_hash(dati.password)
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Recupero l'utente dal database
    cursor.execute(
        "SELECT * FROM utenti WHERE username = ? AND password = ?",
        (dati.username, hash_da_verificare)
    )
    utente = cursor.fetchone()
    conn.close()

    if utente is None or utente[1] != hash_da_verificare:
        conn.close()
        raise HTTPException(
            status_code=401,
            detail="Credenziali non valide"
        )
    
    # Genero il token
    token = secrets.token_hex(16)

    # Salvo il token nel database
    cursor.execute(
        "UPDATE utenti SET token = ? WHERE id = ?",
        (token, utente[0])
    )

    conn.commit()
    conn.close()

    return {
        "status": "Login effettuato con successo",
        "token": token
    }

#rotta protetta dal token
@router.get("/profile_utente")
def profile_user(token: str): #FastAPI cattura il token dall'url(?token= ...)
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, username FROM utenti WHERE token = ?", (token,))
    utente = cursor.fetchone()
    conn.close()

    if utente is None:
        raise HTTPException(status_code=401, detail="Token non valido")

