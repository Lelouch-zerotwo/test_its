from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/utente")
def root():
    return {"nome": "angelo", "cognome": "bachetti"}
#chiamata
#https://obscure-space-spork-9677gq7jr7rj37j4w-8000.app.github.dev/utente

@app.get("/saluta/{name}")
def saluta_utente(name: str):
    return {"saluto": f"Banvenuto {name}!"}
#chiamata
#https://obscure-space-spork-9677gq7jr7rj37j4w-8000.app.github.dev/saluta/Antonio

@app.get("/ricerca")
def cerca(item: str, q: int = 1):
    return {"risultato": item, "quantita": q}
#chiamata
#https://obscure-space-spork-9677gq7jr7rj37j4w-8000.app.github.dev/ricerca?item="cocco"&q=10

@app.get("/somma/{num1}/{num2}")
def somma(num1: int = 0, num2: int = 0):
    return {"risultato": f"{num1+num2}"}
#chiamata
#https://obscure-space-spork-9677gq7jr7rj37j4w-8000.app.github.dev/somma/10/1100

@app.get("/calcola")
def calcola(operazione: str, num1: int, num2: int):
        match operazione:
            #"..." se nell'url e'-> .../calcola?operazione=divisione&... 
            case "somma":
                return {"risultato": f"{num1 + num2}"}
            case "sottrazione":
                return {"risultato": f"{num1 - num2}"}
            case '"moltiplicazione"':
                return {"risultato": f"{num1 * num2}"}
            #'"..."' se nell'url e'-> .../calcola?operazione=%22divisione%22&... --> %22...%22 == "..."(doppie-virgolette) 
            case '"divisione"':
                if num2 == 0:
                    return {"errore": "Divisione per zero non si può fare"}
                else:
                    return {"risultato": f"{num1 / num2}"}
            case _:
                raise HTTPException(status_code=400, detail="Operazione non valida")
#chiamata
#https://obscure-space-spork-9677gq7jr7rj37j4w-8000.app.github.dev/calcola?operazione=%22divisione%22&num1=10&num2=0
#https://obscure-space-spork-9677gq7jr7rj37j4w-8000.app.github.dev/calcola?operazione=sottrazione&num1=10&num2=0