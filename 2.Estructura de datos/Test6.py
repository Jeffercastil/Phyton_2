texto=input("Ingrese un texto:")
palabra=input("Palabra que deseas buscar:")

if palabra.lower() in texto.lower():
   print(f"La palabra: '{palabra}'' si esta en el texto")
else:
     print(f"No se encuentra la palabra '{palabra}'")