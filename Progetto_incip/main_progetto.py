from fastapi import FastAPI
from db_progetto import dbinit
from prodotti_progetto import router as prodotti_router


#inizializzazione del db
dbinit()

# Dichiaro FastAPI
app = FastAPI()

app.include_router(prodotti_router)

# Creo una chiamata base di benvenuto
@app.get("/")
def root():
    return {"messaggio/info": "Benvenuto!/Server principale attivo"}