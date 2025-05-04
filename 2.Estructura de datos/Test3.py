n=int(input("Cuantos clientes desea agregar?"))
clientes=[]

for i in range(n):
  print(f"\Ingresar datos del cliente {i+1}")
  nombre=input("Nombre:")
  Compras=int(input("Numeros de compras: "))
  gasto_total=float(input("Gasto total:"))
  
  cliente.append({
    "id":i+1,
    "Nombre",nombre,
    "Compras",Compras,
    "Gasto total",gasto_total
  })
  
  print("\nResumen de clientes:")
  for cliente in clientes:
    gasto_promedio=
    cliente['gasto_total']/cliente['compras']
    print(f"{cliente['Nombre']}:
      {cliente['compras']}compras,"f"Gastos total:${ cliente['gasto_total']:.2f},"f"Promedio:${gasto_promedio:.2f} por comprar ")
    