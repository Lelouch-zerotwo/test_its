print("Hello wolrd!")

#somma
def somma(x, y):
    return x + y

#questi due print sono la stessa cosa
print("Risultato somma: " + somma(1, 2))
print(f"Risultato somma: {somma(1, 2)}") #la f sta a dire che la stringa può contenere una funzione


#differenza restituisce solo positivi
def diff(x, y):
    if(x > y):
        return x-y
    else :
        return y-x

print(f"Risultato differenza: {diff(5, 6)}")

#moltiplicazione
def moltiplicazione(x, y):
    return x * y

print(f"Risultato moltiplicazione: {moltiplicazione(3, 4)}")

#divisione
def divisione(x, y):
    if(y == 0):
        return print("Non si pu0' dividere per 0")
    else:
        return x / y
    
#radice di un numero
def sqrt_num(x):
    return x * 0.5