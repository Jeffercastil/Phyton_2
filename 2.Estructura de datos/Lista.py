cantidad=int (input(f" ingresar la cantidad de valores:"))
lista=[]
for i in range (cantidad):
   valor =int(input(f" ingrese el valor {i+1} :"))
   lista.append(valor)
   
if lista:
    total =sum(lista)
    promedio = total / len(lista)
    maximo= max(lista)
    minimo = min (lista)
     
    print(" Resumen estadistico")
    print(f" Total de ventas: {total}")
    print(f"promedio de ventas :{promedio:.2f}")
    print(f"Maximo: {maximo}")
    print(f"Minimo: {minimo}")
else:
    print("No se ingresaron datos")
    
  

