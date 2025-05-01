n=int(input("cuantas temperaturas deseas ingresar:"))
temperaturas=[]
for i in range(n):
 temp=float(input(f"ingresa temperatura {i+1} :"))
 temperaturas.append(temp)

 umbral=float(input("\Ingrese el umbral para temperaturas altas :"))
 altas_temperaturas=[temp for temp in temperaturas if temp >umbral ]

print ("\Resultados:")
print(f"Temperaturas orinales:{Temperaturas}")
print(f"Temperaturas mayores :{Temperaturas}")


