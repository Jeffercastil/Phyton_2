texto =input("Ingresa un texto").lower()
palabra=input("Que palabra deseas buscar? ").lower()

veces = texto.count(palabra)
if veces > 0:
  print(f" la palabra aparece {veces} vez/veces")
else:
  print(f"la palabra {palabra} no fue encontrada")
  

