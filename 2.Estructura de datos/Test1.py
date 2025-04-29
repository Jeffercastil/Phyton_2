n = int (input ("Cuantos dias de ventas desea analizar: "))
ventas={}

for i in range (n):
  valor = float(input(f"ingresa ventas del dia {i+1}"))
  ventas.appned(valor)
  
  if ventas:
    total=sum(ventas)
    promedio = total / len(ventas)
    maximo = max(ventas)
    minimo = min(ventas)
    
    print("\Resumen estadistico")
    print(f" Valor total : {total}")
    print(f"El promedio es: {promedio:.2f}")
    print(f"El valor maximo es: {maximo}")
    print(f"El valor minimo es:{minimo}")
  else:
    print("No hay datos")
    
