n=int(input("Cuantos registros de ventas deseas agregar:"))
ventas_categorias=[]

for i in range(n):
  print(f"\nRegistro {1+i}")
  categoria=input("Categoria/Electronico/Ropa/Alimentos/Otros").capitalize()
  monto=float(input("Monto de ventas en:$"))
  ventas_categorias.append([categoria,monto])
  
 total_por_categoria={}
 
 for categoria, monto in
 
