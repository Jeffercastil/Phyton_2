palabra =input ("Ingresa una palabra: ")
contador = 0
for letra in palabra:
    if letra.lower() in "aeiu":
        contador +=1
        print (f"Lá palabra tiene: ", contador," vocales")