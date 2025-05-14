conjunto_a=[]
conjunto_b=[]

ta=int(input("cuantos valores de A deseas agregar"))

for i in range(ta):
  va =float(input(f"Ingresar valores de A :{i+1}"))
  conjunto_a.append(va)
  
tb=int(input("Cuantos valores de B desea agregar"))

for i in range(tb):
  vb=float(input(f"Ingresar valores de B : {i+1}"))
  conjunto_b.append(vb)
  
print(f"los valores del rango A es: {conjunto_a} ,Los valores de B:{conjunto_b}")

set1=set(conjunto_a)
set2=set(conjunto_b)
comunes= set1 & set2
print(f" Los valores que hay en comun son : {comunes}")

  